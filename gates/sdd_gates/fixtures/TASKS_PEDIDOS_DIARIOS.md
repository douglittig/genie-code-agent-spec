# TASKS: Pedidos diários na camada silver

> A silver de pedidos em duas fatias: primeiro sem duplicados, depois validada e pronta no horário.

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | PEDIDOS_DIARIOS |
| **DEFINE** | `docs/specs/DEFINE_PEDIDOS_DIARIOS.md` — v1.0 |
| **ADR** | não há |
| **Épico (Jira)** | DADOS-412 |
| **Data** | 2026-11-02 |
| **Status** | Aprovado |

---

## Histórias

### H1: Finanças lê a silver sem duplicados — 5 pontos

**Como** Finanças, **quero** uma linha por pedido em `silver.pedidos`, **para** fechar a receita sem corrigir duplicados à mão.

**Jira:** DADOS-413

| Task | O que faz | Critérios | Depende de | Teste | Gate |
|------|-----------|-----------|------------|-------|------|
| T1 | Declara o pipeline `pedidos` no bundle, serverless e sem schedule | — | — | — | `databricks bundle validate` |
| T2 | Lê `bronze.pedidos_raw` e mantém o evento de maior `atualizado_em` por `pedido_id` | R1.1, R1.2 | T1 | `tests/test_dedup.py`: dois eventos do mesmo pedido → fica o mais recente, uma linha por pedido (`assertDataFrameEqual`) | `pytest tests/test_dedup.py` |
| T3 | Garante que reprocessar a mesma partição não muda a contagem | R1.3 | T2 | `tests/test_dedup.py::test_reprocessa_mesma_particao` | `pytest tests/test_dedup.py` |

### H2: A carga das 05h chega validada antes das 06h30 — 3 pontos

**Como** Finanças, **quero** a carga das 05h validada e pronta às 06h30, **para** fechar a receita às 7h com dado confiável.

**Jira:** DADOS-414

| Task | O que faz | Critérios | Depende de | Teste | Gate |
|------|-----------|-----------|------------|-------|------|
| T4 | Expectation que descarta `valor_total` nulo ou negativo e conta o descarte | R2.1 | T2 | `tests/test_qualidade.py`: valor nulo e negativo somem da saída; no target dev, o event log do update mostra o descarte | `pytest tests/test_qualidade.py` |
| T5 | Janela de atraso: evento do dia anterior até 02h entra na carga das 05h | R2.2 | T2 | `tests/test_janela.py`: evento das 01h59 entra, o das 02h01 fica para o dia seguinte | `pytest tests/test_janela.py` |
| T6 | Agenda a carga às 05h (America/Sao_Paulo) e confere o horário de fim | R2.3 | T1, T4, T5 | Query no event log do target dev: o update das 05h termina antes das 06h30 | `databricks bundle validate` |

---

## Aprovação

**Aprovado**: 2026-11-02 — v1.0 — usuário: "plano aprovado, pode criar no Jira"

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-11-02 | Versão inicial |
