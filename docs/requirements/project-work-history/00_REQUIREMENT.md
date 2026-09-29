# Histórico de trabajo por proyecto

- **Fuente:** pedido del usuario del 2026-09-25: implementar un histórico de tokens,
  USD y tiempo para nuevas features, bugs, tests, explicaciones y documentación.
- **Alcance confirmado:** trabajos nuevos a partir de esta funcionalidad; no
  importar ni recategorizar sesiones o reportes anteriores.
- **Estado:** alcance y plan v1 aprobados el 2026-09-25; H01/H02 implementadas
  y verificadas con fixtures artificiales.

El histórico debe permitir consultar, por proyecto y tipo de trabajo, valores
observados y faltantes sin presentar tiempo transcurrido como actividad ni un
subtotal sintético como gasto real. Debe preservar S01–S03 de plan-usage-observer
cerradas y no acceder a sesiones reales para construir o probar esta entrega.

La petición autoriza preparar la funcionalidad y su implementación dentro del
alcance acordado. No autoriza importar historial pasado, precios comerciales,
cambios de router/launcher/configuración global, publicación ni commit.
