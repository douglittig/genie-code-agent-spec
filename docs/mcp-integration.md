# Genie Code — Integração com MCP Servers

> **Fonte:** [Connect Genie Code to MCP servers](https://docs.databricks.com/aws/en/genie-code/mcp) — Última atualização: Apr 16, 2026

---

## O que é MCP?

**Model Context Protocol (MCP)** é um padrão open source que conecta agentes de IA a ferramentas, recursos, prompts e outras informações contextuais. Ele fornece uma forma padronizada de expor ferramentas, dados e workflows ao Genie Code **sem embutir esse contexto diretamente em prompts ou instruções**.

> **Importante:** MCP servers são suportados **apenas no Genie Code Agent mode**.

### Por que usar MCP?

MCP é projetado para casos onde contexto importante já existe mas é difícil de acessar por um agente de IA:

| Categoria | Problema sem MCP | Solução com MCP |
|---|---|---|
| **Documentation systems** | Times copiam seções do Confluence manualmente nos prompts | Conteúdo exposto uma vez via MCP server e referenciado quando relevante |
| **Tools and services** | APIs e scripts internos de plataforma não estão acessíveis ao agente | MCP torna essas capacidades diretamente disponíveis |
| **Data sources** | Dados fora do Databricks são inacessíveis | Acesso seguro via MCP servers externos |
| **Custom apps** | Ferramentas proprietárias ou integrações específicas da org | Databricks Apps como MCP servers customizados |

MCP **substitui o copy-paste manual** com uma abordagem estruturada e reutilizável, disponibilizando o contexto certo apenas quando necessário.

---

## Tipos de MCP Server no Genie Code

### 1. Unity Catalog Function
- Seleciona o schema da função
- Permite ao Genie Code usar funções para rodar queries SQL predefinidas

### 2. Vector Search
- Seleciona o schema do índice
- Permite ao Genie Code consultar o índice de vector search para encontrar documentos relevantes
- Seus documentos podem já estar no Databricks como vector search index

### 3. Genie Space
- Seleciona o Genie space
- O Genie MCP invoca o Genie como ferramenta, permitindo consultar o Genie space para analisar dados usando linguagem natural

### 4. External MCP Server
- Seleciona a Unity Catalog connection para usar como MCP server externo
- É necessário fazer login na connection primeiro antes de usá-la

### 5. Custom MCP Server (via Databricks Apps)
- Seleciona o Databricks App para usar como MCP server customizado
- Permite usar quaisquer ferramentas custom-defined
- **Requisitos:**
  - O app deve estar deployado no mesmo workspace
  - O MCP server deve ser acessado em `https://<server-url>/mcp`
  - O app deve ser stateless: `mcp_app = mcp_server.http_app(stateless_http=True)`
  - Para erros de CORS, adicionar a URL do workspace à lista de origens permitidas:
    ```python
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    ```

---

## Conectores de Terceiros (Beta)

> **Preview:** Para usar, o workspace admin deve habilitar "Third Party Connectors for Agents".

O Genie Code oferece conectores embutidos para Google Drive e SharePoint.

### Como conectar

1. No workspace, abrir Genie Code no canto superior direito
2. No prompt bar, clicar no ícone `+`
3. Ao lado da fonte de dados, clicar em **Connect**
4. Completar os passos de login

Cada usuário se autentica individualmente — OAuth tokens **não** são compartilhados entre usuários.

### Limitações do Google Drive

- Tamanho máximo de arquivo: **10 MB**
- Apenas arquivos nativos do Google Workspace: **Docs, Sheets, Slides**
- PDFs, imagens e outros formatos binários **não são suportados**
- Erros de expiração de token podem aparecer no output — reautenticar resolve

### Limitações do SharePoint

- Tamanho máximo de arquivo: **10 MB**
- Formatos suportados: Office documents (`.docx`, `.xlsx`, `.pptx`) + formatos text-based (`.txt`, `.csv`, `.json`, `.md`)
- PDFs, imagens e outros formatos binários **não são suportados**

> **Nota:** Ferramentas de data source nem sempre disparam automaticamente. Se a busca por documentos não iniciar, tente promptar explicitamente: `"use Google Docs"` ou `"use SharePoint"`.

---

## Como Adicionar MCP Servers Manualmente

1. Abrir Genie Code settings (painel → Settings)
2. Em **MCP Servers**, clicar em `+` **Add Server**
3. Selecionar o tipo de MCP server desejado e configurar
4. Clicar em **Save**

Após adicionados, os MCP servers ficam imediatamente disponíveis. O Genie Code os usa automaticamente no Agent mode quando relevante — sem necessidade de alterar prompts ou instruções.

---

## Limites e Controles

| Limite | Valor |
|---|---|
| **Máximo de ferramentas MCP** | 20 tools no total, across all servers |
| **Controle de acesso** | Workspace admins controlam quais servers estão disponíveis; usuários selecionam dentre os aprovados |
| **Permissões** | Metastore admins e connection owners podem gerenciar ou revogar permissões de usuários |

Você pode escolher quais ferramentas e servers habilitar ou desabilitar nas configurações do Genie Code.

---

## Casos de Uso Comuns

```
Jira task → Genie Code coleta contexto → executa tarefa → atualiza ticket
```

```
Confluence/GitHub/Notion → MCP → Genie Code referencia runbooks ao fazer troubleshooting
```

```
Vector search index interno → MCP → Genie Code busca documentos relevantes automaticamente
```

```
Genie Space → MCP → análise de dados em linguagem natural dentro do Agent mode
```

---

## Referências

- [Model Context Protocol (MCP) on Databricks](https://docs.databricks.com/aws/en/genie-code/mcp)
- [Create a GitHub MCP server](https://docs.databricks.com/aws/en/genie-code/mcp)
