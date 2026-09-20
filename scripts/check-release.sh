#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/lib/common.sh"
ROOT="$(factory_root)"
[[ $# -eq 0 ]] || die 'Uso: check-release.sh (sin argumentos)'
for script in "$ROOT"/scripts/*.sh "$ROOT"/scripts/lib/*.sh "$ROOT/scripts/asf"; do
  bash -n "$script"
done
for candidate in python3.14 python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -I -B -c 'import tomllib' >/dev/null 2>&1; then
    exec "$candidate" -I -B "$SCRIPT_DIR/lib/check_release.py" "$ROOT"
  fi
done
die 'Validación de release requiere Python >= 3.11; instalalo y repetí check-release.sh.'
