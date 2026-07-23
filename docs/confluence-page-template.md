# Template: Página Confluence para Pipeline de Dados

> **Como usar:** Copie este template para o Confluence ao criar a spec de um novo pipeline.
> Preencha **todos os campos obrigatórios** (marcados com `*`). Campos opcionais melhoram a qualidade do código gerado.
> O `sdd-define` lerá esta página via MCP (`confluence_get_page`) — estrutura previsível = extração determinística.

---

## 1. Visão Geral *

| Campo | Valor |
|-------|-------|
| **Nome do Projeto** | ex: `Pipeline de Vendas — Medallion` |
| **Objetivo** | 1-2 frases: o que resolve e para quem |
| **Problema Atual** | O que acontece sem esta pipeline? Qual é o impacto? |
| **Usuários / Consumidores** | Quem usa os dados no Gold? (Time de BI, modelo ML, relatório executivo...) |
| **Prazo** | ex: `2025-06-30` |
| **Autor da Spec** | Nome + contato |

---

## 2. Fontes de Dados *

> Uma linha por origem. Preencha o path completo do Unity Catalog quando disponível.

| ID | Sistema de Origem | Tipo | Path / Tabela | Colunas Principais | Volume | Frequência de Chegada |
|----|-------------------|------|---------------|-------------------|--------|----------------------|
| S1 | ex: ERP SAP | Tabela UC | `catalog.schema.tabela` | `order_id INT, amount DECIMAL(18,2), status VARCHAR` | ~500k linhas/dia | Batch diário às 02h UTC |
| S2 | ex: Kafka topic | Streaming | `catalog.schema.tabela` ou `topic-name` | `event_id, user_id, payload JSON` | ~10k eventos/min | Contínuo |
| S3 | ex: S3 clickstream | Arquivo | `s3://bucket/prefix/` | `session_id, page, ts` | ~50GB/dia | Horário |

**Colunas PII (opcional):** Liste as colunas que contêm dados pessoais para aplicar mascaramento no Silver.

| Origem | Coluna | Tipo PII |
|--------|--------|----------|
| S1 | `customer_email` | E-mail |
| S2 | `user_id` | Identificador |

---

## 3. Arquitetura da Pipeline *

### 3.1 Bronze — Ingestão Raw

> Captura fiel da origem, sem transformação. Apenas chegada e tipagem básica.

| Campo | Valor |
|-------|-------|
| **Tabela de destino** | `catalog.bronze.tabela_raw` |
| **O que capturar** | Todas as colunas da origem S1 + metadados de chegada (`_ingest_ts`, `_source`) |
| **Deduplicação** | Sim / Não — se sim, chave: `order_id + created_at` |
| **Retenção** | ex: `90 dias` / `indefinido` |

### 3.2 Silver — Limpeza e Enriquecimento

> Dados confiáveis, limpos e prontos para consumo analítico.

| Campo | Valor |
|-------|-------|
| **Tabela de destino** | `catalog.silver.tabela` |
| **Regras de limpeza** | ex: remover `status NOT IN ('active','pending','closed')` |
| **Regras de negócio** | ex: `amount > 0`, `order_id NOT NULL`, `created_at <= current_timestamp()` |
| **Enriquecimento** | ex: JOIN com `catalog.silver.clientes` pela chave `customer_id` |
| **Schema de saída** | Liste colunas calculadas/renomeadas: ex `revenue = amount * (1 - discount_pct)` |
| **Colunas PII** | Mascarar: `customer_email → SHA256`, `user_id → manter` |

**Joins (se houver múltiplas origens):**

| Join | Tipo | Chave Esquerda | Chave Direita | Resultado |
|------|------|----------------|---------------|-----------|
| S1 + S2 | INNER | `order_id` | `order_ref` | Enriquecer pedido com evento |

### 3.3 Gold — Agregações e Métricas

> Camada analítica. Granularidade e métricas de negócio definidas aqui.

| Campo | Valor |
|-------|-------|
| **Tabela de destino** | `catalog.gold.mart_tabela` |
| **Granularidade** | ex: `1 linha por cliente por dia` |
| **Métricas** | Definição exata de cada métrica (ver tabela abaixo) |
| **Particionamento** | ex: `DATE(event_date)` |
| **Consumidor final** | ex: `Power BI via SQL Warehouse`, `Feature Store`, `API de serving` |

**Definição de Métricas:**

| Métrica | Fórmula | Filtros | Unidade |
|---------|---------|---------|---------|
| `receita_bruta` | `SUM(amount)` | `status = 'paid'` | R$ |
| `ticket_medio` | `AVG(amount)` | `status = 'paid'` | R$ |
| `pedidos_ativos` | `COUNT(DISTINCT order_id)` | `status IN ('active','pending')` | unidade |

---

## 4. Configuração de Execução *

### 4.1 Estratégia de Trigger

| Campo | Valor |
|-------|-------|
| **Tipo de Trigger** | _(escolha uma opção abaixo)_ |

Opções:
- `batch_scheduled` — Execução agendada (ex: diário às 03h UTC). Preencher: `schedule: "0 3 * * *"`
- `continuous` — Pipeline DLT em modo contínuo, auto-restart. Latência mínima, custo mais alto.
- `streaming_triggered` — Micro-batch acionado a cada X minutos. Preencher: `interval: 15 min`
- `one_time` — Execução única para backfill histórico. Preencher: `start_date / end_date`

| Campo | Valor |
|-------|-------|
| **Schedule / Intervalo** | ex: `"0 3 * * *"` (cron) ou `15 min` |
| **SLA de Disponibilidade** | ex: `Gold disponível até 07h UTC` |
| **Tolerância a Atraso** | ex: `até 30 min de atraso é aceitável` |

### 4.2 Compute

| Campo | Valor |
|-------|-------|
| **Tipo de Compute** | _(escolha uma opção abaixo)_ |

Opções:
- `serverless` — DLT Serverless. Recomendado para a maioria dos casos. Sem gestão de cluster.
- `job_cluster` — Cluster dedicado criado e destruído por execução. Preencher: tipo de instância e workers.
- `classic_dlt` — DLT Classic com cluster fixo. Usar quando há restrições de rede/segurança.

| Campo | Valor |
|-------|-------|
| **Instância (se job_cluster)** | ex: `i3.xlarge`, `Standard_DS3_v2` |
| **Workers (se job_cluster)** | ex: `min: 2, max: 8 (autoscaling)` |
| **Região / Cloud** | ex: `AWS us-east-1`, `Azure East US 2` |

---

## 5. Qualidade de Dados (opcional, recomendado)

> Regras de qualidade que o Silver deve enforçar. Falhas bloqueiam ou alertam?

| Regra | Coluna | Condição | Ação ao Falhar |
|-------|--------|----------|----------------|
| Chave primária não nula | `order_id` | `IS NOT NULL` | `DROP` (descartar linha) |
| Valor positivo | `amount` | `> 0` | `DROP` |
| Status válido | `status` | `IN ('active','pending','closed','paid')` | `QUARANTINE` (tabela de rejeitos) |
| Completude | `created_at` | `IS NOT NULL` | `WARN` (alertar, não bloquear) |

---

## 6. Critérios de Aceite *

> Condições verificáveis que definem "pronto". Use números sempre que possível.

- [ ] Gold disponível até HH:MM UTC após início do batch
- [ ] 99,9% dos registros da origem presentes no Bronze dentro do SLA
- [ ] Zero chaves primárias nulas no Silver
- [ ] Métricas do Gold batem com relatório manual em ±0,1%
- [ ] Pipeline reprocessa intervalo histórico sem duplicatas (idempotente)

---

## 7. Restrições *

| Tipo | Restrição | Impacto no Design |
|------|-----------|-------------------|
| Técnica | ex: `Schema da origem não pode ser alterado` | Silver faz adaptação |
| Prazo | ex: `MVP em produção até 30/06` | Limita escopo do Gold |
| Budget | ex: `Sem aumento de custo de compute` | Prefere serverless |
| Segurança | ex: `Dados PII não podem sair do Unity Catalog` | Sem export para S3 externo |
| Legada | ex: `Deve conviver com pipeline atual por 30 dias` | Tabelas destino com prefixo `_v2` |

---

## 8. Fora do Escopo

> Explicitamente NÃO incluído nesta entrega.

- ex: Ingestão de fonte S3 legacy (adiado para Q3)
- ex: Dashboard no Power BI (responsabilidade do time de BI)
- ex: Monitoramento de alertas de SLA (próximo sprint)

---

## Subpáginas desta spec (se houver)

> O `sdd-define` lerá subpáginas automaticamente via `confluence_get_page` na hierarquia desta página.

- `Detalhamento de Schema — S1 (ERP SAP)`
- `Regras de Negócio — Silver`
- `Glossário de Métricas`
