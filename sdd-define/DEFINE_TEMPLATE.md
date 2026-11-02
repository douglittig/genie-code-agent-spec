# DEFINE: {Nome da feature}

> {Uma frase: o que esta feature entrega e para quem.}

<!-- Preencha tudo; o gate `python3 -m sdd_gates define` avisa sobre qualquer {placeholder} que sobrar.
     Seções marcadas (opcional) podem sair inteiras quando não se aplicam. -->

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | {FEATURE_NAME} |
| **Tamanho** | {Médio \| Grande \| Complexo} — {motivo em uma linha} |
| **Jira** | {PROJ-123 \| pendente} |
| **Data** | {AAAA-MM-DD} |
| **Status** | {Rascunho \| Aguardando aprovação \| Aprovado} |

---

## Fontes

| Fonte | Link | O que foi usado |
|-------|------|-----------------|
| {Confluence: nome da página \| Pedido do usuário \| Ticket} | {url \| n/a} | {seções lidas} |

---

## Registro do pedido e das respostas

<!-- Gravado ANTES de perguntar, e atualizado a cada resposta no mesmo turno: o chat não sobrevive
     a uma sessão nova. Transcrição literal. Os IDs Qn.m (n = rodada) são a origem na Rastreabilidade,
     nas Suposições e na rubrica. Pergunta ainda sem resposta: escreva "aguardando". -->

### Pedido original

> "{o pedido do usuário, literal, como chegou}"

### Rodada 1

| ID | Pergunta, com a recomendação | Resposta do usuário |
|----|------------------------------|---------------------|
| Q1.1 | {pergunta, com a sua recomendação} | "{resposta literal \| aguardando}" |

---

## Problema

<!-- Vem do usuário (cite Qn.m) ou vira pergunta. Não preencha com o que parece plausível. -->

{Quem tem o problema, qual é e o que custa hoje. Duas frases no máximo.}

## Quem usa o dado

<!-- Vem do usuário (cite Qn.m). Não perguntado: "não informado" + pergunta em aberto. -->

| Quem | Para quê | Dor hoje |
|------|----------|----------|
| {time ou sistema consumidor} | {decisão ou processo que depende do dado} | {o que falta ou dá errado} |

---

## Escopo

### Dentro do escopo

- {o que esta feature entrega}

### Fora do escopo

- {o que fica de fora, de propósito — nunca deixe vazio}

---

## Requisitos

<!-- Um requisito por história de uso. Prioridade: P1 = sem isso não entrega (MVP); P2 = importante;
     P3 = se der tempo. Critérios no formato EARS (ver @sdd-define), com ID R<n>.<m>. -->

### R1: {título do requisito} — P1

**Por quê:** {o valor para quem usa}

**Critérios de aceite (EARS):**

- **R1.1** QUANDO {gatilho} ENTÃO o {pipeline} DEVE {resultado verificável}.
- **R1.2** SE {condição indesejada} ENTÃO o {pipeline} DEVE {reação verificável}.

---

## Requisitos implícitos de dados

<!-- Cada dimensão termina em um lugar: um critério (R1.2), "fora do escopo", uma suposição (S-1),
     uma decisão do usuário que não vira critério ("decidido em Q2.3: serverless") ou
     "não se aplica: <motivo>". Antes da aprovação, "pergunta em aberto n" vale como destino
     provisório; com --aprovado, não. Nenhuma linha fica sem destino. -->

| Dimensão | Como fica nesta feature |
|----------|-------------------------|
| Idempotência e reprocessamento | {R?.? \| fora do escopo \| S-? \| não se aplica: motivo} |
| Dado atrasado ou fora de ordem | {…} |
| Duplicidade | {…} |
| Evolução de schema | {…} |
| Backfill e carga histórica | {…} |
| Qualidade (nulos, chaves, faixas de valor) | {…} |
| Falha parcial e retomada | {…} |
| PII, grants e Unity Catalog | {…} |
| Freshness e SLA | {…} |
| Volume, custo e compute | {…} |
| Observabilidade e alerta | {…} |

---

## Contrato de dados (opcional)

### Fontes de dados

| Fonte | Tipo | Volume | Freshness | Dono |
|-------|------|--------|-----------|------|
| {fonte} | {tabela UC \| Kafka \| arquivos no volume \| API} | {~linhas/dia} | {SLA} | {time} |

### Schema de saída

| Coluna | Tipo | Regra | PII? |
|--------|------|-------|------|
| {coluna} | {BIGINT \| STRING \| DECIMAL(18,2)} | {NOT NULL, chave, faixa} | {sim \| não} |

---

## Contexto técnico (opcional)

| Aspecto | Valor |
|---------|-------|
| **Onde fica no projeto** | {src/pipelines/… \| resources/…} |
| **Skills Databricks** | {@databricks-pipelines, @databricks-dabs, …} |
| **Infraestrutura nova** | {nenhuma \| recursos novos no bundle: …} |
| **Trigger** | {agendado: cron \| contínuo \| disparado por arquivo \| execução única} |
| **Compute** | {serverless \| job cluster: tipo e workers} |

---

## Áreas cinzentas (opcional — tamanho Complexo)

| Área | Opções consideradas | Decisão | Quem decidiu |
|------|---------------------|---------|--------------|
| {ponto que tinha mais de um caminho válido} | {A; B; C} | {opção escolhida + por quê} | {usuário \| usuário delegou} |

## Diferenças em relação à fonte (opcional)

| O que a fonte diz | O que esta spec faz | Por quê | Aprovado por |
|-------------------|---------------------|---------|--------------|
| {trecho do Confluence} | {o que muda} | {motivo} | {usuário, AAAA-MM-DD} |

---

## Suposições

<!-- Só vira suposição o que o código resolve ou o que o usuário delegou ("você decide").
     Decisão do usuário é pergunta, não suposição. Sem suposições: escreva "Nenhuma."
     Origem, uma destas três: código: <caminho do arquivo que mostra o padrão> |
     usuário delegou (Qn.m) | usuário não quis discutir (Qn.m). -->

| ID | Padrão escolhido | Motivo | Origem | Se estiver errada |
|----|------------------|--------|--------|-------------------|
| S-1 | {o que foi assumido} | {por que este padrão} | {código: `caminho/arquivo` \| usuário delegou (Qn.m) \| usuário não quis discutir (Qn.m)} | {o que muda} |

## Perguntas em aberto

- {Qn.m ainda sem resposta, ou pergunta nova com a sua recomendação. Para aprovar, esta lista precisa ser "Nenhuma."}

---

## Rastreabilidade

| Critério | Origem |
|----------|--------|
| R1.1 | {pedido: "trecho literal" \| Q1.2: "trecho literal da resposta" \| Confluence › seção \| rubrica: dimensão \| área cinzenta} |
| R1.2 | {…} |

---

## Aprovação

<!-- Preenchido só quando o usuário aprovar, com as palavras dele:
     **Aprovado**: AAAA-MM-DD — usuário: "palavras do usuário" -->

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | {AAAA-MM-DD} | Versão inicial |
