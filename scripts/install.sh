#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(factory_root)"
CODEX_DIR="$(codex_dir)"
AGENTS_FILE="$CODEX_DIR/AGENTS.md"
SKILLS_DIR="$(agents_skills_dir)"
DRY_RUN=false

if [[ $# -eq 1 && "$1" == "--dry-run" ]]; then
  DRY_RUN=true
elif [[ $# -gt 0 ]]; then
  echo "Uso: $0 [--dry-run]"
  exit 2
fi

safe_dir "$CODEX_DIR"
safe_dir "$HOME/.agents"
safe_dir "$SKILLS_DIR"
validate_managed_block "$AGENTS_FILE"
if [[ -s "$CODEX_DIR/AGENTS.override.md" ]]; then
  die "AGENTS.override.md tiene prioridad sobre AGENTS.md. Integrá las reglas que querés conservar y retiralo de uso explícitamente antes de repetir install. Factory no lo modifica."
fi

managed_block() {
  cat <<EOF
<!-- AI-SOFTWARE-FACTORY:START -->
## AI Software Factory

Instalación canónica:

\`$ROOT\`

Utilizo AI Software Factory como metodología reutilizable para proyectos nuevos y existentes.

Reglas globales:

- la Factory se adapta al proyecto;
- el repositorio actual es la fuente de verdad;
- el chat no es memoria persistente;
- cargar únicamente contexto relevante;
- integrar antes que migrar;
- no introducir capacidades SaaS si el producto no las necesita;
- utilizar Guided Mode;
- avanzar automáticamente hasta el próximo Decision Boundary;
- no preguntar "¿Cómo continuamos?" cuando la siguiente acción pueda derivarse del estado;
- cuando no se requiera decisión: \`ACCIÓN DEL USUARIO: ninguna\` y continuar;
- mantener \`PROJECT_STATE.md\` y requirement \`STATE.md\` con próxima acción explícita;
- testing proporcional al riesgo;
- AI Model Routing guiado: usar Model Gates solo cuando Switch Benefit sea HIGH;
- escribir siempre nombre completo + ID exacto de modelo;
- no asumir el modelo activo de la sesión;
- evidencia antes de afirmar éxito;
- skills bajo demanda;
- utilizar AI Model Routing por perfiles ECONOMICAL / BALANCED / ADVANCED;
- no fijar un único modelo para todo el proyecto;
- resolver perfiles concretos desde el catálogo central y configuración disponible;
- no afirmar cambios de modelo que el runtime no haya realizado;
- no usar worktrees, parallel agents, auditorías completas o infraestructura adicional por defecto.

Cuando un proyecto use AI Software Factory:

1. leer sus instrucciones locales;
2. leer \`PROJECT_STATE.md\`;
3. si hay requirement activo, leer su \`STATE.md\`;
4. consultar \`$ROOT/workflow/00_SHARED_CONTRACT.md\`;
5. cargar únicamente el workflow/skill requerido para la fase actual.

No buscar ni utilizar automáticamente otra copia de AI Software Factory si esta ruta no existe. Informar el problema.

Las reglas específicas del proyecto y decisiones aprobadas tienen prioridad sobre recomendaciones genéricas de Factory.
<!-- AI-SOFTWARE-FACTORY:END -->
EOF
}

if $DRY_RUN; then
  echo "AI Software Factory — dry run"
  echo
  echo "Factory: $ROOT"
  echo "Codex AGENTS: $AGENTS_FILE"
  echo "Skills: $SKILLS_DIR"
  echo
  echo "Se administrará únicamente el bloque:"
  echo "  <!-- AI-SOFTWARE-FACTORY:START -->"
  echo "  <!-- AI-SOFTWARE-FACTORY:END -->"
  echo
  echo "Skills core a enlazar:"
  for skill in "$ROOT"/skills/core/*; do
    [[ -d "$skill" ]] && echo "  - $(basename "$skill")"
  done
  exit 0
fi

mkdir -p "$CODEX_DIR" "$SKILLS_DIR"

{
  if [[ -f "$AGENTS_FILE" ]]; then
    remove_managed_block "$AGENTS_FILE"
  fi
  managed_block
} | write_file "$AGENTS_FILE"

echo "Configuración global actualizada: $AGENTS_FILE"

for skill in "$ROOT"/skills/core/*; do
  [[ -d "$skill" ]] || continue
  name="$(basename "$skill")"
  dest="$SKILLS_DIR/$name"

  if [[ -L "$dest" ]]; then
    current="$(readlink "$dest")"
    if [[ "$current" == "$skill" ]]; then
      echo "OK skill: $name"
    else
      echo "WARN skill '$name' ya es un symlink a: $current"
      echo "     No se modifica."
    fi
  elif [[ -e "$dest" ]]; then
    echo "WARN skill '$name' ya existe y no es un symlink."
    echo "     No se modifica: $dest"
  else
    ln -s "$skill" "$dest"
    echo "Instalada skill: $name"
  fi
done

echo
echo "Instalación completada."
echo "Siguiente paso:"
printf '  %q\n' "$ROOT/scripts/doctor.sh"
