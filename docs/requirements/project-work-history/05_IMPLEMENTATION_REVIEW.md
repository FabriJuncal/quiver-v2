# Implementation Review — histórico por proyecto

Fecha: 2026-09-25. Modalidad: self review inline N2; no hubo reviewer
independiente ni delegación. Alcance: `scripts/lib/plan_usage.py`, guía, tests,
H01/H02 y compatibilidad del observador existente.

**Veredicto: APROBADO CON NOTAS; sin findings obligatorios abiertos.**

| Riesgo | Evidencia / resolución |
|---|---|
| Mezcla de proyectos o doble suma | Filtro `project_id`; última revisión persistida por binding; dos revisiones, dos proyectos y trabajo multicategoría probados. |
| Cobertura engañosa | Snapshots ausentes o stale informados; sin snapshot no se imputan tokens. Tiempo wall-clock explícito y activo unknown. |
| USD sintético confundido con gasto | `history` usa solo evidencia directa declarada; tarifa sintética no produce USD histórico. Total unknown ante evidencia incompleta. |
| Privacidad y superficie Kev | Historial lee ledger privado aun si la fuente ya no existe. Sugerencia opt-in solo loopback HTTP, sin persistir resumen ni asignar categoría. |
| Compatibilidad | 46/46 `test_plan_usage.py` PASS, incluyendo 35 regresiones del observador existente; `py_compile` y `git diff --check` PASS. |

El test agregado para proyecto vacío falló inicialmente porque no existía ledger;
el fixture se corrigió creando un ledger válido de otro proyecto. La ejecución
posterior de 46 pruebas pasó. La consulta de un ledger inexistente continúa dando
error explícito, conforme al contrato de almacenamiento privado.

Notas no bloqueantes: la procedencia USD es una declaración con ID y SHA-256,
no verificación externa de factura; la integración con un servidor Kev real no
se probó ni instaló. Las pruebas usan fuentes JSONL y transporte Kev artificiales;
no demuestran una medición en trabajo real.
