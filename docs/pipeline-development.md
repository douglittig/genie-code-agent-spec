# Genie Code — Pipeline Development (Agent Mode)

> **Fonte:** [Use Genie Code for pipeline development](https://docs.databricks.com/aws/en/ldp/de-agent) — Última atualização: Apr 15, 2026  
> **Status:** Public Preview

---

## O que é o Genie Code para Pipeline Development?

Genie Code em Agent mode é um parceiro autônomo que automatiza **workflows completos e multi-etapas de engenharia de dados** em Lakeflow Spark Declarative Pipelines (SDP) e no Lakeflow Pipelines Editor.

Comparado ao modo Chat, o Agent mode tem capacidades expandidas:
- Planejar uma solução
- Recuperar assets relevantes
- Rodar código
- Usar outputs do pipeline para melhorar resultados
- Corrigir erros automaticamente

O agente pode gerar pipelines inteiros do zero ou acelerar o trabalho em um pipeline existente. Em ambos os casos, **trabalha em colaboração**: pede aprovação dos planos e confirma os próximos passos antes de proceder.

> **Nota:** Quando Agent mode é ativado, o Genie Code adapta suas capacidades ao contexto atual. No Lakeflow Pipelines Editor, foca em pipeline editing e data engineering. Em notebooks/SQL Editor, foca em data exploration e análise.

---

## Requisitos

- Partner-powered AI features habilitadas na conta **e** no workspace
- Workspace em região suportada (Genie Code é Designated Service que usa Geos para residência de dados)

---

## Como Usar — Passo a Passo

1. No Lakeflow Pipelines Editor, abrir o painel Genie Code clicando em **Genie Code** no canto superior direito

2. No canto inferior direito, selecionar **Agent** — isso ativa o Agent mode

3. Inserir um prompt. Exemplos:
   - `"describe this pipeline"`
   - `"create silver_sales_data in a new file that reads from bronze_sales_data and cleans the data and adds useful quality expectations"`
   - `"Build and run a medallion architecture pipeline for fraud detection using the table transactions and customers in my_catalog.my_schema"`

4. Durante a execução, o Genie Code frequentemente pausa para obter sua entrada:
   - Para tarefas complexas: cria um **plano passo a passo** e faz perguntas de esclarecimento
   - Quando precisa **rodar código ou atualizar o pipeline**: pede aprovação

### Opções de aprovação

| Opção | Comportamento |
|---|---|
| **Allow** | Permite esta ação específica |
| **Decline** | Recusa a ação |
| **Allow in this thread** | Permite para todas as ações nesta conversa |
| **Always allow** | Permite sempre (não pede mais confirmação) |
| **Continue** | Continua para os próximos passos após revisão |
| **Reject** | Pede para tentar outra abordagem |
| **Stop (botão vermelho)** | Para o Genie Code imediatamente enquanto trabalhando |

> **Importante:** Para continuar o trabalho e dar próximos passos, você precisa permanecer na tab atual onde o Genie Code está trabalhando.

---

## Capacidades em Agent Mode

### Data Discovery
Busca tabelas no workspace para encontrar os dados necessários para uma tarefa.

### Pipeline Code Edits
- Cria e edita **múltiplos arquivos ao mesmo tempo**
- Informa quais arquivos está alterando
- Mostra o **code diff** em cada arquivo para revisão individual ou conjunta no final

### Pipeline Execution
- Roda arquivos individuais
- Executa dry-run/run do pipeline
- Realiza full refresh
- Sempre pede confirmação antes de executar

### Understanding and Improving Pipeline Behavior
O Genie Code pode inspecionar datasets e outputs para entender o que o pipeline está fazendo end-to-end:
- Resumir transformações
- Rastrear como dados fluem para tabelas downstream
- Identificar mudanças inesperadas em row counts ou schemas
- Quando identifica problemas de qualidade de dados: raciocina sobre a causa e sugere onde e como endereçar no pipeline

---

## Casos de Uso Suportados

| Caso de Uso | Descrição |
|---|---|
| **Criar novo pipeline** | Genie Code auxilia em todos os passos: ingestão, padronização/limpeza dos dados, transformação e análise. Suporta arquitetura medallion completa (Bronze → Silver → Gold) |
| **Explicar um pipeline** | Analisa e explica um pipeline existente para onboarding rápido |
| **Corrigir issues** | Quando há erros, diagnostica e corrige os problemas iterando por múltiplos arquivos até resolver |

---

## Exemplos de Prompts

```
"Build and run a medallion architecture pipeline for fraud detection using 
the table transactions and customers in my_catalog.my_schema."
```

```
"Explain every step of this pipeline."
```

```
"Fix the failure in this pipeline."
```

```
"Create silver_sales_data in a new file that reads from bronze_sales_data,
cleans the data, and adds useful quality expectations."
```

---

## Governança e Acesso

As ações e o acesso do Genie Code são **governados pelas permissões do usuário**:
- Só pode acessar dados que você tem acesso
- Só pode executar operações para as quais você tem permissões
- Respeita controles do Unity Catalog integralmente

---

## Aviso de Risco

> *"Genie Code em Agent mode pode gerar e executar código no seu pipeline. Embora tenha guardrails para prevenir ações perigosas, ainda há risco. Use apenas com dados em que você confia e revise o código antes de executá-lo."*

---

## Próximos Passos Recomendados

- [Tips to improve Genie Code responses](./tips-and-tricks.md)
- [Add custom instructions](./custom-instructions.md)
- [Extend with agent skills](./agent-skills.md)
- [Connect to MCP servers](./mcp-integration.md)
