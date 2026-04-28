---
name: sdd-workflow
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
Confluence (SPEC) → DEFINE → DESIGN → BUILD → Jira (update) → PR → Review
      ↑                                              ↓
  (via MCP)                                      (via MCP)
```

## As 5 Fases

| Fase | Output | Gate de qualidade |
|------|--------|-------------------|
| 0 — Brainstorm (opcional) | `BRAINSTORM_{FEATURE}.md` | Mín. 3 perguntas, 2 abordagens, YAGNI aplicado |
| 1 — Define | `DEFINE_{FEATURE}.md` | Clarity Score ≥ 12/15 |
| 2 — Design | `DESIGN_{FEATURE}.md` | Todos os arquivos têm agente atribuído no File Manifest |
| 3 — Build | Código + `BUILD_REPORT_{FEATURE}.md` | Testes passam, atribuição por especialista documentada |
| 4 — Ship | `SHIPPED_{DATE}.md` + Jira atualizado | Lições capturadas, ticket fechado |

## Quando Guiar o Usuário

- "Quero construir..." → Sugerir Brainstorm ou Define
- "Tenho a SPEC no Confluence" → Ler via MCP e gerar Define
- Tem DEFINE pronto → Sugerir Design
- Tem DESIGN pronto → Executar Build
- Build completo → Atualizar Jira, criar PR, fazer review, executar Ship

## Regras do Fluxo

1. **Brainstorm** é opcional — pular para Define se a SPEC já está clara
2. **Define** exige Clarity Score ≥ 12/15 antes de avançar — se menor, pedir esclarecimentos à área de negócio
3. **Design** deve ter File Manifest completo — nenhum arquivo sem agente atribuído
4. **Build** delega cada arquivo ao agente especializado e gera BUILD_REPORT com atribuição por arquivo
5. **Ship** arquiva todos os artefatos e atualiza o Jira antes de fechar

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
2. Adicionar link do PR como comentário no ticket
3. Após merge: mover para "Done" + adicionar link do commit

## File Manifest (Design)

Cada arquivo do manifest recebe uma skill Databricks curada pelo time:

| Skill | Especialidade |
|-------|--------------|
| `@databricks-spark-declarative-pipelines` | SDP/DLT pipelines, Auto Loader, streaming tables, medallion |
| `@databricks-spark-structured-streaming` | Structured Streaming, Kafka, checkpoints, stateful operations |
| `@databricks-dbsql` | SQL warehouses, SQL scripting, stored procedures, performance |
| `@databricks-unity-catalog` | Schemas, volumes, governance, lineage, data contracts |
| `@databricks-model-serving` | Model endpoints, ChatAgent, feature serving |
| `@databricks-bundles` | DABs, deploy multi-ambiente, CICD |
| `@databricks-jobs` | Jobs, scheduling, notificações, monitoramento |
| `@python-dev` | Python, uv, type hints, Ruff, Pyright |
| `@test-generator` | pytest, fixtures, suites de teste |
| `@code-reviewer` | Review arquitetural, segurança, boas práticas |

## Criação de PR e Review

Após BUILD completo:

1. Rodar review antes do PR: verificar acceptance tests do DEFINE, segurança, qualidade de código
2. Criar PR com conventional commits (`feat:`, `fix:`, `refactor:`, `test:`, `chore:`)
3. Bloqueadores que impedem merge: falha em acceptance test, credencial exposta, breaking change sem deprecation period

## Iterate — Mudanças Mid-Stream

Quando requisitos mudarem durante qualquer fase, propagar a mudança pelo pipeline:
- Atualizar o documento da fase onde a mudança entrou
- Verificar impacto cascata nas fases seguintes (DEFINE → DESIGN → código)
- Documentar no revision history do artefato

## Localização dos Artefatos

Todos os documentos SDD ficam no workspace do projeto:

```
.claude/sdd/
├── features/       BRAINSTORM_*.md, DEFINE_*.md, DESIGN_*.md
├── reports/        BUILD_REPORT_*.md
└── archive/        {FEATURE}/ com todos os docs + SHIPPED_*.md
```

## Reference Files desta Skill

| Arquivo | Conteúdo |
|---------|---------|
| `templates/BRAINSTORM_TEMPLATE.md` | Template da fase 0 |
| `templates/DEFINE_TEMPLATE.md` | Template da fase 1 (com Clarity Score) |
| `templates/DESIGN_TEMPLATE.md` | Template da fase 2 (com File Manifest) |
| `templates/BUILD_REPORT_TEMPLATE.md` | Template da fase 3 |
| `templates/SHIPPED_TEMPLATE.md` | Template da fase 4 |
| `architecture/WORKFLOW_CONTRACTS.yaml` | Regras de transição entre fases |
| `architecture/ARCHITECTURE.md` | Arquitetura completa do framework |
| `commands/brainstorm.md` | Instrução detalhada da fase Brainstorm |
| `commands/define.md` | Instrução detalhada da fase Define |
| `commands/design.md` | Instrução detalhada da fase Design |
| `commands/build.md` | Instrução detalhada da fase Build |
| `commands/ship.md` | Instrução detalhada da fase Ship |
| `commands/iterate.md` | Instrução detalhada da fase Iterate |
| `commands/create-pr.md` | Criação de PR com conventional commits |
| `commands/review.md` | Dual AI review (análise estática + arquitetural) |
| `agents/brainstorm-agent.md` | Capacidades do agente de Brainstorm |
| `agents/define-agent.md` | Capacidades do agente de Define |
| `agents/design-agent.md` | Capacidades do agente de Design |
| `agents/build-agent.md` | Capacidades do agente de Build |
| `agents/ship-agent.md` | Capacidades do agente de Ship |
| `agents/iterate-agent.md` | Capacidades do agente de Iterate |
