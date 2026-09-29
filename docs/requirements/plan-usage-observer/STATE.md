# Requirement State — plan-usage-observer

## Identificación

- **Ticket / slug:** plan-usage-observer
- **Title:** Medición observable por plan en el flujo habitual de Quiver
- **Status:** complete-with-notes
- **Phase:** S03 cerrada — T13 prospectivo reconciliado
- **Risk level:** N2
- **Last updated:** 2026-09-25

## Decisiones

- **Acceptance criteria:** approved — 01_ACCEPTANCE_CRITERIA.md v1
- **Selected option:** D01 — ledger JSON local privado, fuente nativa por respuesta y binding explícito
- **Test profile:** T2 — reforzado, aprobado para plan v1
- **Plan version:** v1
- **Plan review:** approved-with-notes — self review, 04_PLAN_REVIEW.md
- **Human plan approval:** approved — criterios v1, D01, T2 reforzado y plan v1; mensaje explícito del usuario del 2026-09-24
- **Execution authorization:** completed — S01/S02 completadas; S03 del plan v1 ejecutada con la fuente JSONL exacta y el intervalo prospectivo autorizados el 2026-09-25. No incluye otras sesiones ni precios comerciales.
- **Execution authorization request:** resuelta y ejecutada dentro de S03
- **Workflow size:** full
- **Documentary authorization:** encargo inicial del usuario del 2026-09-24 resumido en 00_REQUIREMENT.md; la implementación S01 fue autorizada después mediante mensajes separados. Delegación no autorizada.

## Ejecución

- **Current slice:** ninguna — S03 cerrada
- **Completed slices:** S01 — tokens atribuibles; S02 — lifecycle, tiempos y costos sintéticos; S03 — integración prospectiva acotada
- **Pending slices:** ninguna del plan v1
- **Pending required findings:** none
- **Implementation review:** approved-with-notes — S03, review inline; 05_IMPLEMENTATION_REVIEW.md
- **Review scope/evidence:** ajuste S03, fuente única autorizada, T13, 35 tests offline, privacidad y límites; sin findings obligatorios
- **Directed correction rounds:** 0 en S03; S01/S02 permanecen cerradas

## AI Strategy

Catálogo canónico leído: config/MODEL_CATALOG.md, v2.2.2, last verified 2026-09-20;
resolución de política del 2026-09-24. Procedimiento local:
skills/core/model-router/SKILL.md. Reglas: «Política inicial», «Selección proporcional
y registro de routing» (routing-v1), «Switch Benefit», «Downgrade» y «Review».
No prueba configuración efectiva ni disponibilidad por cuenta.

| Fase | Recomendación normativa | Motivo y verificación |
|---|---|---|
| Planning N2 | BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`), Medium; fallback GPT-5.6 Sol (`gpt-5.6-sol`), Medium | Propuesta reversible con contexto suficiente; contraste código/contratos y self review; no prueba del host |
| S01/S02 completadas | ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`), High; fallback GPT-5.6 Terra (`gpt-5.6-terra`), High | Recomendación normativa usada para integridad, persistencia y concurrencia; configuración efectiva no verificada |
| S03 completada | ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`), High; mismo fallback condicionado | Integración/privacidad/reconciliación; evidencia real acotada y review N2 inline |

- **Selection basis:** policy, no mediciones comparables de ahorro.
- **Current phase switch benefit:** MEDIUM durante S03; T13 y review se resolvieron con oráculos deterministas, sin insuficiencia material observada. No inferir configuración efectiva.
- **Switch threshold:** no se activó cambio de modelo; reevaluar solo ante un nuevo trabajo material.
- **Model gate required now:** no para el cierre de S03; una tarea futura requiere su propia evaluación.
- **Effective model/reasoning:** NO VERIFICADOS; intención de comenzar con Astra no demuestra runtime.
- **Availability:** pendiente en selector del usuario; catálogo o modelos de delegación no prueban selección del chat principal.
- **Escalation triggers:** riesgo de datos/seguridad material, insuficiencia con contexto suficiente, cambio de fuente/alcance; distinguir falta de evidencia de falta de capacidad.
- **Downgrade opportunities:** registro mecánico de decisión; no interrumpir cierre breve para cambiar sesión.
- **Estimated AI consumption:** unknown — sin estimación cuantitativa validada para los slices.

## Progreso y evidencia

- **Completed S01:** gate 04 PASS; 20/20 focalizados, 19/19 CE-v1, 173/173 globales y check-release PASS; review inline APROBADO CON NOTAS.
- **Completed S02:** lifecycle explícito, reporte v2/revisiones, tiempos por límites y costos sintéticos; 13/13 T2 y 6/6 regresiones afectadas PASS; F05–F07 cerrados.
- **Completed S03:** `S03-SOURCE-01` CLI 0.156.1 (`codex-tui`, `cli`), binding previo en byte `3365161`, refresh en el intervalo autorizado. T13: seis respuestas y 254927 tokens idénticos fuente/ledger, cero duplicados/excluidos, siete registros del turno de binding omitidos, prefijo e identidad preservados; revisión v2 n.º 1 persistida y binding deshabilitado al cierre. Suite offline 35/35 PASS. Ledger externo privado: `/private/tmp/quiver-plan-usage-s03.NoUN9eAY/usage.json` (solo puntero; ruta e IDs de fuente no persistidos aquí).
- **Limits:** el intervalo incluye el turno de aclaración previo a la tarea y el trabajo de guía; no es una métrica aislada de esa tarea. Lifecycle técnico/aceptación, duración, modelo, tier, pago y USD continúan unknown por falta de evidencia; el reporte marca incomplete por esos faltantes, sin inventarlos. La respuesta final y el cierre documental posteriores al refresh quedan fuera.
- **Real integration:** verificada para la captura prospectiva acotada y la conciliación T13; no demuestra cobertura de otras sesiones, hosts ni facturación.
- **Prior work:** PROJECT_STATE previo y 72 untracked preservados; cierres v1/v2.1 no reabiertos.

## Próxima acción

- **Next action:** esperar un nuevo requirement del usuario.
- **Why this is next:** S01–S03 del plan v1 están cerradas y no hay otra ejecución autorizada.
- **User action required:** true
- **Decision required:** nuevo alcance solo si el usuario solicita trabajo adicional.
- **Expected output:** nueva petición concreta.
- **After this:** evaluar el nuevo pedido desde su propio estado y autorización.
- **Blocked by:** none
- **Runtime limitation:** none
- **Runtime limitation detail:** ninguna. Python 3.14.4 validó S01–S03; Python 3.11 local no estaba disponible y CI remoto no se ejecutó.
- **Resume instruction:** leer PROJECT_STATE.md, este STATE, HANDOFF.md y 06_CLOSURE.md; conservar S01–S03 cerradas. No reabrir el intervalo ni refrescar nuevamente el binding sin nueva autorización.

## Decision Boundary

Decisiones resueltas: plan v1 y S01–S03 ejecutadas/cerradas con sus límites.
`S01-GATE-04` y T2 de S02 no se repiten sin regresión afectada. Boundary activo:
esperar nuevo requirement del usuario. Ver [HANDOFF](HANDOFF.md) y
[06_CLOSURE](06_CLOSURE.md).
