---
name: sdd-design
description: |
  Etapa Design do SDD (@sdd-workflow): depois do plano de tarefas aprovado, decide como cada task
  vira um componente no Databricks (tabela, pipeline Lakeflow, job, recurso do bundle, módulo),
  o que se reaproveita do repo, qual skill @databricks-* constrói cada componente e as decisões
  técnicas com a alternativa descartada. Grava docs/designs/DESIGN_<FEATURE>.md, conferido pelo
  gate `sdd_gates tasks`. Use em features Grande ou Complexo, depois do @sdd-po e antes do
  @sdd-build; ou quando o usuário perguntar como estruturar uma feature já planejada.
---

# Design — como a feature fica de pé

Resultado: `docs/designs/DESIGN_{FEATURE}.md`, com todo componente ligado aos critérios e às
tasks do plano. Template: [`DESIGN_TEMPLATE.md`](DESIGN_TEMPLATE.md). Gate: `sdd_gates tasks`,
que lê o DESIGN quando ele existe (onde está e como rodar: `@sdd-workflow`, seção Gates).

Posição no fluxo (Grande e Complexo): Define → ADR, se houver → PO → **Design** → Build → Ship.

O Design responde **como**. O **quê** está no DEFINE e a **ordem** está no TASKS, os dois
aprovados. O Design não muda nenhum dos dois por conta própria.

**A feature vive só nos arquivos:** `docs/` e `.sdd/`. Não grave nada dela na memória do Genie
Code: nem o ponto em que parou, nem as decisões. A memória passa para outras sessões sem
revisão. Para retomar, a sessão seguinte lê o DESIGN e o state.

---

## Passo 0 — Conferir a entrada

1. Leia o state: tamanho, pasta dos gates, etapas concluídas.
2. Rode o gate do plano com `--aprovado`, a partir da raiz do repo do projeto:

   ```bash
   PYTHONPATH=<gates> python3 -m sdd_gates tasks docs/planning/TASKS_{FEATURE}.md --aprovado
   ```

   Ele confere também que o DEFINE está aprovado na versão que o plano cita. Não passou:
   **pare**, diga o que o gate apontou e volte para a etapa que falta.
3. Leia o DEFINE (contrato de dados, contexto técnico), o TASKS e o ADR, se houver. O ADR é
   vinculante: o que ele decidiu não se reabre aqui.

## Passo 1 — O que já existe

Antes de desenhar, olhe o repo do projeto: o pipeline vizinho, o `databricks.yml` e os recursos
do bundle, utilitários, a convenção de nomes, os testes e as fixtures que já existem. Use
`@databricks-data-discovery` para as tabelas de origem.

Cada achado que entra na feature vai para "O que já existe e será reaproveitado". Não achou
nada: uma linha dizendo onde procurou. Seguir o padrão do repo vale mais que um padrão melhor que
ninguém mais usa.

## Passo 2 — Componentes

Um componente é uma coisa que vai existir no repo ou no workspace: uma tabela, uma view, um
pipeline, um job, um recurso do bundle, um módulo Python.

1. Para cada task do plano, diga em qual componente ela trabalha. **Toda task aparece em pelo
   menos um componente**; o gate confere.
2. Para cada componente, os critérios do DEFINE que ele atende.
3. **Antes de escolher o tipo**, leia a skill `@databricks-*` que constrói aquele componente
   (`@databricks-pipelines`, `@databricks-jobs`, `@databricks-dabs`, `@databricks-unity-catalog`…).
   Ela vai na coluna "Constrói com". Nunca invente API, parâmetro ou opção: o que a skill e a
   documentação oficial não mostram, você não usa.

## Passo 3 — Dados

Só o que o DEFINE não fixou: chave, modo de escrita (append, merge, AUTO CDC, overwrite),
clustering ou partição, checkpoint. Se o DEFINE fixou e o Design precisa de outra coisa, isso
é mudança de spec: volte ao `@sdd-define` com a pergunta.

## Passo 4 — Decisões

Registre só as escolhas técnicas que tinham mais de um caminho real, cada uma com a alternativa
descartada, o motivo em uma linha e a base: a skill `@databricks-*`, o arquivo do repo que mostra
o padrão, ou o ADR.

Escolha que muda o comportamento do dado (o que entra, o que sai, quando, com que regra) não é
decisão de design, é do usuário: vira pergunta nova no Registro do DEFINE, pelo `@sdd-define`.

## Passo 5 — Conferir com o plano

Se o Design mostrou que falta uma task, que uma dependência está errada ou que uma história
precisa ser quebrada: atualize o TASKS (versão nova, Status "Em revisão") e peça aprovação nova
do plano (`@sdd-po`, Passo 6). Nunca ajuste o plano aprovado em silêncio.

Rode o gate, que agora lê o DESIGN junto:

```bash
PYTHONPATH=<gates> python3 -m sdd_gates tasks docs/planning/TASKS_{FEATURE}.md --aprovado
```

Exit diferente de 0 → corrija e rode de novo. Cada aviso: corrija, ou explique ao usuário por que
fica. Copie para o state a última linha da saída, como saiu; diga "o gate passou" só depois de
vê-la. Se não conseguir executar, faça as checagens lendo os arquivos e diga que o gate não
rodou.

## Passo 6 — Apresentar e fim de etapa

1. Mostre ao usuário os componentes, o que será reaproveitado e as decisões. Se ele discordar
   de uma decisão, ajuste antes do Build.
2. Atualize o state: etapa Design concluída, artefato e a linha do gate.
3. Chame `@sdd-doc` se houver `jira_key` (comentário no épico; ele faz preview antes).
4. Proponha o próximo passo: `@sdd-build`, que segue as tasks na ordem do plano.

---

## Termos (PT-BR ↔ inglês)

| Aqui | Referência em inglês |
|---|---|
| Componente | *component* |
| Reaproveitamento | *code reuse* |
| Decisão técnica | *tech decision* |
| Alternativa descartada | *rejected alternative* |

---

> A análise do que já existe para reaproveitar, os componentes e as decisões técnicas com o
> motivo foram adaptados do [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills)
> (Tech Leads Club, CC-BY-4.0) para dados no Databricks. Créditos em `THIRD_PARTY_NOTICES.md`.
