---
name: design
description: Crie arquitetura e especificação técnica em uma passagem (Fase 2)
---

# Design

> Criação de arquitetura e especificação técnica em uma passagem (Fase 2)

## Uso

```
design <define-file>
```

## Exemplos

```
design .claude/sdd/features/DEFINE_SISTEMA_NOTIFICACOES.md
design DEFINE_AUTH_USUARIO.md
design .claude/sdd/features/DEFINE_API_BUSCA.md
```

---

## Visão Geral

Esta é a **Fase 2** do workflow SDD de 5 fases:

```text
Fase 0: brainstorm → .claude/sdd/features/BRAINSTORM_{FEATURE}.md (opcional)
Fase 1: define     → .claude/sdd/features/DEFINE_{FEATURE}.md
Fase 2: design     → .claude/sdd/features/DESIGN_{FEATURE}.md (ESTA FASE)
Fase 3: build      → Código + .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md
Fase 4: ship       → .claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md
```

O Design combina o que antes era Plan + Spec + ADRs em um único documento com decisões arquiteturais inline.

---

## O que Esta Fase Faz

1. **Analisar** — Entender os requisitos do DEFINE
2. **Arquitetar** — Projetar a solução de alto nível com diagramas
3. **Decidir** — Documentar decisões principais com justificativa (ADRs inline)
4. **Especificar** — Criar o File Manifest e padrões de código
5. **Planejar Testes** — Definir a estratégia de testes

---

## Processo

### Passo 1: Carregar Contexto

```markdown
Ler .claude/sdd/features/DEFINE_{FEATURE}.md
Ler template DESIGN_TEMPLATE.md
Ler CLAUDE.md

# Explorar padrões no codebase:
Glob(**/*.py) | head -20
Grep("class |def ") | sample
```

### Passo 2: Criar Arquitetura

Projete a solução:

| Componente | Conteúdo |
|------------|---------|
| **Visão Geral** | Diagrama ASCII do sistema |
| **Componentes** | Lista de módulos/serviços |
| **Fluxo de Dados** | Como os dados se movem pelo sistema |
| **Pontos de Integração** | Dependências externas |

### Passo 3: Documentar Decisões (ADRs Inline)

Para cada escolha significativa:

```markdown
### Decisão: {Nome}

| Atributo | Valor |
|----------|-------|
| **Status** | Aceita |
| **Data** | YYYY-MM-DD |

**Contexto:** Por que esta decisão foi necessária

**Escolha:** O que estamos fazendo

**Justificativa:** Por que esta abordagem

**Alternativas Rejeitadas:**
1. Opção A — rejeitada porque X
2. Opção B — rejeitada porque Y

**Consequências:**
- Trade-off que aceitamos
- Benefício que obtemos
```

### Passo 4: Criar o File Manifest

Liste todos os arquivos a criar/modificar:

| # | Arquivo | Ação | Propósito | Dependências |
|---|---------|------|-----------|--------------|
| 1 | `caminho/para/arquivo.py` | Criar | Handler principal | Nenhuma |
| 2 | `caminho/para/config.yaml` | Criar | Configuração | Nenhuma |
| 3 | `caminho/para/handler.py` | Criar | Handler de requisições | 1, 2 |

### Passo 5: Definir Padrões de Código

Forneça snippets prontos para copiar e colar para os padrões principais.

### Passo 6: Planejar Estratégia de Testes

| Tipo de Teste | Escopo | Ferramentas |
|---------------|--------|-------------|
| Unitário | Funções | pytest |
| Integração | API | pytest + requests |
| E2E | Fluxo completo | Manual/automatizado |

### Passo 7: Salvar

```markdown
Salvar em: .claude/sdd/features/DESIGN_{FEATURE_NAME}.md
```

---

## Output

| Artefato | Localização |
|----------|-------------|
| **DESIGN** | `.claude/sdd/features/DESIGN_{FEATURE_NAME}.md` |

**Próximo Passo:** Build — `DESIGN_{FEATURE_NAME}.md`

---

## Gate de Qualidade

Antes de salvar, verifique:

```text
[ ] Diagrama de arquitetura está claro
[ ] Todas as decisões principais documentadas com justificativa
[ ] File Manifest está completo (todos os arquivos listados)
[ ] Padrões de código estão prontos para copiar e colar
[ ] Estratégia de testes cobre os requisitos
[ ] Sem dependências circulares na arquitetura
```

---

## Dicas

1. **Diagrama Primeiro** — ASCII art clarifica o pensamento
2. **Decisões São Permanentes** — Documente o "por quê" e não apenas o "o quê"
3. **Arquivos Autocontidos** — Cada arquivo deve funcionar de forma independente
4. **Config, Não Código** — Use YAML para valores configuráveis, não valores hardcoded
5. **Teste Desde o Início** — Projete para testabilidade desde o começo

---

## Referências

- Agente: `agents/design-agent.md`
- Template: `templates/DESIGN_TEMPLATE.md`
- Contratos: `architecture/WORKFLOW_CONTRACTS.yaml`
- Próxima Fase: `commands/build.md`
