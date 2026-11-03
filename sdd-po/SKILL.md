---
name: sdd-po
description: |
  Etapa de planejamento do SDD (@sdd-workflow), no papel de Product Owner: quebra a feature com
  spec aprovada em histórias (fatias verticais, pontos Fibonacci) e, dentro de cada história, em
  tasks atômicas, cada uma com os critérios de aceite que prova, as dependências, o teste e o
  gate. Grava docs/planning/TASKS_<FEATURE>.md, roda o gate `sdd_gates tasks`, para para a
  aprovação do plano e, se houver jira_key, cria histórias e tasks no Jira sob o épico, com
  preview. Use depois do Define aprovado (e do ADR, se houver) e antes do Design, em features
  Grande ou Complexo; ou quando o usuário pedir para quebrar um épico em histórias e tasks.
---

# PO — histórias e tasks

Resultado: `docs/planning/TASKS_{FEATURE}.md` aprovado pelo usuário e, se houver `jira_key`, as
histórias e tasks criadas no Jira. Template: [`TASKS_TEMPLATE.md`](TASKS_TEMPLATE.md). Pontos:
[`estimation-guide.md`](estimation-guide.md). Gate: `sdd_gates tasks` (onde está e como rodar:
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
   PYTHONPATH=<gates> python3 -m sdd_gates define docs/specs/DEFINE_{FEATURE}.md --aprovado
   ```

   Não passou: **pare**. O plano só nasce de uma spec aprovada na última versão. Diga ao usuário
   o que o gate apontou e volte para o `@sdd-define`.
3. Se houver ADR (`docs/adr/ADR_{FEATURE}.md`), leia: as decisões dele valem para o plano.
4. Anote a versão aprovada do DEFINE. Ela vai na Identificação do TASKS, e o gate confere.

## Passo 1 — Histórias

Uma história é uma **fatia vertical**: entrega algo que quem usa o dado consegue ver, sozinha.
"Só a bronze" ou "só os testes" não é fatia.

- Comece pelos requisitos do DEFINE. Cada requisito costuma virar uma história. Dois requisitos
  pequenos que só fazem sentido juntos podem dividir uma.
- Escreva cada uma como **Como** {quem usa, da seção "Quem usa o dado"}, **quero** {o que a
  fatia entrega}, **para** {o valor}.
- Ordene pelo valor: a primeira história é a menor fatia que já serve a alguém.

## Passo 2 — Pontos

Leia o `estimation-guide.md` e dê pontos a cada história: **1, 2, 3, 5, 8 ou 13**. Acima de 13,
quebre a história. Os pontos vão no título (`### H1: título — 5 pontos`).

Se o guia ainda não foi calibrado pelo time, diga isso ao usuário ao apresentar o plano: os
pontos valem como ordem de grandeza.

## Passo 3 — Tasks

Dentro de cada história, a tabela de tasks. Cada task é **um passo atômico**: um commit, um
resultado que dá para conferir. Se o título precisa de "e", são duas tasks.

| Coluna | O que vai |
|---|---|
| Task | `T1`, `T2`… em ordem no plano todo, na ordem em que serão feitas |
| O que faz | O passo, em uma frase |
| Critérios | Os `R<n>.<m>` do DEFINE que esta task prova; `—` em task de infraestrutura (recurso do bundle, schema) |
| Depende de | Só tasks que vêm antes; `—` se nenhuma |
| Teste | O teste que prova os critérios, **nascido do critério** e não da implementação: arquivo e o que confere |
| Gate | O comando que fecha a task: `pytest …`, `databricks bundle validate`, a query de verificação no target de desenvolvimento |

**Todo critério do DEFINE precisa de pelo menos uma task que o prove.** Que tipo de prova:

| O critério fala de… | Prova |
|---|---|
| Regra sobre as linhas (chave, filtro, desempate, cálculo) | pytest com DataFrames em memória e `assertDataFrameEqual` (base PySpark 4.0) |
| Expectation do Lakeflow (descarte, contagem) | Update do pipeline no target de desenvolvimento + consulta ao event log |
| Horário, agendamento, volume | Query de verificação no target de desenvolvimento |
| Alerta, permissão, configuração | `databricks bundle validate` + conferência do recurso no bundle |

Não decida aqui **como** construir (tabela streaming ou materialized view, AUTO CDC ou merge):
isso é do Design, depois. Se uma task depende de uma decisão do usuário que o DEFINE não tem,
pare e volte ao `@sdd-define` como pergunta nova.

## Passo 4 — Gate

```bash
PYTHONPATH=<gates> python3 -m sdd_gates tasks docs/planning/TASKS_{FEATURE}.md
```

Rode a partir da raiz do repo do projeto. O gate lê também o DEFINE da feature. Exit diferente
de 0 → corrija e rode de novo. Cada aviso: corrija, ou explique ao usuário por que fica. Se não
conseguir executar, faça as mesmas checagens lendo os arquivos e **diga ao usuário que o gate não
rodou**.

Copie para o state a última linha da saída do gate, como saiu. Diga "o gate passou" só depois de
ver essa linha.

## Passo 5 — Apresentar e parar

Mostre o plano em resumo e **pare**. É a segunda parada humana do contrato de execução.

```markdown
## Plano — {Feature}  ·  {N} histórias · {pontos} pontos · {M} tasks

| História | Pontos | Tasks | Critérios |
|----------|--------|-------|-----------|
| H1: … | 5 | T1–T3 | R1.1, R1.2, R1.3 |

Arquivo: `docs/planning/TASKS_{FEATURE}.md` · Gate: {última linha da saída}
```

Diga se o Jira vai receber as histórias (há `jira_key`) ou não.

## Passo 6 — Gravar a aprovação

Quando o usuário aprovar, grave na seção Aprovação a versão e as palavras dele:

```markdown
**Aprovado**: 2026-11-02 — v1.0 — usuário: "plano aprovado"
```

A versão é a última do Histórico de revisões; aprovar não cria versão. Nunca grave uma aprovação
que ele não deu. Depois rode o gate com `--aprovado` e copie a última linha para o state.

## Passo 7 — Jira (só com `jira_key`)

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

## Passo 8 — State e fim de etapa

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

---

> A task atômica com teste e gate, a dependência que só aponta para trás e o gate do plano por
> script foram adaptados do [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills)
> (Tech Leads Club, CC-BY-4.0). Créditos em `THIRD_PARTY_NOTICES.md`.
