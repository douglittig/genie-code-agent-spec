# BUILD REPORT: {Feature Name}

> Relatório de implementação para {Feature Name}

## Metadata

| Atributo | Valor |
|----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Data** | {YYYY-MM-DD} |
| **Autor** | sdd-build |
| **DEFINE** | `docs/specs/DEFINE_{FEATURE}.md` |
| **DESIGN** | `docs/designs/DESIGN_{FEATURE}.md` |
| **Status** | Em Andamento / Completo / Bloqueado |

---

## Resumo

| Métrica | Valor |
|---------|-------|
| **Tarefas Concluídas** | {X}/{Y} |
| **Arquivos Criados** | {N} |
| **Linhas de Código** | {N} |
| **Tempo de Build** | {Duração} |
| **Testes Passando** | {X}/{Y} |
| **Agentes Utilizados** | {N} |

---

## Execução de Tarefas com Atribuição de Agente

| # | Tarefa | Agente | Status | Duração | Notas |
|---|--------|--------|--------|---------|-------|
| 1 | {Descrição da tarefa} | @{nome-do-agente} | ✅ Completo | {Xm} | {Quaisquer notas} |
| 2 | {Descrição da tarefa} | @{nome-do-agente} | ✅ Completo | {Xm} | {Quaisquer notas} |
| 3 | {Descrição da tarefa} | (direto) | 🔄 Em Andamento | - | {Nenhum especialista encontrado} |
| 4 | {Descrição da tarefa} | @{nome-do-agente} | ⏳ Pendente | - | - |

**Legenda:** ✅ Completo | 🔄 Em Andamento | ⏳ Pendente | ❌ Bloqueado

**Chave de Agentes:**
- `@{nome-do-agente}` = Delegado ao agente especialista
- `(direto)` = Construído diretamente pelo sdd-build (nenhum especialista encontrado)

---

## Contribuições dos Agentes

| Agente | Arquivos | Especialização Aplicada |
|--------|----------|------------------------|
| @{agente-1} | {N} | {Quais padrões/KB usados} |
| @{agente-2} | {N} | {Quais padrões/KB usados} |
| (direto) | {N} | Apenas padrões do DESIGN |

---

## Arquivos Criados

| Arquivo | Linhas | Agente | Verificado | Notas |
|---------|--------|--------|------------|-------|
| `{caminho/para/arquivo1.py}` | {N} | @{nome-do-agente} | ✅ | {Quaisquer notas} |
| `{caminho/para/arquivo2.py}` | {N} | @{nome-do-agente} | ✅ | {Quaisquer notas} |
| `{caminho/para/config.yaml}` | {N} | (direto) | ✅ | {Quaisquer notas} |

---

## Resultados de Verificação

### Lint Check

```text
{Output do linter (ex., ruff, eslint) ou "Todas as verificações passaram"}
```

**Status:** ✅ Passou / ❌ Falhou

### Type Check

```text
{Output do verificador de tipos (ex., mypy, tsc) ou "Todas as verificações passaram" ou "N/A — não configurado"}
```

**Status:** ✅ Passou / ❌ Falhou / ⏭️ Pulado

### Testes

```text
{Output do test runner (ex., pytest, jest) ou resumo}
```

| Teste | Resultado |
|-------|-----------|
| `test_funcao_1` | ✅ Passou |
| `test_funcao_2` | ✅ Passou |
| `test_integration` | ✅ Passou |

**Status:** ✅ {X}/{Y} Passaram | ❌ {N} Falharam

---

## Problemas Encontrados

| # | Problema | Resolução | Impacto no Prazo |
|---|----------|-----------|-----------------|
| 1 | {Descrição do problema} | {Como foi resolvido} | {+Xm} |
| 2 | {Descrição do problema} | {Como foi resolvido} | {+Xm} |

---

## Desvios do Design

| Desvio | Motivo | Impacto |
|--------|--------|---------|
| {O que mudou do DESIGN} | {Por que mudou} | {Efeito no sistema} |

---

## Bloqueadores (se houver)

| Bloqueador | Ação Necessária | Responsável |
|------------|-----------------|-------------|
| {Descrição} | {O que precisa acontecer} | {Quem pode desbloquear} |

---

## Verificação dos Acceptance Tests

| ID | Cenário | Status | Evidência |
|----|---------|--------|-----------|
| AT-001 | {Do DEFINE} | ✅ Passou / ❌ Falhou | {Como foi verificado} |
| AT-002 | {Do DEFINE} | ✅ Passou / ❌ Falhou | {Como foi verificado} |
| AT-003 | {Do DEFINE} | ✅ Passou / ❌ Falhou | {Como foi verificado} |

---

## Notas de Performance

| Métrica | Esperado | Medido | Status |
|---------|----------|--------|--------|
| {Métrica 1} | {Do DEFINE} | {Medido} | ✅ / ❌ |
| {Métrica 2} | {Do DEFINE} | {Medido} | ✅ / ❌ |

---

## Resultados de Qualidade de Dados (se aplicável)

> Inclua esta seção quando o build envolver pipelines de dados, modelos dbt ou infraestrutura de dados.

### Resultados do dbt Build

```text
{Output do `dbt build --select {modelos}` ou "N/A"}
```

**Status:** ✅ Passou / ❌ Falhou

### Resultados do SQL Lint

```text
{Output do `sqlfluff lint` ou "N/A"}
```

**Status:** ✅ Passou ({N} arquivos limpos) / ❌ {N} violações

### Verificações de Qualidade de Dados

| Verificação | Ferramenta | Resultado | Detalhes |
|-------------|------------|-----------|---------|
| {Verificação de null em PKs} | {dbt test / GE} | ✅ / ❌ | {0 nulls encontrados} |
| {Verificação de unicidade de PK} | {dbt test / GE} | ✅ / ❌ | {0 duplicatas} |
| {Integridade referencial} | {dbt test / GE} | ✅ / ❌ | {0 órfãos} |
| {Sanidade de contagem de linhas} | {dbt test / GE} | ✅ / ❌ | {N linhas, dentro do intervalo} |
| {Freshness} | {dbt source freshness} | ✅ / ❌ | {Última atualização: HH:MM} |

### Métricas do Pipeline

| Métrica | Valor |
|---------|-------|
| Modelos construídos | {N} |
| Testes passando | {X}/{Y} |
| Violações de SQL lint | {N} |
| Tempo médio de build por modelo | {X}s |
| Freshness dos dados | {Dentro do SLA / Excedido} |

---

## Status Final

### Geral: {✅ COMPLETO / 🔄 EM ANDAMENTO / ❌ BLOQUEADO}

**Checklist de Conclusão:**

- [ ] Todas as tarefas do manifest concluídas
- [ ] Todas as verificações passaram
- [ ] Todos os testes passaram
- [ ] Sem problemas bloqueadores
- [ ] Acceptance tests verificados
- [ ] Pronto para Ship

---

## Próximo Passo

**Se Completo:** Ship (`@sdd-ship`) — a partir de `BUILD_REPORT_{FEATURE_NAME}.md`

**Se Bloqueado:** Resolver bloqueadores, depois retomar o Build

**Se Problemas Encontrados:** Iterate em `DESIGN_{FEATURE}.md` com a mudança necessária
