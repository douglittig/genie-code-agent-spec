# Revisão de Coerência — sdd-workflow

Revisão realizada em 2026-04-27 para verificar coerência de todos os arquivos da skill
`sdd-workflow` com o projeto `genie-code-agent-spec` e com o paradigma do Genie Code.

---

## Arquivos Coerentes

Nenhuma alteração necessária.

| Arquivo | Motivo |
|---------|--------|
| `agents/ship-agent.md` | Lógica de archival autocontida, sem dependências externas |
| `agents/iterate-agent.md` | Gerenciamento de cascata autocontido |
| `templates/BRAINSTORM_TEMPLATE.md` | Conteúdo puro de template, sem dependências |
| `templates/DEFINE_TEMPLATE.md` | Conteúdo puro de template, sem dependências |
| `templates/DESIGN_TEMPLATE.md` | Conteúdo puro de template, sem dependências |
| `templates/BUILD_REPORT_TEMPLATE.md` | Conteúdo puro de template, sem dependências |
| `templates/SHIPPED_TEMPLATE.md` | Conteúdo puro de template, sem dependências |
| `architecture/ARCHITECTURE.md` | Documentação visual; referências a `/command` são ilustrativas |

---

## Arquivos Marcados para Discussão

Marcados com `needs_discussion: true` no frontmatter (ou comentário para YAML). A razão
detalhada está em `discussion_reason:` dentro de cada arquivo.

### Agentes

| Arquivo | Problema | Decisão necessária |
|---------|----------|--------------------|
| `agents/brainstorm-agent.md` | `kb_domains: []` vazio mas corpo diz "KB-FIRST OBRIGATÓRIO"; referencia `kb/_index.yaml` inexistente | Remover arquitetura KB-first ou definir kb_domains concretos |
| `agents/define-agent.md` | Mesma contradição: kb_domains vazio vs KB-first obrigatório | Remover arquitetura KB-first ou definir kb_domains concretos |
| `agents/design-agent.md` | Tabela de delegação referencia agentes inexistentes: `lakeflow-pipeline-builder`, `spark-engineer`, `spark-streaming-architect`, `sql-optimizer`, `medallion-architect`, `data-quality-analyst` | Remover tabela ou mapear para skills Databricks existentes no projeto |
| `agents/build-agent.md` | Delegação DE para `dbt-specialist`, `spark-engineer`, `pipeline-architect`, `data-contracts-engineer`, `data-quality-analyst`, `schema-designer` — nenhum existe como skill; ferramenta `Task` não verificada para Genie Code | Remover mapa de delegação DE ou criar essas skills |
| `agents/code-reviewer.md` | `kb_domains: [data-quality, sql-patterns, dbt]` — nenhum desses KB domains existe no projeto | Remover kb_domains e simplificar para padrões gerais, ou criar estrutura KB |
| `agents/test-generator.md` | `kb_domains: [data-quality, dbt, testing]` — mesma ausência | Remover kb_domains e simplificar, ou criar estrutura KB |

### Commands

| Arquivo | Problema | Decisão necessária |
|---------|----------|--------------------|
| `commands/brainstorm.md` | Frontmatter `name: brainstorm` implica slash command `/brainstorm` — paradigma do Claude Code CLI; Genie Code não tem slash commands | Renomear diretório para `guides/` (documentação pura) ou adaptar ao paradigma `@skill-name` |
| `commands/define.md` | Idem | Idem |
| `commands/design.md` | Idem | Idem |
| `commands/build.md` | Idem | Idem |
| `commands/ship.md` | Idem | Idem |
| `commands/iterate.md` | Idem | Idem |
| `commands/create-pr.md` | Idem + sem agente correspondente em `agents/` | Consolidar em `agents/ship-agent.md` ou manter separado |
| `commands/review.md` | Idem + duplica funcionalidade de `agents/code-reviewer.md` | Consolidar em `agents/code-reviewer.md` ou manter separado |

### Outros

| Arquivo | Problema | Decisão necessária |
|---------|----------|--------------------|
| `SKILL.md` | Tabela "File Manifest" lista `@lakeflow-pipeline-builder`, `@spark-streaming-architect`, `@sql-optimizer`, `@medallion-architect`, `@data-quality-analyst`, `@python-developer` — não existem como skills | Remover agentes inexistentes ou mapeá-los para skills Databricks do projeto |
| `architecture/WORKFLOW_CONTRACTS.yaml` | Referências a `/command` no lugar de `@agent-name`; tool lists divergem dos frontmatters dos agentes; seção `data_engineering_delegation` referencia agentes inexistentes | Atualizar referências de comando e sincronizar tool lists |

---

## Temas para Discussão

Três decisões de design que resolvem a maioria dos problemas:

### 1. Arquitetura KB-first

**Situação:** Agentes (brainstorm, define, design, build) têm arquitetura "KB-FIRST OBRIGATÓRIO" mas o projeto não tem diretório `kb/`. Os `kb_domains` estão vazios na maioria dos agentes.

**Opções:**
- (a) Remover a arquitetura KB-first dos agentes — simplificar para detecção de padrões no codebase existente do usuário
- (b) Criar estrutura `kb/` no projeto com domínios relevantes para Databricks (dbt, spark, sql-patterns, data-quality)
- (c) Tornar o KB-first opcional/condicional — só aplicar se `kb_domains` estiver preenchido

### 2. Agentes especializados inexistentes

**Situação:** `SKILL.md`, `design-agent` e `build-agent` referenciam agentes (`@dbt-specialist`, `@spark-engineer`, `@lakeflow-pipeline-builder`, etc.) que não existem como skills no projeto. O projeto tem skills Databricks que cobrem essas especialidades.

**Opções:**
- (a) Remover o mapa de delegação especializada — build-agent constrói tudo diretamente
- (b) Mapear para skills Databricks existentes: `@databricks-spark-declarative-pipelines` em vez de `@lakeflow-pipeline-builder`, `@databricks-python-sdk` em vez de `@python-developer`, etc.
- (c) Criar as skills especializadas faltantes como novos arquivos em `agents/`

### 3. Diretório `commands/`

**Situação:** Os 8 arquivos em `commands/` têm frontmatter com `name:` sugerindo slash commands (`/brainstorm`, `/define`, etc.). Genie Code não tem slash commands — usa `@skill-name`. Claude Code CLI suporta slash commands mas o projeto foca em Genie Code.

**Opções:**
- (a) Renomear para `guides/` e remover o frontmatter `name:` — manter como documentação de referência
- (b) Manter como está — esses arquivos funcionam no Claude Code CLI mesmo que não no Genie Code
- (c) Converter para o formato correto do Genie Code (documentar como `@sdd-workflow` + fase)
