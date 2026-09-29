# Plan técnico v1 — observador de uso por plan

**PLAN v1 APROBADO por el usuario el 2026-09-24.** Aprobación registrada en
[STATE](STATE.md); autorización de ejecución permanece separada y pendiente.
Self review en [04_PLAN_REVIEW](04_PLAN_REVIEW.md). Alcance y criterios
en [00_REQUIREMENT](00_REQUIREMENT.md) y [01_ACCEPTANCE_CRITERIA](01_ACCEPTANCE_CRITERIA.md).
Decisión propuesta: [D01](02_DECISION.md). Evidencia: [AUDIT](AUDIT.md).

## Objetivo y no objetivos

Entregar un registro reproducible de uso atribuible a un plan hasta aceptación,
con faltantes visibles. No predictor, router, gastos máximos, GUI, cobros, servicios,
importación global, benchmark ni nueva forma obligatoria de ejecutar Codex.
La auditoría ya comprobó 19 tests offline existentes; **ningún slice siguiente está
implementado**. No rehacer esas primitivas ni activar el ayudante API para medirlas.

## Recorrido e integración mínima propuesta

```text
STATE/plan aprobado → opt-in y binding previo de fuente/intento
  → lectura selectiva bajo demanda → normalización por versión
  → transacción local (eventos + checkpoint + binding)
  → JSON privado / resumen textual → cierre provisional / actualización
  → aceptación humana del trabajo, registrada por separado
```

No se modifica scripts/asf.sh. Las convenciones opt-in/inline de Quiver y los briefs
dan el punto de entrada: acción explícita de preparar medición antes de una ejecución
autorizada; consulta al pausar/reanudar/cerrar. No background prometido ni hook
supuesto. Si se desea automatizar después, exigir evidencia y alcance separado.
El lector no envía contenido al modelo ni requiere otro agente.

El uso del comando que realiza el refresh puede aún no haberse emitido al leerlo:
la vista queda provisional. La lectura final debe ocurrir después de terminar los
turnos incluidos, desde una operación local sin inferencia. Si no se hace, conservar
el faltante final; no declarar total definitivo de la misma respuesta que lo consulta.

Puntos existentes: context_economy.py (normalize_usage, patrones de escritura),
templates/slice/EXECUTION_BRIEF.md y CLOSURE_BRIEF.md, workflows/07 y 09 para consumo
de evidencia, guided_status para formato. No cambiar sus reglas de aprobación.
Nuevas rutas **propuestas, no existentes**: `scripts/lib/plan_usage.py`,
`templates/usage/MEASUREMENT.schema.json`, `tests/test_plan_usage.py`,
`docs/guides/PLAN_USAGE.md`. Se evita editar RUN.schema.json: es delegación, no ledger inline.
Los briefs reales de las slices se crearán según workflow/06 solo tras autorizar la ejecución.

## Contratos de datos propuestos

### Identidad y frontera

- Reusar requirement_ref, plan_version, slice_id y attempt_id donde existan; referencia
  y SHA-256 de 03_PLAN.md identifican la revisión exacta. No confundir commit con
  revisión de plan. Cambio material de plan abre otra revisión, no reasigna pasado.
- Si el flujo inline no tiene IDs, crear project_id, execution_id e attempt_id locales
  estables en el registro de medición; no atribuirlos al runtime. Identidad de proyecto
  liga raíz validada una vez, sin publicar rutas personales; un traslado exige rebind.
- Binding durable **antes** de contar: project/requirement/plan-digest/attempt + ruta
  privada explícita + session/thread verificables + frontera lógica y física.
  Capturar cursor/baseline inicial en reposo entre turnos. Historial previo es baseline,
  nunca consumo del plan. Si un turno cruza la frontera queda no atribuido.
- Primera versión requiere sesión raíz dedicada a ese plan durante el intervalo;
  no repartir automáticamente un turno entre planes. Reanudar misma sesión conserva
  binding; nueva sesión requiere binding nuevo del mismo intento o intento nuevo
  explícito. Preparación previa no observable se informa fuera de captura.
- Implementación, validaciones y correcciones se incluyen mientras el intento siga
  vinculado; categoría preparación/ejecución/review solo si hay marcadores explícitos.
  Varias sesiones/planes concurrentes requieren bindings disjuntos bajo el mismo ledger.
- session_id/thread_id/turn_id/response_id/root_turn_id/agente conservados solo cuando
  provienen de la fuente. No generar request_id a partir de turn_id ni inventar granularidad.

### Fuente y normalización

- Adaptador versionado de JSONL plano, inicialmente cualificado contra E-N1–N4
  de AUDIT. El package instalado orienta la investigación, no acredita el host real.
- Fuente contable: `token_usage_record.usage` de respuesta. Clave única en el almacén:
  proveedor/fuente + session/thread + response_id; validar turn/root-turn coherentes.
  Mismo ID/contenido: ignorar duplicado; mismo ID/valores diferentes: conflicto,
  no sobrescribir ni sumar. Fuente física duplicada no crea otra solicitud.
- Conservar original **solo de contadores/identificadores permitidos** y versión,
  ordinal/offset cuando existan, fecha observada y digest del registro permitido.
  No guardar el objeto completo, prompts, respuestas, tool args ni línea sensible.
- input incluye cached-input cuando así lo garantiza la versión cualificada;
  output incluye reasoning. Total=input+output, no sumar subconjuntos de nuevo.
  cache-write se conserva aparte; no forzar semántica de otro proveedor. Si es no
  cero y su pertenencia/tarifa no está cualificada, costos desconocidos y anomalía.
- `turn_token_usage`, `thread_token_usage` y `token_count` son contraste, no otra suma.
  Acumulados se comparan dentro de una época/binding y frontera válida. Disminuciones,
  compactación/revert, reinicios o discrepancias no generan deltas negativos ni
  consumo inventado; abrir anomalía/reconciliación. Registro legacy sin identidad:
  no soportado como fuente principal. No fallback por proximidad temporal.
- Orden físico gobierna cursor; timestamps no únicos no deduplican. Reimportación
  y orden de respuesta diferente se resuelven por ID. Si el contexto de modelo/tier
  es ambiguo, no asignarlo por vecino más cercano: unknown hasta evidencia enlazada.
- Errores/retries/cancelación conservan toda respuesta con uso atribuible, aunque el
  trabajo no sea aceptado. Falta de usage no significa cero. No estimar requests
  ausentes ni porcentaje de cobertura sin denominador observable.
- Forks, descendientes o root_turn ajeno: no leer otros logs por iniciativa propia;
  excluir de suma, informar alcance incompleto. Hijo con historia heredada no es
  otra copia sumable del padre. No prometer soporte de multiagente en v1.

### Persistencia y concurrencia

- Almacén privado elegido explícitamente, fuera de worktrees y Git; un JSON versionado
  contiene bindings, registros normalizados, anomalías, checkpoints, tarifas y revisiones
  de reportes. Nunca escribir al log fuente, estado interno de Codex ni originales.
- Adaptar patrón local `_exclusive_json`/`_replace_json`: tempfile hermano 0600,
  flush/fsync archivo, replace atómico, fsync directorio. Lock de escritor independiente
  sobre archivo estable, con exclusión del SO (fcntl en macOS/Linux), tomado antes de
  leer snapshot y hasta commit. No lock por PID borrable a ciegas.
- Checkpoint y eventos en **el mismo commit atómico**, no dos archivos coordinados.
  Fallo antes de replace: estado anterior; después: snapshot nuevo o relectura para
  reconciliar outcome incierto. Dedup por ID evita doble suma al repetir. No confirmar
  éxito si fsync falla; advertir y conservar evidencia. Archivo corrupto no se resetea.
- Lectura incremental solo de líneas completas hasta tamaño capturado. Línea parcial
  queda pendiente sin avanzar más allá; formato inválido genera anomalía acotada,
  no persistir contenido sensible. Truncado/cambio de identidad/prefijo requiere
  detener importación de esa fuente; nunca borrar checkpoint y recontar todo.
- Identidad del archivo/cursor y hash de prefijo para detectar reescritura, con lectura
  acotada. Límites documentados de bytes/registros por importación y ledger; excederlos
  produce incompleto, no truncamiento silencioso. Definir constantes en la SPEC S01,
  no prometer volumen ilimitado ni inventar capacidad medida ahora.
- Solo FS local cualificado; locks NFS/Windows no soportados sin validación. Un almacén
  coordina varios planes; no garantía entre almacenes copiados/hosts distintos.
- Fallo de medición advierte sin cortar la tarea del usuario ni falsear un total. El
  comando puede devolver error propio; no debe encadenarse como gate del trabajo.

### Tiempo, USD y reportes

- Inicio, pause, resume, close explícitos por intento; sin reloj de trabajo inferido
  desde silencios. elapsed=fin−inicio, tiempo en intervalos habilitados etiquetado
  como tal, no tiempo activo. UTC + monotónico cuando comparten proceso; cambios de
  reloj/cross-process se señalan. Tiempo activo, espera humana y tiempo-agente unknown
  salvo fuente con límites suficientes. Paralelismo: unión de intervalos, no suma
  como elapsed. No tokens/segundo ni tiempo de este CLI como duración del plan.
- Separar modelo solicitado, alias registrado, modelo efectivo probado, proveedor,
  tier y naturaleza de pago. Ni perfil ni nombre en turn_context prueban por sí solos
  backend facturado. En v1 no hay resolución automática de aliases ni fallback tarifario.
- Snapshot de tarifa: moneda USD, proveedor, modelo exacto y tier (o evidencia explícita
  de independencia del tier), vigencia, fuente primaria, fecha de consulta, revisión y
  hash. Entradas Decimal desde texto, nunca float; calcular categorías disjuntas por
  respuesta sin redondeo monetario prematuro, sumar y formatear al final.
- Con datos válidos, costo API calculado; suscripción solo equivalente API claramente
  etiquetado si hay identidad y tarifa verificables. Modalidad unknown no se convierte
  en suscripción/API. Cargos de tools/servicios solo si se observan y no se duplican;
  facturado/conciliado permanece desconocido sin evidencia externa autorizada.
- Faltan uso/modelo/precio/tier aplicable: USD desconocido, subtotal conocido separado
  y total incompleto. No elegir precio de otro modelo. Historial guarda snapshot y
  resultado originales; revaloración explícita crea versión nueva, no reemplaza pasada.
  Tests usan exclusivamente tarifas sintéticas marcadas, nunca comerciales inventadas.
- Reportes versionados JSON privados y texto legible: identidad/revisión/intento/slice,
  aceptación independiente, fuente/versiones, tokens por categoría/modelo conocido,
  costos por naturaleza, tiempos observados, fallbacks (ninguno automático), faltantes
  y anomalías. Estado de datos: provisional / incompleto / sin faltantes detectados
  dentro de las fuentes soportadas; última etiqueta no promete factura completa.
- Falta cierre/evento final: provisional o incompleto según causa. Evento tardío:
  conservar reporte anterior, producir revisión con diferencia/procedencia. No alterar
  aceptación por una actualización contable. Exportación a Git solo resumen sanitizado
  aprobado por separado; nunca log privado ni ruta personal.

## Slices propuestos y dependencias

IDs S01–S03 locales a este requirement; no renumeran otros requirements. No se crean
todavía carpetas SPEC/BRIEF: workflow/06 exige plan aprobado. Sin estimación
cuantitativa validada; orden por dependencia y capacidad de refutar la solución.

### S01 — Recorrido vertical de tokens atribuibles

- **Objetivo:** de binding previo a reporte JSON/texto reproducible usando fixture nativa.
- **Entrada:** criterios/D01/T2/plan aprobados y autorización separada de S01; reconciliar
  baseline; Python/FS compatible. Para la comprobación inicial, permiso de lectura
  de metadatos/contadores de una fuente existente explícita del host habitual,
  sin importar consumo pasado ni generar muestras. No autorización implícita de logs.
- **Gate temprano antes de implementar:** comprobar identidad del host, versión,
  formato y presencia de los campos de E-N1–N4 en esa fuente autorizada. Solo lectura
  selectiva, sin prompts ni copia del log. Si no existe fuente/permiso o es incompatible,
  detener implementación S01 con el dato exacto faltante; no construir primero S02
  ni cambiar de backend. Esta cualificación no equivale a atribuir uso retrospectivo
  ni sustituye el recorrido prospectivo completo de S03.
- **Alcance/tareas:** preparar SPEC/brief según templates; cualificar contrato nativo
  fijado, binding explícito y modo off/on; adaptador, normalización, ledger transaccional,
  dedup, checkpoint, reporte de tokens y unknowns. Usar primitivas existentes tras
  verificar sus límites; mantener la API CE-v1 compatible.
- **Integración:** context_economy.py solo si se necesita extracción compatible;
  nuevos plan_usage.py, MEASUREMENT.schema.json, test_plan_usage.py y guía (propuestos).
  No RUN nuevo ficticio de delegación, launcher ni configuración global.
- **Aceptación:** AC-01/02/03/04/09/10/12 con fixtures; baseline previo excluido,
  dos planes concurrentes sin cruce, reimportación idéntica, crash antes/después de
  replace, archivo inválido/sensible no filtrado. JSON+texto señalan USD/tiempo unknown.
- **Pruebas/evidencia:** T01–T04, T06, T08–T10, T12 abajo; resultados, diff y fixture
  sintética versionada; CE-v1 sin regresión. No afirmar captura real con esos tests.
- **Riesgos/permisos/parada:** discrepancia contrato/versión, lectura excesiva, daño
  potencial al original, lock no fiable o necesidad de dependencia nueva: parar esa
  integración, documentar; no ampliar fuente automáticamente.
- **Rollback:** no invocar observador; deshabilitado no toca runtime. Conservar ledger,
  no borrarlo. Fallo del comando no bloquea ejecución normal.
- **Cierre:** recorrido offline completo y AC cubiertos; desbloquea S02, no S03 real
  ni consumo real sin su permiso. Perfil crítico de STATE, revalidar al ejecutar.

### S02 — Costos trazables, lifecycle y actualización del reporte

- **Objetivo:** pasar de tokens a cierre contable explicable sin falsa precisión.
- **Entrada:** S01 aceptada, autorización S02 y contrato de snapshot de precios
  aprobado; no exigir precio comercial para probar aritmética sintética.
- **Alcance/tareas:** límites temporales explícitos; aceptación separada; estados
  provisional/incompleto, eventos tardíos y revisiones; Decimal y tarifas versionadas;
  fallos/retries/cancelaciones. USD desconocido es resultado válido ante faltantes.
- **Integración:** módulos/schema/tests/guía propuestos en S01; resumen en briefs
  existentes sin cambiar sus reglas. No nuevo proveedor online ni factura automática.
- **Aceptación:** AC-04–10; sin revaloración silenciosa, sin sumar subsets o tiempos
  paralelos, sin confundir subtotal/API-equivalente/facturado. Reporte anterior preservado.
- **Pruebas/evidencia:** T04–T09, T11/T12; errores de almacenamiento/concurrencia y
  escenarios de tarifas sintéticas desconocidas; fixtures exactas y outputs versionados.
- **Riesgos/parada:** se necesita cobrar, conciliar cuentas o adivinar tarifa/modelo:
  mantener unknown, escalar alcance solo si el usuario requiere esa capacidad.
- **Rollback:** conservar reportes; deshabilitar observador, nunca borrar logs;
  schema incompatible no migra silenciosamente. No afectar uso normal de Quiver.
- **Cierre:** reporter/lifecycle y pruebas aprobadas; S03 desbloqueada solo con evidencia
  real permitida. Perfil crítico de STATE, por integridad/arithmetic/concurrencia.

### S03 — Validación del flujo habitual y cierre de primera entrega

- **Objetivo:** probar que lo construido observa una ejecución real autorizada, no
  solamente fixtures, sin cambiar cómo inicia o conversa el usuario con Codex.
- **Entrada:** S01/S02 aceptadas; usuario autoriza una tarea de trabajo habitual y
  fuente exacta/intervalo privado para observación. No generar tarea artificial paga
  ni delegar para medir. Confirmar host/versión/formato sin inspeccionar historial global.
- **Alcance/tareas:** validar metadatos allowlisted de archivo explícito; efectuar binding
  antes del siguiente turno en reposo; capturar trabajo/validación/correcciones hasta
  aceptación o cancelación; refresh posterior al turno final sin inferencia. Contrastar
  IDs/contadores con registro fuente; evidenciar apagado, pause/resume y límites reales.
- **Integración:** guía, comando local y briefs de S01/S02; evidencia privada externa
  al repo y resumen sanitizado. Ningún acceso al piloto de branch-aware.
- **Aceptación:** AC-01/09/11/12 y regresión restante; versión/host observados y binding
  previo verificables, uso concordante de las respuestas soportadas, faltantes visibles,
  original no modificado. Modalidad/modelo/tarifa ausentes siguen unknown.
- **Pruebas/evidencia:** T13 real + suite offline reciente; privacidad/review N2 del
  diff efectivo conforme a workflow/08 (recomendado dedicado, permiso por separado).
  Máximo una corrección dirigida del review; no cerrar con obligatorios abiertos.
- **Parada:** fuente no disponible, incompatible/comprimida, sin frontera previa,
  subagentes no separables, permiso faltante o contenido inesperado: no sustituir por
  exec/App Server; registrar limitación. Mantener S03 pendiente/bloqueada, no declarar
  que el producto mide el flujo habitual. Continuar solo verificaciones independientes.
- **Rollback:** deshabilitar lectura; conservar evidencia privada y estado incompleto.
- **Cierre:** evidencia real + criterios + review válidos; recién entonces 06_CLOSURE
  y cierre del requirement. No autoriza predictor ni publicación. Perfil de review
  crítico en STATE; configuración efectiva verificable o límite explícito.

## Matriz de pruebas T2 reforzado

| ID | Caso / oráculo esperado | Hito / AC |
|---|---|---|
| T01 | Simple: input 100, cache 60, output 30, reasoning 20 → total 130, no 210; cache-write no cualificado → advertencia | S01 / 03 |
| T02 | Duplicado físico/ID/reimportación → mismo total; acumulados no se suman; conflicto ID → incompleto | S01 / 03,04 |
| T03 | Baseline antes de binding, turno cruzado, dos planes/sesiones, sesión compartida rechazada → sin atribución cruzada | S01 / 02,04 |
| T04 | Crash antes/después commit, dos escritores, lock busy, fsync/replace fallan → checkpoint coherente, retry idempotente | S01/S02 / 04 |
| T05 | Reintento con otro response_id y consumo, fallo/cancelación con/sin usage → contar observado, señalar faltante | S02 / 05 |
| T06 | JSON malformado, línea parcial, truncado, reset acumulado, fuera de orden, versión desconocida → advertencia sin recontar | S01/S02 / 03,04,12 |
| T07 | Cambio modelo/tier, alias/reroute no resuelto, uso/precio desconocido, historial tarifario → unknown o subtotal, no cero | S02 / 08 |
| T08 | Secretos/prompts/código canario en campos no permitidos, symlink/archivo ajeno, path de output en worktree → rechazar/no persistir contenido | S01/S03 / 09 |
| T09 | Off sin acceso a logs; on/error no cambia CLI/modelo/permisos; comandos actuales sin regresión | S01/S03 / 01 |
| T10 | Child/fork con prefix heredado, parent repetido, fuente comprimida/legacy → excluir/reportar límite, no total completo | S01/S03 / 12 |
| T11 | Pause/resume explícitos, reloj regresivo, intervalos paralelos, falta de cierre, dato tardío → tiempos etiquetados/revisión conservada | S02 / 06,07 |
| T12 | Binding → captura → normalización → persistencia → cierre/reporte con tarifas sintéticas exactas | S01/S02 / 02–10 |
| T13 | Recorrido habitual real autorizado con frontera previa y refresh posterior; comprobar fuente vs reporte y no escritura del original | S03 / 01,09,11,12 |

Comando existente **ejecutado**: `python3 -I -B tests/test_context_economy.py` (19 OK).
Dry-run existente ejecutado: `bash scripts/asf balanced --dry-run` (sin inferencia).
Suite general y check-release: existentes, inspección parcial, **no ejecutados**;
revisar efectos/permisos antes de incluirlos. No son prueba real de esta integración.
Comando **propuesto, hoy no disponible**: `python3.14 -I -B tests/test_plan_usage.py`.
El intérprete 3.14.4 ya está instalado; el `python3` por defecto es 3.9.6 y no importa
tomllib del doctor. Revalidar el ejecutable compatible en cada entorno, sin instalar
ni cambiar PATH/configuración como efecto secundario.
La CLI de medición se definirá y comprobará en S01; este plan no da comandos inventados
como si ya funcionaran. T13 no puede sustituirse por unittest.

## Aprobaciones, roadmap y cierre documental

Próxima acción al aprobar este plan: solicitar autorización de ejecución acotada de
S01, no todo el roadmap. Estado de ejecución al 2026-09-24: S01 fue autorizada,
implementada y cerrada offline; la próxima decisión vigente es autorizar o no S02.
La falta de fuente real no bloquea aprobar esta planificación ni verificaciones
independientes existentes; sí impide pasar el gate inicial de S01. Cualificado ese
formato, S01/S02 se construyen con fixtures sin llamadas pagas. S03 mantiene el gate
separado de atribución prospectiva y funcionamiento completo.

Después, fuera del alcance: estimador sencillo basado en ejecuciones comparables;
predicción sellada antes de ejecutar, forecast actualizado y actual separados; validación
temporal contra baseline simple, error/cobertura/amplitud de intervalos y fallos/cancelaciones
incluidos. Dependencias/paralelismo del plan requieren modelo conjunto, no sumar percentiles.
MAPIE solo con historial y beneficio propio demostrado. Presupuestos/routing/paneles
requieren otra decisión; pronóstico conservador no garantiza límite de gasto.

AI Strategy: [STATE](STATE.md#ai-strategy). Sin estimación cuantitativa validada para
S01, S02 o S03. Riesgo de fuente/integración se resuelve primero, no con una investigación
abierta de herramientas ni infraestructura por previsión.
