# Spec-Driven Development com Genie Code

Guia de como usar Spec-Driven Development (SDD) no contexto do Databricks Genie Code, integrando Confluence, Jira e fluxos de code review automatizados.

---

## O que é Spec-Driven Development

SDD é a abordagem que resolve o gap entre o "vibe coding" desestruturado e os documentos de especificação que ninguém lê. Em vez de gerar specs estáticas, o SDD usa a spec como **entrada executável**: o agente lê a spec, gera o código, e rastreia cada arquivo de volta ao requisito que o originou.

O framework de referência é o [AgentSpec v2.1](https://github.com/PedroHBCruz/agentspec) — 5 fases, 58 agentes especializados, 23 domínios de conhecimento. A adaptação para Genie Code mantém as fases e os artefatos, mas conecta Confluence e Jira via MCP.

---

## O Fluxo SDD para Genie Code

```
Confluence (SPEC) → DEFINE → ADR → @sdd-po → DESIGN → BUILD → SHIP → PR → Review
       ↑                       (Stories/Jira)                                 │
       │              └────────── sdd-doc documenta cada fase no Jira ──────┘
  (via MCP)                          (comentário + transição via MCP)
```

A cada fim de fase o **sdd-doc** posta um comentário no ticket e transiciona o status. A chave do
Jira é capturada no Define e guardada no ledger `.claude/sdd/state/{FEATURE}.md`.

### Visão geral das etapas

| Etapa | Ferramenta | O que acontece |
|-------|-----------|----------------|
| **1. Ler SPEC do Confluence** | MCP Confluence | Agente lê a página de especificação escrita com a área de negócio e extrai requisitos estruturados |
| **2. DEFINE** | Genie Code Agent Mode | Gera `DEFINE_{FEATURE}.md` com critérios de aceite, contexto técnico, Clarity Score |
| **3. DESIGN** | Genie Code Agent Mode | Gera `DESIGN_{FEATURE}.md` com file manifest, agentes atribuídos e padrões de código |
| **4. BUILD** | Genie Code Agent Mode | Executa o código seguindo o DESIGN, com atribuição por agente especializado |
| **5. Atualizar Jira** | MCP Jira | Move o ticket para "In Review", adiciona link do PR, registra BUILD_REPORT |
| **6. Criar PR** | `/create-pr` | Cria PR com conventional commits e descrição estruturada |
| **7. Review do PR** | `/review` ou skill | Dual AI review (análise estática + revisão arquitetural) |

---

## As 5 Fases SDD

### Fase 0: Brainstorm (Opcional)

Usar quando a ideia ainda está vaga. Para features bem definidas no Confluence, pular direto para o Define.

**Quando usar:**
- A área de negócio ainda está explorando abordagens
- Há múltiplas formas de implementar e você quer decidir antes de escrever spec
- A SPEC no Confluence ainda não está madura

**Artefato:** `.claude/sdd/features/BRAINSTORM_{FEATURE}.md`

**Gate de qualidade:** Mín. 3 perguntas, 2+ abordagens, YAGNI aplicado

---

### Fase 1: Define

O coração do SDD. Transforma a SPEC do Confluence em um documento estruturado com **Clarity Score**.

**Entrada:** Página do Confluence (via MCP) ou texto da SPEC

**Saída:** `.claude/sdd/features/DEFINE_{FEATURE}.md`

**Seções obrigatórias:**

```markdown
## Problem Statement
## Target Users
## Goals (MUST / SHOULD / COULD)
## Success Criteria (com métricas numéricas)
## Acceptance Tests (Given/When/Then)
## Technical Context
  | Deployment Location | src/pipelines/ | onde os arquivos vão |
  | KB Domains          | databricks-spark-declarative-pipelines, databricks-unity-catalog |
  | IaC Impact          | None / New resources / Modify existing |
## Out of Scope
## Clarity Score (mínimo 12/15 para avançar)
```

**Gate:** Clarity Score ≥ 12/15. Se menor, o agente pede esclarecimentos antes de avançar para o Design.

**Como o Confluence entra:**

```
# No Genie Code Agent Mode:
"Leia a page do Confluence [URL] e gere o DEFINE para a feature X"

# O agente via MCP Confluence:
1. Lê o conteúdo da página
2. Extrai requisitos, critérios de aceite, contexto de negócio
3. Mapeia para o template DEFINE
4. Calcula o Clarity Score
5. Pede esclarecimentos se score < 12
```

---

### Fase 2: Design

Transforma o DEFINE em plano técnico executável. Aqui acontece o **Agent Matching** — cada arquivo recebe um agente especializado.

**Entrada:** `DEFINE_{FEATURE}.md`

**Saída:** `.claude/sdd/features/DESIGN_{FEATURE}.md`

**Seções obrigatórias:**

```markdown
## Architecture Overview (diagrama ASCII)
## Key Decisions (com alternativas rejeitadas)
## File Manifest
  | # | File | Action | Purpose | Agent | Dependencies |
  | 1 | src/pipelines/bronze_events.py | Create | Ingestão raw | @lakeflow-pipeline-builder | None |
  | 2 | src/pipelines/silver_events.py | Create | Transformação | @spark-engineer | 1 |
  | 3 | tests/test_events.py | Create | Testes unitários | @custom-test-generator | 1, 2 |
## Agent Assignment Rationale
## Code Patterns (copy-paste ready)
## Testing Strategy
```

**Gate:** Todos os arquivos têm agente atribuído. Nenhum arquivo fica como `(general)` sem justificativa.

---

### Fase 3: Build

Executa a implementação seguindo o File Manifest. Para cada arquivo, invoca o agente especializado.

**Entrada:** `DESIGN_{FEATURE}.md`

**Saída:**
- Código dos arquivos listados no manifest
- `.claude/sdd/reports/BUILD_REPORT_{FEATURE}.md`

**Atribuição no BUILD_REPORT:**

```markdown
## Agent Contributions
| Agent | Files | Specialization Applied |
|-------|-------|------------------------|
| @lakeflow-pipeline-builder | 1 | SDP pipeline patterns, autoloader, medallion |
| @spark-engineer | 2 | PySpark transformations, partition strategy |
| @custom-test-generator | 3 | pytest suite, fixtures, data quality assertions |
```

**Gate:** Todos os testes passam. Zero erros de tipo (Pyright).

---

### Fase 4: Ship

Arquiva os artefatos e captura lições aprendidas. **Antes do archive**, o sdd-doc comenta o
SHIPPED + link do PR no Jira e transiciona o ticket para "Concluído".

**Entrada:** Todos os artefatos do feature

**Saída:**
- `archive/{FEATURE}/` com todos os documentos (incluindo o `{FEATURE}.state.md`)
- `SHIPPED_{DATE}.md` com lições aprendidas
- Ticket Jira atualizado pelo sdd-doc (comentário + transição → Concluído)

---

## Integração com Confluence via MCP

O MCP Confluence permite que o agente leia SPECs diretamente sem copiar/colar.

### Fluxo típico

```
# Usuário:
"Leia a SPEC da feature X no Confluence [page-id] e gere o DEFINE"

# Genie Code Agent:
1. mcp_confluence_get_page(page_id="12345")
2. Extrai: objetivo, usuários, critérios de aceite, restrições
3. Identifica gaps (o que está vago na SPEC)
4. Gera DEFINE_{FEATURE}.md com Clarity Score
5. Apresenta gaps para o usuário resolver antes de avançar
```

### O que extrair da SPEC do Confluence

| Seção da SPEC | Mapeamento no DEFINE |
|---------------|----------------------|
| Objetivo da feature | Problem Statement |
| Usuários impactados | Target Users |
| Critérios de aceite | Acceptance Tests (Given/When/Then) |
| Regras de negócio | Goals + Constraints |
| Integrações | Technical Context → IaC Impact |
| O que NÃO entra | Out of Scope |
| Métricas de sucesso | Success Criteria |

### Tratamento de SPECs incompletas

Uma SPEC de negócio raramente tem tudo. O agente calcula o Clarity Score e pede o que falta:

```
Clarity Score: 8/15

Itens que precisam de esclarecimento:
- Success Criteria (0/3): Sem métricas numéricas definidas. Ex: "processar N eventos/min"
- Technical Context (1/3): Deployment location não especificado. Onde o código vai?
- Scope (1/3): Não está claro o que é excluído do MVP

Antes de avançar para o DESIGN, preciso dessas respostas.
```

---

## Integração com Jira via MCP — sdd-doc

A documentação no Jira **não é manual**: o `sdd-doc` (`sdd-doc/SKILL.md`)
é um hook transversal acionado ao **final de cada fase**. Ele lê a `jira_key` do ledger de state,
monta um comentário a partir de `JIRA_UPDATE_TEMPLATE.md`, mostra um **preview** ao usuário e então
posta o comentário + transiciona o ticket.

### Mapa fase → ação no Jira

| Fase concluída | Comentário | Transição (por intenção) |
|----------------|------------|--------------------------|
| Define | DEFINE + Clarity Score + origem Confluence | To Do → Em andamento |
| ADR | decisões-chave + link do ADR | mantém Em andamento |
| Planejamento (PO) | Stories/Tasks criadas sob o Epic | mantém Em andamento |
| Design | File Manifest + link do DESIGN | mantém Em andamento |
| Build | BUILD_REPORT + verificação | Em andamento → Em revisão |
| Ship | SHIPPED + link do PR | Em revisão → Concluído |

### Ferramentas MCP usadas (4)

`jira_get_issue`, `jira_get_transitions` (descobre a transição por intenção — nunca hardcoda ID),
`jira_add_comment`, `jira_transition_issue`. Sem `jira_key` no state — ou com o MCP Jira
indisponível/falhando — → **modo pendente** (registra e avisa, não escreve no Jira).

> **Limite de 20 slots — ok para a demo:** habilitando o conjunto completo, Confluence + Jira
> passariam de 20. Na demonstração usamos um subconjunto (sdd-doc: 4 tools Jira; intake: ~1 do
> Confluence), ~14 no total — então os dois MCPs podem ficar ativos juntos, sem troca.

---

## Criação de PR

Usar o comando `/create-pr` após o BUILD, com review opcional antes de criar.

```bash
# Review + PR em sequência
/review
/create-pr

# Ou com review integrado (bloqueia se houver críticos)
/create-pr --review
```

### Conventional Commits para Databricks

| Tipo | Quando usar | Exemplo |
|------|-------------|---------|
| `feat` | Nova pipeline, novo job, nova tabela | `feat(bronze): add events ingestion pipeline` |
| `fix` | Correção de bug em pipeline ou query | `fix(silver): handle null event_id in join` |
| `refactor` | Otimização sem mudança de comportamento | `refactor(gold): extract metric calculation to function` |
| `test` | Adição de testes de qualidade de dados | `test(events): add completeness assertions` |
| `chore` | Atualização de dependências, configuração | `chore(bundles): update target cluster version` |

---

## Review Automatizado do PR

Após criar o PR, rodar o review dual — análise estática + revisão arquitetural pelo Genie Code.

```bash
/review
```

**O que é verificado:**

| Categoria | Checks |
|-----------|--------|
| Arquitetura | Alinhamento com DESIGN, separação de concerns |
| Lógica | Implementação correta dos acceptance tests do DEFINE |
| Qualidade de dados | Checagem de nulos em PKs, filtros de partição |
| Código | Type hints, sem `SELECT *`, padrões do projeto |
| Segurança | Sem credenciais hardcoded, secrets via Databricks Secrets |

**Critérios de bloqueio (não faz merge):**
- Crítico: Falha em acceptance test do DEFINE
- Crítico: Credencial ou segredo exposto
- Crítico: Schema breaking change sem deprecation

---

## Artefatos SDD

Todos os artefatos ficam em `.claude/sdd/`:

```
docs/                            # artefatos versionados no repo do projeto
├── specs/    BRAINSTORM_*.md, DEFINE_*.md
├── adr/      ADR_*.md
├── planning/ STORIES_*.md   (@sdd-po)
└── designs/  DESIGN_*.md

.claude/sdd/
├── state/                       # {FEATURE}.md — ledger de rastreabilidade (jira_key, fases, log Jira)
├── reports/                     # BUILD_REPORT_{FEATURE}.md
└── archive/
    └── {FEATURE}/               # Ship (fechado)
        ├── DEFINE_{FEATURE}.md
        ├── ADR_{FEATURE}.md
        ├── DESIGN_{FEATURE}.md
        ├── BUILD_REPORT_{FEATURE}.md
        ├── {FEATURE}.state.md
        └── SHIPPED_{DATE}.md
```

---

## Templates

Cada template vive dentro da skill da fase que o usa (skills autocontidas):

| Template | Skill | Uso |
|----------|-------|-----|
| `sdd-brainstorm/BRAINSTORM_TEMPLATE.md` | `@sdd-brainstorm` | Exploração inicial |
| `sdd-define/DEFINE_TEMPLATE.md` | `@sdd-define` | Captura de requisitos |
| `sdd-define/STATE_TEMPLATE.md` | `@sdd-define` (criado aqui, usado por todas) | Ledger de rastreabilidade (jira_key, fases, log Jira) |
| `sdd-design/DESIGN_TEMPLATE.md` | `@sdd-design` | Design técnico + file manifest |
| `sdd-build/BUILD_REPORT_TEMPLATE.md` | `@sdd-build` | Relatório de construção |
| `sdd-ship/SHIPPED_TEMPLATE.md` | `@sdd-ship` | Archive + lições aprendidas |
| `sdd-doc/JIRA_UPDATE_TEMPLATE.md` | `@sdd-doc` | Comentário de fim de fase postado no Jira |

---

## Agentes Disponíveis para o File Manifest

Para o contexto Databricks, os agentes mais relevantes para atribuição no DESIGN:

| Agente | Especialidade |
|--------|--------------|
| `@lakeflow-pipeline-builder` | SDP pipelines, autoloader, streaming tables |
| `@spark-engineer` | PySpark, DataFrames, transformações |
| `@spark-streaming-architect` | Streaming, checkpoints, stateful ops |
| `@sql-optimizer` | Queries SQL, performance, particionamento |
| `@data-quality-analyst` | Testes de qualidade, assertions, observabilidade |
| `@medallion-architect` | Arquitetura bronze/silver/gold |
| `@lakehouse-architect` | Delta Lake, Iceberg, catalogs |
| `@python-developer` | Scripts Python, utilitários, SDK calls |
| `@custom-test-generator` | pytest, fixtures, suites de teste |
| `@sdd-code-reviewer` | Review arquitetural, boas práticas |

---

## Exemplo Completo: Feature de Ingestão

### Contexto

SPEC no Confluence: "Ingestão de eventos de clique do Kafka para tabela Gold com agregações por sessão".

### Passo 1 — Ler Confluence e gerar DEFINE

```
# Prompt no Genie Code:
"Leia a SPEC no Confluence page-id=98765 e gere o DEFINE para a feature CLICK_EVENTS_PIPELINE"
```

Genie Code lê via MCP, gera `DEFINE_CLICK_EVENTS_PIPELINE.md`:
- Clarity Score: 11/15
- Pede esclarecimento sobre volume esperado e SLA de latência
- Após resposta: 13/15 → avança para DESIGN

### Passo 2 — DESIGN

```
"Crie o DESIGN para .claude/sdd/features/DEFINE_CLICK_EVENTS_PIPELINE.md"
```

File Manifest gerado:

| # | File | Agent | Purpose |
|---|------|-------|---------|
| 1 | `src/pipelines/bronze_clicks.py` | `@lakeflow-pipeline-builder` | Autoloader Kafka → Bronze |
| 2 | `src/pipelines/silver_clicks.py` | `@spark-streaming-architect` | Dedup + parse → Silver |
| 3 | `src/pipelines/gold_sessions.py` | `@spark-engineer` | Agregação por sessão → Gold |
| 4 | `tests/test_click_pipeline.py` | `@custom-test-generator` | Suite de testes |
| 5 | `resources/pipeline_clicks.yml` | `@lakeflow-pipeline-builder` | DABs config |

### Passo 3 — BUILD

```
"Execute o BUILD para .claude/sdd/features/DESIGN_CLICK_EVENTS_PIPELINE.md"
```

Agente executa em paralelo os especialistas. BUILD_REPORT gerado com atribuição por arquivo.

### Passo 4 — Atualizar Jira e criar PR

```
# Atualiza Jira via MCP
"Atualize o ticket PROJ-456 com status In Review e adicione o BUILD_REPORT"

# Cria PR com review
/create-pr --review
```

### Passo 5 — Review e Ship

```
/review
/ship .claude/sdd/features/DEFINE_CLICK_EVENTS_PIPELINE.md
```

---

## Anti-Padrões

| Anti-Padrão | Problema | Solução |
|-------------|---------|---------|
| Pular o DEFINE | O código não tem rastreabilidade para o requisito | Sempre gerar DEFINE, mesmo para features simples |
| Clarity Score < 12 | O DESIGN vai ser incompleto ou errado | Resolver os gaps com a área de negócio antes de avançar |
| File Manifest genérico | Todos os arquivos com `(general)` | Usar os agentes especializados — eles produzem código melhor |
| Jira atualizado manualmente | Fica desatualizado, perde rastreabilidade | Usar MCP Jira no BUILD e SHIP |
| PR sem review | Bugs vão para review humano | Sempre `/review` antes de `/create-pr` ou usar `--review` flag |
| Editar código sem atualizar spec | Spec fica desatualizada, perde traceability | Usar `/iterate` para propagar mudanças pelo pipeline |

---

## Conexão com o Genie Code

### Como invocar o fluxo SDD no Genie Code

O Genie Code no **Agent Mode** executa cada fase como uma sequência de tarefas:

1. **Skills** auto-carregadas: `sdd-workflow` guia o agente pelo pipeline correto
2. **Agentes sub-especializados**: invocados via `Task()` para cada arquivo do manifest
3. **MCP Tools**: Confluence e Jira acessados nativamente no fluxo
4. **Commands** (`/define`, `/design`, `/build`, `/ship`): slash commands configurados em `.claude/commands/`

### Limites do Genie Code a considerar

| Limite | Impacto | Mitigação |
|--------|---------|-----------|
| 20 tools MCP por sessão | Confluence + Jira + Databricks já usa slots | Priorizar tools essenciais; Databricks MCP tem 75+ tools consolidados |
| Agent Mode apenas | SDD não funciona em Chat Mode | Sempre usar Agent Mode para o fluxo SDD |
| 20k chars custom instructions | CLAUDE.md não pode ser enorme | Manter CLAUDE.md conciso; detalhe vai nas skills |

---

## Referências

| Recurso | Local |
|---------|-------|
| Templates SDD | dentro de cada skill `sdd-*` (ex.: `sdd-define/DEFINE_TEMPLATE.md`) |
| Skills SDD | `sdd-workflow/` (orquestrador) + `sdd-brainstorm/`, `sdd-define/`, `sdd-design/`, `sdd-build/`, `sdd-ship/`, `sdd-iterate/`, `sdd-doc/` |
| AgentSpec (fonte) | `assets/repos/agentspec-main/` |
| Agents disponíveis | `assets/repos/agentspec-main/.claude/agents/` |
| Databricks Skills | raiz do repositório |
