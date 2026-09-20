#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(factory_root)"
CODEX_DIR="$(codex_dir)"
SOURCE="$ROOT/config/codex-profiles"
FORCE=false
DRY_RUN=false

for arg in "$@"; do
  case "$arg" in
    --force) FORCE=true ;;
    --dry-run) DRY_RUN=true ;;
    *)
      echo "Uso: $0 [--dry-run] [--force]"
      exit 2
      ;;
  esac
done

safe_dir "$CODEX_DIR"
# Validate every destination before the first write (including --force).
for src in "$SOURCE"/*.config.toml; do
  safe_file "$CODEX_DIR/$(basename "$src")"
done
$DRY_RUN || mkdir -p "$CODEX_DIR"

echo "AI Software Factory — Codex model profiles"
echo
echo "Destino: $CODEX_DIR"
echo

for src in "$SOURCE"/*.config.toml; do
  [[ -f "$src" ]] || continue
  name="$(basename "$src")"
  dest="$CODEX_DIR/$name"

  if [[ -e "$dest" && "$FORCE" != true ]]; then
    echo "KEEP: $dest"
    echo "      Ya existe. Usá --force para reemplazar con backup."
    continue
  fi

  if $DRY_RUN; then
    echo "WOULD INSTALL: $name"
    continue
  fi

  write_file "$dest" < "$src"
  echo "INSTALLED: $dest"
done

echo
echo "Uso recomendado:"
echo "  asf balanced (agregá la carpeta scripts de Factory a PATH)"
echo "Alternativa con perfiles: codex --profile asf-balanced"
echo
echo "Perfiles:"
echo "  asf-economical  → GPT-5.6 Luna (gpt-5.6-luna) / Low"
echo "  asf-balanced    → GPT-5.6 Terra (gpt-5.6-terra) / Medium"
echo "  asf-advanced    → GPT-5.6 Sol (gpt-5.6-sol) / High"
echo "  asf-exceptional → GPT-6 Astra (gpt-6-astra) / High"
echo
echo "La disponibilidad real depende de tu cuenta. /model es la fuente final."
echo "Requiere Codex >= 0.134.0. Configuración del proyecto y flags pueden prevalecer sobre --profile."
echo "Si la tarea depende materialmente de esa selección: /status; si coincide, continuar; si difiere, pegá el resultado."
