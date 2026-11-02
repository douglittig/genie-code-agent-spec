---
name: sdd-define
description: |
  Etapa Define do SDD (@sdd-workflow): transforma um pedido, uma página do Confluence ou notas de
  reunião numa spec de dados testável, DEFINE_<FEATURE>.md, com critérios de aceite em EARS
  (QUANDO/SE…ENTÃO o pipeline DEVE…), rubrica de requisitos implícitos de dados (idempotência,
  atraso, duplicidade, schema, backfill, qualidade, PII, SLA, custo) e rastreabilidade de cada
  critério até a fonte. Use quando o usuário pedir para especificar, definir ou levantar requisitos
  de um pipeline, tabela, job ou métrica; quando trouxer um link do Confluence; ou quando a ideia
  ainda for vaga e precisar de exploração (áreas cinzentas). Pergunta toda decisão do usuário antes
  de apresentar a spec e só segue com a aprovação gravada nas palavras dele.
---

# Define — a spec de dados

Resultado: `docs/specs/DEFINE_{FEATURE}.md` aprovado pelo usuário, e o state da feature criado.
Template: [`DEFINE_TEMPLATE.md`](DEFINE_TEMPLATE.md). Gate: `scripts/validate_define.py`.

Antes de começar, o tamanho da feature já foi decidido no `@sdd-workflow`. Ele define o quanto
preencher:

| Tamanho | O que entra no DEFINE |
|---|---|
| Pequeno | Não há DEFINE: um critério e o teste dele, no chat |
| Médio | Requisitos, critérios, rubrica (pode ter várias linhas "não se aplica: motivo"), escopo e rastreabilidade |
| Grande | Tudo, incluindo contrato de dados e contexto técnico |
| Complexo | Tudo + **áreas cinzentas** (passo 4) |

---

## Passo 1 — Juntar as fontes

- **Confluence:** use **só** `confluence_get_page` na URL que o usuário deu, e nas subpáginas
  diretas dela. **Nunca** `confluence_search`: busca em toda a empresa traz página errada.
  Registre cada página lida na seção Fontes.
- **Pedido no chat, notas, e-mail:** copie as frases do usuário que viram requisito. Elas são a
  origem na rastreabilidade.
- **Varredura leve do projeto:** antes de perguntar, olhe o que já existe — o pipeline vizinho,
  as tabelas de origem, as convenções do repo (`@databricks-data-discovery` ajuda a achar
  tabelas). Serve para perguntar com base no real, não para limitar a spec ao que já existe.

Onde cada seção do Confluence costuma cair:

| Seção no Confluence | Vai para |
|---|---|
| Visão geral, objetivo | Problema, Quem usa o dado |
| Fontes de dados, colunas, PII | Contrato de dados; rubrica (PII) |
| Arquitetura bronze/silver/gold | Requisitos e Escopo |
| Qualidade de dados | Critérios (SE … ENTÃO …) e rubrica (Qualidade) |
| Configuração de execução (trigger, compute) | Contexto técnico; rubrica (SLA, custo) |
| Critérios de aceite | Requisitos, reescritos em EARS, com a seção como origem |
| Fora do escopo, restrições | Fora do escopo; Suposições |

Se a spec precisar fazer diferente do que o Confluence diz, isso é **decisão do usuário**:
pergunte e registre em "Diferenças em relação à fonte", com quem aprovou.

## Passo 2 — Conversar

Você é parceiro de raciocínio, não um formulário. Comece aberto e deixe o usuário despejar o
modelo mental dele; aprofunde no que ele enfatizar. As três perguntas que sempre precisam de
resposta: **qual problema**, **quem usa o dado e para quê**, **como saberemos que deu certo**.

## Passo 3 — Escrever os requisitos e os critérios

Cada requisito é uma história de uso com prioridade (P1 = sem isso não entrega; P2 = importante;
P3 = se der tempo) e critérios com ID `R<n>.<m>`. Todo critério segue um padrão **EARS** e tem um
único jeito de ler, com resultado verificável:

| Padrão | Forma | Referência em inglês | Use para |
|---|---|---|---|
| Sempre | O pipeline DEVE … | *Ubiquitous* | Regra que vale o tempo todo (unicidade, formato) |
| Evento | QUANDO … ENTÃO o pipeline DEVE … | *Event-driven* (WHEN) | Reação a um gatilho (chegada de arquivo, horário) |
| Estado | ENQUANTO … o pipeline DEVE … | *State-driven* (WHILE) | Comportamento durante um estado (backfill, manutenção) |
| Opcional | ONDE … o pipeline DEVE … | *Optional feature* (WHERE) | Comportamento atrás de flag ou configuração |
| Indesejado | SE … ENTÃO o pipeline DEVE … | *Unwanted behavior* (IF/THEN) | Erro, nulo, duplicado, falha de origem |

Troque "o pipeline" pelo sujeito certo (o job, a tabela, o dashboard). Nada de termo vago sem
número: "rápido" vira "até 06h30"; "sem duplicados" vira "no máximo uma linha por `pedido_id`".

## Passo 4 — Áreas cinzentas (tamanho Complexo, ou ideia vaga)

Área cinzenta é um ponto com mais de um caminho válido que muda o resultado para quem usa o dado:
granularidade, chave de deduplicação, janela de atraso, histórico, o que fazer com o registro
inválido.

1. Liste as áreas cinzentas que você encontrou.
2. Para cada uma, apresente 2 ou 3 opções com a sua recomendação e o porquê.
3. Corte o que não é necessário agora (o que não muda a primeira entrega vai para Fora do escopo).
4. Grave a decisão na tabela "Áreas cinzentas", com quem decidiu. Área que o usuário não quis
   discutir vira suposição com origem "usuário não quis discutir".

## Passo 5 — Rubrica de requisitos implícitos de dados

Os requisitos que ninguém pede e todo pipeline precisa. **Cada dimensão termina num lugar:** um
critério, "fora do escopo", uma suposição (`S-n`) ou "não se aplica: motivo".

| Dimensão | Pergunta |
|---|---|
| Idempotência e reprocessamento | Rodar duas vezes a mesma partição dá o mesmo resultado? |
| Dado atrasado ou fora de ordem | Até quando um evento atrasado entra? E depois? |
| Duplicidade | Qual é a chave? Qual registro vence? |
| Evolução de schema | Coluna nova na origem quebra, entra ou é ignorada? |
| Backfill e carga histórica | Desde quando? Como roda a carga inicial? |
| Qualidade | Nulos, chaves, faixas de valor: descarta, isola ou falha? |
| Falha parcial e retomada | O que acontece se cair no meio? Retoma de onde? |
| PII, grants e Unity Catalog | Tem dado pessoal? Quem pode ler? Máscara ou tag? |
| Freshness e SLA | Até que horas o dado precisa estar pronto? |
| Volume, custo e compute | Quanto dado por dia? Serverless ou cluster? |
| Observabilidade e alerta | Que métrica mostra que deu errado? Quem é avisado? |

## Passo 6 — Gate de fechamento

Antes de apresentar, confira os quatro pontos e corrija no próprio arquivo:

1. **Sem ambiguidade:** todo critério tem uma única leitura e um resultado definido pela spec.
   Se não tem, pergunte, divida ou vire suposição explícita.
2. **Decisão do usuário é pergunta:** escopo, comportamento do dado e desvio da fonte são
   perguntados, com a sua recomendação. Só vira suposição o que o código resolve ou o que o
   usuário delegou ("você decide").
3. **Área cinzenta recusada vira suposição**, com origem "usuário não quis discutir". Nunca some.
4. **O pedido, frase a frase:** releia o pedido e a página do Confluence, uma frase por vez.
   Cada frase cai num critério, num item de Fora do escopo ou numa pergunta. Frase que não cai em
   lugar nenhum é o requisito que vai sumir, porque ninguém relê o pedido depois.

O gate esclarece o que foi pedido. Ele não inventa requisito novo.

## Passo 7 — Validar, apresentar e parar

```bash
python3 <pasta-da-skill>/scripts/validate_define.py docs/specs/DEFINE_{FEATURE}.md
```

A pasta da skill é a deste `SKILL.md`: `/Workspace/.assistant/skills/sdd-define` no Genie Code
(ou `/Workspace/Users/<você>/.assistant/skills/sdd-define`, se instalada só para você). Rode o
script em vez de lê-lo: as mensagens dizem o que mudar. Exit diferente de 0 → corrija e rode de
novo. Sem como executar código, faça as mesmas checagens lendo o arquivo e diga isso ao usuário.

Com o validador verde, apresente o DEFINE com as perguntas em aberto e a sua recomendação para
cada uma, e **pare**. É a primeira parada humana do contrato de execução.

## Passo 8 — Gravar a aprovação

Quando o usuário aprovar, grave na seção Aprovação, com as palavras dele:

```markdown
**Aprovado**: 2026-11-02 — usuário: "pode seguir com essa spec"
```

Nunca grave uma aprovação que ele não deu. Depois rode o gate do Build:

```bash
python3 <pasta-da-skill>/scripts/validate_define.py docs/specs/DEFINE_{FEATURE}.md --aprovado
```

## Passo 9 — State, Jira e fim de etapa

1. Pergunte a chave do Jira (ex.: `PROJ-123`); sem chave, registre `pendente`.
2. Crie `.sdd/features/{FEATURE}/state.md` a partir de [`STATE_TEMPLATE.md`](STATE_TEMPLATE.md):
   tamanho, `jira_key`, URL do Confluence, etapa Define concluída, aprovação.
3. Chame `@sdd-doc` (comentário no Jira + transição para Em andamento; ele faz preview antes).
4. Proponha o próximo passo, conforme o tamanho: `@sdd-staff-engineer` (Complexo, ou decisão de
   arquitetura), `@sdd-design` (Grande) ou `@sdd-build` (Médio).

Se a spec mudar depois de aprovada, use `@sdd-iterate`: mudança de spec pede aprovação nova.

---

## Termos (PT-BR ↔ inglês)

| Aqui | Referência em inglês |
|---|---|
| Critério de aceite | *acceptance criterion* |
| EARS | *Easy Approach to Requirements Syntax* |
| Área cinzenta | *gray area* |
| Requisitos implícitos | *implicit requirements* |
| Rastreabilidade | *traceability* |
| Suposição | *assumption* |

---

> Critérios EARS, rubrica de requisitos implícitos, gate de fechamento, áreas cinzentas e gate por
> script foram adaptados do [TLC Spec-Driven](https://github.com/tech-leads-club/agent-skills)
> (Tech Leads Club, CC-BY-4.0); a rubrica foi reescrita para engenharia de dados no Databricks.
> Créditos em `THIRD_PARTY_NOTICES.md`.
