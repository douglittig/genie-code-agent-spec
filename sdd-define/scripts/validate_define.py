"""validate_define.py — gate do Define, por código e não de memória.

Roda ANTES de apresentar a spec ao usuário e de novo, com --aprovado, antes do
Build. Lê só o DEFINE_*.md (markdown), nunca o código do projeto.

Erros (exit 1):
  - falta uma seção obrigatória
  - "Fora do escopo" vazio
  - nenhum critério de aceite, ID malformado ou repetido, critério fora do requisito dele
  - critério sem DEVE (ou SHALL): não é testável no formato EARS
  - dimensão de requisito implícito ausente, vazia ou apontando para critério inexistente
  - suposição sem "Padrão escolhido" ou sem "Motivo"
  - diferença em relação à fonte sem "Aprovado por"
  - critério sem linha na Rastreabilidade, ou linha de rastreabilidade de critério inexistente
  - com --aprovado: sem linha **Aprovado** com as palavras do usuário, ou pergunta em aberto
Avisos (exit 1 só com --estrito):
  - {placeholder} do template que sobrou
  - critério com termo vago sem número (rápido, adequado, eficiente…)
  - SE sem ENTÃO (padrão de comportamento indesejado incompleto)
  - dimensão implícita que não diz para onde foi (critério, fora do escopo, suposição ou não se aplica)
  - pergunta em aberto (antes da aprovação é normal; com --aprovado vira erro)

Uso:
  python3 <pasta-da-skill>/scripts/validate_define.py docs/specs/DEFINE_<FEATURE>.md [--aprovado] [--estrito]

Códigos de saída: 0 ok, 1 o DEFINE não passou, 2 erro de uso.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "sdd-workflow" / "scripts"))
import sdd_md as md  # noqa: E402

SECOES = [
    "Fontes",
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

REQ_RE = re.compile(r"^###\s+(R\d+)\s*:")
CRIT_RE = re.compile(r"^\s*[-*]\s+\*\*(R\d+\.\d+)\*\*\s*(.*)$")
ID_CRIT_RE = re.compile(r"\bR\d+\.\d+\b")
DEVE_RE = re.compile(r"\b(DEVE|SHALL)\b")
SE_RE = re.compile(r"^\s*(SE|IF)\b")
ENTAO_RE = re.compile(r"\b(ENTÃO|ENTAO|THEN)\b")
DESTINO_RE = re.compile(r"\bR\d+\.\d+\b|fora do escopo|\bS-\d+\b|nao se aplica", re.I)


def itens_de_lista(linhas):
    return [l.strip()[2:].strip() for l in linhas if re.match(r"^\s*[-*]\s+\S", l)]


def valida(caminho, aprovado=False):
    rel = md.Relatorio(f"validate_define {caminho.name}")
    linhas = md.prepara(caminho.read_text(encoding="utf-8"))

    # 1. Seções obrigatórias
    for nome in SECOES:
        if md.secao(linhas, nome, nivel=2) is None:
            rel.erro(f"falta a seção '## {nome}'")

    # 2. Escopo: "Fora do escopo" precisa existir e ter conteúdo
    fora = md.secao(linhas, "Fora do escopo", nivel=3)
    itens_fora = [i for i in itens_de_lista(fora or []) if not md.vazia(i)]
    if fora is None or not itens_fora:
        rel.erro("'### Fora do escopo' vazio: liste o que fica de fora de propósito")

    # 3. Requisitos e critérios
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

    # 4. Requisitos implícitos de dados: toda dimensão presente e com destino
    impl = md.secao(linhas, "Requisitos implícitos de dados", nivel=2)
    if impl is not None:
        vistos = {}
        for cab, dados in md.tabelas(impl):
            cd, cc = md.coluna(cab, "Dimens"), md.coluna(cab, "Como fica")
            if cd is None or cc is None:
                continue
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
            if not DESTINO_RE.search(md.normaliza(valor)):
                rel.aviso(f"requisitos implícitos: '{dim}' não diz para onde foi (critério, fora do escopo, S-n ou 'não se aplica: motivo')")

    # 5. Suposições: padrão e motivo preenchidos
    sup = md.secao(linhas, "Suposições", nivel=2) or []
    for cab, dados in md.tabelas(sup):
        cid, cp, cm = md.coluna(cab, "ID"), md.coluna(cab, "Padrao escolhido"), md.coluna(cab, "Motivo")
        if cp is None or cm is None:
            continue
        for row in dados:
            nome = row[cid] if cid is not None and cid < len(row) else "?"
            if cp >= len(row) or md.vazia(row[cp]):
                rel.erro(f"suposição {nome} sem 'Padrão escolhido'")
            if cm >= len(row) or md.vazia(row[cm]):
                rel.erro(f"suposição {nome} sem 'Motivo'")

    # 6. Diferenças em relação à fonte: cada uma aprovada pelo usuário
    dif = md.secao(linhas, "Diferenças em relação à fonte", nivel=2) or []
    for cab, dados in md.tabelas(dif):
        ca = md.coluna(cab, "Aprovado por")
        if ca is None:
            continue
        for row in dados:
            if ca >= len(row) or md.vazia(row[ca]):
                rel.erro(f"diferença em relação à fonte sem 'Aprovado por': {row[0][:60]}")

    # 7. Rastreabilidade: um para um com os critérios
    ras = md.secao(linhas, "Rastreabilidade", nivel=2)
    if ras is not None:
        origem = {}
        for cab, dados in md.tabelas(ras):
            cc, co = md.coluna(cab, "Criterio"), md.coluna(cab, "Origem")
            if cc is None or co is None:
                continue
            for row in dados:
                if len(row) > max(cc, co):
                    origem[row[cc].strip("* ")] = row[co]
        for cid in criterios:
            if cid not in origem:
                rel.erro(f"critério {cid} sem linha na Rastreabilidade")
            elif md.vazia(origem[cid]) or md.PLACEHOLDER_RE.search(origem[cid]):
                rel.erro(f"critério {cid} sem origem na Rastreabilidade")
        for cid in origem:
            if ID_CRIT_RE.fullmatch(cid) and cid not in criterios:
                rel.erro(f"Rastreabilidade cita {cid}, que não existe nos Requisitos")

    # 8. Perguntas em aberto
    perguntas = md.secao(linhas, "Perguntas em aberto", nivel=2) or []
    abertas = [p for p in itens_de_lista(perguntas) if not md.normaliza(p).startswith("nenhuma")]
    for p in abertas:
        (rel.erro if aprovado else rel.aviso)(f"pergunta em aberto: {p[:80]}")

    # 9. Aprovação (só com --aprovado)
    if aprovado:
        ap = md.secao(linhas, "Aprovação", nivel=2) or []
        if not md.aprovacoes(ap):
            rel.erro('sem aprovação: grave **Aprovado**: AAAA-MM-DD — usuário: "<palavras dele>" (só se o usuário aprovou)')

    # 10. Placeholders que sobraram
    for n in md.placeholders(linhas):
        rel.aviso(f"linha {n}: placeholder do template não preenchido")

    return rel


def main(argv=None):
    p = argparse.ArgumentParser(description="Gate do Define (DEFINE_*.md).")
    p.add_argument("arquivo", help="caminho do DEFINE_<FEATURE>.md")
    p.add_argument("--aprovado", action="store_true", help="gate antes do Build: exige aprovação e nenhuma pergunta aberta")
    p.add_argument("--estrito", action="store_true", help="avisos também reprovam")
    a = p.parse_args(argv)
    caminho = Path(a.arquivo)
    if not caminho.is_file():
        print(f"arquivo não encontrado: {caminho}", file=sys.stderr)
        return 2
    return valida(caminho, aprovado=a.aprovado).imprime_e_sai(estrito=a.estrito)


if __name__ == "__main__":
    sys.exit(main())
