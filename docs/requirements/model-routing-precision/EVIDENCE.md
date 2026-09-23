# Evidence — 2026-09-23

Validación local macOS, Python 3.14; ejecutor inline. Sin llamadas de inferencia,
agentes adicionales, instalación global real ni cambios a configuración personal.
Los tests de lifecycle usan HOME temporal y Codex simulado.

| Comprobación | Resultado observado |
|---|---|
| `python3.14 -B -m unittest discover -s tests -p 'test_runtime_guardrails.py' -v` | 25 tests OK, 12.278 s. Incluye 3 nuevos de routing. |
| `python3.14 -B -m unittest discover -s tests -p 'test_scripts.py' -v` | 22 tests OK, 7.496 s. Incluye archive/install, adopción preservadora, idempotencia y syntax. |
| `bash scripts/check-release.sh` | exit 0; estructura, versiones, shell, mappings y ausencia de rutas personales. No publica ni certifica runtime. |
| `git diff --check` | exit 0. |

Incidencias de verificación resueltas:
- `python3` local apunta a 3.9 y no tiene tomllib. Se usó Python 3.14 ya instalado;
  el diagnóstico/CI usa >=3.11. No se instalaron dependencias.
- Primera prueba nueva de pares reconoció 3/4 filas: el parser no contemplaba
  `High o XHigh` de Exceptional Override. Corregido parser, no política/modelos.
  Reejecución completa de runtime guardrails: 25/25 OK.

## Escenarios de política

Método: inspección manual de las reglas y sus puntos de entrada, no ejecución de modelos
ni benchmark. Referencias: config/MODEL_CATALOG.md → Selección proporcional y registro
de routing, Switch Threshold, Escalamiento y Review; workflows 04/05/07/08.

| Caso | Resultado de la inspección |
|---|---|
| Transformación uniforme de muchos archivos, prueba exacta, bajo riesgo | Verificabilidad habilita estrategia económica; tamaño no eleva capacidad por sí solo. |
| Cambio pequeño de autorización con tests | Riesgo crítico conserva ADVANCED/review; pruebas no rebajan consecuencias. |
| Falta permiso, dependencia o red | Diagnosticar entorno, no contar como fallo intelectual ni escalar por ello. |
| Logs ausentes/truncados, contrato desactualizado | Recuperar evidencia focalizada antes de aumentar reasoning. |
| Contradicción de producto | Decisión concreta para parte afectada; trabajo independiente autorizado continúa. |
| Contraejemplo con entrada suficiente | Hipótesis/prueba nueva y revisión de capacidad; no repetir análisis sin progreso. |
| Nueva slice con estrategia todavía suficiente | Referencia heredada; no registro duplicado, releer catálogo ni gate repetido. |
| Misma referencia pero cambio material de riesgo/contexto | Reevaluar: la herencia obsoleta no satisface routing-v1. |
| Sesión nueva con modelo efectivo desconocido | Trabajo normal continúa; no heredar confirmación runtime de otra sesión. |
| Gate HIGH ya confirmado en fase/sesión, sin cambio material | No repetir; catálogo y workflow 07 mantienen la confirmación. |
| Registro ausente descubierto después de implementar | Declarar omisión/revisar impacto; no fabricar cumplimiento previo ni aprobación administrativa. |
| Tarea N0 de un turno o consulta sin artefacto | Evidencia existente o excepción de consulta; no requirement nuevo por routing. |
| Migración a otro modelo | Recalcular esfuerzo; no heredar automáticamente nivel alto ni forzar fallos intermedios. |

## Alcance y límites

AC1–AC3: escenarios y diff del catálogo/model-router/context-scout.
AC4: referencias obligatorias en contrato, planificación, ejecución y review;
decisión real del presente requirement en STATE y heredada por S01.
AC5: install/init/adopt probados; skill instalada resuelve catálogo por su ruta real;
pares del catálogo comparados con TOML y argv reales del launcher contra mock.
AC6: catálogo de modelos y flags runtime no cambian; gates y piloto preservados.

La documentación oficial consultada confirma descubrimiento/precedencia de AGENTS al
iniciar la ejecución/sesión, no una garantía de obediencia:
https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance

No se ejecutó regresión completa ni CI remoto: checks dirigidos al alcance aprobado.
No se midió ahorro, calidad de modelos, identidad efectiva ni enforcement técnico.
La instalación canónica y ZIP candidato previo no contienen automáticamente este diff.
