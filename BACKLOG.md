# BACKLOG

Itens identificados durante o desenvolvimento deste repositório que foram deixados para depois.
Usar como base para próximas sessões de trabalho.

---

## Em Aberto

### 1. PR Template Corporativo
**Contexto:** O arquivo `.claude/skills/dev-workflow/pr-template.md` é um placeholder genérico.
**O que falta:** Definir campos obrigatórios conforme regras da empresa (ex: campo de ticket, aprovadores, checklist de segurança específico).
**Origem:** Sessão de criação da skill `dev-workflow`.

---

### 2. PR Review Rules Corporativas
**Contexto:** O Passo 7 do `dev-workflow` tem um placeholder "a ser lapidado com regras da empresa".
**O que falta:** Definir quem revisa, SLA de review, gates obrigatórios (aprovações mínimas, checks de CI), e se há ferramentas específicas (ex: SonarQube, Checkov).
**Origem:** Sessão de criação da skill `dev-workflow`.

---

### 3. Equivalente ao `/commit` do Claude Code para o Genie Code
**Contexto:** O Claude Code tem uma skill `/commit` que orienta criação de commits com conventional commits e co-authorship. O Genie Code não tem equivalente nativo.
**O que falta:** Criar um comando ou instrução dentro da skill `dev-workflow` (ou skill dedicada) que guie o Genie Code no processo de staging + commit com mensagem estruturada.
**Origem:** Sessão de criação da skill `dev-workflow`.

---

### 4. Branch Protection Rules no Repositório Centralizado
**Contexto:** A regra de "nunca commitar na main" está documentada em AGENTS.md/CLAUDE.md e na skill `dev-workflow`, mas é apenas instrução — sem enforcement técnico.
**O que falta:** Configurar branch protection rules no Git provider (ex: Databricks Repos, GitHub, GitLab) para impedir push direto na `main` a nível de plataforma.
**Origem:** Incidente de commit direto na main durante sessão de criação do AGENTS.md.

---

### 5. Estrutura de AGENTS.md para Asset Bundles Multi-Time
**Contexto:** O plano é ter um repositório centralizado (com `AGENTS.md` raiz) e repositórios por time/projeto (cada um com seu `AGENTS.md`).
**O que falta:** Definir como a hierarquia vai funcionar: quais instruções ficam no repo centralizado vs. no repo do time, como evitar conflito/redundância, e como o Genie Code resolve quando encontra múltiplos `AGENTS.md` ao caminhar na árvore de diretórios do Databricks Workspace.
**Origem:** Discussão sobre estratégia de instruções personalizadas para ambiente corporativo sem Claude Code.

---

### 6. Atlassian MCP — Suporte a Bitbucket Data Center / Server
**Contexto:** O Atlassian Rovo MCP Server suporta apenas Bitbucket **Cloud**. Bitbucket Data Center e Server não têm suporte hoje.
**O que falta:** Se a empresa usar Bitbucket Data Center, acompanhar roadmap da Atlassian ou avaliar alternativa via MCP customizado (Databricks App expondo API do Bitbucket DC).
**Referência:** `docs/bitbucket-mcp-guide.md`
**Origem:** Pesquisa de viabilidade MCP para dev-workflow — 2026-04-28.

---

## Concluídos

| Item | Sessão |
|------|--------|
| Skill `dev-workflow` criada | 2026-04-28 |
| `AGENTS.md` criado como espelho do `CLAUDE.md` | 2026-04-28 |
| `assets/documentation/` removida do `.gitignore` | 2026-04-28 |
| Guia `docs/bitbucket-mcp-guide.md` criado (Atlassian Rovo MCP + Genie Code) | 2026-04-28 |
