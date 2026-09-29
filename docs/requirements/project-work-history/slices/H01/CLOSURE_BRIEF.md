# Closure Brief — H01

- **Estado:** complete, 2026-09-25.
- **Entrega:** `bind` admite marcas opt-in `work_kind`/`work_id`; `history`
  consulta por proyecto y muestra trabajos, categorías, cobertura, seis contadores
  nativos y tiempos explícitos desde la última revisión v2 persistida. Bindings
  anteriores permanecen sin categoría. El mismo trabajo puede dividirse en
  bindings por categoría.
- **Evidencia:** `ProjectWorkHistory` ejercitó dos proyectos, legacy, revisión
  posterior sin doble conteo, trabajo mixto, tiempo conocido/desconocido,
  snapshot desactualizado y consulta CLI con fuente eliminada. Suite afectada
  `python3.14 -I -B tests/test_plan_usage.py`: 46/46 PASS.
- **Límite:** respuestas sin snapshot no se suman; tiempo activo permanece
  unknown y la suma de intervalos paralelos no representa tiempo único.
