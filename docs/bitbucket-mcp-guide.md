# Guia: Atlassian Rovo MCP + Bitbucket Cloud no Genie Code

> **Fonte oficial:** [Atlassian Rovo MCP Server](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/) | [Interacting with Bitbucket via MCP](https://support.atlassian.com/bitbucket-cloud/docs/interacting-with-bitbucket-via-mcp/)
> **Última verificação:** Abril 2026

---

## ⚠️ Pré-requisito Crítico: Bitbucket Cloud ONLY

O Atlassian Rovo MCP Server suporta **apenas Bitbucket Cloud**.

| Plataforma | Suporte |
|---|---|
| Bitbucket Cloud | ✅ Suportado |
| Bitbucket Data Center | ❌ Não suportado |
| Bitbucket Server | ❌ Não suportado |

**Se sua empresa usa Bitbucket Data Center ou Server, esta integração não está disponível hoje.**
Registre a necessidade com a Atlassian via feedback/roadmap. Ver também `BACKLOG.md` item 6.

Requisito adicional: a workspace do Bitbucket Cloud deve estar **vinculada a uma Organização Atlassian**.

---

## Visão Geral da Arquitetura

```
Genie Code (Agent mode)
        │
        │ External MCP Server
        ▼
Unity Catalog Connection
        │
        │ HTTPS / API Token
        ▼
https://mcp.atlassian.com/v1/mcp/authv2
        │
        │ Atlassian permissions
        ▼
Bitbucket Cloud (PRs, repos, pipelines)
```

---

## O que o Genie Code consegue fazer com esta integração

| Operação | Disponível |
|---|---|
| Listar repositórios e workspaces | ✅ |
| Ler branches, commits e conteúdo de arquivos | ✅ |
| Criar e atualizar Pull Requests | ✅ |
| Ler comentários e diffs de PRs | ✅ |
| Aprovar e fazer merge de PRs | ✅ |
| Adicionar comentários em PRs | ✅ |
| Ver pipelines, steps e logs | ✅ |
| Listar ambientes e deployments | ✅ |
| Criar commits (conteúdo de repositório) | ✅ |
| Operações de branch via terminal | ❌ (sem acesso a terminal) |

---

## Impacto no Limite de 20 Ferramentas MCP

O Atlassian Rovo MCP expõe ferramentas para todos os produtos Atlassian habilitados. Ao ativar apenas Bitbucket, as ferramentas consumidas são aproximadamente:

| Grupo de ferramentas | Slots estimados |
|---|---|
| bitbucketWorkspace (list, get) | ~2 |
| bitbucketRepository (list, get, defaultReviewers) | ~3 |
| bitbucketPullRequest (list, get, comments, diff) | ~4 |
| bitbucketPipeline (list, get, steps, logs) | ~4 |
| bitbucketEnvironment + Deployment | ~4 |
| **Total estimado (só Bitbucket)** | **~17 slots** |

> Se você também usa Jira ou Confluence via MCP na mesma sessão, o limite de 20 ferramentas pode ser atingido rapidamente. Priorize as ferramentas essenciais ao configurar.

---

## Passo a Passo de Configuração

### Parte 1 — Administrador Atlassian (uma vez por organização)

1. Confirmar que a workspace do Bitbucket Cloud está vinculada a uma Organização Atlassian:
   - Acessar `admin.atlassian.com`
   - Verificar se a workspace aparece sob a organização

2. Habilitar autenticação via API Token para Bitbucket:
   - `Admin Hub` → `Rovo` → `Rovo MCP Server`
   - Habilitar **"API Token Authentication"**
   - Salvar configuração

> **Nota:** OAuth 2.1 para Bitbucket está em roadmap — hoje o único método é API Token.

---

### Parte 2 — Usuário: Gerar API Token Atlassian

1. Acessar as configurações da conta Atlassian:
   `https://id.atlassian.com/manage-profile/security/api-tokens`

2. Clicar em **"Create API token"**

3. Definir nome descritivo (ex: `genie-code-mcp`)

4. Copiar o token gerado — **ele só é exibido uma vez**

5. Guardar o token de forma segura (gerenciador de senhas corporativo)

---

### Parte 3 — Administrador Databricks: Criar Unity Catalog Connection

Para que o Genie Code acesse um MCP server externo, é necessário criar uma **Unity Catalog Connection** apontando para o endpoint da Atlassian.

1. No Databricks, acessar **Catalog Explorer** → **Connections** → **Create connection**

2. Configurar a connection:
   - **Connection name:** `atlassian_rovo_mcp`
   - **Connection type:** `HTTP`
   - **Host:** `mcp.atlassian.com`
   - **Path:** `/v1/mcp/authv2`
   - **Authentication:** Bearer Token
   - **Token:** `<api-token-do-usuário>` *(ou configurar via secret scope)*

3. Conceder `USE CONNECTION` ao grupo de desenvolvedores:
   ```sql
   GRANT USE CONNECTION ON CONNECTION atlassian_rovo_mcp TO `grupo-desenvolvedores`;
   ```

> **Recomendação de segurança:** Use Databricks Secret Scopes para armazenar o API token em vez de inserí-lo diretamente. Cada usuário deve ter sua própria connection com seu próprio token.

---

### Parte 4 — Usuário: Adicionar MCP Server no Genie Code

1. Abrir o Genie Code no Databricks (ícone no canto superior direito)

2. Clicar em **Settings** (ícone de engrenagem)

3. Em **MCP Servers**, clicar em **+ Add Server**

4. Selecionar **"External MCP Server"**

5. Selecionar a Unity Catalog connection criada: `atlassian_rovo_mcp`

6. Clicar em **Login** quando solicitado e autenticar com o API token

7. Clicar em **Save**

8. Confirmar que está em **Agent mode** (não Chat mode)

---

### Parte 5 — Teste de Verificação

No Genie Code Agent mode, testar:

```
Liste os repositórios disponíveis no workspace do Bitbucket
```

Resposta esperada: lista de repositórios da sua workspace Bitbucket Cloud.

```
Mostre os pull requests abertos no repositório <nome-do-repo>
```

Se ambos funcionarem, a integração está operacional.

---

## Uso no Dev Workflow

Com o MCP configurado, o Genie Code consegue executar automaticamente os passos git do `@sdd-dev-workflow` que antes precisavam ser feitos manualmente via UI:

| Passo do sdd-dev-workflow | Sem MCP | Com MCP Bitbucket |
|---|---|---|
| Criar PR | Manual via UI | Genie Code cria automaticamente |
| Listar PRs abertos | Manual via UI | Genie Code lista e resume |
| Adicionar comentário em PR | Manual via UI | Genie Code adiciona |
| Ver status de pipeline | Manual via UI | Genie Code consulta |
| Aprovar PR | Manual via UI | Genie Code aprova (com confirmação) |

> **O que o MCP NÃO faz:** criar branches, fazer checkout, commitar arquivos locais. Essas operações de fluxo git local continuam sendo feitas via UI do Git Folders do Databricks.

---

## Limitações e Considerações

| Item | Detalhe |
|---|---|
| **Cloud only** | Bitbucket Data Center/Server não suportado |
| **Autenticação** | API Token apenas (OAuth em roadmap) |
| **Escopo de token** | Token tem acesso a todos os repositórios do usuário — não é possível restringir por repo |
| **Rate limit** | 500–10.000 chamadas/hora dependendo do plano Atlassian |
| **Endpoint legado** | `https://mcp.atlassian.com/v1/sse` será descontinuado em 30/06/2026 — usar `/v1/mcp/authv2` |
| **Slots MCP** | ~17 slots apenas para Bitbucket — deixa pouca margem para outros servers |
| **Conexão por usuário** | Cada desenvolvedor precisa de sua própria connection com seu próprio token |

---

## Referências Oficiais

| Recurso | URL |
|---|---|
| Getting Started — Atlassian Rovo MCP | https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/ |
| Bitbucket via MCP — Atlassian | https://support.atlassian.com/bitbucket-cloud/docs/interacting-with-bitbucket-via-mcp/ |
| Atlassian MCP Server — Platform page | https://www.atlassian.com/platform/remote-mcp-server |
| Genie Code MCP — Databricks | https://docs.databricks.com/aws/en/genie-code/mcp |
| API Tokens — Atlassian | https://id.atlassian.com/manage-profile/security/api-tokens |
