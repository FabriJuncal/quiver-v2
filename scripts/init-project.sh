#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(factory_root)"
PROJECT="$(pwd -P)"
GIT_INIT=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --git-init) GIT_INIT=true ;;
    --dry-run) DRY_RUN=true ;;
    *) echo "Uso: $0 [--git-init] [--dry-run]"; exit 2 ;;
  esac
done

project_preflight
project_directories

copy_if_missing "$ROOT/templates/AGENTS.md" "$PROJECT/AGENTS.md"
copy_if_missing "$ROOT/templates/PROJECT_PROFILE.md" "$PROJECT/PROJECT_PROFILE.md"
copy_if_missing "$ROOT/templates/PROJECT_STATE.md" "$PROJECT/PROJECT_STATE.md"
copy_if_missing "$ROOT/templates/CAPABILITY_MAP.md" "$PROJECT/CAPABILITY_MAP.md"

if $GIT_INIT && ! $DRY_RUN && ! git rev-parse --git-dir >/dev/null 2>&1; then
  if git init -b main >/dev/null 2>&1; then
    echo "Git inicializado en branch main."
  else
    git init >/dev/null
    git branch -m main >/dev/null 2>&1 || true
    echo "Git inicializado; branch principal ajustada a main cuando fue posible."
  fi
fi

if $DRY_RUN; then
  echo "Dry run: no se crearon archivos, directorios ni repositorio Git."
  exit 0
fi

echo
echo "Proyecto nuevo preparado para AI Software Factory."
echo
echo "Siguiente mensaje sugerido para Codex:"
echo 'Abrí: codex. Después pegá:'
cat <<'EOF'
Quiero crear un proyecto nuevo usando AI Software Factory.

Comenzá por Project Discovery.
No implementes todavía.
Guiame hasta el próximo Decision Boundary.
EOF
