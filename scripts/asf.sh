#!/usr/bin/env bash
# Deterministic startup intent; account availability remains a runtime concern.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/lib/common.sh"

usage() { echo 'Uso: asf economical|balanced|advanced|exceptional [--dry-run] [--cd PATH] [opciones seguras] [-- PROMPT]'; }
[[ $# -gt 0 ]] || { usage; exit 2; }
PROFILE="$1"
shift
case "$PROFILE" in
  economical) MODEL='gpt-5.6-luna'; NAME='GPT-5.6 Luna'; EFFORT=low; LABEL=Low ;;
  balanced) MODEL='gpt-5.6-terra'; NAME='GPT-5.6 Terra'; EFFORT=medium; LABEL=Medium ;;
  advanced) MODEL='gpt-5.6-sol'; NAME='GPT-5.6 Sol'; EFFORT=high; LABEL=High ;;
  exceptional) MODEL='gpt-6-astra'; NAME='GPT-6 Astra'; EFFORT=high; LABEL=High ;;
  -h|--help) usage; exit 0 ;;
  *) usage; exit 2 ;;
esac
DRY_RUN=false
ARGS=()
PROMPT=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    -C|--cd|--add-dir|-i|--image|-s|--sandbox|-a|--ask-for-approval)
      [[ $# -ge 2 && -n "$2" ]] || die "Falta valor para $1. Ejecutá asf --help."
      ARGS+=("$1" "$2"); shift 2 ;;
    --cd=*|--add-dir=*|--image=*|--sandbox=*|--ask-for-approval=*) ARGS+=("$1"); shift ;;
    --no-alt-screen|--search|--help|--version) ARGS+=("$1"); shift ;;
    --)
      shift
      [[ $# -le 1 ]] || die 'Un único PROMPT después de --; encerralo entre comillas.'
      if [[ $# -eq 1 ]]; then PROMPT=(-- "$1"); fi
      break ;;
    -*) die "Opción no admitida: $1. El launcher fija modelo/reasoning; usá codex directamente para otros overrides. Ejecutá asf --help." ;;
    *)
      [[ ${#PROMPT[@]} -eq 0 ]] || die 'Un único PROMPT; encerralo entre comillas.'
      PROMPT=(-- "$1"); shift ;;
  esac
done
fallback() {
  printf '\nNO SE PUDO INICIAR EL PERFIL\n\nQUÉ HACER\n\n'
  printf '1. ejecutá:\n   codex\n\n2. ejecutá:\n   /model\n\n'
  printf '3. seleccioná:\n   %s (%s)\n   %s\n\n' "$NAME" "$MODEL" "$LABEL"
  printf '4. escribí:\n   continuar\n\n'
  printf 'Si no aparece, pegá el resultado de /model y escribí: Disponibles: [IDs visibles].\n'
  printf 'No hay fallback automático. Conservá el error original para diagnosticarlo.\n'
  printf 'ACCIÓN DEL USUARIO: requerida\n' >&2
}
printf 'AI Software Factory\n\nProfile:\n%s\n\nModel:\n%s\n%s\n\nReasoning:\n%s\n\n' \
  "$(printf '%s' "$PROFILE" | tr '[:lower:]' '[:upper:]')" "$NAME" "$MODEL" "$LABEL"
if ! command -v codex >/dev/null 2>&1; then
  echo 'Codex CLI no está instalado o no está en PATH. Instalalo siguiendo https://developers.openai.com/codex/cli/ y repetí este comando.' >&2
  fallback
  exit 127
fi
CMD=(codex --model "$MODEL" --config "model_reasoning_effort=\"$EFFORT\"")
if [[ ${#ARGS[@]} -gt 0 ]]; then CMD+=("${ARGS[@]}"); fi
if [[ ${#PROMPT[@]} -gt 0 ]]; then CMD+=("${PROMPT[@]}"); fi
if $DRY_RUN; then
  printf 'DRY RUN (sin iniciar sesión; disponibilidad NO VERIFICADA):\n'
  printf '%q ' "${CMD[@]}"
  printf '\n'
  exit 0
fi
echo 'Launching Codex...'
if "${CMD[@]}"; then
  exit 0
else
  result=$?
  fallback
  exit "$result"
fi
