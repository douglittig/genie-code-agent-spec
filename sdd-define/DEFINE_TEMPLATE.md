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
| **Status** | {Rascunho \| Aguardando aprovação \| Aprovado \| Em revisão} |

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
     usuário delegou (Qn.m) | usuário não quis discutir (Qn.m).
     Use as colunas como estão: o gate reprova tabela com coluna renomeada ou faltando. -->

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

## Provas (só no tamanho Médio)

<!-- No Médio não há plano de tarefas: as provas ficam aqui e são aprovadas com a spec. No Grande
     e no Complexo, apague esta seção inteira (as provas vão no TASKS, pelo @sdd-po).
     Uma prova por critério: uma afirmação observável, com o valor, citando o critério, e na linha
     de baixo o que a decide:
       Prova: run <nome> | <a linha que o teste imprime ao passar, com PASSED>
       Prova: `<comando sozinho>`        (prova solta: o código de saída decide)
       Prova: passeio — <o que a consulta no dev mostra>
     **Build**: os comandos de build, lint e validação do repo, entre crases; repo sem build:
     "nenhum — motivo". Guia de cada tipo de prova: sdd-workflow/PROVAS.md. -->

**Build**: {`databricks bundle validate -t dev` | nenhum — motivo}
**Run unit**: {`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/unit -v -p no:cacheprovider`}

**P1** — {afirmação observável, com o valor} ({R1.1})
Prova: {run unit | tests/unit/test_x.py::test_r1_1_o_que_confere PASSED}

---

## Aprovação

<!-- Preenchido só quando o usuário aprovar, com a versão aprovada e as palavras dele:
     **Aprovado**: AAAA-MM-DD — v1.0 — usuário: "palavras do usuário"
     Aprovar não cria versão. Aprovação de uma versão anterior: mantenha como texto simples,
     sem o negrito, para o gate ler só a última. -->

## Histórico de revisões

<!-- Mudou depois de aprovado: versão nova, Status "Em revisão" e aprovação nova. -->

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | {AAAA-MM-DD} | Versão inicial |
