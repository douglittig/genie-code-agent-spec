---
name: build
description: Execute a implementação com geração de tarefas on-the-fly (Fase 3)
---

# Build

> Execução da implementação com geração de tarefas on-the-fly (Fase 3)

## Uso

```
build <design-file>
```

## Exemplos

```
build .claude/sdd/features/DESIGN_SISTEMA_NOTIFICACOES.md
build DESIGN_AUTH_USUARIO.md
```

---

## Visão Geral

Esta é a **Fase 3** do workflow SDD de 5 fases:

```text
Fase 0: brainstorm → .claude/sdd/features/BRAINSTORM_{FEATURE}.md (opcional)
Fase 1: define     → .claude/sdd/features/DEFINE_{FEATURE}.md
Fase 2: design     → .claude/sdd/features/DESIGN_{FEATURE}.md
Fase 3: build      → Código + .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md (ESTA FASE)
Fase 4: ship       → .claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md
```

A fase de build executa a implementação, gerando tarefas on-the-fly a partir do File Manifest.

---

## O que Esta Fase Faz

1. **Parsear** — Extrair o File Manifest do DESIGN
2. **Priorizar** — Ordenar arquivos por dependências
3. **Executar** — Criar cada arquivo com verificação
4. **Validar** — Rodar testes após cada mudança significativa
5. **Reportar** — Gerar o build report

---

## Processo

### Passo 1: Carregar Contexto

```markdown
Ler .claude/sdd/features/DESIGN_{FEATURE}.md
Ler .claude/sdd/features/DEFINE_{FEATURE}.md
Ler CLAUDE.md
```

### Passo 2: Extrair Tarefas do File Manifest

Converta o File Manifest em uma lista de tarefas:

```markdown
Do File Manifest do DESIGN:
| Arquivo | Ação | Propósito |

Gerar:
- [ ] Criar/Modificar {arquivo1}
- [ ] Criar/Modificar {arquivo2}
- [ ] ...
```

### Passo 3: Ordenar por Dependências

Analise imports e dependências para determinar a ordem de execução.

### Passo 4: Executar Cada Tarefa

Para cada arquivo:

1. **Escrever** — Criar o arquivo seguindo os padrões de código do DESIGN
2. **Verificar** — Rodar comando de verificação (lint, type check, import test)
3. **Marcar Completo** — Atualizar progresso

### Passo 5: Rodar Validação Completa

Após todos os arquivos criados:

```bash
# Lint check
ruff check .

# Type check (se aplicável)
mypy .

# Rodar testes
pytest
```

### Passo 6: Gerar Build Report

```markdown
Salvar em: .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md
```

---

## Output

| Artefato | Localização |
|----------|-------------|
| **Código** | Conforme especificado no File Manifest do DESIGN |
| **Build Report** | `.claude/sdd/reports/BUILD_REPORT_{FEATURE}.md` |

**Próximo Passo:** Ship — `DEFINE_{FEATURE}.md` (quando pronto)

---

## Loop de Execução

O build-agent segue este loop para cada tarefa:

```text
┌─────────────────────────────────────────────────────┐
│                  EXECUTAR TAREFA                     │
├─────────────────────────────────────────────────────┤
│  1. Ler tarefa do manifest                          │
│  2. Escrever código seguindo padrões do DESIGN      │
│  3. Rodar comando de verificação                    │
│     └─ Se FALHAR → Corrigir e tentar novamente      │
│        (máx. 3 tentativas)                          │
│  4. Marcar tarefa completa                          │
│  5. Mover para a próxima tarefa                     │
└─────────────────────────────────────────────────────┘
```

---

## Gate de Qualidade

Antes de marcar como completo, verifique:

```text
[ ] Todos os arquivos do manifest criados
[ ] Todos os comandos de verificação passaram
[ ] Lint check passou
[ ] Testes passaram (se aplicável)
[ ] Sem comentários TODO no código
[ ] Build report gerado
```

---

## Dicas

1. **Siga o DESIGN** — Não improvise, use os padrões de código
2. **Verifique Incrementalmente** — Teste após cada arquivo, não no final
3. **Corrija Para Frente** — Se algo quebrar, corrija imediatamente
4. **Autocontido** — Cada arquivo deve ser funcionalmente independente
5. **Sem Comentários** — O código deve ser autodocumentado

---

## Tratando Problemas Durante o Build

Se encontrar problemas:

| Problema | Ação |
|----------|------|
| Requisito faltando | Use iterate para atualizar o DEFINE |
| Problema de arquitetura | Use iterate para atualizar o DESIGN |
| Bug simples | Corrija imediatamente e continue |
| Bloqueador grave | Pare e reporte no build report |

---

## Referências

- Agente: `agents/build-agent.md`
- Template: `templates/BUILD_REPORT_TEMPLATE.md`
- Contratos: `architecture/WORKFLOW_CONTRACTS.yaml`
- Próxima Fase: `commands/ship.md`
