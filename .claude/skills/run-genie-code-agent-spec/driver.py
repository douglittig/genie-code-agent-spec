#!/usr/bin/env python3
"""Driver do repo genie-code-agent-spec.

Este repo não tem app: a "execução" é um agente (Genie Code / Claude Code)
parsear os SKILL.md da raiz. Este driver simula exatamente isso e valida os
invariantes do repo. Python 3.9+, só stdlib.

Modos:
  validate            (default) roda todas as checagens; exit 1 se houver erro
  catalog             imprime o que o agente "vê": name → description de cada skill
  show <skill-dir>    frontmatter resolvido + arquivos de referência de uma skill
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# Pastas da raiz que não são skills.
NON_SKILL_DIRS = {"docs", "assets", ".github", ".claude", ".git"}

# Skills cujo `name:` difere da pasta por mapeamento do upstream
# (ver UPSTREAM_EXTRA no sync: .claude/skills/python-dev → databricks-python-dev).
NAME_EXCEPTIONS = {"databricks-python-dev": "python-dev"}

SYNC_WORKFLOW = ROOT / ".github/workflows/sync-databricks-skills.yml"
LOCK_FILE = ROOT / "databricks-skills.lock"

errors = []
warnings = []


def parse_frontmatter(text, where):
    """Parser mínimo do frontmatter YAML usado nas skills: `key: value`
    (plain ou quotado) e block scalar `key: |`. Sem dependências."""
    if not text.startswith("---"):
        errors.append(f"{where}: não começa com delimitador '---' de frontmatter")
        return {}
    m = re.search(r"^---\s*$", text[3:], flags=re.M)
    if not m:
        errors.append(f"{where}: frontmatter sem '---' de fechamento")
        return {}
    block = text[3 : 3 + m.start()]
    fm = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        km = re.match(r"^(\w[\w-]*):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            if val in ("|", "|-", ">", ">-"):
                body = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                    body.append(lines[i].strip())
                    i += 1
                fm[key] = " ".join(b for b in body if b)
                continue
            if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                val = val[1:-1]
            fm[key] = val
        i += 1
    return fm


def skill_dirs():
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and d.name not in NON_SKILL_DIRS and not d.name.startswith(".")
    )


def load_skills():
    skills = {}
    for d in skill_dirs():
        md = d / "SKILL.md"
        if not md.exists():
            errors.append(f"{d.name}/: sem SKILL.md — não é carregável como skill")
            continue
        fm = parse_frontmatter(md.read_text(encoding="utf-8"), f"{d.name}/SKILL.md")
        skills[d.name] = fm
    return skills


def check_frontmatter(skills):
    for dirname, fm in skills.items():
        where = f"{dirname}/SKILL.md"
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append(f"{where}: frontmatter sem 'name'")
        if not desc:
            errors.append(f"{where}: frontmatter sem 'description' — a skill nunca vai auto-carregar")
        expected = NAME_EXCEPTIONS.get(dirname, dirname.lower())
        if name and name != expected:
            warnings.append(f"{where}: name '{name}' ≠ pasta '{expected}' (invocação @{name} não bate com a pasta)")
        if len(desc) > 1024:
            warnings.append(f"{where}: description com {len(desc)} chars (>1024; risco de truncamento no auto-load)")


def check_own_skills(skills):
    if not SYNC_WORKFLOW.exists():
        errors.append("sync-databricks-skills.yml não encontrado")
        return
    m = re.search(r'OWN_SKILLS:\s*"([^"]+)"', SYNC_WORKFLOW.read_text(encoding="utf-8"))
    if not m:
        errors.append("OWN_SKILLS não encontrado no workflow de sync")
        return
    declared = set(m.group(1).split())
    actual = {d.name for d in skill_dirs() if d.name.startswith(("sdd-", "custom-"))}
    for s in sorted(actual - declared):
        errors.append(f"{s}/ é skill própria mas NÃO está em OWN_SKILLS — o sync vai apagá-la")
    for s in sorted(declared - actual):
        warnings.append(f"OWN_SKILLS declara '{s}' mas a pasta não existe na raiz")


def check_readme(skills):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    linked = set(re.findall(r"\]\(([\w-]+)/\)", readme))
    for d in sorted(skills):
        if d not in linked and d != "TEMPLATE":
            warnings.append(f"README.md: skill {d}/ não aparece no índice")
    for d in sorted(linked - set(skills)):
        if (ROOT / d).is_dir():
            continue
        errors.append(f"README.md: link para {d}/ mas a pasta não existe")


def check_lock():
    if not LOCK_FILE.exists():
        errors.append("databricks-skills.lock não existe")
        return
    text = LOCK_FILE.read_text(encoding="utf-8")
    for field in ("version:", "commit:", "synced_at:"):
        if field not in text:
            errors.append(f"databricks-skills.lock sem campo '{field}'")


def cmd_validate():
    skills = load_skills()
    check_frontmatter(skills)
    check_own_skills(skills)
    check_readme(skills)
    check_lock()
    n = len(skills)
    print(f"{n} skills parseadas em {ROOT}")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERRO  {e}")
    if errors:
        print(f"\nFALHOU: {len(errors)} erro(s), {len(warnings)} warning(s)")
        return 1
    print(f"OK: 0 erros, {len(warnings)} warning(s)")
    return 0


def cmd_catalog():
    skills = load_skills()
    for dirname in sorted(skills):
        fm = skills[dirname]
        desc = fm.get("description", "(sem description)")
        print(f"@{fm.get('name', dirname)}")
        print(f"    {desc[:200]}{'…' if len(desc) > 200 else ''}")
    return 1 if errors else 0


def cmd_show(dirname):
    d = ROOT / dirname
    md = d / "SKILL.md"
    if not md.exists():
        print(f"ERRO: {dirname}/SKILL.md não existe")
        return 1
    fm = parse_frontmatter(md.read_text(encoding="utf-8"), f"{dirname}/SKILL.md")
    print(f"name:        {fm.get('name')}")
    print(f"description: {fm.get('description')}")
    refs = [p.relative_to(d) for p in sorted(d.rglob("*")) if p.is_file() and p.name != "SKILL.md"]
    print(f"arquivos de referência ({len(refs)}):")
    for r in refs:
        print(f"  {r}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "validate":
        sys.exit(cmd_validate())
    if args[0] == "catalog":
        sys.exit(cmd_catalog())
    if args[0] == "show" and len(args) == 2:
        sys.exit(cmd_show(args[1]))
    print(__doc__)
    sys.exit(2)
