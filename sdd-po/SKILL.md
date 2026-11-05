---
name: sdd-po
description: |
  Etapa de planejamento do SDD (@sdd-workflow), no papel de Product Owner: lê como o repo testa,
  monta a matriz de testes e os níveis de gate, quebra a feature com spec aprovada em histórias
  (fatias verticais, pontos Fibonacci) e, dentro de cada história, em tasks atômicas, cada uma
  com os critérios que prova, as dependências, o teste e o nível de gate; e escreve uma prova por
  critério de aceite. Grava docs/planning/TASKS_<FEATURE>.md, roda o gate `sdd_gates tasks`, para
  para a aprovação do plano e, se houver jira_key, cria histórias e tasks no Jira sob o épico,
  com preview. Use depois do Define aprovado (e do ADR, se houver) e antes do Design, em features
  Grande ou Complexo; ou quando o usuário pedir para quebrar um épico em histórias e tasks.
---

# PO — histórias e tasks

Resultado: `docs/planning/TASKS_{FEATURE}.md` aprovado pelo usuário e, se houver `jira_key`, as
histórias e tasks criadas no Jira. Template: [`TASKS_TEMPLATE.md`](TASKS_TEMPLATE.md). Pontos:
[`estimation-guide.md`](estimation-guide.md). Provas: o guia `PROVAS.md` da skill `sdd-workflow`
(na pasta das skills, `sdd-workflow/PROVAS.md`). Gate: `sdd_gates tasks` (onde está e como rodar:
`@sdd-workflow`, seção Gates; `<gates>` é a pasta dele).

Posição no fluxo (Grande e Complexo): Define → ADR, se houver → **PO** → Design → Build → Ship.

**A feature vive só nos arquivos:** `docs/` e `.sdd/`. Não grave nada dela na memória do Genie
Code: nem o ponto em que parou, nem as respostas, nem a aprovação. A memória passa para outras
sessões sem revisão. Para retomar, a sessão seguinte lê o TASKS e o state.

---

## Passo 0 — Conferir a entrada

1. Leia o state (`.sdd/features/{FEATURE}/state.md`): tamanho, `jira_key`, pasta dos gates.
2. Rode o gate do Define com `--aprovado`, a partir da raiz do repo do projeto:

   ```bash
   cd <raiz do projeto> && PYTHONPATH=<gates> python3 -m sdd_gates define docs/specs/DEFINE_{FEATURE}.md --aprovado
   ```

   Não passou: **pare**. O plano só nasce de uma spec aprovada na última versão. Diga ao usuário
   o que o gate apontou e volte para o `@sdd-define`.
3. Se houver ADR (`docs/adr/ADR_{FEATURE}.md`), leia: as decisões dele valem para o plano.
4. Anote a versão aprovada do DEFINE. Ela vai na Identificação do TASKS, e o gate confere.

## Passo 1 — Matriz de testes e gates

Antes das tasks, descubra como o repo do projeto testa. Leia, nesta ordem: as regras de teste
do repo (`AGENTS.md`, guia de contribuição, `docs/`), a configuração (`pyproject.toml`,
`pytest.ini`, `conftest.py`, `databricks.yml`) e o CI (`.github/workflows`, `azure-pipelines`).
Depois abra de 5 a 10 testes que já existem: eles dizem o estilo, o lugar e o tipo, e são o
**piso**. O alvo de profundidade vem dos critérios do DEFINE.

- **Matriz de testes:** uma linha por camada que a feature toca, com o tipo de teste, a
  profundidade, onde fica e o nível de gate. Repo sem nenhum teste: **pergunte** ao usuário que
  tipos de teste e que comandos usar, com a matriz padrão do `PROVAS.md` como recomendação.
  Grave a pergunta no state antes de fazê-la, e a resposta, com as palavras dele, no turno em
  que chegar: o chat não sobrevive a uma sessão nova.
- **Gates:** os três níveis, cada um com o comando entre crases.

  | Nível | Quando |
  |---|---|
  | rápido | Task com teste unitário |
  | completo | Task com integração no target de desenvolvimento |
  | build | Última task de cada história; task só de configuração |

  Sem integração no repo: `nenhum — motivo` no nível completo. Nunca invente comando: use o que
  o repo roda (manifesto, Makefile, CI). Comando que não sabe se existe vira pergunta.
  O nível completo depende de deploy no target de desenvolvimento, e deploy pede o "ok" do
  usuário (raio de ação): diga isso ao apresentar o plano. Cada comando termina em menos de 10
  minutos; a ferramenta do agente não espera mais que isso.

## Passo 2 — Histórias

Uma história é uma **fatia vertical**: entrega algo que quem usa o dado consegue ver, sozinha.
"Só a bronze" ou "só os testes" não é fatia.

- Comece pelos requisitos do DEFINE. Cada requisito costuma virar uma história. Dois requisitos
  pequenos que só fazem sentido juntos podem dividir uma.
- Escreva cada uma como **Como** {quem usa, da seção "Quem usa o dado"}, **quero** {o que a
  fatia entrega}, **para** {o valor}.
- Ordene pelo valor: a primeira história é a menor fatia que já serve a alguém.

## Passo 3 — Pontos

Leia o `estimation-guide.md` e dê pontos a cada história: **1, 2, 3, 5, 8 ou 13**. Acima de 13,
quebre a história. Os pontos vão no título (`### H1: título — 5 pontos`).

Se o guia ainda não foi calibrado pelo time, diga isso ao usuário ao apresentar o plano: os
pontos valem como ordem de grandeza.

## Passo 4 — Tasks

Dentro de cada história, a tabela de tasks. Cada task é **um passo atômico**: um commit, um
resultado que dá para conferir. Se o título precisa de "e", são duas tasks.

| Coluna | O que vai |
|---|---|
| Task | `T1`, `T2`… em ordem no plano todo, na ordem em que serão feitas |
| O que faz | O passo, em uma frase |
| Critérios | Os `R<n>.<m>` do DEFINE que esta task prova; `—` em task de infraestrutura (recurso do bundle, schema) |
| Depende de | Só tasks que vêm antes; `—` se nenhuma |
| Teste | O teste que prova os critérios, **nascido do critério** e não da implementação: arquivo e o que confere |
| Gate | O nível da seção Gates: `rápido`, `completo` ou `build`. O comando fica lá |

- **Todo critério do DEFINE precisa de pelo menos uma task que o prove.**
- **O teste vai na task que cria a camada.** "Testado em outra task" não vale: é teste adiado.
  Se a camada só fica testável depois de outra task, junte as duas ou leve o teste para a task
  em que ele passa a rodar.
- **A última task de cada história roda o nível build.**
- Não decida aqui **como** construir (tabela streaming ou materialized view, AUTO CDC ou merge)
  nem em que arquivo: isso é do Design, depois. Se uma task depende de uma decisão do usuário
  que o DEFINE não tem, pare e volte ao `@sdd-define` como pergunta nova.

## Passo 5 — Provas

Leia o `PROVAS.md` e escreva a seção Provas: **uma prova por critério do DEFINE**. Cada uma é
uma afirmação observável, com o valor, citando o critério, e na linha de baixo o que a decide:

```markdown
**Build**: `databricks bundle validate -t dev`
**Run unit**: `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/unit -v -p no:cacheprovider`

**P3** — Um `payment_id` cujo registro mais recente é `refunded` não aparece na silver (R2.1)
Prova: run unit | tests/unit/test_status.py::test_r2_1_refunded_sai_da_silver PASSED
```

- `run <nome> | <linha>`: a linha que o teste imprime ao passar, com o marcador (`PASSED`). Sem
  ele, a mesma linha aparece quando o teste falha.
- Prova solta, um comando entre crases: o código de saída decide. Serve para o que não roda
  junto com o grupo (a leitura do bundle, uma query no target de desenvolvimento).
- `passeio — …`: o que a consulta no target de desenvolvimento mostra, para o que só se vê
  rodando.
- **Build:** os comandos de build, lint e validação que o repo já tem. Repo novo, sem build:
  `**Build**: nenhum — motivo`, e o que vai existir depois entra como prova dos critérios que
  dependem dele. O `--executar` roda essa linha antes da primeira task: vermelho para o Build.
- Agendamento: a prova confere o target que o critério cita, pela configuração resolvida
  (`databricks bundle validate -t <target> -o json`), e confere `PAUSED` no target de
  desenvolvimento.

O Design, depois, se ajusta a estas provas. Se precisar mudar uma, o plano ganha versão nova e
volta para aprovação.

## Passo 6 — Gate

```bash
cd <raiz do projeto> && PYTHONPATH=<gates> python3 -m sdd_gates tasks docs/planning/TASKS_{FEATURE}.md
```

Rode a partir da raiz do repo do projeto. O gate lê também o DEFINE da feature e confere a
matriz, os gates, as tasks e as provas. Exit diferente de 0 → corrija e rode de novo. Cada
aviso: corrija, ou explique ao usuário por que fica. Se não conseguir executar, faça as mesmas
checagens lendo os arquivos e **diga ao usuário que o gate não rodou**.

Copie para o state a última linha da saída do gate, como saiu. Diga "o gate passou" só depois de
ver essa linha.

## Passo 7 — Apresentar e parar

Mostre o plano em resumo e **pare**. É a segunda parada humana do contrato de execução.

```markdown
## Plano — {Feature}  ·  {N} histórias · {pontos} pontos · {M} tasks · {P} provas

| História | Pontos | Tasks | Critérios |
|----------|--------|-------|-----------|
| H1: … | 5 | T1–T3 | R1.1, R1.2, R1.3 |

Testes: {camadas da matriz} · Build: {comandos ou "nenhum — motivo"}
Arquivo: `docs/planning/TASKS_{FEATURE}.md` · Gate: {última linha da saída}
```

Diga se o Jira vai receber as histórias (há `jira_key`) ou não.

## Passo 8 — Gravar a aprovação

Quando o usuário aprovar, grave na seção Aprovação a versão e as palavras dele:

```markdown
**Aprovado**: 2026-11-02 — v1.0 — usuário: "plano aprovado"
```

A versão é a última do Histórico de revisões; aprovar não cria versão. Nunca grave uma aprovação
que ele não deu. Depois rode o gate com `--aprovado` e copie a última linha para o state.

## Passo 9 — Jira (só com `jira_key`)

Sem `jira_key` no state, pule: o plano vale igual, e o state registra "Jira pendente".

| Ferramenta MCP | Uso |
|---|---|
| `jira_get_issue` | Confirmar o épico do state |
| `jira_create_issue` | Criar cada história (pai: o épico, com os pontos) e cada task (pai: a história) |

1. Confirme o épico com `jira_get_issue(jira_key)`. Opere **só** sob esse épico; nunca use busca
   (`jira_search`) para achar onde criar.
2. Mostre o que vai ser criado (histórias, pontos, tasks) e espere o "ok" para essa ação.
3. Crie e grave cada chave na linha `**Jira:**` da história no TASKS. Gravar as chaves não cria
   versão nova.

## Passo 10 — State e fim de etapa

1. Atualize o state: etapa PO concluída, artefato, a linha do gate `--aprovado`, a aprovação
   (versão e palavras) e as chaves criadas no Jira.
2. Chame `@sdd-doc` se houver `jira_key` (comentário no épico com o resumo do plano; ele faz
   preview antes).
3. Proponha o próximo passo: `@sdd-design`.

**Plano mudou depois de aprovado** (task nova, dependência nova, história quebrada, inclusive
por causa do Design): versão nova no Histórico de revisões, Status "Em revisão", gate de novo e
aprovação nova. A aprovação antiga fica como texto simples, sem o negrito.

---

## Termos (PT-BR ↔ inglês)

| Aqui | Referência em inglês |
|---|---|
| História | *user story* |
| Fatia vertical | *vertical slice* |
| Task atômica | *atomic task* |
| Pontos (Fibonacci) | *story points* |
| Épico | *epic* |
| Matriz de testes | *test coverage matrix* |
| Nível de gate | *gate check level* |
| Prova | *proof* (de um *check*) |

---

> A task atômica com teste e gate, a dependência que só aponta para trás, a matriz de testes, os
> níveis de gate, a prova por critério e o gate do plano por script foram adaptados do
> [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills) (Tech Leads Club,
> CC-BY-4.0). Créditos em `THIRD_PARTY_NOTICES.md`.
