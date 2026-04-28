# Revisão de Coerência — sdd-workflow

Revisão realizada em 2026-04-27. Decisões tomadas e implementadas em 2026-04-27.
Todos os `needs_discussion` foram resolvidos — este documento é histórico.

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

## Decisões Tomadas

### 1. Arquitetura KB-first → Skills-first ✅

**Decisão:** Substituir KB-first por Skills-first usando as skills Databricks curadas pelo time.

**Implementado:**
- Todos os 6 agentes (brainstorm, define, design, build, code-reviewer, test-generator): bloco "KB-FIRST OBRIGATÓRIO" substituído por "SKILLS-FIRST"
- `kb_domains` removido do frontmatter de todos os agentes
- Referências a `kb/_index.yaml` e `kb/{domain}/` removidas
- Princípio Central atualizado para "Skills first" em todos os agentes

### 2. Agentes especializados → Skills Databricks existentes ✅

**Decisão:** Mapear para as skills Databricks existentes no projeto.

**Mapeamento aplicado:**

| Agente agentspec (removido) | Skill Databricks (mapeado) |
|----------------------------|---------------------------|
| `@lakeflow-pipeline-builder` | `@databricks-spark-declarative-pipelines` |
| `@spark-engineer` | `@databricks-spark-declarative-pipelines` |
| `@spark-streaming-architect` | `@databricks-spark-structured-streaming` |
| `@sql-optimizer` | `@databricks-dbsql` |
| `@medallion-architect` | `@databricks-spark-declarative-pipelines` |
| `@data-quality-analyst` | `@databricks-spark-declarative-pipelines` + `@databricks-mlflow-evaluation` |
| `@python-developer` | `@python-dev` |
| `@pipeline-architect` | `@databricks-bundles` + `@databricks-jobs` |
| `@schema-designer` / `@data-contracts-engineer` | `@databricks-unity-catalog` |

**Implementado:**
- `SKILL.md`: tabela do File Manifest atualizada com skills Databricks
- `design-agent.md`: tabela de delegação e referências de capacidades atualizadas
- `build-agent.md`: mapa DE atualizado para skills Databricks; ferramenta `Task` removida

**Nota:** Os agentes especializados originais existem em `assets/repos/agentspec-main/plugin/agents/data-engineering/` para referência.

### 3. `commands/` → guias sem frontmatter (Genie Code first) ✅

**Decisão:** Converter os 8 arquivos para guias de referência sem frontmatter de slash command.

**Implementado:**
- Frontmatter YAML (`name:`, `description:`, `needs_discussion:`, `discussion_reason:`) removido de todos os 8 arquivos em `commands/`
- Arquivos mantidos como guias de referência para o SKILL.md (que já gerencia o roteamento)
- Paradigma Genie Code: invocar via `@sdd-workflow` em Agent mode — o SKILL.md roteia para o agente correto
