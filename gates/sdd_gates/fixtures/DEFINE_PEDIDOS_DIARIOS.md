# DEFINE: Pedidos diários na camada silver

> Tabela silver de pedidos, deduplicada e validada, para o time de Finanças fechar a receita do dia anterior às 7h.

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | PEDIDOS_DIARIOS |
| **Tamanho** | Grande — pipeline novo com duas tabelas e regra de qualidade |
| **Jira** | DADOS-412 |
| **Data** | 2026-11-02 |
| **Status** | Aprovado |

---

## Fontes

| Fonte | Link | O que foi usado |
|-------|------|-----------------|
| Confluence: Pedidos — visão silver | https://exemplo.atlassian.net/wiki/spaces/DADOS/pages/123 | Visão Geral, Fontes de Dados, Qualidade de Dados |
| Pedido do usuário | n/a | Pedido original e respostas, no Registro abaixo |

---

## Registro do pedido e das respostas

### Pedido original

> "quero a silver de pedidos sem duplicado até as 7h"

### Rodada 1

| ID | Pergunta, com a recomendação | Resposta do usuário |
|----|------------------------------|---------------------|
| Q1.1 | Há uma página no Confluence com a especificação? | "https://exemplo.atlassian.net/wiki/spaces/DADOS/pages/123" |
| Q1.2 | Evento que chega depois de 02h entra na carga do dia ou do dia seguinte? Recomendo o dia seguinte. | "você decide" |

---

## Problema

Finanças fecha a receita diária a partir da tabela bruta de pedidos, que tem duplicados quando o sistema de origem reenvia eventos. O fechamento sai com receita inflada em dias de reenvio e é corrigido à mão.

## Quem usa o dado

| Quem | Para quê | Dor hoje |
|------|----------|----------|
| Finanças | Fechamento diário de receita | Corrige duplicados à mão |
| Dashboard de vendas | Receita por canal | Números divergem do fechamento |

---

## Escopo

### Dentro do escopo

- Tabela `silver.pedidos` a partir de `bronze.pedidos_raw`
- Deduplicação por `pedido_id`, mantendo o evento mais recente
- Regras de qualidade com descarte e contagem

### Fora do escopo

- Camada gold de receita (feature separada)
- Correção dos dados históricos antes de 2026-01-01

---

## Requisitos

### R1: Silver sem duplicados — P1

**Por quê:** a receita do fechamento precisa contar cada pedido uma vez.

**Critérios de aceite (EARS):**

- **R1.1** QUANDO dois eventos chegarem com o mesmo `pedido_id` ENTÃO o pipeline DEVE manter só o de maior `atualizado_em`.
- **R1.2** O pipeline DEVE produzir no máximo uma linha por `pedido_id` em `silver.pedidos`.
- **R1.3** QUANDO o pipeline rodar duas vezes sobre a mesma partição ENTÃO a contagem de linhas de `silver.pedidos` DEVE ser a mesma.

### R2: Qualidade e disponibilidade — P1

**Por quê:** Finanças fecha às 7h com dado confiável.

**Critérios de aceite (EARS):**

- **R2.1** SE um evento chegar com `valor_total` nulo ou negativo ENTÃO o pipeline DEVE descartá-lo e contar o descarte na métrica da expectation.
- **R2.2** QUANDO um evento do dia anterior chegar até 02h ENTÃO o pipeline DEVE incluí-lo na carga das 05h.
- **R2.3** O pipeline DEVE terminar a carga diária até 06h30 (America/Sao_Paulo).

---

## Requisitos implícitos de dados

| Dimensão | Como fica nesta feature |
|----------|-------------------------|
| Idempotência e reprocessamento | R1.3 |
| Dado atrasado ou fora de ordem | R2.2; eventos depois de 02h ficam para o dia seguinte (S-1) |
| Duplicidade | R1.1, R1.2 |
| Evolução de schema | fora do escopo: schema da origem congelado neste trimestre |
| Backfill e carga histórica | fora do escopo (antes de 2026-01-01); 2026 entra pela carga inicial |
| Qualidade (nulos, chaves, faixas de valor) | R2.1 |
| Falha parcial e retomada | S-2 |
| PII, grants e Unity Catalog | não se aplica: a tabela não tem PII; grants herdados do schema silver |
| Freshness e SLA | R2.3 |
| Volume, custo e compute | S-3 |
| Observabilidade e alerta | R2.1 (métrica de descarte); alerta de atraso fora do escopo |

---

## Contexto técnico

| Aspecto | Valor |
|---------|-------|
| **Onde fica no projeto** | src/pipelines/pedidos/ |
| **Skills Databricks** | @databricks-pipelines, @databricks-dabs |
| **Infraestrutura nova** | um pipeline novo no bundle |
| **Trigger** | agendado: 0 5 * * * (America/Sao_Paulo) |
| **Compute** | serverless |

---

## Suposições

| ID | Padrão escolhido | Motivo | Origem | Se estiver errada |
|----|------------------|--------|--------|-------------------|
| S-1 | Evento depois de 02h entra na carga do dia seguinte | Combina com o fechamento às 7h | usuário delegou (Q1.2: "você decide") | Fechamento perde pedidos tardios |
| S-2 | Retomada pelo checkpoint do pipeline, sem lógica própria | Padrão do Lakeflow, já usado no projeto | código: `src/pipelines/pedidos/pipeline.py` | Reprocessamento manual em falha |
| S-3 | Serverless padrão, sem modo performance | ~2 milhões de linhas por dia | código: `resources/pedidos.pipeline.yml` | Custo ou tempo acima do previsto |

## Perguntas em aberto

- Nenhuma.

---

## Rastreabilidade

| Critério | Origem |
|----------|--------|
| R1.1 | Confluence › Qualidade de Dados |
| R1.2 | pedido: "sem duplicado" |
| R1.3 | rubrica: idempotência |
| R2.1 | Confluence › Qualidade de Dados |
| R2.2 | Confluence › Fontes de Dados |
| R2.3 | pedido: "até as 7h" |

---

## Aprovação

**Aprovado**: 2026-11-02 — v1.0 — usuário: "pode seguir com essa spec"

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-11-02 | Versão inicial |
