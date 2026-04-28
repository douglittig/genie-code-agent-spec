# DESIGN: {Feature Name}

> Design técnico para implementar {Feature Name}

## Metadata

| Atributo | Valor |
|----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Data** | {YYYY-MM-DD} |
| **Autor** | design-agent |
| **DEFINE** | [DEFINE_{FEATURE}.md](./DEFINE_{FEATURE}.md) |
| **Status** | Rascunho / Pronto para Build |

---

## Visão Geral da Arquitetura

```text
┌─────────────────────────────────────────────────────┐
│                   DIAGRAMA DO SISTEMA                │
├─────────────────────────────────────────────────────┤
│                                                      │
│  {Diagrama ASCII mostrando componentes e fluxo}     │
│                                                      │
│  [Input] → [Componente A] → [Componente B] → [Output]│
│                ↓                 ↓                   │
│           [Storage]         [API Externa]           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Componentes

| Componente | Propósito | Tecnologia |
|------------|-----------|------------|
| {Componente A} | {O que faz} | {Stack tecnológico} |
| {Componente B} | {O que faz} | {Stack tecnológico} |
| {Componente C} | {O que faz} | {Stack tecnológico} |

---

## Decisões Principais

### Decisão 1: {Nome da Decisão}

| Atributo | Valor |
|----------|-------|
| **Status** | Aceita |
| **Data** | {YYYY-MM-DD} |

**Contexto:** {Por que esta decisão foi necessária}

**Escolha:** {O que decidimos fazer}

**Justificativa:** {Por que esta é a escolha certa}

**Alternativas Rejeitadas:**
1. {Opção A} — Rejeitada porque {motivo}
2. {Opção B} — Rejeitada porque {motivo}

**Consequências:**
- {Trade-off que aceitamos}
- {Benefício que obtemos}

---

### Decisão 2: {Nome da Decisão}

{Repita a estrutura acima}

---

## File Manifest

| # | Arquivo | Ação | Propósito | Agente | Dependências |
|---|---------|------|-----------|--------|--------------|
| 1 | `{caminho/para/arquivo.py}` | Criar | {Propósito} | @{nome-do-agente} | Nenhuma |
| 2 | `{caminho/para/config.yaml}` | Criar | {Propósito} | @{nome-do-agente} | Nenhuma |
| 3 | `{caminho/para/handler.py}` | Criar | {Propósito} | @{nome-do-agente} | 1, 2 |
| 4 | `{caminho/para/test.py}` | Criar | {Propósito} | @{nome-do-agente} | 3 |

**Total de Arquivos:** {N}

---

## Justificativa de Atribuição de Agente

> Agentes disponíveis no diretório `agents/` desta skill — a fase de Build invoca os especialistas correspondentes.

| Agente | Arquivos Atribuídos | Por que Este Agente |
|--------|--------------------|--------------------|
| @{agente-1} | 1, 3 | {Match de especialização: ex., "padrões de roteamento de API"} |
| @{agente-2} | 2 | {Match de especialização: ex., "modelos de validação de dados"} |
| @{agente-3} | 4 | {Match de especialização: ex., "fixtures de teste"} |
| (geral) | {se houver} | {Nenhum especialista encontrado — Build trata diretamente} |

**Descoberta de Agentes:**
- Escaneado: `agents/**/*.md`
- Correspondido por: Tipo de arquivo, palavras-chave de propósito, padrões de caminho, KB domains

---

## Padrões de Código

### Padrão 1: {Nome do Padrão}

```python
# {Breve descrição de quando usar este padrão}

{Snippet de código pronto para copiar e colar}
```

### Padrão 2: {Nome do Padrão}

```python
{Snippet de código pronto para copiar e colar}
```

### Padrão 3: Estrutura de Configuração

```yaml
# estrutura do config.yaml
{Template de configuração YAML}
```

---

## Fluxo de Dados

```text
1. {Passo 1: ex., "Usuário submete requisição via API"}
   │
   ▼
2. {Passo 2: ex., "Requisição validada e enfileirada"}
   │
   ▼
3. {Passo 3: ex., "Worker em background processa a requisição"}
   │
   ▼
4. {Passo 4: ex., "Resultados armazenados no banco de dados"}
```

---

## Pontos de Integração

| Sistema Externo | Tipo de Integração | Autenticação |
|-----------------|-------------------|--------------|
| {Sistema A} | {REST API / SDK / Queue} | {Método} |
| {Sistema B} | {REST API / SDK / Queue} | {Método} |

---

## Estratégia de Testes

| Tipo de Teste | Escopo | Arquivos | Ferramentas | Meta de Cobertura |
|---------------|--------|----------|-------------|-------------------|
| Unitário | Funções | `{arquivos de teste}` | {framework de teste} | 80% |
| Integração | Chamadas de API | `{arquivos de integração}` | {framework + mocks} | Caminhos principais |
| E2E | Fluxo completo | Manual | - | Happy path |

---

## Tratamento de Erros

| Tipo de Erro | Estratégia de Tratamento | Retry? |
|--------------|--------------------------|--------|
| {Erro A} | {Como tratar} | Sim/Não |
| {Erro B} | {Como tratar} | Sim/Não |
| {Erro C} | {Como tratar} | Sim/Não |

---

## Configuração

| Chave de Config | Tipo | Padrão | Descrição |
|-----------------|------|--------|-----------|
| `{chave_1}` | string | `{padrão}` | {O que controla} |
| `{chave_2}` | int | `{padrão}` | {O que controla} |
| `{chave_3}` | bool | `{padrão}` | {O que controla} |

---

## Considerações de Segurança

- {Consideração de segurança 1}
- {Consideração de segurança 2}
- {Consideração de segurança 3}

---

## Observabilidade

| Aspecto | Implementação |
|---------|---------------|
| Logging | {Abordagem: ex., "Logging estruturado em JSON"} |
| Métricas | {Abordagem: ex., "Métricas customizadas via serviço de monitoramento"} |
| Tracing | {Abordagem: ex., "Spans OpenTelemetry"} |

---

## Arquitetura de Pipeline (se aplicável)

> Inclua esta seção quando a feature envolver pipelines de dados, ETL ou analytics.

### Diagrama DAG

```text
[Origem A] ──extrai──→ [Camada Raw] ──transforma──→ [Staging] ──modela──→ [Marts]
[Origem B] ──extrai──↗       ↓                          ↓              ↓
                         [Arquivo]            [Gate de Qualidade]  [Dashboard]
```

### Estratégia de Particionamento

| Tabela | Chave de Partição | Granularidade | Justificativa |
|--------|------------------|---------------|---------------|
| {tabela_1} | {coluna} | {diária / mensal} | {Padrões de consulta, volume} |

### Estratégia Incremental

| Modelo | Estratégia | Coluna-Chave | Lookback |
|--------|------------|--------------|----------|
| {modelo_1} | {incremental_by_time / unique_key / full_refresh} | {coluna} | {N dias} |

### Plano de Evolução do Schema

| Tipo de Mudança | Tratamento | Rollback |
|-----------------|------------|----------|
| Nova coluna | {Adicionar com DEFAULT, backfill assíncrono} | {Dropar coluna} |
| Mudança de tipo | {Período de dual-write, depois migrar} | {Reverter tipo} |
| Remoção de coluna | {Deprecar no contrato, remover após N dias} | {Re-adicionar coluna} |

### Gates de Qualidade de Dados

| Gate | Ferramenta | Threshold | Ação em Caso de Falha |
|------|------------|-----------|----------------------|
| {Verificação de null em PKs} | {dbt test / GE} | {0 nulls} | {Bloquear pipeline} |
| {Delta de contagem de linhas} | {dbt test / GE} | {<10% variação} | {Alertar + continuar} |
| {Verificação de freshness} | {dbt source freshness} | {< N horas} | {Alertar} |

---

## Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|---------|
| 1.0 | {YYYY-MM-DD} | design-agent | Versão inicial |

---

## Próximo Passo

**Pronto para:** Build — `DESIGN_{FEATURE_NAME}.md`
