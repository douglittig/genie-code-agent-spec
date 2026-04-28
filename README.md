# genie-code-agent-spec

Repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code.

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

| Skill | Descrição |
|-------|-----------|
| [`code-reviewer`](.claude/skills/code-reviewer/) | Review de segurança, qualidade de código, performance e boas práticas para projetos Databricks e Python |
| [`python-dev`](.claude/skills/python-dev/) | Padrões de desenvolvimento Python: uv, type hints, Ruff, Pyright e pytest |
| [`sdd-workflow`](.claude/skills/sdd-workflow/) | Workflow Spec-Driven Development em 5 fases (Brainstorm → Define → Design → Build → Ship) com integração Confluence e Jira via MCP |
| [`test-generator`](.claude/skills/test-generator/) | Geração de testes unitários pytest, testes de integração e fixtures para código Python e data engineering |

---

## Revisão de Coerência — sdd-workflow

A skill `sdd-workflow` passou por uma revisão de coerência. Três decisões de design foram identificadas e implementadas — ver [`.claude/skills/sdd-workflow/COHERENCE_REVIEW.md`](.claude/skills/sdd-workflow/COHERENCE_REVIEW.md) para o histórico completo.

---

## Estrutura do Repositório

```
.claude/skills/          # 30 skills (Databricks + SDD workflow + Python)
docs/                    # Documentação de referência extraída de fontes Databricks
assets/                  # Assets locais (PDFs, repos) — gitignored
```

## Git Workflow

Nunca commitar direto em `main`. Sempre criar branch → PR → aguardar merge.
