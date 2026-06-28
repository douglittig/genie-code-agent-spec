# genie-code-agent-spec

Repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code.

> **Status:** Fases 1 e 2 prontas para uso. Fases 3 e 4 em desenvolvimento — não testar em ambiente real ainda.

---

## Instalação e Uso

### Pré-requisitos

| Requisito | Detalhes |
|-----------|---------|
| Databricks workspace | Genie Code habilitado (Agent mode disponível) |
| Acesso de admin | Permissão para criar Git Folders em `Workspace/` |
| Git provider configurado | GitHub, GitLab ou Bitbucket conectado ao workspace |
| MCP por fase | Confluence (Fase 1), Jira (Fase 3/6), Bitbucket (Fase 4) |

---

### Passo 1 — Carregar o repositório no workspace

O Genie Code detecta skills em `Workspace/.assistant/skills/<skill-name>/SKILL.md` — **um nível** abaixo de `skills/`. Por isso o repo precisa ser montado **como** a pasta `skills/`, não dentro dela.

**Estrutura esperada:**
```
Workspace/
└── .assistant/
    └── skills/          ← este repo é montado AQUI
        ├── custom-sdd-workflow/
        │   └── SKILL.md
        ├── custom-staff-engineer/
        │   └── SKILL.md
        └── databricks-*/
            └── SKILL.md
```

**No Databricks:**

1. Acesse o painel lateral → **Workspace**
2. Navegue até `Workspace/` (raiz do workspace)
3. Crie a pasta `.assistant/` se não existir — clique com botão direito → **Create folder**
4. Entre na pasta `.assistant/` — **não crie `skills/` manualmente**
5. Clique com botão direito dentro de `.assistant/` → **Add Git Folder**
6. Cole a URL deste repositório: `https://github.com/<org>/genie-code-agent-spec`
7. Escolha a branch `main`
8. **Renomeie o Git Folder para `skills`** (o padrão seria o nome do repo)
9. Confirme — o Git Folder será criado em `Workspace/.assistant/skills/`

> **Por que o nome importa:** O Genie Code procura skills em `Workspace/.assistant/skills/<skill-name>/SKILL.md`. Se o folder for nomeado diferente de `skills`, o caminho quebra. As skills estão na raiz deste repo — com o nome correto, cada skill fica exatamente onde o Genie Code espera.

---

### Passo 2 — Verificar a instalação

Abra o **Genie Code** → mude para **Agent mode** → digite:

```
@custom-sdd-workflow
```

Se a skill aparecer como sugestão no autocomplete, a instalação está correta.

Para verificar todas as skills disponíveis:

```
Quais skills você tem disponíveis?
```

O agente listará as skills carregadas do `Workspace/.assistant/skills/`.

---

### Passo 3 — Configurar MCP por fase

Cada fase usa um conjunto diferente de MCPs. Configure os servidores MCP no Genie Code conforme a fase que vai executar:

| Fase | MCP necessário | Como ativar |
|------|---------------|-------------|
| **Fase 1 — Spec** | Confluence | Settings → MCP → adicionar servidor Confluence |
| **Fase 2 — Arquitetura** | Nenhum | Desativar todos os MCPs opcionais |
| **Fase 3 — Planejamento** | Jira | Settings → MCP → adicionar servidor Jira |
| **Fase 4 — Desenvolvimento** | Jira + Bitbucket | Ativar ambos |

> **Limite:** Genie Code suporta no máximo **20 ferramentas MCP** simultâneas. Ative apenas o MCP da fase atual para não estourar o limite.

---

### Primeiro uso — Fase 1 (Spec via Confluence)

Com o MCP do Confluence ativo e Agent mode ligado:

```
@custom-sdd-workflow define https://seu-confluence.atlassian.net/wiki/spaces/PROJ/pages/12345
```

O agente irá:
1. Ler a página do Confluence via MCP
2. Extrair requisitos, usuários, goals (MoSCoW) e restrições
3. Fazer até 3 perguntas de contexto técnico
4. Calcular o Clarity Score (0–15)
5. Gerar `docs/specs/DEFINE_{FEATURE}.md` no repositório do projeto

Quando o Clarity Score atingir ≥ 12/15, o agente sugere o próximo passo:

```
@custom-staff-engineer  ← Fase 2: revisão arquitetural e geração do ADR
```

---

### Atualizar as skills

Para puxar atualizações deste repositório:

1. No workspace, navegue até `Workspace/.assistant/skills/genie-code-agent-spec/`
2. Clique em **Pull** (ícone de atualização do Git Folder)
3. As skills são recarregadas automaticamente na próxima sessão do Genie Code

---

## Fluxo de Desenvolvimento

O desenvolvimento de features segue 4 fases com configurações MCP distintas por fase. Cada fase produz um artefato que alimenta a próxima — sem dependência de contexto online entre fases.

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1 — Spec                    MCP: Confluence (12 slots)     │
│                                                                 │
│  Quem: Chapter leader / Tech lead                               │
│  Skill: @custom-sdd-workflow → define <url-confluence>                 │
│  Output: docs/specs/DEFINE_{FEATURE}.md                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 2 — Arquitetura             MCP: nenhum                    │
│                                                                 │
│  Quem: Staff Engineer / Tech lead                               │
│  Skill: @custom-staff-engineer                                         │
│  Output: docs/adr/ADR_{FEATURE}.md                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 3 — Planejamento  [EM DESENVOLVIMENTO]                     │
│                                  MCP: Jira (14 slots)           │
│  Quem: Product Owner / Tech lead                                │
│  Skill: @custom-po                                                     │
│  Output: Epic + Stories (Fibonacci) + Tasks no Jira             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 4 — Desenvolvimento  [EM DESENVOLVIMENTO]                  │
│                             MCP: Bitbucket (~6) + Jira (14)     │
│  Quem: Desenvolvedor                                            │
│  Skills: @custom-sdd-workflow (Design → Build → Ship)                  │
│          @custom-dev-workflow  (branch → commit → PR → merge)          │
│  Output: branch → código → PR → ticket Jira atualizado          │
└─────────────────────────────────────────────────────────────────┘
```

### Por que fases separadas?

O Genie Code em Agent mode suporta no máximo **20 ferramentas MCP** simultaneamente. Cada produto Atlassian consome slots:

| MCP | Slots |
|-----|-------|
| Confluence | 12 |
| Jira | 14 |
| Bitbucket (mínimo custom-dev-workflow) | ~6 |
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
    └── designs/    # DESIGN_{FEATURE}.md  — saída do custom-sdd-workflow
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
║  @custom-sdd-workflow / iterate-agent  →  atualiza artefato da fase + cascata       ║
╚══════════════════════════════════════════════════════════════════════════════╝

ENTRADAS                                 NÓS
────────                                 ────────────────────────────────────────

(A) Ideia vaga ──────────────────────→   ┌── [0] BRAINSTORM ──────────────────┐
                                         │  skill:  @custom-sdd-workflow             │ OPCIONAL
                                         │  mcp:    —                         │
                                         │  output: docs/specs/BRAINSTORM_*.md│
                                         │  gate:   usuário confirmou abord.  │
                                         └──────────────────┬─────────────────┘
                                                            │
(B) Notas / docs brutos ────────────────────────────────────┼─────────────────┐
(C) DEFINE_*.md já existe ──────────────────────────────────┼─────────────────┤
(D) URL Confluence ─────────────────────────────────────────┼─────────────────┤
                                                            ▼                 ▼
                                         ┌── [1] DEFINE ───────────────────────┐
                                         │  skill:  @custom-sdd-workflow              │ OBRIGATÓRIO
                                         │  mcp:    Confluence (12 slots)      │
                                         │  output: docs/specs/DEFINE_*.md     │
                                         │  gate:   Clarity Score ≥ 12/15      │
                                         └───────────────────┬─────────────────┘
                                                             │
                                                             ▼
                                         ┌─ ─[2] ARQUITETURA ──────────────────┐
                                         │  skill:  @custom-staff-engineer            │ OBRIGATÓRIO
                                         │  mcp:    —                          │
                                         │  output: docs/adr/ADR_*.md          │
                                         └──────────────────┬──────────────────┘
                                                            │
                                              ┌─────────────┴─────────────┐
                                              ▼                           │
                          ┌── [3] PLANEJAMENTO ────────────┐ OPCIONAL     │
                          │  skill:  @custom-po  [em desenv.]     │              │
                          │  mcp:    Jira (14 slots)       │              │
                          │  output: Epic + Stories + Tasks│              │
                          └──────────────────┬─────────────┘              │
                                             └─────────────────────────▶  │
                                                            ▼
                                         ┌── [4] DESIGN ───────────────────────┐
                                         │  skill:  @custom-sdd-workflow              │ OBRIGATÓRIO
                                         │  mcp:    —                          │
                                         │  input:  ADR_*.md (vinculante)      │
                                         │  output: docs/designs/DESIGN_*.md   │
                                         │  gate:   File Manifest completo     │
                                         └───────────────────┬─────────────────┘
                                                             │
                              ┌──────────────────────────────┤ paralelo
                              ▼                              ▼
                 @custom-dev-workflow (criar branch)  ┌── [5] BUILD ───────────────────┐
                                               │  skill:   @custom-sdd-workflow        │ OBRIGATÓRIO
                                               │  mcp:     —                    │
                                               │  delega:  @databricks-* skills │
                                               │  output:  código gerado        │
                                               │           BUILD_REPORT_*.md    │
                                               │  gate:    lint + testes ok,    │
                                               │           sem credenciais      │
                                               └──────────────────┬─────────────┘
                              ┌─────────────────────────────┤ paralelo
                              ▼                             ▼
                 @custom-dev-workflow (commit + PR)   ┌── [6] SHIP ────────────────────┐
                                               │  skill:   @custom-sdd-workflow        │ OBRIGATÓRIO
                                               │  mcp:     Jira (14 slots)      │
                                               │  delega:  @custom-dev-workflow (PR)   │
                                               │  delega:  @custom-code-reviewer ★     │
                                               │  output:  SHIPPED_*.md         │
                                               │           Jira ticket fechado  │
                                               │  gate:    acceptance tests ok  │
                                               └────────────────────────────────┘

★ RECOMENDADO
```

### Nós — Referência Rápida

| Nó | Skill | MCP ativo | Output | Gate para avançar | Status |
|----|-------|-----------|--------|-------------------|--------|
| [0] Brainstorm | @custom-sdd-workflow | — | `docs/specs/BRAINSTORM_*.md` | Usuário confirmou abordagem → vai para [1] | OPCIONAL |
| [1] Define | @custom-sdd-workflow | Confluence | `docs/specs/DEFINE_*.md` | Clarity Score ≥ 12/15 | PRONTO |
| [2] Arquitetura | @custom-staff-engineer | — | `docs/adr/ADR_*.md` | ADR revisado e aceito | PRONTO |
| [3] Planejamento | @custom-po | Jira | Epic + Stories + Tasks | — | EM DESENVOLVIMENTO |
| [4] Design | @custom-sdd-workflow | — | `docs/designs/DESIGN_*.md` | File Manifest completo | EM DESENVOLVIMENTO |
| [5] Build | @custom-sdd-workflow | — | código + `BUILD_REPORT_*.md` | Lint + testes ok, sem credenciais | EM DESENVOLVIMENTO |
| [6] Ship | @custom-sdd-workflow | Jira | `SHIPPED_*.md` + Jira fechado | Acceptance tests ok | EM DESENVOLVIMENTO |
| Iterate | @custom-sdd-workflow | — | Artefato da fase atualizado | — | CROSS-CUTTING |

### Delegações em Fase 4

Durante os nós [4] a [6], o @custom-sdd-workflow coordena com outras skills:

| Ação | Delegado para | Quando |
|------|--------------|--------|
| Criar branch git | @custom-dev-workflow | Início do Design [4] |
| Implementar cada arquivo | @databricks-* (mapeado no File Manifest) | Build [5] |
| Commit + PR | @custom-dev-workflow | Ship [6] |
| Code review | @custom-code-reviewer | Ship [6] — recomendado |

---

## Índice de Skills

Skills ficam na **raiz do repositório** — cada skill é uma pasta com `SKILL.md` (frontmatter + instruções) e arquivos de referência opcionais. No Genie Code, são invocadas via `@skill-name` em Agent mode. Para usar: carregue este repo como Git Folder em `Workspace/.assistant/skills/` no Databricks.

### IA & ML

| Skill | Descrição |
|-------|-----------|
| [`databricks-agent-bricks`](databricks-agent-bricks/) | Knowledge Assistants para Q&A sobre documentos, Genie Spaces para exploração SQL e Supervisor Agents para orquestração multi-agente |
| [`databricks-ai-functions`](databricks-ai-functions/) | Funções AI nativas do Databricks SQL (`ai_classify`, `ai_extract`, `ai_summarize`, etc.) para adicionar IA diretamente em pipelines SQL e PySpark |
| [`databricks-aibi-dashboards`](databricks-aibi-dashboards/) | Criação de dashboards AI/BI (Lakeview) — exige validação de todas as queries via `execute_sql` antes do deploy |
| [`databricks-genie`](databricks-genie/) | Criação e consulta de Genie Spaces para exploração SQL em linguagem natural; inclui Conversation API e migração entre workspaces |
| [`databricks-mlflow-evaluation`](databricks-mlflow-evaluation/) | Avaliação de agentes GenAI com MLflow 3: `mlflow.genai.evaluate()`, scorers, MemAlign e GEPA para otimização de prompts |
| [`databricks-model-serving`](databricks-model-serving/) | Deploy e consulta de endpoints de Model Serving para modelos MLflow, ChatAgent/ResponsesAgent e agentes com UC Functions |
| [`databricks-vector-search`](databricks-vector-search/) | Criação e consulta de índices de Vector Search para RAG, busca semântica e similaridade |

### Dados & SQL

| Skill | Descrição |
|-------|-----------|
| [`databricks-dbsql`](databricks-dbsql/) | Recursos avançados do Databricks SQL: SQL warehouses, SQL scripting, stored procedures e performance tuning |
| [`databricks-iceberg`](databricks-iceberg/) | Tabelas Apache Iceberg no Databricks: Managed Iceberg, External Reads (Uniform), Iceberg REST Catalog e interop com Snowflake |
| [`databricks-metric-views`](databricks-metric-views/) | Criação e gestão de metric views no Unity Catalog para definir KPIs e métricas de negócio padronizadas em YAML |
| [`databricks-spark-declarative-pipelines`](databricks-spark-declarative-pipelines/) | Lakeflow Spark Declarative Pipelines (SDP/DLT): streaming tables, materialized views, CDC, SCD Type 2 e Auto Loader |
| [`databricks-spark-structured-streaming`](databricks-spark-structured-streaming/) | Spark Structured Streaming em produção: Kafka, Real-Time Mode, triggers, operações stateful, checkpoints e stream-stream joins |
| [`databricks-synthetic-data-gen`](databricks-synthetic-data-gen/) | Geração de dados sintéticos realistas com Spark + Faker em escala, múltiplos formatos (Parquet/JSON/CSV/Delta) |
| [`databricks-unity-catalog`](databricks-unity-catalog/) | System tables (audit, lineage, billing) e operações com volumes (`/Volumes/`) no Unity Catalog |
| [`databricks-zerobus-ingest`](databricks-zerobus-ingest/) | Clientes Zerobus Ingest para ingestão near real-time em tabelas Delta via gRPC, sem message bus |
| [`spark-python-data-source`](spark-python-data-source/) | Data sources Python customizados para Spark (PySpark DataSource API): leitores/escritores batch e streaming para sistemas externos |

### Plataforma Databricks

| Skill | Descrição |
|-------|-----------|
| [`databricks-bundles`](databricks-bundles/) | Declarative Automation Bundles (DABs): criação, configuração e deploy multi-ambiente com CICD |
| [`databricks-config`](databricks-config/) | Gestão de conexões de workspace: verificar perfil atual, trocar workspace e autenticar via `~/.databrickscfg` |
| [`databricks-docs`](databricks-docs/) | Referência de documentação Databricks via llms.txt — usar quando outras skills não cobrirem o tópico |
| [`databricks-execution-compute`](databricks-execution-compute/) | Execução de código e gestão de compute no Databricks: serverless, clusters, Python/Scala/SQL/R |
| [`databricks-jobs`](databricks-jobs/) | Criação, listagem, execução e monitoramento de Databricks Jobs via CLI, Python SDK e Asset Bundles |
| [`databricks-python-sdk`](databricks-python-sdk/) | SDK Python do Databricks, Databricks Connect, CLI e REST API — referência completa com exemplos |

### Aplicações

| Skill | Descrição |
|-------|-----------|
| [`databricks-apps-python`](databricks-apps-python/) | Aplicações Python no Databricks (Dash, Streamlit, Gradio, Flask, FastAPI, Reflex) com OAuth, SQL warehouse e model serving |
| [`databricks-lakebase-autoscale`](databricks-lakebase-autoscale/) | Lakebase Autoscaling (PostgreSQL gerenciado): autoscaling, scale-to-zero, branching, synced tables e OAuth |
| [`databricks-lakebase-provisioned`](databricks-lakebase-provisioned/) | Lakebase Provisioned (PostgreSQL OLTP): criação de instâncias, conexão de apps, reverse ETL e memória de agentes |
| [`databricks-unstructured-pdf-generation`](databricks-unstructured-pdf-generation/) | Geração de PDFs a partir de HTML e upload para volumes do Unity Catalog |

### Desenvolvimento & Workflow

| Skill | Fase | Descrição |
|-------|------|-----------|
| [`custom-sdd-workflow`](custom-sdd-workflow/) | 1 e 4 | Workflow Spec-Driven Development em 5 fases (Brainstorm → Define → Design → Build → Ship). Fase 1: Brainstorm + Define via MCP Confluence. Fase 4: Design + Build + Ship (dentro do @custom-dev-workflow) |
| [`custom-dev-workflow`](custom-dev-workflow/) | 4 | Fluxo de desenvolvimento seguro: discussão → branch → código → validação → auto-review → PR → merge |
| [`custom-code-reviewer`](custom-code-reviewer/) | 4 | Review de segurança, qualidade de código, performance e boas práticas para projetos Databricks e Python |
| [`databricks-python-dev`](databricks-python-dev/) | 4 | Padrões de desenvolvimento Python: uv, type hints, Ruff, Pyright e pytest |
| [`custom-test-generator`](custom-test-generator/) | 4 | Geração de testes unitários pytest, testes de integração e fixtures para código Python e data engineering |
| [`custom-staff-engineer`](custom-staff-engineer/) | 2 | Revisão de spec, discussão arquitetural e geração de ADR (`docs/adr/`) |
| `custom-po` | 3 | Quebra de Epic em Stories (Fibonacci) e Tasks no Jira — **em desenvolvimento** |

---

## Sincronização das Skills Databricks (upstream)

As skills `databricks-*`, `spark-python-data-source` e `TEMPLATE` **não são nossas** — elas vêm do repositório oficial da Databricks [`databricks-solutions/ai-dev-kit`](https://github.com/databricks-solutions/ai-dev-kit), pasta `databricks-skills/`. Para mantê-las atualizadas sem clonar o repo upstream dentro do nosso, há um GitHub Action que sincroniza automaticamente.

### Como funciona

```
┌──────────────────────────────────────────────────────────────────────┐
│  Toda segunda 06:00 UTC  (ou manualmente via "Run workflow")          │
└───────────────────────────────────┬──────────────────────────────────┘
                                    ▼
   1. Descobre a ÚLTIMA TAG semver do upstream (ex: v0.1.12)
      └─ segue releases publicadas, NÃO o branch main do upstream
                                    ▼
   2. Sparse + shallow checkout de databricks-skills/ (+ .claude/skills/
      python-dev) num dir efêmero do runner (.upstream/) — nada do repo
      upstream é commitado no nosso repo (sem submodule, sem subtree)
                                    ▼
   3. Copia cada pasta de skill para a raiz do nosso repo
      └─ NUNCA toca nas nossas skills próprias custom-* (OWN_SKILLS)
      └─ grava versão + commit em databricks-skills.lock
                                    ▼
   4. Se algo mudou → abre/atualiza 1 PR para a main (label: skills-sync)
      Se nada mudou (mesma tag, mesmo conteúdo) → nenhum PR é criado
                                    ▼
   5. Você revisa o diff e faz o merge  ← respeita a Golden Rule
```

> **Por que segue tag e não `main`:** a tag é um corte estável e reproduzível. O `main` do upstream pode conter trabalho em andamento entre releases. Consequência: se o upstream ficar semanas sem nova release, os runs de segunda não geram PR algum — e está tudo certo. O PR só aparece quando há release nova (ou mudança de conteúdo naquela tag).

### Skills próprias vs. upstream

O prefixo da pasta indica a origem: **`databricks-*`** = upstream (não editar), **`custom-*`** = nossa (editável).

| Origem | Skills | Editar à mão? |
|--------|--------|---------------|
| **Upstream** (`ai-dev-kit`) | `databricks-*` (inclui `databricks-python-dev`, de `.claude/skills/python-dev`), `spark-python-data-source`, `TEMPLATE` | ❌ Não — o sync sobrescreve. Contribua no upstream. |
| **Nossas** (`custom-*`) | `custom-sdd-workflow`, `custom-staff-engineer`, `custom-dev-workflow`, `custom-code-reviewer`, `custom-test-generator`, `custom-po` (planejada) | ✅ Sim — não existem no upstream, o sync nunca as toca. |

### Disparar manualmente

Em **Actions → Sync Databricks Skills → Run workflow**. Aceita um input `ref` opcional para fixar uma tag específica (vazio = última release).

> **Pré-requisito:** habilitar *Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests"*, senão a abertura do PR falha.

Arquivos envolvidos:
- [`.github/workflows/sync-databricks-skills.yml`](.github/workflows/sync-databricks-skills.yml) — o workflow
- `databricks-skills.lock` — manifesto de proveniência (versão + commit upstream + data), gerado pelo workflow

---

## Estrutura do Repositório

```
<skill-name>/                       # 33 skills na raiz (Databricks + SDD workflow + Python + Spark)
docs/                               # Documentação de referência extraída de fontes Databricks
.github/workflows/                  # CI — inclui o sync das skills Databricks (upstream)
databricks-skills.lock              # Proveniência do último sync (versão + commit upstream)
assets/                             # Assets locais (PDFs, repos) — gitignored
.claude/                            # Claude Code CLI local — gitignored
```

## Git Workflow

Nunca commitar direto em `main`. Sempre criar branch → PR → aguardar merge.
