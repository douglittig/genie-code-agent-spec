---
name: sdd-workflow
description: |
  Spec-Driven Development (SDD) workflow for Genie Code. Use PROACTIVELY when
  the user discusses building features, reading specs from Confluence, generating
  code from business requirements, updating Jira tickets, creating PRs, or
  reviewing code. Guides through the 5-phase workflow:
  Brainstorm → Define → Design → Build → Ship,
  with Confluence MCP (spec ingestion) and Jira MCP (ticket update) integrated.
---

# SDD Workflow — Genie Code

Spec-Driven Development transforma requisitos em código rastreável. Cada arquivo gerado
é vinculado ao requisito que o originou — sem "vibe coding", sem specs que ninguém lê.

## Fluxo Completo

```
Confluence (SPEC) → DEFINE → DESIGN → BUILD → Jira (update) → PR → Review
      ↑                                              ↓
  (via MCP)                                      (via MCP)
```

## As 5 Fases

| Fase | Output | Gate de qualidade |
|------|--------|-------------------|
| 0 — Brainstorm (opcional) | `BRAINSTORM_{FEATURE}.md` | Mín. 3 perguntas, 2 abordagens, YAGNI aplicado |
| 1 — Define | `DEFINE_{FEATURE}.md` | Clarity Score ≥ 12/15 |
| 2 — Design | `DESIGN_{FEATURE}.md` | Todos os arquivos têm agente atribuído |
| 3 — Build | Código + `BUILD_REPORT_{FEATURE}.md` | Testes passam, atribuição por especialista |
| 4 — Ship | `SHIPPED_{DATE}.md` + Jira atualizado | Lições capturadas |

## Quando Guiar o Usuário

- "Quero construir..." → Sugerir Brainstorm ou Define
- "Tenha a SPEC no Confluence" → Ler via MCP e gerar Define
- Tem DEFINE pronto → Sugerir Design
- Tem DESIGN pronto → Executar Build
- Build completo → Atualizar Jira, criar PR, review, ship

## Regras do Fluxo

1. **Brainstorm** é opcional — pular para DEFINE se a SPEC já está clara
2. **Define** exige Clarity Score ≥ 12/15 antes de avançar — se menor, pedir esclarecimentos
3. **Design** deve ter File Manifest completo — nenhum arquivo sem agente atribuído
4. **Build** delega cada arquivo ao agente especializado, gera BUILD_REPORT com atribuição
5. **Ship** arquiva tudo e atualiza o Jira antes de fechar

## Integração Confluence → Define

Quando o usuário fornecer uma URL ou page-id do Confluence:

1. Ler o conteúdo via MCP Confluence
2. Extrair: objetivo, usuários, critérios de aceite, restrições, integrações
3. Mapear para o template DEFINE (ver `templates/DEFINE_TEMPLATE.md`)
4. Calcular Clarity Score — pedir esclarecimentos se < 12/15
5. Salvar em `.claude/sdd/features/DEFINE_{FEATURE}.md`

## Integração Jira → Ship

Após BUILD e antes do archive:

1. Mover ticket para "In Review"
2. Adicionar link do PR como comentário
3. Após merge: mover para "Done" + link do commit

## File Manifest (Design)

Cada arquivo recebe um agente especializado do ecossistema Databricks:

| Agente | Especialidade |
|--------|--------------|
| `@lakeflow-pipeline-builder` | SDP pipelines, autoloader, streaming tables |
| `@spark-engineer` | PySpark, DataFrames, transformações |
| `@spark-streaming-architect` | Streaming, checkpoints, stateful operations |
| `@sql-optimizer` | SQL, performance, particionamento |
| `@medallion-architect` | Bronze/Silver/Gold layers |
| `@data-quality-analyst` | Testes de qualidade, assertions |
| `@python-developer` | Scripts Python, SDK calls |
| `@test-generator` | pytest, fixtures, suites de teste |
| `@code-reviewer` | Review arquitetural, boas práticas |

## Criação de PR e Review

Após BUILD completo:

1. Rodar review antes do PR: verificar acceptance tests do DEFINE, segurança, qualidade
2. Criar PR com conventional commits (`feat:`, `fix:`, `refactor:`, `test:`, `chore:`)
3. Bloqueadores que impedem merge: falha em acceptance test, credencial exposta, breaking change sem deprecation

## Iterate (Mudanças Mid-Stream)

Quando requisitos mudarem durante qualquer fase, propagar a mudança pelo pipeline:
- Atualizar o documento da fase onde a mudança entrou
- Verificar impacto cascata nas fases seguintes
- Documentar no revision history do artefato

## Localização dos Artefatos

Todos os documentos SDD ficam no workspace do projeto:

```
.claude/sdd/
├── features/       BRAINSTORM_*.md, DEFINE_*.md, DESIGN_*.md
├── reports/        BUILD_REPORT_*.md
└── archive/        {FEATURE}/ com todos os docs + SHIPPED_*.md
```

## Reference Files nesta Skill

| Arquivo | Conteúdo |
|---------|---------|
| `templates/BRAINSTORM_TEMPLATE.md` | Template fase 0 |
| `templates/DEFINE_TEMPLATE.md` | Template fase 1 (com Clarity Score) |
| `templates/DESIGN_TEMPLATE.md` | Template fase 2 (com File Manifest) |
| `templates/BUILD_REPORT_TEMPLATE.md` | Template fase 3 |
| `templates/SHIPPED_TEMPLATE.md` | Template fase 4 |
| `architecture/WORKFLOW_CONTRACTS.yaml` | Regras de transição entre fases |
| `architecture/ARCHITECTURE.md` | Arquitetura completa do framework |
| `commands/define.md` | Instrução detalhada da fase Define |
| `commands/design.md` | Instrução detalhada da fase Design |
| `commands/build.md` | Instrução detalhada da fase Build |
| `commands/ship.md` | Instrução detalhada da fase Ship |
| `commands/create-pr.md` | Criação de PR com conventional commits |
| `commands/review.md` | Dual AI review (estático + arquitetural) |
| `agents/define-agent.md` | Capacidades do agente de Define |
| `agents/design-agent.md` | Capacidades do agente de Design |
| `agents/build-agent.md` | Capacidades do agente de Build |
| `agents/code-reviewer.md` | Capacidades do agente de review |
| `agents/test-generator.md` | Capacidades do agente de testes |
