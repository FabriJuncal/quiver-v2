#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/lib/common.sh"

ROOT="$(factory_root)"
AGENTS_FILE="$(codex_dir)/AGENTS.md"
SKILLS_DIR="$(agents_skills_dir)"
PROJECT=""

if [[ $# -eq 2 && "$1" == "--project" ]]; then
  PROJECT="${2:-}"
  if [[ -z "$PROJECT" ]]; then
    echo "Uso: $0 [--project PATH]"
    exit 2
  fi
elif [[ $# -gt 0 ]]; then
  echo "Uso: $0 [--project PATH]"
  exit 2
fi

fail=0
warn=0

ok()   { printf '✓ %s\n' "$1"; }
warning() { printf '⚠ %s\n' "$1"; warn=$((warn+1)); }
bad()  { printf '✗ %s\n' "$1"; fail=$((fail+1)); }

echo "AI Software Factory Doctor"
echo "=========================="
echo

[[ -f "$ROOT/FACTORY_VERSION.md" ]] && ok "Factory encontrada: $ROOT" || bad "FACTORY_VERSION.md no encontrado"
version="$(factory_version)"
[[ -n "$version" ]] && ok "Versión: $version" || warning "No se pudo leer versión"

if grep -q "Guided Mode" "$ROOT/workflow/00_SHARED_CONTRACT.md" 2>/dev/null; then
  ok "Guided Mode"
else
  bad "Guided Mode no detectado en contrato"
fi

for marker in 'Finalization Gate' 'INVARIANT 1' 'INVARIANT 2' 'INVARIANT 3' 'INVARIANT 4' 'Runtime limitation'; do
  grep -q "$marker" "$ROOT/workflow/00_SHARED_CONTRACT.md" && ok "$marker" || bad "$marker ausente"
done
for resource in scripts/asf scripts/asf.sh scripts/lib/runtime_doctor.py docs/guides/RUNTIME_GUARDRAILS.md docs/guides/SESSION_PREFLIGHT.md; do
  [[ -f "$ROOT/$resource" ]] && ok "$resource" || bad "$resource ausente"
done

if grep -q "Decision Bound" "$ROOT/workflow/00_SHARED_CONTRACT.md" 2>/dev/null; then
  ok "Decision Boundaries"
else
  bad "Decision Boundaries no detectado"
fi

if grep -q "User action required" "$ROOT/templates/PROJECT_STATE.md" 2>/dev/null; then
  ok "PROJECT_STATE actualizado"
else
  bad "PROJECT_STATE no contiene User action required"
fi

if [[ -f "$ROOT/config/MODEL_CATALOG.md" ]]; then
  ok "Model Catalog"
else
  bad "config/MODEL_CATALOG.md no encontrado"
fi

if grep -q "AI Policy" "$ROOT/templates/PROJECT_PROFILE.md" 2>/dev/null; then
  ok "PROJECT_PROFILE con AI Policy"
else
  bad "PROJECT_PROFILE no contiene AI Policy"
fi

if grep -q "AI Strategy" "$ROOT/templates/requirement/STATE.md" 2>/dev/null; then
  ok "Requirement STATE con AI Strategy"
else
  bad "Requirement STATE no contiene AI Strategy"
fi

if grep -q "AI Execution Profile" "$ROOT/templates/slice/EXECUTION_BRIEF.md" 2>/dev/null; then
  ok "Execution Brief con AI Execution Profile"
else
  bad "EXECUTION_BRIEF no contiene AI Execution Profile"
fi

echo
echo "Codex"
echo "-----"

if command -v codex >/dev/null 2>&1; then
  codex_version="$(codex --version 2>/dev/null | sed -n 's/^codex-cli \([0-9]*\.[0-9]*\.[0-9]*\).*/\1/p' || true)"
  if [[ -z "$codex_version" ]]; then
    warning "Versión Codex NO VERIFICADA; ejecutar codex --version."
  elif awk -v version="$codex_version" 'BEGIN {split(version,v,"."); exit (v[1]>0 || v[2]>=134) ? 0 : 1}'; then
    ok "Codex $codex_version: soporta perfiles separados (mínimo 0.134.0)"
  else
    bad "Codex $codex_version no soporta estos perfiles; actualizá Codex a >= 0.134.0."
  fi
else
  warning "Codex CLI no encontrado en PATH"
fi

if ! safe_dir "$(codex_dir)" || ! validate_managed_block "$AGENTS_FILE"; then
  bad "Configuración global insegura o bloque inválido; corregir el destino antes de reinstalar."
elif [[ -f "$AGENTS_FILE" ]]; then
  ok "AGENTS global existe"
  grep -q "<!-- AI-SOFTWARE-FACTORY:START -->" "$AGENTS_FILE" \
    && ok "Bloque Factory instalado" \
    || bad "Bloque Factory no encontrado"

  grep -Fq "$ROOT" "$AGENTS_FILE" \
    && ok "Ruta canónica coincide" \
    || bad "AGENTS global no apunta a esta Factory"
  if ! sed -n '/^<!-- AI-SOFTWARE-FACTORY:START -->$/,/^<!-- AI-SOFTWARE-FACTORY:END -->$/p' "$AGENTS_FILE" | grep -Fq "Factory version: $version"; then
    warning "Capa global Factory desactualizada o sin versión. Ejecutá el install.sh de esta instalación y abrí una nueva sesión."
  fi
else
  bad "No existe $AGENTS_FILE"
fi

if [[ -s "$(codex_dir)/AGENTS.override.md" ]]; then
  bad "AGENTS.override.md tiene prioridad: Factory en AGENTS.md no se carga. Revisá el override, preservá sus reglas y resolvé explícitamente cuál usar."
fi

echo
echo "Perfiles opcionales (validación estática, sin llamadas a modelos)"
parser=""
for candidate in python3.14 python3.13 python3.12 python3.11 python3; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -I -B -c 'import tomllib' >/dev/null 2>&1; then
    parser="$candidate"
    break
  fi
done
for profile in "$(codex_dir)"/asf-*.config.toml; do
  [[ -e "$profile" || -L "$profile" ]] || continue
  if ! safe_file "$profile"; then
    bad "Perfil con destino inseguro: $profile"
  elif [[ -z "$parser" ]]; then
    warning "TOML NO VERIFICADO: $profile. Python >= 3.11 permite validarlo con doctor."
  elif "$parser" -I -B "$SCRIPT_DIR/lib/check_config.py" "$profile"; then
    ok "TOML válido: $(basename "$profile")"
  else
    bad "Perfil inválido: $profile. Corregilo y repetí doctor."
  fi
done


if [[ -f "$ROOT/config/MODEL_CATALOG.md" ]]; then
  ok "MODEL_CATALOG"
  grep -q "GPT-5.6 Luna" "$ROOT/config/MODEL_CATALOG.md" \
    && ok "GPT-5.6 Luna mapping" \
    || bad "MODEL_CATALOG no contiene GPT-5.6 Luna"
  grep -q "GPT-5.6 Terra" "$ROOT/config/MODEL_CATALOG.md" \
    && ok "GPT-5.6 Terra mapping" \
    || bad "MODEL_CATALOG no contiene GPT-5.6 Terra"
  grep -q "GPT-5.6 Sol" "$ROOT/config/MODEL_CATALOG.md" \
    && ok "GPT-5.6 Sol mapping" \
    || bad "MODEL_CATALOG no contiene GPT-5.6 Sol"
  grep -q "GPT-6 Astra" "$ROOT/config/MODEL_CATALOG.md" \
    && ok "GPT-6 Astra exceptional override" \
    || bad "MODEL_CATALOG no contiene GPT-6 Astra"
  grep -q "Switch Benefit" "$ROOT/config/MODEL_CATALOG.md" \
    && ok "Switch Benefit policy" \
    || bad "Switch Benefit no detectado"
else
  bad "MODEL_CATALOG no encontrado"
fi

[[ -f "$ROOT/skills/core/model-router/SKILL.md" ]] \
  && ok "model-router skill" \
  || bad "model-router skill no encontrada"

[[ -f "$ROOT/docs/guides/GUIDED_MODEL_GATES.md" ]] \
  && ok "Guided Model Gates guide" \
  || bad "Guided Model Gates guide no encontrada"

echo
echo "Skills"
echo "------"

for skill in "$ROOT"/skills/core/*; do
  [[ -d "$skill" ]] || continue
  name="$(basename "$skill")"
  dest="$SKILLS_DIR/$name"
  if [[ -L "$dest" ]] && [[ "$(readlink "$dest")" == "$skill" ]] && [[ -f "$dest/SKILL.md" ]]; then
    ok "$name"
  elif [[ -e "$dest" ]]; then
    warning "$name existe pero no apunta a esta Factory"
  else
    bad "$name no instalado"
  fi
done

echo
echo "Herramientas"
echo "------------"
command -v git >/dev/null 2>&1 && ok "Git" || bad "Git no encontrado"
command -v bash >/dev/null 2>&1 && ok "Bash" || bad "Bash no encontrado"

if [[ -n "$PROJECT" ]]; then
  echo
  echo "Proyecto"
  echo "--------"
  PROJECT="$(cd "$PROJECT" 2>/dev/null && pwd -P || true)"
  if [[ -z "$PROJECT" ]]; then
    bad "Ruta de proyecto inválida"
  else
    echo "Ruta: $PROJECT"
    for f in AGENTS.md PROJECT_PROFILE.md PROJECT_STATE.md CAPABILITY_MAP.md; do
      [[ -f "$PROJECT/$f" ]] && ok "$f" || warning "$f no encontrado"
    done
    if [[ -s "$PROJECT/AGENTS.override.md" ]]; then
      warning "AGENTS.override.md del proyecto prevalece sobre AGENTS.md: verificar que conserve la integración Factory."
    fi
    if [[ -f "$PROJECT/.codex/config.toml" ]]; then
      warning "Existe config del proyecto: puede prevalecer sobre --profile. Si la selección es material: /status; si difiere de lo solicitado, pegá el resultado; si coincide, continuar."
    fi
    [[ -d "$PROJECT/docs/requirements" ]] \
      && ok "docs/requirements/" \
      || warning "docs/requirements/ no encontrado"
  fi
fi

if [[ -n "$parser" ]]; then
  helper_status=0
  "$parser" -I -B "$SCRIPT_DIR/lib/check_assistant_proposal.py" || helper_status=$?
  if [[ "$helper_status" -eq 2 ]]; then
    warning "Ayudante DISABLED: propuesta válida; runtime/piloto NO VERIFICADOS. Seguir inline; ver ASSISTANT_INTEGRATION.md."
  else
    bad "Propuesta de ayudante inválida o resultado inesperado; no habilitar delegación."
  fi
  runtime_args=(--root "$ROOT" --codex-home "$(codex_dir)")
  [[ -z "$PROJECT" ]] || runtime_args+=(--project "$PROJECT")
  runtime_report="$("$parser" -I -B "$SCRIPT_DIR/lib/runtime_doctor.py" "${runtime_args[@]}" 2>&1)" || bad "Runtime guardrails: corregir errores indicados debajo."
  printf '%s\n' "$runtime_report"
  if [[ "$runtime_report" == *'WARN:'* ]]; then warning "Diagnóstico estático con advertencias (ver acciones arriba)."; fi
else
  warning "Runtime guardrails/AGENTS size/project state NO VERIFICADOS. Instalá Python >= 3.11 y repetí doctor.sh --project ."
fi

echo
echo "Alcance: archivos, enlaces y configuración estática. Disponibilidad, reasoning efectivo y review en runtime: NO VERIFICADOS."
echo "Solo si la próxima tarea depende materialmente de configuración: /status; si coincide, continuar; si difiere, pegá el resultado."
if (( fail > 0 )); then
  echo "STATUS: FAIL ($fail error/es, $warn warning/s)"
  exit 1
elif (( warn > 0 )); then
  echo "STATUS: OK WITH WARNINGS ($warn)"
  exit 0
else
  echo "STATUS: OK"
fi
