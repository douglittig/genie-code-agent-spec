# Genie Code — Agent Skills

> **Fonte:** [Extend Genie Code with agent skills](https://docs.databricks.com/aws/en/genie-code/skills) — Última atualização: Apr 15, 2026

---

## O que são Skills?

Skills estendem o Genie Code com **capacidades especializadas e domain-specific**. Elas empacotam conhecimento de domínio, workflows, orientações, boas práticas, código reutilizável e scripts executáveis que o Genie Code pode carregar quando relevante.

**Diferença entre Skills e Instruções customizadas:**

| | Custom Instructions | Agent Skills |
|---|---|---|
| Aplicação | Global — toda interação | Automática e contextual — só quando relevante |
| Escopo | Preferências gerais, convenções | Workflows domain-specific detalhados |
| Conteúdo | Texto, guidelines | Scripts, exemplos, documentação adicional |
| Ativação | Sempre ativa (exceto Quick Fix/Autocomplete) | Auto-carregada no contexto certo; ou `@mention` manual |
| Disponibilidade | Chat, inline, Agent mode | **Apenas Agent mode** |

> **Importante:** Skills são suportadas **apenas no Genie Code Agent mode**.

---

## Tipos de Skills

| Tipo | Localização | Acesso | Quando usar |
|---|---|---|---|
| **Workspace skills** | `Workspace/.assistant/skills/` | Todos no workspace | Workflows úteis para a equipe inteira (ML pipelines, processos de domínio) |
| **User skills** | `/Users/{username}/.assistant/skills/` | Apenas você | Workflows pessoais não relevantes para outros |

Workspace admins podem criar workspace skills e conceder acesso à pasta de skills para que outros adicionem mais.

---

## Estrutura de uma Skill

Cada skill **deve ter sua própria pasta** com um arquivo `SKILL.md` dentro:

```
Workspace/.assistant/skills/
└── ml-workflows/
    └── SKILL.md

/Users/{username}/.assistant/skills/
└── personal-workflows/
    └── SKILL.md
```

Para skills mais complexas, você pode incluir arquivos adicionais referenciados pelo `SKILL.md`:

```
Workspace/.assistant/skills/
├── ml-workflows/
│   ├── SKILL.md                  # Visão geral e boas práticas do workflow
│   ├── training-patterns.md      # Padrões padrão de treinamento de ML
│   └── scripts/
│       └── model-deploy.py       # Automação de deploy de modelo

/Users/{username}/.assistant/skills/
├── personal-workflows/
│   ├── SKILL.md                  # Visão geral e boas práticas
│   ├── etl-patterns.md           # Boas práticas pessoais de ETL
│   ├── dashboard-templates.md    # Padrões reutilizáveis de dashboard
│   └── scripts/
│       └── pipeline-setup.sh     # Scripts de setup de ambiente
```

Ao referenciar outros arquivos, use **caminhos relativos a partir da raiz da skill**.

---

## Como Criar uma Skill

1. **Criar a pasta de skills** no caminho correto para o tipo de skill
   - Depois de criar, acesse rapidamente via Genie Code panel → Settings → **Open skills folder**

2. **Criar uma pasta dedicada** para a sua skill dentro da pasta de skills (cada skill = pasta própria)

3. **Criar o arquivo `SKILL.md`** dentro da pasta da skill — esse arquivo é obrigatório e define a skill

4. **Adicionar o frontmatter obrigatório:**

```markdown
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

5. **Adicionar as instruções da skill** em Markdown após o frontmatter. Estrutura recomendada:
   - Instruções passo a passo (orientação procedural clara)
   - Exemplos (inputs de amostra e outputs esperados)
   - Edge cases (variações comuns e exceções)

6. **(Opcional)** Para skills mais complexas, adicionar e referenciar recursos adicionais:
   - Scripts com código executável que o agente pode rodar
   - Arquivos com documentação adicional (boas práticas, templates)

> O Genie Code pega as skills automaticamente na próxima vez que você usar o Agent mode. Você também pode `@mencionar` uma skill para garantir que o Genie Code a utilize.

---

## Exemplo de SKILL.md

```markdown
---
name: pii-masking
description: Use this skill when working with data that contains PII (Personally Identifiable Information). Applies the company standard masking approach for names, emails, SSNs, and phone numbers.
---

## PII Masking Workflow

Follow these steps when masking PII in a pipeline:

### Step-by-step instructions
1. Identify columns containing PII using the approved PII registry table: `governance.pii_registry`
2. Apply masking using the `mask_pii()` UDF from `governance.masking_functions`
3. Add a data quality expectation to verify no raw PII remains in output tables
4. Log the masking operation to `audit.pii_operations`

### Examples

Input: `customers` table with `email`, `full_name`, `ssn` columns
```sql
SELECT
  mask_pii(email, 'email') AS email,
  mask_pii(full_name, 'name') AS full_name,
  mask_pii(ssn, 'ssn') AS ssn
FROM customers
```

### Edge cases
- If a column name is ambiguous, check `governance.pii_registry` for the canonical column list
- Timestamps and IDs are not PII — do not mask them
- For EU customers, apply GDPR-level masking (stricter) using `mask_pii_gdpr()`
```

---

## Invocação de Skills

**Automática:** O Genie Code carrega skills automaticamente com base na sua requisição e na descrição da skill. Mantém uma janela de contexto eficiente e reduz a necessidade de fornecer o mesmo contexto em múltiplos chats.

**Manual:** Use `@<skill-name>` no chat para garantir que o Genie Code use uma skill específica.

---

## Boas Práticas

| Prática | Detalhe |
|---|---|
| **Escolha o tipo certo** | Workspace para workflows que beneficiam muitos; User para workflows pessoais |
| **Mantenha foco** | Skills funcionam melhor quando focam em uma única tarefa ou workflow. Escopo estreito facilita o reconhecimento pelo Genie Code |
| **Use nomes e descrições claras** | Um nome conciso e descritivo ajuda o Genie Code a associar a skill à requisição certa |
| **Seja explícito e orientado a exemplos** | Descreva workflows passo a passo e inclua exemplos concretos ou padrões reutilizáveis |
| **Evite contexto desnecessário** | Inclua apenas informações necessárias para a tarefa. Detalhes extras dificultam a aplicação confiável |
| **Itere ao longo do tempo** | Trate skills como workflows vivos. Pequenas atualizações baseadas no uso real melhoram significativamente os resultados |
| **Separe orientação de automação** | Use Markdown para explicar intenção e boas práticas; use scripts para ações repetíveis. Manter essas preocupações distintas facilita manutenção e reuso |
| **Use versionamento** | Faça backup da pasta de skills com Databricks Git folders para rastrear mudanças, colaborar e fazer rollback quando necessário |

---

## Skills Embutidas

O Genie Code já vem com skills pré-configuradas para workflows Databricks comuns:
- Escrita de código em Databricks notebooks
- Exploração de dados no Unity Catalog
- Criação de dashboards
- Criação de pipelines
- Trabalho com MLflow

---

## Referências

- [Agent skills for AI coding assistants](https://docs.databricks.com/aws/en/genie-code/skills#see-also) — para descobrir e instalar skills para Claude e GitHub Copilot
