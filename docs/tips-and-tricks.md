# Genie Code — Tips & Tricks

> **Fonte:** [Tips to improve Genie Code responses](https://docs.databricks.com/aws/en/genie-code/tips) — Última atualização: Apr 16, 2026

---

## Seja Específico nos Prompts

A estrutura e o nível de detalhe das respostas variam — mesmo para o mesmo prompt. Quanto mais orientação você fornecer, melhor o resultado.

| O que especificar | Exemplo |
|---|---|
| **Nível de detalhe** | `"Explain this code in a couple sentences"` ou `"Explain this code line-by-line"` |
| **Biblioteca específica** | `"Create a visualization using Matplotlib"` ou `"using Seaborn"` |
| **Estrutura da resposta** | `"Provide instructions in numbered steps"` ou `"as bullet points with brief explanations"` |
| **Query em linguagem natural** | `"List active and retired NFL quarterbacks' passing completion rate, for those who had over 500 attempts in a season"` — Genie Code usa colunas como `s.player_id` e `s.attempts` automaticamente |

---

## Forneça Contexto

### Adicionar contexto manualmente

No painel Genie Code, clique em **Add context** para selecionar manualmente recursos como tabelas, pipelines, notebooks, queries e arquivos.

Ou use `@<resource-name>` diretamente no chat. O contexto selecionado aparece no topo do prompt box e **persiste ao longo do chat**.

### Referenciar células específicas (notebooks)

- Clique em **Add context** → **Cells** → selecione a célula desejada
- Ou use `@cell` no chat prompt e selecione na lista

Útil para perguntar sobre o código ou output de uma célula específica.

### Contexto automático disponível

O Genie Code tem acesso automático a:
- Código ou queries na **célula atual** do notebook ou aba do SQL editor
- **Nomes e descrições** de tabelas e colunas
- **Histórico de prompts** anteriores na conversa
- **Tabelas favoritas e ativas**
- Para o feature **diagnose error**: stack trace do output de erro

### Iteração

Como o Genie Code usa o histórico da conversa, você pode pedir para alterar uma resposta anterior **sem reescrever o prompt inteiro**. Use o histórico para iterativamente limpar, explorar, filtrar e fatiar DataFrames.

---

## Anexar Imagens aos Prompts

### Como anexar

- **Copy-paste** da imagem direto no chat prompt
- **Drag and drop** no chat prompt
- Clicar no ícone `+` → **Attach image** para selecionar do seu computador

### Quando usar imagens

| Situação | Detalhe |
|---|---|
| Informação visual que o Genie Code não tem acesso | Genie Code já consegue ver imagens e charts em arquivos/notebooks do workspace — só anexe imagens externas |
| Entender conteúdo visual | Diagramas, flowcharts, esboços de arquitetura, screenshots de slides, fotos de whiteboard |
| Dados externos apresentados visualmente | Gráficos, dashboards ou relatórios onde tendências, anomalias ou labels importam |
| Extrair texto de imagens | Fotos/scans de documentos, notas manuscritas, etiquetas |
| Fotos do mundo real | Descrever cenas, verificar se algo atende uma especificação |

---

## Trabalhando com Datasets

### Encontrar tabelas

Use o prompt `"Find tables"` ou o comando `/findTables` para melhores resultados:
```
"Find tables related to NFL games."
```

### Referenciar tabela específica

Use `@<table-name>` no prompt ou clique em **Add context** no chat. O Genie Code adapta as respostas para usar aquela tabela.

### Selecionar colunas de um DataFrame

Para resultados mais precisos, forneça uma query inicial:
```sql
SELECT * FROM <table_name>
```
Isso permite ao Genie Code obter os nomes das colunas sem precisar adivinhar.

### Conversões de tipo de dado

Se precisar de conversões, forneça detalhes explícitos:
```
"Convert this code from pandas to PySpark, including the code needed to convert 
the pandas DataFrame to a PySpark DataFrame and changing the data type of column 
churn from boolean to integer."
```

### Documentar tabelas no Unity Catalog

Adicionar comentários em tabelas e colunas no Unity Catalog dá mais contexto ao Genie Code. Use table/column comments no Catalog Explorer para adicionar sample data.

Exemplo: se a coluna `height` está no formato `feet-inches`, adicione o comentário:
```
"The height column is in string format and is separated by a hyphen. Example: '6-2'."
```

---

## Executar Código no Chat Pane

Você pode rodar código diretamente no painel Genie Code para validar ou usar como scratchpad.

**Como funciona:**
- Disponível em todas as páginas do Databricks
- Usa o recurso de compute atual da página (ou serverless se não houver)
- **Pede permissão antes de rodar** — você pode escolher "Always allow"
- Output é exibido diretamente no chat pane

Exemplo real (Python):
```python
df = spark.table("samples.nyctaxi.trips").orderBy(F.rand()).limit(10)
display(df)
```

Genie Code encontra a tabela correta automaticamente e sugere a query.

---

## Atalhos e Cell Actions

### Atalho de teclado

| Ação | Tecla |
|---|---|
| Nova linha no chat (sem enviar) | `Shift + Enter` |

### Cell Actions em notebooks

Cell actions são atalhos para tarefas comuns diretamente em células do notebook:
- **Document (comment):** Adiciona comentários/docstrings ao código
- **Fix:** Corrige erros na célula
- **Explain:** Explica o código da célula

---

## Dicas por Perfil

- **Data Analysts:** [Genie Code Tips and Tricks for Data Analysts](https://docs.databricks.com/aws/en/genie-code/tips)
- **Data Engineers:** [Genie Code Tips and Tricks for Data Engineers](https://docs.databricks.com/aws/en/genie-code/tips)

---

## Formas de Customizar o Genie Code

| Mecanismo | Para quê |
|---|---|
| [Custom Instructions](./custom-instructions.md) | Preferências globais, convenções, tom de resposta |
| [Agent Skills](./agent-skills.md) | Capacidades domain-specific reutilizáveis no Agent mode |
| [MCP Servers](./mcp-integration.md) | Acesso a ferramentas externas e fontes de dados |
