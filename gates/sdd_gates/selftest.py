"""selftest.py — testa os próprios gates do SDD por mutação.

Um gate que aprova tudo é decoração, e nada no uso normal revela isso. Então o
gate passa pela mesma disciplina que ele cobra: partimos de artefatos corretos
(as fixtures, que precisam passar limpas), estragamos um ponto de cada vez e
exigimos que o gate reprove com a mensagem certa.

Também confere que os templates das skills ainda têm tudo o que os gates
procuram: se alguém mudar um template e esquecer o gate (ou o contrário),
aparece aqui. Essa parte precisa do repo das skills: no pacote instalado, passe
--repo (ou --template, só para o DEFINE) ou rode do clone.

Rode depois de mexer em qualquer gate, template ou fixture:
  python3 -m sdd_gates selftest [-v] [--repo <raiz do repo das skills>]

Códigos de saída: 0 tudo certo, 1 algum mutante sobreviveu ou a base quebrou.
"""

import argparse
import io
import re
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

from . import define, tasks

AQUI = Path(__file__).resolve().parent
FIXTURES = AQUI / "fixtures"
FIXTURE_DEFINE = FIXTURES / "DEFINE_PEDIDOS_DIARIOS.md"
FIXTURE_TASKS = FIXTURES / "TASKS_PEDIDOS_DIARIOS.md"
FIXTURE_DESIGN = FIXTURES / "DESIGN_PEDIDOS_DIARIOS.md"
# No clone do repo (ou instalação editável), a raiz das skills fica dois níveis acima do pacote.
REPO_PADRAO = AQUI.parents[1]
TEMPLATES = {
    "define": Path("sdd-define") / "DEFINE_TEMPLATE.md",
    "tasks": Path("sdd-po") / "TASKS_TEMPLATE.md",
    "design": Path("sdd-design") / "DESIGN_TEMPLATE.md",
}


def roda_define(texto, *args):
    """Grava o texto num arquivo temporário, roda o gate e devolve (exit, saída)."""
    with tempfile.TemporaryDirectory() as d:
        arq = Path(d) / "DEFINE_TESTE.md"
        arq.write_text(texto, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            codigo = define.main([str(arq), *args])
        return codigo, buf.getvalue()


def roda_tasks(textos, *args):
    """Grava TASKS, DEFINE e (se houver) DESIGN numa pasta temporária e roda o gate tasks."""
    with tempfile.TemporaryDirectory() as d:
        for tipo, texto in textos.items():
            if texto is not None:
                (Path(d) / f"{tipo.upper()}_PEDIDOS_DIARIOS.md").write_text(texto, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            codigo = tasks.main([str(Path(d) / "TASKS_PEDIDOS_DIARIOS.md"), *args])
        return codigo, buf.getvalue()


def troca(texto, antigo, novo):
    assert antigo in texto, f"mutação não aplicável: {antigo[:60]!r}"
    return texto.replace(antigo, novo, 1)


def remove_secao(texto, titulo):
    padrao = re.compile(rf"^## {re.escape(titulo)}\n.*?(?=^## |\Z)", re.M | re.S)
    assert padrao.search(texto), f"seção não encontrada: {titulo}"
    return padrao.sub("", texto, count=1)


# (nome, função que estraga o texto, argumentos do gate, trecho esperado na saída)
MUTANTES_DEFINE = [
    ("critério sem DEVE",
     lambda t: troca(t, "ENTÃO o pipeline DEVE manter só", "ENTÃO o pipeline mantém só"),
     [], "R1.1 sem DEVE"),
    ("ID de critério repetido",
     lambda t: troca(t, "- **R1.2** O pipeline", "- **R1.1** O pipeline"),
     [], "R1.1 repetido"),
    ("critério sob o requisito errado",
     lambda t: troca(t, "- **R2.3** O pipeline", "- **R1.9** O pipeline"),
     [], "R1.9 fora do requisito"),
    ("nenhum critério",
     lambda t: re.sub(r"^- \*\*R\d+\.\d+\*\*.*\n", "", t, flags=re.M),
     [], "nenhum critério de aceite"),
    ("fora do escopo vazio",
     lambda t: troca(t, "- Camada gold de receita (feature separada)\n- Correção dos dados históricos antes de 2026-01-01\n", ""),
     [], "Fora do escopo' vazio"),
    ("seção obrigatória ausente",
     lambda t: remove_secao(t, "Problema"),
     [], "falta a seção '## Problema'"),
    ("dimensão implícita ausente",
     lambda t: troca(t, "| Duplicidade | R1.1, R1.2 |\n", ""),
     [], "falta a dimensão 'Duplicidade'"),
    ("dimensão implícita sem destino",
     lambda t: troca(t, "| Freshness e SLA | R2.3 |", "| Freshness e SLA |  |"),
     [], "'Freshness e SLA' sem destino"),
    ("dimensão aponta para critério inexistente",
     lambda t: troca(t, "| Freshness e SLA | R2.3 |", "| Freshness e SLA | R2.9 |"),
     [], "aponta para R2.9"),
    ("suposição sem motivo",
     lambda t: troca(t, "| Combina com o fechamento às 7h |", "|  |"),
     [], "S-1 sem 'Motivo'"),
    ("critério sem rastreabilidade",
     lambda t: troca(t, "| R2.3 | pedido: \"até as 7h\" |\n", ""),
     [], "R2.3 sem linha na Rastreabilidade"),
    ("rastreabilidade de critério inexistente",
     lambda t: troca(t, "| R2.3 | pedido: \"até as 7h\" |", "| R2.3 | pedido: \"até as 7h\" |\n| R3.1 | pedido |"),
     [], "cita R3.1"),
    ("diferença com a fonte sem aprovação",
     lambda t: troca(t, "## Suposições", "## Diferenças em relação à fonte\n\n| O que a fonte diz | O que esta spec faz | Por quê | Aprovado por |\n|---|---|---|---|\n| Carga às 04h | Carga às 05h | Origem fecha às 04h30 |  |\n\n## Suposições"),
     [], "sem 'Aprovado por'"),
    ("aprovação ausente (gate do Build)",
     lambda t: troca(t, '**Aprovado**: 2026-11-02 — v1.0 — usuário: "pode seguir com essa spec"', ""),
     ["--aprovado"], "sem aprovação"),
    ("aprovação sem as palavras do usuário",
     lambda t: troca(t, '**Aprovado**: 2026-11-02 — v1.0 — usuário: "pode seguir com essa spec"', "**Aprovado**: 2026-11-02 — v1.0"),
     ["--aprovado"], "sem aprovação"),
    ("aprovação sem a versão",
     lambda t: troca(t, "— v1.0 — usuário:", "— usuário:"),
     ["--aprovado"], "aprovação sem a versão aprovada"),
    ("spec mudou depois de aprovada",
     lambda t: troca(t, "| 1.0 | 2026-11-02 | Versão inicial |", "| 1.0 | 2026-11-02 | Versão inicial |\n| 1.1 | 2026-11-03 | R2.3 passa para 06h |"),
     ["--aprovado"], "a aprovação é da v1.0, mas a última versão"),
    ("pergunta em aberto no gate do Build",
     lambda t: troca(t, "- Nenhuma.", "- A carga roda no feriado?"),
     ["--aprovado"], "pergunta em aberto"),
    ("pergunta em aberto numerada no gate do Build",
     lambda t: troca(t, "- Nenhuma.", "1. A carga roda no feriado?"),
     ["--aprovado"], "pergunta em aberto"),
    ("seção do registro ausente",
     lambda t: remove_secao(t, "Registro do pedido e das respostas"),
     [], "falta a seção '## Registro do pedido e das respostas'"),
    ("pedido original vazio",
     lambda t: troca(t, '> "quero a silver de pedidos sem duplicado até as 7h"\n', ""),
     [], "'### Pedido original' vazio"),
    ("pergunta do registro sem resposta no gate do Build",
     lambda t: troca(t, '| "você decide" |', "| aguardando |"),
     ["--aprovado"], "Q1.2 sem resposta"),
    ("origem cita Qn.m que não está no registro",
     lambda t: troca(t, "| R1.3 | rubrica: idempotência |", '| R1.3 | Q9.9: "sim" |'),
     [], "cita Q9.9"),
    ("frase atribuída ao pedido que não está nele",
     lambda t: troca(t, 'pedido: "até as 7h"', 'pedido: "até as 6h"'),
     [], "não está em pedido original"),
    ("frase atribuída a uma resposta que não está nela",
     lambda t: troca(t, "| R2.2 | Confluence › Fontes de Dados |", '| R2.2 | Q1.2: "pode ser no dia seguinte" |'),
     [], "não está em Q1.2"),
    ("origem que não aponta para nada verificável",
     lambda t: troca(t, "| R1.3 | rubrica: idempotência |", '| R1.3 | resposta final: "ok" |'),
     [], "não aponta para pedido"),
    ("suposição com origem inventada",
     lambda t: troca(t, "| código: `resources/pedidos.pipeline.yml` |", "| usuário, em conversa |"),
     [], "S-3: origem 'usuário, em conversa' não vale"),
    ("suposição 'código' sem o arquivo",
     lambda t: troca(t, "| código: `src/pipelines/pedidos/pipeline.py` |", "| código |"),
     [], "S-2: origem 'código' sem o caminho"),
    ("suposição delegada sem a pergunta",
     lambda t: troca(t, '| usuário delegou (Q1.2: "você decide") |', "| usuário delegou |"),
     [], "S-1: origem 'usuário delegou' sem o Qn.m"),
    ("dimensão esperando pergunta no gate do Build",
     lambda t: troca(t, "| Volume, custo e compute | S-3 |", "| Volume, custo e compute | pergunta em aberto 1 |"),
     ["--aprovado"], "'Volume, custo e compute' aguarda uma pergunta em aberto"),
    ("suposições com o cabeçalho trocado",
     lambda t: troca(t, "| ID | Padrão escolhido | Motivo | Origem | Se estiver errada |", "| ID | Suposição | Origem | Motivo | Se estiver errada |"),
     [], "Suposições: tabela sem a coluna 'Padrão escolhido'"),
    ("suposições sem a coluna Origem",
     lambda t: troca(t, "| Motivo | Origem | Se estiver errada |", "| Motivo | Fonte | Se estiver errada |"),
     [], "Suposições: tabela sem a coluna 'Origem'"),
    ("suposições em lista, fora da tabela",
     lambda t: re.sub(r"(^## Suposições\n).*?(?=^## )", "\\1\n- S-1: execução que falha não avança o ponto de leitura (decisão minha)\n\n", t, count=1, flags=re.M | re.S),
     [], "Suposições: use a tabela do template"),
    ("diferença com a fonte sem a coluna Aprovado por",
     lambda t: troca(t, "## Suposições", "## Diferenças em relação à fonte\n\n| O que a fonte diz | O que esta spec faz | Por quê |\n|---|---|---|\n| Carga às 04h | Carga às 05h | Origem fecha às 04h30 |\n\n## Suposições"),
     [], "Diferenças em relação à fonte: tabela sem a coluna 'Aprovado por'"),
    ("registro com o cabeçalho trocado",
     lambda t: troca(t, "| Resposta do usuário |", "| Retorno |"),
     [], "tabela sem a coluna 'Resposta'"),
    ("rastreabilidade com o cabeçalho trocado",
     lambda t: troca(t, "| Critério | Origem |", "| Critério | Fonte |"),
     [], "Rastreabilidade: tabela sem a coluna 'Origem'"),
    ("trecho do pedido sem destino (estrito)",
     lambda t: troca(t, "sem duplicado até as 7h\"\n", "sem duplicado até as 7h, com receita por canal no dashboard\"\n"),
     ["--estrito"], "trecho do pedido sem destino"),
    ("termo vago sem número (estrito)",
     lambda t: troca(t, "DEVE terminar a carga diária até 06h30 (America/Sao_Paulo)", "DEVE terminar a carga de forma rápida"),
     ["--estrito"], "termo vago"),
    ("placeholder esquecido (estrito)",
     lambda t: troca(t, "Finanças fecha a receita diária", "{Quem tem o problema} fecha a receita diária"),
     ["--estrito"], "placeholder"),
]


# (nome, artefato estragado, função que estraga, argumentos do gate, trecho esperado na saída)
MUTANTES_TASKS = [
    ("seção obrigatória ausente", "tasks",
     lambda t: remove_secao(t, "Histórico de revisões"),
     [], "falta a seção '## Histórico de revisões'"),
    ("nenhuma história", "tasks",
     lambda t: remove_secao(t, "Histórias"),
     [], "sem nenhuma história"),
    ("história sem pontos", "tasks",
     lambda t: troca(t, " — 5 pontos", ""),
     [], "H1 sem pontos"),
    ("pontos fora de Fibonacci", "tasks",
     lambda t: troca(t, "— 3 pontos", "— 4 pontos"),
     [], "H2 com 4 pontos"),
    ("história grande demais", "tasks",
     lambda t: troca(t, "— 5 pontos", "— 21 pontos"),
     [], "quebre a história"),
    ("história sem task", "tasks",
     lambda t: troca(t, "---\n\n## Aprovação", "### H3: Extra — 2 pontos\n\n**Como** Finanças, **quero** mais, **para** testar.\n\n---\n\n## Aprovação"),
     [], "H3 sem task"),
    ("tabela de tasks com coluna trocada", "tasks",
     lambda t: troca(t, "| Teste | Gate |", "| Prova | Gate |"),
     [], "H1: tabela sem a coluna 'Teste'"),
    ("ID de task malformado", "tasks",
     lambda t: troca(t, "| T4 | Expectation", "| Tarefa 4 | Expectation"),
     [], "com ID malformado"),
    ("task repetida", "tasks",
     lambda t: troca(t, "| T3 | Garante", "| T2 | Garante"),
     [], "task T2 repetida"),
    ("task sem 'O que faz'", "tasks",
     lambda t: troca(t, "| Garante que reprocessar a mesma partição não muda a contagem |", "|  |"),
     [], "task T3 sem 'O que faz'"),
    ("task com critério sem teste", "tasks",
     lambda t: troca(t, "`tests/test_dedup.py::test_reprocessa_mesma_particao`", "—"),
     [], "task T3 cobre R1.3 e não diz o teste"),
    ("task sem gate", "tasks",
     lambda t: troca(t, "| `pytest tests/test_janela.py` |", "| — |"),
     [], "task T5 sem 'Gate'"),
    ("task cita critério que não existe", "tasks",
     lambda t: troca(t, "| R1.3 | T2 |", "| R1.3, R3.1 | T2 |"),
     [], "task T3 cita R3.1"),
    ("critério do DEFINE sem task", "tasks",
     lambda t: troca(t, "| R2.2 | T2 |", "| — | T2 |"),
     [], "critério R2.2 do DEFINE sem task"),
    ("dependência para a frente", "tasks",
     lambda t: troca(t, "| R1.1, R1.2 | T1 |", "| R1.1, R1.2 | T3 |"),
     [], "task T2 depende de T3, que não vem antes"),
    ("task depende de si mesma", "tasks",
     lambda t: troca(t, "| R1.3 | T2 |", "| R1.3 | T3 |"),
     [], "task T3 depende de si mesma"),
    ("plano sem a versão do DEFINE", "tasks",
     lambda t: troca(t, "`docs/specs/DEFINE_PEDIDOS_DIARIOS.md` — v1.0", "`docs/specs/DEFINE_PEDIDOS_DIARIOS.md`"),
     [], "não diz a versão da spec"),
    ("plano sobre outra versão do DEFINE", "tasks",
     lambda t: troca(t, "`docs/specs/DEFINE_PEDIDOS_DIARIOS.md` — v1.0", "`docs/specs/DEFINE_PEDIDOS_DIARIOS.md` — v0.9"),
     [], "o plano foi feito sobre a v0.9"),
    ("DEFINE sem aprovação", "define",
     lambda t: troca(t, '**Aprovado**: 2026-11-02 — v1.0 — usuário: "pode seguir com essa spec"', ""),
     [], "o DEFINE não tem aprovação com versão"),
    ("DEFINE mudou depois de aprovado", "define",
     lambda t: troca(t, "| 1.0 | 2026-11-02 | Versão inicial |", "| 1.0 | 2026-11-02 | Versão inicial |\n| 1.1 | 2026-11-03 | R2.3 passa para 06h |"),
     [], "o DEFINE mudou depois de aprovado"),
    ("plano sem aprovação no gate do Build", "tasks",
     lambda t: troca(t, '**Aprovado**: 2026-11-02 — v1.0 — usuário: "plano aprovado, pode criar no Jira"', ""),
     ["--aprovado"], "sem aprovação"),
    ("plano mudou depois de aprovado", "tasks",
     lambda t: troca(t, "| 1.0 | 2026-11-02 | Versão inicial |", "| 1.0 | 2026-11-02 | Versão inicial |\n| 1.1 | 2026-11-03 | T7 nova |"),
     ["--aprovado"], "o plano mudou depois de aprovado"),
    ("DESIGN cita task que não existe", "design",
     lambda t: troca(t, "| T1, T6 |", "| T1, T6, T9 |"),
     [], "cita T9, que não existe no plano"),
    ("DESIGN cita critério que não existe", "design",
     lambda t: troca(t, "| R2.3 | T1, T6 |", "| R2.3, R4.1 | T1, T6 |"),
     [], "cita R4.1, que não existe no DEFINE"),
    ("DESIGN com a coluna Tasks trocada", "design",
     lambda t: troca(t, "| Critérios | Tasks | Constrói com |", "| Critérios | Trabalho | Constrói com |"),
     [], "DESIGN › Componentes: tabela sem a coluna 'Tasks'"),
    ("task fora de todo componente (estrito)", "design",
     lambda t: troca(t, "| T2, T3, T5 |", "| T2, T3 |"),
     ["--estrito"], "task T5 não aparece em nenhum componente"),
    ("história sem 'Como … quero … para' (estrito)", "tasks",
     lambda t: troca(t, "**Como** Finanças, **quero** uma linha por pedido em `silver.pedidos`, **para** fechar a receita sem corrigir duplicados à mão.\n", ""),
     ["--estrito"], "H1 sem 'Como"),
]


def checa_templates(repo, template_define, verbose):
    """Cada template precisa ter as seções, dimensões e colunas que os gates exigem."""
    caminhos = {}
    if repo is not None:
        caminhos = {k: repo / v for k, v in TEMPLATES.items()}
    if template_define is not None:
        caminhos["define"] = template_define
    if not caminhos:
        print("  aviso  templates não checados: rode do clone do repo ou passe --repo")
        return True
    faltas = []
    for tipo, caminho in caminhos.items():
        if not caminho.is_file():
            faltas.append(f"{caminho} não encontrado")
            continue
        texto = caminho.read_text(encoding="utf-8")
        tem_secao = lambda s: re.search(rf"^## {re.escape(s)}\b", texto, re.M)
        if tipo == "define":
            faltas += [f"DEFINE sem a seção '## {s}'" for s in define.SECOES if not tem_secao(s)]
            faltas += [f"DEFINE sem a dimensão '{d}'" for d in define.DIMENSOES if f"| {d}" not in texto]
            if not re.search(r"^### Pedido original\b", texto, re.M):
                faltas.append("DEFINE sem '### Pedido original' dentro do Registro")
        elif tipo == "tasks":
            faltas += [f"TASKS sem a seção '## {s}'" for s in tasks.SECOES if not tem_secao(s)]
            if "| " + " | ".join(tasks.COLUNAS_TASK) + " |" not in texto:
                faltas.append("TASKS sem o cabeçalho da tabela de tasks: | " + " | ".join(tasks.COLUNAS_TASK) + " |")
            if not tasks.HISTORIA_RE.search("\n".join(l for l in texto.splitlines() if l.startswith("### H"))):
                faltas.append("TASKS sem um exemplo de história '### H1: …'")
        elif tipo == "design":
            if not tem_secao("Componentes"):
                faltas.append("DESIGN sem a seção '## Componentes'")
            cab = next((l for l in texto.splitlines() if l.startswith("| Componente |")), "")
            faltas += [f"DESIGN › Componentes sem a coluna '{c}'" for c in tasks.COLUNAS_COMPONENTE if f"| {c} |" not in cab + "|"]
    for f in faltas:
        print(f"  FALHA  template: {f}")
    if verbose and not faltas:
        print(f"  ok     templates ({', '.join(sorted(caminhos))}) têm o que os gates leem")
    return not faltas


def roda_mutantes(nome_gate, mutantes, roda, verbose):
    ok = True
    for nome, estraga, args, esperado in mutantes:
        codigo, saida = roda(estraga, args)
        if not (codigo == 1 and esperado in saida):
            ok = False
            print(f"  FALHA  mutante sobreviveu ({nome_gate}): {nome} (exit {codigo}; esperava '{esperado}')\n{saida}")
        elif verbose:
            print(f"  ok     {nome_gate}: {nome}")
    return ok


def main(argv=None):
    p = argparse.ArgumentParser(prog="python3 -m sdd_gates selftest", description="Testa os gates por mutação.")
    p.add_argument("-v", "--verbose", action="store_true", help="mostra cada mutante")
    p.add_argument("--repo", type=Path, help="raiz do repo das skills (confere os templates)")
    p.add_argument("--template", type=Path, help="só o DEFINE_TEMPLATE.md da skill sdd-define")
    a = p.parse_args(argv)
    repo = a.repo or (REPO_PADRAO if (REPO_PADRAO / TEMPLATES["define"]).is_file() else None)
    if a.repo is not None and not a.repo.is_dir():
        print(f"repo não encontrado: {a.repo}", file=sys.stderr)
        return 2
    if a.template is not None and not a.template.is_file():
        print(f"template não encontrado: {a.template}", file=sys.stderr)
        return 2

    base = {"define": FIXTURE_DEFINE.read_text(encoding="utf-8"),
            "tasks": FIXTURE_TASKS.read_text(encoding="utf-8"),
            "design": FIXTURE_DESIGN.read_text(encoding="utf-8")}

    codigo, saida = roda_define(base["define"], "--aprovado", "--estrito")
    if codigo != 0:
        print("  FALHA  a fixture do DEFINE deveria passar limpa:\n" + saida)
        return 1
    codigo, saida = roda_tasks(base, "--aprovado", "--estrito")
    if codigo != 0:
        print("  FALHA  as fixtures do TASKS e do DESIGN deveriam passar limpas:\n" + saida)
        return 1
    if a.verbose:
        print("  ok     fixtures do DEFINE, TASKS e DESIGN passam com --aprovado --estrito")

    ok = checa_templates(repo, a.template, a.verbose)
    ok &= roda_mutantes("define", MUTANTES_DEFINE,
                        lambda estraga, args: roda_define(estraga(base["define"]), *args), a.verbose)

    def roda_um_tasks(alvo_estraga, args):
        alvo, estraga = alvo_estraga
        textos = dict(base)
        textos[alvo] = estraga(textos[alvo])
        return roda_tasks(textos, *args)

    ok &= roda_mutantes("tasks", [(n, (alvo, f), args, esp) for n, alvo, f, args, esp in MUTANTES_TASKS],
                        roda_um_tasks, a.verbose)

    total = len(MUTANTES_DEFINE) + len(MUTANTES_TASKS)
    print(f"selftest: {'OK' if ok else 'FALHOU'} — {total} mutantes "
          f"({len(MUTANTES_DEFINE)} do gate define, {len(MUTANTES_TASKS)} do gate tasks)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
