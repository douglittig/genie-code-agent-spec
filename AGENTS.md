# AGENTS.md

This file provides guidance to Genie Code when working with code in this repository.

> **Status:** As 5 fases do `@custom-sdd-workflow` (Brainstorm → Define → Design → Build → Ship) + `@custom-staff-engineer` (ADR) + `@custom-po` (Stories/Tasks no Jira) estão prontas para uso, com **documentação automática no Jira via `doc-agent`** ao final de cada fase. Ainda em desenvolvimento: `@custom-dev-workflow` e `@custom-code-reviewer`.

## Project

`genie-code-agent-spec` — repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code. **Genie Code first**: todas as decisões de design priorizam o paradigma do Genie Code (Agent mode + `@skill-name`), não o paradigma de slash commands do Claude Code CLI.

## Repository Layout

```
<skill-name>/            # 34 skills na raiz (Databricks + SDD workflow + Python + Spark)
docs/                    # Documentação de referência sobre features do Genie Code
assets/                  # Assets locais (PDFs, repos fonte) — gitignored
.claude/                 # Claude Code CLI local — gitignored
```

> **Como usar no Genie Code:** carregue este repo como Git Folder em `Workspace/.assistant/skills/`. As skills ficam disponíveis automaticamente em Agent mode.

## Agent Skills (raiz do repositório)

Cada subpasta na raiz é uma skill autocontida seguindo o padrão open Agent Skills:
- `SKILL.md` — frontmatter (`name`, `description`) + conteúdo que o agente lê
- Arquivos de referência opcionais (`.md`, `.py`, `.sh`)

**Para criar uma nova skill:** copiar `TEMPLATE/` e editar `SKILL.md`.

O índice completo das skills está no **[README.md](README.md)**, organizado por categoria (IA & ML, Dados & SQL, Plataforma Databricks, Aplicações, Desenvolvimento & Workflow).

### Proveniência: skills upstream vs. skills próprias

Há dois prefixos que indicam a origem da skill:

- **`databricks-*`** + `spark-python-data-source` + `TEMPLATE` → vêm do upstream [`databricks-solutions/ai-dev-kit`](https://github.com/databricks-solutions/ai-dev-kit). ⚠️ **NÃO editar à mão** — o sync sobrescreve. Para mudar, contribuir no upstream.
- **`custom-*`** → skills **nossas**, não existem no upstream, livres para editar.

- **Sincronização:** [`.github/workflows/sync-databricks-skills.yml`](.github/workflows/sync-databricks-skills.yml) faz sparse checkout efêmero do upstream, copia as pastas para a raiz e abre um PR. O upstream **nunca** é commitado aqui (sem submodule/subtree). Roda semanalmente + `workflow_dispatch`.
- **Versão fixada:** última tag semver do upstream, registrada em `databricks-skills.lock` (gerado pelo workflow).
- **Origem das pastas upstream:** a maioria vem de `databricks-skills/`. Exceção: **`databricks-python-dev`** vem de `.claude/skills/python-dev` do upstream (mapeado para `databricks-python-dev` no sync).
- **Skills NOSSAS, editáveis** (prefixo `custom-`, salvaguardadas em `OWN_SKILLS`): `custom-sdd-workflow`, `custom-staff-engineer`, `custom-po`, `custom-dev-workflow`, `custom-code-reviewer`, `custom-test-generator`. O workflow nunca as sobrescreve.

### Skills de Workflow

| Skill | Fase | Status | Propósito |
|-------|------|--------|-----------|
| `custom-sdd-workflow` (Brainstorm + Define) | 1 | **PRONTO** | Brainstorm + Define via MCP Confluence → `docs/specs/DEFINE_*.md` (+ captura `jira_key` no state) |
| `custom-staff-engineer` | 2 | **PRONTO** | Revisão de spec, decisão arquitetural → `docs/adr/ADR_*.md` |
| `custom-po` | 3 | **PRONTO** | Epic → Stories (Fibonacci) → Tasks no Jira → `docs/planning/STORIES_*.md` |
| `custom-sdd-workflow` (Design + Build + Ship) | 4 | **PRONTO** | Design + Build + Ship a partir do DEFINE/ADR aprovados |
| `custom-sdd-workflow` → `doc-agent` | — | **PRONTO** | Hook de fim de fase: comentário + transição no Jira (MCP) |
| `custom-dev-workflow` | 4 | EM DESENVOLVIMENTO | Branch → código → validação → PR → merge |
| `custom-code-reviewer` | 4 | EM DESENVOLVIMENTO | Code review: segurança, qualidade, performance |

### custom-sdd-workflow — estrutura especial

A skill `custom-sdd-workflow` tem subdivisões além do `SKILL.md`:

```
custom-sdd-workflow/
├── SKILL.md          # Entry point — orquestra as 5 fases + Protocolo de Fim-de-Fase
├── agents/           # 7 agentes (brainstorm, define, design, build, ship, iterate, doc-agent)
└── templates/        # 7 templates (BRAINSTORM, DEFINE, DESIGN, BUILD_REPORT, SHIPPED, STATE, JIRA_UPDATE)
```

**Paradigma skills-first:** agentes desta skill usam as skills `@databricks-*` curadas pelo time Databricks ao invés de KB domains.

**doc-agent + state:** o `doc-agent` é um hook transversal chamado ao final de **cada** fase — lê a `jira_key` do ledger `.claude/sdd/state/{FEATURE}.md` (criado no Define), monta um comentário a partir do `JIRA_UPDATE_TEMPLATE`, faz **preview** e então posta no Jira + transiciona o ticket (MCP: `jira_get_issue`, `jira_get_transitions`, `jira_add_comment`, `jira_transition_issue`). Sem `jira_key` → modo pendente (não escreve).

**Artefatos SDD** (DEFINE, ADR, DESIGN, BUILD_REPORT, SHIPPED, state) são criados no repositório do projeto em `docs/specs/`, `docs/adr/`, `docs/designs/` e `.claude/sdd/`.

## docs/

Documentação de referência sobre features do Genie Code extraída de fontes Databricks:

| Arquivo | Conteúdo |
|---------|---------|
| `agent-skills.md` | Como funcionam as Agent Skills, auto-load e invocação |
| `custom-instructions.md` | Workspace vs user instructions, limites e precedência |
| `genie-code-overview.md` | Visão geral do Genie Code (Agent mode vs Chat mode) |
| `mcp-integration.md` | Configuração MCP, limite de 20 ferramentas, restrições |
| `pipeline-development.md` | Desenvolvimento de pipelines no Databricks |
| `spec-driven-development.md` | Conceito SDD e como usar o custom-sdd-workflow |
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
