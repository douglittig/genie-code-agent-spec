---
name: sdd-design
description: |
  Etapa Design do SDD (@sdd-workflow): depois do plano de tarefas aprovado, apresenta 2 ou 3
  abordagens e confirma uma com o usuário; decide como cada task vira um componente no
  Databricks (tabela, pipeline Lakeflow, job, recurso do bundle, módulo) e em que lugar, onde
  cada regra roda para o teste alcançar, o que se reaproveita do repo, qual skill @databricks-*
  constrói cada componente, os riscos com mitigação, o tratamento de dado ruim e as decisões
  técnicas com a alternativa descartada. Grava docs/designs/DESIGN_<FEATURE>.md, conferido pelo
  gate `sdd_gates tasks`. Use em features Grande ou Complexo, depois do @sdd-po e antes do
  @sdd-build; ou quando o usuário perguntar como estruturar uma feature já planejada.
---

# Design — como a feature fica de pé

Resultado: `docs/designs/DESIGN_{FEATURE}.md`, com todo componente ligado aos critérios e às
tasks do plano. Template: [`DESIGN_TEMPLATE.md`](DESIGN_TEMPLATE.md). Gate: `sdd_gates tasks`,
que lê o DESIGN quando ele existe (onde está e como rodar: `@sdd-workflow`, seção Gates).

Posição no fluxo (Grande e Complexo): Define → ADR, se houver → PO → **Design** → Build → Ship.

O Design responde **como**. O **quê** está no DEFINE, a **ordem** e as **provas** estão no
TASKS, os dois aprovados. O Design se ajusta às provas e não muda nenhum dos dois por conta
própria.

**A feature vive só nos arquivos:** `docs/` e `.sdd/`. Não grave nada dela na memória do Genie
Code: nem o ponto em que parou, nem as decisões. A memória passa para outras sessões sem
revisão. Para retomar, a sessão seguinte lê o DESIGN e o state.

**Relate só o que a ferramenta confirmou.** "O gate passou" vem depois da linha de saída dele.

---

## Passo 0 — Conferir a entrada

1. Leia o state: tamanho, pasta dos gates, etapas concluídas.
2. Rode o gate do plano com `--aprovado`, a partir da raiz do repo do projeto:

   ```bash
   cd <raiz do projeto> && PYTHONPATH=<gates> python3 -m sdd_gates tasks docs/planning/TASKS_{FEATURE}.md --aprovado
   ```

   Ele confere também que o DEFINE está aprovado na versão que o plano cita. Não passou:
   **pare**, diga o que o gate apontou e volte para a etapa que falta.
3. Leia o DEFINE (contrato de dados, contexto técnico), o TASKS (tasks e provas) e o ADR, se
   houver. O ADR é vinculante: o que ele decidiu não se reabre aqui.

## Passo 1 — O que já existe

Antes de desenhar, olhe o repo do projeto: o pipeline vizinho, o `databricks.yml` e os recursos
do bundle, utilitários, a convenção de nomes, os testes e as fixtures que já existem. Use
`@databricks-data-discovery` para as tabelas de origem.

- Cada achado que entra na feature vai para "O que já existe e será reaproveitado". Não achou
  nada: uma linha dizendo onde procurou. Seguir o padrão do repo vale mais que um padrão melhor
  que ninguém mais usa.
- Enquanto lê, anote os **riscos** nas áreas que a feature toca: código frágil, dívida técnica,
  PII ou grant aberto, varredura completa de tabela, small files, skew, evolução de schema, teste
  que falta no que a feature usa. Eles vão para o Passo 6.

## Passo 2 — Abordagens

Apresente **2 ou 3 abordagens** que entregam o **mesmo escopo** (nunca um escopo menor como
alternativa), cada uma com prós e contras, a recomendada primeiro. Exemplos em dados: materialized
view × tabela streaming; AUTO CDC × `MERGE` num job; pipeline novo × etapa num pipeline que já
existe.

Mostre ao usuário e **espere a confirmação** antes de detalhar os componentes. Grave com as
palavras dele, no turno em que chegar:

```markdown
**Confirmada**: A1 — usuário: "vai de view, com a regra testável"
```

Nunca grave uma confirmação que ele não deu. Se ele escolher uma abordagem que muda o que o
DEFINE pede, é mudança de spec: volte ao `@sdd-define`.

## Passo 3 — Componentes

Um componente é uma coisa que vai existir no repo ou no workspace: uma tabela, uma view, um
pipeline, um job, um recurso do bundle, um módulo Python.

1. Para cada task do plano, diga em qual componente ela trabalha. **Toda task aparece em pelo
   menos um componente**; o gate confere.
2. **Uma task, um lugar.** O "Onde fica" de cada componente é o arquivo ou a pasta. Task que cai
   em componentes de lugares diferentes precisa ser quebrada: o plano ganha versão nova e volta
   para aprovação (Passo 8). O gate avisa.
3. Para cada componente, os critérios do DEFINE que ele atende.
4. **Antes de escolher o tipo**, leia a skill `@databricks-*` que constrói aquele componente
   (`@databricks-pipelines`, `@databricks-jobs`, `@databricks-dabs`, `@databricks-unity-catalog`…).
   Ela vai na coluna "Constrói com". Nunca invente API, parâmetro ou opção: o que a skill e a
   documentação oficial não mostram, você não usa.

## Passo 4 — Onde a regra roda

Toda regra que muda o que o consumidor vê (filtro, chave, desempate, cálculo, quarentena)
**roda numa função Python que o teste em memória alcança**. O pipeline só liga as funções.

- Na seção "Onde a regra roda", cada critério de regra com a função (`arquivo::função`) e o tipo
  de prova.
- Regra que só pode existir no SQL do pipeline ou no AUTO CDC tem prova de integração no target
  de desenvolvimento. Diga isso na tabela.
- Se a prova aprovada no TASKS para um critério é unitária e a regra não pode rodar numa função,
  a prova muda: o plano ganha versão nova e volta para aprovação (Passo 8). O Design não troca
  a prova em silêncio.

## Passo 5 — Dados

Só o que o DEFINE não fixou: chave, modo de escrita (append, merge, AUTO CDC, overwrite),
clustering ou partição, checkpoint. Se o DEFINE fixou e o Design precisa de outra coisa, isso
é mudança de spec: volte ao `@sdd-define` com a pergunta.

**Agendamento:** o recurso base do bundle **nunca fixa `pause_status`**. O `mode: development`
pausa o agendamento só quando o recurso não fixa: um `pause_status: UNPAUSED` no recurso vence o
preset e deixa o job rodando no target de desenvolvimento. O `UNPAUSED` vai só no target de
produção. Os exemplos das skills oficiais fixam `UNPAUSED` no recurso: não copie essa parte.

## Passo 6 — Riscos e dado ruim

- **Riscos e pontos de atenção:** cada risco do Passo 1 com onde está, o impacto e a
  **mitigação** (o design já resolve, ou uma task resolve). Nada encontrado: "Nenhum encontrado"
  e onde você olhou.
- **Dado ruim e falhas:** cada cenário que a feature encontra (nulo, duplicado, atrasado, origem
  vazia ou indisponível, schema mudou), o tratamento e o que o consumidor vê. O tratamento sai do
  DEFINE (rubrica, quarentena, expectation). Tratamento que o DEFINE não decidiu e muda o
  comportamento do dado é pergunta para o usuário, pelo `@sdd-define`.

## Passo 7 — Decisões

Registre só as escolhas técnicas que tinham mais de um caminho real, cada uma com a alternativa
descartada, o motivo em uma linha e a base: a skill `@databricks-*`, o arquivo do repo que mostra
o padrão, ou o ADR.

Escolha que muda o comportamento do dado (o que entra, o que sai, quando, com que regra) não é
decisão de design, é do usuário: vira pergunta nova no Registro do DEFINE, pelo `@sdd-define`.

## Passo 8 — Conferir com o plano

Se o Design mostrou que falta uma task, que uma dependência está errada, que uma task precisa ser
quebrada ou que uma prova precisa mudar: atualize o TASKS (versão nova, Status "Em revisão") e
peça aprovação nova do plano (`@sdd-po`, Passo 8). Nunca ajuste o plano aprovado em silêncio.

Rode o gate, que agora lê o DESIGN junto:

```bash
cd <raiz do projeto> && PYTHONPATH=<gates> python3 -m sdd_gates tasks docs/planning/TASKS_{FEATURE}.md --aprovado
```

Exit diferente de 0 → corrija e rode de novo. Cada aviso: corrija, ou explique ao usuário por que
fica. Copie para o state a última linha da saída, como saiu; diga "o gate passou" só depois de
vê-la. Se não conseguir executar, faça as checagens lendo os arquivos e diga que o gate não
rodou.

## Passo 9 — Apresentar e fim de etapa

1. Mostre ao usuário os componentes, onde cada regra roda, o que será reaproveitado, os riscos e
   as decisões. Se ele discordar de uma decisão, ajuste antes do Build.
2. Atualize o state: etapa Design concluída, artefato, a abordagem confirmada e a linha do gate.
3. Chame `@sdd-doc` se houver `jira_key` (comentário no épico; ele faz preview antes).
4. Proponha o próximo passo: `@sdd-build`, que começa rodando `sdd_gates tasks … --executar`.

---

## Termos (PT-BR ↔ inglês)

| Aqui | Referência em inglês |
|---|---|
| Abordagem | *approach* |
| Componente | *component* |
| Onde a regra roda | *where the rules run* |
| Reaproveitamento | *code reuse* |
| Riscos e pontos de atenção | *risks & concerns* |
| Dado ruim e falhas | *error handling strategy* |
| Decisão técnica | *tech decision* |
| Alternativa descartada | *rejected alternative* |

---

> As abordagens confirmadas antes dos componentes, a análise do que já existe para reaproveitar,
> a regra numa camada que o teste alcança, os riscos com mitigação, a estratégia de erro e as
> decisões técnicas com o motivo foram adaptados do
> [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills) (Tech Leads Club,
> CC-BY-4.0) para dados no Databricks. Créditos em `THIRD_PARTY_NOTICES.md`.
