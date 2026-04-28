---
name: brainstorm
description: Explore ideias por diálogo colaborativo antes da captura de requisitos (Fase 0)
---

# Brainstorm

> Exploração colaborativa antes da captura de requisitos (Fase 0)

## Uso

```
brainstorm <ideia-ou-pedido>
brainstorm "Construir um sistema de notificações em tempo real"
brainstorm notas/ideia-bruta.txt
```

## Exemplos

```
# A partir de uma ideia direta
brainstorm "Quero automatizar verificações de qualidade de dados"

# A partir de um arquivo com notas
brainstorm docs/notas-de-reuniao.md

# A partir de um problem statement
brainstorm "Nosso time gasta muito tempo com entrada manual de dados"
```

---

## Visão Geral

Esta é a **Fase 0** do workflow SDD de 5 fases:

```text
Fase 0: brainstorm → .claude/sdd/features/BRAINSTORM_{FEATURE}.md (ESTA FASE)
Fase 1: define     → .claude/sdd/features/DEFINE_{FEATURE}.md
Fase 2: design     → .claude/sdd/features/DESIGN_{FEATURE}.md
Fase 3: build      → Código + .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md
Fase 4: ship       → .claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md
```

A fase de brainstorm explora ideias por diálogo antes de capturar requisitos formais.

---

## O que Esta Fase Faz

1. **Explorar** — Entender o contexto do projeto e padrões existentes
2. **Questionar** — Fazer uma pergunta por vez para clarificar a intenção
3. **Coletar** — Reunir arquivos de exemplo, ground truth ou dados de referência para grounding do LLM
4. **Propor** — Apresentar 2-3 abordagens com trade-offs
5. **Simplificar** — Aplicar YAGNI para remover features desnecessárias
6. **Validar** — Confirmar o entendimento de forma incremental
7. **Documentar** — Gerar o documento BRAINSTORM para o Define

---

## Processo

### Passo 1: Coletar Contexto

```markdown
Ler CLAUDE.md
Ler template BRAINSTORM_TEMPLATE.md
Explorar estrutura do projeto, commits recentes, padrões existentes
```

### Passo 2: Perguntas de Descoberta

Faça perguntas UMA DE CADA VEZ:

| Tipo de Pergunta | Quando Usar |
|-----------------|-------------|
| Múltipla Escolha | Quando as opções são claras (preferido) |
| Aberta | Quando explorando território desconhecido |
| Esclarecedora | Quando a resposta foi vaga |

**Mínimo:** 3 perguntas antes de propor abordagens

### Passo 3: Coleta de Amostras (Grounding do LLM)

Pergunte sobre amostras disponíveis para melhorar a precisão:

```markdown
"Você tem alguma amostra que possa ajudar a embasar a solução?
(a) Arquivos de input de exemplo
(b) Exemplos de output esperado
(c) Ground truth / dados verificados
(d) Nenhum disponível"
```

Se existirem amostras, analise-as e documente no output do BRAINSTORM.

### Passo 4: Explorar Abordagens

Apresente 2-3 abordagens distintas:

```markdown
### Approach A: {Nome} ⭐ Recomendada
**Por quê:** {Raciocínio}
**Prós:** {Benefícios}
**Contras:** {Trade-offs}

### Approach B: {Nome}
**Por que não recomendada:** {Raciocínio}
```

### Passo 5: Aplicar YAGNI

Para cada feature, pergunte:
- Precisamos disso para o MVP?
- Isso resolve o problema central?

Remova as features que não passarem. Documente o que foi removido e por quê.

### Passo 6: Validar Incrementalmente

Apresente o design em seções (200-300 palavras cada):

```text
Seção → Verificar com o usuário → Ajustar se necessário → Próxima seção
```

**Mínimo:** 2 checkpoints de validação

### Passo 7: Gerar Documento

```markdown
Salvar em: .claude/sdd/features/BRAINSTORM_{FEATURE}.md
```

---

## Output

| Artefato | Localização |
|----------|-------------|
| **Documento Brainstorm** | `.claude/sdd/features/BRAINSTORM_{FEATURE}.md` |

**Próximo Passo:** Define — `BRAINSTORM_{FEATURE}.md`

---

## Gate de Qualidade

Antes de marcar como completo:

```text
[ ] Mínimo de 3 perguntas de descoberta feitas
[ ] Pergunta sobre coleta de amostras feita
[ ] Pelo menos 2 abordagens exploradas
[ ] YAGNI aplicado (features removidas)
[ ] Mínimo de 2 validações concluídas
[ ] Usuário confirmou a abordagem selecionada
[ ] Requisitos de rascunho incluídos
```

---

## Estilo de Interação

### Uma Pergunta por Vez

```markdown
BOM:
"Qual é o caso de uso principal?
(a) Relatório interno
(b) Voltado ao cliente
(c) Ambos"

RUIM:
"Qual é o caso de uso? Quem são os usuários? Qual é o prazo?"
```

### Lidere com a Recomendação

```markdown
BOM:
"Recomendo a Approach A porque [raciocínio].
Aqui estão as alternativas a considerar..."

RUIM:
"Aqui estão três abordagens. Qual você quer?"
```

### Esteja Pronto para Voltar

```markdown
BOM:
"Isso é diferente do que eu entendi. Deixa eu revisar..."

RUIM:
"Passando para a próxima seção..."
```

---

## Quando Usar Brainstorm vs Define

| Cenário | Use |
|---------|-----|
| Ideia vaga, precisa explorar | `brainstorm` |
| Requisitos claros, pronto para capturar | `define` diretamente |
| Documento BRAINSTORM existente | `define <brainstorm-file>` |
| Notas de reunião com pedidos claros | `define` diretamente |
| "Quero construir algo mas não sei exatamente o quê" | `brainstorm` |

---

## Dicas

1. **Tome seu tempo** — Exploração é sobre entendimento, não velocidade
2. **Pergunte o porquê** — "Por que você precisa disso?" revela os requisitos reais
3. **Desafie o escopo** — A maioria das features não é necessária para o MVP
4. **Confie no usuário** — Ele conhece o domínio, você conhece os padrões
5. **Documente features removidas** — Elas podem voltar mais tarde

---

## Tratando Diferentes Tipos de Input

| Tipo de Input | Abordagem |
|---------------|-----------|
| Ideia vaga | Comece com "Me conta mais sobre..." |
| Pedido específico | Valide o entendimento, depois explore abordagens |
| Problem statement | Foque nos pain points, depois nas soluções |
| Feature request | Questione a necessidade, explore alternativas |
| Pedido de comparação | Explore trade-offs, faça uma recomendação |

---

## Referências

- Agente: `agents/brainstorm-agent.md`
- Template: `templates/BRAINSTORM_TEMPLATE.md`
- Contratos: `architecture/WORKFLOW_CONTRACTS.yaml`
- Próxima Fase: `commands/define.md`
