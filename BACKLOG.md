# BACKLOG

Itens identificados durante o desenvolvimento deste repositório que foram deixados para depois.
Usar como base para próximas sessões de trabalho.

---

## Em Aberto

### 1. PR Template Corporativo
**Contexto:** O arquivo `custom-dev-workflow/pr-template.md` é um placeholder genérico.
**O que falta:** Definir campos obrigatórios conforme regras da empresa (ex: campo de ticket, aprovadores, checklist de segurança específico).
**Origem:** Sessão de criação da skill `custom-dev-workflow`.

---

### 2. PR Review Rules Corporativas
**Contexto:** O Passo 7 do `custom-dev-workflow` tem um placeholder "a ser lapidado com regras da empresa".
**O que falta:** Definir quem revisa, SLA de review, gates obrigatórios (aprovações mínimas, checks de CI), e se há ferramentas específicas (ex: SonarQube, Checkov).
**Origem:** Sessão de criação da skill `custom-dev-workflow`.

---

### 3. Equivalente ao `/commit` do Claude Code para o Genie Code
**Contexto:** O Claude Code tem uma skill `/commit` que orienta criação de commits com conventional commits e co-authorship. O Genie Code não tem equivalente nativo.
**O que falta:** Criar um comando ou instrução dentro da skill `custom-dev-workflow` (ou skill dedicada) que guie o Genie Code no processo de staging + commit com mensagem estruturada.
**Origem:** Sessão de criação da skill `custom-dev-workflow`.

---

### 4. Branch Protection Rules no Repositório Centralizado
**Contexto:** A regra de "nunca commitar na main" está documentada em AGENTS.md/CLAUDE.md e na skill `custom-dev-workflow`, mas é apenas instrução — sem enforcement técnico.
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
**Origem:** Pesquisa de viabilidade MCP para custom-dev-workflow — 2026-04-28.

---

### 7. Guardrails Determinísticos, Evals e Model Routing (fechar o harness)
**Contexto:** A seção "Harness & Guardrails" do `CLAUDE.md`/`AGENTS.md` mapeia os 6 componentes do harness (paper *The New SDLC with Vibe Coding*, Google, Day 1). Três lacunas ficaram explícitas:

1. **Guardrails são prompt-level, não determinísticos.** Os gates (sem credencial hardcoded, preview antes de escrever no Jira, nunca commitar na `main`) são checklists nos agentes — o agente pode esquecer. O paper posiciona hooks como "o lugar das coisas que o agente nunca deveria esquecer mas sempre esquece".
2. **Faltam evals.** O Build valida só o determinístico (lint/testes). Falta avaliação por rubrica/LM-judge do **output** e da **trajetória** (o agente seguiu os passos certos?). Máxima do paper: *"set the bar at the eval, not the demo"*.
3. **Sem model routing.** O paper recomenda modelo frontier para Requisitos/Arquitetura/Implementação e modelos menores e baratos para tarefas determinísticas (geração de testes, code review, monitoramento) — alavanca direta de OpEx.

**O que falta:**
- Hooks determinísticos: pre-commit (segredos + bloqueio de push na `main`) e, no Claude Code, `PreToolUse` em `settings.json`. Complementa o item 4 (branch protection no provider).
- Eval-gate por rubrica no Build — possivelmente evolução do `custom-test-generator` ou uma skill `custom-evals`. O ledger `.claude/sdd/state/` já registra a trajetória e pode servir de insumo.
- Anotar tier de modelo sugerido por fase/agente.

**Referência:** `assets/documentation/Day_1_v3.pdf` (pp. 26–30 harness, 14–15 evals, 42 model routing).
**Origem:** Leitura do paper Day 1 durante a evolução do `custom-sdd-workflow`.

---

## Concluídos

| Item | Sessão |
|------|--------|
| Skill `custom-dev-workflow` criada | 2026-04-28 |
| `AGENTS.md` criado como espelho do `CLAUDE.md` | 2026-04-28 |
| `assets/documentation/` removida do `.gitignore` | 2026-04-28 |
| Guia `docs/bitbucket-mcp-guide.md` criado (Atlassian Rovo MCP + Genie Code) | 2026-04-28 |
