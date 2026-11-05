# DESIGN: {Nome da feature}

> {Uma frase: como a feature fica de pé no Databricks.}

<!-- O Design vem depois do plano aprovado (@sdd-po) e diz COMO cada task vira algo no workspace.
     Não muda o que o DEFINE pede nem as tasks aprovadas: se precisar, volta para lá. -->

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | {FEATURE_NAME} |
| **DEFINE** | `docs/specs/DEFINE_{FEATURE}.md` — v{versão aprovada} |
| **TASKS** | `docs/planning/TASKS_{FEATURE}.md` — v{versão aprovada} |
| **ADR** | {`docs/adr/ADR_{FEATURE}.md` \| não há} |
| **Data** | {AAAA-MM-DD} |

---

## Visão geral

<!-- O caminho do dado, da origem ao destino. Só o que esta feature cria ou toca. -->

```mermaid
flowchart LR
  A[{origem}] --> B[{componente}] --> C[{destino}]
```

## Abordagens

<!-- 2 ou 3 abordagens que entregam o MESMO escopo, a recomendada primeiro. Mostre ao usuário e
     confirme ANTES de detalhar os componentes; grave a confirmação com as palavras dele. -->

| ID | Abordagem | Prós | Contras |
|----|-----------|------|---------|
| A1 | {a recomendada} | {o que ganha} | {o que custa} |
| A2 | {outra abordagem real para o mesmo escopo} | {o que ganha} | {o que custa} |

**Recomendada**: {A1} — {o motivo, em uma linha}

**Confirmada**: {A1} — usuário: "{palavras do usuário}"

## Componentes

<!-- Um por linha: tabela, view, pipeline, job, recurso do bundle, módulo Python, notebook.
     Toda task do plano aparece em pelo menos um componente (o gate tasks confere).
     "Constrói com": a skill @databricks-* lida antes de decidir o componente. -->

| Componente | Tipo | Onde fica | Critérios | Tasks | Constrói com |
|------------|------|-----------|-----------|-------|--------------|
| {silver.pedidos} | {tabela streaming \| materialized view \| job \| recurso do bundle \| módulo} | {src/… \| resources/…} | {R1.1, R1.2} | {T1, T2} | {@databricks-pipelines} |

## Onde a regra roda

<!-- Toda regra que muda o que o consumidor vê (filtro, chave, desempate, cálculo, quarentena)
     roda numa função Python que o teste em memória alcança; o pipeline só liga as funções.
     Regra que só existe no SQL do pipeline ou no AUTO CDC tem prova de integração no target de
     desenvolvimento: diga isso aqui. Se a prova aprovada no plano é outra, o plano muda (versão
     nova e aprovação nova, @sdd-po). -->

| Critérios | Onde roda | Prova |
|-----------|-----------|-------|
| {R1.1, R1.2} | {`src/<pacote>/regras.py::<função>` \| SQL do pipeline \| AUTO CDC} | {unitário em memória \| integração no dev} |

## O que já existe e será reaproveitado

<!-- Resultado da varredura do repo: pipeline vizinho, utilitário, convenção de nomes, recurso do
     bundle, fixture de teste. Nada a reaproveitar: uma linha dizendo onde você procurou. -->

| O quê | Onde | Como entra nesta feature |
|-------|------|--------------------------|
| {pipeline, utilitário ou convenção} | {caminho} | {estende \| importa \| segue o mesmo padrão} |

## Decisões

<!-- Só as escolhas técnicas desta feature; arquitetura é do ADR, que não se reabre aqui.
     Escolha que muda o comportamento do dado é do usuário: volta para o DEFINE como pergunta.
     Base: a skill @databricks-* ou o arquivo do repo que sustenta a escolha, ou o ADR. -->

| ID | Decisão | Alternativa descartada | Por quê | Base |
|----|---------|------------------------|---------|------|
| D-1 | {o que foi escolhido} | {a outra opção real} | {o motivo, em uma linha} | {@databricks-* \| `caminho/arquivo` \| ADR} |

## Dados

<!-- Só o que o DEFINE não fixou: chave, modo de escrita (append, merge, AUTO CDC, overwrite),
     clustering ou partição, checkpoint.
     Agendamento: o recurso base do bundle nunca fixa `pause_status`. O `mode: development` só
     pausa o que não fixa; um `pause_status: UNPAUSED` no recurso vence o preset e deixa o job
     rodando no dev. O UNPAUSED vai só no target de produção. -->

| Tabela | Chave | Escrita | Observação |
|--------|-------|---------|------------|
| {catalogo.schema.tabela} | {coluna} | {append \| merge \| AUTO CDC \| overwrite} | {clustering, checkpoint…} |

## Riscos e pontos de atenção

<!-- O que você viu no repo e no workspace nas áreas que a feature toca: código frágil, dívida
     técnica, PII ou grant, varredura completa, small files, skew, evolução de schema, teste que
     falta. Cada um com a mitigação. Nada encontrado: escreva "Nenhum encontrado" e onde olhou. -->

| Ponto | Onde | Impacto | Mitigação |
|-------|------|---------|-----------|
| {o que pode dar errado} | {arquivo, tabela ou recurso} | {o que quebra ou piora} | {como o design ou uma task resolve} |

## Dado ruim e falhas

<!-- Cada cenário de dado ruim ou falha que a feature encontra: nulo, duplicado, atrasado, origem
     vazia ou indisponível, schema mudou. O tratamento sai do DEFINE (rubrica, quarentena,
     expectation); escolha que muda o comportamento do dado é do usuário, não daqui. -->

| Cenário | Tratamento | O que o consumidor vê |
|---------|------------|-----------------------|
| {registro com campo obrigatório nulo} | {expectation descarta e conta \| quarentena com motivo \| falha o update} | {o que aparece ou some na tabela} |

## Testes

{Onde os testes rodam (em memória, no compute, no target dev) e com que dados. A prova de cada
critério está na coluna Teste do plano.}

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | {AAAA-MM-DD} | Versão inicial |
