# Informe del benchmark operativo branch-aware

Fecha: 2026-09-23. Plan: v1. Alcance: tarea documental que requiere evidencia de otra
variante. Estado: final, review N2 `APROBADO CON NOTAS`.

## Resultado ejecutivo

El plan v1 no permite probar un beneficio comparativo. La integridad y frescura del snapshot,
el presupuesto y la ausencia observada de atribuciones severas pasaron sus controles,
pero el answer key firmado no define denominadores para recall, omisiones ni precisión.
Completarlo después de las respuestas contaminaría el protocolo.

Resultado final: **beneficio no probado**.

## Comparación por corrida

| Par | A — bytes; input/output tokens | B — bytes; input/output tokens | Calidad relativa |
|---:|---:|---:|---|
| 1 | 43362; 26376/2305 | 87116; 37221/3916 | recall/precisión/omisiones unscorable; unknown |
| 2 | 43362; 26376/1956 | 87116; 37221/3199 | recall/precisión/omisiones unscorable; unknown |
| 3 | 43362; 29162/2192 | 87116; 37221/3210 | recall/precisión/omisiones unscorable; unknown |

Todas las corridas registraron cero tool calls. El orden de ejecución fue AB, BA, AB; la tabla
normaliza columnas por modalidad para comparar cada par.

## Comparación agregada

| Métrica | A — HEAD-only | B — branch-aware | Evidencia |
|---|---:|---:|---|
| Cobertura de refs/tips | no aplica al paquete A | 95 refs; 82/82 tips | snapshot estático |
| Recall / precisión / omisiones | unscorable | unscorable | unknown por key insuficiente |
| Atribuciones severidad alta/baja | 0/0 en 3 corridas | 0/0 en 3 corridas | scoring ciego |
| Bytes serializados, mediana (rango) | 43362 (0) | 87116 (0) | medido |
| Archivos / fragmentos / blobs únicos | 5 / 5 / 5 | 10 / 10 / 9 | medido |
| Deduplicación | 0 bytes | 3889 bytes | medido por blob compartido |
| Input tokens, mediana (rango) | 26376 (2786) | 37221 (0) | evento del runtime |
| Output tokens, mediana (rango) | 2192 (349) | 3210 (717) | evento del runtime |
| Cached input tokens, mediana (rango) | 9984 (4096) | 9984 (4096) | evento del runtime |
| Reasoning output tokens, mediana (rango) | 138 (121) | 408 (358) | evento del runtime |
| Costo / latencia | unknown | unknown | no expuesto/no medido |
| Tiempo Git | unknown | unknown | el estado previo reporta una medición de planning, pero su fuente no integró el paquete P5 |
| Preparación / tiempo humano / pasos manuales | unknown | unknown | no instrumentado |
| Retrabajo | un retry técnico; minutos unknown | minutos unknown | observación parcial |
| Frescura / integridad | PASS / PASS | PASS / PASS | snapshots exactos |

Pasaron integridad/frescura, presupuesto y cero atribuciones severas en B según el scoring.
No son evaluables recall absoluto, mejora, omisiones, precisión relativa ni repetibilidad.
El conjunto completo de umbrales de release candidate no está satisfecho.

## Hechos, inferencias y unknowns

Hechos medidos: seis respuestas preservadas con hashes estables, presupuesto respetado,
tokens y cero tool calls comprobados por el coordinador en eventos crudos, y snapshots de
integridad iguales. El orden AB/BA/AB y los flags de aislamiento están registrados en el
manifest; el enforcement efectivo del aislamiento no es verificable desde estos artefactos.

Inferencia limitada: B transportó más evidencia y produjo respuestas más extensas en tokens;
eso no demuestra mayor calidad ni ahorro económico.

Unknowns: recall, precisión, omisiones, repetibilidad de calidad, costo, latencia, tiempo
humano, pasos manuales, minutos de retrabajo, configuración efectiva de modelo/reasoning y
conducta en dispositivo/backend.

## Desviaciones y límites

- La primera invocación de una corrida A falló antes de una sesión completa; el retry generó
  la única respuesta válida.
- Los eventos de la tercera corrida A contienen un warning no mutante sobre descripciones de
  Skills acortadas por presupuesto de contexto. La corrida completó con una respuesta y cero
  tool calls; su impacto efectivo sobre la respuesta es `unknown` y no se usa para rescatar
  ni rechazar métricas ya unscorable.
- El coordinador P3 abrió una vez esa respuesta para confirmar escritura; no actuó como scorer.
- El scorer pudo inferir modalidad por contenido; el cegado ocultó el mapa, no garantizó doble ciego.
- Después de revelar el mapa, el review invalidó tres observaciones del scoring sobre
  respuestas A: no recibir evidencia del sibling era el diseño aprobado, no un error factual.
  El scoring cerrado no se modificó y esas observaciones no se convirtieron en métricas.
- Las restricciones de agentes son instrucciones auditadas; no hay allowlist ni solo lectura
  impuestos técnicamente por worker.
- Los hashes del key y prompt están verificados. La precedencia temporal del key está
  declarada y corroborada por metadata de archivos, pero no enlazada criptográficamente a
  cada corrida; el binding del prompt por corrida también está declarado, no probado por los
  eventos. No se reconstruyó evidencia retrospectiva.
- La conclusión no se generaliza a tareas resolubles enteramente en HEAD, calidad global del
  modelo, producción, dispositivos o backend.

## Decisión derivada

Este benchmark v1 no habilita release candidate. La conclusión sustentada es
**beneficio no probado**. Un plan v2 necesitaría un answer key nuevo, cerrado y firmado antes
de respuestas nuevas; estas respuestas no deben reutilizarse para rescatar métricas.

## Review N2 y cierre

El review independiente inicial emitió `REQUIERE CORRECCIÓN` por cuatro problemas de
trazabilidad. La única ronda dirigida los cerró sin modificar answer key, scoring ciego o
respuestas. Veredicto final: **APROBADO CON NOTAS**; cero findings obligatorios abiertos.
La nota residual sobre wording de precedencia está acotada por los límites probatorios de
este informe y no cambia el resultado.
