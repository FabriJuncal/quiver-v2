# Plan v1 — AI Software Factory v2.2.2 — Runtime Guardrails

Autorizado por solicitud del usuario del 2026-09-20. Sin cambios de arquitectura,
código de proyectos, configuración personal, publicación ni multi-agent.

1. Verificar documentación oficial y CLI local: precedencia, perfiles, reasoning e instrucciones.
2. Centralizar Finalization Gate, cuatro invariants, runtime limitations y jerarquía de evidencia.
3. Incorporar launcher determinista, metadata y doctor de solo lectura; preservar instalación/adopción.
4. Actualizar routing, preflight, review acotado y guías de upgrade; versionar distribución y CI.
5. Ejecutar suite real aislada, revisar diff contra baseline y cerrar con evidencia y límites explícitos.

## Criterios verificables

- Contrato canónico prohíbe finalizar con trabajo autorizado ejecutable; templates/skills lo referencian.
- STATE vence al recap; estado activo exige próxima acción y permite persistir limitaciones de runtime.
- Launcher fija modelo/reasoning mediante flags, preserva argumentos seguros y guía ante errores.
- Doctor detecta estado inconsistente, capas antiguas, riesgo de truncamiento y configuración conflictiva sin escribir.
- Install/reinstall/uninstall, perfiles, launcher, init/adopt y fixtures de estado pasan en HOME temporal.
- Upgrade limita cambios a metadata/instrucciones/estado activo, conserva decisiones y slices cerradas.
- CI verifica scripts, archivos, versiones, mappings y regresiones sin llamadas a modelos.

## Testing / review

T2 focalizado: unittest sobre procesos reales y filesystem temporal, Codex simulado
para fallos deterministas; CLI real solo comandos sin inferencia. Sin E2E pago.
Review local del diff completo contra baseline y pruebas; /review no disponible
en esta distribución sin Git y no obligatorio para N2. No afirmar review independiente.
Mantener límite ya existente de una ronda dirigida de corrección en review formal.
