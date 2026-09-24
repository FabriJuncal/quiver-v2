# C01 — aplicación y canarios

Fecha: 2026-09-23.

## Cambio aplicado

Se modificó únicamente el bloque objetivo intencional:

```toml
[plugins."vercel@openai-curated"]
enabled = false
```

Backup dirigido:

`~/.codex/backups/context-budget-c01-2026-09-23/`

Contiene bloque anterior/posterior, procedimiento de rollback, metadata y una
copia verificable del metadata de instalación de Vercel. No contiene un snapshot
completo de configuración.

## Deriva concurrente preservada

Entre la línea base y la escritura aparecieron dos cambios no pertenecientes a
C01: `model` pasó de `gpt-5.6-terra` a `gpt-5.6-sol` y
`model_reasoning_effort` de `medium` a `high`. Son coherentes con un cambio de
modelo de la sesión. No se restauraron ni editaron.

Por esa deriva, el hash completo anterior no puede reconstruirse cambiando solo
la línea de Vercel. El bloque dirigido sí coincide con el candidato aprobado.

## Canarios locales

| Canario | Resultado |
| --- | --- |
| Parser TOML estándar | PASS — `@iarna/toml` 3.0.0 |
| Vercel deshabilitado | PASS — `enabled = false` |
| Overrides de Skills | PASS — 31 deshabilitados, sin cambio |
| Catálogo CLI | PASS — 49 entradas |
| Skills core | PASS — debugging, requirements, API y CI presentes |
| Vercel en catálogo CLI | 0 entradas |
| Warning en catálogo CLI | 0 |
| Metadata Vercel | PASS — hash y mtime/ctime sin cambios |
| Metadata plugins agregada | PASS — snapshot `5ebc47…6d98` sin cambios |
| Caché temporal del parser | eliminada |

## Canario de host pendiente

La sesión actual no recarga Skills después de cambiar `config.toml` y la ruta
`codex debug prompt-input` no carga las familias curated del host. La prueba
concluyente requiere una conversación nueva en el mismo host. No debe ejecutarse
otra modificación antes de observar ese resultado.

## Resultado posterior del host

El usuario ejecutó el canario en una conversación nueva: el warning no apareció,
las cuatro Skills core estuvieron disponibles y Vercel continuó presente. En el
catálogo suministrado a esta sesión todavía se observan descripciones cortadas.
C01 no controla la carga curated del host; ver `HOST_CANARY.md`. La ausencia del
warning no se atribuye a C01 ni demuestra que el truncamiento haya cesado.
