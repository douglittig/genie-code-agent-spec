# Arquitetura SDD

> Referência visual para o workflow de desenvolvimento Spec-Driven de 5 fases

---

## Visão Geral do Sistema

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PIPELINE SDD — 5 FASES                                                 │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                          │
│   FASE 0              FASE 1              FASE 2              FASE 3              FASE 4                │
│   ════════             ════════             ════════             ════════             ════════            │
│   BRAINSTORM           DEFINE               DESIGN               BUILD                SHIP              │
│   (Explorar)           (O quê + Por quê)    (Como)               (Fazer)              (Fechar)          │
│   [Opcional]                                                                                             │
│                                                                                                          │
│   brainstorm           define               design               build                ship              │
│        │                    │                    │                    │                    │             │
│        ▼                    ▼                    ▼                    ▼                    ▼             │
│   ┌──────────┐         ┌─────────┐          ┌─────────┐          ┌─────────┐          ┌─────────┐       │
│   │BRAINSTORM│────────▶│ DEFINE  │─────────▶│ DESIGN  │─────────▶│  BUILD  │─────────▶│  SHIP   │       │
│   │  AGENT   │ ou pula │  AGENT  │          │  AGENT  │          │  AGENT  │          │  AGENT  │       │
│   │  (Opus)  │         │ (Opus)  │          │ (Opus)  │          │(Sonnet) │          │(Haiku)  │       │
│   └──────────┘         └─────────┘          └─────────┘          └─────────┘          └─────────┘       │
│        │                    │                    │                    │                    │             │
│        ▼                    ▼                    ▼                    ▼                    ▼             │
│   features/            features/            features/            reports/ +           archive/          │
│   BRAINSTORM_*.md      DEFINE_*.md          DESIGN_*.md          ARQUIVOS DE CÓDIGO   {FEATURE}/        │
│                                                                  BUILD_REPORT_*.md    SHIPPED_*.md      │
│                                                                                                          │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                          │
│                                      CROSS-PHASE: ITERATE                                                │
│                                      ═══════════════════                                                 │
│                                                                                                          │
│                                           iterate                                                        │
│                                                │                                                         │
│                                                ▼                                                         │
│                                           ┌─────────┐                                                    │
│                                           │ ITERATE │                                                    │
│                                           │  AGENT  │                                                    │
│                                           │(Sonnet) │                                                    │
│                                           └─────────┘                                                    │
│                                                │                                                         │
│                              ┌─────────────────┼─────────────────┐                                       │
│                              ▼                 ▼                 ▼                                       │
│                       Atualiza BRAINSTORM  Atualiza DEFINE   Atualiza DESIGN                             │
│                       (com cascata)        (com cascata)     (com cascata)                               │
│                                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo das Fases

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    WORKFLOW DE DESENVOLVIMENTO                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   IDEIA BRUTA                                                                            │
│   (pedido vago,         FASE 0: BRAINSTORM (Opcional)                                   │
│    problema)       ──────────────────────────▶   BRAINSTORM_{FEATURE}.md                │
│                           Uma pergunta por vez    - Perguntas de Descoberta              │
│                           2-3 Abordagens          - Abordagens Exploradas                │
│                           YAGNI Aplicado          - Features Removidas                  │
│                                                   - Abordagem Selecionada               │
│                                  │                                                       │
│                                  ▼                                                       │
│   INPUT BRUTO                                                                            │
│   (notas, e-mails,      FASE 1: DEFINE                                                  │
│    brainstorm doc)  ──────────────────────────▶   DEFINE_{FEATURE}.md                   │
│                           Extrair + Validar       - Problem Statement                    │
│                           Clarity Score ≥12       - Usuários-Alvo                        │
│                                                   - Critérios de Sucesso                 │
│                                                   - Acceptance Tests                    │
│                                                   - Fora do Escopo                      │
│                                  │                                                       │
│                                  ▼                                                       │
│                           FASE 2: DESIGN                                                │
│   DEFINE_{FEATURE}.md ─────────────────────▶     DESIGN_{FEATURE}.md                   │
│                           Arquitetar + Decidir    - Diagrama de Arquitetura              │
│                           Sem Dependências        - Decisões Principais                  │
│                           Compartilhadas          - File Manifest                        │
│                                                   - Padrões de Código                   │
│                                                   - Estratégia de Testes                │
│                                  │                                                       │
│                                  ▼                                                       │
│                           FASE 3: BUILD                                                 │
│   DESIGN_{FEATURE}.md ─────────────────────▶     CÓDIGO + BUILD_REPORT                  │
│                           Executar + Verificar    - Todos os arquivos do manifest        │
│                                                   - Resultados de verificação            │
│                           Testes Passam           - Problemas encontrados                │
│                                  │                                                       │
│                                  ▼                                                       │
│                           FASE 4: SHIP                                                  │
│   Todos os Artefatos ───────────────────────▶     archive/{FEATURE}/                    │
│                           Arquivar + Aprender     - Todos os artefatos movidos           │
│                                                   - SHIPPED_{DATE}.md                   │
│                                                   - Lições aprendidas                   │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Estrutura de Pastas (dentro da Skill)

```text
.claude/skills/sdd-workflow/
├── SKILL.md                     # Ponto de entrada da skill
├── templates/                   # 5 templates de documentos
│   ├── BRAINSTORM_TEMPLATE.md
│   ├── DEFINE_TEMPLATE.md
│   ├── DESIGN_TEMPLATE.md
│   ├── BUILD_REPORT_TEMPLATE.md
│   └── SHIPPED_TEMPLATE.md
├── architecture/                # Referência arquitetural
│   ├── WORKFLOW_CONTRACTS.yaml
│   └── ARCHITECTURE.md          (este arquivo)
├── commands/                    # Instruções detalhadas por fase
│   ├── brainstorm.md
│   ├── define.md
│   ├── design.md
│   ├── build.md
│   ├── ship.md
│   ├── iterate.md
│   ├── create-pr.md
│   └── review.md
└── agents/                      # Capacidades dos agentes especializados
    ├── brainstorm-agent.md
    ├── define-agent.md
    ├── design-agent.md
    ├── build-agent.md
    ├── ship-agent.md
    ├── iterate-agent.md
    ├── code-reviewer.md
    └── test-generator.md
```

---

## Atribuição de Modelos

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              ATRIBUIÇÃO ESTRATÉGICA DE MODELOS                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ┌────────────────────────────────────────────────────────────────────────────────┐    │
│   │                                    OPUS                                         │    │
│   │                    (Compreensão Nuançada e Pensamento Criativo)                  │    │
│   │                                                                                 │    │
│   │   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │    │
│   │   │   BRAINSTORM    │    │     DEFINE      │    │     DESIGN      │            │    │
│   │   │     AGENT       │    │     AGENT       │    │     AGENT       │            │    │
│   │   │                 │    │                 │    │                 │            │    │
│   │   │ Exploração      │    │ Extração de     │    │ Decisões de     │            │    │
│   │   │ colaborativa    │    │ requisitos      │    │ arquitetura     │            │    │
│   │   └─────────────────┘    └─────────────────┘    └─────────────────┘            │    │
│   └────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                          │
│   ┌────────────────────────────────────────────────────────────────────────────────┐    │
│   │                                   SONNET                                        │    │
│   │                           (Codificação Rápida e Precisa)                        │    │
│   │                                                                                 │    │
│   │   ┌─────────────────┐              ┌─────────────────┐                         │    │
│   │   │      BUILD      │              │     ITERATE     │                         │    │
│   │   │      AGENT      │              │      AGENT      │                         │    │
│   │   │                 │              │                 │                         │    │
│   │   │ Geração de      │              │ Gerenciamento   │                         │    │
│   │   │ código e        │              │ de mudanças     │                         │    │
│   │   │ verificação     │              │                 │                         │    │
│   │   └─────────────────┘              └─────────────────┘                         │    │
│   └────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                          │
│   ┌────────────────────────────────────────────────────────────────────────────────┐    │
│   │                                    HAIKU                                        │    │
│   │                             (Rápido, Tarefas Simples)                           │    │
│   │                                                                                 │    │
│   │   ┌─────────────────┐                                                          │    │
│   │   │      SHIP       │                                                          │    │
│   │   │      AGENT      │                                                          │    │
│   │   │                 │                                                          │    │
│   │   │ Arquivamento    │                                                          │    │
│   │   │ e documentação  │                                                          │    │
│   │   └─────────────────┘                                                          │    │
│   └────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Dados

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    FLUXO DE DADOS                                        │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   ╔═══════════════════╗                                                                 │
│   ║    IDEIA BRUTA    ║   (Fase 0 Opcional)                                             │
│   ║  (Pedido vago)    ║                                                                 │
│   ╚═════════╤═════════╝                                                                 │
│             │                                                                            │
│             ▼                                                                            │
│   ┌───────────────────┐                                                                 │
│   │ BRAINSTORM_*.md   │─────┐                                                           │
│   │                   │     │                                                           │
│   │ - Perguntas Q&A   │     │                                                           │
│   │ - Abordagens      │     │ (ou pular para DEFINE                                     │
│   │ - Lista YAGNI     │     │  com input bruto)                                         │
│   │ - Caminho Escolh. │     │                                                           │
│   └─────────┬─────────┘     │                                                           │
│             │               │                                                           │
│             ▼               ▼                                                           │
│   ┌───────────────────┐         ┌───────────────────┐                                   │
│   │ DEFINE_*.md       │────────▶│ DESIGN_*.md       │                                   │
│   │                   │         │                   │                                   │
│   │ - Problema        │         │ - Arquitetura     │                                   │
│   │ - Usuários        │         │ - Decisões        │                                   │
│   │ - Sucesso         │         │ - File Manifest   │                                   │
│   │ - Testes          │         │ - Padrões         │                                   │
│   │ - Escopo          │         │ - Testes          │                                   │
│   └───────────────────┘         └─────────┬─────────┘                                   │
│                                           │                                              │
│             ┌─────────────────────────────┴─────────────────────────────┐               │
│             │                                                           │               │
│             ▼                                                           ▼               │
│   ┌───────────────────┐                                       ┌───────────────────┐    │
│   │ ARQUIVOS DE       │                                       │ BUILD_REPORT_*.md │    │
│   │ CÓDIGO            │                                       │                   │    │
│   │                   │                                       │ - Tarefas concl.  │    │
│   │ (Do manifest)     │                                       │ - Verificação     │    │
│   │                   │                                       │ - Problemas       │    │
│   └─────────┬─────────┘                                       └─────────┬─────────┘    │
│             │                                                           │               │
│             └─────────────────────────────┬─────────────────────────────┘               │
│                                           │                                              │
│                                           ▼                                              │
│                              ╔═══════════════════════╗                                  │
│                              ║  archive/{FEATURE}/   ║                                  │
│                              ║                       ║                                  │
│                              ║  - BRAINSTORM_*.md    ║                                  │
│                              ║  - DEFINE_*.md        ║                                  │
│                              ║  - DESIGN_*.md        ║                                  │
│                              ║  - BUILD_REPORT_*.md  ║                                  │
│                              ║  - SHIPPED_*.md       ║                                  │
│                              ╚═══════════════════════╝                                  │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Iteração

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                  FLUXO DE ITERAÇÃO                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│                         iterate DEFINE_*.md "mudança"                                   │
│                                      │                                                   │
│                                      ▼                                                   │
│                              ┌──────────────┐                                            │
│                              │ DETECTAR     │                                            │
│                              │ FASE         │                                            │
│                              └──────┬───────┘                                            │
│                                     │                                                    │
│                    ┌────────────────┴────────────────┐                                   │
│                    ▼                                 ▼                                   │
│            ┌──────────────┐                  ┌──────────────┐                            │
│            │   DEFINE_*   │                  │   DESIGN_*   │                            │
│            │   (Fase 1)   │                  │   (Fase 2)   │                            │
│            └──────┬───────┘                  └──────┬───────┘                            │
│                   │                                 │                                    │
│                   ▼                                 ▼                                    │
│            ┌──────────────┐                  ┌──────────────┐                            │
│            │ APLICAR      │                  │ APLICAR      │                            │
│            │ MUDANÇA +    │                  │ MUDANÇA +    │                            │
│            │ VERSIONAR    │                  │ VERSIONAR    │                            │
│            └──────┬───────┘                  └──────┬───────┘                            │
│                   │                                 │                                    │
│                   ▼                                 ▼                                    │
│            ┌──────────────┐                  ┌──────────────┐                            │
│            │ VERIFICAR    │                  │ VERIFICAR    │                            │
│            │ CASCATA      │                  │ CASCATA      │                            │
│            └──────┬───────┘                  └──────┬───────┘                            │
│                   │                                 │                                    │
│          ┌───────┴────────┐                ┌───────┴────────┐                            │
│          ▼                ▼                ▼                ▼                            │
│   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐                      │
│   │ Sem Impacto│   │ DESIGN     │   │ Sem Impacto│   │  CÓDIGO    │                      │
│   │            │   │ pode       │   │            │   │ pode       │                      │
│   │            │   │ precisar   │   │            │   │ precisar   │                      │
│   │            │   │ atualizar  │   │            │   │ atualizar  │                      │
│   └────────────┘   └────────────┘   └────────────┘   └────────────┘                      │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Gates de Qualidade

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   GATES DE QUALIDADE                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│   FASE 0: BRAINSTORM (Opcional)                                                          │
│   ══════════════════════════════                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐                   │
│   │ Checklist de Exploração                                          │                   │
│   ├─────────────────────────────────────────────────────────────────┤                   │
│   │ [ ] Mínimo de 3 perguntas de descoberta feitas                   │                   │
│   │ [ ] 2-3 abordagens exploradas com trade-offs                     │                   │
│   │ [ ] YAGNI aplicado (seção de features removidas não vazia)       │                   │
│   │ [ ] Mínimo de 2 validações incrementais concluídas               │                   │
│   │ [ ] Usuário confirmou a abordagem selecionada                    │                   │
│   │ [ ] Requisitos de rascunho prontos para o Define                  │                   │
│   └─────────────────────────────────────────────────────────────────┘                   │
│                                                                                          │
│   FASE 1: DEFINE                                                                         │
│   ═══════════════                                                                        │
│   ┌─────────────────────────────────────────────────────────────────┐                   │
│   │ Breakdown do Clarity Score                      Mínimo: 12/15   │                   │
│   ├─────────────────────────────────────────────────────────────────┤                   │
│   │ Problema:  [0-3] Claro, específico, acionável?                  │                   │
│   │ Usuários:  [0-3] Identificados com pain points?                 │                   │
│   │ Goals:     [0-3] Resultados mensuráveis?                        │                   │
│   │ Sucesso:   [0-3] Critérios testáveis?                           │                   │
│   │ Escopo:    [0-3] Limites explícitos?                            │                   │
│   └─────────────────────────────────────────────────────────────────┘                   │
│                                                                                          │
│   FASE 2: DESIGN                                                                         │
│   ═══════════════                                                                        │
│   ┌─────────────────────────────────────────────────────────────────┐                   │
│   │ Checklist                                                        │                   │
│   ├─────────────────────────────────────────────────────────────────┤                   │
│   │ [ ] Diagrama de arquitetura presente                             │                   │
│   │ [ ] Pelo menos uma decisão com justificativa                     │                   │
│   │ [ ] File Manifest completo                                       │                   │
│   │ [ ] Padrões de código prontos para copiar e colar                │                   │
│   │ [ ] Estratégia de testes definida                                │                   │
│   │ [ ] Sem dependências compartilhadas entre unidades               │                   │
│   └─────────────────────────────────────────────────────────────────┘                   │
│                                                                                          │
│   FASE 3: BUILD                                                                          │
│   ══════════════                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐                   │
│   │ Verificação                                                      │                   │
│   ├─────────────────────────────────────────────────────────────────┤                   │
│   │ [ ] Todos os arquivos do manifest criados                        │                   │
│   │ [ ] Todos os comandos de verificação passaram                    │                   │
│   │ [ ] Lint check passou                                            │                   │
│   │ [ ] Testes passaram                                              │                   │
│   │ [ ] Sem comentários TODO no código                               │                   │
│   └─────────────────────────────────────────────────────────────────┘                   │
│                                                                                          │
│   FASE 4: SHIP                                                                           │
│   ═════════════                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐                   │
│   │ Checklist Pré-Ship                                               │                   │
│   ├─────────────────────────────────────────────────────────────────┤                   │
│   │ [ ] BUILD_REPORT mostra 100% de conclusão                        │                   │
│   │ [ ] Todos os testes passando                                     │                   │
│   │ [ ] Sem problemas bloqueadores                                   │                   │
│   │ [ ] Acceptance tests verificados                                 │                   │
│   └─────────────────────────────────────────────────────────────────┘                   │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Histórico de Versões

| Versão | Data | Mudanças |
|--------|------|---------|
| 3.0.0 | 2026-04-14 | Adaptado para o Genie Code / skill system; tradução PT-BR |
| 2.1.0 | 2026-03-26 | Cobertura multi-cloud; 58 agentes, 8 categorias, 23 KB domains |
| 2.0.0 | 2026-03-26 | Pivot de data engineering |
| 1.0.0 | 2026-02-17 | Release pública como AgentSpec v1.0.0 |
