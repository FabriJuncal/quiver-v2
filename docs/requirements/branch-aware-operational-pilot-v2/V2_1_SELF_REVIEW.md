# Self review — delta documental v2.1

Fecha: 2026-09-23. Modalidad: **self review del coordinador; no independiente**.
Veredicto: **APROBADO CON NOTAS**.

## Trazabilidad

| Criterio | Protocolo | Validación |
|---|---|---|
| V21-AC01 | alcance, denylist v1 | seis hashes nuevos; ninguna respuesta v1 en paquetes |
| V21-AC02 | frescura focalizada | `check` de dos manifests y snapshot igual al baseline |
| V21-AC03 | derivation manifest | reproducción, hashes, cambio permitido y scan sensible |
| V21-AC04 | key cerrado | `KEY_VALIDATION`, `K>0`, IDs/evidence refs válidos |
| V21-AC05, V21-AC06, V21-AC07 | paquetes y formato | hashes iguales de prompt/schema, presupuesto y validación estructural |
| V21-AC08 | scoring ciego | numeradores/denominadores/IDs, hash previo al mapa y penalizaciones justificadas |
| V21-AC09 | sello único | inputs firmados antes de respuestas; cada run referencia el sello |
| V21-AC10 | umbrales | fracciones exactas y tres pares válidos |
| V21-AC11 | P5 acotada | muestra A/B y un par completo recalculados; cero obligatorios abiertos |
| V21-AC12 | resultado | regla exhaustiva de tres salidas y conclusión sin release |
| V21-AC13 | límites | snapshots, diff y autorizaciones separadas |

## Revisión de proporcionalidad

- El único denominador cerrado resuelve el defecto de v1 sin sostener dos recalls que no
  cambian la decisión.
- Los umbrales `0.90`, `0.25` o tres omisiones, precisión no inferior y cero errores graves
  se conservan; no se inventa un criterio de éxito más favorable.
- Exigir tres pares válidos evita convertir una corrida incompleta en evidencia negativa o
  positiva.
- Los fragmentos derivados permiten excluir E-SENS-01 con provenance auditable. El protocolo
  distingue fuente y derivado y no afirma identidad byte a byte.
- El sello único conserva precedencia e integridad; retirar la cadena entre corridas no
  afecta la pregunta porque cada manifest sigue ligado al mismo input congelado.
- T2 reforzado cubre privacidad, drift, denominadores, contaminación, errores de atribución
  y recuperación por detención. T3 no añade evidencia decisiva al no haber cambios de
  producto, datos o runtime.

## AI Strategy

ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High es proporcional para el delta, key y review
por el fallo contractual de v1 y E-SENS-01. BALANCED — GPT-5.6 Terra
(`gpt-5.6-terra`) / Medium es suficiente para pasos deterministas y corridas comparables.
Effective session config permanece `unknown`; la revisión valida artefactos, no identidad
del runtime.

## Findings

### Obligatorios

Ninguno abierto.

### Opcionales

- **O1 — modelo efectivo:** seguirá `unknown` si el runtime no lo expone. No bloquea el
  benchmark, pero impide atribuir el resultado a una identidad de modelo comprobada.
- **O2 — timestamp externo:** el sello prueba consistencia y orden registrado, no tiempo
  autenticado por un tercero. No es necesario para la comparación local.

## Límite del veredicto

Este review aprueba coherencia interna para decisión humana. No aprueba v2.1 en nombre del
usuario, no resuelve E-SENS-01 y no autoriza P2–P6, delegación ni publicación.

Estado posterior: el usuario aprobó el delta v2.1 y T2 reforzado el 2026-09-23. La misma
instrucción mantuvo P2–P6, sanitización, respuestas, scoring, delegación y publicación sin
autorización.
