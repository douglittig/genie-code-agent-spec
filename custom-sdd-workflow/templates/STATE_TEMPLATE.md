# SDD STATE: {Feature Name}

> Ledger de rastreabilidade da feature — **fonte única da verdade** do fluxo SDD.
> Criado na fase Define, atualizado ao final de cada fase, arquivado no Ship.
> Localização: `.claude/sdd/state/{FEATURE}.md`

## Identidade

| Atributo | Valor |
|----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Jira Key** | {PROJ-123 \| `pendente` se não informada} |
| **Confluence URL** | {url da página SPEC \| `n/a`} |
| **Fase Atual** | {Brainstorm \| Define \| ADR \| Design \| Build \| Ship \| Shipped} |
| **Criado em** | {YYYY-MM-DD HH:MM UTC} |
| **Atualizado em** | {YYYY-MM-DD HH:MM UTC} |

---

## Status das Fases

| Fase | Status | Artefato | Gate | Concluída em |
|------|--------|----------|------|--------------|
| Brainstorm | {pendente \| concluída \| pulada} | `docs/specs/BRAINSTORM_{FEATURE}.md` | {n/a} | {YYYY-MM-DD} |
| Define | {pendente \| concluída} | `docs/specs/DEFINE_{FEATURE}.md` | Clarity {X}/15 | {YYYY-MM-DD} |
| ADR | {pendente \| concluída} | `docs/adr/ADR_{FEATURE}.md` | {decisões aprovadas} | {YYYY-MM-DD} |
| Planejamento (PO) | {pendente \| concluída} | `docs/planning/STORIES_{FEATURE}.md` | {stories estimadas + criadas} | {YYYY-MM-DD} |
| Design | {pendente \| concluída} | `docs/designs/DESIGN_{FEATURE}.md` | {File Manifest completo} | {YYYY-MM-DD} |
| Build | {pendente \| concluída} | `.claude/sdd/reports/BUILD_REPORT_{FEATURE}.md` | {lint/testes ✅} | {YYYY-MM-DD} |
| Ship | {pendente \| concluída} | `.claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md` | {ticket fechado} | {YYYY-MM-DD} |

---

## Backlog Criado (custom-po)

> Preenchido pelo `@custom-po` na Fase 3. Registra as Stories/Tasks criadas sob o Epic (`jira_key`).

| Tipo | Jira | Resumo | Pontos | Parent |
|------|------|--------|--------|--------|
| Story | {STORY-KEY} | {título} | {Fibonacci} | {Epic} |
| Task | {TASK-KEY} | {título} | — | {Story} |

---

## Log de Ações no Jira

> Registrado pelo `doc-agent` ao final de cada fase. Garante idempotência (não duplicar comentário da mesma fase).

| Fase | Comentário | Transição | Quando |
|------|------------|-----------|--------|
| Define | {postado \| pendente} | To Do → Em andamento | {YYYY-MM-DD HH:MM} |
| ADR | {postado \| pendente} | (mantém Em andamento) | {YYYY-MM-DD HH:MM} |
| Design | {postado \| pendente} | (mantém Em andamento) | {YYYY-MM-DD HH:MM} |
| Build | {postado \| pendente} | Em andamento → Em revisão | {YYYY-MM-DD HH:MM} |
| Ship | {postado \| pendente} | Em revisão → Concluído | {YYYY-MM-DD HH:MM} |

---

## Histórico de Revisões

| Versão | Data | Fase | Mudança |
|--------|------|------|---------|
| 1.0 | {YYYY-MM-DD} | Define | State criado |
