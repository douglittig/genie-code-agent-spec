# SDD STATE: {Feature Name}

> Ledger de rastreabilidade da feature — **fonte única da verdade** do fluxo SDD.
> Criado na fase Define, atualizado ao final de cada fase, arquivado no Ship.
> Localização: `.sdd/features/{FEATURE}/state.md`

## Identidade

| Atributo | Valor |
|----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Tamanho** | {Pequeno \| Médio \| Grande \| Complexo} — {motivo em uma linha} |
| **Jira Key** | {PROJ-123 \| `pendente` se não informada} |
| **Confluence URL** | {url da página SPEC \| `n/a`} |
| **Gates** | {caminho de `<gates>`, ex.: `/Workspace/Users/<usuário>/sdd-gates/gates`} — versão {0.3.0} |
| **Fase Atual** | {Define \| ADR \| PO \| Design \| Build \| Ship \| Shipped} |
| **Criado em** | {YYYY-MM-DD HH:MM UTC} |
| **Atualizado em** | {YYYY-MM-DD HH:MM UTC} |

---

## Aprovações

> As duas paradas humanas do contrato de execução (`@sdd-workflow`). Grave só a aprovação que o
> usuário deu, com a versão e as palavras dele. A mesma linha vai também no artefato aprovado.
> Aprovação nova de uma versão nova: linha nova, a antiga fica.

| Etapa | Versão | Aprovado em | Palavras do usuário |
|-------|--------|-------------|---------------------|
| Spec (Define) | {v1.0} | {YYYY-MM-DD} | "{palavras}" |
| Plano de tarefas (PO) | {v1.0 \| n/a no tamanho Médio} | {YYYY-MM-DD} | "{palavras}" |

---

## Status das Fases

| Fase | Status | Artefato | Gate | Concluída em |
|------|--------|----------|------|--------------|
| Define | {pendente \| concluída} | `docs/specs/DEFINE_{FEATURE}.md` | {última linha da saída do gate, como saiu, ex.: `sdd_gates define DEFINE_X.md: OK — 0 aviso(s)`; + aprovado} | {YYYY-MM-DD} |
| ADR | {pendente \| concluída} | `docs/adr/ADR_{FEATURE}.md` | {decisões aprovadas} | {YYYY-MM-DD} |
| Planejamento (PO) | {pendente \| concluída} | `docs/planning/TASKS_{FEATURE}.md` | {última linha do gate `tasks --aprovado`, como saiu; + chaves criadas no Jira} | {YYYY-MM-DD} |
| Design | {pendente \| concluída} | `docs/designs/DESIGN_{FEATURE}.md` | {última linha do gate `tasks`, rodado com o DESIGN pronto} | {YYYY-MM-DD} |
| Build | {pendente \| concluída} | `.sdd/features/{FEATURE}/BUILD_REPORT.md` | {lint/testes ✅} | {YYYY-MM-DD} |
| Ship | {pendente \| concluída} | `.sdd/archive/{FEATURE}/SHIPPED_{DATE}.md` | {ticket fechado} | {YYYY-MM-DD} |

---

## Log de Ações no Jira

> Registrado pelo `sdd-doc` ao final de cada fase. Garante idempotência (não duplicar comentário da mesma fase).

| Fase | Comentário | Transição | Quando |
|------|------------|-----------|--------|
| Define | {postado \| pendente} | To Do → Em andamento | {YYYY-MM-DD HH:MM} |
| ADR | {postado \| pendente} | (mantém Em andamento) | {YYYY-MM-DD HH:MM} |
| Planejamento (PO) | {postado \| pendente} | (mantém Em andamento) | {YYYY-MM-DD HH:MM} |
| Design | {postado \| pendente} | (mantém Em andamento) | {YYYY-MM-DD HH:MM} |
| Build | {postado \| pendente} | Em andamento → Em revisão | {YYYY-MM-DD HH:MM} |
| Ship | {postado \| pendente} | Em revisão → Concluído | {YYYY-MM-DD HH:MM} |

---

## Histórico de Revisões

| Versão | Data | Fase | Mudança |
|--------|------|------|---------|
| 1.0 | {YYYY-MM-DD} | Define | State criado |
