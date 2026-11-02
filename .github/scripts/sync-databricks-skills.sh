#!/usr/bin/env bash
# Copia as skills oficiais da Databricks (databricks/databricks-agent-skills)
# de um checkout do upstream para a raiz deste repo.
#
# Uso:  sync-databricks-skills.sh <checkout-do-upstream> <raiz-deste-repo>
#
# Variáveis de ambiente (o workflow define todas):
#   UPSTREAM       owner/repo do upstream (vai para o lock)
#   UPSTREAM_PATH  pasta das skills no upstream (ex.: skills)
#   UPSTREAM_REF   tag sincronizada (vai para o lock)
#   EXTRA_SKILLS   "<path no upstream>:<pasta na raiz>" separados por espaço
#   OWN_SKILLS     skills nossas: nunca sobrescritas nem apagadas
#   FROZEN_SKILLS  skills upstream que não existem mais lá e mantemos congeladas
#
# Roda igual no GitHub Actions e na máquina local, para testar antes do PR.
set -euo pipefail

UP="${1:?informe o checkout do upstream}"
ROOT="${2:?informe a raiz do repo}"
SRC="$UP/$UPSTREAM_PATH"
LOCK="$ROOT/databricks-skills.lock"

protected() { # skill nossa ou congelada → não mexe
  case " $OWN_SKILLS $FROZEN_SKILLS " in *" $1 "*) return 0 ;; esac
  return 1
}

# 1. Descobrir as skills do upstream: só pastas com SKILL.md.
#    Falhar com mensagem clara se não achar nenhuma (layout do upstream mudou).
found=()
if [ -d "$SRC" ]; then
  for dir in "$SRC"/*/; do
    [ -f "$dir/SKILL.md" ] && found+=("$(basename "$dir")")
  done
fi
if [ "${#found[@]}" -eq 0 ]; then
  echo "ERRO: nenhuma skill (pasta com SKILL.md) em $UPSTREAM_PATH/ do upstream." >&2
  echo "O layout do $UPSTREAM mudou — revise UPSTREAM_PATH no workflow." >&2
  exit 1
fi

# 2. Copiar cada skill. --delete poda arquivos removidos no upstream,
#    só dentro da pasta da skill.
synced=()
for name in "${found[@]}"; do
  if protected "$name"; then echo "skip (protegida): $name"; continue; fi
  echo "sync: $name"
  rsync -a --delete "$SRC/$name/" "$ROOT/$name/"
  synced+=("$name")
done

# 3. Skills que vivem fora de UPSTREAM_PATH.
for map in $EXTRA_SKILLS; do
  src="$UP/${map%%:*}"; dest="${map##*:}"
  if [ ! -f "$src/SKILL.md" ]; then
    echo "ERRO: skill extra não encontrada no upstream: ${map%%:*}" >&2; exit 1
  fi
  echo "sync (extra): ${map%%:*} -> $dest"
  rsync -a --delete "$src/" "$ROOT/$dest/"
  synced+=("$dest")
done

# 4. Podar skills que o sync anterior trouxe e o upstream removeu/renomeou.
#    A lista anterior vem do próprio lock; skills nossas e congeladas ficam.
if [ -f "$LOCK" ]; then
  while read -r old; do
    [ -z "$old" ] && continue
    case " ${synced[*]} " in *" $old "*) continue ;; esac
    if protected "$old"; then continue; fi
    if [ -d "$ROOT/$old" ]; then echo "prune (saiu do upstream): $old"; rm -rf "${ROOT:?}/$old"; fi
  done < <(sed -n 's/^  - //p' "$LOCK")
fi

# 5. A licença da Databricks exige repassar uma cópia a quem recebe as skills.
cp "$UP/LICENSE" "$ROOT/LICENSE-databricks-agent-skills"
cp "$UP/NOTICE" "$ROOT/NOTICE-databricks-agent-skills"

# 6. Lock: versão + lista exata do que veio do upstream (base da poda no próximo sync).
{
  echo "# Gerado automaticamente por .github/scripts/sync-databricks-skills.sh"
  echo "# Não editar à mão."
  echo "upstream_repo: $UPSTREAM"
  echo "upstream_path: $UPSTREAM_PATH"
  echo "version: $UPSTREAM_REF"
  echo "commit: $(git -C "$UP" rev-parse HEAD)"
  echo "synced_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "skills:"
  printf '  - %s\n' "${synced[@]}" | sort
} > "$LOCK"
cat "$LOCK"
