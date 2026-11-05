# Databricks notebook source
# MAGIC %md
# MAGIC # Sondagem do Build no Genie Code, rodada 2 (teste F)
# MAGIC
# MAGIC A rodada 1 mostrou que, num subprocesso, o pytest não consegue sessão Spark: o subprocesso herda a URL do Spark Connect da sessão do notebook (`unix:///databricks/sparkconnect/grpc.sock;…`). O cliente padrão recusa essa URL (`INVALID_CONNECT_URL`), e o `local[1]` conflita com ela (`CANNOT_CONFIGURE_SPARK_CONNECT_MASTER`). O SDK no subprocesso do clássico também falhou: a autenticação "runtime" tentou criar um SparkContext. Esta rodada testa as saídas:
# MAGIC
# MAGIC | # | Pergunta | Por que importa |
# MAGIC |---|---|---|
# MAGIC | F2e | Subprocesso **sem** as variáveis do Spark Connect, com `local[1]` | Spark local, sem rede nem token (só no clássico: o serverless não tem JVM) |
# MAGIC | F2f | Subprocesso sem as variáveis, com Databricks Connect e o token do notebook | Sessão remota num processo novo, nos dois computes |
# MAGIC | F2g | Por que o pytest **no kernel** saiu com código 2 | Saída capturada, numa pasta do workspace e numa pasta local |
# MAGIC | F2h | Pytest no kernel vê a mudança no arquivo, ou usa o módulo velho da memória? | Se usar o velho, rodar o gate dentro do kernel dá resultado falso |
# MAGIC | F4b | SDK no subprocesso com `DATABRICKS_AUTH_TYPE=pat` | Para o update do pipeline e o event log no target de desenvolvimento |
# MAGIC
# MAGIC **Como rodar:** do Git Folder `sdd-gates`, como a rodada 1. O compute (serverless ou clássico) é detectado sozinho. Rode tudo uma vez em cada compute e cole os dois JSONs na conversa. O F2f abre uma sessão do Databricks Connect, que usa compute (no serverless, poucos segundos de serverless).

# COMMAND ----------

import contextlib, io, json, os, subprocess, sys, tempfile, textwrap, time

COMPUTE = "serverless" if os.environ.get("DATABRICKS_RUNTIME_VERSION", "").startswith("client.") else "classico"
resultado = {"compute": COMPUTE, "runtime": os.environ.get("DATABRICKS_RUNTIME_VERSION")}

ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
nb_path = ctx.notebookPath().get()
usuario = nb_path.split("/")[2]
PASTA = f"/Workspace/Users/{usuario}/sondagem-build/rodada-2"
try:
    HOST, TOKEN = ctx.apiUrl().get(), ctx.apiToken().get()
except Exception:
    HOST, TOKEN = None, None
try:
    CLUSTER_ID = spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
except Exception:
    CLUSTER_ID = None

# Variáveis que apontam o subprocesso para a sessão Spark Connect do notebook. Só os nomes vão para o JSON.
def eh_connect(nome, valor):
    return ("SPARK" in nome.upper() and ("grpc.sock" in valor or valor.startswith(("sc://", "unix://")))) or \
        nome in ("SPARK_REMOTE", "SPARK_CONNECT_MODE_ENABLED")

VARS_CONNECT = sorted(k for k, v in os.environ.items() if eh_connect(k, v))
ENV_LIMPO = {k: v for k, v in os.environ.items() if k not in VARS_CONNECT}
CRED = {"DATABRICKS_HOST": HOST, "DATABRICKS_TOKEN": TOKEN, "DATABRICKS_AUTH_TYPE": "pat"} if HOST and TOKEN else {}


def limpa(texto):
    return texto.replace(TOKEN, "***") if TOKEN else texto


def roda(cmd, cwd=None, env=None, timeout=600, linhas=8):
    """Roda num subprocesso com o env dado (padrão: o do notebook). Saída sem o token."""
    env = {**(os.environ if env is None else env), "PYTHONDONTWRITEBYTECODE": "1"}
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        todas = limpa(p.stdout + p.stderr).strip().splitlines()
        return {"exit": p.returncode, "segundos": round(time.time() - t0, 1), "saida": todas[-linhas:], "_todas": todas}
    except Exception as e:
        return {"exit": None, "segundos": round(time.time() - t0, 1), "erro": limpa(f"{type(e).__name__}: {e}"), "_todas": []}


def guarda(r):
    return {k: v for k, v in r.items() if not k.startswith("_")}


def escreve(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w") as f:
        f.write(textwrap.dedent(texto).lstrip())


TESTE = '''
    from pyspark.testing import assertDataFrameEqual

    def test_passa(spark):
        df = spark.createDataFrame([(1, "a"), (2, "b")], "id int, v string")
        assertDataFrameEqual(df, spark.createDataFrame([(1, "a"), (2, "b")], "id int, v string"))

    def test_falha(spark):
        df = spark.createDataFrame([(1, "a")], "id int, v string")
        assertDataFrameEqual(df, spark.createDataFrame([(1, "x")], "id int, v string"))
'''


def avalia(r):
    todas = r["_todas"]
    passa = any("test_passa PASSED" in ln for ln in todas)
    falha = any("test_falha FAILED" in ln for ln in todas)
    return {**guarda(r), "linha_passa": passa, "linha_falha": falha, "separa": r["exit"] == 1 and passa and falha}


def pytest_sub(pasta, env):
    return avalia(roda(["python3", "-m", "pytest", pasta, "-v", "-p", "no:cacheprovider"], cwd=pasta, env=env))


resultado["ambiente"] = {
    "variaveis_connect_removidas": VARS_CONNECT,
    "variaveis_SPARK": sorted(k for k in os.environ if "SPARK" in k.upper()),
    "token_do_contexto": bool(TOKEN),
    "cluster_id": CLUSTER_ID,
}
resultado["ambiente"]

# COMMAND ----------

# MAGIC %md ## F2e e F2f. Subprocesso sem as variáveis do Spark Connect

# COMMAND ----------

escreve(f"{PASTA}/e_local/conftest.py", '''
    import pytest
    from pyspark.sql import SparkSession

    @pytest.fixture(scope="session")
    def spark():
        return SparkSession.builder.master("local[1]").appName("sondagem").getOrCreate()
''')
escreve(f"{PASTA}/f_connect/conftest.py", '''
    import pytest
    from databricks.connect import DatabricksSession

    @pytest.fixture(scope="session")
    def spark():
        return DatabricksSession.builder.getOrCreate()
''')
for nome in ("e_local", "f_connect"):
    escreve(f"{PASTA}/{nome}/test_sondagem.py", TESTE)

f2 = {"e_local_sem_connect": pytest_sub(f"{PASTA}/e_local", ENV_LIMPO)}
if CRED:
    f2["f_connect_serverless"] = pytest_sub(f"{PASTA}/f_connect",
                                            {**ENV_LIMPO, **CRED, "DATABRICKS_SERVERLESS_COMPUTE_ID": "auto"})
    if COMPUTE == "classico" and CLUSTER_ID:
        f2["f_connect_neste_cluster"] = pytest_sub(f"{PASTA}/f_connect",
                                                   {**ENV_LIMPO, **CRED, "DATABRICKS_CLUSTER_ID": CLUSTER_ID})
f2["serve"] = [k for k, v in f2.items() if isinstance(v, dict) and v.get("separa")]
resultado["F2ef_subprocesso_limpo"] = f2
{k: (v.get("separa") if isinstance(v, dict) else v) for k, v in f2.items()}

# COMMAND ----------

# MAGIC %md ## F2g e F2h. Pytest no kernel

# COMMAND ----------

import pytest


class PluginSpark:
    """Entrega a sessão Spark do notebook aos testes como fixture `spark`."""
    @pytest.fixture
    def spark(self):
        return spark


def pytest_kernel(pasta, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        codigo = pytest.main([pasta, "-v", "-p", "no:cacheprovider", *args], plugins=[PluginSpark()])
    linhas = buf.getvalue().strip().splitlines()
    return {"exit": int(codigo), "fim": linhas[-12:]}


# Nomes de arquivo diferentes nas duas pastas: o mesmo nome de módulo duas vezes no kernel dá conflito no pytest.
f2g = {}
escreve(f"{PASTA}/g_kernel/test_sondagem_ws.py", TESTE)
f2g["workspace"] = pytest_kernel(f"{PASTA}/g_kernel")
local = tempfile.mkdtemp()
escreve(f"{local}/test_sondagem_local.py", TESTE)
f2g["pasta_local"] = pytest_kernel(local)

# F2h: o código da regra muda entre duas rodadas no mesmo kernel. O valor esperado é lido de um
# arquivo na hora do teste, então só um módulo velho em memória faz a 2ª rodada falhar.
modulo = f"regra_sondagem_{int(time.time())}"
pasta_h = tempfile.mkdtemp()
escreve(f"{pasta_h}/test_regra.py", f'''
    from pathlib import Path
    from {modulo} import valor

    def test_valor():
        esperado = int((Path(__file__).parent / "esperado.txt").read_text())
        assert valor() == esperado
''')
escreve(f"{pasta_h}/{modulo}.py", "def valor():\n    return 1\n")
escreve(f"{pasta_h}/esperado.txt", "1")
f2h = {"rodada_1": pytest_kernel(pasta_h, "--rootdir", pasta_h)}
escreve(f"{pasta_h}/{modulo}.py", "def valor():\n    return 2\n")
escreve(f"{pasta_h}/esperado.txt", "2")
f2h["rodada_2_codigo_novo"] = pytest_kernel(pasta_h, "--rootdir", pasta_h)
f2h["usou_o_modulo_velho"] = f2h["rodada_1"]["exit"] == 0 and f2h["rodada_2_codigo_novo"]["exit"] != 0
f2h["modulo_ficou_em_sys_modules"] = modulo in sys.modules
resultado["F2g_kernel"] = f2g
resultado["F2h_modulo_velho"] = f2h
{"F2g": {k: v["exit"] for k, v in f2g.items()}, "F2h_usou_o_modulo_velho": f2h["usou_o_modulo_velho"]}

# COMMAND ----------

# MAGIC %md ## F4b. SDK no subprocesso com `DATABRICKS_AUTH_TYPE=pat`

# COMMAND ----------

codigo_sdk = ("from databricks.sdk import WorkspaceClient; "
              "print('usuario-ok' if WorkspaceClient().current_user.me().user_name else 'sem-usuario')")


def sdk_sub(env):
    r = roda(["python3", "-c", codigo_sdk], env=env)
    # Linha exata: no Python 3.13+, o traceback de um "-c" repete o código, com o texto "usuario-ok"
    return {"exit": r["exit"], "ok": any(ln.strip() == "usuario-ok" for ln in r["_todas"]), "fim": r["saida"][-2:]}


f4b = {}
if CRED:
    f4b["pat"] = sdk_sub({**os.environ, **CRED})
    f4b["pat_sem_connect"] = sdk_sub({**ENV_LIMPO, **CRED})
resultado["F4b_sdk_pat"] = f4b
f4b

# COMMAND ----------

# MAGIC %md ## Resultado: copie e cole na conversa

# COMMAND ----------

print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------

# MAGIC %md **Limpeza:** apague a pasta `/Workspace/Users/<você>/sondagem-build` quando terminar as duas rodadas.
