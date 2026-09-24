# Acceptance criteria propuestos — Plan v1

Pendientes de aprobación humana junto con el plan v1.

| ID | Criterio observable |
|---|---|
| AC1 | A y B usan exactamente la misma pregunta, rubric, modelo/reasoning observado cuando esté disponible y límite total de 131072 bytes de contexto. |
| AC2 | Cada ejecución parte de los mismos OID fijados; un cambio de ref, HEAD, índice, status u overlay invalida el par antes de comparar resultados. |
| AC3 | A recibe solo evidencia de `CURRENT`; no recibe inventario, nombres, deltas ni conclusiones de otras refs. |
| AC4 | B recibe evidencia atribuida de `CURRENT`, `IOS_SIBLING` y un resumen determinista de cohortes; cada fragmento conserva ref/OID/ruta/blob. |
| AC5 | Tres pares independientes se ejecutan en orden predefinido `AB`, `BA`, `AB`; no se reutiliza conversación, respuesta ni cache semántica entre corridas. |
| AC6 | Un answer key privado, fijado antes de las corridas, puntúa hechos requeridos, omisiones, claims verificables y atribuciones cruzadas. No se entrega a los modelos evaluados. |
| AC7 | Branch-aware logra al menos 90% de recall de hechos requeridos en dos de tres corridas y mejora al menos 25 puntos porcentuales sobre HEAD-only, o reduce al menos tres omisiones cuando A responde legítimamente `unknown`. |
| AC8 | B tiene cero errores de atribución de severidad alta y no empeora la precisión de claims verificables frente a A. |
| AC9 | Ambos modos respetan el presupuesto; bytes, archivos, fragmentos y blobs únicos se miden. Tokens/costo solo se informan si el runtime los expone. |
| AC10 | Tiempo Git, tiempo de preparación, tiempo humano y tiempo de modelo se separan; lo no observable queda `unknown`. |
| AC11 | La integridad antes/después coincide para HEAD, refs, índice, status, diffs y contenido untracked; cualquier diferencia detiene el piloto. |
| AC12 | El review N2 decide `release candidate`, `ajustar` o `sin beneficio probado`; una corrida fallida o ambigua nunca se convierte en recomendación de release. |

## Incógnitas aceptadas

El benchmark no determina qué instalación está activa, ni prueba comportamiento de
OneSignal/backend en runtime. La respuesta correcta debe declarar esos límites.
