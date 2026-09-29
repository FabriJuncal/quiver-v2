# D01 aprobada — histórico prospectivo con marcas explícitas

**Estado: aprobada con plan v1 y ejecutada el 2026-09-25.**

Un binding nuevo puede incluir proyecto, identificador opaco de trabajo y una
categoría primaria: `feature`, `bug`, `test`, `explanation` o `documentation`.
La categoría se confirma antes de medir. Kev puede sugerirla desde un resumen
breve proporcionado por el usuario a un endpoint local, pero nunca clasifica
silenciosamente el log ni abre sesiones. Si Kev no está disponible, se elige
manualmente. Un trabajo que mezcla categorías se divide en bindings explícitos;
el observador no reparte tokens automáticamente dentro de un turno.

El histórico se calcula desde la última revisión v2 persistida de cada binding
nuevo y marcado. Agrupa por proyecto, trabajo y categoría, sin sumar dos veces
revisiones ni incorporar bindings anteriores. Muestra tokens observados y
cobertura. Tiempo se etiqueta como transcurrido/no pausado con límites lifecycle
explícitos; no se llama actividad.

USD real se mantiene unknown salvo declaración de un importe directo con
referencia opaca de comprobante, moneda USD y cobertura completa/parcial. Esa
declaración se etiqueta como aportada por el usuario, no verificada por Quiver;
no se convierten subtotales `synthetic` en gasto. La misma evidencia no puede
asignarse dos veces en el ledger. Suscripciones y asignaciones proporcionales
quedan fuera hasta contar con un contrato de facturación específico.

## Alternativas y trade-offs

| Opción | Resolución |
|---|---|
| D01: marca por binding + vista histórica del ledger existente | Reutiliza checkpoint, lock y reportes; exige tarea dedicada y snapshot explícito; recomendada |
| Desglose de fases dentro de un binding | Más detalle, pero necesita fronteras y asignación de respuestas que el contrato v1 no observa; diferida |
| Kev como clasificador automático obligatorio | Requiere instalar/servir pesos y enviar texto; error de categoría afectaría contabilidad; usar solo sugerencia local opt-in |
| Importar sesiones/reportes previos | Podría llenar el histórico de inmediato, pero contradice la elección prospectiva y permisos previos; excluida |

**Testing:** T2 dirigido con fixtures artificiales, 46/46 PASS. Estrategia de modelo
en [STATE](STATE.md#ai-strategy); configuración efectiva desconocida.
