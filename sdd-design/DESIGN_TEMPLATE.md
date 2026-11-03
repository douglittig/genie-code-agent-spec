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

## Componentes

<!-- Um por linha: tabela, view, pipeline, job, recurso do bundle, módulo Python, notebook.
     Toda task do plano aparece em pelo menos um componente (o gate tasks confere).
     "Constrói com": a skill @databricks-* lida antes de decidir o componente. -->

| Componente | Tipo | Onde fica | Critérios | Tasks | Constrói com |
|------------|------|-----------|-----------|-------|--------------|
| {silver.pedidos} | {tabela streaming \| materialized view \| job \| recurso do bundle \| módulo} | {src/… \| resources/…} | {R1.1, R1.2} | {T1, T2} | {@databricks-pipelines} |

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
     clustering ou partição, checkpoint. -->

| Tabela | Chave | Escrita | Observação |
|--------|-------|---------|------------|
| {catalogo.schema.tabela} | {coluna} | {append \| merge \| AUTO CDC \| overwrite} | {clustering, checkpoint…} |

## Testes

{Onde os testes rodam (em memória, no compute, no target dev) e com que dados. A prova de cada
critério está na coluna Teste do plano.}

## Histórico de revisões

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | {AAAA-MM-DD} | Versão inicial |
