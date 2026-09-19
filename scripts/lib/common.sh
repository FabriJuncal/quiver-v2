#!/usr/bin/env bash

set -euo pipefail

factory_root() {
  cd "$(dirname "${BASH_SOURCE[0]}")/../.." >/dev/null 2>&1
  pwd -P
}

codex_dir() {
  if [[ -n "${CODEX_HOME:-}" ]]; then
    printf '%s\n' "$CODEX_HOME"
  else
    printf '%s\n' "$HOME/.codex"
  fi
}

agents_skills_dir() {
  printf '%s\n' "$HOME/.agents/skills"
}

factory_version() {
  local root
  root="$(factory_root)"
  sed -n 's/^- \*\*Version:\*\* //p' "$root/FACTORY_VERSION.md" 2>/dev/null | head -n 1
}

remove_managed_block() {
  local input="$1"
  validate_managed_block "$input" || return 1
  awk '
    $0 == "<!-- AI-SOFTWARE-FACTORY:START -->" {skip=1; next}
    $0 == "<!-- AI-SOFTWARE-FACTORY:END -->"   {skip=0; next}
    !skip {print}
  ' "$input"
}

die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# Managed entries must be ordinary files/directories, including when dangling.
safe_file() {
  [[ ! -L "$1" ]] && { [[ ! -e "$1" ]] || [[ -f "$1" ]]; } || {
    printf 'ERROR: destino no regular o symlink: %s. Revisalo manualmente; no se modifica.\n' "$1" >&2
    return 1
  }
}

safe_dir() {
  [[ ! -L "$1" ]] && { [[ ! -e "$1" ]] || [[ -d "$1" ]]; } || {
    printf 'ERROR: directorio inválido o symlink: %s. Revisalo manualmente; no se modifica.\n' "$1" >&2
    return 1
  }
}

validate_managed_block() {
  safe_file "$1" || return 1
  [[ -f "$1" ]] || return 0
  # Refuse to normalize a user's final line while editing a line-based block.
  if [[ -s "$1" ]] && [[ "$(tail -c 1 "$1" | wc -l | tr -d ' ')" != 1 ]]; then
    printf 'ERROR: %s no termina en newline. Agregá el salto de línea en tu editor y repetí el comando.\n' "$1" >&2
    return 1
  fi
  awk '
    /AI-SOFTWARE-FACTORY:(START|END)/ {
      if ($0 == "<!-- AI-SOFTWARE-FACTORY:START -->" && !opened && !seen) {opened=1; seen=1}
      else if ($0 == "<!-- AI-SOFTWARE-FACTORY:END -->" && opened) {opened=0}
      else {bad=1}
    }
    END {exit (bad || opened) ? 1 : 0}
  ' "$1" || {
    printf 'ERROR: bloque Factory ambiguo en %s. Repará los delimitadores tras revisar el archivo; no se modifica.\n' "$1" >&2
    return 1
  }
}

# Same-directory exclusive temporary, unique backup and preserved metadata.
# No shared/predictable .new path; identical input is a complete no-op.
write_file() (
  local dest="$1" tmp backup
  safe_dir "$(dirname "$dest")" || exit 1
  safe_file "$dest" || exit 1
  tmp="$(mktemp "$(dirname "$dest")/.asf-write.XXXXXX")"
  trap 'rm -f "$tmp"' EXIT
  [[ ! -f "$dest" ]] || cp -p "$dest" "$tmp"
  cat > "$tmp"
  if [[ -f "$dest" ]]; then
    cmp -s "$tmp" "$dest" && exit 0
    backup="$(mktemp "$dest.backup-$(date +%Y%m%d-%H%M%S).XXXXXX")"
    cp -p "$dest" "$backup"
    printf 'BACKUP: %s\n' "$backup"
  fi
  safe_file "$dest" || exit 1
  mv -f "$tmp" "$dest"
)

copy_if_missing() {
  safe_file "$2" || return 1
  if [[ -f "$2" ]]; then
    printf 'KEEP: %s\n' "$2"
  elif $DRY_RUN; then
    printf 'WOULD CREATE: %s\n' "$2"
  else
    write_file "$2" < "$1"
    printf 'CREATE: %s\n' "$2"
  fi
}

project_preflight() {
  local entry
  for entry in docs docs/architecture docs/decisions docs/requirements .agents .agents/skills; do
    safe_dir "$PROJECT/$entry" || return 1
  done
  for entry in AGENTS.md PROJECT_PROFILE.md PROJECT_STATE.md CAPABILITY_MAP.md docs/AI_SOFTWARE_FACTORY_AGENTS_SNIPPET.md; do
    safe_file "$PROJECT/$entry" || return 1
  done
}

project_directories() {
  $DRY_RUN || mkdir -p "$PROJECT/docs/architecture" "$PROJECT/docs/decisions" \
    "$PROJECT/docs/requirements" "$PROJECT/.agents/skills"
}
