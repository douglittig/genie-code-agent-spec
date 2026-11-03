# genie-code-agent-spec

Repositório de skills, custom instructions e integrações MCP para Databricks Genie Code e Claude Code.

> **Status:** O workflow SDD é composto por **skills autocontidas com prefixo `sdd-*`** (padrão de ativos do Genie Code): `@sdd-workflow` decide o tamanho da feature e orquestra; `@sdd-define`, `@sdd-design`, `@sdd-build` e `@sdd-ship` executam as fases; `@sdd-staff-engineer` (ADR), `@sdd-po` (Stories/Tasks no Jira) e `@sdd-iterate` (mudanças mid-stream) completam o fluxo, com **documentação automática no Jira via `@sdd-doc`** ao final de cada fase. `@sdd-dev-workflow` e `@sdd-code-reviewer` ainda em desenvolvimento.

---

## Instalação e Uso

### Pré-requisitos

| Requisito | Detalhes |
|-----------|---------|
| Databricks workspace | Genie Code habilitado (Agent mode disponível) |
| Acesso de admin | Permissão para criar Git Folders em `Workspace/` |
| Git provider configurado | GitHub, GitLab ou Bitbucket conectado ao workspace |
| MCP por fase | Confluence (Define), Jira (sdd-doc ao fim de cada fase + Ship), Bitbucket (Fase 4) |
| Compute para os gates | Serverless (environment 5 ou mais) ou cluster com DBR 17.0 ou mais |
| Git Folder do projeto | Criado com a opção **Use Git CLI** ligada. Os gates leem o git do projeto, e a opção não pode ser ligada depois numa pasta que já existe |

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
6. Cole a URL deste repositório: `https://github.com/douglittig/genie-code-agent-spec` (ou a do seu fork)
7. Escolha a branch `main`
8. **Renomeie o Git Folder para `skills`** (o padrão seria o nome do repo)
9. Confirme — o Git Folder será criado em `Workspace/.assistant/skills/`

> **Por que o nome importa:** O Genie Code procura skills em `Workspace/.assistant/skills/<skill-name>/SKILL.md`. Se o folder for nomeado diferente de `skills`, o caminho quebra. As skills estão na raiz deste repo — com o nome correto, cada skill fica exatamente onde o Genie Code espera.

> **Só para você:** o mesmo procedimento em `/Users/<você>/.assistant/` instala as skills só para o seu usuário. É o jeito de testar antes de liberar para o workspace inteiro, que exige admin.

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

### Passo 2b — Montar os gates (segundo Git Folder)

Os gates são scripts que decidem, por código, se uma etapa pode avançar (ex.: o Define só sai com a spec válida e aprovada). O código fica no pacote [`gates/`](gates/), e o Genie Code bloqueia os dois caminhos óbvios para rodá-lo: executar script dentro de `.assistant/skills` e fazer `pip install` direto do GitHub. Por isso o **mesmo repo é montado uma segunda vez, fora de `.assistant`**, e o agente roda os gates de lá, sem instalar nada.

1. Crie um Git Folder deste repo em `/Users/<você>/` (só para você) ou em `/Workspace/Shared/` (para o workspace).
2. Renomeie para **`sdd-gates`**. Este folder só guarda código: não precisa de "Use Git CLI".
3. Teste, numa célula `%sh` ou no terminal web:

```bash
cd /tmp && PYTHONPATH=/Workspace/Users/<você>/sdd-gates/gates python3 -m sdd_gates selftest
```

`selftest: OK` quer dizer que os gates reprovam o que devem reprovar. As skills procuram o folder nesses dois lugares; se estiver em outro, o agente pergunta e grava o caminho no state da feature.

> **Fora do Genie Code** (Claude Code, CI, máquina local), instale como pacote: `pip install "git+https://github.com/douglittig/genie-code-agent-spec@main#subdirectory=gates"`. Empresas que distribuem bibliotecas por Volume do Unity Catalog ou PyPI interno podem gerar um wheel com `python -m build gates`.

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
2. Perguntar o que for decisão sua (escopo, comportamento do dado, desvio da página), com recomendação
3. Escrever os critérios de aceite em EARS (`QUANDO … ENTÃO o pipeline DEVE …`) e passar pela rubrica de requisitos implícitos de dados
4. Gerar `docs/specs/DEFINE_{FEATURE}.md` no repositório do projeto e rodar o gate `sdd_gates define`
5. Parar e esperar a sua aprovação, gravada com as suas palavras

Com a spec aprovada, o agente sugere o próximo passo (conforme o tamanho da feature):

```
@sdd-staff-engineer  ← Fase 2: revisão arquitetural e geração do ADR
```

---

### Atualizar as skills

Para puxar atualizações deste repositório:

1. No workspace, navegue até `Workspace/.assistant/skills/` (o Git Folder renomeado no Passo 1)
2. Clique em **Pull** (ícone de atualização do Git Folder)
3. As skills são recarregadas automaticamente na próxima sessão do Genie Code
4. Faça **Pull** também no Git Folder `sdd-gates`. Os dois folders precisam estar na mesma versão: se o `sdd-gates` ficar atrás, o agente avisa e pede o pull antes de rodar um gate

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
│  Output: docs/planning/TASKS_*.md + histórias/tasks no Jira     │
│          + @sdd-doc comenta o plano no épico                    │
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
    ├── planning/   # TASKS_{FEATURE}.md    — saída da Fase 3 (@sdd-po)
    └── designs/    # DESIGN_{FEATURE}.md   — saída da Fase 4 (@sdd-design)

.sdd/               # estado e relatórios do fluxo (no repo do projeto)
├── features/
│   └── {FEATURE}/
│       ├── state.md          # ledger: jira_key, fases, aprovações, log Jira
│       └── BUILD_REPORT.md   # relatório do Build
└── archive/
    └── {FEATURE}/            # docs + state + SHIPPED_{DATE}.md depois do Ship
```

### Documentação automática no Jira (@sdd-doc)

Ao final de **cada** fase, a skill `@sdd-doc` posta um comentário estruturado no ticket Jira (resumo +
link do artefato + origem Confluence + gate) e **transiciona** o status (Define → Em andamento,
Build → Em revisão, Ship → Concluído). A chave do ticket é capturada uma vez no Define e guardada
no ledger `.sdd/features/{FEATURE}/state.md`. Há **preview** antes de qualquer escrita; sem chave, o
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

(A) Ideia vaga ─────────────────────────────────────────────┬─────────────────┐
(B) Notas / docs brutos ────────────────────────────────────┼─────────────────┐
(C) DEFINE_*.md já existe ──────────────────────────────────┼─────────────────┤
(D) URL Confluence ─────────────────────────────────────────┼─────────────────┤
                                                            ▼                 ▼
                                         ┌── [1] DEFINE ───────────────────────┐
                                         │  skill:  @sdd-define                │ OBRIGATÓRIO
                                         │  mcp:    Confluence (12 slots)      │
                                         │  output: docs/specs/DEFINE_*.md     │
                                         │  gate:   define + aprovação         │
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
                          │  output: TASKS_*.md (+ Jira)   │              │
                          └──────────────────┬─────────────┘              │
                                             └─────────────────────────▶  │
                                                            ▼
                                         ┌── [4] DESIGN ───────────────────────┐
                                         │  skill:  @sdd-design                │ OBRIGATÓRIO
                                         │  mcp:    —                          │
                                         │  input:  ADR_*.md (vinculante)      │
                                         │  output: docs/designs/DESIGN_*.md   │
                                         │  gate:   sdd_gates tasks, c/ DESIGN │
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
| [1] Define | @sdd-define | Confluence | `docs/specs/DEFINE_*.md` | gate `sdd_gates define` verde + aprovação gravada (ideia vaga: áreas cinzentas dentro do Define) | PRONTO |
| [2] Arquitetura | @sdd-staff-engineer | — | `docs/adr/ADR_*.md` | ADR revisado e aceito | PRONTO |
| [3] Planejamento | @sdd-po | Jira | `docs/planning/TASKS_*.md` (histórias + tasks) + Jira, se houver épico | gate `sdd_gates tasks` verde + plano aprovado (todo critério com task, teste e gate) | PRONTO |
| [4] Design | @sdd-design | — | `docs/designs/DESIGN_*.md` | gate `sdd_gates tasks` verde com o DESIGN (toda task num componente) | PRONTO |
| [5] Build | @sdd-build | — | código + `BUILD_REPORT_*.md` | Lint + testes ok, sem credenciais | PRONTO |
| [6] Ship | @sdd-ship | Jira | `SHIPPED_*.md` + Jira fechado | Acceptance tests ok | PRONTO |
| Iterate | @sdd-iterate | — | Artefato da fase atualizado | — | CROSS-CUTTING |
| Doc | @sdd-doc | Jira | comentário + transição no ticket + `.sdd/features/*/state.md` | — | CROSS-CUTTING (fim de fase) |

### Delegações em Fase 4

Durante os nós [4] a [6], o orquestrador @sdd-workflow coordena com outras skills:

| Ação | Delegado para | Quando |
|------|--------------|--------|
| Criar branch git | @sdd-dev-workflow | Início do Design [4] |
| Implementar cada task | @databricks-* (coluna "Constrói com" do DESIGN) | Build [5] |
| Commit + PR | @sdd-dev-workflow | Ship [6] |
| Code review | @sdd-code-reviewer | Ship [6] — recomendado |

---

## Índice de Skills

Skills ficam na **raiz do repositório** — cada skill é uma pasta com `SKILL.md` (frontmatter + instruções) e arquivos de referência opcionais. No Genie Code, são invocadas via `@skill-name` em Agent mode. Para usar: carregue este repo como Git Folder em `Workspace/.assistant/skills/` no Databricks.

> As skills `databricks-*` são cópia do repo oficial [`databricks/databricks-agent-skills`](https://github.com/databricks/databricks-agent-skills) (ver [Sincronização](#sincronização-das-skills-databricks-upstream)). Descrições resumidas do frontmatter de cada uma.

### IA & ML

| Skill | Descrição |
|-------|-----------|
| [`databricks-ai-functions`](databricks-ai-functions/) | Funções AI nativas do Databricks SQL (`ai_classify`, `ai_extract`, `ai_summarize`, etc.) em pipelines SQL e PySpark |
| [`databricks-ai-runtime`](databricks-ai-runtime/) | AI Runtime (`databricks air`): submeter e acompanhar workloads de treino em GPU serverless |
| [`databricks-genie-agents`](databricks-genie-agents/) | Genie Agents (antigos Genie Spaces) sobre tabelas UC, Metric Views e documentos; substitui Knowledge Assistant e Supervisor Agent |
| [`databricks-ml-training`](databricks-ml-training/) | Treino de modelos (XGBoost, scikit-learn, PyTorch) com Optuna, aliases @prod/@challenger, feature tables e batch scoring |
| [`databricks-mlflow-evaluation`](databricks-mlflow-evaluation/) | Avaliação de agentes GenAI com MLflow 3: `mlflow.genai.evaluate()`, scorers e otimização de prompts |
| [`databricks-mlflow-tracing`](databricks-mlflow-tracing/) | Tracing e observabilidade com MLflow: instrumentar apps e agentes GenAI, analisar traces e métricas |
| [`databricks-model-serving`](databricks-model-serving/) | Deploy e consulta de endpoints de Model Serving (MLflow, ChatAgent/ResponsesAgent, agentes com UC Functions) |
| [`databricks-unity-gateway`](databricks-unity-gateway/) | Unity AI Gateway: modelos de fundação pay-per-token, serviços de modelo e MCP, orçamento e alertas de uso |
| [`databricks-vector-search`](databricks-vector-search/) | Índices de Vector Search para RAG, busca semântica e similaridade |

### Dados & SQL

| Skill | Descrição |
|-------|-----------|
| [`databricks-data-discovery`](databricks-data-discovery/) | Achar e consultar dados via Genie: "que tabelas existem", "onde vive X", perguntas em linguagem natural e geração de SQL |
| [`databricks-dbsql`](databricks-dbsql/) | Databricks SQL: SQL warehouses, SQL scripting, stored procedures e performance tuning |
| [`databricks-iceberg`](databricks-iceberg/) | Apache Iceberg no Databricks: Managed Iceberg, Uniform, Iceberg REST Catalog e interop |
| [`databricks-lakeflow-connect`](databricks-lakeflow-connect/) | Ingestão gerenciada com Lakeflow Connect (Salesforce, Workday, ServiceNow, SQL Server, CDC de Postgres/MySQL) |
| [`databricks-metric-views`](databricks-metric-views/) | Metric views no Unity Catalog: KPIs e métricas de negócio padronizadas em YAML |
| [`databricks-pipelines`](databricks-pipelines/) | Lakeflow Spark Declarative Pipelines (antigo DLT): batch e streaming em Python/SQL, Auto CDC |
| [`databricks-spark-structured-streaming`](databricks-spark-structured-streaming/) | Structured Streaming em produção: Kafka, Real-Time Mode, triggers, stateful, checkpoints e joins |
| [`databricks-synthetic-data-gen`](databricks-synthetic-data-gen/) | Dados sintéticos realistas com Spark + Faker em escala |
| [`databricks-unity-catalog`](databricks-unity-catalog/) | System tables (audit, lineage, billing) e volumes (`/Volumes/`) no Unity Catalog |
| [`databricks-zerobus-ingest`](databricks-zerobus-ingest/) | Zerobus Ingest: ingestão near real-time em tabelas Delta via gRPC, sem message bus |
| [`spark-python-data-source`](spark-python-data-source/) | Data sources Python customizados (PySpark DataSource API) para batch e streaming — *experimental* no upstream |

### Plataforma Databricks

| Skill | Descrição |
|-------|-----------|
| [`databricks-core`](databricks-core/) | Ponto de entrada do Databricks CLI: autenticação, perfis e bundles; carregar antes da skill do produto |
| [`databricks-dabs`](databricks-dabs/) | Declarative Automation Bundles (DABs): criar, validar, fazer deploy e rodar jobs, pipelines, dashboards e apps |
| [`databricks-docs`](databricks-docs/) | Documentação Databricks via llms.txt, quando outras skills não cobrem o tema |
| [`databricks-execution-compute`](databricks-execution-compute/) | Execução de código e gestão de compute: serverless, clusters, Python/Scala/SQL/R |
| [`databricks-jobs`](databricks-jobs/) | Databricks Jobs via CLI, Python SDK e bundles: criar, rodar e monitorar |
| [`databricks-python-sdk`](databricks-python-sdk/) | Python SDK, Databricks Connect, CLI e REST API |
| [`databricks-sandbox`](databricks-sandbox/) | Sandbox serverless sob demanda para rodar código gerado por agente ou não confiável |
| [`databricks-serverless`](databricks-serverless/) | Compute serverless para jobs, pipelines e DABs (STANDARD ou PERFORMANCE_OPTIMIZED); carregar antes de escrever o job |
| [`databricks-serverless-migration`](databricks-serverless-migration/) | Migrar notebooks, jobs, pipelines e JARs de compute clássico para serverless |
| [`databricks-setup-local`](databricks-setup-local/) | Montar ou diagnosticar o `.venv` local (uv) para Databricks Connect, serverless ou bundle |

### Aplicações

| Skill | Descrição |
|-------|-----------|
| [`databricks-apps`](databricks-apps/) | Databricks Apps (AppKit): apps de dados, ferramentas analíticas e visualizações interativas |
| [`databricks-apps-python`](databricks-apps-python/) | Apps Python (Dash, Streamlit, Gradio, Flask, FastAPI, Reflex) com OAuth, SQL warehouse e model serving |
| [`databricks-app-design`](databricks-app-design/) | UX de telas de dados em AppKit/React: layout, gráficos, KPIs e estados obrigatórios |
| [`databricks-lakebase`](databricks-lakebase/) | Lakebase Postgres: projetos, escala, conectividade, synced tables e Data API |
| [`databricks-aibi-dashboards`](databricks-aibi-dashboards/) | Dashboards AI/BI (Lakeview), com validação das queries antes do deploy |
| [`databricks-unstructured-pdf-generation`](databricks-unstructured-pdf-generation/) | Geração de PDFs a partir de HTML e upload para volumes do Unity Catalog |

### Desenvolvimento & Workflow — família SDD (`sdd-*`)

Cada fase do workflow SDD é uma skill autocontida (SKILL.md + template próprio). `@sdd-workflow` é o orquestrador que roteia entre elas.

| Skill | Fase | Descrição |
|-------|------|-----------|
| [`sdd-workflow`](sdd-workflow/) | — | Orquestrador: tamanho da feature (Pequeno → Complexo), contrato de execução, raio de ação no Databricks e fim de etapa |
| [`sdd-define`](sdd-define/) | 1 | Spec de dados testável: critérios EARS, rubrica de requisitos implícitos, áreas cinzentas, gate `sdd_gates define` e aprovação gravada → `docs/specs/DEFINE_*.md` |
| [`sdd-staff-engineer`](sdd-staff-engineer/) | 2 | Revisão de spec, discussão arquitetural e geração de ADR (`docs/adr/`) |
| [`sdd-po`](sdd-po/) | 3 | Product Owner: quebra a feature em histórias (fatias verticais, pontos Fibonacci) e tasks atômicas com teste e gate, gate `sdd_gates tasks` e aprovação gravada → `docs/planning/TASKS_*.md`; cria no Jira via MCP quando há épico |
| [`sdd-design`](sdd-design/) | 4 | Como cada task vira componente no Databricks: reaproveitamento, componentes ligados a critérios e tasks, skill `@databricks-*` de cada um e decisões → `docs/designs/DESIGN_*.md` |
| [`sdd-build`](sdd-build/) | 5 | Implementação das tasks do plano, na ordem, delegando às skills `@databricks-*` → código + `BUILD_REPORT_*.md` |
| [`sdd-ship`](sdd-ship/) | 6 | Archive da feature, lições aprendidas e fechamento do ticket → `SHIPPED_*.md` |
| [`sdd-iterate`](sdd-iterate/) | cross | Mudanças mid-stream em documentos SDD com análise de cascata |
| [`sdd-doc`](sdd-doc/) | cross | Hook de fim de fase: comentário + transição no ticket Jira via MCP |
| [`sdd-dev-workflow`](sdd-dev-workflow/) | 4+ | Fluxo de desenvolvimento seguro: discussão → branch → código → validação → auto-review → PR → merge |
| [`sdd-code-reviewer`](sdd-code-reviewer/) | 4+ | Review de segurança, qualidade de código, performance e boas práticas para projetos Databricks e Python |
| [`databricks-python-dev`](databricks-python-dev/) | 4+ | Padrões de desenvolvimento Python: uv, type hints, Ruff, Pyright e pytest — *congelada* (ai-dev-kit v0.1.14; não existe no repo oficial) |
| [`custom-test-generator`](custom-test-generator/) | 4+ | Geração de testes unitários pytest, testes de integração e fixtures para código Python e data engineering |

---

## Sincronização das Skills Databricks (upstream)

As skills `databricks-*` e `spark-python-data-source` **não são nossas** — vêm do repositório oficial da Databricks [`databricks/databricks-agent-skills`](https://github.com/databricks/databricks-agent-skills) (pasta `skills/`; a `spark-python-data-source` vem de `experimental/`). Um GitHub Action mantém a cópia atualizada sem clonar o upstream dentro do nosso repo.

> **Mudança de upstream (nov/2026):** até a v0.1.14 as skills vinham de [`databricks-solutions/ai-dev-kit`](https://github.com/databricks-solutions/ai-dev-kit). Na v0.2.0 (28/07/2026) o ai-dev-kit deixou de distribuí-las e passou o papel para o `databricks-agent-skills`, mantido pela engenharia da Databricks. Algumas skills mudaram de nome:
>
> | Antes (ai-dev-kit) | Agora (oficial) |
> |---|---|
> | `databricks-bundles` | `databricks-dabs` |
> | `databricks-genie`, `databricks-agent-bricks` | `databricks-genie-agents` |
> | `databricks-spark-declarative-pipelines` | `databricks-pipelines` |
> | `databricks-lakebase-autoscale`, `databricks-lakebase-provisioned` | `databricks-lakebase` |
> | `databricks-config` | `databricks-core` |
>
> `databricks-python-dev` não existe no repo oficial e ficou **congelada** na versão do ai-dev-kit v0.1.14 (`FROZEN_SKILLS`). O `TEMPLATE/` também não é mais sincronizado.

### Como funciona

```
┌──────────────────────────────────────────────────────────────────────┐
│  Toda segunda 06:00 UTC  (ou manualmente via "Run workflow")          │
└───────────────────────────────────┬──────────────────────────────────┘
                                    ▼
   1. Descobre a ÚLTIMA RELEASE do upstream (ex: v0.2.40)
      └─ segue releases publicadas, NÃO o branch main do upstream
                                    ▼
   2. Sparse + shallow checkout de skills/ (+ experimental/
      spark-python-data-source) num dir efêmero do runner (.upstream/)
      — nada do repo upstream é commitado (sem submodule, sem subtree)
                                    ▼
   3. .github/scripts/sync-databricks-skills.sh:
      └─ copia cada pasta com SKILL.md para a raiz
      └─ PODA as skills que o sync anterior trouxe e o upstream removeu
      └─ NUNCA toca OWN_SKILLS (sdd-*/custom-*) nem FROZEN_SKILLS
      └─ copia LICENSE e NOTICE da Databricks
      └─ grava versão, commit e lista de skills em databricks-skills.lock
                                    ▼
   4. Se algo mudou → abre/atualiza 1 PR para a main (label: skills-sync)
      Se nada mudou (mesma release) → nenhum PR é criado
                                    ▼
   5. Você revisa o diff e faz o merge  ← respeita a Golden Rule
```

> **Por que segue release e não `main`:** a release é um corte estável e reproduzível. O `main` do upstream pode conter trabalho em andamento.

> **Se o upstream renomear uma skill:** o PR vai mostrar a pasta antiga apagada e a nova criada. Antes do merge, troque as referências `@databricks-*` nas skills `sdd-*` (`grep -rn "@databricks-<nome-antigo>" sdd-*`) e rode o validador.

### Testar o sync localmente

```bash
git clone --depth 1 --filter=blob:none --sparse --branch v0.2.40 \
  https://github.com/databricks/databricks-agent-skills /tmp/up
git -C /tmp/up sparse-checkout set skills experimental/spark-python-data-source
UPSTREAM=databricks/databricks-agent-skills UPSTREAM_PATH=skills UPSTREAM_REF=v0.2.40 \
  EXTRA_SKILLS="experimental/spark-python-data-source:spark-python-data-source" \
  FROZEN_SKILLS="databricks-python-dev" OWN_SKILLS="$(grep '^  OWN_SKILLS' .github/workflows/sync-databricks-skills.yml | cut -d'"' -f2)" \
  bash .github/scripts/sync-databricks-skills.sh /tmp/up .
python3 .claude/skills/run-genie-code-agent-spec/driver.py validate
```

### Skills próprias vs. upstream

O prefixo da pasta indica a origem: **`databricks-*`** = upstream (não editar), **`sdd-*`** e **`custom-*`** = nossas (editáveis).

| Origem | Skills | Editar à mão? |
|--------|--------|---------------|
| **Upstream** (`databricks-agent-skills`) | `databricks-*`, `spark-python-data-source` | ❌ Não — o sync sobrescreve. Contribua no upstream. |
| **Congelada** (ai-dev-kit v0.1.14) | `databricks-python-dev` | ⚠️ Pode — o sync não toca mais (`FROZEN_SKILLS`). |
| **Nossas** (`sdd-*`, `custom-*` e `TEMPLATE`) | `sdd-workflow`, `sdd-define`, `sdd-design`, `sdd-build`, `sdd-ship`, `sdd-iterate`, `sdd-doc`, `sdd-staff-engineer`, `sdd-po`, `sdd-dev-workflow`, `sdd-code-reviewer`, `custom-test-generator` | ✅ Sim — o sync nunca as toca (`OWN_SKILLS`). |

### Licença das skills Databricks

As skills upstream seguem a **Databricks License**: uso permitido em conexão com os serviços Databricks, e quem redistribui precisa repassar a licença. Por isso o sync copia [`LICENSE-databricks-agent-skills`](LICENSE-databricks-agent-skills) e [`NOTICE-databricks-agent-skills`](NOTICE-databricks-agent-skills) para a raiz.

### Disparar manualmente

Em **Actions → Sync Databricks Skills → Run workflow**. Aceita um input `ref` opcional para fixar uma release específica (vazio = última).

> **Pré-requisito:** habilitar *Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests"*, senão a abertura do PR falha.

Arquivos envolvidos:
- [`.github/workflows/sync-databricks-skills.yml`](.github/workflows/sync-databricks-skills.yml) — o workflow
- [`.github/scripts/sync-databricks-skills.sh`](.github/scripts/sync-databricks-skills.sh) — a cópia, poda e lock (roda igual local)
- `databricks-skills.lock` — proveniência (release + commit upstream + data + lista de skills), gerado pelo sync

---

## Estrutura do Repositório

```
<skill-name>/                       # 50 skills na raiz (Databricks oficiais + SDD workflow + Python + Spark)
docs/                               # Documentação de referência extraída de fontes Databricks
gates/                              # pacote sdd-gates: gates do SDD (no Databricks, rodado de um 2º Git Folder)
.github/workflows/ e scripts/       # CI — sync das skills Databricks (upstream)
LICENSE-/NOTICE-databricks-agent-skills  # licença das skills upstream
databricks-skills.lock              # Proveniência do último sync (versão + commit upstream)
THIRD_PARTY_NOTICES.md              # créditos e licenças de terceiros (AgentSpec, Databricks)
assets/                             # cópias locais de referência — gitignored
.claude/                            # Claude Code CLI local — gitignored
```

## Git Workflow

Nunca commitar direto em `main`. Sempre criar branch → PR → aguardar merge.

---

## Créditos

O workflow SDD deste repositório começou como uma adaptação do **[AgentSpec](https://github.com/luanmorenommaciel/agentspec), de [Luan Moreno](https://github.com/luanmorenommaciel)** (v2.1, abril/2026, licença MIT), um framework de Spec-Driven Development para Claude Code.

| Veio do AgentSpec | Construído aqui |
|---|---|
| As fases Brainstorm → Define → Design → Build → Ship e o Iterate | Adaptação para o Genie Code: skills autocontidas em `Workspace/.assistant/skills/`, Agent mode e `@skill` |
| Clarity Score, File Manifest e os templates de artefato (BRAINSTORM, DEFINE, DESIGN, BUILD_REPORT, SHIPPED) | Define a partir do Confluence e documentação no Jira por fase via MCP (`sdd-doc`), dentro do limite de 20 ferramentas |
| Code reviewer e gerador de testes | `sdd-staff-engineer` (ADR vinculante), `sdd-po` (Epic → Stories → Tasks), `sdd-dev-workflow` e o ledger de estado por feature |
| | Delegação do Build às skills oficiais `@databricks-*`, com sync automático do upstream |

O tamanho da feature (*auto-sizing*), o contrato de execução e o raio de ação do `sdd-workflow`, os critérios EARS, a rubrica de requisitos implícitos e o gate por script do `sdd-define`, as tasks atômicas com teste e gate do `sdd-po` e o reaproveitamento, os componentes e as decisões do `sdd-design` foram adaptados do **[TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills), de Felipe Rodrigues / Tech Leads Club** (CC-BY-4.0), com regras próprias para o Databricks.

Os arquivos derivados e o aviso de licença estão em [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Referências

- [Introducing Genie Code](https://www.databricks.com/blog/introducing-genie-code) — blog da Databricks
- Documentação do Genie Code: [skills](https://docs.databricks.com/aws/en/genie-code/skills), [custom instructions](https://docs.databricks.com/aws/en/genie-code/instructions), [MCP](https://docs.databricks.com/aws/en/genie-code/mcp), [dicas](https://docs.databricks.com/aws/en/genie-code/tips) e [desenvolvimento de pipelines](https://docs.databricks.com/aws/en/ldp/de-agent)
- [The New SDLC With Vibe Coding](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding) — Addy Osmani, Shubham Saboo e Sokratis Kartakis (Google, mai/2026), base da seção Harness & Guardrails
