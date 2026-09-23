# Technical plan — v1

Una slice S01, sin cambios runtime:

1. AC1–AC3: política canónica en MODEL_CATALOG; model-router y context-scout la aplican sin repetir tablas.
2. AC4–AC5: enlazar aplicación obligatoria y registro mínimo desde contrato, planificación, ejecución, review, templates e instalación/adopción.
3. AC5–AC6: pruebas aisladas de propagación y correspondencia real catálogo/perfiles/argv del launcher; escenarios manuales con entradas/salidas esperadas.
4. AC1–AC6: revisión del diff, evidencia de pruebas y límites; cierre del requirement, preservando la release pendiente.

Validación: unittest de runtime guardrails y scripts; check-release (offline);
git diff --check; escenarios de riesgo, fallo de entorno/contexto, gate ya resuelto,
nueva sesión, herencia obsoleta y registro ausente. No confundir checks estáticos
con evaluación empírica de obediencia de modelos.

Riesgos: burocracia por registro obligatorio y referencias perdidas al instalar.
Mitigaciones: referencia heredada sin duplicación; excepción N0 en evidencia existente;
pruebas de install/init/adopt con HOME temporal y enlaces a rutas de Factory explícitos.
Rollback: revertir este diff aislado; no migraciones ni datos de usuario afectados.
