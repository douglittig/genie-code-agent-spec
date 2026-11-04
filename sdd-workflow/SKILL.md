---
name: sdd-workflow
description: |
  Orquestrador do Spec-Driven Development (SDD) para o Genie Code em projetos de dados no
  Databricks. Use de forma PROATIVA quando o usuário pedir uma feature, um pipeline, uma tabela,
  um job ou uma correção a partir de um requisito, de uma página do Confluence ou de um ticket do
  Jira; e quando pedir para retomar, pausar ou continuar uma feature. Decide o tamanho da feature
  (Pequeno, Médio, Grande, Complexo), escolhe só as etapas necessárias, aplica o contrato de
  execução (aprovação gravada, teste derivado do critério, um commit por tarefa) e o raio de ação
  no Databricks, e roteia cada etapa para a skill dedicada (@sdd-define, @sdd-staff-engineer,
  @sdd-po, @sdd-design, @sdd-build, @sdd-ship, @sdd-doc).
---

# SDD Workflow — Genie Code

Esta skill decide **quanto processo** uma feature precisa e garante as regras que valem em todas
as etapas. O trabalho de cada etapa fica na skill dedicada, que carrega o próprio template.

Ordem de leitura: **Contrato de execução** → **Tamanho da feature** → a skill da etapa atual.

---

## Contrato de execução

Vale em toda feature, mesmo que nenhuma outra skill tenha sido aberta.

1. **Pergunte, depois pare para aprovação.** O que é decisão do usuário (escopo, comportamento
   do dado, desvio do que está no Confluence) é perguntado **antes** de apresentar a spec, com a
   sua recomendação. Suposição nunca substitui pergunta. Sem ninguém para responder, termine o
   turno com as perguntas.
   - Há duas paradas humanas: **aprovar a spec** e **aprovar o plano de tarefas** (no tamanho
     Médio, só a spec).
   - Toda aprovação é gravada no artefato, com a versão aprovada e as palavras do usuário:
     `**Aprovado**: AAAA-MM-DD — v<versão> — usuário: "<palavras dele>"`. Nunca grave uma
     aprovação que o usuário não deu.
   - Aprovação vale para uma versão. Mudou o artefato depois: versão nova no histórico, Status
     "Em revisão" e aprovação nova. Os gates reprovam aprovação de versão antiga.
   - Toda pergunta vai para o arquivo da etapa **antes** de ser feita, e toda resposta do usuário
     **no mesmo turno**. O chat não sobrevive a uma sessão nova nem a um chat novo.
2. **Teste nasce do critério de aceite** (*acceptance criterion*) e confere o resultado que a
   spec define. Nunca espelha a implementação.
3. **Uma tarefa só termina quando o gate passa.** Quem decide é o test runner, não a
   autoavaliação. Um commit por tarefa; nunca agrupe tarefas. Nunca enfraqueça, pule ou apague
   um teste para ele passar.
4. **Respeite o raio de ação** (*blast radius*) no Databricks — seção abaixo.
5. **Fatos se consultam, decisões se perguntam.** Para fatos, siga esta ordem: o código e as
   convenções do repo → os artefatos em `docs/` e `.sdd/` → as skills `@databricks-*` → a
   documentação oficial. Nunca invente API, parâmetro ou comportamento: "não encontrei
   documentação para isso" vale mais que um palpite plausível.
6. **A feature vive nos arquivos, nunca na memória do Genie Code.** Estado, decisões e respostas
   do usuário vão para `docs/` e `.sdd/`. Não grave a feature na memória do assistente: ela passa
   para outras sessões, inclusive a do Verifier, sem passar por revisão.
7. **Relate só o que a ferramenta confirmou.** "Passou", "gravei", "fiz o commit" vêm depois da
   saída que mostra isso, nunca antes. Ainda não viu o resultado: diga que ainda não viu.

---

## Tamanho da feature (*auto-sizing*)

**A complexidade define a profundidade, não um pipeline fixo.** Antes de começar, classifique a
feature, anuncie o tamanho em uma linha com o motivo e deixe o usuário corrigir. Grave no state,
que nasce no começo do Define (Passo 0 do `@sdd-define`).

| Tamanho | Exemplos em dados | Etapas |
|---|---|---|
| **Pequeno** | Corrigir um filtro, renomear coluna, ajustar uma query; ≤ 3 arquivos, cabe numa frase | Spec de uma linha no chat (critério + teste) → `@sdd-build` |
| **Médio** | Tabela ou coluna derivada nova num pipeline que já existe; job novo com padrão conhecido; < 10 tarefas | `@sdd-define` (curto) → `@sdd-build` → `@sdd-ship` |
| **Grande** | Pipeline novo, mudança no modelo de dados, vários componentes | `@sdd-define` → `@sdd-po` → `@sdd-design` → `@sdd-build` → `@sdd-ship`; `@sdd-staff-engineer` antes do PO se houver decisão de arquitetura |
| **Complexo** | Domínio novo, migração, vários sistemas, requisito ambíguo | `@sdd-define` (com áreas cinzentas) → `@sdd-staff-engineer` → `@sdd-po` → `@sdd-design` → `@sdd-build` → `@sdd-ship` |

**Regras:**
- **Define e Build sempre existem.** No Pequeno, o Define é a spec de uma linha no chat, sem arquivo.
- **Áreas cinzentas** (exploração de opções dentro do `@sdd-define`) só no Complexo, ou quando a ideia ainda é vaga.
- **Staff Engineer (ADR)** quando há decisão de arquitetura: padrão novo, tecnologia nova, trade-off
  com consequência duradoura.
- **PO** sempre no Grande e no Complexo: quebra a feature em histórias com pontos e tasks
  atômicas (`docs/planning/TASKS_{FEATURE}.md`). O plano é a segunda parada humana. O Jira entra
  quando há `jira_key`.
- **Design** sempre no Grande e no Complexo, depois do plano aprovado: diz como cada task vira um
  componente no Databricks. Se precisar de task nova, o plano ganha versão nova e volta para
  aprovação.
- **Válvula de segurança:** o Build sempre começa listando os passos atômicos. Se a lista passar de
  5 passos, ou tiver dependências complicadas, **pare** e suba o tamanho: a etapa foi pulada por
  engano.

---

## Raio de ação no Databricks (*blast radius*)

Aprovar a spec e o plano libera **só o que é local ou do ambiente de desenvolvimento**.

| Liberado pela aprovação | Exige um "ok" explícito, para aquela ação |
|---|---|
| Editar código, testes e docs na branch da feature | `git push` para a `main`, force-push, merge, abrir PR |
| Commit na branch da feature (no Git Folder do Databricks, commit e push saem juntos: na branch da feature, liberado) | `databricks bundle deploy` em qualquer target que não seja o de desenvolvimento |
| Rodar testes no compute | Escrever, alterar ou apagar tabela fora do schema de desenvolvimento |
| `databricks bundle validate` | `DROP`, `TRUNCATE` ou `DELETE` em tabela que esta feature não criou |
| `databricks bundle deploy` no target de desenvolvimento (`mode: development`) e rodar o job ou pipeline ali, **com o agendamento pausado lá** (abaixo) | Ativar schedule ou trigger em qualquer target, inclusive deixar um agendamento rodando no desenvolvimento |
| Ler tabelas e metadados que o usuário já pode ler | `GRANT`/`REVOKE` e qualquer mudança de permissão no Unity Catalog; criar ou alterar cluster, SQL warehouse, endpoint ou segredo |

Na dúvida se uma ação sai do ambiente de desenvolvimento, trate como "exige ok".

**O `mode: development` só pausa o agendamento que não fixa `pause_status`.** Ele liga
`presets.trigger_pause_status: PAUSED`, mas um `pause_status: UNPAUSED` no recurso vence o preset
e deixa o job rodando no desenvolvimento ([deployment modes](https://docs.databricks.com/aws/en/dev-tools/bundles/deployment-modes)).
O recurso base nunca fixa `pause_status`; o `UNPAUSED` vai só no target de produção. Antes do
deploy no desenvolvimento, confira com `databricks bundle validate -t <dev> -o json`: todo
agendamento precisa sair `PAUSED`.

Trabalhe sempre na branch da feature, criada antes do primeiro arquivo. No Genie Code, a própria
plataforma bloqueia o push para a `main`, mesmo com o ok do usuário.

---

## Gates (pacote `sdd-gates`)

Um gate é um script que decide, por código, se a etapa pode avançar. O código dos gates fica num
**segundo Git Folder deste mesmo repo, fora de `.assistant`**, chamado `sdd-gates`. Versão mínima
exigida por estas skills: **0.4.0**.

Duas coisas que o Genie Code bloqueia, e que você não deve tentar contornar:
- executar scripts dentro de `.assistant/skills` (nem copiando o código de lá);
- `pip install` direto do GitHub.

1. **Ache a pasta dos gates** (`<gates>`): a do state da feature, se houver; senão tente
   `/Workspace/Users/<usuário>/sdd-gates/gates` e depois `/Workspace/Shared/sdd-gates/gates`.
   Não achou: pergunte ao usuário onde está o Git Folder `sdd-gates` (ou peça para ele criar,
   README do repo, Passo 2b). Grave o caminho no state.
2. **Confira a versão:** `PYTHONPATH=<gates> python3 -m sdd_gates --version`. Abaixo da mínima,
   peça ao usuário um pull no Git Folder `sdd-gates`; não rode gate velho.
3. **Rode o gate** a partir da raiz do repo do projeto:
   `PYTHONPATH=<gates> python3 -m sdd_gates <gate> …`. Nada é instalado.
   Exit 0: passou. Exit 1: não passou, e a saída diz o que corrigir. Exit 2: erro de uso.
   Copie para o state a última linha da saída, como saiu (ex.:
   `sdd_gates define DEFINE_X.md: OK — 0 aviso(s)`). É a prova de que o gate rodou.
4. Se não conseguir executar, faça as checagens lendo o artefato, registre no state que o gate
   não rodou e diga isso ao usuário. **Nunca grave "gate ✅" sem ter rodado o gate.**

| Gate | Etapa | Comando |
|---|---|---|
| `define` | Define | `PYTHONPATH=<gates> python3 -m sdd_gates define docs/specs/DEFINE_{FEATURE}.md` (com `--aprovado` antes do PO ou do Build) |
| `define … --executar` | Antes da 1ª mudança do Build, no Médio | O mesmo do `--aprovado` + roda a linha `**Build**` das Provas uma vez: vermelho antes de mudar = parar |
| `tasks` | PO e Design | `PYTHONPATH=<gates> python3 -m sdd_gates tasks docs/planning/TASKS_{FEATURE}.md` (lê o DEFINE e, se existir, o DESIGN; com `--aprovado` depois da aprovação do plano) |
| `tasks … --executar` | Antes da 1ª task do Build, no Grande e no Complexo | O mesmo do `--aprovado` + DESIGN presente + roda a linha `**Build**` das Provas uma vez: vermelho antes de mudar = parar |

**Provas:** o guia [`PROVAS.md`](PROVAS.md), nesta skill, diz como escrever a prova de cada
critério (formato, tipo por critério, matriz de testes padrão, antipadrões). É lido pelo
`@sdd-po`, pelo `@sdd-define` (Médio) e pelo `@sdd-build`.

---

## Etapas e artefatos

| Etapa | Skill | Artefato |
|---|---|---|
| Define | `@sdd-define` | `docs/specs/DEFINE_{FEATURE}.md` + `.sdd/features/{FEATURE}/state.md`; gate `sdd_gates define` |
| Arquitetura | `@sdd-staff-engineer` | `docs/adr/ADR_{FEATURE}.md` (vinculante para Design e Build) |
| Planejamento | `@sdd-po` | `docs/planning/TASKS_{FEATURE}.md` (matriz de testes, gates, histórias + tasks, provas) + Jira, se houver `jira_key`; gate `sdd_gates tasks` |
| Design | `@sdd-design` | `docs/designs/DESIGN_{FEATURE}.md`; conferido pelo gate `sdd_gates tasks` |
| Build | `@sdd-build` | código + `.sdd/features/{FEATURE}/BUILD_REPORT.md` |
| Ship | `@sdd-ship` | `.sdd/archive/{FEATURE}/` + ticket fechado |

**Transversais:**
- `@sdd-doc` documenta o fim de cada etapa no Jira, se houver `jira_key` no state.
- `@sdd-iterate` cuida de mudança de requisito no meio do caminho.
- `@sdd-dev-workflow` cuida de branch, commit e PR.
- `@sdd-code-reviewer` faz a revisão antes do merge.

Cada skill de etapa define o próprio gate. O orquestrador não repete os gates: ele garante que a
etapa certa rode e que o fim de etapa aconteça.

### Fim de etapa

Toda etapa termina igual:

1. Gerar o artefato da etapa.
2. Atualizar `.sdd/features/{FEATURE}/state.md`: etapa, resultado do gate, aprovação.
3. Chamar `@sdd-doc` se houver `jira_key` (ele faz preview antes de escrever no Jira).
4. Propor o próximo passo. Numa parada humana (spec, plano), **esperar** o usuário.

O state é a fonte da verdade da feature: tamanho, `jira_key`, URL do Confluence, etapa atual,
caminho dos artefatos, aprovações e log do Jira. Nasce no Define (template
`sdd-define/STATE_TEMPLATE.md`) e vai para o archive no Ship.

---

## Retomar uma feature

Numa sessão nova, ou depois que o contexto foi resumido:

1. Releia esta skill e a skill da etapa atual. Um resumo guarda a tarefa, não as regras.
2. Leia o state e os artefatos da feature. Confira contra o git (branch, últimos commits):
   **a evidência vence a anotação**.
3. Proponha o próximo passo reconciliado **antes** de escrever código.

---

## Onde ficam os artefatos

Tudo fica no repo do projeto (o Git Folder do projeto), nunca no Git Folder das skills nem no
`sdd-gates`.

```
docs/                          # documentação da feature (revisada por humanos)
├── specs/      DEFINE_*.md
├── adr/        ADR_*.md
├── planning/   TASKS_*.md
└── designs/    DESIGN_*.md

.sdd/                          # estado e evidências do fluxo
├── features/
│   └── {FEATURE}/
│       ├── state.md           # ledger: tamanho, jira_key, etapas, aprovações, log Jira
│       └── BUILD_REPORT.md
└── archive/
    └── {FEATURE}/             # docs + state + SHIPPED_{DATA}.md depois do Ship
```

**Crie os arquivos só quando a etapa produzir conteúdo.** Nunca crie `DESIGN` ou `TASKS` vazios
de antemão: a ausência do arquivo é o estado certo de uma etapa pulada.

---

## Termos (PT-BR ↔ inglês)

| Aqui | Referência em inglês |
|---|---|
| Tamanho da feature | *auto-sizing* |
| Contrato de execução | *execution contract* |
| Critério de aceite | *acceptance criterion* |
| Raio de ação | *blast radius* |
| Gate | *gate* |
| Parada humana | *human checkpoint* |
| Área cinzenta | *gray area* |

---

> Tamanho da feature, contrato de execução, raio de ação e retomada foram adaptados do
> [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills) (Tech Leads Club,
> CC-BY-4.0) para o Genie Code e para dados no Databricks. Créditos em `THIRD_PARTY_NOTICES.md`.
