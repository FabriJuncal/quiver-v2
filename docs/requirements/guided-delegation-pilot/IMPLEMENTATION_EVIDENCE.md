# Evidencia de implementación offline — P01–P04

Fecha: 2026-09-20; macOS, Python 3.14; distribución v2.2.2 sin cambio de versión.
Autorización: plan v1 y ejecución P01–P04; sin workers reales ni publicación.
EVIDENCE.md conserva evidencia histórica del diseño; este archivo registra implementación.

## Verificaciones ejecutadas

| Comando / verificación | Resultado observado |
|---|---|
| `python3.14 -B -m unittest discover -s tests -v` | 78 tests OK en 19.543 s tras correcciones dirigidas: 34 nuevas + 44 existentes |
| Suite completa inicial | 75 tests OK en 20.056 s; luego se agregaron tres regresiones del review |
| `python3.14 -B -m unittest discover -s tests` repetida con ejemplo de cierre incluido | 78 tests OK en 20.343 s; check-release y ejemplo también PASS en la misma ejecución |
| `bash scripts/check-release.sh` | PASS: sintaxis Bash, archivos, versión 2.2.2, guardrails, mappings y rutas |
| `python3.14 -I -B scripts/lib/check_execution.py --project examples/guided-delegation/project` | STATIC PASS, 1 run sintético; modelo unknown, runtime no verificado |
| `python3.14 -B scripts/lib/check_execution.py --project .` | STATIC PASS, 0 runs; no activa delegación |
| `bash scripts/doctor.sh --project .` | Exit 0, OK WITH WARNINGS; estados válidos, ninguna instalación personal modificada |
| `quick_validate.py` con Python 3, sobre context-scout/model-router/requirement-state/slice-executor | Cuatro resultados Skill is valid; Python 3.14 carecía de PyYAML, se usó Python 3 existente con PyYAML 6.0.3, sin instalar dependencias |
| `git diff --no-index --check` contra snapshot previo | Sin diagnósticos de whitespace; exit 1 por diferencias, no fallo de tests |
| Diff contra snapshot, revisión de criterios y contrato | Self review + una corrección dirigida; GDP-IR-F01–F04 cerrados |
| Validación final de estados con parser real y enlaces Markdown locales | PASS: requirement completed, cuatro slices completed, Active requirement none, próxima acción y enlaces existentes |
| Doctor y check-release tras persistir cierre | Exit 0: OK WITH WARNINGS y PASS respectivamente; sin requirement activo ficticio |

Los tests de instalación, uninstall, init/adopt, perfiles y launcher usan HOME y
directorios temporales (incluidos paths con espacios), con Codex simulado. No se
ejecutó inferencia ni se instaló en HOME real. Los tests nuevos comprueban ausencia
de escrituras del checker y preservación de proyectos legacy. El ejemplo distribuido
se compara byte a byte con el generador de fixtures y se valida read-only.

## Trazabilidad y límites de cobertura

| Criterios | Evidencia automatizada / documental | No demostrado |
|---|---|---|
| AC01 | Legacy sin runs + regresiones; inline default en contrato/skills | Continuidad autónoma real V02 |
| AC02–AC03 | Scope vacío de escritura, opt-in, dependencia/ciclo/ownership; refs y hashes | Sandbox, autoría auténtica o control de despacho real |
| AC04 | Context manifest, paths internos, digest, nombres sensibles rechazados | Detección completa de secretos o prompt injection V09 |
| AC05–AC06 | Entrega/base/scope, stop/aceptación referenciados, validaciones requeridas | Veracidad semántica de evidencia, aplicación de patch viva |
| AC07–AC08 | Unknown/cancel/retry, IDs, transiciones, máximo dos intentos, no_recursion | Exactly-once, cancelación/recursión efectivas del runtime |
| AC09 | Catálogo único, config separada y unknown/evidencia | Modelo/reasoning o precedencia efectivos del worker V19 |
| AC10–AC11 | Recorridos documentales en examples/guided-delegation/WALKTHROUGHS.md | Obediencia UX del modelo V02/V20; controles slash no implementados |
| AC12 | Schema/ejemplo/checker/doctor y 44 regresiones existentes | CI remota y comportamiento vivo, fuera de autorización |

V01 y V03–V18/V21–V23 tienen cobertura estática acorde al escenario; no se declara
que fixtures prueben el comportamiento de agentes descrito por esos escenarios.
V02/V09/V19/V20 incluyen revisión documental explícita. Prueba viva: NOT RUN.

## Diagnóstico preservado

Doctor advierte capa global sin versión vigente, perfiles opcionales no instalados
y metadata de proyecto desconocida en la propia distribución (sin AGENTS/PROFILE/
CAPABILITY_MAP). No se crearon archivos artificiales ni se modificó configuración
personal para silenciarlo. AGENTS global observado: 11.041 bytes; no evidencia de truncamiento.

P01 reconcilió publish-v2.2.1 con consulta read-only `gh release view` y tag local:
release publicada 2026-09-19, commit db1eb677c6b067751fbe66cb013fea0a79ebe688,
assets presentes; detalle en su STATE. No hubo push, tag, release ni repetición de CI.
Checkout local de publicación verificado sin cambios; HEAD conservado en
e8e16cdd12d3d53022d36537601bee1c6d005794.

## AI Execution Record

Perfil recomendado: BALANCED según catálogo. Modelo/reasoning efectivos: unknown;
sin introspección ni cambio afirmado. Self review en misma sesión, sin independencia.
Workers lanzados: 0. Tokens/costo/ahorro: unknown. Rework: corrección del import -I,
ajustes de fixtures y una ronda dirigida de review. No métricas de eficiencia inventadas.

## Recuperabilidad

Snapshot previo en `/tmp/asf-pilot-implementation.X1mfFj/baseline`; recuperar solo hunks
propios tras verificar cambios posteriores. No restauración masiva ni eliminación de
archivos ajenos. Snapshot temporal no sustituye control de versiones duradero.
