---
name: run-genie-code-agent-spec
description: >
  Run, validate, smoke-test or catalog the skills of this repo. Use when asked to
  "run" this project, validate a skill change, check frontmatter, verify OWN_SKILLS /
  provenance / README index consistency, or preview what an agent sees when loading
  a skill (@name + description). This repo has no app or build — the driver simulates
  the Genie Code / Claude Code skill-loading step.
---

# Run: genie-code-agent-spec

Este repo é conteúdo (41 skills em Markdown na raiz), não uma aplicação. "Rodar"
o projeto = fazer o que o Genie Code/Claude Code faz ao carregar as skills:
parsear o frontmatter de cada `SKILL.md`. O driver
[.claude/skills/run-genie-code-agent-spec/driver.py](driver.py) simula isso e
valida os invariantes do repo. Caminhos abaixo são relativos à **raiz do repo**.

## Pré-requisitos

Só `python3` (stdlib; testado com 3.9.6, já presente no macOS). Sem instalação,
sem build.

## Run (caminho do agente)

```bash
# Validação completa — o "smoke test" do repo. Exit 1 se houver erro.
python3 .claude/skills/run-genie-code-agent-spec/driver.py validate

# O que o agente "vê" para auto-load: @name + description de todas as skills
python3 .claude/skills/run-genie-code-agent-spec/driver.py catalog

# Simular o carregamento de uma skill: frontmatter resolvido + arquivos de referência
python3 .claude/skills/run-genie-code-agent-spec/driver.py show sdd-define
```

`validate` é o gate para qualquer mudança em skill: rode antes e depois de
editar. Ele checa, por skill: `SKILL.md` presente, frontmatter com `---` de
fechamento, `name` e `description` não-vazios, `name` == pasta, description
≤ 1024 chars (warn). E, no repo: paridade `OWN_SKILLS` (workflow de sync) ×
pastas `sdd-*`/`custom-*` da raiz, índice do `README.md` × pastas existentes,
e campos do `databricks-skills.lock`.

Saída esperada num repo saudável:

```
41 skills parseadas em <raiz>
OK: 0 erros, 0 warning(s)
```

## Run (caminho humano)

Não existe. Sem `npm start`, sem servidor, sem GUI. O consumo real é carregar
o repo como Git Folder em `Workspace/.assistant/skills/` no Databricks — isso
só é verificável dentro de um workspace, não daqui.

## Test

Não há suite de testes no repo; `driver.py validate` é o smoke test. Para
testar o próprio driver, monte uma árvore quebrada num diretório temporário
(skill sem `SKILL.md`, frontmatter sem fechamento, `OWN_SKILLS` divergente),
copie o `driver.py` para `<tmp>/.claude/skills/x/` e rode `validate` — deve
sair com 1 e listar cada defeito. O driver deriva a raiz da própria
localização (`parents[3]`), então ele valida a árvore onde estiver copiado.

## Gotchas

- **`databricks-python-dev` tem `name: python-dev`** — não é bug: o upstream
  mapeia `.claude/skills/python-dev` → `databricks-python-dev` no sync. É a
  única exceção name≠pasta e está hardcoded em `NAME_EXCEPTIONS` no driver.
- **Frontmatter não é YAML uniforme:** skills `databricks-*` usam string
  quotada; `sdd-*`/`custom-*` usam block scalar `|` multilinha. O parser do
  driver cobre os dois — não troque por `yaml.safe_load` sem lembrar que não
  há PyYAML garantido no ambiente.
- **Pasta `sdd-*`/`custom-*` fora do `OWN_SKILLS` é erro fatal**: o workflow
  de sync semanal apaga qualquer pasta que não esteja na lista. O driver
  detecta isso mesmo se a pasta ainda não tiver `SKILL.md`.
- **`TEMPLATE/` é skill válida mas isenta do índice do README** (é o
  template de criação, não uma skill de uso).
- **`.claude/` é gitignored exceto `.claude/skills/`** — o carve-out no
  `.gitignore` (`.claude/*` + `!.claude/skills/`) existe para esta skill ser
  versionada; `settings.local.json` continua ignorado. Não reverta para
  `.claude/` inteiro.

## Troubleshooting

- **`validate` passou mas o sync apagou uma skill sua** → a pasta não estava
  em `OWN_SKILLS` quando o workflow rodou; o driver só protege se for rodado
  antes do merge. Rode `validate` em todo PR que criar pasta `sdd-*`/`custom-*`.
- **`no matches found: .../skills/*/SKILL.md` no zsh** → glob sem match
  aborta o comando no zsh (sem nullglob). Use o driver em vez de globs soltos.
