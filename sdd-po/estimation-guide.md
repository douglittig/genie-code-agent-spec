# Estimation Guide — Calibração Fibonacci do Time

> **Preencher antes de usar.** Este guia calibra como o time traduz complexidade em pontos.
> Sem calibração, pontos viram números sem significado. O `sdd-po` lê este arquivo na
> Capacidade 2 (Estimativa Fibonacci).

---

## Escala

Use **apenas** valores Fibonacci: `1, 2, 3, 5, 8, 13`. Quanto maior, maior a incerteza embutida.
**Story > 13 → quebrar.** Não cabe numa sprint e esconde risco.

---

## Âncoras de Referência (exemplos — ajustar ao seu time)

| Pontos | Significado | Exemplo de referência (data engineering) |
|--------|-------------|--------------------------------------------|
| **1** | Trivial, sem incerteza | Adicionar uma coluna derivada simples num modelo existente |
| **2** | Pequeno, caminho conhecido | Nova tabela silver a partir de uma bronze já existente |
| **3** | Médio, algum trabalho | Pipeline bronze→silver para uma fonte nova já mapeada |
| **5** | Considerável, partes móveis | Ingestão de fonte nova (Auto Loader) + contrato de schema + testes |
| **8** | Grande, incerteza relevante | Camada gold com agregações por sessão + SLA de freshness |
| **13** | Muito grande — candidato a quebrar | Pipeline ponta a ponta nova com governança/PII e múltiplas fontes |

---

## Fatores que Puxam a Estimativa para Cima

| Fator | Sinal no DEFINE/ADR |
|-------|---------------------|
| Incerteza técnica | ADR marcou a decisão com confiança baixa / sem precedente |
| Governança / PII | DEFINE/ADR exigem mascaramento, row/column security |
| Volume / performance | SLAs de freshness apertados, grandes volumes |
| Integrações externas | Dependência de sistema/fonte fora do controle do time |
| Evolução de schema | Contratos que mudam, rescue columns, merge schema |

---

## Definition of Ready (uma Story pode ser estimada quando…)

```text
[ ] A Story é uma fatia vertical (entrega valor observável)
[ ] Tem critérios de aceite vindos dos acceptance tests do DEFINE
[ ] A unidade deployável correspondente no ADR está clara
[ ] As dependências externas estão identificadas
```

---

## Definition of Done (referência para o time — usada no Build/Ship)

```text
[ ] Código implementado conforme o DESIGN
[ ] Testes (unit + qualidade de dados) passando
[ ] Sem credenciais hardcoded
[ ] Acceptance tests do DEFINE verificados
[ ] Ticket atualizado pelo sdd-doc
```

> **Times diferentes calibram diferente.** Ajuste as âncoras acima após algumas sprints para que os
> pontos reflitam a realidade do seu time — é isso que torna a velocity comparável entre features.
