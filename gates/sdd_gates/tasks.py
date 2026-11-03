"""tasks.py — gate do plano de tarefas (TASKS_*.md), escrito pelo @sdd-po.

Roda ANTES de apresentar o plano ao usuário e de novo, com --aprovado, antes do
Build. Lê o TASKS_*.md e o DEFINE_*.md da mesma feature, e o DESIGN_*.md quando
ele já existe. Nunca lê o código do projeto.

Erros (exit 1):
  - falta uma seção obrigatória
  - o DEFINE não está aprovado na última versão dele, ou o plano cita outra versão do DEFINE
  - nenhuma história; história sem pontos, com pontos fora de Fibonacci (1, 2, 3, 5, 8, 13)
    ou sem task
  - tabela de tasks sem uma coluna do template
  - ID de task malformado ou repetido
  - task sem "O que faz" ou sem "Gate"; task que cobre critério sem "Teste"
  - task que cita critério que não existe no DEFINE
  - dependência que não existe, que aponta para a própria task ou para uma task posterior
  - critério do DEFINE que nenhuma task cobre
  - DESIGN que cita task ou critério que não existe; tabela de Componentes sem uma coluna
  - com --aprovado: sem aprovação do plano, ou aprovação de uma versão que não é a última
Avisos (exit 1 só com --estrito):
  - história sem "Como … quero … para …"
  - task que nenhum componente do DESIGN cita (só quando o DESIGN existe)
  - {placeholder} do template que sobrou

Uso:
  python3 -m sdd_gates tasks docs/planning/TASKS_<FEATURE>.md [--define …] [--design …]
                              [--aprovado] [--estrito]

O DEFINE e o DESIGN são procurados pelo nome da feature (TASKS_X.md → DEFINE_X.md,
DESIGN_X.md) em docs/specs e docs/designs a partir da pasta atual, depois ao lado
da pasta do TASKS (../specs, ../designs) e por fim na mesma pasta do TASKS.

Códigos de saída: 0 ok, 1 o plano não passou, 2 erro de uso (inclui DEFINE não encontrado).
"""

import argparse
import re
import sys
from pathlib import Path

from . import define, md

SECOES = ["Identificação", "Histórias", "Aprovação", "Histórico de revisões"]
COLUNAS_TASK = ["Task", "O que faz", "Critérios", "Depende de", "Teste", "Gate"]
COLUNAS_COMPONENTE = ["Componente", "Critérios", "Tasks"]
FIBONACCI = {1, 2, 3, 5, 8, 13}

HISTORIA_RE = re.compile(r"^###\s+(H\d+)\b\s*:?\s*(.*)$")
PONTOS_RE = re.compile(r"(\d+)\s*(?:pontos?|pts?)\b", re.I)
TASK_RE = re.compile(r"\bT\d+\b")
COMO_RE = re.compile(r"\bcomo\b.*\bquero\b.*\bpara\b", re.I)


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


def linha_da_identificacao(linhas, campo):
    """Valor da linha `campo` na tabela da Identificação; '' se não houver."""
    ident = md.secao(linhas, "Identificação", nivel=2) or []
    for cab, dados in md.tabelas(ident):
        for row in dados:
            if row and md.normaliza(row[0]).strip("* ") == md.normaliza(campo) and len(row) > 1:
                return row[1]
    return ""


def versao_citada(valor):
    m = re.search(r"\bv(\d+(?:\.\d+)*)\b", valor)
    return m.group(1) if m else None


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


def le_tasks(hist, criterios, rel):
    """Valida histórias e tasks. Devolve ({task: critérios}, critérios cobertos)."""
    tasks, cobertos = {}, set()
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
        n_tasks = 0
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
                n_tasks += 1
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
                    rel.erro(f"task {tid} cobre {', '.join(refs)} e não diz o teste que prova")
                if md.vazia(cel(cg)):
                    rel.erro(f"task {tid} sem 'Gate': o comando que fecha a task")
                for dep in TASK_RE.findall(cel(cd)):
                    if dep == tid:
                        rel.erro(f"task {tid} depende de si mesma")
                    elif dep not in tasks:
                        rel.erro(f"task {tid} depende de {dep}, que não vem antes dela no plano "
                                 "(dependência só aponta para trás)")
                tasks[tid] = refs
        if n_tasks == 0:
            rel.erro(f"{hid} sem task")
    return tasks, cobertos


def confere_design(des_linhas, tasks, criterios, rel):
    """O DESIGN, quando existe, aponta para tasks e critérios que existem."""
    comp = md.secao(des_linhas, "Componentes", nivel=2)
    if comp is None:
        rel.erro("DESIGN sem a seção '## Componentes'")
        return
    citadas = set()
    for cab, dados in md.tabelas(comp):
        cols = md.colunas(cab, COLUNAS_COMPONENTE, "DESIGN › Componentes", rel)
        if cols is None:
            continue
        cn, cc, ct = cols
        for row in dados:
            nome = row[cn][:40] if cn < len(row) else "?"
            for r in define.ID_CRIT_RE.findall(row[cc] if cc < len(row) else ""):
                if r not in criterios:
                    rel.erro(f"DESIGN: componente '{nome}' cita {r}, que não existe no DEFINE")
            for t in TASK_RE.findall(row[ct] if ct < len(row) else ""):
                if t not in tasks:
                    rel.erro(f"DESIGN: componente '{nome}' cita {t}, que não existe no plano")
                citadas.add(t)
    for t in tasks:
        if t not in citadas:
            rel.aviso(f"task {t} não aparece em nenhum componente do DESIGN")


def valida(caminho, def_caminho, des_caminho, aprovado=False):
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
    confere_define(def_linhas, versao_citada(linha_da_identificacao(linhas, "DEFINE")), rel)

    # 3. Histórias e tasks
    tasks, cobertos = le_tasks(historias(linhas), set(criterios), rel)

    # 4. Cobertura: todo critério do DEFINE tem uma task que o prova
    for c in criterios:
        if c not in cobertos:
            rel.erro(f"critério {c} do DEFINE sem task que o prove")

    # 5. O DESIGN, se já existe
    if des_caminho is not None:
        confere_design(md.prepara(des_caminho.read_text(encoding="utf-8")), tasks, set(criterios), rel)

    # 6. Aprovação do plano (só com --aprovado)
    if aprovado:
        md.confere_aprovacao(linhas, rel, "o plano")

    # 7. Placeholders que sobraram
    for n in md.placeholders(linhas):
        rel.aviso(f"linha {n}: placeholder do template não preenchido")

    return rel


def main(argv=None):
    p = argparse.ArgumentParser(prog="python3 -m sdd_gates tasks", description="Gate do plano de tarefas (TASKS_*.md).")
    p.add_argument("arquivo", help="caminho do TASKS_<FEATURE>.md")
    p.add_argument("--define", help="caminho do DEFINE_<FEATURE>.md (padrão: procura pelo nome da feature)")
    p.add_argument("--design", help="caminho do DESIGN_<FEATURE>.md (padrão: procura; se não existe, não confere)")
    p.add_argument("--aprovado", action="store_true", help="gate antes do Build: exige o plano aprovado na última versão")
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
    return valida(caminho, def_caminho, des_caminho, aprovado=a.aprovado).imprime_e_sai(estrito=a.estrito)


if __name__ == "__main__":
    sys.exit(main())
