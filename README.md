# genie-code-agent-spec

Repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code.

> **Status:** O workflow SDD é composto por **skills autocontidas com prefixo `sdd-*`** (padrão de ativos do Genie Code): `@sdd-workflow` orquestra; `@sdd-brainstorm`, `@sdd-define`, `@sdd-design`, `@sdd-build` e `@sdd-ship` executam as fases; `@sdd-staff-engineer` (ADR), `@sdd-po` (Stories/Tasks no Jira) e `@sdd-iterate` (mudanças mid-stream) completam o fluxo, com **documentação automática no Jira via `@sdd-doc`** ao final de cada fase. `@sdd-dev-workflow` e `@sdd-code-reviewer` ainda em desenvolvimento.

---

## Instalação e Uso

### Pré-requisitos

| Requisito | Detalhes |
|-----------|---------|
| Databricks workspace | Genie Code habilitado (Agent mode disponível) |
| Acesso de admin | Permissão para criar Git Folders em `Workspace/` |
| Git provider configurado | GitHub, GitLab ou Bitbucket conectado ao workspace |
| MCP por fase | Confluence (Define), Jira (sdd-doc ao fim de cada fase + Ship), Bitbucket (Fase 4) |

---

### Passo 1 — Carregar o repositório no workspace

O Genie Code detecta skills em `Workspace/.assistant/skills/<skill-name>/SKILL.md` — **um nível** abaixo de `skills/`. Por isso o repo precisa ser montado **como** a pasta `skills/`, não dentro dela.

**Estrutura esperada:**
```
Workspace/
└── .assistant/
    └── skills/          ← este repo é montado AQUI
        ├── sdd-workflow/
        │   └── SKILL.md
        ├── sdd-staff-engineer/
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
@sdd-workflow
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
@sdd-define https://seu-confluence.atlassian.net/wiki/spaces/PROJ/pages/12345
```

O agente irá:
1. Ler a página do Confluence via MCP
2. Extrair requisitos, usuários, goals (MoSCoW) e restrições
3. Fazer até 3 perguntas de contexto técnico
4. Calcular o Clarity Score (0–15)
5. Gerar `docs/specs/DEFINE_{FEATURE}.md` no repositório do projeto

Quando o Clarity Score atingir ≥ 12/15, o agente sugere o próximo passo:

```
@sdd-staff-engineer  ← Fase 2: revisão arquitetural e geração do ADR
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
│  Skill: @sdd-define <url-confluence>                            │
│  Output: docs/specs/DEFINE_{FEATURE}.md                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 2 — Arquitetura             MCP: nenhum                    │
│                                                                 │
│  Quem: Staff Engineer / Tech lead                               │
│  Skill: @sdd-staff-engineer                                     │
│  Output: docs/adr/ADR_{FEATURE}.md                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 3 — Planejamento                                          │
│                                  MCP: Jira                      │
│  Quem: Product Owner / Tech lead                                │
│  Skill: @sdd-po                                                 │
│  Output: docs/planning/STORIES_*.md + Stories/Tasks no Jira     │
│          + @sdd-doc comenta o plano no Epic                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│ FASE 4 — Desenvolvimento                                       │
│   @sdd-design/build/ship: PRONTO · @sdd-dev-workflow: EM DEV    │
│                             MCP: Jira (14)                      │
│  Quem: Desenvolvedor                                            │
│  Skills: @sdd-design → @sdd-build → @sdd-ship                   │
│          + @sdd-doc documenta cada fase no Jira                 │
│  Output: código + DESIGN/BUILD_REPORT/SHIPPED + Jira atualizado │
└─────────────────────────────────────────────────────────────────┘
```

### Por que fases separadas?

O Genie Code em Agent mode suporta no máximo **20 ferramentas MCP** simultaneamente. Cada produto Atlassian consome slots:

| MCP | Slots |
|-----|-------|
| Confluence | 12 |
| Jira | 14 |
| Bitbucket (mínimo sdd-dev-workflow) | ~6 |
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
    ├── specs/      # DEFINE_{FEATURE}.md   — saída da Fase 1
    ├── adr/        # ADR_{FEATURE}.md      — saída da Fase 2
    ├── planning/   # STORIES_{FEATURE}.md  — saída da Fase 3 (@sdd-po)
    └── designs/    # DESIGN_{FEATURE}.md   — saída da Fase 4 (@sdd-design)

.claude/sdd/        # estado e relatórios do fluxo (no repo do projeto)
├── state/          # {FEATURE}.md  — ledger de rastreabilidade (jira_key, fases, log Jira)
├── reports/        # BUILD_REPORT_{FEATURE}.md
└── archive/        # {FEATURE}/ com todos os docs + state + SHIPPED_*.md
```

### Documentação automática no Jira (@sdd-doc)

Ao final de **cada** fase, a skill `@sdd-doc` posta um comentário estruturado no ticket Jira (resumo +
link do artefato + origem Confluence + gate) e **transiciona** o status (Define → Em andamento,
Build → Em revisão, Ship → Concluído). A chave do ticket é capturada uma vez no Define e guardada
no ledger `.claude/sdd/state/{FEATURE}.md`. Há **preview** antes de qualquer escrita; sem chave, o
agente entra em modo pendente e não toca o Jira.

> **Limite de 20 slots MCP — ok para a demo:** habilitando o *conjunto completo* de ferramentas,
> Confluence + Jira passariam de 20. Mas na demonstração usamos só um **subconjunto** (o @sdd-doc
> precisa de 4 tools Jira; o intake usa ~1 do Confluence), totalizando ~14 — dentro do limite. Logo,
> Confluence e Jira podem ficar **ativos juntos** durante todo o fluxo, sem troca de MCP.

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
║  @sdd-iterate  →  atualiza artefato da fase + cascata                        ║
║  SDD-DOC — cross-cutting (fim de cada fase)                                  ║
║  @sdd-doc  →  Jira: comentário + transição + state                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

ENTRADAS                                 NÓS
────────                                 ────────────────────────────────────────

(A) Ideia vaga ──────────────────────→   ┌── [0] BRAINSTORM ──────────────────┐
                                         │  skill:  @sdd-brainstorm           │ OPCIONAL
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
                                         │  skill:  @sdd-define                │ OBRIGATÓRIO
                                         │  mcp:    Confluence (12 slots)      │
                                         │  output: docs/specs/DEFINE_*.md     │
                                         │  gate:   Clarity Score ≥ 12/15      │
                                         └───────────────────┬─────────────────┘
                                                             │
                                                             ▼
                                         ┌─ ─[2] ARQUITETURA ──────────────────┐
                                         │  skill:  @sdd-staff-engineer        │ OBRIGATÓRIO
                                         │  mcp:    —                          │
                                         │  output: docs/adr/ADR_*.md          │
                                         └──────────────────┬──────────────────┘
                                                            │
                                              ┌─────────────┴─────────────┐
                                              ▼                           │
                          ┌── [3] PLANEJAMENTO ────────────┐ OPCIONAL     │
                          │  skill:  @sdd-po               │              │
                          │  mcp:    Jira (14 slots)       │              │
                          │  output: Epic + Stories + Tasks│              │
                          └──────────────────┬─────────────┘              │
                                             └─────────────────────────▶  │
                                                            ▼
                                         ┌── [4] DESIGN ───────────────────────┐
                                         │  skill:  @sdd-design                │ OBRIGATÓRIO
                                         │  mcp:    —                          │
                                         │  input:  ADR_*.md (vinculante)      │
                                         │  output: docs/designs/DESIGN_*.md   │
                                         │  gate:   File Manifest completo     │
                                         └───────────────────┬─────────────────┘
                                                             │
                              ┌──────────────────────────────┤ paralelo
                              ▼                              ▼
                 @sdd-dev-workflow (criar branch)  ┌── [5] BUILD ───────────────────┐
                                               │  skill:   @sdd-build          │ OBRIGATÓRIO
                                               │  mcp:     —                    │
                                               │  delega:  @databricks-* skills │
                                               │  output:  código gerado        │
                                               │           BUILD_REPORT_*.md    │
                                               │  gate:    lint + testes ok,    │
                                               │           sem credenciais      │
                                               └──────────────────┬─────────────┘
                              ┌─────────────────────────────┤ paralelo
                              ▼                             ▼
                 @sdd-dev-workflow (commit + PR)   ┌── [6] SHIP ────────────────────┐
                                               │  skill:   @sdd-ship            │ OBRIGATÓRIO
                                               │  mcp:     Jira (14 slots)      │
                                               │  delega:  @sdd-dev-workflow (PR)   │
                                               │  delega:  @sdd-code-reviewer ★     │
                                               │  output:  SHIPPED_*.md         │
                                               │           Jira ticket fechado  │
                                               │  gate:    acceptance tests ok  │
                                               └────────────────────────────────┘

★ RECOMENDADO
```

### Nós — Referência Rápida

| Nó | Skill | MCP ativo | Output | Gate para avançar | Status |
|----|-------|-----------|--------|-------------------|--------|
| [0] Brainstorm | @sdd-brainstorm | — | `docs/specs/BRAINSTORM_*.md` | Usuário confirmou abordagem → vai para [1] | OPCIONAL |
| [1] Define | @sdd-define | Confluence | `docs/specs/DEFINE_*.md` | Clarity Score ≥ 12/15 | PRONTO |
| [2] Arquitetura | @sdd-staff-engineer | — | `docs/adr/ADR_*.md` | ADR revisado e aceito | PRONTO |
| [3] Planejamento | @sdd-po | Jira | `docs/planning/STORIES_*.md` + Stories/Tasks no Jira | Stories estimadas (Fibonacci) e criadas | PRONTO |
| [4] Design | @sdd-design | — | `docs/designs/DESIGN_*.md` | File Manifest completo | PRONTO |
| [5] Build | @sdd-build | — | código + `BUILD_REPORT_*.md` | Lint + testes ok, sem credenciais | PRONTO |
| [6] Ship | @sdd-ship | Jira | `SHIPPED_*.md` + Jira fechado | Acceptance tests ok | PRONTO |
| Iterate | @sdd-iterate | — | Artefato da fase atualizado | — | CROSS-CUTTING |
| Doc | @sdd-doc | Jira | comentário + transição no ticket + `.claude/sdd/state/*` | — | CROSS-CUTTING (fim de fase) |

### Delegações em Fase 4

Durante os nós [4] a [6], o orquestrador @sdd-workflow coordena com outras skills:

| Ação | Delegado para | Quando |
|------|--------------|--------|
| Criar branch git | @sdd-dev-workflow | Início do Design [4] |
| Implementar cada arquivo | @databricks-* (mapeado no File Manifest) | Build [5] |
| Commit + PR | @sdd-dev-workflow | Ship [6] |
| Code review | @sdd-code-reviewer | Ship [6] — recomendado |

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

### Desenvolvimento & Workflow — família SDD (`sdd-*`)

Cada fase do workflow SDD é uma skill autocontida (SKILL.md + template próprio). `@sdd-workflow` é o orquestrador que roteia entre elas.

| Skill | Fase | Descrição |
|-------|------|-----------|
| [`sdd-workflow`](sdd-workflow/) | — | Orquestrador do workflow SDD: fases, gates, handoffs e Protocolo de Fim-de-Fase |
| [`sdd-brainstorm`](sdd-brainstorm/) | 0 | Exploração colaborativa de ideias, comparação de abordagens e YAGNI → `docs/specs/BRAINSTORM_*.md` |
| [`sdd-define`](sdd-define/) | 1 | Extração de requisitos via MCP Confluence, Clarity Score e criação do state → `docs/specs/DEFINE_*.md` |
| [`sdd-staff-engineer`](sdd-staff-engineer/) | 2 | Revisão de spec, discussão arquitetural e geração de ADR (`docs/adr/`) |
| [`sdd-po`](sdd-po/) | 3 | Product Owner: quebra a feature em Epic → Stories (Fibonacci) → Tasks, cria no Jira via MCP e gera `docs/planning/STORIES_*.md` |
| [`sdd-design`](sdd-design/) | 4 | Design técnico com File Manifest a partir do DEFINE/ADR → `docs/designs/DESIGN_*.md` |
| [`sdd-build`](sdd-build/) | 5 | Implementação do File Manifest delegando às skills `@databricks-*` → código + `BUILD_REPORT_*.md` |
| [`sdd-ship`](sdd-ship/) | 6 | Archive da feature, lições aprendidas e fechamento do ticket → `SHIPPED_*.md` |
| [`sdd-iterate`](sdd-iterate/) | cross | Mudanças mid-stream em documentos SDD com análise de cascata |
| [`sdd-doc`](sdd-doc/) | cross | Hook de fim de fase: comentário + transição no ticket Jira via MCP |
| [`sdd-dev-workflow`](sdd-dev-workflow/) | 4+ | Fluxo de desenvolvimento seguro: discussão → branch → código → validação → auto-review → PR → merge |
| [`sdd-code-reviewer`](sdd-code-reviewer/) | 4+ | Review de segurança, qualidade de código, performance e boas práticas para projetos Databricks e Python |
| [`databricks-python-dev`](databricks-python-dev/) | 4+ | Padrões de desenvolvimento Python: uv, type hints, Ruff, Pyright e pytest |
| [`custom-test-generator`](custom-test-generator/) | 4+ | Geração de testes unitários pytest, testes de integração e fixtures para código Python e data engineering |

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
      └─ NUNCA toca nas nossas skills próprias sdd-*/custom-* (OWN_SKILLS)
      └─ grava versão + commit em databricks-skills.lock
                                    ▼
   4. Se algo mudou → abre/atualiza 1 PR para a main (label: skills-sync)
      Se nada mudou (mesma tag, mesmo conteúdo) → nenhum PR é criado
                                    ▼
   5. Você revisa o diff e faz o merge  ← respeita a Golden Rule
```

> **Por que segue tag e não `main`:** a tag é um corte estável e reproduzível. O `main` do upstream pode conter trabalho em andamento entre releases. Consequência: se o upstream ficar semanas sem nova release, os runs de segunda não geram PR algum — e está tudo certo. O PR só aparece quando há release nova (ou mudança de conteúdo naquela tag).

### Skills próprias vs. upstream

O prefixo da pasta indica a origem: **`databricks-*`** = upstream (não editar), **`sdd-*`** e **`custom-*`** = nossas (editáveis).

| Origem | Skills | Editar à mão? |
|--------|--------|---------------|
| **Upstream** (`ai-dev-kit`) | `databricks-*` (inclui `databricks-python-dev`, de `.claude/skills/python-dev`), `spark-python-data-source`, `TEMPLATE` | ❌ Não — o sync sobrescreve. Contribua no upstream. |
| **Nossas** (`sdd-*` e `custom-*`) | `sdd-workflow`, `sdd-brainstorm`, `sdd-define`, `sdd-design`, `sdd-build`, `sdd-ship`, `sdd-iterate`, `sdd-doc`, `sdd-staff-engineer`, `sdd-po`, `sdd-dev-workflow`, `sdd-code-reviewer`, `custom-test-generator` | ✅ Sim — não existem no upstream, o sync nunca as toca (`OWN_SKILLS`). |

### Disparar manualmente

Em **Actions → Sync Databricks Skills → Run workflow**. Aceita um input `ref` opcional para fixar uma tag específica (vazio = última release).

> **Pré-requisito:** habilitar *Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests"*, senão a abertura do PR falha.

Arquivos envolvidos:
- [`.github/workflows/sync-databricks-skills.yml`](.github/workflows/sync-databricks-skills.yml) — o workflow
- `databricks-skills.lock` — manifesto de proveniência (versão + commit upstream + data), gerado pelo workflow

---

## Estrutura do Repositório

```
<skill-name>/                       # 41 skills na raiz (Databricks + SDD workflow + Python + Spark)
docs/                               # Documentação de referência extraída de fontes Databricks
.github/workflows/                  # CI — inclui o sync das skills Databricks (upstream)
databricks-skills.lock              # Proveniência do último sync (versão + commit upstream)
assets/                             # documentation/ versionada (PDFs); repos/ gitignored
.claude/                            # Claude Code CLI local — gitignored
```

## Git Workflow

Nunca commitar direto em `main`. Sempre criar branch → PR → aguardar merge.
