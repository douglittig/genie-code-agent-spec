"""execucao.py — roda os comandos do projeto que um gate precisa executar.

Os gates não conhecem test runner nem build: rodam o comando que o artefato
escreveu, como o projeto roda, num shell, um de cada vez e sem limite de tempo
(como o TLC Spec-Driven). `PYTHONDONTWRITEBYTECODE=1` evita que o `__pycache__`
suje a árvore do git.
"""

import os
import subprocess


def roda(comando, cwd=None):
    """(código de saída, saída) do comando, rodado em /bin/sh na pasta `cwd`."""
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    p = subprocess.run(comando, shell=True, cwd=cwd, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, p.stdout + p.stderr


def confere_build(comandos, rel, cwd=None):
    """Roda cada comando da linha **Build** uma vez, antes de qualquer mudança.

    Vermelho aqui é erro: um comando que já falha antes da primeira task não serve de gate.
    """
    if not comandos:
        rel.nota("build: nenhum comando (Build: nenhum — motivo)")
        return
    for cmd in comandos:
        codigo, saida = roda(cmd, cwd)
        linhas = [l for l in saida.strip().splitlines() if l.strip()]
        if codigo != 0:
            fim = linhas[-1].strip() if linhas else "sem saída"
            rel.erro(f"build vermelho antes de qualquer mudança: `{cmd}` saiu com {codigo} ({fim[:120]}). "
                     "Um comando que já falha não serve de gate: corrija o comando no artefato, ou diga "
                     "ao usuário e pare")
        else:
            rel.nota(f"build: `{cmd}` passou")
