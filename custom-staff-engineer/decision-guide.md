# Decision Guide — Padrões Arquiteturais do Time

> **Este arquivo é de propriedade do time de engenharia.**
> É aqui que o time documenta suas decisões arquiteturais padronizadas, restrições
> corporativas, políticas de PII e orientações técnicas que o `@custom-staff-engineer`
> deve seguir em TODA discussão arquitetural.
>
> **Preencha este arquivo antes de usar a skill `@custom-staff-engineer` em produção.**
> Quanto mais completo este guia, menos perguntas o custom-staff-engineer precisará fazer
> e mais consistentes serão os ADRs gerados.
>
> Seções marcadas com `[PREENCHER]` são obrigatórias.
> Seções marcadas com `[EXEMPLO]` são referências técnicas — revise e adapte ao contexto do time.

---

## 1. Padrões de Processamento [PREENCHER]

> Documente quando usar cada padrão de processamento. Isso elimina discussão
> recorrente e garante consistência entre times.

### Quando usar Lakeflow SDP (DLT)
<!-- Documente os critérios do seu time. Exemplos de critérios comuns: -->
- [PREENCHER] Ex: Pipelines com Auto Loader (ingestão de arquivos)
- [PREENCHER] Ex: Casos com necessidade de qualidade de dados nativa (expectations)
- [PREENCHER] Ex: CDC a partir de fontes relacionais

### Quando usar Structured Streaming
- [PREENCHER] Ex: Consumo de Kafka com lógica stateful complexa
- [PREENCHER] Ex: Stream-stream joins com watermark
- [PREENCHER] Ex: Latência abaixo de X segundos (definir o threshold)

### Quando usar Batch Jobs
- [PREENCHER] Ex: Transformações simples com frequência > 1 hora
- [PREENCHER] Ex: Relatórios e agregações históricas
- [PREENCHER] Ex: Casos onde custo é prioridade sobre frescor

### Regra de desempate
- [PREENCHER] Ex: "Em caso de dúvida, preferir DLT sobre Structured Streaming manual"

---

## 2. Arquitetura de Camadas [PREENCHER]

> Defina a nomenclatura e responsabilidade de cada camada do seu lakehouse.
> O padrão de referência é o Medallion Architecture (Bronze → Silver → Gold).

| Camada Medallion | Nome no time | Responsabilidade | Formato | Particionamento padrão |
|-----------------|-------------|-----------------|---------|----------------------|
| Bronze | [PREENCHER] | [PREENCHER] | Delta / Parquet | [PREENCHER] |
| Silver | [PREENCHER] | [PREENCHER] | Delta | [PREENCHER] |
| Gold | [PREENCHER] | [PREENCHER] | Delta | [PREENCHER] |

**Regras de camada:**
- [PREENCHER] Ex: "Nenhuma regra de negócio na camada Bronze — ingestão fiel à fonte"
- [PREENCHER] Ex: "Silver é a camada canônica — dados limpos, tipados e validados"
- [PREENCHER] Ex: "Gold é somente leitura para consumidores externos e BI"

---

## 3. Políticas de PII e Dados Sensíveis [PREENCHER]

> **Esta seção é crítica.** Documente as políticas de PII do time/empresa.
> O `@custom-staff-engineer` usará isto para classificar campos e definir controles.

### Classificação de dados
| Categoria | Definição | Exemplos de campos |
|-----------|-----------|-------------------|
| PII Direto | [PREENCHER] | CPF, RG, e-mail, telefone, nome completo |
| PII Indireto | [PREENCHER] | IP, device ID, localização |
| Sensível | [PREENCHER] | Dados financeiros, dados de saúde |
| Interno | [PREENCHER] | Dados operacionais sem PII |
| Público | [PREENCHER] | Dados abertos, catálogos |

### Controles obrigatórios por categoria
| Categoria | Mascaramento | Acesso | Retenção | Auditoria |
|-----------|-------------|--------|----------|-----------|
| PII Direto | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| PII Indireto | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Sensível | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

### Funções de mascaramento aprovadas
- [PREENCHER] Ex: `ai_mask()` para mascaramento em SQL
- [PREENCHER] Ex: SHA-256 para tokenização de identificadores
- [PREENCHER] Ex: Column masking via Unity Catalog para acesso diferenciado por grupo

### Ambientes e PII
- [PREENCHER] Ex: "Dados de produção com PII nunca podem estar no ambiente dev"
- [PREENCHER] Ex: "Usar dados sintéticos em dev/stg para campos PII"

---

## 4. Padrões de Governança (Unity Catalog) [PREENCHER]

### Estrutura de catalogs e schemas
- [PREENCHER] Ex: Um catalog por ambiente (dev_catalog, stg_catalog, prod_catalog)
- [PREENCHER] Ex: Schemas por domínio de negócio (vendas, marketing, financeiro)

### Controle de acesso padrão
- [PREENCHER] Ex: Grupos por função (engenharia, analytics, ciência de dados)
- [PREENCHER] Ex: Regra de menor privilégio: leitura por padrão, escrita explícita

### Data contracts
- [PREENCHER] Ex: "Toda tabela Silver deve ter um owner declarado"
- [PREENCHER] Ex: "Breaking changes em schemas requerem aprovação do data owner"

---

## 5. Padrões de Deploy (Asset Bundles) [PREENCHER]

### Ambientes obrigatórios
- [PREENCHER] Ex: dev → stg → prod (três ambientes)
- [PREENCHER] Ex: Aprovação manual para deploy em prod

### Secrets e configuração
- [PREENCHER] Ex: Databricks Secrets por ambiente (dev-scope, prod-scope)
- [PREENCHER] Ex: Variáveis de ambiente no databricks.yml por target

### Nomeação de recursos
- [PREENCHER] Ex: `[{env}] {time} - {nome do recurso}`

---

## 6. Confiabilidade e SLA [PREENCHER]

### SLAs padrão por criticidade
| Criticidade | Frescor máximo | RTO | RPO |
|-------------|---------------|-----|-----|
| Alta | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Média | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Baixa | [PREENCHER] | [PREENCHER] | [PREENCHER] |

### Política de retry
- [PREENCHER] Ex: Máximo de 3 tentativas com backoff exponencial
- [PREENCHER] Ex: Dead letter table obrigatório para pipelines críticos

### Alertas obrigatórios
- [PREENCHER] Ex: Alerta se pipeline não executar no SLA
- [PREENCHER] Ex: Alerta se taxa de erros > X%

---

## 7. Referências Técnicas [EXEMPLO]

> Conteúdo abaixo é referência técnica baseada em padrões Databricks.
> Revise e adapte ao contexto do time — não é política, é contexto técnico.

### Guia rápido de decisão: DLT vs Streaming vs Batch

| Critério | Favorece DLT | Favorece Streaming | Favorece Batch |
|----------|-------------|-------------------|----------------|
| Fonte de dados | Arquivos, CDC relacional | Kafka, Kinesis | Qualquer |
| Latência necessária | Minutos | Segundos | Horas |
| Complexidade de estado | Baixa | Alta | Qualquer |
| Qualidade de dados | Nativa (expectations) | Manual | Manual |
| Custo relativo | Médio | Alto | Baixo |
| Complexidade operacional | Baixa | Alta | Baixa |

### Decisões de clustering e particionamento

| Volume da tabela | Estratégia recomendada |
|-----------------|----------------------|
| < 1 TB | Sem particionamento |
| 1–10 TB | Liquid Clustering nas colunas de filtro frequente |
| > 10 TB | Particionamento por data + Liquid Clustering |

> Liquid Clustering é o sucessor do Z-Order — use um ou outro, nunca os dois.

### Quando usar cada camada de serving

| Caso de uso | Serving recomendado |
|-------------|-------------------|
| BI e dashboards | DBSQL Warehouse |
| Exploração ad-hoc por negócio | Genie Space |
| APIs com baixa latência | Model Serving |
| Queries programáticas | DBSQL + SDK |
