# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`genie-code-agent-spec` — a spec-driven development repository for using Databricks Genie Code with agent skills, custom instructions, and MCP integrations.

## Repository Layout

```
.claude/skills/          # 28 Databricks agent skills (for Genie Code / Claude Code)
docs/                    # Reference documentation extracted from Databricks sources
assets/                  # Local assets (PDFs, source repos) — gitignored, not committed
```

## Agent Skills (`.claude/skills/`)

Each subfolder is a self-contained skill following the open Agent Skills standard:
- `SKILL.md` — frontmatter (`name`, `description`) + content the agent reads
- Optional reference files (`.md`) and scripts (`.py`, `.sh`)

Skills are sourced from the [Databricks AI Dev Kit](https://github.com/databricks/ai-dev-kit). Key skills:

| Skill | Purpose |
|-------|---------|
| `databricks-agent-bricks` | Knowledge Assistants, Genie Spaces, Supervisor Agents |
| `databricks-aibi-dashboards` | LAKEVIEW dashboard creation (mandatory 5-step validation workflow) |
| `databricks-bundles` | Databricks Asset Bundles (DABs) for deployment |
| `databricks-genie` | Genie Space CRUD and Conversation API |
| `databricks-mlflow-evaluation` | MLflow 3 GenAI evaluation, MemAlign, GEPA |
| `databricks-python-sdk` | Full SDK reference with examples |
| `databricks-spark-declarative-pipelines` | SDP / Lakeflow pipeline development |
| `databricks-unity-catalog` | Catalog, schema, governance, system tables |
| `python-dev` | uv, type hints, Ruff, Pyright, pytest standards |

## Git Workflow — Golden Rule

**Never commit directly to `main`.** Always:
1. `git checkout main && git pull origin main`
2. Create a new branch from main
3. Make changes and commit
4. Push and open a PR
5. Wait for the user to merge

## Key Concepts

- **Genie Code**: Databricks autonomous AI agent (Agent mode + Chat mode)
- **Agent Skills**: Only work in Agent mode; auto-loaded or invoked via `@skill-name`
- **MCP**: Limited to 20 tools across all servers; only in Agent mode
- **Custom Instructions**: Workspace (`Workspace/.assistant_workspace_instructions.md`) overrides user (`/Users/<username>/.assistant_instructions.md`); 20k char limit

See `docs/` for detailed documentation on each Genie Code feature.
