# Databricks Genie Code — Visão Geral Detalhada

> **Fontes:** [Blog de lançamento](https://www.databricks.com/blog/introducing-genie-code) (Patrick Wendell, Matei Zaharia, Weston Hutchins, Gal Oshri — 11 de março de 2026) · [Documentação Genie Code](https://docs.databricks.com/aws/en/genie-code/) · [DE Agent](https://docs.databricks.com/aws/en/ldp/de-agent)

---

## O que é o Genie Code?

Genie Code é o **agente de IA autônomo da Databricks para equipes de dados**, anunciado em 11 de março de 2026 como o mais novo membro da família Genie. Ele traz para times de dados a mesma transformação que ferramentas agênticas de código trouxeram para engenharia de software.

> *"Com Genie Code, equipes de dados deixam de simplesmente 'promptar um copiloto' e passam a **delegar trabalho real**: construir pipelines, depurar falhas, entregar dashboards e manter sistemas em produção — de forma autônoma, de ponta a ponta."*

A premissa central é que **código é apenas um veículo para manipular e compreender dados**. Agentes focados em software frequentemente falham em trabalho com dados porque, em um ecossistema de dados, o contexto está não apenas no script, mas também em padrões de uso, linhagem e semântica de negócio.

---

## Por que agentes genéricos falham com dados?

- **Contexto além do código:** tabelas, linhagem, semântica de negócio e padrões de uso não estão no código-fonte.
- **Stakes altíssimos:** dashboards guiam decisões de negócio, pipelines alimentam sistemas em produção, modelos de ML influenciam resultados do mundo real.
- **Acurácia, reprodutibilidade e governança** são exigências não-negociáveis — a velocidade dos agentes precisa ser acompanhada dessas garantias.

Genie Code resolve isso sendo **construído diretamente sobre o Unity Catalog**, que fornece o contexto completo de dados da organização.

---

## O que o Genie Code faz — visão de alto nível

| Papel | Descrição |
|---|---|
| **Expert ML Engineer** | Workflows end-to-end: planejamento, escrita, deploy de modelos, logging no MLflow, tuning de endpoints |
| **Senior Data Engineer** | Pipelines prontos para produção, diferenciando staging vs. produção, change data capture, data quality expectations |
| **Agente de Observabilidade** | Monitora Lakeflow pipelines e modelos em background, faz triagem de falhas e investiga anomalias |
| **Parceiro de Contexto Empresarial** | Entende semântica de negócio, governance policies e dados de plataformas externas via Unity Catalog |
| **Agente que Evolui** | Aprende com cada interação via persistent memory; atualiza instruções internas automaticamente |

---

## Capacidades Detalhadas

### 1. Treinamento e Avaliação de Modelos de ML

Genie Code age como um **ML engineer dedicado embarcado no seu workflow**. Com um prompt como *"train a forecasting model predicting sales in @sales_table"*, ele executa o pipeline completo:

1. **Identificação e profiling de features**
2. **Divisão correta** de datasets de treino, validação e teste
3. **Treinamento de múltiplos tipos de modelo** com hyperparameter sweeps para encontrar o melhor
4. **Avaliação** em métricas como AUC, F1, RMSE e R²
5. **Geração de plots:** feature importance, confusion matrices, ROC curves
6. **Tracking de experimentos no MLflow**
7. **Recomendações de melhoria** baseadas em diagnósticos do modelo

Após o deploy no **Databricks Model Serving**, o Genie Code permanece no loop: verifica saúde dos endpoints, analisa traces e recomenda otimizações.

> *"Genie Code acelera tudo, desde previsão de séries temporais até deploy em produção, sem sacrificar rigor ou controle."*
> — Emilio Martín Gallardo, Principal Data Scientist, Repsol

---

### 2. Criação de Pipelines de Dados Prontos para Produção

Genie Code é um **engenheiro de dados expert** que projeta como um arquiteto sênior — não como um novato que escreve um script que funciona apenas em dados de teste. Ele leva em conta as diferenças entre ambientes de staging e produção.

**O que ele pode fazer:**

- **Criar pipelines a partir de linguagem natural:** descreva o que precisa e ele gera um Spark Declarative Pipeline completo com ingestão, transformações e data quality expectations embutidas
- **Estender pipelines existentes:** adicionar datasets, modificar transformações, escrever AutoCDC flows, configurar Auto Loader, aplicar data quality expectations — tudo dentro do contexto do pipeline atual
- **Entender comportamento de pipelines:** inspecionar outputs, rastrear fluxo de dados para tabelas downstream, e identificar mudanças inesperadas em row counts ou schemas
- **Arquitetura medallion completa em uma única conversa**, por exemplo:
  - Bronze: `bronze_properties.sql`, `bronze_bookings.sql`, `bronze_reviews.sql`
  - Silver: `silver_bookings.sql` (bookings joined com properties, com data quality expectation `check_out > check_in`)
  - Gold: `gold_property_performance.sql` (agregações por property)
- **Propor multi-file changes com diffs** para revisão antes de confirmar
- **Executar pipelines com safeguards:** arquivos individuais, dry-runs ou full refresh — sempre mediante aprovação do usuário
- **Iterar por falhas** automaticamente até os problemas serem resolvidos

> *"Genie Code nos moveu para além do assisted coding rumo à verdadeira engenharia de dados agêntica. Ele pode analisar nossos pipelines Lakeflow, propor mudanças em múltiplos arquivos com diffs, executar runs com salvaguardas e iterar por falhas até que os problemas sejam resolvidos. Parece menos com autocomplete e mais com um colaborador embarcado no nosso workflow."*
> — Nishit Gajjar, Tech Lead, Global Infrastructure Technology Provider

---

### 3. Dashboards com Definições Semânticas Reutilizáveis

Genie Code pode:
- **Gerar visualizações** com definições semânticas reutilizáveis
- **Configurar filtros, cálculos e layouts multi-página** que escalam à medida que os dashboards crescem
- Conectar definições semânticas a filtros e cálculos de forma consistente, mantendo a equipe rápida sem perder consistência
- Construir dashboards a partir de um **esboço desenhado à mão** (uso real interno da Databricks por Product Managers)

> *"Com Genie Code, nossas equipes entregam analytics com IA e workflows automatizados em semanas, não meses. Low-code agents nos ajudam a avançar mais rápido enquanto permanecemos alinhados à governança, permitindo que equipes de projetos e engenharia obtenham insights em linguagem natural de dados complexos sem desacelerar a entrega."*
> — Russell Singer, Chief Data Architect, Bechtel Corporation

---

### 4. Planejamento e Execução Autônoma Multi-Etapas

Forneça um objetivo de alto nível — como *"Identify flight delay risks and build a monitoring dashboard"* — e o Genie Code:

1. Raciocina sobre os requisitos
2. Formula um **plano multi-etapas detalhado**
3. Executa o plano cruzando **Databricks Notebooks, AI/BI Dashboards e Lakeflow** em um único thread de conversa

---

### 5. Análise Exploratória de Dados com Busca Contextual Profunda

O Genie Code usa **popularidade, linhagem, code samples e metadata do Unity Catalog** para encontrar os datasets mais relevantes para qualquer análise. Essa busca contextual profunda elimina o esforço manual de procurar dados e garante que o trabalho seja baseado nas tabelas mais precisas e frequentemente usadas da organização.

> *"O que estamos vendo na Danfoss é que o Genie Code muda os papéis dentro de um time de dados. Data scientists ainda fornecem direção e revisão, mas engenheiros, analistas e especialistas de domínio agora podem trabalhar ativamente em notebooks com o assistente e contribuir para workflows de analytics avançados. Ele transforma data science em uma atividade muito mais colaborativa."*
> — Radu Dragusin, Principal Engineer, Data & AI, Danfoss

---

### 6. Observabilidade em Produção

Escrever código é apenas o primeiro passo. Mantê-lo é o verdadeiro desafio. O Genie Code integra diretamente com **Databricks Model Serving e MLflow 3.0** para automatizar:

| Capacidade | Descrição |
|---|---|
| **Endpoint health checks** | Relatório completo de status — compute, request handling e server logs — em um único prompt |
| **Agent quality analysis** | Identifica problemas sutis como hallucinations, incorrect tool calls e padrões de frustração de usuários em agent traces complexos em tempo real |
| **Production troubleshooting** | Quando incidentes ocorrem, cruza server logs e métricas para automatizar o primeiro round de diagnóstico e reduzir o time-to-resolution |
| **Endpoint optimization** | Recomendações de provisioned concurrency, hardware configs e auto-scaling baseadas nas melhores práticas da Databricks |

**Exemplo real de health check (endpoint `test-xgboost`):**
- Status: READY, deployed ~30 minutos antes
- CPU e memória: baixíssimos (~0.9% CPU, ~4.5% memória)
- Sem erros de request nas últimas 24 horas
- Recomendação prioritária: aumentar provisioned concurrency de 4 para mínimo de 8 para workloads de produção

---

### 7. Background Agents — Manutenção Proativa (Em Breve)

Genie Code foi projetado para **trabalhar em background**, mantendo os dados saudáveis mesmo depois que você fecha o laptop. Múltiplos agentes podem ser deployados em paralelo para lidar com o trabalho operacional que tipicamente consome a semana de um data engineer.

**Como funcionam:**
- Vão além do suporte reativo para **manutenção proativa**
- Lidam com tarefas repetitivas: responder a falhas de jobs, gerenciar upgrades rotineiros de DBR
- Quando um pipeline quebra, o agente **identifica a causa raiz e sugere um fix apenas após validá-lo em um ambiente sandbox seguro**

**Exemplo concreto:** Se um pipeline de produção falha por schema mismatch — como uma coluna mudando de `INT (150)` para `STRING ("150 USD")` — o Genie Code identifica a falha e automaticamente corrige o pipeline.

---

## Arquitetura Técnica

### Sistema Multi-Modelo

Genie Code **não é alimentado por um único modelo**. É um sistema agêntico que roteia tarefas entre múltiplos modelos e ferramentas, selecionando automaticamente o melhor para cada job:

- Frontier LLMs (modelos de fronteira)
- Modelos open-source
- Modelos customizados hospedados no Databricks

Isso elimina a necessidade de o usuário alternar manualmente entre modelos. A **Databricks Research** afina continuamente o sistema, benchmarking os modelos mais recentes de leading AI labs junto com modelos customizados rodando na plataforma.

### Integração Profunda com APIs Databricks

O Genie Code é profundamente integrado com as **APIs Databricks**, permitindo identificar os assets de dados corretos, montar contexto rico e gerar queries de maior qualidade — o que é fundamentalmente diferente de um agente genérico que simplesmente lê dados de fora.

### Unity Catalog como Fundação

Genie Code leverage o Unity Catalog para **curar automaticamente os dados e conteúdo mais relevantes enquanto você trabalha**. Especificamente, ele:

- Cria **personalized search indexes** (índices de busca personalizados por organização)
- Mantém **custom instructions** atualizadas com base nas interações do time
- Constrói **knowledge stores** (bases de conhecimento internas)
- Extrai **usage patterns from lineage** (padrões de uso a partir da linhagem)
- Fica **mais inteligente quanto mais a equipe o usa**

> *"Esta integração profunda com o Unity Catalog é muito superior a qualquer sistema que simplesmente lê os dados de fora."*

---

## Customização e Extensibilidade

Três formas primárias de estender as capacidades do Genie Code:

### 1. Model Context Protocol (MCP)

Padrão aberto que permite ao Genie Code interagir de forma segura com ferramentas externas, APIs e documentação, habilitando workflows autônomos que se estendem além do workspace Databricks.

**Exemplos:**
- **Jira:** Receber uma task para treinar um novo modelo de ML → Genie Code coleta o contexto da issue, executa a tarefa e atualiza o ticket com os resultados automaticamente
- **Confluence, Google Drive, GitHub, Notion:** referenciar runbooks e data dictionaries específicos da equipe durante troubleshooting

### 2. Agent Skills

Definem **domain-specific capabilities** para ensinar o Genie Code a executar tarefas complexas de forma consistente. Exemplos:

- Forma específica da empresa de fazer **PII masking**
- **Framework customizado** para validação de dados

Skills garantem que a IA siga as melhores práticas da organização toda vez. Seguem o **formato aberto Agent Skills**.

### 3. Persistent Memory

Genie Code fica mais inteligente quanto mais você o usa. Através de persistent memory, o agente:

- Atualiza automaticamente suas instruções internas com base em interações passadas
- Aprende **coding preferences** do usuário
- Lembra **quais datasets são usados com mais frequência**
- **Retém contexto entre sessões**

---

## Governança e Segurança

Genie Code segue as **mesmas regras de segurança e governança** do restante da plataforma Databricks.

| Garantia | Descrição |
|---|---|
| **Access Control Enforcement** | Nunca expõe assets de dados que o usuário não tem permissão para ver |
| **Native Revision History** | Todas as edições são rastreadas pelo sistema de versionamento Databricks; rollback disponível em notebooks, queries, arquivos e pipelines Lakeflow |
| **Built-in Guardrails** | Proativamente solicita confirmação antes de executar código que pode modificar tabelas subjacentes |
| **Comprehensive Audit Logging** | Visibilidade completa de como o Genie Code está sendo usado, via infraestrutura de auditoria existente |
| **Lineage Adherence** | Ao construir pipelines, adere aos controles de acesso e linhagem existentes |

---

## Performance

### Benchmark Interno — Real-World Data Science Tasks

Tarefas coletadas de usuários internos da Databricks:

| Sistema | Taxa de conclusão de tarefas |
|---|---|
| **Genie Code** | **77.1%** |
| Leading Coding Agent + Databricks MCP | 32.1% |

Genie Code supera o competidor por **mais de 2x** em tarefas reais de data science e analytics.

---

## Casos de Uso Internos na Databricks

| Equipe | Uso |
|---|---|
| **Vendas** | Perfil completo de cada cliente antes de reuniões: métricas de consumo, tickets de suporte e interações recentes em segundos |
| **Product Managers** | Dashboards a partir de esboços desenhados à mão |
| **Finanças** | Análise budget-versus-actual e modelagem de ROI avançada |
| **Liderança** | Respostas a perguntas de dados em tempo real durante discussões estratégicas, reduzindo follow-ups e acelerando decisões complexas |

---

## Depoimentos de Clientes

> *"No SiriusXM, Genie Code apoia tudo, desde a criação de notebooks e SQL complexo até o raciocínio sobre relacionamentos entre tabelas e debugging de pipelines. Ele age como um parceiro de desenvolvimento hands-on que ajuda nossas equipes a entregarem trabalho de alta qualidade em menos tempo."*
> — Bernie Graham, Vice President, Data, SiriusXM

> *"Genie Code mudou como nossas equipes de dados operam. Em vez de montar notebooks, pipelines e modelos manualmente, podemos entregar workflows complexos para um parceiro de IA que entende nossos dados, governança, contexto de negócio e bibliotecas internas."*
> — Emilio Martín Gallardo, Principal Data Scientist, Repsol

> *"Estou genuinamente maravilhado. Genie Code parece um vislumbre do futuro de como o trabalho com dados será feito."*
> — Sameer Yasser, Sr. Data Engineer, Sundt Construction

---

## Disponibilidade e Acesso

- **Status:** Generally Available (GA) no workspace Databricks — sem configuração complexa
- **Custo:** Gratuito para todas as capacidades atuais; paga-se apenas pelos recursos de computação. Fair usage limits se aplicam.
- **Onde encontrar:** Painel Genie Code em notebooks, SQL editor e Lakeflow Pipelines editor
- **Pré-requisitos para Agent Mode:**
  - Partner-powered AI features habilitadas na conta e no workspace
  - Workspace em região geográfica suportada (Genie Code é um Designated Service com zonas de residência de dados por Geo)
  - Permissões de usuário respeitam os controles do Unity Catalog

---

## Modo Padrão vs. Modo Agente

| Aspecto | Modo Padrão (Chat) | Modo Agente |
|---|---|---|
| Interação | Chat com sugestões inline, autocomplete, quick fix | Planejamento autônomo multi-etapas |
| Escopo | Arquivo/célula atual | Múltiplos arquivos e recursos |
| Execução | Sugestão ao usuário | Executa após aprovação |
| Recursos extras | Slash commands, natural language filtering, error diagnosis avançado | Data discovery, pipeline execution, iteração automática por erros |
| Aviso | — | Pode gerar e executar código. Revisar sempre antes de confirmar execuções. |

**Fluxo do Agent Mode:**
1. Usuário ativa Agent Mode e submete um prompt
2. Genie Code cria um **plano passo a passo** para a tarefa
3. Solicita aprovação antes de executar código ou atualizar pipelines
4. Pausa para **perguntas de esclarecimento** quando necessário
5. Permite revisão das mudanças antes de prosseguir
6. **Itera automaticamente por falhas** até resolver os problemas

---

## Superfícies de Integração

| Superfície | Capacidades Específicas |
|---|---|
| **Notebooks** | Data science, ML, EDA, inline suggestions, quick fix, error diagnosis |
| **SQL Editor** | Queries, análise ad-hoc, autocomplete Python e SQL |
| **Lakeflow Pipelines Editor** | Agent Mode completo: ETL, pipelines declarativos, diff reviews, execução com safeguards |
| **AI/BI Dashboards** | Geração de visualizações, filtros, layouts multi-página com definições semânticas |
| **Catalog Explorer** | Exploração de dados com linguagem natural, sample data queries |

---

## Referências

- [Genie Code — Documentação](https://docs.databricks.com/aws/en/genie-code/)
- [Data Engineering Agent (DE Agent)](https://docs.databricks.com/aws/en/ldp/de-agent)
- [Blog: Introducing Genie Code](https://www.databricks.com/blog/introducing-genie-code)
