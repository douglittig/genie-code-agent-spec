# ADR: {Nome da Feature}

> **Architecture Decision Record** — documento vinculante para o design e build desta feature.
> Gerado pelo `@custom-staff-engineer` na Fase 2 do fluxo de desenvolvimento.

## Metadata

| Atributo | Valor |
|----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Data** | {YYYY-MM-DD} |
| **Autor** | {autor} |
| **Status** | Proposto / Aceito / Revisado / Obsoleto |
| **DEFINE de origem** | `docs/specs/DEFINE_{FEATURE}.md` |
| **Próximo passo** | `@custom-sdd-workflow design` (doc-agent documenta este ADR no Jira) |

---

## Contexto

{Resumo do problema técnico a resolver. O que a spec pede, quais são as restrições do ambiente Databricks e do time, e por que as decisões abaixo foram necessárias.}

---

## Decisões

### Processamento
| Atributo | Valor |
|----------|-------|
| **Decisão** | {DLT/SDP / Structured Streaming / Batch Jobs} |
| **Racional** | {por que esta escolha para este caso} |
| **Descartado** | {o que foi considerado e rejeitado, com motivo} |

### Arquitetura de Camadas
| Atributo | Valor |
|----------|-------|
| **Decisão** | {Medallion Bronze/Silver/Gold / outra estrutura} |
| **Camadas** | {nomes e responsabilidades de cada camada} |
| **Racional** | {por que esta estrutura} |

### Ingestão
| Atributo | Valor |
|----------|-------|
| **Decisão** | {Auto Loader / Zerobus / JDBC / API / outro} |
| **Racional** | {frequência, volume, fonte, SLA} |

### Serving
| Atributo | Valor |
|----------|-------|
| **Decisão** | {DBSQL / Genie Space / Model Serving / API REST} |
| **Racional** | {quem consome, latência esperada, volume} |

### Governança e PII
| Campo | Classificação | Tratamento |
|-------|--------------|------------|
| {campo_1} | PII / Sensível / Público | {mascarar / tokenizar / restringir acesso} |
| {campo_2} | PII / Sensível / Público | {mascarar / tokenizar / restringir acesso} |

**Controle de acesso:** {row-level security / column masking / permissões UC}
**Auditoria:** {system tables a monitorar}

### Evolução de Schema
| Atributo | Valor |
|----------|-------|
| **Estratégia** | {rescue column / merge schema / schema enforcement} |
| **Contrato** | {quem é dono do schema, quem pode quebrar} |

### Confiabilidade
| Atributo | Valor |
|----------|-------|
| **Idempotência** | {como garantir execução repetível} |
| **Retry** | {política de retry, max tentativas} |
| **Dead letter** | {o que fazer com registros inválidos} |
| **Alertas** | {o que monitorar, quem notificar} |

### Custo e Compute
| Atributo | Valor |
|----------|-------|
| **Compute** | {Serverless / cluster dedicado / SQL Warehouse} |
| **Sizing** | {DBUs estimados, justificativa} |
| **Otimização** | {particionamento, liquid clustering, z-order} |

### Deploy e Ambientes
| Atributo | Valor |
|----------|-------|
| **Ferramenta** | {DABs / outro} |
| **Ambientes** | {dev / stg / prod — configurações distintas} |
| **Secrets** | {como gerenciar credenciais por ambiente} |

### Estratégia de Testes
| Tipo | O que cobrir |
|------|-------------|
| **Unitário** | {funções de transformação, lógica de negócio} |
| **Integração** | {pipeline end-to-end, schema validation} |
| **Dados** | {data quality checks, expectativas DLT} |

---

## Alternativas Descartadas

| Opção | Área | Motivo da rejeição |
|-------|------|--------------------|
| {opção A} | {processamento} | {custo, complexidade, SLA} |
| {opção B} | {serving} | {não atende latência exigida} |

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| {risco 1} | Alta / Média / Baixa | Alto / Médio / Baixo | {ação concreta} |
| {risco 2} | Alta / Média / Baixa | Alto / Médio / Baixo | {ação concreta} |

---

## Restrições Vinculantes para o Design

> O `design-agent` **não pode** alterar as decisões abaixo sem um novo ADR aprovado.

- {restrição 1 — ex: "Usar exclusivamente DLT para o pipeline de ingestão"}
- {restrição 2 — ex: "Campo CPF deve ser mascarado em todas as camadas Silver e Gold"}
- {restrição 3 — ex: "Deploy via DABs com targets dev/stg/prod obrigatórios"}

---

## Skills Databricks Aprovadas para este Feature

| Skill | Uso |
|-------|-----|
| `@databricks-spark-declarative-pipelines` | {pipeline principal} |
| `@databricks-unity-catalog` | {governança e permissões} |
| `@databricks-bundles` | {deploy multi-ambiente} |

## Skills Databricks Descartadas

| Skill | Motivo |
|-------|--------|
| `@databricks-spark-structured-streaming` | {DLT cobre o caso com menos complexidade} |
