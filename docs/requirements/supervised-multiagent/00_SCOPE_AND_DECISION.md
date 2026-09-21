# Alcance, decisión y criterios — v1

## Necesidad y autorización

Incluir Factory multiagente supervisada sin diseñar un orquestador propio. Usuario
aprobó opción A: aceptar que «no escribir» sea una instrucción supervisada, no una
garantía técnica. Esta etapa prepara el plan y las pruebas, no activa la función.

Base: P01–P04 de [guided-delegation-pilot](../guided-delegation-pilot/STATE.md)
completadas; [preflight](../delegation-config-preflight/REPORT.md) conservado como
evidencia histórica. Su configuración permanece inactiva y no se declara reparada.
No se ha vuelto a comprobar compatibilidad del cliente en esta etapa documental.

## Decisión D01 — controles distintos, sin garantía falsa

| Control | Tratamiento propuesto |
|---|---|
| No escribir en la copia de trabajo | Instrucción explícita + comparación final; no prevención demostrada |
| Proyecto original y configuración habitual | No autorizar escrituras; exigir protección efectiva antes de piloto vivo, no asumirla por usar una copia |
| Copia y contexto | Allowlist de archivos regulares, contenido revisado, sin secretos, enlaces ni configuración personal; copiar nunca equivale a sandbox |
| Acciones externas mutantes | Siguen prohibidas; controles efectivos obligatorios para habilitar piloto |
| Recursión | Sigue prohibida; no se aprobó sustituir el control efectivo por una promesa del hijo |
| Fin, cancelación y ownership | Evidencia observable; desconocido impide reasignación o nueva ejecución |
| Comparaciones antes/después | Detectan diferencias persistentes dentro del alcance registrado, no actividad transitoria ni ausencia de efectos externos |

Propuesta de política nueva: `supervised-audited-v1`. No reinterpretar la existente
`supervised-sequential-v1` ni migrar registros cerrados. Hasta aprobación e
implementación del nuevo contrato, [guía vigente](../../guides/GUIDED_DELEGATION.md)
sigue operativa. Este documento no es una autorización de dispatch.

## D02 — mínima experiencia inicial

Inline por defecto. Un coordinador integra y escribe estado; un ayudante máximo,
secuencial, para análisis/revisión o propuesta textual. No desarrolladores paralelos,
escrituras deliberadas del hijo, cambios invisibles de modelo ni agentes recursivos.
El primer piloto futuro: datos sintéticos, un encargo, un intento, sin retry automático.
El techo existente de dos intentos para el contrato general no se amplía.

Antes/después registrar inventario de la copia (paths, tipos, hashes y permisos),
identidad/base del original y diff relevante. La medición no es un control de acceso.
Si aparecen cambios inesperados, conservar evidencia y marcar entrega rechazada.
Tras confirmar detención, poner la copia en cuarentena lógica (no reutilizable);
«descartar» significa excluir su resultado, no borrar archivos automáticamente.
Si el original cambió, no atribuirlo automáticamente al hijo ni restaurarlo: detener
integración y pedir reconciliación, preservando trabajo humano y evidencia.

## D03 — recuperación e integración

Reutilizar estados de slices e intentos existentes. Incidente se registra como razón
y evidencia, no como otra máquina de estados. Si no se puede confirmar fin, mantener
observación unknown y cupo ocupado. El padre no «arregla» restaurando el original.
Propuestas se inspeccionan como datos; nunca ejecutar comandos recibidos del hijo.
Solo el padre aplica cambios aprobados sobre base vigente, ejecuta tests y acepta.
Detectar una diferencia no demuestra quién la causó ni que la supervisión fue completa.

## Criterios de aceptación para implementación propuesta

- **AC01:** opt-in nuevo explícito, inline intacto, sin habilitación ni migración silenciosa.
- **AC02:** distinguir requested, enforced, observed y unknown por control; ninguna instrucción, hash o declaración del hijo equivale a enforcement.
- **AC03:** copia mínima con manifest, sin secretos conocidos, symlinks/hardlinks ni rutas externas; ningún checker escribe sobre el original.
- **AC04:** detectar cambios persistentes agregados/modificados/borrados y de tipo/permisos; incidente rechaza entrega y preserva evidencia, sin rollback automático.
- **AC05:** aceptación solo con entrega vigente, evidencia de fin, base válida, revisión del padre y validación proporcional; hijo DONE no cierra slice.
- **AC06:** límites existentes conservados: cupo uno, sin recursión, intentos acotados, no retry con trabajo unknown ni reset por otro ID/modelo.
- **AC07:** contratos históricos y proyectos inline siguen válidos; records nuevos no pueden disfrazarse de política estricta antigua.
- **AC08:** usuario conoce último evento observable, pendiente, riesgo y próxima acción; sin progreso/modelo/costo inventados; continuar trabajo autorizado cuando corresponda.
- **AC09:** preparación y tests no llaman modelos, instalan configuración, publican, ni usan servicios externos; piloto vivo separado y no autorizado por tests verdes.
- **AC10:** límites explícitos: cambios transitorios/no observados y acciones externas no se prueban con snapshots; modelo y costo siguen unknown sin evidencia.

Fuera de alcance: dispatcher, scheduler, locks, worktrees por defecto, aislamiento
nuevo de sistema operativo, compatibilidad Codex certificada, release/versionado,
configuración personal, piloto vivo y afirmaciones de ahorro. No se promete que
este cambio por sí solo quite todos los blockers del preflight anterior.
