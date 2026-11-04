# TASKS: {Nome da feature}

> {Uma frase: o que o plano entrega e em quantas fatias.}

<!-- Preencha tudo; o gate `python3 -m sdd_gates tasks` avisa sobre qualquer {placeholder} que sobrar.
     O gate lê também o DEFINE da feature: todo critério de aceite dele precisa de uma task e de
     uma prova. Guia das provas: sdd-workflow/PROVAS.md. -->

## Identificação

| Campo | Valor |
|-------|-------|
| **Feature** | {FEATURE_NAME} |
| **DEFINE** | `docs/specs/DEFINE_{FEATURE}.md` — v{versão aprovada} |
| **ADR** | {`docs/adr/ADR_{FEATURE}.md` \| não há} |
| **Épico (Jira)** | {PROJ-123 \| pendente} |
| **Data** | {AAAA-MM-DD} |
| **Status** | {Rascunho \| Aguardando aprovação \| Aprovado \| Em revisão} |

---

## Matriz de testes

<!-- Uma linha por camada que a feature toca. Antes de preencher, leia as regras de teste do repo
     (AGENTS.md, pyproject.toml/pytest.ini, CI) e 5 a 10 testes que já existem: eles são o piso,
     não o teto. Repo sem testes: pergunte ao usuário, com a matriz padrão do PROVAS.md como
     recomendação. Nível: rápido, completo ou build (seção Gates). -->

| Camada | Teste | Profundidade | Onde | Nível |
|--------|-------|--------------|------|-------|
| {Transformação: função PySpark com a regra} | {Unitário em memória, `assertDataFrameEqual`} | {Cada critério de regra, 1:1, e os casos de borda da rubrica} | {`tests/unit/`} | {rápido} |

## Gates

<!-- Os três níveis, com o comando de cada um entre crases. A coluna Gate de cada task cita o
     nível, não o comando. A última task de cada história roda o build. Sem integração no repo:
     "nenhum — motivo" no nível completo. Comando com | não cabe na tabela: use um script. -->

| Nível | Quando usar | Comando |
|-------|-------------|---------|
| rápido | Task com teste unitário | {`python3 -m pytest tests/unit -q -p no:cacheprovider`} |
| completo | Task com integração no target de desenvolvimento | {`python3 -m pytest tests/unit tests/integracao -q -p no:cacheprovider` \| nenhum — motivo} |
| build | Última task de cada história; task só de configuração | {`databricks bundle validate -t dev`; `python3 -m pytest tests -q -p no:cacheprovider`} |

---

## Histórias

<!-- Uma história é uma fatia vertical: entrega algo que quem usa o dado consegue ver sozinha.
     "Só a camada bronze" não é fatia. Pontos em Fibonacci (1, 2, 3, 5, 8, 13), calibrados pelo
     estimation-guide.md; acima de 13, quebre a história.

     Task: um passo atômico, um commit, um resultado que dá para conferir. IDs T1, T2… em ordem
     no plano todo. Critérios: os R<n>.<m> do DEFINE que a task prova ("—" em task de
     infraestrutura). Depende de: só tasks que vêm antes. Teste: o teste que prova os critérios,
     nascido do critério (arquivo e o que confere), na mesma task que cria a camada ("testado em
     outra task" não vale). Gate: o nível da seção Gates (rápido, completo, build); a última task
     da história é build. -->

### H1: {título da fatia} — {pontos} pontos

**Como** {quem usa o dado}, **quero** {o que a fatia entrega}, **para** {o valor}.

**Jira:** {PROJ-124 \| pendente}

| Task | O que faz | Critérios | Depende de | Teste | Gate |
|------|-----------|-----------|------------|-------|------|
| T1 | {passo atômico} | {R1.1, R1.2 \| —} | {— \| T?} | {`tests/unit/test_x.py`: o que confere} | {rápido \| completo \| build} |

---

## Provas

<!-- Uma prova por critério do DEFINE: uma afirmação observável, com o valor, citando o critério,
     e na linha de baixo o que a decide. Três formas:
       Prova: run <nome> | <a linha que o teste imprime ao passar, com PASSED>
       Prova: `<comando sozinho>`        (prova solta: o código de saída decide)
       Prova: passeio — <o que a consulta no dev mostra>
     **Build**: os comandos de build, lint e validação do repo, entre crases, que rodam uma vez
     antes da 1ª task (gate tasks --executar) e no fim. Repo novo, sem build: "nenhum — motivo".
     **Run <nome>**: um grupo de testes rodado uma vez; ponha o -v para cada teste imprimir a linha.
     Guia de cada tipo de prova: sdd-workflow/PROVAS.md. -->

**Build**: {`databricks bundle validate -t dev` | nenhum — repo novo, sem bundle nem testes}
**Run unit**: {`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/unit -v -p no:cacheprovider`}

**P1** — {afirmação observável, com o valor} ({R1.1})
Prova: {run unit | tests/unit/test_x.py::test_r1_1_o_que_confere PASSED}

---

## Aprovação

<!-- Preenchido só quando o usuário aprovar o plano, com as palavras dele e a versão aprovada:
     **Aprovado**: AAAA-MM-DD — v1.0 — usuário: "palavras do usuário"
     Aprovar não cria versão. Gravar as chaves do Jira depois também não. -->

## Histórico de revisões

<!-- Mudou uma task, uma dependência ou uma história depois de aprovado: versão nova, Status
     "Em revisão" e aprovação nova. -->

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | {AAAA-MM-DD} | Versão inicial |
