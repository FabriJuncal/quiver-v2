# Candidato reversible — reducción de presión del host

## Cambio mínimo recomendado: C01

Deshabilitar temporalmente solo el plugin Vercel configurado actualmente:

```toml
[plugins."vercel@openai-curated"]
enabled = false
```

Motivo: es la familia de mayor volumen observada, con 54 Skills fuente y cerca de
13.067 caracteres de descripción. Una sola desactivación ofrece la mayor
reducción esperada con rollback directo.

## Aplicación propuesta

1. Capturar backup dirigido de `config.toml` y metadata del plugin.
2. Cambiar únicamente `enabled = true` a `enabled = false` para Vercel.
3. Abrir una sesión nueva en el mismo host que mostró el warning.
4. Verificar ausencia o persistencia del warning y catálogo visible.
5. Ejecutar canarios positivos para Skills core y negativos para Vercel.

## Rollback

Restaurar exclusivamente:

```toml
[plugins."vercel@openai-curated"]
enabled = true
```

## Gate original

C01 no fue aplicada. Requiere aprobación específica porque modifica
`~/.codex/config.toml` y deshabilita temporalmente un plugin instalado.

Si C01 no elimina el warning, no se propone deshabilitar familias adicionales en
serie sin una nueva medición del host. Figma, Canva y Product Design serían los
siguientes contribuyentes a estudiar, pero sus mecanismos efectivos de enable/
disable no quedaron verificados en esta reproducción.

## Resultado

C01 fue aprobada y aplicada, pero el canario del host mostró que las Skills
`vercel:*` continúan visibles. El mecanismo propuesto no controla el catálogo del
host. No se autoriza extender el mismo patrón a otras familias.

## Gate de rollback

Se recomienda restaurar únicamente `enabled = true` para
`vercel@openai-curated`, usando el backup dirigido de C01. El rollback requiere
aprobación humana porque vuelve a modificar `~/.codex/config.toml`.

## Resultado del rollback

El rollback fue aprobado y ejecutado. Vercel quedó nuevamente en `enabled = true`;
TOML, 31 overrides y manifest del backup validaron. Ver `06_CLOSURE.md`.
