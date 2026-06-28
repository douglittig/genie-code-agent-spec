---
name: custom-sdd-workflow
description: |
  Workflow de Spec-Driven Development (SDD) para o Genie Code. Use de forma PROATIVA
  quando o usuário falar em construir features, ler specs do Confluence, gerar código
  a partir de requisitos de negócio, atualizar tickets no Jira, criar PRs ou revisar
  código. Guia pelas 5 fases: Brainstorm → Define → Design → Build → Ship,
  com integração Confluence MCP (ingestão de spec) e Jira MCP (atualização de ticket).
---

# SDD Workflow — Genie Code

Spec-Driven Development transforma requisitos em código rastreável. Cada arquivo gerado
é vinculado ao requisito que o originou — sem "vibe coding", sem specs que ninguém lê.

## Fluxo Completo

```
Confluence (SPEC) → DEFINE → @custom-staff-engineer → DESIGN → BUILD → PR/Review → SHIP
      ↑                           (ADR)                                            ↓
  (via MCP)                                                                  (via MCP Jira)
                      └──────────── doc-agent (hook por fase) ───────────────┘
                            comentário + transição no ticket Jira
```

O **doc-agent** é transversal: ao final de **cada** fase ele documenta o avanço no ticket Jira
(comentário estruturado + transição de status) e atualiza o ledger de rastreabilidade.

## Regras do Fluxo

1. **Brainstorm** é opcional — pular para Define se a SPEC já está clara
2. **Define** exige Clarity Score ≥ 12/15 antes de avançar; captura a `jira_key` e cria o **state**
3. **Após Define** — acionar `@custom-staff-engineer` para gerar o ADR antes do Design
4. **Design** usa o ADR como fonte de verdade vinculante; deve ter File Manifest completo
5. **Build** delega cada arquivo à skill Databricks indicada no manifest
6. **Ship** arquiva todos os artefatos (incluindo o state) e fecha o ticket no Jira

### Protocolo de Fim-de-Fase (obrigatório em toda fase)

Toda fase termina com a mesma sequência — é o que mantém o Jira e o state sincronizados:

```
1. Gerar o artefato da fase (DEFINE / ADR / DESIGN / BUILD_REPORT / SHIPPED)
2. Atualizar o ledger:        .claude/sdd/state/{FEATURE}.md
3. Chamar o doc-agent:        documenta no Jira (comentário + transição) — agents/doc-agent.md
4. Sugerir a próxima fase
```

### Ledger de Rastreabilidade (state)

`.claude/sdd/state/{FEATURE}.md` é a **fonte única da verdade** da feature: guarda a `jira_key`,
a URL do Confluence, a fase atual, os caminhos dos artefatos, os gate scores e o log de ações no
Jira. Criado na fase Define, atualizado por toda fase, arquivado no Ship. É de onde o doc-agent
obtém a chave do ticket.

---

## Fase 0 — Brainstorm (opcional)

**Quando usar:** ideia vaga, requisitos não claros, precisa explorar abordagens antes de capturar requisitos formais.
**Quando pular:** SPEC do Confluence já clara, ou BRAINSTORM_*.md já existe.

**Output:** `docs/specs/BRAINSTORM_{FEATURE}.md`
**Gate:** mín. 3 perguntas, 2 abordagens exploradas, YAGNI aplicado, usuário confirmou abordagem.

> **Para executar esta fase:** ler `agents/brainstorm-agent.md` e usar `templates/BRAINSTORM_TEMPLATE.md`

---

## Fase 1 — Define

**Quando usar:** BRAINSTORM pronto ou SPEC do Confluence disponível.
**Integração Confluence:** fornecer URL ou page-id → ler via MCP → extrair objetivo, usuários, critérios de aceite, restrições → mapear para o template.
**Integração Jira:** capturar a chave do ticket (ex: `PROJ-123`) e gravá-la no **state** — é o que todas as fases e o doc-agent reutilizam. Sem chave → o doc-agent opera em modo pendente.

**Output:** `docs/specs/DEFINE_{FEATURE}.md` + `.claude/sdd/state/{FEATURE}.md` (ledger criado aqui)
**Gate:** Clarity Score ≥ 12/15. Se menor, pedir esclarecimentos antes de avançar.
**Fim-de-fase:** atualizar o state → doc-agent documenta no Jira (transição → Em andamento).
**Próximo passo natural:** `@custom-staff-engineer` — revisão da spec e decisão arquitetural (ADR) antes do Design.

### Como funciona

Ao chamar `@custom-sdd-workflow define <url-confluence>`, este SKILL.md carrega:

| O que carrega | Arquivo | Papel |
|---------------|---------|-------|
| Agente | `agents/define-agent.md` | Executa as 4 capacidades abaixo |
| Template | `templates/DEFINE_TEMPLATE.md` | Estrutura do documento de saída |
| Template | `templates/STATE_TEMPLATE.md` | Estrutura do ledger de rastreabilidade |
| Hook | `agents/doc-agent.md` | Documenta o fim da fase no Jira |

O **define-agent** executa nesta ordem:

1. Lê `AGENTS.md` — contexto do projeto
2. Lê a página do Confluence via MCP — input principal
3. **Capacidade 1 — Extração de Requisitos:** extrai Problema, Usuários, Goals (MoSCoW), Critérios de Sucesso, Restrições, Fora do Escopo
4. **Capacidade 2 — Contexto Técnico:** faz 3 perguntas (localização no projeto, quais `@databricks-*` skills se aplicam, impacto de infraestrutura)
5. **Capacidade 3 — Contexto DE** *(se detectar keywords: pipeline, ETL, warehouse, schema):* extrai origens, volumes, SLAs de freshness, contratos de schema
6. **Capacidade 4 — Clarity Score:** pontua 5 elementos (0–3 cada) → total 0–15

**Gate iterativo — o agente não avança até a spec estar validada:**

| Score | Ação |
|-------|------|
| ≥ 12/15 | Gera `DEFINE_{FEATURE}.md` → sugere `@custom-staff-engineer` |
| 9–11/15 | Faz perguntas direcionadas → re-pontua |
| < 9/15  | Bloqueia — exige esclarecimento antes de continuar |

> **Nota:** As skills `@databricks-*` não são invocadas nesta fase — são apenas *identificadas* no Contexto Técnico para uso nas fases de Design e Build.

> **Para executar esta fase:** ler `agents/define-agent.md` e usar `templates/DEFINE_TEMPLATE.md`

---

## Fase 2 — Design

**Quando usar:** DEFINE pronto com Clarity Score ≥ 12/15.
**ADR:** se `docs/adr/ADR_{FEATURE}.md` existir (gerado pelo `@custom-staff-engineer`), ele é vinculante — o design-agent executa o ADR, não reabre decisões.

**Output:** `docs/designs/DESIGN_{FEATURE}.md`
**Gate:** File Manifest completo — todos os arquivos com agente Databricks atribuído.
**Fim-de-fase:** atualizar o state → doc-agent documenta no Jira (mantém Em andamento).

> **Para executar esta fase:** ler `agents/design-agent.md` e usar `templates/DESIGN_TEMPLATE.md`

---

## Fase 3 — Build

**Quando usar:** DESIGN pronto com File Manifest completo.
**Processo:** executar o File Manifest arquivo por arquivo, delegando para a skill Databricks indicada.

**Output:** código + `.claude/sdd/reports/BUILD_REPORT_{FEATURE}.md`
**Gate:** todos os arquivos criados, lint e testes passando, sem credenciais hardcoded.
**Fim-de-fase:** atualizar o state → doc-agent documenta no Jira (transição → Em revisão).

> **Para executar esta fase:** ler `agents/build-agent.md` e usar `templates/BUILD_REPORT_TEMPLATE.md`

---

## Fase 4 — Ship

**Quando usar:** Build completo e validado.
**Integração Jira:** o doc-agent comenta o SHIPPED + link do PR e transiciona o ticket para "Concluído".
**PR e Review:** delegar para `@custom-dev-workflow` (branch → commit → PR) e `@custom-code-reviewer` (review de segurança e qualidade).

**Bloqueadores de merge:** falha em acceptance test, credencial exposta, breaking change sem deprecation period.

**Output:** `.claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md` (com o state arquivado) + Jira atualizado
**Gate:** lições capturadas, ticket fechado, artefatos arquivados.
**Fim-de-fase:** doc-agent documenta no Jira (transição → Concluído) → arquivar o state.

> **Para executar esta fase:** ler `agents/ship-agent.md` e usar `templates/SHIPPED_TEMPLATE.md`

---

## Iterate — Mudanças Mid-Stream

Quando requisitos mudarem durante qualquer fase:
1. Atualizar o documento da fase onde a mudança entrou
2. Verificar impacto cascata nas fases seguintes (DEFINE → DESIGN → código)
3. Documentar no revision history do artefato e no state
4. Fim-de-fase: doc-agent registra a mudança de escopo como comentário no Jira (sem transição)

> **Para executar:** ler `agents/iterate-agent.md`

---

## Documentação no Jira — doc-agent

O `agents/doc-agent.md` é o hook transversal chamado no **fim de cada fase** (ver Protocolo de
Fim-de-Fase). Ele lê a `jira_key` do state, monta o comentário com `templates/JIRA_UPDATE_TEMPLATE.md`,
mostra um **preview** ao usuário, e então posta o comentário + transiciona o ticket.

| O que carrega | Arquivo | Papel |
|---------------|---------|-------|
| Hook | `agents/doc-agent.md` | Comentário + transição no Jira por fase |
| Template | `templates/JIRA_UPDATE_TEMPLATE.md` | Estrutura do comentário de fim de fase |

**Ferramentas MCP Jira (4):** `jira_get_issue`, `jira_get_transitions`, `jira_add_comment`,
`jira_transition_issue`. Sem `jira_key` no state → modo pendente (não escreve, registra e avisa).

---

## Localização dos Artefatos

```
docs/
├── specs/      BRAINSTORM_*.md, DEFINE_*.md
├── adr/        ADR_*.md  (gerado pelo @custom-staff-engineer)
└── designs/    DESIGN_*.md

.claude/sdd/
├── state/      {FEATURE}.md  (ledger de rastreabilidade — fonte da verdade)
├── reports/    BUILD_REPORT_*.md
└── archive/    {FEATURE}/ com todos os docs + state + SHIPPED_*.md
```
