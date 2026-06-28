# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **Status:** Fases 1 e 2 prontas para uso (`@sdd-workflow` Define + `@staff-engineer`). Fases 3 e 4 em desenvolvimento — não usar `@po`, `@dev-workflow` nem as fases Design/Build/Ship do `@sdd-workflow` em ambiente real ainda.

## Project

`genie-code-agent-spec` — repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code. **Genie Code first**: todas as decisões de design priorizam o paradigma do Genie Code (Agent mode + `@skill-name`), não o paradigma de slash commands do Claude Code CLI.

## Repository Layout

```
<skill-name>/            # 33 skills na raiz (Databricks + SDD workflow + Python + Spark)
docs/                    # Documentação de referência sobre features do Genie Code
assets/                  # Assets locais (PDFs, repos fonte) — gitignored
.claude/                 # Claude Code CLI local — gitignored
```

> **Como usar no Genie Code:** carregue este repo como Git Folder em `Workspace/.assistant/skills/`. As skills ficam disponíveis automaticamente em Agent mode.

> **Sem build/lint/test:** este é um repositório de conteúdo (Markdown + arquivos de referência), não uma aplicação. Não há `package.json`, `pyproject.toml` nem pipeline de CI — a "compilação" é o Genie Code/Claude Code lendo os `SKILL.md`. Validar uma mudança = revisar o Markdown e confirmar que o frontmatter está correto.

> **Arquivos de instrução paralelos:** [`CLAUDE.md`](CLAUDE.md) (Claude Code) e [`AGENTS.md`](AGENTS.md) (Genie Code) cobrem o mesmo conteúdo para dois agentes. Ao editar um, **atualizar o outro** para mantê-los em sincronia. [`BACKLOG.md`](BACKLOG.md) rastreia trabalho adiado (placeholders corporativos, skills futuras) — consultar antes de começar trabalho novo em `dev-workflow`/`code-reviewer`.

## Agent Skills (raiz do repositório)

Cada subpasta na raiz é uma skill autocontida seguindo o padrão open Agent Skills:
- `SKILL.md` — frontmatter (`name`, `description`) + conteúdo que o agente lê
- Arquivos de referência opcionais (`.md`, `.py`, `.sh`)

**O campo `description` do frontmatter dispara o auto-load.** O agente decide carregar uma skill comparando o pedido do usuário com a `description` — por isso as skills `databricks-*` escrevem descrições em inglês, ricas em gatilhos ("Use when building..., querying..., migrating..."). Ao criar/editar uma skill, otimizar a `description` para casar com como o usuário descreveria a tarefa, não para resumir o conteúdo.

**Para criar uma nova skill:** copiar `TEMPLATE/` e editar `SKILL.md`.

O índice completo das skills está no **[README.md](README.md)**, organizado por categoria (IA & ML, Dados & SQL, Plataforma Databricks, Aplicações, Desenvolvimento & Workflow).

### Proveniência: skills upstream vs. skills próprias

⚠️ **As skills `databricks-*`, `spark-python-data-source` e `TEMPLATE` vêm do upstream [`databricks-solutions/ai-dev-kit`](https://github.com/databricks-solutions/ai-dev-kit) (`databricks-skills/`). NÃO editar à mão** — o sync sobrescreve. Para mudar uma delas, contribuir no upstream.

- **Sincronização:** [`.github/workflows/sync-databricks-skills.yml`](.github/workflows/sync-databricks-skills.yml) faz sparse checkout efêmero do upstream, copia as pastas para a raiz e abre um PR. O upstream **nunca** é commitado aqui (sem submodule/subtree). Roda semanalmente + `workflow_dispatch`.
- **Versão fixada:** última tag semver do upstream, registrada em `databricks-skills.lock` (gerado pelo workflow).
- **Skills NOSSAS, editáveis** (não existem no upstream): `sdd-workflow`, `staff-engineer`, `dev-workflow`, `code-reviewer`, `po`, `python-dev`, `test-generator`. O workflow tem uma salvaguarda (`OWN_SKILLS`) que nunca as sobrescreve.

### Skills de Workflow

| Skill | Fase | Status | Propósito |
|-------|------|--------|-----------|
| `sdd-workflow` | 1 | **PRONTO** | Brainstorm + Define via MCP Confluence → `docs/specs/DEFINE_*.md` |
| `staff-engineer` | 2 | **PRONTO** | Revisão de spec, decisão arquitetural → `docs/adr/ADR_*.md` |
| `po` | 3 | EM DESENVOLVIMENTO | Epic → Stories (Fibonacci) → Tasks no Jira |
| `sdd-workflow` (Design→Ship) | 4 | EM DESENVOLVIMENTO | Design + Build + Ship a partir do DEFINE aprovado |
| `dev-workflow` | 4 | EM DESENVOLVIMENTO | Branch → código → validação → PR → merge |
| `code-reviewer` | 4 | EM DESENVOLVIMENTO | Code review: segurança, qualidade, performance |

### sdd-workflow — estrutura especial

A skill `sdd-workflow` tem subdivisões além do `SKILL.md`:

```
sdd-workflow/
├── SKILL.md          # Entry point — orquestra as 5 fases
├── agents/           # 6 agentes por fase (brainstorm, define, design, build, ship, iterate)
└── templates/        # 5 templates de documentos SDD
```

**Paradigma skills-first:** agentes desta skill usam as skills `@databricks-*` curadas pelo time Databricks ao invés de KB domains.

**Artefatos SDD** (DEFINE, DESIGN, BUILD_REPORT, etc.) são criados no repositório do projeto em `docs/specs/`, `docs/designs/` e `.claude/sdd/`.

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
