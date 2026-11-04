"""tasks.py — gate do plano de tarefas (TASKS_*.md), escrito pelo @sdd-po.

Roda ANTES de apresentar o plano ao usuário, de novo depois do Design, e com
--executar antes da primeira task do Build. Lê o TASKS_*.md e o DEFINE_*.md da
mesma feature, e o DESIGN_*.md quando ele já existe. Nunca lê o código do
projeto; só o --executar roda os comandos da linha **Build**.

Erros (exit 1):
  - falta uma seção obrigatória
  - o DEFINE não está aprovado na última versão dele, ou o plano cita outra versão do DEFINE
  - Matriz de testes sem as colunas do template, vazia, ou com nível que não existe
  - Gates sem os níveis rápido, completo e build, nível sem comando (ou "nenhum — motivo")
  - nenhuma história; história sem pontos, com pontos fora de Fibonacci (1, 2, 3, 5, 8, 13)
    ou sem task
  - tabela de tasks sem uma coluna do template
  - ID de task malformado ou repetido
  - task sem "O que faz"; task que cobre critério sem "Teste"
  - Gate da task que não é um nível da seção Gates, ou nível sem comando
  - task que cita critério que não existe no DEFINE
  - dependência que não existe, que aponta para a própria task ou para uma task posterior
  - critério do DEFINE que nenhuma task cobre
  - Provas: sem a linha **Build**; Run sem comando; prova sem critério, com critério que não
    existe, sem "Prova:", em formato desconhecido; `run` sem a linha Run, sem a linha esperada
    ou com linha esperada sem marcador de passou; critério do DEFINE sem prova
  - DESIGN sem uma seção obrigatória; DESIGN que cita task ou critério que não existe;
    tabela do DESIGN sem uma coluna; menos de 2 abordagens; abordagem sem a confirmação do
    usuário; risco sem mitigação; dado ruim sem tratamento
  - com --aprovado: sem aprovação do plano, ou aprovação de uma versão que não é a última
  - com --executar: o mesmo do --aprovado, DESIGN ausente, ou build vermelho antes de mudar
Avisos (exit 1 só com --estrito):
  - história sem "Como … quero … para …"
  - última task de uma história fora do nível build
  - Run declarado que nenhuma prova usa
  - task que nenhum componente do DESIGN cita; task ligada a componentes em lugares diferentes
  - {placeholder} do template que sobrou

Uso:
  python3 -m sdd_gates tasks docs/planning/TASKS_<FEATURE>.md [--define …] [--design …]
                              [--aprovado | --executar] [--estrito]

O DEFINE e o DESIGN são procurados pelo nome da feature (TASKS_X.md → DEFINE_X.md,
DESIGN_X.md) em docs/specs e docs/designs a partir da pasta atual, depois ao lado
da pasta do TASKS (../specs, ../designs) e por fim na mesma pasta do TASKS.

Códigos de saída: 0 ok, 1 o plano não passou, 2 erro de uso (inclui DEFINE não encontrado).
"""

import argparse
import re
import sys
from pathlib import Path

from . import define, execucao, md

SECOES = ["Identificação", "Matriz de testes", "Gates", "Histórias", "Provas", "Aprovação",
          "Histórico de revisões"]
COLUNAS_TASK = ["Task", "O que faz", "Critérios", "Depende de", "Teste", "Gate"]
COLUNAS_MATRIZ = ["Camada", "Teste", "Profundidade", "Onde", "Nível"]
COLUNAS_GATES = ["Nível", "Quando", "Comando"]
NIVEIS = ["rápido", "completo", "build"]
FIBONACCI = {1, 2, 3, 5, 8, 13}

SECOES_DESIGN = ["Abordagens", "Componentes", "Onde a regra roda", "Riscos e pontos de atenção",
                 "Dado ruim e falhas"]
COLUNAS_ABORDAGEM = ["ID", "Abordagem", "Prós", "Contras"]
COLUNAS_COMPONENTE = ["Componente", "Onde fica", "Critérios", "Tasks"]
COLUNAS_REGRA = ["Critérios", "Onde roda", "Prova"]
COLUNAS_RISCO = ["Ponto", "Onde", "Impacto", "Mitigação"]
COLUNAS_DADO_RUIM = ["Cenário", "Tratamento", "O que o consumidor vê"]

HISTORIA_RE = re.compile(r"^###\s+(H\d+)\b\s*:?\s*(.*)$")
PONTOS_RE = re.compile(r"(\d+)\s*(?:pontos?|pts?)\b", re.I)
TASK_RE = re.compile(r"\bT\d+\b")
ABORDAGEM_RE = re.compile(r"\bA\d+\b")
COMO_RE = re.compile(r"\bcomo\b.*\bquero\b.*\bpara\b", re.I)
CONFIRMADA_RE = re.compile(r'\*\*Confirmada\*\*:\s*(A\d+)\b.*?usu[aá]rio:\s*["“](.+?)["”]')


def acha(tipo, pasta_docs, feature, tasks, explicito):
    """Caminho do DEFINE_/DESIGN_ da feature, ou None se não achar."""
    if explicito:
        return Path(explicito)
    nome = f"{tipo}_{feature}.md"
    for cand in (Path.cwd() / "docs" / pasta_docs / nome,
                 tasks.parent.parent / pasta_docs / nome,
                 tasks.parent / nome):
        if cand.is_file():
            return cand
    return None


def versao_citada(valor):
    m = re.search(r"\bv(\d+(?:\.\d+)*)\b", valor)
    return m.group(1) if m else None


def nivel(texto):
    """Nível de gate normalizado ('rapido', 'completo', 'build') ou o texto normalizado."""
    return md.normaliza(texto.replace("`", "")).strip("* ")


def historias(linhas):
    """Lista de (ID, resto do título, linhas da história) dentro de '## Histórias'."""
    sec = md.secao(linhas, "Histórias", nivel=2) or []
    resultado, atual = [], None
    for linha in sec:
        m = HISTORIA_RE.match(linha)
        if m:
            atual = (m.group(1), m.group(2), [])
            resultado.append(atual)
        elif atual is not None:
            atual[2].append(linha)
    return resultado


def confere_define(def_linhas, cit, rel):
    """O plano só vale sobre uma spec aprovada, e sobre a versão aprovada."""
    ap = md.ultima_aprovacao(def_linhas)
    ultima = md.ultima_versao(def_linhas)
    if ap is None or not ap[1]:
        rel.erro("o DEFINE não tem aprovação com versão: aprove a spec antes do plano (@sdd-define, Passo 8)")
        return
    if ap[1] != ultima:
        rel.erro(f"o DEFINE mudou depois de aprovado (aprovada a v{ap[1]}, última versão {ultima}): "
                 "a spec precisa de aprovação nova antes do plano")
    if cit is None:
        rel.erro("Identificação: a linha DEFINE não diz a versão da spec (ex.: `docs/specs/DEFINE_X.md` — v1.2)")
    elif cit != ap[1]:
        rel.erro(f"o plano foi feito sobre a v{cit} do DEFINE, mas a aprovada é a v{ap[1]}: revise o plano")


def le_gates(linhas, rel):
    """{nível normalizado: comandos} da seção Gates; lista vazia = 'nenhum — motivo'."""
    sec = md.secao(linhas, "Gates", nivel=2)
    niveis = {}
    if sec is None:
        return niveis
    for cab, dados in md.tabelas(sec):
        cols = md.colunas(cab, COLUNAS_GATES, "Gates", rel)
        if cols is None:
            continue
        cn, _, cc = cols
        for row in dados:
            n = nivel(row[cn]) if cn < len(row) else ""
            if n not in [md.normaliza(x) for x in NIVEIS]:
                rel.erro(f"Gates: nível '{row[cn] if cn < len(row) else ''}' não existe (use {', '.join(NIVEIS)})")
                continue
            cmd = row[cc] if cc < len(row) else ""
            if md.vazia(cmd):
                rel.erro(f"Gates: nível '{n}' sem comando (ou 'nenhum — motivo')")
                continue
            niveis[n] = md.le_build(cmd, rel, f"Gates › {n}") or []
    for n in NIVEIS:
        if md.normaliza(n) not in niveis:
            rel.erro(f"Gates: falta o nível '{n}' (com o comando, ou 'nenhum — motivo')")
    return niveis


def confere_matriz(linhas, rel):
    sec = md.secao(linhas, "Matriz de testes", nivel=2)
    if sec is None:
        return
    n_linhas = 0
    for cab, dados in md.tabelas(sec):
        cols = md.colunas(cab, COLUNAS_MATRIZ, "Matriz de testes", rel)
        if cols is None:
            continue
        cc, _, _, _, cn = cols
        for row in dados:
            n_linhas += 1
            camada = row[cc][:40] if cc < len(row) else "?"
            valor = row[cn] if cn < len(row) else ""
            if not md.vazia(valor) and nivel(valor) not in [md.normaliza(x) for x in NIVEIS]:
                rel.erro(f"Matriz de testes: camada '{camada}' com nível '{valor}', que não existe "
                         f"(use {', '.join(NIVEIS)})")
    if n_linhas == 0:
        rel.erro("Matriz de testes vazia: uma linha por camada que a feature toca (camada, teste, "
                 "profundidade, onde, nível)")


def le_tasks(hist, criterios, niveis, rel):
    """Valida histórias e tasks. Devolve ({task: critérios}, critérios cobertos)."""
    tasks, cobertos = {}, set()
    validos = [md.normaliza(x) for x in NIVEIS]
    if not hist:
        rel.erro("'## Histórias' sem nenhuma história (### H1: título — N pontos)")
    for hid, titulo, corpo in hist:
        p = PONTOS_RE.search(titulo)
        if not p:
            rel.erro(f"{hid} sem pontos: escreva no título, ex.: '### {hid}: título — 3 pontos'")
        else:
            pts = int(p.group(1))
            if pts > 13:
                rel.erro(f"{hid} com {pts} pontos: quebre a história (máximo 13)")
            elif pts not in FIBONACCI:
                rel.erro(f"{hid} com {pts} pontos: use 1, 2, 3, 5, 8 ou 13")
        if not any(COMO_RE.search(md.normaliza(l)) for l in corpo):
            rel.aviso(f"{hid} sem 'Como … quero … para …': diga quem usa e o valor da fatia")
        da_historia = []
        for cab, dados in md.tabelas(corpo):
            cols = md.colunas(cab, COLUNAS_TASK, f"{hid}", rel)
            if cols is None:
                continue
            ct, co, cc, cd, cte, cg = cols
            for row in dados:
                cel = lambda i: row[i] if i < len(row) else ""
                tid = cel(ct).strip("* ")
                if not re.fullmatch(r"T\d+", tid):
                    rel.erro(f"{hid}: task '{tid}' com ID malformado (use T1, T2…)")
                    continue
                if tid in tasks:
                    rel.erro(f"task {tid} repetida")
                if md.vazia(cel(co)):
                    rel.erro(f"task {tid} sem 'O que faz'")
                refs = define.ID_CRIT_RE.findall(cel(cc))
                for r in refs:
                    if r not in criterios:
                        rel.erro(f"task {tid} cita {r}, que não existe no DEFINE")
                cobertos.update(refs)
                if refs and md.vazia(cel(cte)):
                    rel.erro(f"task {tid} cobre {', '.join(refs)} e não diz o teste que prova "
                             "(o teste vai na task que cria a camada; 'testado em outra task' não vale)")
                g = nivel(cel(cg))
                if md.vazia(cel(cg)):
                    rel.erro(f"task {tid} sem 'Gate': o nível que fecha a task ({', '.join(NIVEIS)})")
                elif g not in validos:
                    rel.erro(f"task {tid}: gate '{cel(cg)[:40]}' não é um nível da seção Gates "
                             f"({', '.join(NIVEIS)}); o comando fica na seção Gates")
                elif g in niveis and not niveis[g]:
                    rel.erro(f"task {tid} usa o nível '{g}', que não tem comando na seção Gates")
                for dep in TASK_RE.findall(cel(cd)):
                    if dep == tid:
                        rel.erro(f"task {tid} depende de si mesma")
                    elif dep not in tasks:
                        rel.erro(f"task {tid} depende de {dep}, que não vem antes dela no plano "
                                 "(dependência só aponta para trás)")
                tasks[tid] = refs
                da_historia.append((tid, g))
        if not da_historia:
            rel.erro(f"{hid} sem task")
        elif da_historia[-1][1] != "build":
            rel.aviso(f"{hid}: a última task ({da_historia[-1][0]}) não roda o nível build; "
                      "a última task de cada história fecha com o build")
    return tasks, cobertos


def confere_design(des_linhas, tasks, criterios, rel):
    """O DESIGN, quando existe: seções, abordagens confirmadas, e tudo apontando para o que existe."""
    for nome in SECOES_DESIGN:
        if md.secao(des_linhas, nome, nivel=2) is None:
            rel.erro(f"DESIGN sem a seção '## {nome}'")

    # Abordagens: 2 ou 3, e a escolhida confirmada pelo usuário com as palavras dele
    abord = md.secao(des_linhas, "Abordagens", nivel=2)
    if abord is not None:
        ids = []
        for cab, dados in md.tabelas(abord):
            cols = md.colunas(cab, COLUNAS_ABORDAGEM, "DESIGN › Abordagens", rel)
            if cols is None:
                continue
            ids += [row[cols[0]].strip("* ") for row in dados if cols[0] < len(row)]
        if len(ids) < 2:
            rel.erro("DESIGN › Abordagens: apresente 2 ou 3 abordagens para o mesmo escopo, com a recomendada primeiro")
        conf = [m for l in abord for m in [CONFIRMADA_RE.search(l)] if m]
        if not conf:
            rel.erro('DESIGN › Abordagens: sem a confirmação do usuário (**Confirmada**: A<n> — usuário: "…"); '
                     "confirme a abordagem antes dos componentes")
        elif conf[-1].group(1) not in ids:
            rel.erro(f"DESIGN › Abordagens: a confirmação cita {conf[-1].group(1)}, que não está na tabela")

    # Componentes: apontam para tasks e critérios que existem; uma task, um lugar
    comp = md.secao(des_linhas, "Componentes", nivel=2)
    citadas, lugares = set(), {}
    for cab, dados in md.tabelas(comp or []):
        cols = md.colunas(cab, COLUNAS_COMPONENTE, "DESIGN › Componentes", rel)
        if cols is None:
            continue
        cn, cl, cc, ct = cols
        for row in dados:
            nome = row[cn][:40] if cn < len(row) else "?"
            lugar = md.normaliza(row[cl].replace("`", "")) if cl < len(row) else ""
            for r in define.ID_CRIT_RE.findall(row[cc] if cc < len(row) else ""):
                if r not in criterios:
                    rel.erro(f"DESIGN: componente '{nome}' cita {r}, que não existe no DEFINE")
            for t in TASK_RE.findall(row[ct] if ct < len(row) else ""):
                if t not in tasks:
                    rel.erro(f"DESIGN: componente '{nome}' cita {t}, que não existe no plano")
                citadas.add(t)
                if lugar:
                    lugares.setdefault(t, set()).add(lugar)
    for t in tasks:
        if t not in citadas:
            rel.aviso(f"task {t} não aparece em nenhum componente do DESIGN")
        elif len(lugares.get(t, ())) > 1:
            rel.aviso(f"task {t} cai em componentes de lugares diferentes ({', '.join(sorted(lugares[t]))}): "
                      "uma task, um lugar; quebre a task (versão nova do plano)")

    # Onde a regra roda: critérios que existem, e um lugar para cada regra
    for cab, dados in md.tabelas(md.secao(des_linhas, "Onde a regra roda", nivel=2) or []):
        cols = md.colunas(cab, COLUNAS_REGRA, "DESIGN › Onde a regra roda", rel)
        if cols is None:
            continue
        cc, co, _ = cols
        for row in dados:
            refs = define.ID_CRIT_RE.findall(row[cc] if cc < len(row) else "")
            for r in refs:
                if r not in criterios:
                    rel.erro(f"DESIGN › Onde a regra roda: cita {r}, que não existe no DEFINE")
            if co >= len(row) or md.vazia(row[co]):
                rel.erro(f"DESIGN › Onde a regra roda: {', '.join(refs) or 'linha'} sem dizer onde a regra roda")

    # Riscos (com mitigação) e dado ruim (com tratamento); "nenhum encontrado" vale nos riscos
    for nome, colunas_, ci, rotulo in (("Riscos e pontos de atenção", COLUNAS_RISCO, 3, "sem mitigação"),
                                        ("Dado ruim e falhas", COLUNAS_DADO_RUIM, 1, "sem tratamento")):
        sec = md.secao(des_linhas, nome, nivel=2)
        if sec is None:
            continue
        linhas_tab = 0
        for cab, dados in md.tabelas(sec):
            cols = md.colunas(cab, colunas_, f"DESIGN › {nome}", rel)
            if cols is None:
                continue
            for row in dados:
                linhas_tab += 1
                if cols[ci] >= len(row) or md.vazia(row[cols[ci]]):
                    rel.erro(f"DESIGN › {nome}: '{row[cols[0]][:40] if cols[0] < len(row) else '?'}' {rotulo}")
        solto = " ".join(md.normaliza(l) for l in sec if l.strip() and not l.strip().startswith("|"))
        if linhas_tab == 0 and not re.search(r"\bnenhum\b|nao se aplica", solto):
            rel.erro(f"DESIGN › {nome}: vazio (preencha a tabela, ou escreva 'nenhum encontrado' / "
                     "'não se aplica' com o motivo)")


def valida(caminho, def_caminho, des_caminho, aprovado=False, executar=False):
    rel = md.Relatorio(f"sdd_gates tasks {caminho.name}")
    linhas = md.prepara(caminho.read_text(encoding="utf-8"))

    # 1. Seções obrigatórias
    for nome in SECOES:
        if md.secao(linhas, nome, nivel=2) is None:
            rel.erro(f"falta a seção '## {nome}'")

    # 2. O DEFINE: aprovado, na versão que o plano cita
    def_linhas = md.prepara(def_caminho.read_text(encoding="utf-8"))
    criterios = define.criterios_do_define(def_linhas)
    if not criterios:
        rel.erro(f"{def_caminho.name} sem critérios de aceite: o plano não tem o que cobrir")
    confere_define(def_linhas, versao_citada(md.campo_da_identificacao(linhas, "DEFINE")), rel)

    # 3. Matriz de testes e níveis de gate
    confere_matriz(linhas, rel)
    niveis = le_gates(linhas, rel)

    # 4. Histórias e tasks
    tasks, cobertos = le_tasks(historias(linhas), set(criterios), niveis, rel)

    # 5. Cobertura: todo critério do DEFINE tem uma task que o prova
    for c in criterios:
        if c not in cobertos:
            rel.erro(f"critério {c} do DEFINE sem task que o prove")

    # 6. Provas: uma por critério, com o comando que a decide
    provas = None
    sec_provas = md.secao(linhas, "Provas", nivel=2)
    if sec_provas is not None:
        provas = md.confere_provas(sec_provas, criterios, rel)

    # 7. O DESIGN, se já existe
    if des_caminho is not None:
        confere_design(md.prepara(des_caminho.read_text(encoding="utf-8")), tasks, set(criterios), rel)

    # 8. Aprovação do plano (com --aprovado ou --executar)
    if aprovado or executar:
        md.confere_aprovacao(linhas, rel, "o plano")

    # 9. Antes da primeira task: o Design existe e o build está verde
    if executar:
        if des_caminho is None:
            rel.erro("--executar: falta o DESIGN (docs/designs/DESIGN_<FEATURE>.md); no Grande e no "
                     "Complexo, o Build começa depois do Design (@sdd-design)")
        if rel.erros:
            rel.nota("build não rodou: corrija os erros acima primeiro")
        elif provas is not None and provas["build"] is not None:
            execucao.confere_build(provas["build"], rel)

    # 10. Placeholders que sobraram
    for n in md.placeholders(linhas):
        rel.aviso(f"linha {n}: placeholder do template não preenchido")

    return rel


def main(argv=None):
    p = argparse.ArgumentParser(prog="python3 -m sdd_gates tasks", description="Gate do plano de tarefas (TASKS_*.md).")
    p.add_argument("arquivo", help="caminho do TASKS_<FEATURE>.md")
    p.add_argument("--define", help="caminho do DEFINE_<FEATURE>.md (padrão: procura pelo nome da feature)")
    p.add_argument("--design", help="caminho do DESIGN_<FEATURE>.md (padrão: procura; se não existe, não confere)")
    p.add_argument("--aprovado", action="store_true", help="exige o plano aprovado na última versão")
    p.add_argument("--executar", action="store_true",
                   help="antes da 1ª task do Build: o mesmo do --aprovado, o DESIGN presente e o build verde")
    p.add_argument("--estrito", action="store_true", help="avisos também reprovam")
    a = p.parse_args(argv)
    caminho = Path(a.arquivo)
    if not caminho.is_file():
        print(f"arquivo não encontrado: {caminho}", file=sys.stderr)
        return 2
    m = re.fullmatch(r"TASKS_(.+)\.md", caminho.name)
    if not m and not a.define:
        print("o nome do arquivo precisa ser TASKS_<FEATURE>.md (ou passe --define)", file=sys.stderr)
        return 2
    feature = m.group(1) if m else ""
    def_caminho = acha("DEFINE", "specs", feature, caminho, a.define)
    if def_caminho is None or not def_caminho.is_file():
        print(f"DEFINE da feature não encontrado (DEFINE_{feature}.md); passe --define", file=sys.stderr)
        return 2
    des_caminho = acha("DESIGN", "designs", feature, caminho, a.design)
    if des_caminho is not None and not des_caminho.is_file():
        print(f"DESIGN não encontrado: {des_caminho}", file=sys.stderr)
        return 2
    rel = valida(caminho, def_caminho, des_caminho, aprovado=a.aprovado, executar=a.executar)
    return rel.imprime_e_sai(estrito=a.estrito)


if __name__ == "__main__":
    sys.exit(main())
