---
name: create-pr
description: Crie pull requests com conventional commits e descrições estruturadas
needs_discussion: true
discussion_reason: |
  Frontmatter 'name:' implica slash command (/create-pr), paradigma do Claude Code CLI.
  Genie Code não tem slash commands — invocação é via @skill-name em Agent mode.
  Adicionalmente: este arquivo é um command isolado sem agente correspondente em agents/.
  Decidir: manter como documentação de referência ou unificar com ship-agent.
---

# Create PR

> Criação profissional de pull requests com conventional commits e descrições estruturadas

## Uso

```
create-pr                           # Detectar mudanças automaticamente e criar PR
create-pr "feat: adicionar auth"    # Criar PR com título customizado
create-pr --draft                   # Criar como draft PR
create-pr --review                  # Rodar dual AI review antes de criar o PR
create-pr --review --draft          # Review + criar como draft
```

---

## Opção de Review Pré-PR

Quando usar `--review`, o comando roda um **dual AI review** antes de criar o PR:

```text
┌─────────────────────────────────────────────────────────────────┐
│              WORKFLOW create-pr --review                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. Analisar Mudanças                                           │
│          ↓                                                       │
│   2. Rodar Análise Estática (CodeRabbit)                        │
│          ↓                                                       │
│   3. Rodar Review Claude (Arquitetural)                         │
│          ↓                                                       │
│   4. Verificar Problemas Críticos                               │
│          ↓                                                       │
│   ┌──────┴──────┐                                               │
│   │             │                                                │
│   ▼             ▼                                                │
│ Problemas    Sem Problemas                                       │
│ Críticos     Críticos                                            │
│   │             │                                                │
│   ▼             ▼                                                │
│ PARAR &      Continuar                                           │
│ Mostrar      para Criação                                        │
│ Problemas    do PR                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Comportamento do Review

| Resultado do Review | Ação |
|--------------------|------|
| 🔴 Problemas críticos encontrados | Parar e mostrar problemas, não criar PR |
| 🟠 Erros encontrados | Avisar usuário, perguntar se continua ou corrige |
| 🟡 Apenas avisos | Continuar para o PR, incluir avisos na descrição |
| ✅ Limpo | Continuar para o PR |

---

## Visão Geral

Este processo simplifica a criação de PRs:

1. **Analisar** — Todas as mudanças staged/unstaged
2. **Categorizar** — Mudanças por tipo (feat/fix/refactor/docs)
3. **Gerar** — Mensagens de conventional commits
4. **Construir** — Descrições estruturadas de PR com test plans
5. **Criar** — O PR via GitHub CLI

---

## Processo

### Passo 1: Analisar Mudanças

```bash
# Rodar estes comandos para entender o escopo da mudança
git status
git diff --stat
git log origin/main..HEAD --oneline
```

Categorize arquivos em tipos de mudança:

```text
CATEGORIAS DE MUDANÇA
═════════════════════

feat:     Novas features, capacidades
fix:      Correções de bugs
refactor: Reestruturação de código, sem mudança de comportamento
docs:     Somente documentação
test:     Adições ou correções de testes
chore:    Build, CI/CD, dependências
style:    Formatação, espaços em branco
perf:     Melhorias de performance
```

### Passo 2: Determinar Tipo do PR

Com base na análise de arquivos, identifique o tipo principal de mudança:

| Arquivos Alterados | Tipo Provável |
|--------------------|---------------|
| `src/**/*.py` + nova funcionalidade | `feat:` |
| `src/**/*.py` + correção de bug | `fix:` |
| `src/**/*.py` + reestruturação | `refactor:` |
| `*.md`, `docs/**` | `docs:` |
| `tests/**`, `*_test.py` | `test:` |
| `.github/**`, `Makefile`, `pyproject.toml` | `chore:` |
| `.claude/skills/**` | `refactor(skills):` |
| `.claude/sdd/**` | `docs(sdd):` |

### Passo 3: Gerar Mensagem de Commit

Use o formato de Conventional Commits:

```text
<type>(<scope>): <descrição curta>

<body - o que mudou e por quê>

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Exemplos:**

```text
feat(auth): adicionar fluxo de refresh OAuth2

- Implementar refresh de token OAuth2 com PKCE
- Adicionar compatibilidade retroativa com auth baseada em sessão
- Atualizar regras de validação para novo formato de token

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Passo 4: Fazer Perguntas de Esclarecimento

**Pergunta 1: Tipo do PR**
- Esta categorização está correta?
- Opções: feat, fix, refactor, docs, test, chore

**Pergunta 2: Escopo**
- Qual componente/área isso afeta?
- Opções: baseado nos caminhos de arquivo detectados

**Pergunta 3: Breaking Changes**
- Há algum breaking change?
- Opções: Sim (descreva), Não

**Pergunta 4: Issues Relacionadas**
- Link para alguma issue relacionada?
- (Texto livre — ex., "Closes #123")

### Passo 5: Construir Descrição do PR

Gere a descrição estruturada:

```markdown
## Resumo

{2-3 bullet points descrevendo a mudança}

### Principais Mudanças
- {Mudança principal 1}
- {Mudança principal 2}
- {Mudança principal 3}

## O que Mudou

### {Categoria 1}
{Descrição das mudanças nesta categoria}

### {Categoria 2}
{Descrição das mudanças nesta categoria}

## Arquivos Alterados

| Categoria | Arquivos | Descrição |
|-----------|----------|-----------|
| {cat1} | {count} | {breve descrição} |
| {cat2} | {count} | {breve descrição} |

## Test Plan

- [ ] {Caso de teste 1}
- [ ] {Caso de teste 2}
- [ ] {Caso de teste 3}

## Breaking Changes

{Descreva breaking changes ou "Nenhum"}

## Issues Relacionadas

{Closes #XXX ou "Nenhuma"}

---

Gerado com [Claude Code](https://claude.ai/code)
```

### Passo 6: Criar Branch (se necessário)

```bash
# Se estiver em main, criar branch de feature
git checkout -b <type>/<short-description>

# Exemplos:
git checkout -b feat/autenticacao-usuario
git checkout -b fix/tratamento-null-parser
git checkout -b refactor/padronizacao-agentes
```

### Passo 7: Commit e Push

```bash
# Stage das mudanças
git add <arquivos-especificos>

# Commit com mensagem conventional
git commit -m "<mensagem>"

# Push com tracking upstream
git push -u origin <nome-da-branch>
```

### Passo 8: Criar PR

```bash
gh pr create \
  --title "<type>(<scope>): <descrição>" \
  --body "<body-gerado>" \
  --base main
```

Para draft PRs:
```bash
gh pr create --draft ...
```

---

## Output

- **Branch:** `<type>/<short-description>`
- **Commit:** Formato conventional commit
- **URL do PR:** Retornado pelo `gh pr create`

---

## Checklist de Qualidade

Antes de criar o PR, verifique:

```text
MENSAGEM DE COMMIT
[ ] Usa formato de conventional commits
[ ] Tipo corresponde à mudança principal
[ ] Scope é específico e significativo
[ ] Descrição é concisa (< 72 chars)

DESCRIÇÃO DO PR
[ ] Resumo explica o POR QUÊ e não apenas o O QUÊ
[ ] Tabela de arquivos alterados é precisa
[ ] Test plan tem itens acionáveis
[ ] Breaking changes documentados (se houver)

BRANCH
[ ] Nome da branch segue a convenção
[ ] Não está fazendo commit diretamente na main
[ ] Todas as mudanças estão staged
```

---

## Referência de Conventional Commits

| Tipo | Quando Usar | Exemplo |
|------|-------------|---------|
| `feat` | Nova feature | `feat(api): adicionar endpoint de usuário` |
| `fix` | Correção de bug | `fix(parser): tratar datas nulas` |
| `refactor` | Reestruturação de código | `refactor(auth): extrair serviço de token` |
| `docs` | Documentação | `docs(readme): adicionar instruções de setup` |
| `test` | Testes | `test(parser): adicionar cobertura de edge cases` |
| `chore` | Manutenção | `chore(deps): atualizar dependências` |
| `style` | Formatação | `style: aplicar formatação black` |
| `perf` | Performance | `perf(query): adicionar index para lookups` |
| `ci` | CI/CD | `ci: adicionar workflow github actions` |
| `build` | Build system | `build: atualizar dockerfile` |

---

## Dicas

1. **Mantenha PRs Pequenos** — Mire em < 400 linhas alteradas
2. **Uma Preocupação por PR** — Não misture features com refactors
3. **Escreva para os Revisores** — Assuma que eles não conhecem o contexto
4. **Linke Issues** — Use "Closes #XX" para fechar issues automaticamente
5. **Test Plan Importa** — Os revisores precisam saber como verificar

---

## Referências

- Comando de Review: `commands/review.md`
- Agente Code Reviewer: `agents/code-reviewer.md`
