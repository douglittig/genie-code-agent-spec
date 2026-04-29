# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`genie-code-agent-spec` — repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code. **Genie Code first**: todas as decisões de design priorizam o paradigma do Genie Code (Agent mode + `@skill-name`), não o paradigma de slash commands do Claude Code CLI.

## Repository Layout

```
.claude/skills/          # 28 skills (Databricks + SDD workflow + Python + Spark)
docs/                    # Documentação de referência sobre features do Genie Code
assets/                  # Assets locais (PDFs, repos fonte) — gitignored
```

## Agent Skills (`.claude/skills/`)

Cada subpasta é uma skill autocontida seguindo o padrão open Agent Skills:
- `SKILL.md` — frontmatter (`name`, `description`) + conteúdo que o agente lê
- Arquivos de referência opcionais (`.md`, `.py`, `.sh`)

**Para criar uma nova skill:** copiar `.claude/skills/TEMPLATE/` e editar `SKILL.md`.

O índice completo das skills está no **[README.md](README.md)**, organizado por categoria (IA & ML, Dados & SQL, Plataforma Databricks, Aplicações, Desenvolvimento & Workflow).

### Skills de Workflow (essenciais para todo desenvolvimento)

| Skill | Fase | Propósito |
|-------|------|---------|
| `sdd-workflow` | 1 e 4 | Fase 1: Brainstorm + Define via MCP Confluence. Fase 4: Design + Build + Ship (dentro do @dev-workflow) |
| `dev-workflow` | 4 | Fluxo de desenvolvimento: discussão → branch → código → validação → review → PR → merge |
| `code-reviewer` | 4 | Code review: segurança, qualidade, performance, data engineering |
| `staff-engineer` | 2 | Revisão de spec, discussão arquitetural e geração de ADR (`docs/adr/`) |
| `po` | 3 | Epic → Stories (Fibonacci) → Tasks no Jira — **em desenvolvimento** |

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
