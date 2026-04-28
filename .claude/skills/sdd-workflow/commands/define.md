# Define

> Captura e validação de requisitos em uma passagem (Fase 1)

## Uso

```
define <input>
```

## Exemplos

```
# A partir de um documento BRAINSTORM (recomendado após brainstorm)
define .claude/sdd/features/BRAINSTORM_SISTEMA_NOTIFICACOES.md

# A partir de notas de reunião ou input bruto
define notas/notas-de-reuniao.md
define "Construir um API gateway para gestão de usuários"
define docs/email-stakeholder.txt
```

---

## Visão Geral

Esta é a **Fase 1** do workflow SDD de 5 fases:

```text
Fase 0: brainstorm → .claude/sdd/features/BRAINSTORM_{FEATURE}.md (opcional)
Fase 1: define     → .claude/sdd/features/DEFINE_{FEATURE}.md (ESTA FASE)
Fase 2: design     → .claude/sdd/features/DESIGN_{FEATURE}.md
Fase 3: build      → Código + .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md
Fase 4: ship       → .claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md
```

O Define combina o que antes era Intake + PRD + Refine em uma única fase iterativa. Quando alimentado com um documento BRAINSTORM, extrai requisitos pré-validados com mínima necessidade de esclarecimento.

---

## O que Esta Fase Faz

1. **Extrair** — Puxar requisitos de qualquer input (notas, e-mails, conversas)
2. **Estruturar** — Organizar em problema, usuários, goals, critérios de sucesso
3. **Validar** — Pontuação de clareza integrada (deve atingir 12/15 para prosseguir)
4. **Esclarecer** — Fazer perguntas direcionadas para preencher lacunas

---

## Processo

### Passo 1: Carregar Contexto

```markdown
Ler template DEFINE_TEMPLATE.md
Ler CLAUDE.md

# Se arquivo fornecido:
Ler <arquivo-de-input>
```

### Passo 2: Classificar Input

Identifique o tipo de input para guiar a extração:

| Tipo de Input | Padrão | Foco |
|---------------|--------|------|
| `brainstorm_document` | BRAINSTORM_*.md do brainstorm | Pré-validado, extrair diretamente |
| `meeting_notes` | Bullet points, ações | Decisões, requisitos |
| `email_thread` | Re:, Fwd:, assinaturas | Pedidos, restrições |
| `conversation` | Linguagem informal | Problema central, usuários |
| `direct_requirement` | Pedido estruturado | Todos os elementos presentes |
| `mixed_sources` | Múltiplos formatos | Consolidar, desduplicar |

**Nota:** Quando o input é um documento BRAINSTORM, a extração é simplificada porque:
- Perguntas de descoberta já foram respondidas
- Abordagens já foram avaliadas
- YAGNI já foi aplicado
- Usuário validou a direção

### Passo 3: Extrair Entidades

Extraia estes elementos do input:

| Elemento | Padrões de Extração |
|----------|---------------------|
| **Problema** | "Estamos com dificuldade em...", "O problema é...", "Pain point:" |
| **Usuários** | "Para o time...", "Os clientes querem...", "Os usuários precisam..." |
| **Goals** | "Precisamos de...", "O goal é...", "Sucesso parece..." |
| **Critérios de Sucesso** | "Sucesso significa...", "Saberemos quando...", "Medido por..." |
| **Acceptance Tests** | "Given/When/Then", "Caso de teste:", "Cenário:" |
| **Restrições** | "Deve funcionar com...", "Não pode mudar...", "Limitado por..." |
| **Fora do Escopo** | "Não inclui...", "Adiado para...", "Excluído:" |

### Passo 4: Calcular o Clarity Score

Pontue cada elemento (0-3 pontos):

| Elemento | Pontuação | Significado |
|----------|-----------|-------------|
| Problema | 0-3 | Claro, específico, acionável |
| Usuários | 0-3 | Identificados com pain points |
| Goals | 0-3 | Resultados mensuráveis |
| Sucesso | 0-3 | Critérios testáveis |
| Escopo | 0-3 | Limites explícitos |

**Guia de Pontuação:**
- 0 = Completamente ausente
- 1 = Vago ou incompleto
- 2 = Claro mas faltam detalhes
- 3 = Crystal clear, acionável

**Mínimo para prosseguir:** 12/15 (80%)

### Passo 5: Preencher Lacunas (se necessário)

Se a pontuação for < 12, faça perguntas específicas:

```markdown
Exemplos de perguntas:
- "Quem é o usuário principal: (a) time interno, (b) clientes, (c) ambos?"
- "Qual é o prazo: (a) este sprint, (b) este trimestre, (c) sem prazo?"
```

### Passo 6: Gerar Documento

Escreva o documento estruturado seguindo o template e salve:

```markdown
Salvar em: .claude/sdd/features/DEFINE_{FEATURE_NAME}.md
```

---

## Output

| Artefato | Localização |
|----------|-------------|
| **DEFINE** | `.claude/sdd/features/DEFINE_{FEATURE_NAME}.md` |

**Próximo Passo:** Design — `DEFINE_{FEATURE_NAME}.md`

---

## Gate de Qualidade

Antes de salvar, verifique:

```text
[ ] Problem statement é claro e específico
[ ] Pelo menos um user persona identificado
[ ] Critérios de sucesso são mensuráveis
[ ] Acceptance tests são testáveis
[ ] Fora do escopo é explícito
[ ] Clarity Score >= 12/15
```

---

## Dicas

1. **Seja Específico** — "Melhorar performance" → "Reduzir latência da API para <200ms"
2. **Use Números** — "Suportar muitos usuários" → "Suportar 1000 usuários simultâneos"
3. **Teste os Critérios** — Se não consegue testar, não está claro o suficiente
4. **Delimite com Ruthlessness** — O que está FORA é tão importante quanto o que está DENTRO

---

## Referências

- Agente: `agents/define-agent.md`
- Template: `templates/DEFINE_TEMPLATE.md`
- Contratos: `architecture/WORKFLOW_CONTRACTS.yaml`
- Fase Anterior: `commands/brainstorm.md` (opcional)
- Próxima Fase: `commands/design.md`
