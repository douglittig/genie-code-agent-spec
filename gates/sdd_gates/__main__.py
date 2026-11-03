"""Linha de comando: python3 -m sdd_gates <gate> [argumentos].

  define     gate do Define (DEFINE_*.md)
  tasks      gate do plano de tarefas (TASKS_*.md)
  selftest   testa os gates por mutação

Códigos de saída: 0 ok, 1 não passou, 2 erro de uso.
"""

import sys

from . import __version__, define, selftest, tasks

GATES = {
    "define": define.main,
    "tasks": tasks.main,
    "selftest": selftest.main,
}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 2
    if argv[0] == "--version":
        print(f"sdd_gates {__version__}")
        return 0
    gate = GATES.get(argv[0])
    if gate is None:
        print(f"gate desconhecido: {argv[0]} (use: {', '.join(GATES)})", file=sys.stderr)
        return 2
    return gate(argv[1:])


if __name__ == "__main__":
    sys.exit(main())
