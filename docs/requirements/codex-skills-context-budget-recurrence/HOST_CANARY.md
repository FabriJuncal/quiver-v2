# Canario de host post-C01

Fecha informada: 2026-09-23. Fuente: ejecución en una conversación nueva del
mismo host, reportada por el usuario.

## Resultado observado

| Verificación | Resultado |
| --- | --- |
| Warning de descripciones truncadas | No apareció |
| Descripciones efectivamente completas | FAIL — el catálogo suministrado a esta sesión aún contiene descripciones cortadas |
| Vercel ausente de Skills | FAIL — continuaron visibles múltiples Skills `vercel:*` |
| `systematic-debugging` | Disponible |
| `requirements-planning` | Disponible |
| `api-contracts` | Disponible |
| `ci-diagnostics` | Disponible |
| Archivos o configuración modificados por el canario | Ninguno, según el reporte |

## Diagnóstico reconciliado

### Hechos

- C01 dejó `[plugins."vercel@openai-curated"] enabled = false` en
  `~/.codex/config.toml`.
- Una sesión nueva del host continuó exponiendo Skills `vercel:*`.
- El warning no apareció, pero varias descripciones suministradas a esta sesión
  siguen cortadas; las cuatro Skills core permanecieron disponibles.

### Inferencia

El override de `config.toml` probado por C01 no gobierna la inyección de Skills
Vercel del host actual. Por lo tanto, la ausencia del warning no demuestra que
C01 redujera el catálogo ni que resolviera la causa. Además, la presencia del
warning no es un indicador confiable del truncamiento: este puede ocurrir sin que
el aviso sea visible. El comportamiento depende de una ruta del host no controlada
por la configuración probada.

### Siguiente acción mínima

Revertir el override experimental de C01 a `enabled = true`, porque no produjo el
efecto medible buscado y mantenerlo podría afectar otras rutas de Codex sin reducir
el catálogo del host. No deshabilitar otras familias hasta identificar el control
real del host o disponer de una medición soportada.
