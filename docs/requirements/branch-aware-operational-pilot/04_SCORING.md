# P4 — Scoring ciego y agregación

Fecha de cierre: 2026-09-23. Resultado: **unscorable**.

## Avance recuperado y validado

- Scorer previo: sesión efímera nueva, labels `X1/Y1`, `X2/Y2`, `X3/Y3`.
- El mapa A/B permaneció fuera de su directorio y se abrió después de
  `blind_scoring_closed=true`.
- El scorer terminó con cero tool calls; configuración efectiva no expuesta.
- Las copias anonimizadas conservan los hashes de las seis respuestas originales.
- Scoring SHA-256: `39ea8fad727fb5a474b9f5da4750cff5d0c8f4e9bdfee5fd3c63ccbffdb3371f`.
- El answer key y las respuestas no se modificaron.

## Reconciliación post-unblind

El review N2 detectó que las observaciones ciegas que calificaban como incorrecta la ausencia
de evidencia `IOS_SIBLING` en `X1`, `Y2` y `X3` no son válidas después de abrir el mapa: las
tres respuestas son A y AC3 exigía que A recibiera solo `CURRENT`. El scoring ciego permanece
intacto y firmado; una reconciliación privada invalida esas tres observaciones sin convertirlas
en errores factuales ni en omisiones contables. El key no permite cuantificar omisiones de
utilidad retrospectivamente.

## Hallazgo bloqueante del protocolo

El answer key firmado antes de P3 contiene scope, paths, blobs, deltas, unknowns y claims
prohibidos, pero no fija un conjunto cerrado y denominador para recall/omisiones, unidades
contables para precisión ni una frontera exhaustiva entre omisiones de evidencia y utilidad.
Completarlo después de leer las respuestas violaría AC6. Recall, precisión, omisiones,
mejora por par y repetibilidad de calidad quedan `unknown`/`not_evaluable`.

## Agregación observable

| Métrica | A — HEAD-only | B — branch-aware |
|---|---:|---:|
| Corridas | 3 | 3 |
| Recall / precisión / omisiones | unscorable | unscorable |
| Atribuciones alta / baja | 0 / 0 en cada corrida | 0 / 0 en cada corrida |
| Bytes serializados, mediana (rango) | 43362 (0) | 87116 (0) |
| Archivos / fragmentos / blobs únicos | 5 / 5 / 5 | 10 / 10 / 9 |
| Bytes deduplicados | 0 | 3889 |
| Input tokens, mediana (rango) | 26376 (2786) | 37221 (0) |
| Output tokens, mediana (rango) | 2192 (349) | 3210 (717) |
| Cached input tokens, mediana (rango) | 9984 (4096) | 9984 (4096) |
| Reasoning output tokens, mediana (rango) | 138 (121) | 408 (358) |

Los tokens y cero tool calls fueron comprobados por el coordinador en los eventos crudos y
revisados en la ronda dirigida P5; no prueban el aislamiento efectivo, modelo ni costo. Los
flags de ejecución aislada están registrados en el manifest, pero su enforcement técnico
permanece `unknown`. Costo,
latencia, pasos manuales, minutos humanos y retrabajo temporal no fueron medidos. Se observó
un retry técnico previo a la única respuesta válida de la primera corrida A.

## Umbrales

| Umbral | Resultado |
|---|---|
| Integridad y frescura | PASS |
| B >= 90% recall en dos de tres | no evaluable |
| B mejora >= 25 pp o elimina >= 3 omisiones | no evaluable |
| B con cero atribuciones severidad alta | PASS según scoring ciego |
| Precisión B no inferior a A | no evaluable |
| Ambos modos <= 131072 bytes | PASS |
| Resultado favorable repetido en dos de tres | no evaluable |

No están demostrados todos los umbrales de release candidate. El resultado provisional
para P5 es **beneficio no probado**.
