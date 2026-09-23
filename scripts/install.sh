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

Factory version: 2.3.0-rc.2

- La Factory se adapta al proyecto: integrar antes que migrar; contexto/skills bajo demanda.
- Guided Mode: ejecutar trabajo autorizado hasta un Decision Boundary real.
- Finalization Gate: con trabajo pendiente ejecutable y usuario false, PROHIBIDO FINALIZAR.
  \`ACCIÓN DEL USUARIO: ninguna\` exige continuar en el mismo turno; no es cierre.
- Source of Truth: evidencia/código > requirement STATE > PROJECT_STATE > artifacts aprobados
  > docs > Conversation Recap > chat. Registrar contradicciones; STATE vence al recap.
- Mantener próxima acción, motivo, usuario requerido, resultado, después y reanudación;
  registrar limitaciones reales de runtime por separado. Evidencia antes de afirmar éxito.
- Testing proporcional; sin infraestructura, worktrees ni multi-agent por defecto.
- Routing: ECONOMICAL / BALANCED / ADVANCED desde config/MODEL_CATALOG.md;
  nombre completo + ID exacto. Perfil solicitado no prueba modelo/reasoning activo.
  Session Preflight solo por necesidad material; Model Gate solo con Switch Benefit HIGH.
- Aplicar model-router / routing-v1 antes de planificar/implementar: decisión breve o
  referencia vigente en STATE/brief; excepciones compactas del catálogo. Review verifica evidencia.

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
