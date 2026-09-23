#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(factory_root)"
PROJECT="$(pwd -P)"
DRY_RUN=false

if [[ $# -eq 1 && "$1" == "--dry-run" ]]; then
  DRY_RUN=true
elif [[ $# -gt 0 ]]; then
  echo "Uso: $0 [--dry-run]"
  exit 2
fi

project_preflight
project_directories

if [[ -f "$PROJECT/AGENTS.md" ]]; then
  echo "KEEP: $PROJECT/AGENTS.md"
  snippet="$PROJECT/docs/AI_SOFTWARE_FACTORY_AGENTS_SNIPPET.md"
  if [[ ! -f "$snippet" ]] && ! $DRY_RUN; then
    write_file "$snippet" <<'EOF'
# AI Software Factory — snippet para AGENTS.md existente

Este repositorio utiliza AI Software Factory.

Factory version: 2.3.0-rc.2 (propuesta; integrar en AGENTS antes de declarar la capa actualizada).

Antes de cambios significativos:
- leer PROJECT_STATE.md;
- leer requirement STATE.md activo;
- usar Guided Mode;
- avanzar hasta el próximo Decision Boundary;
- no declarar éxito sin evidencia;
- integrar antes que migrar.
- aplicar Finalization Gate e invariants de workflow/00_SHARED_CONTRACT.md de la Factory canónica;
- trabajo autorizado ejecutable + User action required false obliga a continuar en el mismo turno;
- STATE prevalece sobre Conversation Recap; registrar contradicciones;
- persistir runtime limitations, pendiente y reanudación exacta sin fingir cierre.
- aplicar model-router / routing-v1 del catálogo de Factory antes de planificar/implementar;
- registrar decisión breve o referencia vigente en STATE/brief; review verifica evidencia;
- respetar ruta rápida y excepciones N0/consultas; no inferir modelo activo ni crear gates por trámites.
EOF
    echo "CREATE: $snippet"
    echo "Discovery debe comparar este snippet con AGENTS.md, integrar solo reglas compatibles si está autorizado y registrar el resultado."
  fi
else
  copy_if_missing "$ROOT/templates/AGENTS.md" "$PROJECT/AGENTS.md"
fi

copy_if_missing "$ROOT/templates/PROJECT_PROFILE.md" "$PROJECT/PROJECT_PROFILE.md"
copy_if_missing "$ROOT/templates/PROJECT_STATE.md" "$PROJECT/PROJECT_STATE.md"
copy_if_missing "$ROOT/templates/CAPABILITY_MAP.md" "$PROJECT/CAPABILITY_MAP.md"

if $DRY_RUN; then
  echo "Dry run: se crearían los directorios de documentación/skills faltantes y el snippet si AGENTS.md ya existe. Ninguna escritura realizada."
  exit 0
fi

echo
echo "Scaffold no destructivo creado."
echo "No se modificó código de aplicación."
echo
echo "Siguiente mensaje sugerido para Codex:"
echo 'Abrí: codex. Después pegá:'
cat <<'EOF'
Adoptá este proyecto existente usando AI Software Factory.

Comenzá por Project Discovery.
No modifiques código ni arquitectura durante el discovery inicial.

Completá:
- PROJECT_PROFILE.md
- CAPABILITY_MAP.md
- PROJECT_STATE.md

Integrá antes que migrar.
Revisá el snippet de AGENTS si existe; registrá si quedó integrado, ya cubierto o si hay un conflicto concreto que deba decidir.
Guiame hasta el próximo Decision Boundary.
EOF
