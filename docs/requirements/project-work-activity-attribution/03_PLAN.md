# Plan v2 — histórico automático por actividad con Kev

2026-09-25. **Aprobado; A01–A03 ejecutadas offline y A04/A05 pendientes.** Es la
evolución v2 del histórico, dentro del nuevo requirement
`project-work-activity-attribution`; H01/H02 y S01–S03 conservan su cierre.

## Objetivo y alcance

Una tarea nueva puede contener código de feature, bugfix, tests, documentación y
explicaciones. El usuario no elige una etiqueta global. Quiver registra acciones,
Kev clasifica su propósito y el histórico vincula contadores observados cuando
existe evidencia suficiente. Lectura, planificación, esperas y tareas ambiguas
no desaparecen: quedan visibles como consumo sin atribuir o tiempo no cubierto.

Entrega objetivo: flujo local opt-in de Quiver, historial JSON/texto por tarea y
actividad, procedencia de clasificación, cobertura y revisiones. No incluye UI
web, importación retrospectiva, precios comerciales, entrenamiento de Kev,
servicio remoto, delegación, cambios globales, publicación ni commit.

El usuario aprobó el plan y A01–A03 con fixtures. A04 requiere autorización
separada de un servidor
local concreto o de una instalación aislada; A05 requiere fuente y ventana
prospectiva exactas. Aprobar el plan no amplía esos permisos.

## Base verificada y límites

- `scripts/lib/plan_usage.py`: tokens por `response_id`; ledger privado con lock,
  snapshots v2, historia v1 por binding, costos declarados e integración Kev
  de una sola elección. `bind` v1 exige `work_kind` y `work_id` juntos.
- H01/H02 registraron 46/46 pruebas PASS. Es evidencia previa del alcance v1,
  no una nueva ejecución ni validación del desglose v2.
- No hay productor de actividades ni relación acción→respuesta cualificados
  para esta v2. No se presupone que los hooks del host estén disponibles.
- [API oficial Kev](https://github.com/jaredpalmer/kev#api), consultada
  2026-09-25: preguntas independientes `noul` y `choice`; probabilidades de
  clasificación. Su `usage` pertenece a la consulta Kev y `output_tokens`
  cuenta la respuesta serializada. No son tokens del agente que desarrolla.
  Ejecutarlo localmente requiere entorno/pesos adicionales; no se instalan aquí.

## Contrato propuesto

**Captura.** Un binding nuevo opt-in para historia v2 conserva proyecto, tarea,
sesión y frontera prospectiva, admite `work_id` sin categoría y no reclasifica
bindings v1. Un tramo registra `activity_id`, `operation_id`, identidad de
ejecución, referencias a respuestas, límites observados y resultado
`completed|failed|cancelled|unknown`. La evidencia indica si viene de eventos
del host o recibos emitidos por el ejecutor; una declaración del agente no se
presenta como observación independiente.

El productor se invoca desde el flujo de ejecución local antes/después de las
acciones soportadas. Editores, comandos de tests y respuestas explicativas
necesitan adaptadores explícitos; un watcher de archivos no cubre explicaciones
ni pensamiento. Cambios mediante shell no observado quedan fuera de cobertura.
El recibo proyecta solo rutas relativas afectadas/roles y resultado; no archiva
diffs ni argumentos. El resumen efímero de objetivo/acción tiene máximo 512
caracteres, sin texto sensible; se envía solo a loopback y no al ledger.

**Clasificación.** Indicadores independientes para las cinco categorías,
procedencia `rule|kev_inferred|unknown`, versión de reglas/preguntas/checkpoint
y abstención. El subtipo feature/fix necesita objetivo del cambio además de la
ruta. Reglas claras reconocen documentación/tests; contradicción de señales o
varios positivos produce mixto. Un resumen solo no demuestra qué se ejecutó.
No usar etiquetas del fixture como input al clasificador ni pedir etiquetas
globales al usuario. Sin política Kev validada en A04, sus resultados quedan
marcados no validados y no se aceptan automáticamente en datos reales.

**Tokens.** Relación por IDs nativos verificados, no por cercanía de timestamps.
Unidad contable indivisible: respuesta. Varios eventos de una misma categoría
pueden recibir el contador una sola vez en el agregado de respuesta/categoría;
no se duplica por archivo. Si hay varias categorías, el contador va a mixto; si
falta relación, va a sin atribuir. Cache y reasoning conservan semántica nativa.
La atribución exclusiva exige evidencia de que la lista de acciones de la
respuesta está completa: observar una sola edición no demuestra que haya sido
la única actividad. Sin esa cobertura cerrada, dejar sin atribuir. La
instrumentación incrustada no se resta del consumo de una respuesta por
estimación; solo una respuesta exclusiva identificada permite separar su
sobrecarga nativa. Kev tiene métricas externas separadas.

**Tiempo.** Duración de pared del tramo y duración de herramienta son campos
distintos. Sin límites observados son null. Informar suma de duraciones y unión
de intervalos cuando estos sean compatibles; nunca sumar solapamientos como
tiempo único. Tiempo activo/pensamiento de IA desconocido. Fallo o cancelación
no borra consumo. El tiempo fuera de tramos se muestra como cobertura faltante.

**USD.** Evidencia directa declarada solo al ámbito que cubre: trabajo, respuesta
o actividad. Evitar reutilizar el mismo cargo o sumar el cargo del trabajo más
sus detalles; referencia única y cobertura explícita. No repartir un cargo global
por tokens o duración. Si una actividad no tiene evidencia directa, USD unknown.
No llamarlo factura verificada. Métricas propias de Kev se muestran aparte como
sobrecarga de clasificación; nunca se agregan como tokens nativos del desarrollador.

**Historia.** Nuevo `history_version: 2`, selección explícita en CLI, conservando
salida v1. Guarda revisiones con versión de eventos y clasificación. Reclasificar
crea revisión; no cambia contadores ni duplica trabajo. Mostrar categorías,
mixto, implementación sin subtipo, sin atribuir y sobrecarga, con cobertura y
procedencia. Total de respuestas reconciliado incluso con fuentes incompletas.

## Componentes previstos

- `scripts/lib/plan_usage.py`: binding opt-in, lectura/commit de extensión de
  actividades, CLI, histórico v2 y compatibilidad de snapshots.
- Nuevo `scripts/lib/work_activity.py`: contrato de eventos, proyección privada,
  productor local, clasificación y asignación; biblioteca estándar, sin SDK nuevo.
- Nuevos schemas bajo `templates/usage/`: eventos/clasificación/history v2;
  conservar `MEASUREMENT.schema.json` y su v1 salvo regresión realmente afectada.
- `tests/test_work_activity.py`, fixtures artificiales y regresiones afectadas
  de `tests/test_plan_usage.py`.
- `docs/guides/PLAN_USAGE.md`, protocolo local de captura bajo este requirement,
  estados, briefs, review, cierre y wireframe.

## Slices y dependencias

| Slice | Trabajo y entregable | Condición de salida | Perfil provisional |
|---|---|---|---|
| A01 — captura y contrato | Schema de actividad, modo binding sin etiqueta global, productor de recibos y adaptador de eventos; recorrido automático artificial código→test→docs. Inventario de señales del host con referencias verificables, sin leer sesiones. | T01–T03 PASS; contrato de enlace explícito; capacidad viva declarada NO VERIFICADA hasta A05. Si el único diseño requiere acceso/configuración no autorizados, parar esa parte. | BALANCED / Medium: contrato local verificable. |
| A02 — clasificación automática | Cliente Kev multiactividad con transporte inyectable, reglas, abstención, privacidad y evaluación reproducible. Dataset artificial de desarrollo/evaluación congelado. | T06–T08/T13 PASS con transporte falso. Contrato y fallos probados; precisión Kev todavía NO VERIFICADA. | BALANCED / Medium: parsing y reglas acotadas. |
| A03 — historial y conciliación | Asignación por respuesta, mezclas, tiempos, evidencia USD, revisiones y CLI; integrar productor→clasificador→historial con fixtures. Guía y review del diff. | T04/T05/T09–T13 PASS y regresiones afectadas; listo offline, requisito completo todavía NO. | BALANCED / Medium; review crítico ADVANCED / High. |
| A04 — evaluación Kev real | Tras permiso específico: servidor local con checkpoint/revisión fijados, ejecutar dataset artificial y medir precisión, abstención, cobertura y sobrecarga. No usar datos de proyecto ni entrenar. | T14 PASS con evidencia reproducible; si falla, mantener Kev sin habilitar y presentar resultado. | BALANCED / Medium: evaluación y diagnóstico, no entrenamiento. |
| A05 — piloto del flujo habitual y cierre | Tras permiso específico: conectar productor a señal real disponible del host, iniciar frontera antes de tarea nueva, observar desarrollo/tests/docs sin etiquetas manuales, refresh/snapshot y conciliación. | T15 PASS, review N2, 05_IMPLEMENTATION_REVIEW/06_CLOSURE y estados actualizados. Si no hay enlace nativo, no afirmar atribución exacta ni cerrar automatización completa. | BALANCED / Medium; review crítico ADVANCED / High. |

Orden: A01 → A02 → A03 → A04 → A05. A01–A03 no necesitan instalar Kev ni
leer una sesión real. A05 verifica la vía de integración que A01 solo prepara;
no reabre T13 del observador anterior ni hereda el permiso de su sesión.

## Matriz T2 y oráculos

| ID | Caso discriminante / resultado esperado |
|---|---|
| T01 | Una tarea artificial hace feature, test, docs y explicación; productor emite eventos sin pedir categoría al usuario. |
| T02 | Join por identidad exacta y manifest de acciones completo; una edición visible con otras acciones no observadas, respuesta ajena, evento sin ID, solo timestamps, duplicado y recibo contradictorio: rechazar/abstener, nunca reasignar. |
| T03 | Edición completada/fallida, explicación sin archivos, comando no observado y límites faltantes; origen de evidencia y cobertura correctos. |
| T04 | Una respuesta toca código y docs: tokens solo en mixto. Tres ediciones de docs de una respuesta: se cuenta una vez. |
| T05 | Dos proyectos y dos trabajos de categorías mixtas, legacy sin marcas y opt-in v2 sin `work_kind`: aislamiento y compatibilidad. |
| T06 | Kev falso: positivos múltiples, subtipo ambiguo, falta de objetivo y conflicto con acción observada: mixto o unknown, nunca reparto probabilístico. |
| T07 | Respuesta inválida, NaN, probabilidades fuera de rango, distribución choice inválida, timeout y servicio caído: abstención. Indicadores noul independientes no requieren sumar uno. Sin bloquear la tarea ni persistir texto. |
| T08 | Endpoint externo, redirección, resumen largo/canarios sensibles y rutas fuera de raíz: rechazo; loopback y campos mínimos verificados. |
| T09 | Suma componente a componente de los seis contadores = total observado. Reintento con nuevo ID suma; repetición del mismo ID no; overhead Kev separado. |
| T10 | Inicio/fin, pausa, cancelación, intervalos superpuestos e incompletos; segundos exactos y unknowns, sin atribuir pensamiento. |
| T11 | Cargo global, cargo directo por actividad, evidencia parcial/duplicada y tarifa sintética: USD sin doble suma ni prorrateo. |
| T12 | Historia v1/v2, revisiones de categoría y reportes stale, JSON/texto consistentes; consultar sin fuente disponible y rollback sin pérdida. |
| T13 | Dataset/ledger/salida/error no contienen canarios de prompt, diff, argumentos o secretos; fixtures no abren ninguna sesión real. |
| T14 | Kev real: dataset, checkpoint y política fijados; informe por categoría, mixtos y ambiguos, precisión/cobertura y latencia observadas; umbrales siguientes. |
| T15 | Piloto vivo autorizado: acciones observadas→categorías automáticas→respuestas→histórico, total conciliado, cobertura explícita y fuente limitada al intervalo. |

**T14, condiciones propuestas de aceptación.** Crear 100 ejemplos de desarrollo
y 200 de evaluación separados por familias de tarea: en evaluación, 30 por cada
categoría (150), 25 mixtos y 25 de evidencia insuficiente. Etiquetas/oráculos
provienen del escenario artificial conocido; revisar conflictos antes de congelar
hashes, sin afirmar anotación independiente si no la hubo. Ajustar umbrales solo
con desarrollo; congelarlos antes de correr evaluación una vez por candidato.
Exigir precisión ≥95% entre etiquetas automáticas aceptadas, cobertura ≥60% de
los 150 claros y al menos 10 aceptados por categoría; ≥90% de los 50 mixtos o
insuficientes conservan ese estado. Son criterios de piloto, no garantía estadística
de producción. Registrar matriz de confusión, tamaño de cada denominador y p50/p95
de latencia. Si no alcanza, no mover umbral mirando test ni entrenar por iniciativa
propia: presentar resultado y decisión sobre un nuevo candidato/dataset.

**T15, límite de éxito.** Debe haber al menos una respuesta enlazada por cada
actividad realmente ejercitada, y cero doble conteo. Si toda la tarea cae en
mixto/sin atribuir, el ledger puede conciliar pero el objetivo de desglose no
está demostrado. Preparar una tarea pequeña que naturalmente incluya código,
pruebas y documentación, sin forzar turnos adicionales solo para inflar cobertura.
No exigir que cada pensamiento interno sea separable: ese dato no existe aquí.

## Errores, riesgos, rollback y revisión

Metadatos ausentes no justifican leer conversaciones. El flujo local puede carecer
de hooks o de IDs vinculables: registrar `unsupported_source` y devolver los
contadores al total sin atribuir; un fixture no resuelve esa limitación viva.
Cambio de checkpoint/política invalida la habilitación Kev hasta evaluar de nuevo.
Un fallo de observación no interrumpe el trabajo principal ni pierde ledger.

Escrituras atómicas con las garantías existentes; extensión opt-in, sin migración
destructiva. Desactivar productor/consumo de eventos vuelve al comportamiento
previo; conservar eventos y revisiones. No limpiar worktree ni tocar datos previos.

Revisar A03 y A05 contra criterios, privacidad, conciliación y compatibilidad.
Review inline N2 declarado, sin independencia ni delegación; review crítico
dedicado solo si se autoriza expresamente en otra ejecución. Repetir tests solo
por cambios o findings afectados. No ejecutar gates cerrados por rutina.

## Continuación recomendada

Aprobar criterios v2, D01 y este plan, y autorizar únicamente A01–A03 offline.
Detenerse allí con código probado, evidencia y preparación concreta de A04.
A04/A05 mantienen permisos propios. La AI Strategy está en [STATE](STATE.md);
el modelo efectivo no se deduce del catálogo ni de este documento.
