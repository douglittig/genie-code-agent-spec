---
name: review
description: Dual AI code review com análise estática + arquitetural para cobertura máxima
needs_discussion: true
discussion_reason: |
  Frontmatter 'name:' implica slash command (/review), paradigma do Claude Code CLI.
  Genie Code não tem slash commands — invocação é via @skill-name em Agent mode.
  Adicionalmente: este arquivo é um command isolado mas code-reviewer.md em agents/
  já cobre a funcionalidade. Decidir: manter duplicidade ou consolidar em agents/code-reviewer.md.
---

# Review

> Dual AI code review com análise estática + arquitetural para cobertura máxima

## Uso

```
review                        # Review de todas as mudanças vs main
review uncommitted            # Review apenas de mudanças não comitadas
review committed              # Review apenas de mudanças comitadas
review --base develop         # Comparar com branch específica
review --quick                # Somente análise estática (mais rápido)
review --deep                 # Somente Claude (mais profundo)
```

---

## Visão Geral

Este comando orquestra um **dual AI review** combinando:

| Revisor | Pontos Fortes |
|---------|---------------|
| **Análise Estática** | Análise estática, scanning de segurança (Gitleaks, Semgrep), linting (Ruff, Pylint), detecção de padrões |
| **Claude** | Review arquitetural, lógica de negócio, design patterns, entendimento contextual |

```text
┌─────────────────────────────────────────────────────────────────┐
│                 PIPELINE DE DUAL AI REVIEW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌───────────────┐          ┌───────────────┐                  │
│   │  Análise      │          │    Claude     │                  │
│   │  Estática     │          │    Code       │                  │
│   └───────┬───────┘          └───────┬───────┘                  │
│           │                          │                           │
│   ┌───────▼───────┐          ┌───────▼───────┐                  │
│   │ • Segurança   │          │ • Arquitetura │                  │
│   │ • Linting     │          │ • Lógica      │                  │
│   │ • Padrões     │          │ • Design      │                  │
│   │ • Estilo      │          │ • Intenção    │                  │
│   └───────┬───────┘          └───────┬───────┘                  │
│           │                          │                           │
│           └────────────┬─────────────┘                          │
│                        │                                         │
│                ┌───────▼───────┐                                 │
│                │   RELATÓRIO   │                                 │
│                │   UNIFICADO   │                                 │
│                └───────────────┘                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Processo

### Passo 1: Determinar Escopo

```bash
# Verificar estado atual
git status
git diff --stat HEAD
git log origin/main..HEAD --oneline 2>/dev/null || echo "Sem commits à frente de main"
```

**Seleção de Escopo:**

| Input do Usuário | Escopo |
|-----------------|--------|
| `review` | Todas as mudanças vs main |
| `review uncommitted` | Apenas diretório de trabalho |
| `review committed` | Apenas mudanças comitadas |
| `review --base <branch>` | Comparar com branch específica |

### Passo 2: Rodar Análise Estática (se disponível)

Se CodeRabbit CLI ou ferramenta similar estiver disponível:

```bash
# Para todas as mudanças:
coderabbit review --plain

# Para uncommitted apenas:
coderabbit review --type uncommitted --plain
```

**Mapeamento de Severidade:**

```text
MAPEAMENTO DE SEVERIDADE
├─ [CRITICAL] → Deve corrigir antes do merge
├─ [ERROR]    → Deveria corrigir antes do merge
├─ [WARNING]  → Recomendado corrigir
└─ [INFO]     → Seria bom ter
```

### Passo 3: Rodar Análise Profunda Claude

**Áreas de Foco:**

| Categoria | Verificar |
|-----------|-----------|
| **Arquitetura** | Alinhamento com padrões do projeto, separação de responsabilidades |
| **Lógica de Negócio** | Implementação correta, edge cases, tratamento de erros |
| **Design Patterns** | Convenções do projeto, padrões estabelecidos, consistência |
| **Manutenibilidade** | Código autodocumentado, type hints, princípio DRY |

### Passo 4: Sintetizar Descobertas

Combine resultados dos dois revisores:

1. **Desduplicar** — Mesmo problema encontrado pelos dois → manter um, anotar "Ambos"
2. **Priorizar** — Crítico > Erro > Aviso > Info
3. **Categorizar** — Segurança, Qualidade, Performance, Estilo
4. **Ação** — Deve corrigir vs Deveria corrigir vs Seria bom ter

### Passo 5: Gerar Relatório

---

## Formato do Output

```markdown
## 🔍 Relatório de Dual AI Review

**Revisores:** Análise Estática + Claude Code
**Escopo:** {descrição do escopo}
**Arquivos:** {count} arquivos, {linhas} linhas alteradas
**Data:** {timestamp}

---

### 📊 Resumo

| Fonte | 🔴 Crítico | 🟠 Erro | 🟡 Aviso | 🔵 Info |
|-------|-----------|---------|----------|---------|
| Análise Estática | {n} | {n} | {n} | {n} |
| Claude | {n} | {n} | {n} | {n} |
| **Total** | {n} | {n} | {n} | {n} |

---

### 🔴 Problemas Críticos

> Deve corrigir antes do merge

#### [C1] {Título}
- **Fonte:** {Análise Estática|Claude|Ambos}
- **Arquivo:** `{caminho}:{linha}`
- **Problema:** {descrição}
- **Correção:**
```{lang}
{código}
```

---

### 🟠 Erros

> Deveria corrigir antes do merge

#### [E1] {Título}
- **Fonte:** {fonte}
- **Arquivo:** `{caminho}:{linha}`
- **Problema:** {descrição}

---

### 🟡 Avisos

> Recomendado corrigir

- [{fonte}] `{arquivo}`: {descrição}

---

### 🔵 Sugestões

- {sugestão 1}
- {sugestão 2}

---

### ✅ Observações Positivas

- {boa prática 1}
- {boa prática 2}

---

### 📋 Checklist de Ações

- [ ] Corrigir: {crítico 1}
- [ ] Corrigir: {crítico 2}
- [ ] Considerar: {aviso 1}

---

**Status de Merge:** {✅ Pronto | ⚠️ Corrigir avisos primeiro | 🚫 Corrigir problemas críticos}
```

---

## Tratamento de Erros

### Ferramenta de Análise Estática Não Disponível

```text
Se ferramenta não encontrada:
  1. Prosseguir com review somente Claude
  2. Notar no relatório: "Análise estática indisponível"
```

### Changeset Grande

```text
Se > 50 arquivos alterados:
  1. Sugerir: "Changeset grande detectado. Use 'review uncommitted' para feedback mais rápido"
  2. Prosseguir com review mas notar potencial de timeout
```

---

## Modo Rápido (`--quick`)

Análise estática somente — para feedback rápido:

```
review --quick
```

**Processo:**
1. Rodar análise estática
2. Parsear e formatar resultados
3. Pular análise Claude
4. Retornar imediatamente

**Use Quando:**
- Verificação rápida de sanidade
- Validação pré-commit
- Integração com CI/CD

---

## Modo Profundo (`--deep`)

Somente Claude — para análise detalhada:

```
review --deep
```

**Processo:**
1. Pular análise estática
2. Análise completa Claude com todas as capacidades
3. Review arquitetural detalhado
4. Recomendações estendidas

**Use Quando:**
- Análise estática indisponível
- Precisa de análise contextual mais profunda
- Revisando decisões de design

---

## Integração

### Antes de Criar PR

```
# Review primeiro, depois criar PR
review
# Se tudo ok:
create-pr
```

### Com create-pr

```
# Roda review automaticamente antes do PR
create-pr --review
```

### No Loop de Desenvolvimento

```
# Feedback rápido em trabalho em progresso
review uncommitted

# Review completo antes do commit
review committed
```

---

## Dicas

1. **Revise Cedo** — Rode `review uncommitted` frequentemente durante o desenvolvimento
2. **Corrija Críticos Primeiro** — Sempre resolva problemas críticos e erros antes do PR
3. **Aprenda com o Feedback** — Ambos os AIs fornecem explicações educativas
4. **Use Modo Rápido** — Para iteração rápida, `review --quick` é seu amigo
5. **Hábito Pré-PR** — Sempre faça `review` antes de `create-pr`

---

## Referências

- Agente: `agents/code-reviewer.md`
- Criar PR: `commands/create-pr.md`
