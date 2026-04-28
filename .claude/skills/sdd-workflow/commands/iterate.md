---
name: iterate
description: Atualize qualquer documento de fase quando requisitos ou design mudarem (Cross-Phase)
---

# Iterate

> Atualização de documentos de fase quando requisitos ou design mudam (Cross-Phase)

## Uso

```
iterate <arquivo> "<descrição-da-mudança>"
```

## Exemplos

```
iterate BRAINSTORM_API_BUSCA.md "Considerar ElasticSearch ao invés de PostgreSQL full-text search"
iterate DEFINE_API_BUSCA.md "Adicionar suporte a busca fuzzy, não apenas busca exata"
iterate DESIGN_API_BUSCA.md "Serviços precisam ser autocontidos, sem common/ compartilhado"
iterate .claude/sdd/features/DEFINE_AUTH.md "Mudar de JWT para autenticação baseada em sessão"
```

---

## Visão Geral

O iterate funciona com as **fases de documento** do workflow SDD:

```text
Fase 0: brainstorm → BRAINSTORM_{FEATURE}.md ← iterate pode atualizar
Fase 1: define     → DEFINE_{FEATURE}.md     ← iterate pode atualizar
Fase 2: design     → DESIGN_{FEATURE}.md     ← iterate pode atualizar
Fase 3: build      → (código)                ← Atualize DESIGN, depois build
Fase 4: ship       → (archive)               ← N/A
```

Use iterate quando você descobrir algo que precisa mudar no meio do processo.

**Importante:** Para mudar código durante a Fase 3, atualize o documento DESIGN primeiro. A cascata para o código dispara um rebuild via build. Isso garante rastreabilidade.

---

## O que Esta Fase Faz

1. **Detectar Fase** — Identificar qual documento de fase está sendo atualizado
2. **Analisar Impacto** — Determinar efeitos downstream
3. **Atualizar Documento** — Aplicar mudanças com controle de versão
4. **Cascata** — Propagar mudanças para documentos downstream se necessário

---

## Processo

### Passo 1: Carregar Documento Alvo

```markdown
Ler <arquivo-alvo>

# Identificar tipo de documento:
# - BRAINSTORM_*.md → Fase 0
# - DEFINE_*.md → Fase 1
# - DESIGN_*.md → Fase 2
```

### Passo 2: Analisar a Mudança

Determine o tipo de mudança:

| Tipo de Mudança | Exemplo | Impacto |
|-----------------|---------|---------|
| **Aditiva** | "Também suportar PDF" | Baixo — adiciona ao existente |
| **Modificadora** | "Mudar de X para Y" | Médio — atualiza o existente |
| **Removendo** | "Remover feature Z" | Médio — simplifica |
| **Arquitetural** | "Usar padrão diferente" | Alto — pode exigir redesign |

### Passo 3: Aplicar Mudanças

Atualize o documento com:

1. **Mudança Aplicada** — A modificação real
2. **Bump de Versão** — Incrementar versão no histórico de revisões
3. **Nota de Mudança** — O que mudou e por quê

### Passo 4: Avaliar Necessidade de Cascata

| Origem | Cascata Para |
|--------|--------------|
| Mudança no DEFINE | Pode precisar de atualização no DESIGN |
| Mudança no DESIGN | Pode precisar de atualização no código |

Determine se documentos downstream precisam de atualização com base nas regras de cascata.

### Passo 5: Executar Cascata (se necessário)

Se cascata for necessária, pergunte ao usuário:

```markdown
"Esta mudança no {DOCUMENTO} afeta o {DOWNSTREAM}. Opções:
(a) Atualizar {DOWNSTREAM} automaticamente
(b) Apenas atualizar {DOCUMENTO}, cuido do {DOWNSTREAM} manualmente
(c) Me mostre o que mudaria primeiro"
```

### Passo 6: Salvar Atualizações

```markdown
Salvar <arquivo-alvo>
# Se cascata:
Salvar <documento-downstream>
```

---

## Output

| Artefato | Localização |
|----------|-------------|
| **Documento Atualizado** | Mesmo local do input |
| **Atualizações de Cascata** | Documentos downstream (se aplicável) |

---

## Regras de Cascata

### Mudanças no DEFINE → Impacto no DESIGN

| Mudança no DEFINE | Impacto no DESIGN |
|-------------------|-------------------|
| Novo requisito | Pode precisar de novo componente |
| Critério de sucesso alterado | Pode precisar de abordagem diferente |
| Expansão de escopo | Precisa de novas seções |
| Redução de escopo | Pode simplificar |
| Nova restrição | Deve ser acomodada |

### Mudanças no DESIGN → Impacto no Código

| Mudança no DESIGN | Impacto no Código |
|-------------------|-------------------|
| Novo arquivo no manifest | Criar arquivo |
| Arquivo removido | Deletar arquivo |
| Padrão alterado | Atualizar arquivos afetados |
| Nova decisão | Pode precisar de refactor |
| Mudança arquitetural | Atualizações significativas necessárias |

---

## Controle de Versão

Cada documento mantém um histórico de revisões:

```markdown
## Histórico de Revisões

| Versão | Data | Autor | Mudanças |
|--------|------|-------|---------|
| 1.0 | 2026-01-25 | define-agent | Versão inicial |
| 1.1 | 2026-01-25 | iterate-agent | Adicionado suporte a PDF conforme pedido |
```

---

## Dicas

1. **Itere Cedo** — Capture mudanças antes de começar a codificar
2. **Seja Específico** — "Adicionar X" é melhor que "melhorar isso"
3. **Verifique a Cascata** — Mudanças reverberam downstream
4. **Mantenha o Histórico** — O controle de versão mostra a evolução
5. **Não Resista** — Requisitos mudam, isso é normal

---

## Quando Usar Iterate vs Começar Novamente

| Situação | Ação |
|----------|------|
| < 30% de mudança | `iterate` |
| Adicionar/modificar features | `iterate` |
| Mudar restrições | `iterate` |
| > 50% diferente | Novo `define` |
| Problema completamente diferente | Novo `define` |
| Usuários-alvo diferentes | Novo `define` |

---

## Referências

- Agente: `agents/iterate-agent.md`
- Contratos: `architecture/WORKFLOW_CONTRACTS.yaml`
