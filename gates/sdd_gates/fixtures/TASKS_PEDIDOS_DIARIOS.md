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

## Matriz de testes

| Camada | Teste | Profundidade | Onde | Nível |
|--------|-------|--------------|------|-------|
| Regras de pedidos (dedup, janela de atraso) | Unitário em memória, `assertDataFrameEqual` | Cada critério de regra, 1:1, mais empate e reprocessamento | `tests/unit/` | rápido |
| Pipeline Lakeflow (expectation, horário) | Integração no target `dev`: update do pipeline + event log | Cada expectation e o horário que os critérios citam | `tests/integracao/` | completo |
| Recurso do bundle | Sem teste próprio: `databricks bundle validate` | — | — | build |

## Gates

| Nível | Quando usar | Comando |
|-------|-------------|---------|
| rápido | Task com teste unitário | `python3 -m pytest tests/unit -q -p no:cacheprovider` |
| completo | Task com integração no `dev` | `python3 -m pytest tests/unit tests/integracao -q -p no:cacheprovider` |
| build | Última task de cada história; task só de configuração | `databricks bundle validate -t dev`; `python3 -m pytest tests -q -p no:cacheprovider` |

---

## Histórias

### H1: Finanças lê a silver sem duplicados — 5 pontos

**Como** Finanças, **quero** uma linha por pedido em `silver.pedidos`, **para** fechar a receita sem corrigir duplicados à mão.

**Jira:** DADOS-413

| Task | O que faz | Critérios | Depende de | Teste | Gate |
|------|-----------|-----------|------------|-------|------|
| T1 | Declara o pipeline `pedidos` no bundle, serverless e sem schedule | — | — | — | build |
| T2 | Mantém o evento de maior `atualizado_em` por `pedido_id` | R1.1, R1.2 | T1 | `tests/unit/test_dedup.py`: dois eventos do mesmo pedido → fica o mais recente, uma linha por pedido (`assertDataFrameEqual`) | rápido |
| T3 | Garante que reprocessar a mesma partição não muda a contagem | R1.3 | T2 | `tests/unit/test_dedup.py::test_r1_3_reprocessa_mesma_particao` | build |

### H2: A carga das 05h chega validada antes das 06h30 — 3 pontos

**Como** Finanças, **quero** a carga das 05h validada e pronta às 06h30, **para** fechar a receita às 7h com dado confiável.

**Jira:** DADOS-414

| Task | O que faz | Critérios | Depende de | Teste | Gate |
|------|-----------|-----------|------------|-------|------|
| T4 | Expectation que descarta `valor_total` nulo ou negativo e conta o descarte | R2.1 | T2 | `tests/integracao/test_qualidade.py`: no target `dev`, o event log do update mostra o descarte | completo |
| T5 | Janela de atraso: evento do dia anterior até 02h entra na carga das 05h | R2.2 | T2 | `tests/unit/test_janela.py`: evento das 01h59 entra, o das 02h01 fica para o dia seguinte | rápido |
| T6 | Agenda a carga às 05h (America/Sao_Paulo) e confere o horário de fim | R2.3 | T1, T4, T5 | Query no event log do target `dev`: o update das 05h termina antes das 06h30 | build |

---

## Provas

**Build**: nenhum — fixture do selftest; num projeto real, os comandos de build, lint e `databricks bundle validate`
**Run unit**: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/unit -v -p no:cacheprovider`

**P1** — Dois eventos do mesmo `pedido_id` viram uma linha, a de maior `atualizado_em` (R1.1)
Prova: run unit | tests/unit/test_dedup.py::test_r1_1_fica_o_evento_mais_recente PASSED

**P2** — `silver.pedidos` tem no máximo uma linha por `pedido_id` (R1.2)
Prova: run unit | tests/unit/test_dedup.py::test_r1_2_uma_linha_por_pedido PASSED

**P3** — Rodar duas vezes sobre a mesma partição deixa a mesma contagem (R1.3)
Prova: run unit | tests/unit/test_dedup.py::test_r1_3_reprocessa_mesma_particao PASSED

**P4** — `valor_total` nulo ou negativo some da silver, e o event log do update no `dev` conta o descarte (R2.1)
Prova: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/integracao/test_qualidade.py -q -p no:cacheprovider`

**P5** — Evento do dia anterior com `atualizado_em` 01h59 entra na carga das 05h; o das 02h01, não (R2.2)
Prova: run unit | tests/unit/test_janela.py::test_r2_2_ate_02h_entra_na_carga PASSED

**P6** — O update das 05h no `dev` termina antes das 06h30 (America/Sao_Paulo) (R2.3)
Prova: `python3 tests/integracao/confere_horario.py --target dev --ate 06:30`

---

## Aprovação

**Aprovado**: 2026-11-02 — v1.0 — usuário: "plano aprovado, pode criar no Jira"

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-11-02 | Versão inicial |
