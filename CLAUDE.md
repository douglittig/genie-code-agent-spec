# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Status:** O workflow SDD foi decomposto em **skills autocontidas com prefixo `sdd-*`** (alinhado à mudança da Databricks que trata cada skill como um ativo individual, em vez de agentes encadeados dentro de uma skill). `@sdd-workflow` decide o tamanho da feature e orquestra; `@sdd-define`, `@sdd-design`, `@sdd-build` e `@sdd-ship` executam cada uma, com `@sdd-staff-engineer` (ADR), `@sdd-po` (Stories/Tasks no Jira), `@sdd-iterate` (mudanças mid-stream) e **documentação automática no Jira via `@sdd-doc`** ao final de cada fase. Ainda em desenvolvimento: `@sdd-dev-workflow` e `@sdd-code-reviewer`.

## Project

`genie-code-agent-spec` — repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code. **Genie Code first**: todas as decisões de design priorizam o paradigma do Genie Code (Agent mode + `@skill-name`), não o paradigma de slash commands do Claude Code CLI.

## Repository Layout

```
<skill-name>/            # 50 skills na raiz (Databricks oficiais + SDD workflow + Python + Spark)
docs/                    # Documentação de referência sobre features do Genie Code
assets/                  # cópias locais de referência — gitignored (links no README, seção Referências)
gates/                   # pacote sdd-gates: gates do SDD por código (no Databricks, rodado de um 2º Git Folder)
THIRD_PARTY_NOTICES.md   # créditos e licenças de terceiros (AgentSpec — MIT; skills Databricks)
.claude/                 # Claude Code CLI local — gitignored, exceto .claude/skills/ (run-genie-code-agent-spec: validador do repo)
```

> **Como usar no Genie Code:** carregue este repo como Git Folder em `Workspace/.assistant/skills/`. As skills ficam disponíveis automaticamente em Agent mode.

> **Quase só conteúdo:** as skills são Markdown, e a "compilação" é o Genie Code/Claude Code lendo os `SKILL.md`. Validar uma skill = revisar o Markdown e rodar `python3 .claude/skills/run-genie-code-agent-spec/driver.py validate`. O único código é o pacote [`gates/`](gates/) (Python puro, sem dependências): mexeu num gate, num template que um gate lê ou numa fixture, rode `python3 -m sdd_gates selftest` a partir de `gates/` (ou com `pip install -e gates`). O CI roda o mesmo selftest em todo PR.

> **Arquivos de instrução paralelos:** [`CLAUDE.md`](CLAUDE.md) (Claude Code) e [`AGENTS.md`](AGENTS.md) (Genie Code) cobrem o mesmo conteúdo para dois agentes. Ao editar um, **atualizar o outro** para mantê-los em sincronia. [`BACKLOG.md`](BACKLOG.md) rastreia trabalho adiado (placeholders corporativos, skills futuras) — consultar antes de começar trabalho novo em `sdd-dev-workflow`/`sdd-code-reviewer`.

## Agent Skills (raiz do repositório)

Cada subpasta na raiz é uma skill autocontida seguindo o padrão open Agent Skills:
- `SKILL.md` — frontmatter (`name`, `description`) + conteúdo que o agente lê
- Arquivos de referência opcionais (`.md`, `.py`, `.sh`)

**O campo `description` do frontmatter dispara o auto-load.** O agente decide carregar uma skill comparando o pedido do usuário com a `description` — por isso as skills `databricks-*` escrevem descrições em inglês, ricas em gatilhos ("Use when building..., querying..., migrating..."). Ao criar/editar uma skill, otimizar a `description` para casar com como o usuário descreveria a tarefa, não para resumir o conteúdo.

**Para criar uma nova skill:** copiar `TEMPLATE/` e editar `SKILL.md`.

O índice completo das skills está no **[README.md](README.md)**, organizado por categoria (IA & ML, Dados & SQL, Plataforma Databricks, Aplicações, Desenvolvimento & Workflow).

### Proveniência: skills upstream vs. skills próprias

> **Origem do workflow SDD:** as fases `sdd-design/build/ship/iterate`, seus templates, `sdd-code-reviewer` e `custom-test-generator` derivam do [AgentSpec](https://github.com/luanmorenommaciel/agentspec), de Luan Moreno (MIT). Ao editar esses arquivos, manter o crédito em [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md); ao reescrever um deles do zero, atualizar a lista de arquivos derivados lá.

O prefixo indica a origem da skill:

- **`databricks-*`** + `spark-python-data-source` → vêm do repo oficial [`databricks/databricks-agent-skills`](https://github.com/databricks/databricks-agent-skills) (Databricks License — cópia em `LICENSE-databricks-agent-skills`). ⚠️ **NÃO editar à mão** — o sync sobrescreve. Para mudar, contribuir no upstream.
- **Congelada:** `databricks-python-dev` veio do antigo upstream `databricks-solutions/ai-dev-kit` (v0.1.14), que deixou de distribuir skills na v0.2.0. Não existe no repo oficial; o sync não a toca (`FROZEN_SKILLS`). `TEMPLATE/` também ficou conosco.
- **`sdd-*`** e **`custom-*`** → skills **nossas**, não existem no upstream, livres para editar. `sdd-*` = skills do workflow de Spec-Driven Development; `custom-*` = demais skills próprias.

- **Sincronização:** [`.github/workflows/sync-databricks-skills.yml`](.github/workflows/sync-databricks-skills.yml) faz sparse checkout efêmero do upstream e chama [`.github/scripts/sync-databricks-skills.sh`](.github/scripts/sync-databricks-skills.sh), que copia as pastas para a raiz, poda as que saíram do upstream e grava o lock; o workflow abre um PR. O script roda igual na máquina local. O upstream **nunca** é commitado aqui (sem submodule/subtree). Roda semanalmente + `workflow_dispatch`.
- **Versão fixada:** última release do upstream, registrada em `databricks-skills.lock` (versão, commit e lista de skills sincronizadas).
- **Origem das pastas upstream:** `skills/` do repo oficial. Exceção: **`spark-python-data-source`** vem de `experimental/` (`EXTRA_SKILLS`).
- **Upstream renomeou uma skill?** O PR do sync mostra a pasta antiga apagada e a nova criada. Antes do merge, trocar as referências `@databricks-*` nas skills `sdd-*` e rodar o validador.
- **Skills NOSSAS, editáveis** (prefixos `sdd-` e `custom-`, salvaguardadas em `OWN_SKILLS`): `sdd-workflow`, `sdd-define`, `sdd-design`, `sdd-build`, `sdd-ship`, `sdd-iterate`, `sdd-doc`, `sdd-staff-engineer`, `sdd-po`, `sdd-dev-workflow`, `sdd-code-reviewer`, `custom-test-generator`. O workflow nunca as sobrescreve.

### Skills de Workflow (família `sdd-*`)

| Skill | Fase | Status | Propósito |
|-------|------|--------|-----------|
| `sdd-workflow` | — | **PRONTO** | Orquestrador: tamanho da feature, contrato de execução, raio de ação no Databricks, fim de etapa |
| `sdd-define` | 1 | **PRONTO** | Spec de dados testável (Confluence via MCP): critérios EARS, rubrica de requisitos implícitos, áreas cinzentas, gate `sdd_gates define`, aprovação gravada → `docs/specs/DEFINE_*.md` (+ `jira_key` e state) |
| `sdd-staff-engineer` | 2 | **PRONTO** | Revisão de spec, decisão arquitetural → `docs/adr/ADR_*.md` |
| `sdd-po` | 3 | **PRONTO** | Histórias (Fibonacci) → tasks atômicas com teste e gate → `docs/planning/TASKS_*.md` + gate `sdd_gates tasks`; Jira quando há épico |
| `sdd-design` | 4 | **PRONTO** | Componentes ligados a critérios e tasks, reaproveitamento e decisões → `docs/designs/DESIGN_*.md` (conferido pelo gate `tasks`) |
| `sdd-build` | 5 | **PRONTO** | Implementação delegando às `@databricks-*` → código + `BUILD_REPORT_*.md` |
| `sdd-ship` | 6 | **PRONTO** | Archive + lições aprendidas + fechamento do ticket → `SHIPPED_*.md` |
| `sdd-iterate` | cross | **PRONTO** | Mudanças mid-stream com análise de cascata |
| `sdd-doc` | cross | **PRONTO** | Hook de fim de fase: comentário + transição no Jira (MCP) |
| `sdd-dev-workflow` | 4+ | EM DESENVOLVIMENTO | Branch → código → validação → PR → merge |
| `sdd-code-reviewer` | 4+ | EM DESENVOLVIMENTO | Code review: segurança, qualidade, performance |

### Arquitetura do workflow SDD — skills autocontidas

Cada fase é uma **skill de primeira classe na raiz do repo** (padrão de ativos do Genie Code) — não há mais `agents/` nem `templates/` compartilhados. `sdd-workflow/SKILL.md` é só o orquestrador: descreve fases, gates e handoffs e roteia para a skill de cada fase. Cada skill de fase carrega **seu próprio template** ao lado do `SKILL.md` (ex.: `sdd-define/DEFINE_TEMPLATE.md` + `STATE_TEMPLATE.md`, `sdd-doc/JIRA_UPDATE_TEMPLATE.md`).

**Gates fora das skills:** os scripts de gate moram no pacote `gates/` (`sdd-gates`), nunca dentro de uma pasta de skill. O Genie Code se recusa a executar scripts dentro de `.assistant/skills` e a fazer `pip install` do GitHub, então no Databricks o repo é montado uma segunda vez como Git Folder `sdd-gates`, fora de `.assistant`, e o agente roda `PYTHONPATH=<sdd-gates>/gates python3 -m sdd_gates <gate>`. A skill diz quando rodar o gate e a versão mínima; o pacote diz se passou. Mudou o comportamento de um gate: suba `__version__` e a versão mínima no `sdd-workflow`.

**Paradigma skills-first:** as skills `sdd-*` usam as skills `@databricks-*` curadas pelo time Databricks ao invés de KB domains.

**sdd-doc + state:** a `@sdd-doc` é um hook transversal chamado ao final de **cada** fase — lê a `jira_key` do ledger `.sdd/features/{FEATURE}/state.md` (criado no Define), monta um comentário a partir do seu `JIRA_UPDATE_TEMPLATE.md`, faz **preview** e então posta no Jira + transiciona o ticket (MCP: `jira_get_issue`, `jira_get_transitions`, `jira_add_comment`, `jira_transition_issue`). Sem `jira_key` — ou com MCP Jira indisponível — → modo pendente (não escreve).

**Artefatos SDD** (DEFINE, ADR, DESIGN, BUILD_REPORT, SHIPPED, state) são criados no repositório do projeto em `docs/specs/`, `docs/adr/`, `docs/designs/` e `.sdd/`.

## Harness & Guardrails

> **Agent = Model + Harness** — framing do paper [*The New SDLC With Vibe Coding*](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding) (Google, Day 1, mai/2026). O modelo é o motor; o **harness** é tudo em volta que faz ele *terminar* a tarefa. Regra prática do paper: **a maioria das falhas de agente é falha de configuração, não do modelo** — ao errar, revisar o harness antes de culpar o modelo.

Este repositório **é** um harness. Mapa dos 6 componentes:

| Componente | Onde vive aqui | Status |
|---|---|---|
| **Instructions & Rule Files** | `CLAUDE.md`, `AGENTS.md` e os `SKILL.md` das skills (incl. a família `sdd-*`) | ✅ |
| **Tools** | MCP Confluence (`confluence_get_page`) + Jira (`jira_get_issue`, `jira_get_transitions`, `jira_add_comment`, `jira_transition_issue`, `jira_create_issue`) — limite de 20 ferramentas | ✅ |
| **Sandbox / execução** | Genie Code Agent mode no workspace Databricks; compute definido no Contexto Técnico do DEFINE | ✅ |
| **Orchestration** | Tamanho da feature (Pequeno → Complexo) escolhe as etapas + fim de etapa; handoffs Define→ADR→PO→Design→Build→Ship; delegação às `@databricks-*` pela coluna "Constrói com" do DESIGN; `sdd-doc` como hook transversal | ✅ |
| **Guardrails / Hooks** | Gates de fase (tabela abaixo) — hoje **prompt-level** (checklists nos agentes), **não** hooks determinísticos | ⚠️ parcial |
| **Observability** | Ledger `.sdd/features/{FEATURE}/state.md` (trajetória das fases + log de ações no Jira), `BUILD_REPORT_*`, `SHIPPED_*`, archive | ⚠️ sem custo/latência/evals |

### Guardrails inegociáveis

Regras que o agente **nunca** deve esquecer — valem em qualquer fase:

| Guardrail | Onde é aplicado |
|---|---|
| Nunca commitar direto em `main` (Golden Rule) | Git Workflow |
| Sem credenciais/segredos hardcoded | Gate do Build |
| **Preview antes de qualquer escrita externa** (comentário, transição, criação de issue) | `sdd-doc`, `sdd-po` |
| Operar somente na `jira_key` do state — nunca busca (`jira_search`) | `sdd-doc`, `sdd-po` |
| Confluence: só `confluence_get_page` na URL dada — nunca `confluence_search` | `sdd-define` |
| Não editar skills `databricks-*` à mão (o sync sobrescreve) | Proveniência + `OWN_SKILLS` |
| `python3 -m sdd_gates define` verde e aprovação gravada antes de sair do Define; `--aprovado` antes do Build | Gate do Define (pacote `gates/`) |
| ADR é vinculante — não reabrir decisões no Design/Build | `sdd-design` |
| Aprovação da spec e do plano gravada com as palavras do usuário — nunca inventada | Contrato de execução (`sdd-workflow`) |
| Raio de ação: aprovação libera só branch da feature e ambiente de desenvolvimento; deploy fora do dev, tabela de produção, grant e schedule pedem ok explícito | Contrato de execução (`sdd-workflow`) |
| Teste nasce do critério de aceite; nunca enfraquecer, pular ou apagar teste para passar | Contrato de execução (`sdd-workflow`) |

**Lacuna conhecida:** esses guardrails são *instruções*, não código determinístico. O paper é explícito que hooks existem justamente para "o que o agente nunca deveria esquecer mas sempre esquece". Fechar isso exige enforcement real (pre-commit, `PreToolUse`, branch protection) — ver [`BACKLOG.md`](BACKLOG.md) itens 4 e 7.

### Loop de feedback do harness

Quando um agente fizer algo que não deveria repetir, **virar regra**: adicionar o guardrail na tabela acima e no agente da fase correspondente, em vez de corrigir caso a caso. O harness é versionado e revisado como código.

## docs/

Documentação de referência sobre features do Genie Code extraída de fontes Databricks:

| Arquivo | Conteúdo |
|---------|---------|
| `agent-skills.md` | Como funcionam as Agent Skills, auto-load e invocação |
| `custom-instructions.md` | Workspace vs user instructions, limites e precedência |
| `genie-code-overview.md` | Visão geral do Genie Code (Agent mode vs Chat mode) |
| `mcp-integration.md` | Configuração MCP, limite de 20 ferramentas, restrições |
| `pipeline-development.md` | Desenvolvimento de pipelines no Databricks |
| `spec-driven-development.md` | Conceito SDD e como usar o sdd-workflow |
| `tips-and-tricks.md` | Boas práticas e dicas para o Genie Code |

## Git Workflow — Golden Rule

**Nunca commitar direto em `main`.** Sempre:
1. `git checkout main && git pull origin main`
2. Criar branch a partir do main
3. Fazer changes e commitar
4. Push e abrir PR
5. Aguardar o usuário fazer merge

## Key Concepts

- **Genie Code**: agente AI autônomo do Databricks (Agent mode + Chat mode)
- **Agent Skills**: só funcionam em Agent mode; carregadas automaticamente ou via `@skill-name`
- **MCP**: limitado a 20 ferramentas por workspace; só em Agent mode
- **Custom Instructions**: Workspace (`Workspace/.assistant_workspace_instructions.md`) tem precedência sobre user (`/Users/<username>/.assistant_instructions.md`); limite de 20k chars
- **Skills-first**: este repo usa skills Databricks curadas no lugar de KB domains locais
