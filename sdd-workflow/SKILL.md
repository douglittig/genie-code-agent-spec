---
name: sdd-workflow
description: |
  Orquestrador do workflow de Spec-Driven Development (SDD) para o Genie Code. Use de forma
  PROATIVA quando o usuário falar em construir features, ler specs do Confluence, gerar código
  a partir de requisitos de negócio, atualizar tickets no Jira, criar PRs ou revisar código.
  Guia pelas 5 fases: Brainstorm → Define → Design → Build → Ship, roteando cada fase para a
  skill dedicada (@sdd-brainstorm, @sdd-define, @sdd-design, @sdd-build, @sdd-ship), com
  integração Confluence MCP (ingestão de spec) e Jira MCP via @sdd-doc (atualização de ticket).
---

# SDD Workflow — Genie Code

Spec-Driven Development transforma requisitos em código rastreável. Cada arquivo gerado
é vinculado ao requisito que o originou — sem "vibe coding", sem specs que ninguém lê.

**Esta skill é o orquestrador:** ela conhece as fases, os gates e os handoffs, e delega a
execução de cada fase para a skill dedicada. Cada skill de fase é **autocontida** — carrega
seu próprio template e suas próprias instruções.

## Skills do Workflow

| Fase | Skill | Papel |
|------|-------|-------|
| 0 — Brainstorm (opcional) | `@sdd-brainstorm` | Explorar ideia, comparar abordagens, definir escopo |
| 1 — Define | `@sdd-define` | Extrair requisitos (Confluence MCP), Clarity Score, criar o state |
| 2 — Arquitetura | `@sdd-staff-engineer` | Revisão da spec + decisão arquitetural → ADR |
| 3 — Planejamento | `@sdd-po` | Epic → Stories (Fibonacci) → Tasks no Jira |
| 4 — Design | `@sdd-design` | Arquitetura técnica + File Manifest a partir do ADR |
| 5 — Build | `@sdd-build` | Implementação delegando às skills `@databricks-*` |
| 6 — Ship | `@sdd-ship` | Archive + lições aprendidas + fechamento do ticket |
| Cross-cutting | `@sdd-iterate` | Mudanças mid-stream com análise de cascata |
| Cross-cutting | `@sdd-doc` | Hook de fim de fase: comentário + transição no Jira |
| Suporte (Fase 4+) | `@sdd-dev-workflow` | Branch → commit → PR → merge |
| Suporte (Fase 4+) | `@sdd-code-reviewer` | Review de segurança, qualidade e performance |

## Fluxo Completo

```
Confluence (SPEC) → DEFINE → @sdd-staff-engineer → @sdd-po → DESIGN → BUILD → PR/Review → SHIP
      ↑                           (ADR)           (Stories/Jira)                          ↓
  (via MCP)                                                                        (via MCP Jira)
                      └──────────────────── @sdd-doc (hook por fase) ────────────────────┘
                                    comentário + transição no ticket Jira
```

O **`@sdd-doc`** é transversal: ao final de **cada** fase ele documenta o avanço no ticket Jira
(comentário estruturado + transição de status) e atualiza o ledger de rastreabilidade.

## Regras do Fluxo

1. **Brainstorm** é opcional — pular para Define se a SPEC já está clara
2. **Define** exige Clarity Score ≥ 12/15 antes de avançar; captura a `jira_key` (Epic) e cria o **state**
3. **Após Define** — acionar `@sdd-staff-engineer` para gerar o ADR
4. **Após ADR** — acionar `@sdd-po` para quebrar em Stories (Fibonacci) + Tasks no Jira
5. **Design** usa o ADR como fonte de verdade vinculante; deve ter File Manifest completo
6. **Build** delega cada arquivo à skill Databricks indicada no manifest
7. **Ship** arquiva todos os artefatos (incluindo o state) e fecha o ticket no Jira

### Protocolo de Fim-de-Fase (obrigatório em toda fase)

Toda fase termina com a mesma sequência — é o que mantém o Jira e o state sincronizados:

```
1. Gerar o artefato da fase (DEFINE / ADR / DESIGN / BUILD_REPORT / SHIPPED)
2. Atualizar o ledger:        .claude/sdd/state/{FEATURE}.md
3. Acionar a skill @sdd-doc:  documenta no Jira (comentário + transição)
4. Sugerir a próxima fase
```

### Ledger de Rastreabilidade (state)

`.claude/sdd/state/{FEATURE}.md` é a **fonte única da verdade** da feature: guarda a `jira_key`,
a URL do Confluence, a fase atual, os caminhos dos artefatos, os gate scores e o log de ações no
Jira. Criado na fase Define (template `STATE_TEMPLATE.md` da `@sdd-define`), atualizado por toda
fase, arquivado no Ship. É de onde o `@sdd-doc` obtém a chave do ticket.

---

## Fase 0 — Brainstorm (opcional) → `@sdd-brainstorm`

**Quando usar:** ideia vaga, requisitos não claros, precisa explorar abordagens antes de capturar requisitos formais.
**Quando pular:** SPEC do Confluence já clara, ou BRAINSTORM_*.md já existe.

**Output:** `docs/specs/BRAINSTORM_{FEATURE}.md`
**Gate:** mín. 3 perguntas, 2 abordagens exploradas, YAGNI aplicado, usuário confirmou abordagem.

---

## Fase 1 — Define → `@sdd-define`

**Quando usar:** BRAINSTORM pronto ou SPEC do Confluence disponível.
**Integração Confluence:** fornecer URL ou page-id → ler via MCP (`confluence_get_page`, nunca `confluence_search`) → extrair objetivo, usuários, critérios de aceite, restrições.
**Integração Jira:** capturar a chave do ticket (ex: `PROJ-123`) e gravá-la no **state** — é o que todas as fases e o `@sdd-doc` reutilizam. Sem chave → o `@sdd-doc` opera em modo pendente.

**Output:** `docs/specs/DEFINE_{FEATURE}.md` + `.claude/sdd/state/{FEATURE}.md` (ledger criado aqui)
**Gate:** Clarity Score ≥ 12/15. Se menor, pedir esclarecimentos antes de avançar.
**Fim-de-fase:** atualizar o state → `@sdd-doc` documenta no Jira (transição → Em andamento).
**Próximo passo natural:** `@sdd-staff-engineer` — revisão da spec e decisão arquitetural (ADR) antes do Design.

**Gate iterativo — a skill não avança até a spec estar validada:**

| Score | Ação |
|-------|------|
| ≥ 12/15 | Gera `DEFINE_{FEATURE}.md` → sugere `@sdd-staff-engineer` |
| 9–11/15 | Faz perguntas direcionadas → re-pontua |
| < 9/15  | Bloqueia — exige esclarecimento antes de continuar |

> **Nota:** As skills `@databricks-*` não são invocadas nesta fase — são apenas *identificadas*
> no Contexto Técnico para uso nas fases de Design e Build.

---

## Fase 2 — Arquitetura (ADR) → `@sdd-staff-engineer`

**Quando usar:** DEFINE pronto com Clarity Score ≥ 12/15.
**Output:** `docs/adr/ADR_{FEATURE}.md` — **vinculante** para o Design e o Build.
**Fim-de-fase:** atualizar o state → `@sdd-doc` documenta no Jira (mantém Em andamento).

---

## Fase 3 — Planejamento → `@sdd-po`

**Quando usar:** ADR aprovado.
**Output:** `docs/planning/STORIES_{FEATURE}.md` + Stories/Tasks criadas no Jira sob o Epic.
**Fim-de-fase:** `@sdd-doc` comenta o plano no Epic (mantém Em andamento).

---

## Fase 4 — Design → `@sdd-design`

**Quando usar:** DEFINE pronto com Clarity Score ≥ 12/15 (e ADR, se existir).
**ADR:** se `docs/adr/ADR_{FEATURE}.md` existir, ele é vinculante — o `@sdd-design` executa o ADR, não reabre decisões.

**Output:** `docs/designs/DESIGN_{FEATURE}.md`
**Gate:** File Manifest completo — todos os arquivos com skill Databricks atribuída.
**Fim-de-fase:** atualizar o state → `@sdd-doc` documenta no Jira (mantém Em andamento).

---

## Fase 5 — Build → `@sdd-build`

**Quando usar:** DESIGN pronto com File Manifest completo.
**Processo:** executar o File Manifest arquivo por arquivo, delegando para a skill Databricks indicada.

**Output:** código + `.claude/sdd/reports/BUILD_REPORT_{FEATURE}.md`
**Gate:** todos os arquivos criados, lint e testes passando, sem credenciais hardcoded.
**Fim-de-fase:** atualizar o state → `@sdd-doc` documenta no Jira (transição → Em revisão).

---

## Fase 6 — Ship → `@sdd-ship`

**Quando usar:** Build completo e validado.
**Integração Jira:** o `@sdd-doc` comenta o SHIPPED + link do PR e transiciona o ticket para "Concluído".
**PR e Review:** delegar para `@sdd-dev-workflow` (branch → commit → PR) e `@sdd-code-reviewer` (review de segurança e qualidade).

**Bloqueadores de merge:** falha em acceptance test, credencial exposta, breaking change sem deprecation period.

**Output:** `.claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md` (com o state arquivado) + Jira atualizado
**Gate:** lições capturadas, ticket fechado, artefatos arquivados.
**Fim-de-fase:** `@sdd-doc` documenta no Jira (transição → Concluído) → arquivar o state.

---

## Iterate — Mudanças Mid-Stream → `@sdd-iterate`

Quando requisitos mudarem durante qualquer fase:
1. Atualizar o documento da fase onde a mudança entrou
2. Verificar impacto cascata nas fases seguintes (DEFINE → DESIGN → código)
3. Documentar no revision history do artefato e no state
4. Fim-de-fase: `@sdd-doc` registra a mudança de escopo como comentário no Jira (sem transição)

---

## Documentação no Jira → `@sdd-doc`

A skill `@sdd-doc` é o hook transversal chamado no **fim de cada fase** (ver Protocolo de
Fim-de-Fase). Ela lê a `jira_key` do state, monta o comentário com seu `JIRA_UPDATE_TEMPLATE.md`,
mostra um **preview** ao usuário, e então posta o comentário + transiciona o ticket.

**Ferramentas MCP Jira (4):** `jira_get_issue`, `jira_get_transitions`, `jira_add_comment`,
`jira_transition_issue`. Sem `jira_key` no state — ou com o MCP Jira indisponível/falhando —
→ modo pendente (não escreve, registra e avisa).

---

## Localização dos Artefatos

```
docs/
├── specs/      BRAINSTORM_*.md, DEFINE_*.md
├── adr/        ADR_*.md  (gerado pelo @sdd-staff-engineer)
├── planning/   STORIES_*.md  (gerado pelo @sdd-po)
└── designs/    DESIGN_*.md

.claude/sdd/
├── state/      {FEATURE}.md  (ledger de rastreabilidade — fonte da verdade)
├── reports/    BUILD_REPORT_*.md
└── archive/    {FEATURE}/ com todos os docs + state + SHIPPED_*.md
```
