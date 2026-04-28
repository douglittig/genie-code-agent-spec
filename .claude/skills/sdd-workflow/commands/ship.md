---
name: ship
description: Archive a feature concluída com lições aprendidas (Fase 4)
---

# Ship

> Archive da feature concluída com lições aprendidas (Fase 4)

## Uso

```
ship <define-file>
```

## Exemplos

```
ship .claude/sdd/features/DEFINE_SISTEMA_NOTIFICACOES.md
ship DEFINE_AUTH_USUARIO.md
```

---

## Visão Geral

Esta é a **Fase 4** do workflow SDD de 5 fases:

```text
Fase 0: brainstorm → .claude/sdd/features/BRAINSTORM_{FEATURE}.md (opcional)
Fase 1: define     → .claude/sdd/features/DEFINE_{FEATURE}.md
Fase 2: design     → .claude/sdd/features/DESIGN_{FEATURE}.md
Fase 3: build      → Código + .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md
Fase 4: ship       → .claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md (ESTA FASE)
```

A fase de ship arquiva todos os artefatos da feature e captura as lições aprendidas.

---

## O que Esta Fase Faz

1. **Verificar** — Confirmar que todos os artefatos existem e o build passou
2. **Arquivar** — Mover documentos da feature para a pasta archive
3. **Documentar** — Criar resumo SHIPPED com lições aprendidas
4. **Limpar** — Remover arquivos de trabalho da pasta features

---

## Processo

### Passo 1: Verificar Conclusão

```markdown
Ler .claude/sdd/features/DEFINE_{FEATURE}.md
Ler .claude/sdd/features/DESIGN_{FEATURE}.md
Ler .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md

# Verificar se o build report mostra sucesso
```

### Passo 2: Criar Pasta Archive

```bash
mkdir -p .claude/sdd/archive/{FEATURE_NAME}/
```

### Passo 3: Copiar Artefatos para o Archive

```bash
cp .claude/sdd/features/DEFINE_{FEATURE}.md .claude/sdd/archive/{FEATURE}/
cp .claude/sdd/features/DESIGN_{FEATURE}.md .claude/sdd/archive/{FEATURE}/
cp .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md .claude/sdd/archive/{FEATURE}/
```

### Passo 4: Gerar Documento SHIPPED

Crie o resumo com:

| Seção | Conteúdo |
|-------|---------|
| **Resumo** | O que foi construído |
| **Timeline** | Datas Início → Ship |
| **Métricas** | Linhas de código, arquivos criados |
| **Lições Aprendidas** | O que funcionou, o que melhorar |
| **Artefatos** | Lista de todos os documentos arquivados |

### Passo 5: Atualizar Status dos Documentos

Atualize os documentos arquivados para status "Shipped":

```markdown
Editar: archive/{FEATURE}/DEFINE_{FEATURE}.md
  - Status: → "✅ Shipped"
  - Adicionar revisão: "Shipped e arquivado"

Editar: archive/{FEATURE}/DESIGN_{FEATURE}.md
  - Status: → "✅ Shipped"
  - Adicionar revisão: "Shipped e arquivado"
```

### Passo 6: Limpar Arquivos de Trabalho

```bash
rm .claude/sdd/features/DEFINE_{FEATURE}.md
rm .claude/sdd/features/DESIGN_{FEATURE}.md
rm .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md
```

### Passo 7: Salvar Documento SHIPPED

```markdown
Salvar em: .claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md
```

---

## Output

| Artefato | Localização |
|----------|-------------|
| **SHIPPED** | `.claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md` |
| **DEFINE** | `.claude/sdd/archive/{FEATURE}/DEFINE_{FEATURE}.md` |
| **DESIGN** | `.claude/sdd/archive/{FEATURE}/DESIGN_{FEATURE}.md` |
| **BUILD_REPORT** | `.claude/sdd/archive/{FEATURE}/BUILD_REPORT_{FEATURE}.md` |

**Próximo Passo:** Iniciar nova feature com Define

---

## Gate de Qualidade

Antes de fazer o ship, verifique:

```text
[ ] BUILD_REPORT mostra todas as tarefas concluídas
[ ] Sem problemas críticos no build report
[ ] Todos os testes passando
[ ] Código deployado (se aplicável)
```

---

## Quando Fazer o Ship

Faça o ship quando:
- Todos os acceptance tests do DEFINE passaram
- Build report mostra 100% de conclusão
- Sem problemas bloqueadores restantes

---

## Categorias de Lições Aprendidas

Documente as lições nestas áreas:

| Categoria | Exemplo |
|-----------|---------|
| **Processo** | "Quebrar tarefas em partes menores ajudou" |
| **Técnico** | "Arquivos de config funcionam melhor que env vars" |
| **Comunicação** | "Esclarecimento antecipado evitou retrabalho" |
| **Ferramentas** | "Usar a biblioteca X simplificou Y" |

---

## Dicas

1. **Não Pule Esta Etapa** — Lições aprendidas previnem erros futuros
2. **Seja Honesto** — Documente o que não funcionou também
3. **Seja Específico** — "Melhor planejamento" → "Criar diagrama de arquitetura antes de codificar"
4. **Archive Tudo** — O você do futuro agradecerá o você do presente

---

## Referências

- Agente: `agents/ship-agent.md`
- Template: `templates/SHIPPED_TEMPLATE.md`
- Contratos: `architecture/WORKFLOW_CONTRACTS.yaml`
- Fase Anterior: `commands/build.md`
