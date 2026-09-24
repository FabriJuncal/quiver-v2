# Plan review — Benchmark operativo v2

Fecha: 2026-09-23. Modalidad: **self review del coordinador; no independiente**.
Veredicto: **APROBADO CON NOTAS**.

## Trazabilidad

| Criterios | Paso | Validación |
|---|---|---|
| AC1, AC8 | P1, P3 | root nuevo, paquetes sin v1, hashes v2 distintos y sesiones independientes |
| AC2, AC9 | P2, P3 | hashes de prompt/schema, presupuesto y separación A/B por par |
| AC3, AC12 | P1, P3, P6 | baseline y snapshots after idénticos |
| AC4, AC5, AC6 | P2, P4 | `KEY_VALIDATION`, denominadores sellados y claims estructurados |
| AC7 | P2, P3 | sello previo, ausencia de respuestas y cadena de manifests |
| AC10, AC11 | P4 | scoring ciego cerrado, aritmética recalculada y agregación por par |
| AC13 | P0–P6 | provenance por métrica; ausencia de evidencia implica `unknown` |
| AC14 | P5 | reviewer distinto, muestra recalculada y cero obligatorios abiertos |
| AC15 | P6 | aplicación exacta de umbrales y conclusión limitada |
| AC16 | P0–P6 | diff/status, integridad del piloto y ausencia de publicación/delegación no autorizada |

## Revisión del protocolo

- Los denominadores ya no dependen de interpretar prosa después de las corridas.
- Recall de utilidad y recall acotado evitan confundir una limitación legítima de A con un
  error factual, sin ocultar la diferencia de utilidad entre modalidades.
- Precision, atribución y retrabajo tienen unidades contables explícitas.
- Los casos cero y `unknown` tienen comportamiento definido.
- El hash chain impide aceptar silenciosamente un cambio de contenido, pero no se presenta
  como firma de autoría ni timestamp confiable.
- Las respuestas v1 quedan fuera del corpus v2.

## AI Strategy

La solicitud ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High es proporcional al antecedente
de protocolo inválido y a la dificultad de detectar un segundo error antes de P4. El fallback
GPT-5.6 Terra (`gpt-5.6-terra`) / High o XHigh coincide con el catálogo. Configuración efectiva
`unknown`; esta revisión no la infiere. Para ejecución mecánica futura se propone BALANCED y
para review crítico ADVANCED, optimizando costo total sin bajar el control independiente.

## Findings

### Obligatorios

Ninguno abierto.

Corrección dirigida D1 cerrada durante el self review: se alineó el contrato para exigir
`forbidden_claims` no vacío, aplicabilidad de unknowns por modalidad y una relación máxima
de un fact ID por claim. No cambió alcance ni decisión humana.

### Opcionales

- **O1 — timestamp externo:** SHA-256 y los manifests prueban consistencia interna, no tiempo
  verificable por un tercero. Incorporar una timestamp authority requeriría una decisión de
  infraestructura fuera de alcance; por ahora la propiedad queda explícitamente `unknown`.

## Límite del veredicto

El veredicto aprueba la coherencia interna del plan para decisión humana. No aprueba el plan
en nombre del usuario, no autoriza P0–P6 y no prueba el comportamiento del futuro runtime.

Estado posterior: el usuario aprobó criterios, plan v2 y T3 el 2026-09-23, pero negó
expresamente P0–P6, respuestas, scoring, delegación y publicación.
