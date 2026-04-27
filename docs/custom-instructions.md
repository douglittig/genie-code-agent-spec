# Genie Code — Instruções Customizadas

> **Fonte:** [Add custom instructions](https://docs.databricks.com/aws/en/genie-code/instructions) — Última atualização: Apr 15, 2026

---

## O que são instruções customizadas?

Instruções customizadas permitem configurar como o Genie Code responde. Ele considera essas instruções ao gerar novas respostas, incluindo sugestões inline, chat, Suggest Fix e Agent mode — **exceto** Quick Fix e Autocomplete.

Exemplos do que incluir nas instruções:
- Preferências de bibliotecas (ex.: "use sempre PySpark, não pandas")
- Contexto sobre quem você é (nome, cargo)
- Convenções de código a seguir
- Guidelines de estilo e estrutura
- Tom de resposta (ex.: "use linguagem casual")

### Descoberta automática de arquivos de instrução

O Genie Code **descobre e lê automaticamente** `AGENTS.md` e `CLAUDE.md` no workspace. Ao abrir um notebook ou arquivo, ele percorre o diretório para cima (directory tree) e injeta o conteúdo de qualquer arquivo de instrução encontrado no seu contexto — **sem configuração necessária**.

---

## Dois tipos de instruções

| Tipo | Escopo | Arquivo | Quem pode criar |
|---|---|---|---|
| **User instructions** | Apenas você | `/Users/<username>/.assistant_instructions.md` | Qualquer usuário |
| **Workspace instructions** | Todo o workspace | `Workspace/.assistant_workspace_instructions.md` | Apenas admins |

Quando há conflito, o Genie Code **prioriza workspace instructions** sobre user instructions (salvo instrução explícita contrária).

---

## Instruções de Usuário

### Como criar

1. Abrir o painel Genie Code (ícone no canto superior direito do workspace)
2. Clicar no ícone de engrenagem para abrir as configurações
3. Em **User instructions**, clicar em **Add instructions file**
   - Isso cria o arquivo `.assistant_instructions.md` em `/Users/<seu-email>/`
4. Editar o arquivo com as instruções

> O Genie Code pega as novas instruções automaticamente na próxima interação.

**Atalho:** Você pode pedir ao próprio Genie Code para adicionar instruções. No painel, diga "remember that..." e ele atualiza o arquivo por você.

**Dica rápida:** A forma mais rápida de adicionar uma instrução é começar o input com o caractere `#`.

---

## Instruções de Workspace (Admin)

### Como criar (apenas admins)

1. No diretório `Workspace/` do workspace, criar um arquivo chamado `.assistant_workspace_instructions.md`
2. Adicionar as instruções no arquivo

### Como visualizar (todos os usuários)

1. Abrir o painel Genie Code → ícone de engrenagem → Settings
2. Em **Workspace instructions**, clicar em **View file**

Não-admins podem visualizar o arquivo para entender quais instruções o Genie Code está seguindo além das suas instruções de usuário.

---

## Boas Práticas para Escrever Instruções

| Prática | Detalhe |
|---|---|
| **Seja claro e específico** | Seja explícito e sem ambiguidade |
| **Limite de 20.000 caracteres** | Instruções além desse limite são ignoradas. Priorize o que é mais importante |
| **Use headings e bullet points** | Os arquivos são Markdown. Use formatação para dar estrutura (ex.: heading "Python code conventions" com lista de regras) |
| **Mantenha amplo escopo** | Instruções se aplicam a Inline, Chat, Suggest Fix e Agent mode, mas NÃO a Quick Fix e Autocomplete. Evite instruções muito específicas de contexto |
| **Inclua contexto e referências** | O Genie Code não busca informações adicionais proativamente. Inclua detalhes-chave diretamente nas instruções (ex.: quando usar uma tabela ou função específica) |

### Exemplo de estrutura de arquivo de instrução

```markdown
## Python code conventions
- Use PySpark instead of pandas for large datasets
- Always include type hints in function signatures
- Prefer f-strings over .format()

## Code style
- Keep functions under 50 lines
- Add docstrings to all public functions

## Data preferences
- Default catalog: my_catalog
- Default schema: my_schema
- Preferred table for customer data: customer_master
```

---

## Prioridade e Escopo

```
Workspace instructions  (maior prioridade)
        ↓
User instructions
        ↓
Context automático (código da célula atual, metadata do Unity Catalog, histórico)
```

As instruções se aplicam a:
- Inline suggestions (sugestões inline no editor)
- General Chat
- Suggest Fix
- Agent mode

**NÃO se aplicam a:**
- Quick Fix
- Autocomplete
