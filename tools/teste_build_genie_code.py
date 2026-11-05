# Databricks notebook source
# MAGIC %md
# MAGIC # Sondagem do Build no Genie Code (teste F)
# MAGIC
# MAGIC Na Fase 4, o `@sdd-build` fecha cada task com um gate, e o gate `sdd_gates provas` roda a prova de cada critério de aceite. O gate é chamado como subprocesso (`PYTHONPATH=<gates> python3 -m sdd_gates …`) e roda os comandos do projeto num shell. Este notebook confere, no seu workspace, o que isso precisa:
# MAGIC
# MAGIC | # | Pergunta | Por que importa |
# MAGIC |---|---|---|
# MAGIC | F2 | Num subprocesso, o pytest consegue uma SparkSession? Três jeitos: (a) `getOrCreate()`, (b) Spark local `local[1]`, (c) Databricks Connect | Na Fase 0, o pytest rodou dentro do kernel do notebook. O gate roda à parte |
# MAGIC | F3 | A CLI `databricks` existe e autentica? `bundle validate -o json` mostra a configuração resolvida de cada target? | Prova de agendamento, alerta e compute; nível "completo" do Build |
# MAGIC | F4 | O SDK (`WorkspaceClient()`) autentica no kernel e no subprocesso? | Alternativa à CLI |
# MAGIC | F5 | `import yaml` funciona no subprocesso? | Só se a CLI não rodar |
# MAGIC | F6 | `git commit` sem push fica local no Git Folder? | Decide se cada task vai para o remoto na hora |
# MAGIC
# MAGIC O F1 (como o agente executa um comando) e o F7 (quanto tempo ele espera um comando) dependem do agente: estão nos testes com o Genie Code, no fim.
# MAGIC
# MAGIC **Como rodar:**
# MAGIC 1. Faça pull no Git Folder `sdd-gates` (fora de `.assistant`) e abra este notebook de lá (`sdd-gates/tools/`). O F6 faz um commit vazio numa branch temporária desse Git Folder e apaga a branch no fim.
# MAGIC 2. Ajuste `COMPUTE` na próxima célula e rode tudo (*Run all*). Rode uma vez em **serverless** e uma vez num **cluster clássico**.
# MAGIC 3. A última célula imprime um JSON: cole o das duas rodadas na conversa.
# MAGIC
# MAGIC No serverless, o Databricks grava no topo deste notebook o bloco de ambiente (`# /// script`). Não commite: descarte com `git checkout -- tools/teste_build_genie_code.py`.
# MAGIC
# MAGIC O notebook cria a pasta `/Workspace/Users/<você>/sondagem-build`, com os testes e um bundle mínimo, que os testes com o Genie Code reaproveitam. Apague a pasta quando terminar.

# COMMAND ----------

COMPUTE = "serverless"  # "serverless" ou "classico": ajuste antes de rodar
TESTAR_DEPLOY = False   # True: bundle deploy -t dev de um job mínimo (o modo development deixa o agendamento pausado) e bundle destroy logo depois

# COMMAND ----------

import json, os, shutil, subprocess, sys, textwrap, time

resultado = {"compute": COMPUTE}

ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
nb_path = ctx.notebookPath().get()
raiz = "/Workspace" + nb_path.rsplit("/tools/", 1)[0]
usuario = nb_path.split("/")[2]  # /Users/<usuário>/...
PASTA = f"/Workspace/Users/{usuario}/sondagem-build"

# Credenciais do notebook, para ver se o subprocesso autentica com elas.
# Nunca são impressas: roda() troca o token por *** em toda saída.
try:
    HOST = ctx.apiUrl().get()
except Exception:
    HOST = None
try:
    TOKEN = ctx.apiToken().get()
except Exception:
    TOKEN = None
CRED = {"DATABRICKS_HOST": HOST, "DATABRICKS_TOKEN": TOKEN} if HOST and TOKEN else {}

try:
    CLUSTER_ID = spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
except Exception:
    CLUSTER_ID = None


def limpa(texto):
    return texto.replace(TOKEN, "***") if TOKEN else texto


def roda(cmd, cwd=None, env_extra=None, timeout=600, linhas=10):
    """Roda um comando num subprocesso. Devolve código de saída, tempo e o fim da saída.
    As chaves que começam com "_" guardam a saída inteira e saem antes de imprimir."""
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", **(env_extra or {})}
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        todas = limpa(p.stdout + p.stderr).strip().splitlines()
        return {"exit": p.returncode, "segundos": round(time.time() - t0, 1), "saida": todas[-linhas:],
                "_todas": todas, "_stdout": limpa(p.stdout)}
    except Exception as e:  # comando inexistente, timeout etc.
        return {"exit": None, "segundos": round(time.time() - t0, 1), "erro": limpa(f"{type(e).__name__}: {e}"),
                "_todas": [], "_stdout": ""}


def guarda(r):
    """O resultado sem as chaves internas (saída inteira)."""
    return {k: v for k, v in r.items() if not k.startswith("_")}


def escreve(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w") as f:
        f.write(textwrap.dedent(texto).lstrip())


resultado["ambiente"] = {
    "notebook": nb_path,
    "raiz_repo": raiz,
    "git_folder": os.path.isdir(f"{raiz}/.git"),
    "python_kernel": sys.executable,
    "python3_no_path": guarda(roda(["python3", "-c", "import sys; print(sys.executable)"], linhas=2)),
    "python": sys.version.split()[0],
    "pyspark": __import__("pyspark").__version__,
    "spark": spark.version,
    "DATABRICKS_RUNTIME_VERSION": os.environ.get("DATABRICKS_RUNTIME_VERSION"),
    "variaveis_DATABRICKS": sorted(k for k in os.environ if k.startswith("DATABRICKS_")),  # só os nomes
    "host_do_contexto": bool(HOST),
    "token_do_contexto": bool(TOKEN),
    "cluster_id": CLUSTER_ID,
}
resultado["ambiente"]

# COMMAND ----------

# MAGIC %md ## F2. pytest com Spark num subprocesso
# MAGIC
# MAGIC O mesmo par de testes nas três variantes: um teste que deve passar e outro que deve falhar. A variante serve se o pytest sair com código 1 e a saída tiver as duas linhas (`test_passa PASSED` e `test_falha FAILED`). É nessas linhas que o gate `provas` procura cada prova. A variante (d) roda no kernel, como na Fase 0, só para comparar.

# COMMAND ----------

TESTE = '''
    from pyspark.testing import assertDataFrameEqual

    def test_passa(spark):
        df = spark.createDataFrame([(1, "a"), (2, "b")], "id int, v string")
        esperado = spark.createDataFrame([(1, "a"), (2, "b")], "id int, v string")
        assertDataFrameEqual(df, esperado)

    def test_falha(spark):
        df = spark.createDataFrame([(1, "a")], "id int, v string")
        esperado = spark.createDataFrame([(1, "x")], "id int, v string")
        assertDataFrameEqual(df, esperado)
'''

CONFTEST = {
    "a_getorcreate": '''
        import pytest
        from pyspark.sql import SparkSession

        @pytest.fixture(scope="session")
        def spark():
            return SparkSession.builder.getOrCreate()
    ''',
    "b_local": '''
        import pytest
        from pyspark.sql import SparkSession

        @pytest.fixture(scope="session")
        def spark():
            return SparkSession.builder.master("local[1]").appName("sondagem").getOrCreate()
    ''',
    "c_connect": '''
        import pytest
        from databricks.connect import DatabricksSession

        @pytest.fixture(scope="session")
        def spark():
            return DatabricksSession.builder.getOrCreate()
    ''',
}

# Databricks Connect escolhe o compute pelas variáveis de ambiente (doc: tutorial serverless do Databricks Connect)
ALVO_CONNECT = {"DATABRICKS_SERVERLESS_COMPUTE_ID": "auto"} if COMPUTE == "serverless" else (
    {"DATABRICKS_CLUSTER_ID": CLUSTER_ID} if CLUSTER_ID else {})


def avalia(r):
    todas = r["_todas"]
    passa = any("test_passa PASSED" in ln for ln in todas)
    falha = any("test_falha FAILED" in ln for ln in todas)
    return {**guarda(r), "linha_passa": passa, "linha_falha": falha,
            "separa": r["exit"] == 1 and passa and falha}


def roda_pytest(pasta, env_extra=None):
    return avalia(roda(["python3", "-m", "pytest", pasta, "-v", "-p", "no:cacheprovider"],
                       cwd=pasta, env_extra=env_extra))


f2 = {}
for nome, conftest in CONFTEST.items():
    pasta = f"{PASTA}/f2/{nome}"
    escreve(f"{pasta}/conftest.py", conftest)
    escreve(f"{pasta}/test_sondagem.py", TESTE)

f2["a_getorcreate"] = roda_pytest(f"{PASTA}/f2/a_getorcreate")
f2["b_local"] = roda_pytest(f"{PASTA}/f2/b_local")
f2["c_connect_herdado"] = roda_pytest(f"{PASTA}/f2/c_connect", env_extra=ALVO_CONNECT)
if CRED:
    f2["c_connect_com_credencial"] = roda_pytest(f"{PASTA}/f2/c_connect", env_extra={**CRED, **ALVO_CONNECT})

# (d) no kernel, como na Fase 0: o spark do notebook entra como fixture
try:
    import pytest

    class PluginSpark:
        @pytest.fixture
        def spark(self):
            return spark

    pasta_d = f"{PASTA}/f2/d_kernel"
    escreve(f"{pasta_d}/test_sondagem.py", TESTE)
    codigo = pytest.main([pasta_d, "-q", "-p", "no:cacheprovider"], plugins=[PluginSpark()])
    f2["d_kernel"] = {"exit": int(codigo), "esperado": 1, "pytest": pytest.__version__}
except Exception as e:
    f2["d_kernel"] = {"erro": f"{type(e).__name__}: {e}"}

f2["serve"] = [k for k, v in f2.items() if isinstance(v, dict) and v.get("separa")]
resultado["F2_pytest_subprocesso"] = f2
{k: (v.get("separa") if isinstance(v, dict) else v) for k, v in f2.items()}

# COMMAND ----------

# MAGIC %md ## F3. CLI `databricks` e configuração resolvida do bundle
# MAGIC
# MAGIC Um bundle mínimo com dois jobs serverless (sem bloco de cluster), agendados no minuto 0 de toda hora em America/Sao_Paulo, com e-mail em falha. A diferença entre os dois: `sondagem_job` fixa `pause_status: UNPAUSED` no recurso, como nos exemplos oficiais; `sondagem_job_sem_pause` não fixa. O `validate -o json` de cada target mostra o que o target muda.
# MAGIC
# MAGIC Esperado (visto em 04/11 com a CLI v1.23.0, fora do workspace): no `dev`, o `mode: development` liga `presets.trigger_pause_status: PAUSED`, mas isso só pausa o job **sem** `pause_status` no recurso. O que fixa `UNPAUSED` continua agendado no `dev`.

# COMMAND ----------

BUNDLE = f"{PASTA}/bundle"
escreve(f"{BUNDLE}/databricks.yml", '''
    bundle:
      name: sondagem_build

    resources:
      jobs:
        sondagem_job:
          name: sondagem_job
          schedule:
            quartz_cron_expression: "0 0 * * * ?"
            timezone_id: "America/Sao_Paulo"
            pause_status: UNPAUSED
          email_notifications:
            on_failure:
              - "sondagem@example.com"
          tasks:
            - task_key: principal
              notebook_task:
                notebook_path: ./nb_sondagem.py
        sondagem_job_sem_pause:
          name: sondagem_job_sem_pause
          schedule:
            quartz_cron_expression: "0 0 * * * ?"
            timezone_id: "America/Sao_Paulo"
          tasks:
            - task_key: principal
              notebook_task:
                notebook_path: ./nb_sondagem.py

    targets:
      dev:
        default: true
        mode: development
      prod:
        default: false
''')
escreve(f"{BUNDLE}/nb_sondagem.py", '''
    # Databricks notebook source
    print("sondagem")
''')

cli = shutil.which("databricks")
f3 = {"cli": cli}


def auth(env_extra=None):
    r = roda([cli, "current-user", "me", "-o", "json"], env_extra=env_extra)
    return {"exit": r["exit"], "userName_na_saida": any('"userName"' in ln for ln in r["_todas"]),
            "fim": r["saida"][-2:] if r["exit"] else None}


def resumo_validate(target, env_extra):
    r = roda([cli, "bundle", "validate", "-t", target, "-o", "json"], cwd=BUNDLE, env_extra=env_extra)
    try:
        cfg = json.loads(r["_stdout"])
        jobs = cfg["resources"]["jobs"]
        return {"exit": r["exit"], "segundos": r["segundos"],
                "trigger_pause_status": cfg.get("presets", {}).get("trigger_pause_status"),
                "com_UNPAUSED_no_recurso": jobs["sondagem_job"].get("schedule"),
                "sem_pause_status_no_recurso": jobs["sondagem_job_sem_pause"].get("schedule"),
                "nome": jobs["sondagem_job"].get("name"),
                "email_notifications": jobs["sondagem_job"].get("email_notifications"),
                "bundle": {k: v for k, v in cfg.get("bundle", {}).items() if k in ("name", "target", "mode")}}
    except Exception as e:
        return {**guarda(r), "erro_json": f"{type(e).__name__}: {e}"}


if cli:
    f3["versao"] = guarda(roda([cli, "--version"], linhas=2))
    f3["auth_herdada"] = auth()
    if CRED:
        f3["auth_com_credencial"] = auth(CRED)
    env_cli = {} if f3["auth_herdada"]["exit"] == 0 else CRED
    f3["credencial_usada_no_validate"] = "herdada" if not env_cli else "do contexto do notebook"
    f3["validate_dev"] = resumo_validate("dev", env_cli)
    f3["validate_prod"] = resumo_validate("prod", env_cli)
    if TESTAR_DEPLOY:
        f3["deploy_dev"] = guarda(roda([cli, "bundle", "deploy", "-t", "dev"], cwd=BUNDLE, env_extra=env_cli))
        f3["destroy_dev"] = guarda(roda([cli, "bundle", "destroy", "-t", "dev", "--auto-approve"],
                                        cwd=BUNDLE, env_extra=env_cli))
resultado["F3_cli"] = f3
f3

# COMMAND ----------

# MAGIC %md ## F4. SDK no kernel e no subprocesso · F5. PyYAML

# COMMAND ----------

f4 = {}
try:
    from databricks.sdk import WorkspaceClient
    f4["kernel"] = {"ok": bool(WorkspaceClient().current_user.me().user_name)}
except Exception as e:
    f4["kernel"] = {"ok": False, "erro": limpa(f"{type(e).__name__}: {e}")[:300]}

codigo_sdk = ("from databricks.sdk import WorkspaceClient; "
              "print('usuario-ok' if WorkspaceClient().current_user.me().user_name else 'sem-usuario')")


def sdk_subprocesso(env_extra=None):
    r = roda(["python3", "-c", codigo_sdk], env_extra=env_extra)
    return {"exit": r["exit"], "ok": any("usuario-ok" in ln for ln in r["_todas"]), "fim": r["saida"][-2:]}


f4["subprocesso_herdado"] = sdk_subprocesso()
if CRED:
    f4["subprocesso_com_credencial"] = sdk_subprocesso(CRED)
resultado["F4_sdk"] = f4
resultado["F5_yaml"] = guarda(roda(["python3", "-c", "import yaml; print(yaml.__version__)"], linhas=2))
{"F4": f4, "F5": resultado["F5_yaml"]}

# COMMAND ----------

# MAGIC %md ## F6. `git commit` sem push no Git Folder
# MAGIC
# MAGIC Cria uma branch temporária, faz um commit vazio (nenhum arquivo muda), espera 30 s e pergunta ao remoto se a branch chegou lá. Depois volta para a branch original e apaga a temporária. Se `foi_para_o_remoto` sair `true`, apague a branch `sondagem-f6-…` no GitHub.

# COMMAND ----------

G = ["git", "-c", f"safe.directory={raiz}", "-c", "user.name=sondagem", "-c", "user.email=sondagem@example.com",
     "-C", raiz]
f6 = {"git_folder": os.path.isdir(f"{raiz}/.git")}
if f6["git_folder"]:
    ref = roda(G + ["symbolic-ref", "--short", "-q", "HEAD"])
    origem = ref["_stdout"].strip() if ref["exit"] == 0 else roda(G + ["rev-parse", "HEAD"])["_stdout"].strip()
    temporaria = f"sondagem-f6-{int(time.time())}"
    f6["branch_original"] = origem
    try:
        f6["checkout_b"] = guarda(roda(G + ["checkout", "-q", "-b", temporaria]))
        if f6["checkout_b"]["exit"] == 0:
            f6["commit_vazio"] = guarda(roda(G + ["commit", "-q", "--allow-empty", "-m", "chore: sondagem f6 (apagar)"]))
            time.sleep(30)  # tempo para uma sincronização automática, se existir
            f6["status"] = guarda(roda(G + ["status", "-sb"], linhas=3))
            remoto = roda(G + ["ls-remote", "--heads", "origin", temporaria])
            f6["ls_remote"] = guarda(remoto)
            f6["foi_para_o_remoto"] = bool(remoto["_stdout"].strip()) if remoto["exit"] == 0 else None
    finally:
        f6["volta"] = guarda(roda(G + ["checkout", "-q", origem]))
        f6["apaga_temporaria"] = guarda(roda(G + ["branch", "-D", temporaria]))
resultado["F6_git"] = f6
f6

# COMMAND ----------

# MAGIC %md ## Resultado: copie e cole na conversa

# COMMAND ----------

print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Testes com o Genie Code (Agent mode)
# MAGIC
# MAGIC São poucos turnos, mas pagos: a cota grátis de novembro acabou. Use uma **sessão nova** e troque `<você>` pelo seu usuário. Rode depois do notebook, que cria a pasta `sondagem-build`.
# MAGIC
# MAGIC **E. Como o agente executa um comando (F1)**
# MAGIC 1. Peça: *"Rode exatamente este comando e me mostre a saída, sem resumir: `python3 -c "import sys, os; print(sys.executable); print(os.getcwd())"`"*
# MAGIC 2. Anote: como ele executou (célula nova num notebook, `%sh`, terminal, outro jeito), em que compute, e se pediu aprovação.
# MAGIC
# MAGIC **F. O agente roda o pytest com Spark (F2)**
# MAGIC 1. Peça: *"Rode `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest /Workspace/Users/<você>/sondagem-build/f2/a_getorcreate -v -p no:cacheprovider` e me mostre as linhas da saída que têm PASSED ou FAILED."*
# MAGIC 2. Esperado: uma linha `test_passa PASSED` e uma `test_falha FAILED`. Se no notebook a variante que funcionou não foi a (a), repita com a pasta dela.
# MAGIC
# MAGIC **G. O agente roda a CLI (F3)**
# MAGIC 1. Peça: *"Na pasta `/Workspace/Users/<você>/sondagem-build/bundle`, rode `databricks bundle validate -t dev -o json` e me diga o `pause_status` do schedule de cada job."*
# MAGIC 2. Anote se ele aceitou rodar a CLI, se autenticou e o valor que relatou.
# MAGIC
# MAGIC **H. Quanto tempo ele espera um comando (F7)**
# MAGIC 1. Peça: *"Rode `python3 -c "import time; time.sleep(120); print('fim 120')"` e me mostre a saída."*
# MAGIC 2. Depois, o mesmo com `600` no lugar de `120` (10 minutos).
# MAGIC 3. Anote se ele esperou, se desistiu, depois de quanto tempo, e o que relatou. Se disse "terminou" antes de mostrar `fim`, é o mesmo "relata antes de confirmar" do teste E.
# MAGIC
# MAGIC **Limpeza:** apague a pasta `/Workspace/Users/<você>/sondagem-build`. Se rodou com `TESTAR_DEPLOY = True`, confira que o job `[dev …] sondagem_job` não ficou no workspace.
