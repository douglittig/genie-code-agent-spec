# Databricks notebook source
# MAGIC %md
# MAGIC # Teste do ambiente para os gates do SDD
# MAGIC
# MAGIC Os gates do workflow SDD são scripts Python (pacote `sdd-gates`, pasta `gates/` do repo) que leem os arquivos de spec, rodam os testes do projeto e gravam o resultado. Este notebook confere, no seu workspace, o que eles precisam:
# MAGIC
# MAGIC | # | Pergunta | Por que importa |
# MAGIC |---|---|---|
# MAGIC | 1 | O compute roda um script `.py` guardado no Git Folder? | O validador do repo é um script |
# MAGIC | 2 | Dá para saber o commit atual e se há mudança não commitada? | A prova vale para um commit específico |
# MAGIC | 3 | O compute grava arquivo dentro do Git Folder? | Os gates gravam `proofs.md` e `verification.md` em `.sdd/` |
# MAGIC | 4 | pytest e `assertDataFrameEqual` rodam aqui? | São a forma padrão de prova |
# MAGIC | 5 | O pacote `sdd-gates` instala do GitHub e passa no selftest? | Os gates rodam pelo pacote, porque o Genie Code não executa scripts dentro de `.assistant/skills` |
# MAGIC
# MAGIC **Como rodar:** abra este notebook a partir do Git Folder do repo (`Workspace/.assistant/skills/tools/`) e rode tudo (*Run all*). Rode uma vez em **serverless** e uma vez num **cluster clássico**. A última célula imprime um JSON: cole o resultado das duas rodadas na conversa.
# MAGIC
# MAGIC O git precisa de duas coisas: o Git Folder criado com a opção **Use Git CLI**, e `-c safe.directory=<raiz>` em cada chamada (no cluster clássico, o usuário do sistema não é o dono dos arquivos e o git recusa o repo sem isso).
# MAGIC
# MAGIC Os testes manuais com o Genie Code estão no fim do notebook.

# COMMAND ----------

import json, os, subprocess, sys, tempfile, textwrap

resultado = {}

def roda(cmd, cwd=None):
    """Roda um comando e devolve código de saída + o fim da saída."""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
        saida = (p.stdout + p.stderr).strip().splitlines()
        return {"exit": p.returncode, "saida": saida[-5:]}
    except Exception as e:  # comando inexistente, timeout etc.
        return {"exit": None, "erro": f"{type(e).__name__}: {e}"}

# Raiz do repo = pasta acima de tools/, a partir do caminho deste notebook
ctx = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
nb_path = ctx.notebookPath().get()
raiz = "/Workspace" + nb_path.rsplit("/tools/", 1)[0]
resultado["ambiente"] = {
    "notebook": nb_path,
    "raiz_repo": raiz,
    "raiz_existe": os.path.isdir(raiz),
    "cwd": os.getcwd(),
    "python": sys.version.split()[0],
    "pyspark": __import__("pyspark").__version__,
    "spark": spark.version,
}
resultado["ambiente"]

# COMMAND ----------

# MAGIC %md ## 1. Rodar um script guardado no Git Folder

# COMMAND ----------

validador = f"{raiz}/.claude/skills/run-genie-code-agent-spec/driver.py"
resultado["1_script"] = {
    "pasta_oculta_visivel": os.path.exists(validador),  # pastas que começam com "." chegam ao workspace?
    "python_script": roda([sys.executable, validador, "validate"], cwd=raiz),
    "python3_no_path": roda(["python3", "--version"]),
    "bash": roda(["bash", "-c", "echo bash-ok"]),
}
resultado["1_script"]

# COMMAND ----------

# MAGIC %md ## 2. Commit atual e mudanças não commitadas

# COMMAND ----------

git = {
    "pasta_.git_existe": os.path.isdir(f"{raiz}/.git"),
    "git_instalado": roda(["git", "--version"]),
    "git_rev_parse": roda(["git", "-c", f"safe.directory={raiz}", "-C", raiz, "rev-parse", "HEAD"]),
    "git_status": roda(["git", "-c", f"safe.directory={raiz}", "-C", raiz, "status", "--porcelain"]),
}
try:
    from databricks.sdk import WorkspaceClient
    w = WorkspaceClient()
    caminho_ws = raiz.removeprefix("/Workspace")
    repos = list(w.repos.list(path_prefix=caminho_ws))
    git["repos_api"] = [
        {k: v for k, v in r.as_dict().items() if k in ("id", "path", "branch", "head_commit_id", "url", "provider")}
        for r in repos
    ]
    # Campos completos do primeiro repo: procurar algo como "mudanças não commitadas"
    git["repos_api_campos"] = sorted(repos[0].as_dict().keys()) if repos else []
except Exception as e:
    git["repos_api_erro"] = f"{type(e).__name__}: {e}"
resultado["2_git"] = git
git

# COMMAND ----------

# MAGIC %md ## 3. Gravar arquivo dentro do Git Folder

# COMMAND ----------

alvo = f"{raiz}/.sdd/_teste_ambiente.txt"
try:
    os.makedirs(os.path.dirname(alvo), exist_ok=True)
    with open(alvo, "w") as f:
        f.write("teste")
    with open(alvo) as f:
        lido = f.read()
    os.remove(alvo)
    try:
        os.rmdir(os.path.dirname(alvo))  # remove .sdd/ se ficou vazia
    except OSError:
        pass
    resultado["3_gravar"] = {"ok": lido == "teste"}
except Exception as e:
    resultado["3_gravar"] = {"ok": False, "erro": f"{type(e).__name__}: {e}"}
resultado["3_gravar"]

# COMMAND ----------

# MAGIC %md ## 4. pytest com `assertDataFrameEqual`
# MAGIC
# MAGIC Dois testes: um que deve passar e um que deve falhar. O gate só serve se distinguir os dois.

# COMMAND ----------

teste = textwrap.dedent('''
    from pyspark.testing import assertDataFrameEqual

    def test_deve_passar(spark):
        df = spark.createDataFrame([(1, "a"), (2, "b")], "id int, v string")
        assertDataFrameEqual(df, [(1, "a"), (2, "b")])

    def test_deve_falhar(spark):
        df = spark.createDataFrame([(1, "a")], "id int, v string")
        assertDataFrameEqual(df, [(1, "x")])
''')

try:
    import pytest

    class PluginSpark:
        """Entrega a sessão Spark do notebook aos testes como fixture `spark`."""
        @pytest.fixture
        def spark(self):
            return spark

    pasta = tempfile.mkdtemp()
    with open(f"{pasta}/test_probe.py", "w") as f:
        f.write(teste)
    codigo = pytest.main([pasta, "-q", "-p", "no:cacheprovider", "-rA"], plugins=[PluginSpark()])
    # exit 1 = algum teste falhou (o esperado aqui: 1 passa, 1 falha)
    resultado["4_pytest"] = {"pytest": pytest.__version__, "exit": int(codigo), "esperado": 1}
except Exception as e:
    resultado["4_pytest"] = {"erro": f"{type(e).__name__}: {e}"}
resultado["4_pytest"]

# COMMAND ----------

# MAGIC %md ## 5. Instalar e rodar o pacote `sdd-gates`
# MAGIC
# MAGIC Instala do GitHub, no mesmo Python do notebook, e roda o selftest (os gates contra artefatos com defeitos plantados). Troque `REF` para testar uma branch antes do merge.

# COMMAND ----------

REF = "main"
pacote = f"git+https://github.com/douglittig/genie-code-agent-spec@{REF}#subdirectory=gates"
resultado["5_sdd_gates"] = {
    "ref": REF,
    "pip_install": roda([sys.executable, "-m", "pip", "install", "--quiet", "--force-reinstall", "--no-deps", pacote]),
    "versao": roda([sys.executable, "-m", "sdd_gates", "--version"]),
    "selftest": roda([sys.executable, "-m", "sdd_gates", "selftest"]),
}
resultado["5_sdd_gates"]

# COMMAND ----------

# MAGIC %md ## Resultado: copie e cole na conversa

# COMMAND ----------

try:
    resultado["compute"] = {"cluster_id": spark.conf.get("spark.databricks.clusterUsageTags.clusterId")}
except Exception:
    resultado["compute"] = "sem cluster_id"
# O serverless também devolve um cluster_id: diga na conversa se a rodada foi serverless ou clássica.
print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Testes manuais com o Genie Code (Agent mode)
# MAGIC
# MAGIC **A. Uma sessão nova começa limpa?** (base do Verificador em sessão separada)
# MAGIC 1. Sessão A: *"Guarde esta palavra-código para depois: ABACAXI-42. E anote que o pipeline X usa a tabela Y."*
# MAGIC 2. Abra uma **sessão nova** (B) e pergunte: *"Qual palavra-código eu te passei? Que tabela o pipeline X usa?"*
# MAGIC 3. Anote o que a B sabe e de onde veio. O chat não passa de uma sessão para outra, mas a memória do Genie Code passa: se você pediu para "guardar", a B lê da memória.
# MAGIC
# MAGIC **B. O Genie Code roda um script do repo sozinho?**
# MAGIC 1. Em Agent mode, peça: *"Rode `python3 .claude/skills/run-genie-code-agent-spec/driver.py validate` a partir da raiz do Git Folder `.assistant/skills` e me mostre a saída."*
# MAGIC 2. Esperado: **recusa**. O Genie Code não executa scripts dentro de `.assistant/skills`. Repita com um `teste.py` numa pasta comum: ali ele roda.
# MAGIC
# MAGIC **C. Sessão nova lê só o que mandamos?**
# MAGIC 1. Numa sessão nova, peça para ler **um arquivo específico** do repo e resumir.
# MAGIC 2. Anote se ela abriu outros arquivos ou consultou o workspace por conta própria. O Verificador não pode ler as notas do autor da feature.
# MAGIC
# MAGIC **D. O Genie Code instala e roda os gates pela skill?**
# MAGIC 1. Numa sessão nova, em Agent mode: *"@sdd-workflow confira se os gates do SDD estão instalados neste compute e rode o selftest."*
# MAGIC 2. Esperado: ele confere com `python3 -m sdd_gates --version`, instala com `pip` se faltar, roda `python3 -m sdd_gates selftest` e mostra `selftest: OK`. Anote se pediu aprovação para instalar e se algum passo foi recusado.
