# Implementation review — hardening

- Fecha: 2026-09-19.
- Modalidad: self review; sin reviewer independiente ni llamada remota.
- Alcance: plan v1 y F01–F14; scripts y lib, tests/CI, workflows, skills, templates, catálogo, onboarding y distribución. Base real `2c72d1c`, cambios locales sin commit; no atribuir todos los cambios del working tree a esta tarea.
- Resultado: aprobado con notas para cierre de las correcciones locales; publicación no autorizada ni certificada.

## Comprobaciones

Se inspeccionó implementación y diff, no solo un brief: flujo de validación antes de escrituras, destinos de symlinks, temporales/backups/permisos, qué elimina uninstall, argumentos/dry-run y estados de salida de doctor. La suite verifica filesystem antes/después y casos adversos en macOS/Linux; ver [EVIDENCE.md](EVIDENCE.md).

Se contrastaron aprobaciones, reanudación, Gates, testing, herencia de estrategia y límites del review entre contrato, workflows, templates, skills y guías. Se eliminaron reglas locales que contradecían la política canónica. No se confundió una aprobación de modelo con aprobación de implementación.

## Hallazgos de esta revisión

- Corregido: doctor salía abruptamente si fallaba el comando de versión de Codex; ahora advierte NO VERIFICADO y tiene prueba propia.
- Corregido: algunas formulaciones repetidas permitían Model Gates por review/escalamiento sin comprobar HIGH y confirmación previa; alineadas con el catálogo.
- Corregido: ejemplos de confirmación podían indicar acción ninguna sin considerar otros boundaries; aclaración explícita y template de requirement sin false predeterminado.
- Obligatorios pendientes dentro del plan: ninguno tras las verificaciones registradas.
- Nota no bloqueante para el cierre local: prueba real de modelos y reviewer adicional antes de publicación no ejecutados; no afirmar equivalencia con tests deterministas de scripts.

No se hicieron ciclos automáticos de review remoto. Los ajustes anteriores corresponden a una ronda dirigida de revisión local.
