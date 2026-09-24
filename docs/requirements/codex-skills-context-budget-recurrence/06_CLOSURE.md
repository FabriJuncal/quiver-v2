# Cierre — recurrencia del warning de Skills context budget

Fecha: 2026-09-23.

## Resultado

C01 demostró que `[plugins."vercel@openai-curated"] enabled = false` no controla
la exposición de Skills `vercel:*` en el host. El experimento fue revertido de
forma dirigida y el bloque quedó nuevamente en `enabled = true`.

El warning no apareció en el canario de host, pero el catálogo siguió mostrando
Vercel y descripciones truncadas. La ausencia del aviso no prueba ausencia de
truncamiento.

## Evidencia de rollback

| Verificación | Resultado |
| --- | --- |
| Bloque Vercel | PASS — `enabled = true` |
| Exclusividad del cambio | PASS — volver virtualmente a `false` reconstruye exactamente el hash pre-rollback `42e600…ca95` |
| Hash posterior | `43bc0619…06520` |
| Parser TOML | PASS — `@iarna/toml` 3.0.0 |
| Overrides de Skills | PASS — 31 deshabilitados |
| Modelo/reasoning concurrentes | preservados: `gpt-5.6-sol` / `high` |
| Backup dirigido | PASS — 5/5 entradas del manifest |
| Metadata Vercel | contenido estable: SHA-256 `b17d16…be31` |
| Caché temporal del parser | eliminada |

## Desviaciones

El host actualizó mtime/ctime de
`.codex-remote-plugin-install.json` durante las sesiones nuevas y nuevamente
alrededor del cambio de configuración. El contenido permaneció idéntico. No se
restauró metadata sin una captura de estado gestionada por el host.

## Riesgo residual

No se identificó un control soportado en `config.toml` para el catálogo curated
del host. `codex debug prompt-input` tampoco reproduce esa ruta. Investigar o
cambiar el mecanismo del host requiere un requirement separado y documentación
oficial o capacidad específica del producto.

## Decisión

El requirement se cierra sin deshabilitaciones activas nuevas. No se modificaron
Skills ni archivos de plugin. El backup de C01 se conserva como evidencia.

## AI Execution Record

- Perfil recomendado: ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High.
- Fallback recomendado: GPT-5.6 Terra (`gpt-5.6-terra`) / High.
- Configuración efectiva de la sesión: desconocida.
- Rework: C01 aplicada, canario de host no confirmó exclusión, rollback dirigido
  aprobado y ejecutado; una interrupción de turno se reanudó verificando el
  estado persistente antes de continuar.
- Tokens/costo: información no disponible.
