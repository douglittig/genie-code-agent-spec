# STORIES: {Feature Name}

> Backlog derivado do DEFINE + ADR pelo `@custom-po`. Espelha o que foi criado no Jira.
> Localização: `docs/planning/STORIES_{FEATURE}.md`

## Metadata

| Atributo | Valor |
|----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Epic (Jira)** | {PROJ-123} |
| **Data** | {YYYY-MM-DD} |
| **Autor** | custom-po |
| **DEFINE de origem** | `docs/specs/DEFINE_{FEATURE}.md` |
| **ADR de origem** | `docs/adr/ADR_{FEATURE}.md` |

---

## Resumo do Backlog

| Métrica | Valor |
|---------|-------|
| **Stories** | {N} |
| **Pontos totais (Fibonacci)** | {soma} |
| **Tasks** | {M} |

---

## Stories

### Story 1 — {título curto}

> **Como** {usuário}, **quero** {capacidade}, **para** {valor}.

| Campo | Valor |
|-------|-------|
| **Jira** | {STORY-KEY} |
| **Pontos** | {1 / 2 / 3 / 5 / 8 / 13} |
| **Goals atendidos (DEFINE)** | {MUST-1, SHOULD-2} |
| **Unidade deployável (ADR)** | {ex: camada silver, endpoint, job} |

**Critérios de aceite** (dos acceptance tests do DEFINE):

- [ ] {AT-001: Given / When / Then}
- [ ] {AT-002: ...}

**Tasks:**

| # | Task | Jira | Skill `@databricks-*` sugerida |
|---|------|------|-------------------------------|
| 1 | {passo técnico} | {TASK-KEY} | {ex: @databricks-spark-declarative-pipelines} |
| 2 | {passo técnico} | {TASK-KEY} | {ex: @databricks-unity-catalog} |

---

### Story 2 — {título curto}

> **Como** {usuário}, **quero** {capacidade}, **para** {valor}.

| Campo | Valor |
|-------|-------|
| **Jira** | {STORY-KEY} |
| **Pontos** | {1 / 2 / 3 / 5 / 8 / 13} |
| **Goals atendidos (DEFINE)** | {...} |
| **Unidade deployável (ADR)** | {...} |

**Critérios de aceite:**

- [ ] {...}

**Tasks:**

| # | Task | Jira | Skill `@databricks-*` sugerida |
|---|------|------|-------------------------------|
| 1 | {...} | {TASK-KEY} | {...} |

---

## Rastreabilidade

| Goal (DEFINE) | Prioridade | Stories que o atendem |
|---------------|------------|------------------------|
| {goal} | MUST | Story 1, Story 3 |
| {goal} | SHOULD | Story 2 |

> Toda story criada no Jira é registrada também no state `.claude/sdd/state/{FEATURE}.md` (seção "Backlog Criado").

---

## Próximo Passo

**Pronto para:** Design — `@custom-sdd-workflow design` (executa Story por Story).
