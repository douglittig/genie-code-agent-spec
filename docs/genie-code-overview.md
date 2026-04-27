# Databricks Genie Code — Visão Geral

> Fontes: [Documentação oficial](https://docs.databricks.com/aws/en/genie-code/), [DE Agent](https://docs.databricks.com/aws/en/ldp/de-agent), [Blog de lançamento](https://www.databricks.com/blog/introducing-genie-code)

---

## O que é o Genie Code?

Genie Code é um **agente de IA autônomo construído especificamente para equipes de dados dentro da plataforma Databricks**. Diferente de assistentes de código genéricos, o Genie Code entende que *"código é apenas um veículo para manipular e compreender os dados subjacentes"* — ou seja, o foco não é gerar código bonito, mas executar trabalho real sobre dados reais.

Ele opera ao longo de todo o ciclo de vida do trabalho com dados: desde a criação de pipelines até a manutenção em produção, passando por análise exploratória, machine learning e observabilidade.

---

## Visão e Posicionamento

Databricks posiciona o Genie Code como a mesma revolução que os agentes de código trouxeram para engenharia de software — agora aplicada a equipes de dados. A proposta é ser um **parceiro de IA proativo em produção**: monitora sistemas, faz triagem de falhas e otimiza fluxos de forma autônoma.

**Benchmark interno:** 77,1% de taxa de conclusão de tarefas do mundo real vs. 32,1% de um "leading coding agent equipado com MCP do Databricks" — segundo os próprios dados da Databricks.

---

## Capacidades Principais

### 1. Data Science & Machine Learning
- Automação de workflows end-to-end em notebooks
- Identificação de features, divisão de datasets, tuning de hiperparâmetros
- Tracking de experimentos via MLflow
- Otimização de endpoints de serving

### 2. Engenharia de Dados (Lakeflow Pipelines)
- Criação de pipelines Spark Declarativos a partir de linguagem natural
- Construção de arquitetura medallion (Bronze → Silver → Gold) de ponta a ponta
- Edição de múltiplos arquivos simultaneamente com revisão de diff
- Configuração de AutoCDC flows e data quality expectations
- Diagnóstico e correção iterativa de falhas em pipelines

### 3. Dashboards e Análise
- Geração de visualizações com definições semânticas reutilizáveis
- Filtros e layouts multi-página
- Análise de dados com linguagem natural (Natural Language Data Filtering)

### 4. Observabilidade em Produção
- Integração com Databricks Model Serving e MLflow 3.0
- Health checks automáticos de endpoints
- Análise de qualidade de agentes GenAI
- Triagem de incidentes e recomendações de otimização

### 5. Background Agents (em breve)
- Agentes autônomos para tarefas rotineiras (responder a falhas de jobs, gerenciar upgrades) sem intervenção humana

---

## Como Funciona — Modo Padrão vs. Modo Agente

| Aspecto | Modo Padrão | Modo Agente (Agent Mode) |
|---|---|---|
| Interação | Chat com sugestões inline | Planejamento autônomo multi-etapas |
| Execução | Sugestão ao usuário | Executa após aprovação do usuário |
| Escopo | Arquivo/célula atual | Múltiplos arquivos e recursos |
| Uso típico | Autocomplete, correção de erros, slash commands | Construção de pipelines completos, diagnóstico de falhas |

**Fluxo do Modo Agente:**
1. Usuário ativa Agent Mode e submete um prompt
2. Genie Code cria um **plano passo a passo** para a tarefa
3. Solicita aprovação antes de executar código ou atualizar pipelines
4. Pausa para perguntas de esclarecimento quando necessário
5. Permite revisão das mudanças antes de prosseguir

---

## Arquitetura Técnica

### Sistema Multi-Modelo
Genie Code **não depende de um único LLM**. Ele roteia tarefas entre múltiplos modelos automaticamente:
- Frontier LLMs (modelos de fronteira)
- Modelos open-source
- Modelos customizados hospedados no Databricks

A seleção do modelo é feita automaticamente de acordo com o tipo de tarefa.

### Integração com Unity Catalog
O agente é **construído diretamente sobre o Unity Catalog**, o que significa:
- Entende tabelas, colunas, descrições e linhagem de dados da organização
- Respeita políticas de segurança e controles de acesso existentes
- Só expõe assets de dados que o usuário tem permissão para acessar
- Respostas personalizadas baseadas na governança de dados da organização

### Superfícies de Integração
Genie Code adapta suas funcionalidades conforme o contexto:
- **Notebooks** → Data science, ML, análise exploratória
- **SQL Editor** → Queries, análise ad-hoc
- **Lakeflow Pipelines Editor** → ETL, pipelines declarativos
- **Catalog Explorer** → Exploração de dados de exemplo
- **Dashboards** → Geração de visualizações

---

## Extensibilidade

Três formas de customizar e estender o Genie Code:

| Mecanismo | Para quê |
|---|---|
| **Model Context Protocol (MCP)** | Conectar ferramentas externas (Jira, Confluence, etc.) |
| **Agent Skills** | Adicionar capacidades específicas do domínio do negócio |
| **Persistent Memory** | O agente aprende com interações e preferências da equipe ao longo do tempo |

---

## Governança e Auditoria

- Todas as edições são rastreadas pelo sistema de versionamento do Databricks
- Audit logging completo de todas as ações do Genie Code
- Guardrails embutidos para prevenir ações destrutivas
- **Importante:** O Agent Mode pode gerar e executar código. Embora existam guardrails, há risco inerente — usuário deve revisar antes de confirmar execuções.

---

## Disponibilidade e Custo

- **Custo:** Todas as capacidades atuais são gratuitas para todos os clientes. O usuário paga apenas pelos recursos de computação utilizados. Fair usage limits se aplicam.
- **Acesso:** Disponível diretamente nos workspaces Databricks, sem configuração complexa.
- **Pré-requisitos para Agent Mode:**
  - Partner-powered AI features habilitadas a nível de conta e workspace
  - Workspace em região geográfica suportada
  - Permissões do usuário respeitam controles do Unity Catalog
- **Residência de dados:** Genie Code opera como Designated Service com zonas geográficas de processamento; disponibilidade varia por região.

---

## Referências

- [Genie Code Docs](https://docs.databricks.com/aws/en/genie-code/)
- [Data Engineering Agent (DE Agent)](https://docs.databricks.com/aws/en/ldp/de-agent)
- [Blog: Introducing Genie Code](https://www.databricks.com/blog/introducing-genie-code)
