# genie-code-agent-spec

Repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code.

> **Status:** Fases 1 e 2 prontas para uso. Fases 3 e 4 em desenvolvimento — não testar em ambiente real ainda.

---

## Fluxo de Desenvolvimento

O desenvolvimento de features segue 4 fases com configurações MCP distintas por fase. Cada fase produz um artefato que alimenta a próxima — sem dependência de contexto online entre fases.

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1 — Spec                    MCP: Confluence (12 slots)     │
│                                                                 │
│  Quem: Chapter leader / Tech lead                               │
│  Skill: @sdd-workflow → define <url-confluence>                 │
│  Output: docs/specs/DEFINE_{FEATURE}.md                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 2 — Arquitetura             MCP: nenhum                    │
│                                                                 │
│  Quem: Staff Engineer / Tech lead                               │
│  Skill: @staff-engineer                                         │
│  Output: docs/adr/ADR_{FEATURE}.md                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 3 — Planejamento  [EM DESENVOLVIMENTO]                     │
│                                  MCP: Jira (14 slots)           │
│  Quem: Product Owner / Tech lead                                │
│  Skill: @po                                                     │
│  Output: Epic + Stories (Fibonacci) + Tasks no Jira             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 4 — Desenvolvimento  [EM DESENVOLVIMENTO]                  │
│                             MCP: Bitbucket (~6) + Jira (14)     │
│  Quem: Desenvolvedor                                            │
│  Skills: @sdd-workflow (Design → Build → Ship)                  │
│          @dev-workflow  (branch → commit → PR → merge)          │
│  Output: branch → código → PR → ticket Jira atualizado          │
└─────────────────────────────────────────────────────────────────┘
```

### Por que fases separadas?

O Genie Code em Agent mode suporta no máximo **20 ferramentas MCP** simultaneamente. Cada produto Atlassian consome slots:

| MCP | Slots |
|-----|-------|
| Confluence | 12 |
| Jira | 14 |
| Bitbucket (mínimo dev-workflow) | ~6 |
| **Total se todos juntos** | **~32 — estoura o limite** |

A separação em fases resolve o problema: cada fase ativa apenas os MCPs que precisa, mantendo sempre abaixo de 20 slots.

### Documentação por fase

Todos os artefatos ficam no repositório do projeto, dentro de `docs/`:

```
projeto/
├── databricks.yml
├── resources/
├── src/
├── tests/
└── docs/
    ├── specs/      # DEFINE_{FEATURE}.md  — saída da Fase 1
    ├── adr/        # ADR_{FEATURE}.md     — saída da Fase 2
    └── designs/    # DESIGN_{FEATURE}.md  — saída do sdd-workflow
```

### Configuração MCP por fase

| Fase | Ativar | Desativar |
|------|--------|-----------|
| 1 — Spec | Confluence | Jira, Bitbucket |
| 2 — Arquitetura | — | Todos |
| 3 — Planejamento | Jira | Confluence, Bitbucket |
| 4 — Desenvolvimento | Bitbucket + Jira | Confluence |

> Guia de configuração do Bitbucket MCP: [`docs/bitbucket-mcp-guide.md`](docs/bitbucket-mcp-guide.md)

---

## Mapa de Interação Detalhado

Mostra todos os pontos de entrada, o que cada nó chama, para onde vai, o que é fixo e o que é opcional.

### Diagrama

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  ITERATE — cross-cutting (disponível em qualquer fase)                       ║
║  @sdd-workflow / iterate-agent  →  atualiza artefato da fase + cascata       ║
╚══════════════════════════════════════════════════════════════════════════════╝

ENTRADAS                                 NÓS
────────                                 ────────────────────────────────────────

(A) Ideia vaga ──────────────────────→   ┌── [0] BRAINSTORM ──────────────────┐
                                         │  skill:  @sdd-workflow             │ OPCIONAL
                                         │  mcp:    —                         │
                                         │  output: docs/specs/BRAINSTORM_*.md│
                                         │  gate:   usuário confirmou abord.  │
                                         └───────────────────┬────────────────┘
                                                            │
(B) Notas / docs brutos ────────────────────────────────────┼─────────────────┐
(C) DEFINE_*.md já existe ──────────────────────────────────┼─────────────────┤
(D) URL Confluence ─────────────────────────────────────────┼─────────────────┤
                                                            ▼                 ▼
                                         ┌── [1] DEFINE ───────────────────────┐
                                         │  skill:  @sdd-workflow              │ OBRIGATÓRIO
                                         │  mcp:    Confluence (12 slots)      │
                                         │  output: docs/specs/DEFINE_*.md     │
                                         │  gate:   Clarity Score ≥ 12/15      │
                                         └───────────────────┬─────────────────┘
                                                             │
                                                             ▼
                                         ┌─ ─[2] ARQUITETURA ──────────────────┐
                                         │  skill:  @staff-engineer            │ OBRIGATÓRIO
                                         │  mcp:    —                          │
                                         │  output: docs/adr/ADR_*.md          │
                                         └──────────────────┬──────────────────┘
                                                            │
                                              ┌─────────────┴─────────────┐
                                              ▼                           │
                          ┌── [3] PLANEJAMENTO ────────────┐ OPCIONAL     │
                          │  skill:  @po  [em desenv.]     │              │
                          │  mcp:    Jira (14 slots)       │              │
                          │  output: Epic + Stories + Tasks│              │
                          └──────────────────┬─────────────┘              │
                                             └─────────────────────────▶  │
                                                            ▼
                                         ┌── [4] DESIGN ───────────────────────┐
                                         │  skill:  @sdd-workflow              │ OBRIGATÓRIO
                                         │  mcp:    —                          │
                                         │  input:  ADR_*.md (vinculante)      │
                                         │  output: docs/designs/DESIGN_*.md   │
                                         │  gate:   File Manifest completo     │
                                         └───────────────────┬─────────────────┘
                                                             │
                              ┌──────────────────────────────┤ paralelo
                              ▼                              ▼
                 @dev-workflow (criar branch)  ┌── [5] BUILD ───────────────────┐
                                               │  skill:   @sdd-workflow        │ OBRIGATÓRIO
                                               │  mcp:     —                    │
                                               │  delega:  @databricks-* skills │
                                               │  output:  código gerado        │
                                               │           BUILD_REPORT_*.md    │
                                               │  gate:    lint + testes ok,    │
                                               │           sem credenciais      │
                                               └──────────────────┬─────────────┘
                              ┌─────────────────────────────┤ paralelo
                              ▼                             ▼
                 @dev-workflow (commit + PR)   ┌── [6] SHIP ────────────────────┐
                                               │  skill:   @sdd-workflow        │ OBRIGATÓRIO
                                               │  mcp:     Jira (14 slots)      │
                                               │  delega:  @dev-workflow (PR)   │
                                               │  delega:  @code-reviewer ★     │
                                               │  output:  SHIPPED_*.md         │
                                               │           Jira ticket fechado  │
                                               │  gate:    acceptance tests ok  │
                                               └────────────────────────────────┘

★ RECOMENDADO
```

### Nós — Referência Rápida

| Nó | Skill | MCP ativo | Output | Gate para avançar | Status |
|----|-------|-----------|--------|-------------------|--------|
| [0] Brainstorm | @sdd-workflow | — | `docs/specs/BRAINSTORM_*.md` | Usuário confirmou abordagem → vai para [1] | OPCIONAL |
| [1] Define | @sdd-workflow | Confluence | `docs/specs/DEFINE_*.md` | Clarity Score ≥ 12/15 | PRONTO |
| [2] Arquitetura | @staff-engineer | — | `docs/adr/ADR_*.md` | ADR revisado e aceito | PRONTO |
| [3] Planejamento | @po | Jira | Epic + Stories + Tasks | — | EM DESENVOLVIMENTO |
| [4] Design | @sdd-workflow | — | `docs/designs/DESIGN_*.md` | File Manifest completo | EM DESENVOLVIMENTO |
| [5] Build | @sdd-workflow | — | código + `BUILD_REPORT_*.md` | Lint + testes ok, sem credenciais | EM DESENVOLVIMENTO |
| [6] Ship | @sdd-workflow | Jira | `SHIPPED_*.md` + Jira fechado | Acceptance tests ok | EM DESENVOLVIMENTO |
| Iterate | @sdd-workflow | — | Artefato da fase atualizado | — | CROSS-CUTTING |

### Delegações em Fase 4

Durante os nós [4] a [6], o @sdd-workflow coordena com outras skills:

| Ação | Delegado para | Quando |
|------|--------------|--------|
| Criar branch git | @dev-workflow | Início do Design [4] |
| Implementar cada arquivo | @databricks-* (mapeado no File Manifest) | Build [5] |
| Commit + PR | @dev-workflow | Ship [6] |
| Code review | @code-reviewer | Ship [6] — recomendado |

---

## Índice de Skills

Skills ficam em `.claude/skills/`. Cada skill é uma pasta com `SKILL.md` (frontmatter + instruções) e arquivos de referência opcionais. No Genie Code, são invocadas via `@skill-name` em Agent mode; no Claude Code CLI, são carregadas automaticamente.

### IA & ML

| Skill | Descrição |
|-------|-----------|
| [`databricks-agent-bricks`](.claude/skills/databricks-agent-bricks/) | Knowledge Assistants para Q&A sobre documentos, Genie Spaces para exploração SQL e Supervisor Agents para orquestração multi-agente |
| [`databricks-ai-functions`](.claude/skills/databricks-ai-functions/) | Funções AI nativas do Databricks SQL (`ai_classify`, `ai_extract`, `ai_summarize`, etc.) para adicionar IA diretamente em pipelines SQL e PySpark |
| [`databricks-aibi-dashboards`](.claude/skills/databricks-aibi-dashboards/) | Criação de dashboards AI/BI (Lakeview) — exige validação de todas as queries via `execute_sql` antes do deploy |
| [`databricks-genie`](.claude/skills/databricks-genie/) | Criação e consulta de Genie Spaces para exploração SQL em linguagem natural; inclui Conversation API e migração entre workspaces |
| [`databricks-mlflow-evaluation`](.claude/skills/databricks-mlflow-evaluation/) | Avaliação de agentes GenAI com MLflow 3: `mlflow.genai.evaluate()`, scorers, MemAlign e GEPA para otimização de prompts |
| [`databricks-model-serving`](.claude/skills/databricks-model-serving/) | Deploy e consulta de endpoints de Model Serving para modelos MLflow, ChatAgent/ResponsesAgent e agentes com UC Functions |
| [`databricks-vector-search`](.claude/skills/databricks-vector-search/) | Criação e consulta de índices de Vector Search para RAG, busca semântica e similaridade |

### Dados & SQL

| Skill | Descrição |
|-------|-----------|
| [`databricks-dbsql`](.claude/skills/databricks-dbsql/) | Recursos avançados do Databricks SQL: SQL warehouses, SQL scripting, stored procedures e performance tuning |
| [`databricks-iceberg`](.claude/skills/databricks-iceberg/) | Tabelas Apache Iceberg no Databricks: Managed Iceberg, External Reads (Uniform), Iceberg REST Catalog e interop com Snowflake |
| [`databricks-metric-views`](.claude/skills/databricks-metric-views/) | Criação e gestão de metric views no Unity Catalog para definir KPIs e métricas de negócio padronizadas em YAML |
| [`databricks-spark-declarative-pipelines`](.claude/skills/databricks-spark-declarative-pipelines/) | Lakeflow Spark Declarative Pipelines (SDP/DLT): streaming tables, materialized views, CDC, SCD Type 2 e Auto Loader |
| [`databricks-spark-structured-streaming`](.claude/skills/databricks-spark-structured-streaming/) | Spark Structured Streaming em produção: Kafka, Real-Time Mode, triggers, operações stateful, checkpoints e stream-stream joins |
| [`databricks-synthetic-data-gen`](.claude/skills/databricks-synthetic-data-gen/) | Geração de dados sintéticos realistas com Spark + Faker em escala, múltiplos formatos (Parquet/JSON/CSV/Delta) |
| [`databricks-unity-catalog`](.claude/skills/databricks-unity-catalog/) | System tables (audit, lineage, billing) e operações com volumes (`/Volumes/`) no Unity Catalog |
| [`databricks-zerobus-ingest`](.claude/skills/databricks-zerobus-ingest/) | Clientes Zerobus Ingest para ingestão near real-time em tabelas Delta via gRPC, sem message bus |
| [`spark-python-data-source`](.claude/skills/spark-python-data-source/) | Data sources Python customizados para Spark (PySpark DataSource API): leitores/escritores batch e streaming para sistemas externos |

### Plataforma Databricks

| Skill | Descrição |
|-------|-----------|
| [`databricks-bundles`](.claude/skills/databricks-bundles/) | Declarative Automation Bundles (DABs): criação, configuração e deploy multi-ambiente com CICD |
| [`databricks-config`](.claude/skills/databricks-config/) | Gestão de conexões de workspace: verificar perfil atual, trocar workspace e autenticar via `~/.databrickscfg` |
| [`databricks-docs`](.claude/skills/databricks-docs/) | Referência de documentação Databricks via llms.txt — usar quando outras skills não cobrirem o tópico |
| [`databricks-execution-compute`](.claude/skills/databricks-execution-compute/) | Execução de código e gestão de compute no Databricks: serverless, clusters, Python/Scala/SQL/R |
| [`databricks-jobs`](.claude/skills/databricks-jobs/) | Criação, listagem, execução e monitoramento de Databricks Jobs via CLI, Python SDK e Asset Bundles |
| [`databricks-python-sdk`](.claude/skills/databricks-python-sdk/) | SDK Python do Databricks, Databricks Connect, CLI e REST API — referência completa com exemplos |

### Aplicações

| Skill | Descrição |
|-------|-----------|
| [`databricks-app-python`](.claude/skills/databricks-app-python/) | Aplicações Python no Databricks (Dash, Streamlit, Gradio, Flask, FastAPI, Reflex) com OAuth, SQL warehouse e model serving |
| [`databricks-lakebase-autoscale`](.claude/skills/databricks-lakebase-autoscale/) | Lakebase Autoscaling (PostgreSQL gerenciado): autoscaling, scale-to-zero, branching, synced tables e OAuth |
| [`databricks-lakebase-provisioned`](.claude/skills/databricks-lakebase-provisioned/) | Lakebase Provisioned (PostgreSQL OLTP): criação de instâncias, conexão de apps, reverse ETL e memória de agentes |
| [`databricks-unstructured-pdf-generation`](.claude/skills/databricks-unstructured-pdf-generation/) | Geração de PDFs a partir de HTML e upload para volumes do Unity Catalog |

### Desenvolvimento & Workflow

| Skill | Fase | Descrição |
|-------|------|-----------|
| [`sdd-workflow`](.claude/skills/sdd-workflow/) | 1 e 4 | Workflow Spec-Driven Development em 5 fases (Brainstorm → Define → Design → Build → Ship). Fase 1: Brainstorm + Define via MCP Confluence. Fase 4: Design + Build + Ship (dentro do @dev-workflow) |
| [`dev-workflow`](.claude/skills/dev-workflow/) | 4 | Fluxo de desenvolvimento seguro: discussão → branch → código → validação → auto-review → PR → merge |
| [`code-reviewer`](.claude/skills/code-reviewer/) | 4 | Review de segurança, qualidade de código, performance e boas práticas para projetos Databricks e Python |
| [`python-dev`](.claude/skills/python-dev/) | 4 | Padrões de desenvolvimento Python: uv, type hints, Ruff, Pyright e pytest |
| [`test-generator`](.claude/skills/test-generator/) | 4 | Geração de testes unitários pytest, testes de integração e fixtures para código Python e data engineering |
| [`staff-engineer`](.claude/skills/staff-engineer/) | 2 | Revisão de spec, discussão arquitetural e geração de ADR (`docs/adr/`) |
| `po` | 3 | Quebra de Epic em Stories (Fibonacci) e Tasks no Jira — **em desenvolvimento** |

---

## Estrutura do Repositório

```
.claude/skills/          # 30 skills (Databricks + SDD workflow + Python)
docs/                    # Documentação de referência extraída de fontes Databricks
assets/                  # Assets locais (PDFs, repos) — gitignored
```

## Git Workflow

Nunca commitar direto em `main`. Sempre criar branch → PR → aguardar merge.
