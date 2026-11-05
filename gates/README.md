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
| `python3 -m sdd_gates define … --aprovado` | antes do PO e do Build | O mesmo + aprovação gravada para a última versão do histórico, nenhuma pergunta em aberto (nem no registro) e toda dimensão da rubrica com destino. No tamanho Médio, a seção Provas: uma prova por critério |
| `python3 -m sdd_gates define … --executar` | antes da 1ª mudança do Build, no Médio | O mesmo do `--aprovado` + roda a linha `**Build**` das Provas uma vez; vermelho antes de mudar reprova |
| `python3 -m sdd_gates tasks docs/planning/TASKS_<FEATURE>.md` | PO e Design | Matriz de testes e os três níveis de gate; histórias com pontos Fibonacci, tasks com critério, dependência só para trás, teste e nível de gate; uma prova por critério (linha `Build`, grupos `Run`, linha esperada com marcador de passou); DEFINE aprovado na versão que o plano cita. Se o DESIGN existe: abordagens confirmadas pelo usuário, componentes e regras apontando para tasks e critérios que existem, uma task por lugar, riscos com mitigação, dado ruim com tratamento |
| `python3 -m sdd_gates tasks … --aprovado` | depois da aprovação do plano | O mesmo + plano aprovado na última versão do histórico |
| `python3 -m sdd_gates tasks … --executar` | antes da 1ª task do Build | O mesmo do `--aprovado` + DESIGN presente + roda a linha `**Build**` das Provas uma vez; vermelho antes de mudar reprova |
| `python3 -m sdd_gates selftest` | — | Testa os próprios gates por mutação |

Códigos de saída: `0` passou, `1` não passou (a saída diz o que corrigir), `2` erro de uso. `--estrito` faz os avisos também reprovarem.

## Desenvolver

```bash
python3 -m pip install -e gates
python3 -m sdd_gates selftest -v      # do clone, também confere os templates das skills (DEFINE, TASKS, DESIGN)
```

Mexeu num gate, num template ou numa fixture: rode o `selftest`. Todo mutante tem que morrer.
