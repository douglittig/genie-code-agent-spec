# DESIGN: Pedidos diários na camada silver

> Um pipeline Lakeflow serverless, declarado no bundle e agendado às 05h, lê a bronze, deduplica e valida.

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | PEDIDOS_DIARIOS |
| **DEFINE** | `docs/specs/DEFINE_PEDIDOS_DIARIOS.md` — v1.0 |
| **TASKS** | `docs/planning/TASKS_PEDIDOS_DIARIOS.md` — v1.0 |
| **ADR** | não há |
| **Data** | 2026-11-02 |

---

## Visão geral

```mermaid
flowchart LR
  A[bronze.pedidos_raw] --> B[pipeline pedidos: dedup + expectation] --> C[silver.pedidos]
```

## Componentes

| Componente | Tipo | Onde fica | Critérios | Tasks | Constrói com |
|------------|------|-----------|-----------|-------|--------------|
| Pipeline `pedidos` | recurso do bundle | `resources/pedidos.pipeline.yml` | R2.3 | T1, T6 | @databricks-dabs |
| `silver.pedidos` | tabela streaming | `src/pipelines/pedidos/pipeline.py` | R1.1, R1.2, R1.3, R2.2 | T2, T3, T5 | @databricks-pipelines |
| Expectation de `valor_total` | expectation do Lakeflow | `src/pipelines/pedidos/pipeline.py` | R2.1 | T4 | @databricks-pipelines |

## O que já existe e será reaproveitado

| O quê | Onde | Como entra nesta feature |
|-------|------|--------------------------|
| Bundle do projeto, com target `dev` em `mode: development` | `databricks.yml` | O pipeline novo entra no mesmo bundle |

## Decisões

| ID | Decisão | Alternativa descartada | Por quê | Base |
|----|---------|------------------------|---------|------|
| D-1 | Deduplicar com AUTO CDC (SCD tipo 1) por `pedido_id`, em sequência por `atualizado_em` | Materialized view com `row_number()` | A view recalcula tudo a cada carga | @databricks-pipelines |

## Dados

| Tabela | Chave | Escrita | Observação |
|--------|-------|---------|------------|
| `silver.pedidos` | `pedido_id` | AUTO CDC, SCD tipo 1 | Sequência por `atualizado_em` |

## Testes

Testes unitários em `tests/`, com DataFrames em memória e `assertDataFrameEqual` (PySpark 4.0). As provas de expectation e de horário rodam no target `dev`, lendo o event log do pipeline.

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-11-02 | Versão inicial |
