"""selftest.py — testa os próprios gates do SDD por mutação.

Um gate que aprova tudo é decoração, e nada no uso normal revela isso. Então o
gate passa pela mesma disciplina que ele cobra: partimos de um artefato correto
(a fixture, que precisa passar limpo), estragamos um ponto de cada vez e
exigimos que o gate reprove com a mensagem certa.

Também confere que o template da skill ainda tem tudo o que o gate procura: se
alguém mudar o template e esquecer o gate (ou o contrário), aparece aqui. Essa
parte precisa do repo: no pacote instalado, passe --template ou rode do clone.

Rode depois de mexer em qualquer gate, template ou fixture:
  python3 -m sdd_gates selftest [-v] [--template sdd-define/DEFINE_TEMPLATE.md]

Códigos de saída: 0 tudo certo, 1 algum mutante sobreviveu ou a base quebrou.
"""

import argparse
import io
import re
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

from . import define

AQUI = Path(__file__).resolve().parent
FIXTURE_DEFINE = AQUI / "fixtures" / "DEFINE_PEDIDOS_DIARIOS.md"
# No clone do repo (ou instalação editável), o template fica dois níveis acima do pacote.
TEMPLATE_NO_REPO = AQUI.parents[1] / "sdd-define" / "DEFINE_TEMPLATE.md"


def roda_define(texto, *args):
    """Grava o texto num arquivo temporário, roda o gate e devolve (exit, saída)."""
    with tempfile.TemporaryDirectory() as d:
        arq = Path(d) / "DEFINE_TESTE.md"
        arq.write_text(texto, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            codigo = define.main([str(arq), *args])
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
     lambda t: troca(t, '**Aprovado**: 2026-11-02 — usuário: "pode seguir com essa spec"', ""),
     ["--aprovado"], "sem aprovação"),
    ("aprovação sem as palavras do usuário",
     lambda t: troca(t, '**Aprovado**: 2026-11-02 — usuário: "pode seguir com essa spec"', "**Aprovado**: 2026-11-02"),
     ["--aprovado"], "sem aprovação"),
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


def checa_template(template, verbose):
    """O template precisa ter cada seção e cada dimensão que o gate exige."""
    if template is None:
        print("  aviso  template não checado: rode do clone do repo ou passe --template")
        return True
    texto = template.read_text(encoding="utf-8")
    faltas = [f"seção '## {s}'" for s in define.SECOES if not re.search(rf"^## {re.escape(s)}\b", texto, re.M)]
    faltas += [f"dimensão '{d}'" for d in define.DIMENSOES if f"| {d}" not in texto]
    if not re.search(r"^### Pedido original\b", texto, re.M):
        faltas.append("'### Pedido original' dentro do Registro")
    for f in faltas:
        print(f"  FALHA  template sem {f}")
    if verbose and not faltas:
        print("  ok     template tem todas as seções e dimensões do gate")
    return not faltas


def main(argv=None):
    p = argparse.ArgumentParser(prog="python3 -m sdd_gates selftest", description="Testa os gates por mutação.")
    p.add_argument("-v", "--verbose", action="store_true", help="mostra cada mutante")
    p.add_argument("--template", type=Path, help="DEFINE_TEMPLATE.md da skill sdd-define")
    a = p.parse_args(argv)
    template = a.template or (TEMPLATE_NO_REPO if TEMPLATE_NO_REPO.is_file() else None)
    if template is not None and not template.is_file():
        print(f"template não encontrado: {template}", file=sys.stderr)
        return 2
    ok = True

    base = FIXTURE_DEFINE.read_text(encoding="utf-8")
    codigo, saida = roda_define(base, "--aprovado", "--estrito")
    if codigo != 0:
        print("  FALHA  a fixture do DEFINE deveria passar limpa:\n" + saida)
        return 1
    if a.verbose:
        print("  ok     fixture do DEFINE passa com --aprovado --estrito")

    ok &= checa_template(template, a.verbose)

    for nome, estraga, args, esperado in MUTANTES_DEFINE:
        codigo, saida = roda_define(estraga(base), *args)
        morto = codigo == 1 and esperado in saida
        if not morto:
            ok = False
            print(f"  FALHA  mutante sobreviveu: {nome} (exit {codigo}; esperava '{esperado}')\n{saida}")
        elif a.verbose:
            print(f"  ok     {nome}")

    total = len(MUTANTES_DEFINE)
    print(f"selftest: {'OK' if ok else 'FALHOU'} — {total} mutantes do gate define")
    return 0 if ok else 1
