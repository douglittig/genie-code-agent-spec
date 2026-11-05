# Provas — cada critério com o teste que decide

Guia de quem escreve prova: o `@sdd-po` (seção Provas do TASKS, no Grande e no Complexo), o
`@sdd-define` (seção Provas do DEFINE, no Médio) e o `@sdd-build` (os testes). O gate
`sdd_gates tasks` (ou `define`, no Médio) confere o formato; na Fase 4, o gate `provas` roda
cada uma no commit atual.

**A prova nasce do critério de aceite, nunca da implementação.** O valor esperado é o que a spec
define, escrito no teste. Spec sem valor preciso para um caso é pergunta para o usuário, não
asserção vaga.

---

## Formato

```markdown
**Build**: `databricks bundle validate -t dev`
**Run unit**: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/unit -v -p no:cacheprovider`

**P3** — Um `payment_id` cujo registro mais recente é `refunded` não aparece na silver, mesmo já publicado (R2.1)
Prova: run unit | tests/unit/test_status.py::test_r2_1_refunded_sai_da_silver PASSED

**P9** — O job roda no minuto 0 de toda hora, em America/Sao_Paulo (R3.1)
Prova: `databricks bundle validate -t prod -o json | python3 tests/config/confere_agenda.py`
```

- **Uma prova por critério do DEFINE**, no mínimo. A afirmação é observável e traz o valor
  ("não aparece", "uma linha por `payment_id`", "minuto 0"), e cita o critério entre parênteses.
- **`run <nome> | <linha>`:** testes que rodam juntos ficam num `**Run <nome>**:`, rodado uma
  vez. A prova passa quando as palavras depois do `|` aparecem, nessa ordem, numa linha da saída.
  - A linha leva o marcador de "passou" (`PASSED` no pytest com `-v`). Sem ele, a mesma linha
    aparece quando o teste falha.
  - Teste renomeado, ou filtro que não seleciona nada, aparece como "nenhum teste rodou", e não
    como verde. Por isso o nome do teste vai na linha, e não só "passou".
- **Prova solta:** um comando entre crases, julgado pelo código de saída. Serve para o que não
  roda junto com o grupo: a leitura do bundle, uma query de conferência no target de
  desenvolvimento. O comando precisa falhar quando o critério é falso; um comando que sempre sai
  0 não prova nada.
- **`passeio — …`:** o que a consulta no target de desenvolvimento mostra, para o que só se vê
  rodando a feature. Use pouco: o passeio não roda de novo sozinho.
- **`**Build**:`** os comandos de build, lint e validação que o repo já tem, entre crases. Rodam
  uma vez antes da primeira task (`--executar`): vermelho ali para o Build, porque um comando que
  já falha não serve de gate. Repo novo, sem build: `**Build**: nenhum — motivo`. O que vai
  existir depois (testes de configuração, `bundle validate`) entra como prova dos critérios que
  dependem dele.
- **Bytecode e cache:** `PYTHONDONTWRITEBYTECODE=1` e `-p no:cacheprovider` nos comandos de
  teste, para o `__pycache__` não sujar a árvore do git. A primeira task de um repo novo cria o
  `.gitignore` com `__pycache__/`.

---

## Que prova cada critério pede

| O critério fala de… | Prova | Nível de gate |
|---|---|---|
| Regra sobre as linhas: chave, filtro, desempate, cálculo, quarentena | Unitário em memória: pytest com DataFrames criados no teste e `assertDataFrameEqual` | rápido |
| Agendamento, fuso, alerta, compute serverless | Configuração resolvida do bundle: `databricks bundle validate -t <target> -o json` lido por um script de conferência | rápido |
| Expectation do Lakeflow (descarte, contagem) | Integração no target de desenvolvimento: update do pipeline + consulta ao event log | completo |
| Horário de término, volume, freshness | Integração no target de desenvolvimento: query de conferência, ou consulta ao event log do update | completo |
| Tabela, schema, grant | `databricks bundle validate` (sem teste próprio) | build |

**Matriz de testes padrão**, para repo sem testes (recomendação ao usuário, não decisão sua):

| Camada | Teste | Profundidade | Onde | Nível |
|---|---|---|---|---|
| Transformação (função PySpark com a regra) | Unitário em memória, `assertDataFrameEqual` | Cada critério de regra, 1:1, e cada caso de borda da rubrica (nulo, empate, atraso, reprocessamento) | `tests/unit/` | rápido |
| Configuração do bundle | Leitura da configuração resolvida | Cada critério de horário, alerta e compute | `tests/config/` | rápido |
| Pipeline Lakeflow | Integração no target de desenvolvimento | Cada expectation que um critério cita | `tests/integracao/` | completo |
| Tabela, schema, grant | Sem teste próprio | — | — | build |

A regra que o critério descreve precisa rodar numa função Python que o teste em memória alcança
(o Design diz onde, na seção "Onde a regra roda"). Regra que só existe no SQL do pipeline ou no
AUTO CDC só tem prova de integração.

---

## Unitário em memória

```python
from pyspark.testing import assertDataFrameEqual

from pagamentos.regras import publicaveis

ESQUEMA = "payment_id bigint, status string, _ingerido_em timestamp"


def test_r2_1_refunded_sai_da_silver(spark):
    bronze = spark.createDataFrame(
        [(1, "completed", "2026-11-02 10:00:00"), (1, "refunded", "2026-11-02 11:00:00"),
         (2, "completed", "2026-11-02 10:00:00")],
        ESQUEMA,
    )
    esperado = spark.createDataFrame([(2, "completed", "2026-11-02 10:00:00")], ESQUEMA)
    assertDataFrameEqual(publicaveis(bronze), esperado)
```

- **O nome do teste começa pelo critério** (`test_r2_1_…`): é o que vai na linha da prova, e o
  que o Verifier usa para achar o teste de cada critério.
- **Dados escritos no teste**, com esquema explícito. O esperado é o valor da spec, digitado. Nunca
  calcule o esperado com a função que está sendo testada.
- **Um teste por critério e um por caso de borda** que o DEFINE ou a rubrica citam (empate, nulo,
  atraso, reprocessar duas vezes). Conjunto com vários membros (todos os status, todos os motivos
  de quarentena): `@pytest.mark.parametrize` sobre todos, um caso por membro.
- `assertDataFrameEqual` compara o conteúdo; a ordem das linhas não conta (`checkRowOrder=False`
  é o padrão desde o PySpark 3.5). `ignoreColumnOrder`, `ignoreNullable` e os outros `ignore*`
  existem a partir do PySpark 4.0, que é a base dos testes gerados (o clássico DBR 17).
- Nada que só exista no PySpark 4.1 ou depois.

### A sessão Spark dos testes

Os testes rodam num processo novo (o shell do agente, ou o gate), nunca dentro do kernel do
notebook: rodar o pytest duas vezes no mesmo kernel usa o código velho que ficou na memória.
Num processo novo no Databricks, o Spark local não roda (o cluster bloqueia o `spark-submit`), e
o processo herda a sessão Spark Connect do notebook (`SPARK_REMOTE`), que ele não consegue usar.
O que funciona é o **Databricks Connect abrindo uma sessão no serverless**, depois de tirar essa
herança:

```python
# tests/conftest.py
import os

import pytest

# No Databricks, o processo herda a sessão Spark Connect do notebook, que um processo novo não usa.
for _var in ("SPARK_REMOTE", "SPARK_CONNECT_MODE_ENABLED"):
    os.environ.pop(_var, None)


@pytest.fixture(scope="session")
def spark():
    if os.environ.get("DATABRICKS_RUNTIME_VERSION"):  # no Databricks: sessão nova no serverless
        os.environ.setdefault("DATABRICKS_SERVERLESS_COMPUTE_ID", "auto")
        from databricks.connect import DatabricksSession
        return DatabricksSession.builder.getOrCreate()
    from pyspark.sql import SparkSession  # fora do Databricks (máquina local, CI)
    return SparkSession.builder.master("local[1]").getOrCreate()
```

- No shell do agente, a autenticação já está no ambiente (`DATABRICKS_HOST`, `DATABRICKS_TOKEN`).
- Cada execução do pytest abre uma sessão no serverless: ~15 s e um pouco de compute serverless
  (não é Genie Code). Junte os testes num `Run` para abrir uma sessão só.
- O `DatabricksSession` para o próprio cluster clássico não funciona num processo novo
  (`KeyError: 'SPARK_REMOTE'`); use o serverless.
- `PYTHONDONTWRITEBYTECODE=1` e `-p no:cacheprovider`: o `/Workspace` não aceita a pasta
  `__pycache__` (`OSError: [Errno 95]`), e o pytest para na coleta.
- O pytest colore a saída mesmo sem terminal. O gate tira as cores antes de procurar a linha
  esperada; ao copiar a linha de uma execução, copie sem os códigos de cor.

---

## Configuração do bundle

```bash
databricks bundle validate -t prod -o json | python3 tests/config/confere_agenda.py
databricks bundle validate -t dev -o json | python3 tests/config/confere_pausa_no_dev.py
```

- O `-o json` dá a configuração **resolvida**, com o que cada target muda (nome com prefixo,
  presets, agendamento). O YAML cru não mostra isso.
- O script lê o JSON da entrada, confere o recurso que o critério cita (`resources.jobs.<chave>`)
  e sai com 1 quando o valor não bate: `schedule.quartz_cron_expression`, `schedule.timezone_id`,
  `email_notifications.on_failure`, ausência de bloco de cluster no serverless.
- **No target de desenvolvimento, o agendamento precisa sair `PAUSED`.** O `mode: development`
  liga `presets.trigger_pause_status: PAUSED`, mas um `pause_status` fixado no recurso vence o
  preset ([deployment modes](https://docs.databricks.com/aws/en/dev-tools/bundles/deployment-modes)).
  O recurso base não fixa `pause_status`; o `UNPAUSED` vai só no target de produção.

---

## Integração no target de desenvolvimento

Sequência da skill `@databricks-pipelines`: `databricks bundle validate`, `databricks bundle deploy
-t dev`, `databricks bundle run <pipeline> -t dev`. **Deploy, run e destroy pedem o "ok" do
usuário**, mesmo no target de desenvolvimento: a ferramenta de execução do Genie Code bloqueia o
deploy sem autorização explícita, e o raio de ação também exige. Peça junto com a conferência de
que todo agendamento sai `PAUSED` no `validate -t dev -o json`.

- **A prova não faz deploy.** Ela só lê o resultado de um update que já rodou: o deploy e o run
  são passos com o "ok" do usuário, registrados no state, antes de rodar as provas.
- **Leitura pelo Spark ou pela CLI.** No shell do agente, a CLI funciona e o SDK do Python não (no
  clássico, `KeyError: 'SPARK_REMOTE'`). Consulte o event log com o Spark da sessão do Databricks
  Connect (`spark.sql(...)`), ou com a CLI.
- **Cada comando termina em menos de 10 minutos.** A ferramenta do agente não deixa um comando
  esperar mais que isso (um `sleep 600` foi bloqueado). Prova que espera um update longo vira
  dois passos: disparar e, depois, conferir.

- **Expectation:** depois do update, consulte o event log do pipeline
  (`SELECT * FROM event_log(<pipelineId>)`). As métricas ficam nos eventos `flow_progress`, em
  `details:flow_progress.data_quality.expectations` (registros que passaram e que falharam, por
  expectation) e `details:flow_progress.data_quality` (descartados)
  ([event log](https://docs.databricks.com/aws/en/ldp/monitor-event-logs)).
- **`expect_or_fail` não grava métrica:** a prova é o update falhar com o dado ruim e passar sem
  ele ([expectations](https://docs.databricks.com/aws/en/ldp/expectations)).
- Os dados de entrada da prova ficam no schema de desenvolvimento, criados pela própria prova.
  Escrever fora dele exige um "ok" à parte.
- Se o critério pede testes só em memória (como num DEFINE que diz "sem criar ou ler tabelas"),
  prova de integração contradiz a spec: pergunte ao usuário antes de escrever.

---

## Antipadrões

| Antipadrão | Por que não prova |
|---|---|
| Esperado calculado com a função testada | O teste repete a implementação: passa com o erro junto |
| Contar linhas quando o critério fala do conteúdo | A contagem bate com as linhas erradas |
| Só o caminho feliz, quando o critério ou a rubrica citam casos de borda | O caso que quebra fica sem teste |
| Ler tabela de verdade num teste que a spec quer em memória | Depende de dado que muda; contradiz o critério |
| Mock do Spark, ou teste do próprio Spark | Prova a biblioteca, não a feature |
| `skip`, `xfail` ou asserção afrouxada para passar | Apaga a prova em vez de corrigir o código |
| Prova solta que sempre sai 0 | Não falha quando o critério é falso |
| Linha esperada sem `PASSED` | Aparece também quando o teste falha |

Antes de dar uma prova por boa: ela **falharia se o critério fosse falso?** Se uma implementação
errada plausível ainda passa, a prova é rasa.

---

> O formato de prova por critério (`Run`, linha esperada com marcador, prova solta, `Build`), a
> matriz de testes e os antipadrões de teste foram adaptados do
> [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills) (Tech Leads Club,
> CC-BY-4.0) para dados no Databricks. Créditos em `THIRD_PARTY_NOTICES.md`.
