# sdd-gates

Gates do Spec-Driven Development para o Genie Code no Databricks. Um gate decide **por código** se uma etapa do SDD pode avançar; a skill da etapa diz quando rodar cada um.

Os gates ficam neste pacote, e não dentro das skills, porque o Genie Code não executa scripts que moram em `.assistant/skills`.

## Rodar no Databricks (Genie Code)

O Genie Code também bloqueia `pip install` direto do GitHub. Então o repo é montado uma segunda vez como Git Folder, fora de `.assistant` (ex.: `/Workspace/Users/<você>/sdd-gates`), e os gates rodam dali, sem instalação:

```bash
PYTHONPATH=/Workspace/Users/<você>/sdd-gates/gates python3 -m sdd_gates selftest
```

Passo a passo no [README do repo](../README.md) (Passo 2b).

## Instalar (fora do Genie Code)

Claude Code, CI ou máquina local:

```bash
python3 -m pip install "git+https://github.com/douglittig/genie-code-agent-spec@main#subdirectory=gates"
```

Só biblioteca padrão; sem dependências. Para distribuir por Volume do Unity Catalog ou PyPI interno, gere um wheel com `python -m build gates`.

## Gates

| Comando | Etapa | O que confere |
|---|---|---|
| `python3 -m sdd_gates define docs/specs/DEFINE_<FEATURE>.md` | Define | Seções, registro literal do pedido e das respostas (`Qn.m`), critérios EARS, rubrica de requisitos implícitos, origem das suposições, rastreabilidade com a frase citada conferida na fonte. Tabela com coluna do template renomeada ou faltando é erro, não tabela ignorada |
| `python3 -m sdd_gates define … --aprovado` | antes do Build | O mesmo + aprovação gravada, nenhuma pergunta em aberto (nem no registro) e toda dimensão da rubrica com destino |
| `python3 -m sdd_gates selftest` | — | Testa os próprios gates por mutação |

Códigos de saída: `0` passou, `1` não passou (a saída diz o que corrigir), `2` erro de uso. `--estrito` faz os avisos também reprovarem.

## Desenvolver

```bash
python3 -m pip install -e gates
python3 -m sdd_gates selftest -v      # do clone, também confere o DEFINE_TEMPLATE.md da skill
```

Mexeu num gate, num template ou numa fixture: rode o `selftest`. Todo mutante tem que morrer.
