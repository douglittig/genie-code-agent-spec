# TASKS: {Nome da feature}

> {Uma frase: o que o plano entrega e em quantas fatias.}

<!-- Preencha tudo; o gate `python3 -m sdd_gates tasks` avisa sobre qualquer {placeholder} que sobrar.
     O gate lê também o DEFINE da feature: todo critério de aceite dele precisa de uma task. -->

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

## Histórias

<!-- Uma história é uma fatia vertical: entrega algo que quem usa o dado consegue ver sozinha.
     "Só a camada bronze" não é fatia. Pontos em Fibonacci (1, 2, 3, 5, 8, 13), calibrados pelo
     estimation-guide.md; acima de 13, quebre a história.

     Task: um passo atômico, um commit, um resultado que dá para conferir. IDs T1, T2… em ordem
     no plano todo. Critérios: os R<n>.<m> do DEFINE que a task prova ("—" em task de
     infraestrutura). Depende de: só tasks que vêm antes. Teste: o teste que prova os critérios,
     nascido do critério (arquivo e o que confere). Gate: o comando que fecha a task. -->

### H1: {título da fatia} — {pontos} pontos

**Como** {quem usa o dado}, **quero** {o que a fatia entrega}, **para** {o valor}.

**Jira:** {PROJ-124 \| pendente}

| Task | O que faz | Critérios | Depende de | Teste | Gate |
|------|-----------|-----------|------------|-------|------|
| T1 | {passo atômico} | {R1.1, R1.2 \| —} | {— \| T?} | {`tests/test_x.py`: o que confere} | {`pytest tests/test_x.py` \| `databricks bundle validate`} |

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
