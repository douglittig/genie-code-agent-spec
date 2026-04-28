---
name: dev-workflow
description: |
  Fluxo de desenvolvimento seguro: discussão → branch → código → validação → review → PR → merge.
  Use de forma PROATIVA sempre que o usuário quiser modificar código, criar uma feature,
  corrigir um bug ou qualquer mudança que precise entrar no repositório.

  Exemplo 1 — Usuário quer criar algo novo sem discutir antes:
  user: "Vamos criar o arquivo X direto"
  assistant: "Antes de qualquer mudança, vamos alinhar a abordagem. [inicia discussão]"

  Exemplo 2 — Usuário acabou de alinhar a abordagem:
  user: "Ok, vamos implementar dessa forma"
  assistant: "Vou criar a feature branch e seguir o dev-workflow."
---

# Dev Workflow

> Fluxo de desenvolvimento seguro para repositórios com branch protection em `main`.

## Regra de Ouro

**Nunca modificar código sem discussão prévia. Nunca commitar diretamente na `main`.**

---

## Fluxo Completo

```
Discussão → Branch → Desenvolvimento → Validação Local → Auto-review → Revisão Humana → PR → PR Review → Merge
```

---

## Passo 0 — Discutir Antes de Codar

**Regra absoluta:** antes de qualquer mudança no código, alinhar a abordagem com o usuário.

| Situação | Rota |
|----------|------|
| Ideia vaga ou requisito impreciso | Usar `@sdd-workflow` fase Brainstorm |
| Múltiplas abordagens possíveis | Apresentar opções com trade-offs, aguardar decisão |
| Mudança simples e clara | Descrever o que será feito e aguardar aprovação inline |

**Gate:** usuário aprovou a abordagem → avançar para Passo 1.

---

## Passo 1 — Criar Feature Branch

```bash
# 1. Sempre sincronizar com main antes de criar a branch
git checkout main
git pull origin main

# 2. Criar branch com naming convention
git checkout -b <type>/<short-description>
```

### Naming Convention

| Tipo | Quando usar | Exemplo |
|------|-------------|---------|
| `feat/` | Nova funcionalidade | `feat/autenticacao-oauth` |
| `fix/` | Correção de bug | `fix/null-pointer-parser` |
| `refactor/` | Reestruturação sem mudança de comportamento | `refactor/padronizacao-agentes` |
| `docs/` | Apenas documentação | `docs/guia-instalacao` |
| `chore/` | Manutenção, dependências, CI | `chore/atualizar-deps` |
| `test/` | Adição ou correção de testes | `test/cobertura-pipeline` |

**Nunca** criar branches a partir de outra branch de feature sem justificativa explícita.

---

## Passo 2 — Desenvolvimento

### Commits Atômicos

- Um commit = uma preocupação lógica
- Meta: < 400 linhas por PR

### Conventional Commits

```
<type>(<scope>): <descrição curta em imperativo>

<body opcional: o que e por que, não como>

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Tipos:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `style`, `perf`, `ci`

```bash
# Exemplos
git commit -m "feat(auth): adicionar refresh token OAuth2"
git commit -m "fix(parser): tratar campo de data nulo"
git commit -m "docs(readme): adicionar instruções de setup local"
```

### Sincronização com Main

Durante desenvolvimento longo, sincronizar periodicamente:

```bash
git fetch origin
git rebase origin/main
```

---

## Passo 3 — Validação Local

Antes de fazer push, executar:

```bash
# Linting e formatação (Python)
ruff check .
ruff format --check .

# Type checking
pyright  # ou mypy

# Testes
pytest
```

**Gate:** sem erros críticos de linting, tipo ou teste antes do push.

> Se o projeto não tiver esses checks configurados, registrar como item de backlog.

---

## Passo 4 — Auto-review com `@code-reviewer`

Antes de solicitar revisão humana, rodar o `@code-reviewer` nas mudanças:

```
@code-reviewer revise as mudanças na branch atual
```

| Resultado | Ação |
|-----------|------|
| CRÍTICO encontrado | Corrigir antes de continuar |
| ERRO encontrado | Corrigir antes de continuar |
| AVISO | Documentar na descrição do PR, avançar |
| Limpo | Avançar para revisão humana |

---

## Passo 5 — Aguardar Revisão do Desenvolvedor

```bash
# Push da branch com tracking
git push -u origin <nome-da-branch>
```

- Solicitar review ao time/par designado
- Endereçar comentários com **novos commits** (nunca `--force-push` em branch compartilhada)
- Marcar conversas resolvidas após endereçar

---

## Passo 6 — Criar PR

Usar o template em [`pr-template.md`](pr-template.md) desta skill.

Para o processo detalhado de criação de PR (conventional commits, categorização de mudanças, uso do `gh` CLI), referenciar `@sdd-workflow` comando `create-pr`.

**Checklist antes de criar o PR:**

```text
[ ] Branch está atualizada com main (git rebase origin/main)
[ ] Validação local passou (linting, testes)
[ ] Auto-review com @code-reviewer concluído
[ ] Nenhum segredo ou credencial no código
[ ] Título segue conventional commits
[ ] Descrição tem Resumo, Test Plan e Breaking Changes
[ ] Issue relacionada linkada (se houver)
```

---

## Passo 7 — PR Review

> **Placeholder corporativo** — processo a ser lapidado com regras específicas da empresa.

Por padrão, aplicar:

- Revisão por pelo menos 1 desenvolvedor do time
- Dual AI review: análise estática + `@code-reviewer` arquitetural (via `@sdd-workflow` comando `review`)

### Bloqueadores que impedem merge

| Bloqueador | Motivo |
|------------|--------|
| Acceptance test falhando | Quebra contrato funcional |
| Credencial ou segredo exposto | Risco de segurança crítico |
| Breaking change sem deprecation period | Quebra contratos de API |
| Mudança direta em `main` sem PR | Viola regra de ouro |

---

## Referências desta Skill

| Arquivo | Conteúdo |
|---------|---------|
| [`pr-template.md`](pr-template.md) | Template base de PR (placeholder corporativo) |
| `@sdd-workflow` → `commands/brainstorm.md` | Fase de Brainstorm (Passo 0) |
| `@sdd-workflow` → `commands/create-pr.md` | Criação detalhada de PR (Passo 6) |
| `@sdd-workflow` → `commands/review.md` | Dual AI review (Passo 7) |
| `@code-reviewer` | Auto-review antes de PR (Passo 4) |

## Integração MCP (opcional)

Com o **Atlassian Rovo MCP** configurado, o Genie Code consegue criar PRs, ler diffs e gerenciar comentários diretamente via chat, sem precisar da UI do Git Folders.

> **Pré-requisito crítico: Bitbucket Cloud apenas.** Data Center não é suportado.

Guia completo de configuração: `docs/bitbucket-mcp-guide.md`
