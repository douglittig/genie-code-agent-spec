"""define.py — gate do Define, por código e não de memória.

Roda ANTES de apresentar a spec ao usuário e de novo, com --aprovado, antes do
Build. Lê só o DEFINE_*.md (markdown), nunca o código do projeto.

Erros (exit 1):
  - falta uma seção obrigatória
  - "Pedido original" vazio no Registro do pedido e das respostas; ID Qn.m repetido
  - "Fora do escopo" vazio
  - nenhum critério de aceite, ID malformado ou repetido, critério fora do requisito dele
  - critério sem DEVE (ou SHALL): não é testável no formato EARS
  - dimensão de requisito implícito ausente, vazia ou apontando para critério ou Qn.m inexistente
  - tabela sem uma coluna do template (Registro, rubrica, Suposições, Diferenças,
    Rastreabilidade): o gate não pula tabela com cabeçalho trocado
  - Suposições fora de tabela (lista ou texto) que não seja "Nenhuma."
  - suposição sem "Padrão escolhido" ou sem "Motivo"
  - suposição com origem fora das três aceitas; "código" sem o caminho do arquivo;
    "usuário delegou" ou "não quis discutir" sem o Qn.m ou a frase do usuário
  - diferença em relação à fonte sem "Aprovado por"
  - critério sem linha na Rastreabilidade, ou linha de rastreabilidade de critério inexistente
  - origem de critério que não aponta para pedido, Qn.m, Confluence, ticket, rubrica ou área cinzenta
  - Qn.m citado que não está no Registro; frase entre aspas que não está no pedido ou na linha Qn.m
  - com --aprovado: sem linha **Aprovado** com as palavras do usuário, pergunta em aberto,
    pergunta do Registro sem resposta, ou dimensão implícita sem destino
Avisos (exit 1 só com --estrito):
  - {placeholder} do template que sobrou
  - critério com termo vago sem número (rápido, adequado, eficiente…)
  - SE sem ENTÃO (padrão de comportamento indesejado incompleto)
  - dimensão implícita que não diz para onde foi (antes da aprovação)
  - pergunta em aberto, ou pergunta do Registro sem resposta (antes da aprovação)
  - trecho do pedido original que nenhuma origem cita

Uso:
  python3 -m sdd_gates define docs/specs/DEFINE_<FEATURE>.md [--aprovado] [--estrito]

Códigos de saída: 0 ok, 1 o DEFINE não passou, 2 erro de uso.
"""

import argparse
import re
import sys
from pathlib import Path

from . import md

REGISTRO = "Registro do pedido e das respostas"

SECOES = [
    "Fontes",
    REGISTRO,
    "Problema",
    "Escopo",
    "Requisitos",
    "Requisitos implícitos de dados",
    "Suposições",
    "Perguntas em aberto",
    "Rastreabilidade",
    "Aprovação",
]

DIMENSOES = [
    "Idempotência e reprocessamento",
    "Dado atrasado ou fora de ordem",
    "Duplicidade",
    "Evolução de schema",
    "Backfill e carga histórica",
    "Qualidade",
    "Falha parcial e retomada",
    "PII, grants e Unity Catalog",
    "Freshness e SLA",
    "Volume, custo e compute",
    "Observabilidade e alerta",
]

# Raízes (texto já sem acento): cobrem gênero, plural e advérbio (rápido, rápida, rapidamente…)
TERMOS_VAGOS = [
    r"rapid\w*", r"adequad\w*", r"eficient\w*", r"otimizad\w*", r"robust\w*",
    r"aceitave\w*", r"razoave\w*", r"melhor\w*", r"em tempo habil", r"quando possivel",
    r"o quanto antes",
]

# Origens aceitas para uma suposição (texto normalizado, sem acento)
ORIGENS_SUPOSICAO = ("codigo", "usuario delegou", "usuario nao quis discutir")

REQ_RE = re.compile(r"^###\s+(R\d+)\s*:")
CRIT_RE = re.compile(r"^\s*[-*]\s+\*\*(R\d+\.\d+)\*\*\s*(.*)$")
ID_CRIT_RE = re.compile(r"\bR\d+\.\d+\b")
QID_RE = re.compile(r"\bQ\d+\.\d+\b", re.I)
DEVE_RE = re.compile(r"\b(DEVE|SHALL)\b")
SE_RE = re.compile(r"^\s*(SE|IF)\b")
ENTAO_RE = re.compile(r"\b(ENTÃO|ENTAO|THEN)\b")
DESTINO_RE = re.compile(r"\bR\d+\.\d+\b|fora do escopo|\bS-\d+\b|nao se aplica|\bQ\d+\.\d+\b", re.I)
LISTA_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+(\S.*)$")
CITACAO_RE = re.compile(r'["“]([^"“”]{2,})["”]')
TIPO_ORIGEM_RE = re.compile(r"\bpedido\b|confluence|\bticket\b|\bjira\b|rubrica|area cinzenta|\bq\d+\.\d+\b")
CAMINHO_RE = re.compile(r"[\w.-]+/[\w./-]*|\b[\w-]+\.(?:py|sql|ya?ml|json|toml|md|ipynb|cfg|txt)\b")
ELIPSE_RE = re.compile(r"\(?(?:\.\.\.|…)\)?")


def itens_de_lista(linhas):
    """Itens de lista com marcador (-, *) ou numerados (1., 2))."""
    return [m.group(1).strip() for linha in linhas for m in [LISTA_RE.match(linha)] if m]


def texto_solto(linhas):
    """Linhas com conteúdo que não são título, tabela, citação nem separador."""
    return [l.strip() for l in linhas if l.strip() and not l.strip().startswith(("#", "|", ">", "---"))]


def partes_da_origem(texto):
    """Divide a origem em partes por ';', sem quebrar dentro de parênteses ou aspas."""
    partes, atual, nivel, aspas = [], "", 0, False
    for ch in texto:
        if ch in '"“”':
            aspas = not aspas
        elif ch == "(" and not aspas:
            nivel += 1
        elif ch == ")" and not aspas and nivel:
            nivel -= 1
        if ch == ";" and nivel == 0 and not aspas:
            partes.append(atual)
            atual = ""
        else:
            atual += ch
    partes.append(atual)
    return [p.strip() for p in partes if p.strip()]


def citacao_esta_em(citacao, fonte):
    """A frase citada (aceita '...' no meio) aparece na fonte, ignorando acento e caixa."""
    fonte_n = md.normaliza(fonte)
    pedacos = [md.normaliza(p).strip(" .,;:!?") for p in ELIPSE_RE.split(citacao)]
    return all(p in fonte_n for p in pedacos if p)


def trechos_do_pedido(pedido):
    """Trechos do pedido (frases e orações separadas por vírgula) com 3 palavras ou mais."""
    sem_mencao = re.sub(r"@[\w-]+", " ", pedido)
    trechos = [t.strip(" \"“”'") for t in re.split(r"[.!?;,\n]+", sem_mencao)]
    return [t for t in trechos if len(t.split()) >= 3]


def le_registro(linhas, rel, aprovado):
    """Devolve (texto do pedido original, {Qn.m: texto da linha}) e valida o Registro."""
    reg = md.secao(linhas, REGISTRO, nivel=2)
    if reg is None:
        return "", {}
    ped = md.secao(reg, "Pedido original", nivel=3) or []
    pedido = " ".join(l.strip().lstrip(">").strip() for l in ped if l.strip().startswith(">"))
    if md.vazia(pedido) or md.PLACEHOLDER_RE.search(pedido):
        rel.erro(f"'### Pedido original' vazio: cole o pedido do usuário, literal, como citação (> …), dentro de '## {REGISTRO}'")
    perguntas = {}
    for cab, dados in md.tabelas(reg):
        cols = colunas(cab, ["ID", "Resposta"], REGISTRO, rel)
        if cols is None:
            continue
        ci, cr = cols
        for row in dados:
            qid = row[ci].strip("* ").upper() if ci < len(row) else ""
            if not QID_RE.fullmatch(qid):
                continue
            if qid in perguntas:
                rel.erro(f"Registro: {qid} repetido")
            perguntas[qid] = " | ".join(row)
            resposta = row[cr] if cr < len(row) else ""
            if md.vazia(resposta) or md.PLACEHOLDER_RE.search(resposta) or md.normaliza(resposta).startswith("aguardando"):
                (rel.erro if aprovado else rel.aviso)(f"Registro: {qid} sem resposta do usuário")
    return pedido, perguntas


def colunas(cab, nomes, onde, rel):
    """Índices das colunas que o gate lê. Se faltar alguma, é erro: tabela com cabeçalho
    trocado não pode passar sem ser conferida. Devolve None nesse caso."""
    idx = [md.coluna(cab, n) for n in nomes]
    faltam = [n for n, i in zip(nomes, idx) if i is None]
    if faltam:
        rotulo = "a coluna" if len(faltam) == 1 else "as colunas"
        rel.erro(f"{onde}: tabela sem {rotulo} {', '.join(repr(n) for n in faltam)}; "
                 "use as colunas do template, sem renomear nem juntar")
        return None
    return idx


def confere_qids(texto, perguntas, onde, rel):
    for q in QID_RE.findall(texto):
        if q.upper() not in perguntas:
            rel.erro(f"{onde} cita {q.upper()}, que não está no '{REGISTRO}'")


def valida(caminho, aprovado=False):
    rel = md.Relatorio(f"sdd_gates define {caminho.name}")
    linhas = md.prepara(caminho.read_text(encoding="utf-8"))

    # 1. Seções obrigatórias
    for nome in SECOES:
        if md.secao(linhas, nome, nivel=2) is None:
            rel.erro(f"falta a seção '## {nome}'")

    # 2. Registro do pedido e das respostas: o pedido literal e cada pergunta com resposta
    pedido, perguntas = le_registro(linhas, rel, aprovado)

    # 3. Escopo: "Fora do escopo" precisa existir e ter conteúdo
    fora = md.secao(linhas, "Fora do escopo", nivel=3)
    itens_fora = [i for i in itens_de_lista(fora or []) if not md.vazia(i)]
    if fora is None or not itens_fora:
        rel.erro("'### Fora do escopo' vazio: liste o que fica de fora de propósito")

    # 4. Requisitos e critérios
    reqs = md.secao(linhas, "Requisitos", nivel=2) or []
    criterios, req_atual = {}, None
    for linha in reqs:
        m = REQ_RE.match(linha)
        if m:
            req_atual = m.group(1)
            continue
        c = CRIT_RE.match(linha)
        if not c:
            continue
        cid, texto = c.groups()
        if cid in criterios:
            rel.erro(f"critério {cid} repetido")
        criterios[cid] = texto
        if req_atual is None or not cid.startswith(req_atual + "."):
            rel.erro(f"critério {cid} fora do requisito dele (deveria estar sob '### {cid.split('.')[0]}: …')")
        if not DEVE_RE.search(texto):
            rel.erro(f"critério {cid} sem DEVE: escreva no formato EARS (ex.: QUANDO … ENTÃO o pipeline DEVE …)")
        if SE_RE.match(texto) and not ENTAO_RE.search(texto):
            rel.aviso(f"critério {cid} começa com SE e não tem ENTÃO")
        texto_n = md.normaliza(texto)
        vagos = [m.group(0) for t in TERMOS_VAGOS for m in [re.search(rf"\b{t}\b", texto_n)] if m]
        if vagos and not re.search(r"\d", texto):
            rel.aviso(f"critério {cid} usa termo vago sem número ({', '.join(vagos)}): diga o valor esperado")
    if not criterios:
        rel.erro("nenhum critério de aceite: use '- **R1.1** QUANDO … ENTÃO o pipeline DEVE …' sob '### R1: …'")

    # 5. Requisitos implícitos de dados: toda dimensão presente e com destino
    impl = md.secao(linhas, "Requisitos implícitos de dados", nivel=2)
    if impl is not None:
        vistos = {}
        for cab, dados in md.tabelas(impl):
            cols = colunas(cab, ["Dimensão", "Como fica"], "Requisitos implícitos de dados", rel)
            if cols is None:
                continue
            cd, cc = cols
            for row in dados:
                if len(row) > max(cd, cc):
                    vistos[md.normaliza(row[cd])] = row[cc]
        for dim in DIMENSOES:
            chave = next((k for k in vistos if k.startswith(md.normaliza(dim))), None)
            if chave is None:
                rel.erro(f"requisitos implícitos: falta a dimensão '{dim}'")
                continue
            valor = vistos[chave]
            if md.vazia(valor) or md.PLACEHOLDER_RE.search(valor):
                rel.erro(f"requisitos implícitos: '{dim}' sem destino")
                continue
            for ref in ID_CRIT_RE.findall(valor):
                if ref not in criterios:
                    rel.erro(f"requisitos implícitos: '{dim}' aponta para {ref}, que não existe")
            confere_qids(valor, perguntas, f"requisitos implícitos: '{dim}'", rel)
            valor_n = md.normaliza(valor)
            if not DESTINO_RE.search(valor_n):
                motivo = ("aguarda uma pergunta em aberto" if "pergunta em aberto" in valor_n else
                          "não diz para onde foi (critério, fora do escopo, S-n, decisão em Qn.m ou 'não se aplica: motivo')")
                (rel.erro if aprovado else rel.aviso)(f"requisitos implícitos: '{dim}' {motivo}")

    # 6. Suposições: padrão, motivo e uma origem verificável
    sup = md.secao(linhas, "Suposições", nivel=2)
    if sup is not None and not md.tabelas(sup):
        soltas = [l for l in texto_solto(sup) if not md.normaliza(l).strip("-*_ ").startswith("nenhuma")]
        if soltas or not texto_solto(sup):
            rel.erro("Suposições: use a tabela do template (ID, Padrão escolhido, Motivo, Origem, "
                     "Se estiver errada) ou escreva 'Nenhuma.'")
    for cab, dados in md.tabelas(sup or []):
        cols = colunas(cab, ["ID", "Padrão escolhido", "Motivo", "Origem"], "Suposições", rel)
        if cols is None:
            continue
        cid, cp, cm, co = cols
        for row in dados:
            nome = row[cid] if cid < len(row) else "?"
            if cp >= len(row) or md.vazia(row[cp]):
                rel.erro(f"suposição {nome} sem 'Padrão escolhido'")
            if cm >= len(row) or md.vazia(row[cm]):
                rel.erro(f"suposição {nome} sem 'Motivo'")
            origem = row[co] if co < len(row) else ""
            origem_n = md.normaliza(origem)
            tipo = next((o for o in ORIGENS_SUPOSICAO if origem_n.startswith(o)), None)
            if tipo is None:
                rel.erro(f"suposição {nome}: origem '{origem[:40]}' não vale; use 'código: <arquivo>', "
                         "'usuário delegou (Qn.m)' ou 'usuário não quis discutir (Qn.m)'. Decisão do usuário não é suposição")
            elif tipo == "codigo" and not CAMINHO_RE.search(origem):
                rel.erro(f"suposição {nome}: origem 'código' sem o caminho do arquivo que mostra o padrão")
            elif tipo != "codigo" and not (QID_RE.search(origem) or CITACAO_RE.search(origem)):
                rel.erro(f"suposição {nome}: origem '{origem[:40]}' sem o Qn.m ou a frase do usuário")
            confere_qids(origem, perguntas, f"suposição {nome}", rel)

    # 7. Diferenças em relação à fonte: cada uma aprovada pelo usuário
    dif = md.secao(linhas, "Diferenças em relação à fonte", nivel=2) or []
    for cab, dados in md.tabelas(dif):
        cols = colunas(cab, ["O que a fonte diz", "Aprovado por"], "Diferenças em relação à fonte", rel)
        if cols is None:
            continue
        cf, ca = cols
        for row in dados:
            if ca >= len(row) or md.vazia(row[ca]):
                rel.erro(f"diferença em relação à fonte sem 'Aprovado por': {row[cf][:60] if cf < len(row) else '?'}")

    # 8. Rastreabilidade: um para um com os critérios, e cada origem verificável
    ras = md.secao(linhas, "Rastreabilidade", nivel=2)
    citacoes_do_pedido = []
    if ras is not None:
        origem = {}
        for cab, dados in md.tabelas(ras):
            cols = colunas(cab, ["Critério", "Origem"], "Rastreabilidade", rel)
            if cols is None:
                continue
            cc, co = cols
            for row in dados:
                if len(row) > max(cc, co):
                    origem[row[cc].strip("* ")] = row[co]
        for cid in criterios:
            if cid not in origem:
                rel.erro(f"critério {cid} sem linha na Rastreabilidade")
            elif md.vazia(origem[cid]) or md.PLACEHOLDER_RE.search(origem[cid]):
                rel.erro(f"critério {cid} sem origem na Rastreabilidade")
        for cid, texto in origem.items():
            if ID_CRIT_RE.fullmatch(cid) and cid not in criterios:
                rel.erro(f"Rastreabilidade cita {cid}, que não existe nos Requisitos")
            if md.vazia(texto) or md.PLACEHOLDER_RE.search(texto):
                continue
            confere_qids(texto, perguntas, f"origem de {cid}", rel)
            for parte in partes_da_origem(texto):
                parte_n = md.normaliza(parte)
                if not TIPO_ORIGEM_RE.search(parte_n):
                    rel.erro(f"origem de {cid}: '{parte[:50]}' não aponta para pedido, Qn.m, Confluence, "
                             "ticket, rubrica ou área cinzenta")
                    continue
                citadas = CITACAO_RE.findall(parte)
                qids = [q.upper() for q in QID_RE.findall(parte) if q.upper() in perguntas]
                if qids:
                    fonte, nome_fonte = " ".join(perguntas[q] for q in qids), ", ".join(qids)
                elif re.search(r"\bpedido\b", parte_n):
                    fonte, nome_fonte = pedido, "pedido original"
                    citacoes_do_pedido += citadas
                else:
                    continue  # Confluence, ticket, rubrica: o gate não tem a fonte para conferir
                for c in citadas:
                    if not citacao_esta_em(c, fonte):
                        rel.erro(f"origem de {cid}: a frase \"{c[:50]}\" não está em {nome_fonte}")

    # 9. Pedido frase a frase: todo trecho do pedido original é citado em algum lugar
    if pedido:
        abertas_txt = "\n".join(md.secao(linhas, "Perguntas em aberto", nivel=2) or [])
        citacoes = citacoes_do_pedido + CITACAO_RE.findall("\n".join(fora or []) + "\n" + abertas_txt)
        for trecho in trechos_do_pedido(pedido):
            t = md.normaliza(trecho)
            if not any((c := md.normaliza(x).strip(" .,;:!?")) and (c in t or t in c) for x in citacoes):
                rel.aviso(f"trecho do pedido sem destino: \"{trecho[:60]}\" (cite com pedido: \"…\" na "
                          "Rastreabilidade ou em Fora do escopo, ou pergunte)")

    # 10. Perguntas em aberto (lista com -, * ou numerada; ou texto solto)
    perguntas_abertas = md.secao(linhas, "Perguntas em aberto", nivel=2) or []
    itens = itens_de_lista(perguntas_abertas) or texto_solto(perguntas_abertas)
    abertas = [p for p in itens if not md.normaliza(p).strip("*_ ").startswith("nenhuma")]
    for p in abertas:
        (rel.erro if aprovado else rel.aviso)(f"pergunta em aberto: {p[:80]}")

    # 11. Aprovação (só com --aprovado)
    if aprovado:
        ap = md.secao(linhas, "Aprovação", nivel=2) or []
        if not md.aprovacoes(ap):
            rel.erro('sem aprovação: grave **Aprovado**: AAAA-MM-DD — usuário: "<palavras dele>" (só se o usuário aprovou)')

    # 12. Placeholders que sobraram
    for n in md.placeholders(linhas):
        rel.aviso(f"linha {n}: placeholder do template não preenchido")

    return rel


def main(argv=None):
    p = argparse.ArgumentParser(prog="python3 -m sdd_gates define", description="Gate do Define (DEFINE_*.md).")
    p.add_argument("arquivo", help="caminho do DEFINE_<FEATURE>.md")
    p.add_argument("--aprovado", action="store_true",
                   help="gate antes do Build: exige aprovação, nenhuma pergunta aberta e toda dimensão com destino")
    p.add_argument("--estrito", action="store_true", help="avisos também reprovam")
    a = p.parse_args(argv)
    caminho = Path(a.arquivo)
    if not caminho.is_file():
        print(f"arquivo não encontrado: {caminho}", file=sys.stderr)
        return 2
    return valida(caminho, aprovado=a.aprovado).imprime_e_sai(estrito=a.estrito)


if __name__ == "__main__":
    sys.exit(main())
