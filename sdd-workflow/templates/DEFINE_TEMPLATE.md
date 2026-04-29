# DEFINE: {Feature Name}

> Descrição em uma frase do que estamos construindo

## Metadata

| Atributo | Valor |
|----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Data** | {YYYY-MM-DD} |
| **Autor** | {autor} |
| **Status** | {Rascunho / Em Andamento / Precisa de Esclarecimento / Pronto para Design} |
| **Clarity Score** | {X}/15 |

---

## Problem Statement

{1-2 frases descrevendo o problema que estamos resolvendo. Seja específico sobre quem tem o problema e qual é o impacto.}

---

## Usuários-Alvo

| Usuário | Função | Pain Point |
|---------|--------|------------|
| {Usuário 1} | {Função} | {O que os frustra} |
| {Usuário 2} | {Função} | {O que os frustra} |

---

## Goals

Como fica o sucesso (priorizado):

| Prioridade | Goal |
|------------|------|
| **MUST** | {Goal primário - não negociável para o MVP} |
| **MUST** | {Outro goal crítico} |
| **SHOULD** | {Importante mas pode ser adiado se prazo for apertado} |
| **COULD** | {Nice-to-have se houver tempo} |

**Guia de Prioridade:**
- **MUST** = MVP falha sem isso
- **SHOULD** = Importante, mas existe workaround
- **COULD** = Nice-to-have, cortar primeiro se necessário

---

## Critérios de Sucesso

Resultados mensuráveis (devem incluir números):

- [ ] {Métrica 1: ex., "Suportar 1000 requisições por minuto"}
- [ ] {Métrica 2: ex., "Atingir 99,9% de uptime"}
- [ ] {Métrica 3: ex., "Tempo de resposta abaixo de 200ms"}

---

## Acceptance Tests

| ID | Cenário | Given | When | Then |
|----|---------|-------|------|------|
| AT-001 | {Happy path} | {Estado inicial} | {Ação} | {Resultado esperado} |
| AT-002 | {Caso de erro} | {Estado inicial} | {Ação} | {Resultado esperado} |
| AT-003 | {Edge case} | {Estado inicial} | {Ação} | {Resultado esperado} |

---

## Fora do Escopo

Explicitamente NÃO incluído nesta feature:

- {Item 1: O que NÃO estamos fazendo}
- {Item 2: O que está adiado para o futuro}
- {Item 3: O que está explicitamente excluído}

---

## Restrições

| Tipo | Restrição | Impacto |
|------|-----------|---------|
| Técnica | {ex., "Deve usar o schema de banco de dados existente"} | {Como isso afeta o design} |
| Prazo | {ex., "Deve ser entregue no Q1"} | {Como isso afeta o escopo} |
| Recurso | {ex., "Sem budget adicional de infraestrutura"} | {Como isso afeta a abordagem} |

---

## Contexto Técnico

> Contexto essencial para a fase de Design — previne arquivos mal posicionados e necessidades de infraestrutura ignoradas.

| Aspecto | Valor | Notas |
|---------|-------|-------|
| **Localização do Deploy** | {src/ \| functions/ \| gen/ \| deploy/ \| caminho customizado} | {Por que esta localização} |
| **Skills Databricks** | {Lista de domains relevantes para esta feature} | {Quais padrões consultar} |
| **Impacto IaC** | {Novos recursos \| Modificar existentes \| Nenhum \| A definir} | {Mudanças de infraestrutura necessárias} |

**Por que isso importa:**

- **Localização** → A fase de Design usa a estrutura correta do projeto, evita arquivos mal posicionados
- **Skills Databricks** → A fase de Design usa os padrões corretos
- **Impacto IaC** → Dispara planejamento de infraestrutura, evita falhas "funciona localmente"

---

## Data Contract (se aplicável)

> Inclua esta seção quando a feature envolver pipelines de dados, ETL ou analytics.

### Inventário de Origens
| Origem | Tipo | Volume | Freshness | Dono |
|--------|------|--------|-----------|------|
| {origem_1} | {Postgres / Kafka / S3 / API} | {~linhas/dia} | {SLA} | {Time} |

### Contrato de Schema
| Coluna | Tipo | Restrições | PII? |
|--------|------|------------|------|
| {coluna_1} | {INT / VARCHAR / DECIMAL} | {NOT NULL, UNIQUE} | {Sim/Não} |

### SLAs de Freshness
| Camada | Meta | Medição |
|--------|------|---------|
| Raw / Staging | {Dentro de X minutos após mudança na origem} | {Comparação de timestamp} |
| Marts | {Atualizado até HH:MM UTC diariamente} | {Tempo de conclusão do DAG} |

### Métricas de Completude
- {ex., 99,9% dos registros da origem presentes dentro do SLA}
- {ex., Zero chaves primárias nulas em todos os modelos}

### Requisitos de Lineage
- {ex., Lineage em nível de coluna da origem ao mart}
- {ex., Análise de impacto antes de mudanças no schema}

---

## Premissas

Premissas que, se erradas, poderiam invalidar o design:

| ID | Premissa | Se Errada, Impacto | Validada? |
|----|----------|--------------------|-----------|
| A-001 | {ex., "O banco de dados suporta a carga esperada"} | {Precisaria de camada de cache} | [ ] |
| A-002 | {ex., "Volume de requisições fica abaixo de 1000/hora"} | {Precisaria de rate limiting} | [ ] |
| A-003 | {ex., "Usuários têm navegadores modernos"} | {Precisaria de polyfills para suporte legado} | [ ] |

**Nota:** Valide premissas críticas antes da fase de Design. Premissas não validadas se tornam riscos.

---

## Breakdown do Clarity Score

| Elemento | Pontuação (0-3) | Notas |
|----------|-----------------|-------|
| Problema | {0-3} | {Por que esta pontuação} |
| Usuários | {0-3} | {Por que esta pontuação} |
| Goals | {0-3} | {Por que esta pontuação} |
| Sucesso | {0-3} | {Por que esta pontuação} |
| Escopo | {0-3} | {Por que esta pontuação} |
| **Total** | **{X}/15** | |

**Guia de Pontuação:**
- 0 = Completamente ausente
- 1 = Vago ou incompleto
- 2 = Claro mas faltam detalhes
- 3 = Crystal clear, acionável

**Mínimo para prosseguir: 12/15**

---

## Questões em Aberto

{Liste quaisquer questões pendentes que precisam de resposta antes da fase de Design. Se não houver, declare "Nenhuma — pronto para o Design."}

---

## Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|---------|
| 1.0 | {YYYY-MM-DD} | define-agent | Versão inicial |

---

## Próximo Passo

**Pronto para:** Design — `DEFINE_{FEATURE_NAME}.md`
