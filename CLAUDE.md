# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Status:** O workflow SDD foi decomposto em **skills autocontidas com prefixo `sdd-*`** (alinhado à mudança da Databricks que trata cada skill como um ativo individual, em vez de agentes encadeados dentro de uma skill). `@sdd-workflow` orquestra as fases; `@sdd-brainstorm`, `@sdd-define`, `@sdd-design`, `@sdd-build` e `@sdd-ship` executam cada uma, com `@sdd-staff-engineer` (ADR), `@sdd-po` (Stories/Tasks no Jira), `@sdd-iterate` (mudanças mid-stream) e **documentação automática no Jira via `@sdd-doc`** ao final de cada fase. Ainda em desenvolvimento: `@sdd-dev-workflow` e `@sdd-code-reviewer`.

## Project

`genie-code-agent-spec` — repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code. **Genie Code first**: todas as decisões de design priorizam o paradigma do Genie Code (Agent mode + `@skill-name`), não o paradigma de slash commands do Claude Code CLI.

## Repository Layout

```
<skill-name>/            # 41 skills na raiz (Databricks + SDD workflow + Python + Spark)
docs/                    # Documentação de referência sobre features do Genie Code
assets/                  # documentation/ versionada (PDFs de referência); repos/ gitignored
.claude/                 # Claude Code CLI local — gitignored, exceto .claude/skills/ (run-genie-code-agent-spec: validador do repo)
```

> **Como usar no Genie Code:** carregue este repo como Git Folder em `Workspace/.assistant/skills/`. As skills ficam disponíveis automaticamente em Agent mode.

> **Sem build/lint/test:** este é um repositório de conteúdo (Markdown + arquivos de referência), não uma aplicação. Não há `package.json`, `pyproject.toml` nem pipeline de CI — a "compilação" é o Genie Code/Claude Code lendo os `SKILL.md`. Validar uma mudança = revisar o Markdown e confirmar que o frontmatter está correto.

> **Arquivos de instrução paralelos:** [`CLAUDE.md`](CLAUDE.md) (Claude Code) e [`AGENTS.md`](AGENTS.md) (Genie Code) cobrem o mesmo conteúdo para dois agentes. Ao editar um, **atualizar o outro** para mantê-los em sincronia. [`BACKLOG.md`](BACKLOG.md) rastreia trabalho adiado (placeholders corporativos, skills futuras) — consultar antes de começar trabalho novo em `sdd-dev-workflow`/`sdd-code-reviewer`.

## Agent Skills (raiz do repositório)

Cada subpasta na raiz é uma skill autocontida seguindo o padrão open Agent Skills:
- `SKILL.md` — frontmatter (`name`, `description`) + conteúdo que o agente lê
- Arquivos de referência opcionais (`.md`, `.py`, `.sh`)

**O campo `description` do frontmatter dispara o auto-load.** O agente decide carregar uma skill comparando o pedido do usuário com a `description` — por isso as skills `databricks-*` escrevem descrições em inglês, ricas em gatilhos ("Use when building..., querying..., migrating..."). Ao criar/editar uma skill, otimizar a `description` para casar com como o usuário descreveria a tarefa, não para resumir o conteúdo.

**Para criar uma nova skill:** copiar `TEMPLATE/` e editar `SKILL.md`.

O índice completo das skills está no **[README.md](README.md)**, organizado por categoria (IA & ML, Dados & SQL, Plataforma Databricks, Aplicações, Desenvolvimento & Workflow).

### Proveniência: skills upstream vs. skills próprias

O prefixo indica a origem da skill:

- **`databricks-*`** + `spark-python-data-source` + `TEMPLATE` → vêm do upstream [`databricks-solutions/ai-dev-kit`](https://github.com/databricks-solutions/ai-dev-kit). ⚠️ **NÃO editar à mão** — o sync sobrescreve. Para mudar, contribuir no upstream.
- **`sdd-*`** e **`custom-*`** → skills **nossas**, não existem no upstream, livres para editar. `sdd-*` = skills do workflow de Spec-Driven Development; `custom-*` = demais skills próprias.

- **Sincronização:** [`.github/workflows/sync-databricks-skills.yml`](.github/workflows/sync-databricks-skills.yml) faz sparse checkout efêmero do upstream, copia as pastas para a raiz e abre um PR. O upstream **nunca** é commitado aqui (sem submodule/subtree). Roda semanalmente + `workflow_dispatch`.
- **Versão fixada:** última tag semver do upstream, registrada em `databricks-skills.lock` (gerado pelo workflow).
- **Origem das pastas upstream:** a maioria vem de `databricks-skills/`. Exceção: **`databricks-python-dev`** vem de `.claude/skills/python-dev` do upstream (mapeado para `databricks-python-dev` no sync).
- **Skills NOSSAS, editáveis** (prefixos `sdd-` e `custom-`, salvaguardadas em `OWN_SKILLS`): `sdd-workflow`, `sdd-brainstorm`, `sdd-define`, `sdd-design`, `sdd-build`, `sdd-ship`, `sdd-iterate`, `sdd-doc`, `sdd-staff-engineer`, `sdd-po`, `sdd-dev-workflow`, `sdd-code-reviewer`, `custom-test-generator`. O workflow nunca as sobrescreve.

### Skills de Workflow (família `sdd-*`)

| Skill | Fase | Status | Propósito |
|-------|------|--------|-----------|
| `sdd-workflow` | — | **PRONTO** | Orquestrador: fases, gates, handoffs e Protocolo de Fim-de-Fase |
| `sdd-brainstorm` | 0 | **PRONTO** | Exploração de ideia, comparação de abordagens, YAGNI → `docs/specs/BRAINSTORM_*.md` |
| `sdd-define` | 1 | **PRONTO** | Define via MCP Confluence → `docs/specs/DEFINE_*.md` (+ captura `jira_key` e cria o state) |
| `sdd-staff-engineer` | 2 | **PRONTO** | Revisão de spec, decisão arquitetural → `docs/adr/ADR_*.md` |
| `sdd-po` | 3 | **PRONTO** | Epic → Stories (Fibonacci) → Tasks no Jira → `docs/planning/STORIES_*.md` |
| `sdd-design` | 4 | **PRONTO** | Arquitetura + File Manifest a partir do DEFINE/ADR → `docs/designs/DESIGN_*.md` |
| `sdd-build` | 5 | **PRONTO** | Implementação delegando às `@databricks-*` → código + `BUILD_REPORT_*.md` |
| `sdd-ship` | 6 | **PRONTO** | Archive + lições aprendidas + fechamento do ticket → `SHIPPED_*.md` |
| `sdd-iterate` | cross | **PRONTO** | Mudanças mid-stream com análise de cascata |
| `sdd-doc` | cross | **PRONTO** | Hook de fim de fase: comentário + transição no Jira (MCP) |
| `sdd-dev-workflow` | 4+ | EM DESENVOLVIMENTO | Branch → código → validação → PR → merge |
| `sdd-code-reviewer` | 4+ | EM DESENVOLVIMENTO | Code review: segurança, qualidade, performance |

### Arquitetura do workflow SDD — skills autocontidas

Cada fase é uma **skill de primeira classe na raiz do repo** (padrão de ativos do Genie Code) — não há mais `agents/` nem `templates/` compartilhados. `sdd-workflow/SKILL.md` é só o orquestrador: descreve fases, gates e handoffs e roteia para a skill de cada fase. Cada skill de fase carrega **seu próprio template** ao lado do `SKILL.md` (ex.: `sdd-define/DEFINE_TEMPLATE.md` + `STATE_TEMPLATE.md`, `sdd-doc/JIRA_UPDATE_TEMPLATE.md`).

**Paradigma skills-first:** as skills `sdd-*` usam as skills `@databricks-*` curadas pelo time Databricks ao invés de KB domains.

**sdd-doc + state:** a `@sdd-doc` é um hook transversal chamado ao final de **cada** fase — lê a `jira_key` do ledger `.claude/sdd/state/{FEATURE}.md` (criado no Define), monta um comentário a partir do seu `JIRA_UPDATE_TEMPLATE.md`, faz **preview** e então posta no Jira + transiciona o ticket (MCP: `jira_get_issue`, `jira_get_transitions`, `jira_add_comment`, `jira_transition_issue`). Sem `jira_key` — ou com MCP Jira indisponível — → modo pendente (não escreve).

**Artefatos SDD** (DEFINE, ADR, DESIGN, BUILD_REPORT, SHIPPED, state) são criados no repositório do projeto em `docs/specs/`, `docs/adr/`, `docs/designs/` e `.claude/sdd/`.

## Harness & Guardrails

> **Agent = Model + Harness** — framing do paper *The New SDLC with Vibe Coding* (Google, Day 1, mai/2026; PDF em `assets/documentation/`). O modelo é o motor; o **harness** é tudo em volta que faz ele *terminar* a tarefa. Regra prática do paper: **a maioria das falhas de agente é falha de configuração, não do modelo** — ao errar, revisar o harness antes de culpar o modelo.

Este repositório **é** um harness. Mapa dos 6 componentes:

| Componente | Onde vive aqui | Status |
|---|---|---|
| **Instructions & Rule Files** | `CLAUDE.md`, `AGENTS.md` e os `SKILL.md` das skills (incl. a família `sdd-*`) | ✅ |
| **Tools** | MCP Confluence (`confluence_get_page`) + Jira (`jira_get_issue`, `jira_get_transitions`, `jira_add_comment`, `jira_transition_issue`, `jira_create_issue`) — limite de 20 ferramentas | ✅ |
| **Sandbox / execução** | Genie Code Agent mode no workspace Databricks; compute definido no Contexto Técnico do DEFINE | ✅ |
| **Orchestration** | 5 fases + Protocolo de Fim-de-Fase; handoffs Define→ADR→PO→Design→Build→Ship; delegação por File Manifest às `@databricks-*`; `sdd-doc` como hook transversal | ✅ |
| **Guardrails / Hooks** | Gates de fase (tabela abaixo) — hoje **prompt-level** (checklists nos agentes), **não** hooks determinísticos | ⚠️ parcial |
| **Observability** | Ledger `.claude/sdd/state/{FEATURE}.md` (trajetória das fases + log de ações no Jira), `BUILD_REPORT_*`, `SHIPPED_*`, archive | ⚠️ sem custo/latência/evals |

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
| Clarity Score ≥ 12/15 antes de avançar do Define | Gate do Define |
| ADR é vinculante — não reabrir decisões no Design/Build | `sdd-design` |

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
