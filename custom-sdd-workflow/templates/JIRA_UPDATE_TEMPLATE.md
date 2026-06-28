# Template — Comentário de Fim de Fase no Jira

> Usado pelo `doc-agent` para montar o comentário postado no ticket Jira ao final de cada fase.
> Mantém o ticket contando a história do desenvolvimento em tempo real.
> O comentário é mostrado ao usuário (**preview**) antes de ser escrito via `jira_add_comment`.

---

## Estrutura do comentário

```
🟦 SDD · Fase {NOME_DA_FASE} concluída

{Resumo de 1–2 frases do que foi feito nesta fase.}

📄 Artefato: {caminho/no/repo/ARTEFATO_{FEATURE}.md}
📐 Origem: {URL da página Confluence | n/a}
✅ Gate: {resultado do gate — ex: "Clarity Score 13/15", "File Manifest completo", "lint + 8/8 testes ✅"}

🔜 Próxima fase: {nome da próxima fase + agente responsável}

— doc-agent · {YYYY-MM-DD HH:MM UTC}
```

---

## Variações por fase

| Fase | Resumo (exemplo) | Gate (exemplo) | Próxima fase |
|------|------------------|----------------|--------------|
| **Define** | Requisitos extraídos da SPEC e validados. | Clarity Score {X}/15 | ADR — `@custom-staff-engineer` |
| **ADR** | Decisões arquiteturais registradas e aprovadas. | {N} decisões / {M} domínios cobertos | Design — `@custom-sdd-workflow design` |
| **Design** | Arquitetura e File Manifest definidos a partir do ADR. | File Manifest completo ({N} arquivos) | Build — `@custom-sdd-workflow build` |
| **Build** | Código implementado e verificado. | lint ✅ · {X}/{Y} testes ✅ | Ship — `@custom-sdd-workflow ship` |
| **Ship** | Feature arquivada, lições capturadas, PR aberto. | Critérios de sucesso atendidos | — (Concluído) |
| **Iterate** | Mudança de escopo registrada na fase {fase}. | impacto cascata avaliado | (retoma a fase impactada) |

---

## Transição associada (por intenção, não por ID)

> O `doc-agent` chama `jira_get_transitions` e escolhe a transição cujo destino casa com a **intenção** abaixo.
> Nunca hardcodar IDs de transição — os nomes variam por projeto Jira.

| Fase concluída | Intenção da transição |
|----------------|------------------------|
| Define | To Do → **Em andamento** (In Progress) |
| ADR | mantém Em andamento |
| Design | mantém Em andamento |
| Build | Em andamento → **Em revisão** (In Review) |
| Ship | Em revisão → **Concluído** (Done) |
| Brainstorm / Iterate | nenhuma transição |

---

## Regras

- **Preview obrigatório:** mostrar o comentário renderizado ao usuário antes de escrever.
- **Sem `jira_key`:** não escrever no Jira — registrar como `pendente` no state e avisar.
- **Idempotência:** se o log do state já marca a fase como `postado`, não repetir o comentário.
- **Rastreabilidade:** sempre incluir o caminho do artefato e, quando houver, a URL do Confluence.
