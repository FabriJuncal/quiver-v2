#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(factory_root)"
AGENTS_FILE="$(codex_dir)/AGENTS.md"
SKILLS_DIR="$(agents_skills_dir)"
DRY_RUN=false

if [[ $# -eq 1 && "$1" == "--dry-run" ]]; then
  DRY_RUN=true
elif [[ $# -gt 0 ]]; then
  echo "Uso: $0 [--dry-run]"
  exit 2
fi

safe_dir "$(codex_dir)"
safe_dir "$HOME/.agents"
safe_dir "$SKILLS_DIR"
validate_managed_block "$AGENTS_FILE"

if [[ -f "$AGENTS_FILE" ]] && grep -Fxq '<!-- AI-SOFTWARE-FACTORY:START -->' "$AGENTS_FILE"; then
  if ! sed -n '/^<!-- AI-SOFTWARE-FACTORY:START -->$/,/^<!-- AI-SOFTWARE-FACTORY:END -->$/p' "$AGENTS_FILE" | grep -Fxq "\`$ROOT\`"; then
    echo "KEEP: bloque gestionado por otra copia de Factory."
  elif $DRY_RUN; then
    echo "Would remove managed block from: $AGENTS_FILE"
  else
    remove_managed_block "$AGENTS_FILE" | write_file "$AGENTS_FILE"
    echo "Bloque global removido."
  fi
fi

for skill in "$ROOT"/skills/core/*; do
  [[ -d "$skill" ]] || continue
  name="$(basename "$skill")"
  dest="$SKILLS_DIR/$name"
  if [[ -L "$dest" ]] && [[ "$(readlink "$dest")" == "$skill" ]]; then
    if $DRY_RUN; then
      echo "Would remove symlink: $dest"
    else
      rm "$dest"
      echo "Removida skill: $name"
    fi
  fi
done

echo
echo "La carpeta de AI Software Factory y tus proyectos NO fueron eliminados."
echo "Se conservan backups y perfiles asf-*.config.toml opcionales: pueden contener preferencias personales."
echo "Para dejar de usar esos perfiles, iniciá Codex sin --profile asf-...; revisalos antes de retirarlos manualmente."
