# Handoff — observador de uso por plan

Fecha: 2026-09-25. Continuidad sin historial del chat. Fuente canónica:
[STATE.md](STATE.md), indexada por [PROJECT_STATE.md](../../../PROJECT_STATE.md).
Este resumen y su wireframe son vistas derivadas, no estados paralelos.

## Objetivo, alcance y estado

Medición atribuible a un plan antes de predecir consumo. S01 implementó tokens
atribuibles; S02 agregó lifecycle explícito, límites temporales, reporte v2/revisiones
y costos con tarifas sintéticas. Ambas quedaron cerradas offline. No cambió launcher,
modelo, permisos ni dependencias. Predictor, panel y presupuesto restrictivo permanecen
fuera del requirement actual. S03 tiene fuente/frontera autorizadas y T13
reconciliado; plan v1 cerrado con notas.

| Entregable / aprobación | Estado |
|---|---|
| Auditoría y documentos | Elaborados |
| Criterios v1 / D01 / T2 reforzado / plan v1 | Aprobados explícitamente por el usuario el 2026-09-24; versiones en STATE |
| Plan review | APROBADO CON NOTAS; self review, sin independencia |
| Implementación S01 | COMPLETADA offline; gate 04 PASS, review APROBADO CON NOTAS |
| Implementación S02 | COMPLETADA offline; review APROBADO CON NOTAS |
| Implementación S03 | CERRADA CON NOTAS; T13 real reconciliado, review inline aprobado con notas |
| Tests S02 | 13 T2 + 6 regresiones S01 afectadas; PASS |
| Integración real / precios comerciales | Intervalo/fuente autorizados verificados; precios comerciales fuera de alcance |

## Baseline y propiedad de cambios

Rama `docs/archive-closed-requirements-2026-09-24`, HEAD
`2b92c74602bf244e9a3e03829e5c07f2b233e8a4`. No cambio de rama ni sync remoto.
PROJECT_STATE.md ya tenía una actualización sin commit del merge documental previo.
Esta sesión conserva ese archivo histórico, cambia su cabecera operativa y agrega
el enlace al requirement nuevo. No atribuir todo su diff a esta sesión.
72 untracked previos: 24 discovery + 48 optimización de Skills, preservados.
Digest inicial/procedimiento en [AUDIT §1](AUDIT.md#1-baseline-y-alcance).

Archivos del requirement, incluyendo la implementación S01:

- `docs/requirements/plan-usage-observer/00_REQUIREMENT.md`
- `docs/requirements/plan-usage-observer/AUDIT.md`
- `docs/requirements/plan-usage-observer/01_ACCEPTANCE_CRITERIA.md`
- `docs/requirements/plan-usage-observer/02_DECISION.md`
- `docs/requirements/plan-usage-observer/03_PLAN.md` (no PLAN.md duplicado)
- `docs/requirements/plan-usage-observer/04_PLAN_REVIEW.md`
- `docs/requirements/plan-usage-observer/05_IMPLEMENTATION_REVIEW.md`
- `docs/requirements/plan-usage-observer/06_CLOSURE.md`
- `docs/requirements/plan-usage-observer/STATE.md`
- `docs/requirements/plan-usage-observer/HANDOFF.md`
- `docs/requirements/plan-usage-observer/slices/S01/SPEC.md`
- `docs/requirements/plan-usage-observer/slices/S01/EXECUTION_BRIEF.md`
- `docs/requirements/plan-usage-observer/slices/S01/CLOSURE_BRIEF.md`
- `docs/requirements/plan-usage-observer/slices/S02/SPEC.md`
- `docs/requirements/plan-usage-observer/slices/S02/EXECUTION_BRIEF.md`
- `docs/requirements/plan-usage-observer/slices/S02/CLOSURE_BRIEF.md`
- `docs/requirements/plan-usage-observer/slices/S03/SPEC.md`
- `docs/requirements/plan-usage-observer/slices/S03/EXECUTION_BRIEF.md`
- `docs/requirements/plan-usage-observer/slices/S03/CLOSURE_BRIEF.md`
- `scripts/lib/plan_usage.py`
- `tests/test_plan_usage.py`
- `templates/usage/MEASUREMENT.schema.json`
- `templates/usage/MEASUREMENT.v1.schema.json`
- `docs/guides/PLAN_USAGE.md`
- `FILE_INDEX.md`
- `PROJECT_STATE.md` (modificación adicional acotada).

## Orden mínimo para continuar

1. PROJECT_STATE.md → STATE.md de este requirement → este HANDOFF.
2. Para auditar S03: 03_PLAN.md, brief/cierre S03, 05_IMPLEMENTATION_REVIEW.md y
   06_CLOSURE.md; no reabrir el binding ni repetir gates sin nueva autorización.
3. AUDIT solo para discrepancias del contrato o procedencia.
4. Política cuando sea material o haya cambiado: workflow/00_SHARED_CONTRACT.md,
   workflow/05_PLAN_REVIEW.md, workflow/06_CREATE_SLICES.md, workflow/10_RESUME.md;
   config/MODEL_CATALOG.md y skills/core/model-router/SKILL.md.

Ya inspeccionados prioritariamente: FILE_INDEX, README, FACTORY_VERSION,
SOURCE_OF_TRUTH, RISK_AND_WORKFLOW, templates de requirement/slice, scripts/asf.sh,
context_economy.py, check_execution.py, runtime_doctor.py, RUN.schema.json,
tests/test_context_economy.py y delegation_fixture.py; guías ASF_LAUNCHER,
SESSION_PREFLIGHT, GUIDED_DELEGATION y CONTEXT_ECONOMY_TEXT_HELPER.
Fuentes externas fijadas por commit en AUDIT; no repetir búsqueda de herramientas.

Si cambia HEAD, instrucciones, código pertinente, versión del plan o estado:
reconciliar únicamente ese delta antes de actuar. No reiniciar auditoría completa
ni aprobar una propuesta cambiada por mencionar una versión anterior.

## Decisiones y límites que deben conservarse

- Criterios v1, D01, T2 reforzado, plan v1 y ejecución S01/S02 fueron aprobados por el
  usuario el 2026-09-24. S03 fue autorizada el 2026-09-25 para una fuente/frontera
  exactas. S01/S02 siguen cerradas.
- Quiver inicia/orienta Codex; las primitivas de consumo existentes son offline.
  Fin del proceso, fin del turno y aceptación del plan no equivalen.
- CLI instalado declara 0.156.1; contrato público por respuesta inspeccionado.
  Host real de la experiencia del usuario aún no probado; no leer logs generales.
- Binding previo, no última sesión/cwd/tiempos próximos; primera versión raíz inline,
  formato plano cualificado, sin forks/subagentes. Modelo/pago efectivos unknown.
- USD puede seguir unknown aun con tokens verificables; no inventar tarifas/facturas.
- Ledger JSON privado: uso/checkpoint en un commit y lock local. SQLite diferido.
- S01 fue autorizada y completada el 2026-09-24 después de cualificar una fuente
  mediante `S01-GATE-04`. El gate no importó historial. S03 conserva el recorrido
  real prospectivo completo. No cambiar a App Server/exec sin nueva decisión.
- S02 fue autorizada y completada el 2026-09-24 con fixtures artificiales. Reporte v2,
  revisiones y snapshots `synthetic` no prueban precios, modalidad ni uso real.
- `S03-SOURCE-01` es la única fuente permitida. El ledger privado y checkpoint se
  referencian en STATE; no copiar ruta/IDs de runtime al repositorio. Un modo S03
  explícito admite turnos raíz posteriores del mismo thread y excluye el turno de
  binding; thread distinto sigue fuera. T13 terminó; no repetir refresh.
- No tocar piloto/evidencia privada, benchmarks cerrados, codex-skills-optimization,
  configuración global, router, launcher ni otros cambios. No staging ni publicación.

## Comprobaciones

| Control | Resultado / límite |
|---|---|
| CE-v1 | `python3 -I -B tests/test_context_economy.py`: 19 OK; mismos 19 OK con python3.14; transporte falso y temporales |
| Launcher | `bash scripts/asf balanced --dry-run`: exit 0; no sesión ni disponibilidad probada |
| Externo | Lectura primaria con commits fijados; ningún paquete instalado/test upstream ejecutado |
| Git previo | Rama/HEAD/diff/72 untracked registrados, sin limpieza |
| Estado canónico | Doctor.state en ambos archivos: 0 errores con Python 3.14.4; primer intento con Python 3.9.6 falló por tomllib |
| Enlaces / whitespace | Enlaces relativos del requirement revisados; sin whitespace final; git diff --check PASS |
| Preservación | Mismo digest de los 72 archivos previos; tramo histórico de PROJECT_STATE idéntico al baseline |
| Alcance / privacidad | Implementación S01 y documentación listadas en este handoff. Lectura real limitada a estructura/versiones/contadores de una fuente autorizada; revisión dirigida, no garantía exhaustiva |
| Gate S01-GATE-01 | Fuente privada autorizada: regular/no symlink; SHA-256 estable; CLI 0.149.0; 1.006 líneas, 8 inválidas; 137 `token_count` agregados; cero `token_usage_record` e IDs por respuesta. INCOMPATIBLE |
| Selección S01-CANDIDATE-02 | 84 JSONL por nombre/stat/versión; seis aparentes `>=0.156.1`; uno seleccionado, CLI 0.156.1, sin contadores ni contenido leídos |
| Gate S01-GATE-02 | Versión, registros e IDs esperados observados; tamaño/mtime cambiaron desde la selección. NO ACEPTADO; sin importación ni código |
| Selección S01-CANDIDATE-03 | 84 JSONL por nombre/versión/dos `stat`; seis aparentes `>=0.156.1`, cinco estables; un alias propuesto, CLI 0.156.1, sin contadores ni contenido leídos |
| Gate S01-GATE-03 | Primer `stat`: 24.469.346 bytes frente a baseline 22.548.201. Detenido antes de formato/contadores/IDs; sin código |
| Gate S01-GATE-04 | Prefijo 24.888.278 bytes estable; CLI 0.156.1; 403 registros por respuesta; cero errores de forma. PASS |
| S01 focalizada | `python3.14 -I -B tests/test_plan_usage.py -v`: 20/20 OK; fixtures sintéticas |
| Regresiones | CE-v1 19/19; suite global 173/173; `check-release.sh` PASS |
| Review S01 | Inline, una ronda dirigida; F01–F04 cerrados; APROBADO CON NOTAS |
| S02 focalizada | Clase `PlanUsageS02`: 13/13 OK; T04–T07, T11/T12 artificiales |
| Regresión S01 afectada | Seis casos dirigidos: 6/6 OK; no se repitieron gates ni suites ajenas |
| Review S02 | Inline, una ronda dirigida; F05–F07 cerrados; APROBADO CON NOTAS |
| Estáticos S02 | Compilación Python, dos esquemas JSON y `git diff --check`: PASS |
| S03 preparación | Fuente única CLI 0.156.1, binding previo, checkpoint privado y 0 importados; cuatro pruebas dirigidas PASS |
| S03 T13 | Seis respuestas y 254927 tokens idénticos fuente/ledger; siete del turno binding omitidas, cero duplicados/excluidos, identidad y prefijo preservados |
| Suite offline S03 | `python3.14 -I -B tests/test_plan_usage.py`: 35/35 PASS |
| Review S03 | Inline N2, APROBADO CON NOTAS; F08/F09 opcionales, cero obligatorios |

No se ejecutó CI remoto ni benchmark. El recorrido real fue acotado a la fuente
autorizada; incluye aclaración y tarea, por lo que no aísla consumo de la tarea.
Usar `python3.14` disponible para ese comprobador: `python3` por defecto es 3.9.6
y carece de tomllib. No instalar otro intérprete ni modificar configuración global.

Invocación diagnóstica ad hoc **ejecutada**, reutilizando el comprobador existente
(no es una nueva CLI ni un archivo de script):

```bash
python3.14 -I -B -c 'import sys; from pathlib import Path; sys.path.insert(0, str(Path("scripts/lib").resolve())); from runtime_doctor import Doctor; d=Doctor(); d.state(Path("PROJECT_STATE.md")); d.state(Path("docs/requirements/plan-usage-observer/STATE.md")); print("State errors:", d.errors); raise SystemExit(bool(d.errors))'
```

## Acción inmediatamente siguiente

**Esperar un nuevo requirement del usuario.** S01–S03 están cerradas. El binding
S03 no debe refrescarse nuevamente ni ampliarse a otras fuentes sin autorización.

No hace falta nueva sesión para una actualización mecánica breve. Si se abre otra,
leer estos documentos, comprobar delta del baseline y no heredar identidad de modelo.

## Modelo recomendado para la próxima acción

| Campo | Recomendación |
|---|---|
| Fase | Nuevo requirement aún no definido; reevaluar al recibirlo |
| Perfil | No seleccionado para trabajo futuro |
| Modelo | No seleccionado para trabajo futuro |
| Motivo | La recomendación ADVANCED/GPT-5.6 Sol fue de S03 y no se hereda automáticamente |
| Switch Benefit | Sin evaluar para un nuevo pedido |
| Fallback | No seleccionado para trabajo futuro |
| Fuente | config/MODEL_CATALOG.md y STATE del nuevo requirement, cuando exista |
| Configuración efectiva | NO VERIFICADA |
| Disponibilidad | Pendiente en selector del runtime del usuario |

## Razonamiento recomendado para la próxima acción

| Campo | Recomendación |
|---|---|
| Nivel | Pendiente de evaluar para un nuevo pedido |
| Motivo | No hay fase activa que justifique una selección nueva |
| Escalado/reducción | Según riesgo y Switch Benefit del nuevo trabajo |
| Fallback | Pendiente de evaluar |
| Fuente | config/MODEL_CATALOG.md y STATE del nuevo requirement |
| Configuración efectiva | NO VERIFICADA |

## Wireframe — vista derivada de STATE

```text
┌────────────────────────────────────────────────────────────────────┐
│           QUIVER V2 · MEDICIÓN POR PLAN                            │
├────────────────────────────────────────────────────────────────────┤
│ AUDITORÍA                                                          │
│  ████████████  DOCUMENTADA                                         │
│  ● Flujo local y primitivas revisados; 19 tests offline OK         │
│  ● Contrato nativo cualificado por gate 04                         │
├────────────────────────────────────────────────────────────────────┤
│ PLAN Y HANDOFF                                                     │
│  ████████████  ELABORADOS · PLAN APROBADO                          │
│  ● Tres slices, criterios y pruebas; self review con notas         │
│  ● Plan v1 aprobado y ejecutado por slices                         │
│  ● S01/S02 offline; S03 real acotada                                │
├────────────────────────────────────────────────────────────────────┤
│ PRIMERA ENTREGA                                                    │
│  ● S01  Tokens atribuibles offline; cierre preservado              │
│  ● S02  Lifecycle/costo sintético; 13 T2 + 6 regresiones OK        │
│  ● S03  T13: 6 respuestas / 254927 tokens; cierre con notas        │
├────────────────────────────────────────────────────────────────────┤
│ DESPUÉS · FUERA DE ESTA ENTREGA       ◀ ESTAMOS ACÁ               │
│  ○ Estimación previa y comparación con resultados                  │
│  ○ Evaluación temporal y calibración                               │
│  ○ Presupuestos, routing o paneles solo si se justifican           │
├────────────────────────────────────────────────────────────────────┤
│ LÍMITES                                                            │
│  ! Intervalo cerrado; incluye aclaración y tarea                   │
│  · USD desconocido si faltan identidad o tarifa verificables       │
│  · Sin cambios de configuración, dependencias ni publicación       │
└────────────────────────────────────────────────────────────────────┘
```

## Formato de continuidad

Al finalizar: resultado/evidencia, estado y archivos, wireframe derivado con un solo
marcador, una siguiente acción, modelo y razonamiento en apartados separados según
router, mensaje único resuelto en cita Markdown idéntico al persistido, sin datos
de configuración dentro de la cita. No recomendar implementación cuando solo
corresponda registrar una aprobación.

## Mensaje exacto para continuar

> Quiero iniciar un nuevo requirement de Quiver: [objetivo y alcance]. Conservá
> plan-usage-observer S01–S03 cerrado; no reabras su binding ni amplíes la fuente.
