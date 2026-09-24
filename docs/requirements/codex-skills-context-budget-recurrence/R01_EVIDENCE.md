# R01 — reproducción controlada

Fecha: 2026-09-23.

## Síntoma

El host de la sesión volvió a mostrar:

> Skill descriptions were shortened to fit the skills context budget.

La lista suministrada a esta sesión contiene Skills de múltiples familias
`openai-curated-remote` y varias descripciones aparecen recortadas.

## Reproducción única

Comando ejecutado una sola vez:

```text
codex debug prompt-input 'Respondé solamente: OK.'
```

Resultado observado:

| Métrica | Resultado |
| --- | ---: |
| Exit code | 0 |
| Warning | 0 |
| Skills expuestas | 49 |
| Caracteres de descripción | 10.029 |
| Roots expuestos | 7 |

Los roots de plugin expuestos por esa ruta fueron únicamente
`openai-bundled`, `sites` y `openai-primary-runtime`. No aparecieron Vercel,
Figma, Canva, Stripe, Supabase, Notion ni otras familias
`openai-curated-remote` observadas en el host de esta sesión.

## Comparación antes/después

| Señal | Antes | Después | Delta |
| --- | --- | --- | --- |
| SHA-256 `config.toml` | `a9ade1…3ad0` | `a9ade1…3ad0` | ninguno |
| mtime/ctime `config.toml` | `1790196077` | `1790196077` | ninguno |
| Metadata de plugins | 19 archivos | 19 archivos | ninguno |
| Hash snapshot metadata | `5ebc47…6d98` | `5ebc47…6d98` | ninguno |

Esta ejecución no repitió la desviación de metadata de H01.

## Diagnóstico

### Observado

- La ruta CLI conserva el catálogo histórico de H01: 49 Skills y 10.029
  caracteres, sin warning.
- El host que emitió el warning carga un catálogo sustancialmente mayor con
  familias curated que la ruta CLI omite.
- El inventario fuente de los roots visibles para el host estima hasta 156
  entradas activas y 39.522 caracteres; 118 entradas y 32.134 caracteres
  provienen de plugins. Es una estimación de presión, no una captura exacta del
  prompt efectivo.
- La familia Vercel es el mayor contribuyente disponible: 54 `SKILL.md` y
  aproximadamente 13.067 caracteres de descripción fuente.

### Inferencia

La causa más probable del warning es la expansión del catálogo por el host de
plugins, especialmente las familias curated, y no las 49 Skills que expone
`codex debug prompt-input`. La confianza es alta para la causa de presión de
contexto y media para la identidad exacta del cargador, porque la CLI local no
puede reproducir la ruta del host.

### Limitación

`codex debug prompt-input` no es un canario suficiente para el catálogo del host
actual. La validación de una corrección debe hacerse abriendo una sesión nueva del
mismo host y comprobando warning, conteo y routing visible.
