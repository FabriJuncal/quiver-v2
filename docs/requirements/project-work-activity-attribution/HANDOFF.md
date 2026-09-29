# Handoff — contrato OTel v1.2-r3 listo para revisión

2026-09-29. La corrección documental autorizada de H-C2/H-C4 terminó sin abrir
procesos ni repetir el preflight. El contrato actual es
[OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md), versión v1.2-r3,
SHA-256
`ac685955886ba10a1171a5f7787c0d0195613661215f2cd400ded35097da60ad`.

## Resultado verificable

- H-C2 fija `CODEX_HOME`, `CODEX_SQLITE_HOME`/`sqlite_home` y `log_dir` dentro de
  una única raíz temporal.
- El observador debe autocomprobarse con un descriptor centinela y controles
  negativos antes de abrir herdr. El PASS exige selección AND entre el PID nativo
  exacto y un descriptor SQLite/log conocido; el rollout no es el único oráculo.
- H-C4 se ejecuta desde un supervisor externo revisado. Debe haber cero procesos
  Codex antes del baseline y durante la ventana solo puede existir el árbol
  iniciado por ese supervisor.
- El supervisor toma ambos inventarios, coordina el cierre, elimina el temporal y
  compara antes de permitir que otra sesión Codex lea el resultado sanitizado.
- A2/D12-AUTH, P1–P4, R-OTEL-C12-01/02/03 y todos los cierres anteriores se
  conservan. Los tres cambios HMAC históricos continúan sin causa atribuida.

La corrección todavía no demuestra viabilidad viva ni está aprobada por review.
No se abrió Codex, herdr, pane, sesión, login o red; no se leyó sesión,
credencial, ruta personal cambiada o valor de configuración. No hubo preflight,
H-C5/Paso 3, dependencias, cambios globales, publicación o commit.

## Única siguiente acción

Autorizar una revisión documental de v1.2-r3 limitada a H-C2, H-C4 y los efectos
directos de la corrección. La revisión no corrige el contrato ni ejecuta el
preflight. Si cierra, se solicitará por separado la aprobación del contrato
concreto antes de preparar otra ejecución.

## Mensaje para continuar

> En Quiver, revisá únicamente OTEL_PILOT_CONTRACT_v1.2.md versión v1.2-r3 aplicando 04_REVISAR_PLAN.md, limitado a H-C2, H-C4 y los efectos directos de la corrección. Verificá que CODEX_HOME, CODEX_SQLITE_HOME/sqlite_home y log_dir queden dentro de una única raíz temporal; que la autocomprobación positiva/negativa y el vínculo lsof con selección AND prueben el PID nativo exacto contra un descriptor SQLite/log conocido; y que el supervisor externo pueda demostrar cero procesos Codex preexistentes, mantener únicamente el árbol controlado, inventariar, cerrar, revertir y comparar antes de abrir otra sesión. Conservá A2/D12-AUTH, P1–P4, R-OTEL-C12-01/02/03 y todos los hallazgos y cierres anteriores. No atribuyas los tres cambios HMAC históricos ni des por demostrada la viabilidad viva. Registrá el veredicto en OTEL_PLAN_REVIEW.md, EVIDENCE.md, STATE.md, PROJECT_STATE.md y HANDOFF.md con una única siguiente acción. No corrijas el contrato, abras procesos, sesiones, panes, login o red autenticada; no ejecutes preflight, H-C5/Paso 3, leas sesiones, credenciales, rutas personales cambiadas o valores de configuración, instales dependencias, delegues ni cambies router, launcher o configuración global. No publiques ni hagas commit.
