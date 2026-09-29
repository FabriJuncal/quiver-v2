# Plan de implementación: tokens y tiempo por bloque de actividad

**Entorno a preservar:** terminal → herdr → chat interactivo nativo de Codex CLI.  
**Integración prevista:** Quiver/Kiver, reutilizando lo que realmente exista en el proyecto.  
**Fecha de verificación documental:** 26 de septiembre de 2026.  
**Versión:** plan OTel v1.3 — corrección dirigida de P4, 28 de septiembre de 2026. Versionado independiente del contrato de aislamiento OTel v1.2 y del plan histórico v2 del requirement.
**Estado:** PLAN_CON_INCERTIDUMBRE_CRITICA; R-OTEL-P4-01/02 corregidos y listo para revisión dirigida. P1–P4 conservadas; integración real no probada, sin autorización de implementación ni otro ensayo.

Se aplica [03_PLANIFICAR.md](../workflow_verificable/03_PLANIFICAR.md) junto con
[01_POLITICA_COMUN.md](../workflow_verificable/01_POLITICA_COMUN.md).
Entradas históricas: criterios v2, D01 y plan v2 aprobados el 2026-09-25, y
[OTEL_PLAN_REVIEW.md](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md)
del 2026-09-26. La corrección v1.1 atendió únicamente R-OTEL-01–03 sobre la
propuesta original SHA-256 `5a1c949424376f3b010c81357e19d127e617fe922600d0d13fb84690f194a54d`.
La revisión v1.1 cerró R-OTEL-01–03 y el usuario aprobó P1–P3 el 2026-09-28.
Entradas vigentes de v1.2: [STATE.md](docs/requirements/project-work-activity-attribution/STATE.md),
[EVIDENCE.md](docs/requirements/project-work-activity-attribution/EVIDENCE.md),
el contrato de aislamiento v1.2 y la aceptación «Dale, hazlo» de incorporar
bloques por categoría. Pasos 0–1 ya se completaron; Paso 2 quedó BLOCKED.
Esta edición no repite auditorías, revisiones, pilotos ni pruebas de producto.
La corrección v1.3 fue autorizada mediante «Apruebo» como respuesta a la única
acción pendiente registrada tras el review v1.2. Su alcance se limita a
R-OTEL-P4-01/02; no inicia otra ronda de revisión.

> **Resultado requerido:** contabilizar automáticamente el consumo de tokens y el tiempo de los bloques de **Análisis, Desarrollo, Pruebas y Documentación**, sin reemplazar el chat nativo, sin una interfaz propia y sin obligarte a marcar cada cambio de actividad manualmente.

## 1. Qué se va a construir y qué no

Se propone un **registrador de actividad**, no un nuevo agente que dirija Codex. Su trabajo será recibir mediciones, asociarlas con bloques identificados por el flujo de trabajo, conservarlas y mostrar un resultado verificable.

La separación de responsabilidades será:

- **Codex:** sigue conversando y realizando el trabajo en su interfaz actual.
- **OpenTelemetry Collector:** recibe la telemetría que se compruebe disponible y filtra los datos que se conservarán.
- **Registrador integrado en Quiver:** relaciona las mediciones con las actividades y calcula el reporte. Se implementa con reglas explícitas, no con otra IA que estime el consumo.

La ruta queda condicionada a una comprobación temprana: **tener telemetría no demuestra que podamos atribuirla correctamente a las cuatro actividades**. Esa atribución debe probarse antes de construir la integración completa.

### Alcance incluido

Captura prospectiva del consumo real informado; identificación automática de los bloques; medición temporal con límites observables; persistencia local mínima; prevención de duplicados; histórico JSON/texto por proyecto, tarea y actividad con revisiones preservadas; verificación de que la experiencia nativa permanece intacta. Los cuatro bloques son agrupaciones propuestas con el detalle de §1.1; no eliminan silenciosamente feature, bug o explicación.

### Fuera de alcance

No se incluye una web, TUI propia, dashboard, proxy de las peticiones al modelo, nuevo chat, reemplazo de herdr, migración a `codex exec`, cliente propio de `app-server`, cambio de autenticación, cambio de modelo, router, predictor, presupuesto, facturación, cálculo monetario, alertas, nuevas integraciones empresariales ni creación de otros agentes.

Langfuse, Grafana y similares **no son dependencias de esta entrega**. Haberlos mencionado como visores posibles no equivale a una decisión de instalarlos.

No se alterarán permisos, aprobaciones, pausas, modos de trabajo ni pasos funcionales para facilitar la medición. Si la solución necesita un cambio de esa naturaleza, se informará como incompatibilidad o decisión pendiente; no se ejecutará silenciosamente.

### 1.1. Transición del contrato aprobado — R-OTEL-01

P1–P3 fueron aprobadas para v1.1; su registro y hash se conservan en STATE.
La matriz siguiente documenta esa transición, originalmente propuesta en v1.1,
y no vuelve a solicitar decisiones resueltas. La autorización actual incorpora
P4 al plan y actualiza continuidad; no autoriza spec, slices ejecutables, pilotos
ni implementación. S01–S03, H01/H02 y A01–A03 siguen cerradas. A04/T14 ya no es
dependencia de la ruta OTel aprobada, pero no se declara PASS ni se cierra A04/A05.
El [plan v2](docs/requirements/project-work-activity-attribution/03_PLAN.md)
y sus aprobaciones mantienen su alcance histórico.

| Criterio vigente | Tratamiento en esta propuesta | Paso y comprobación prevista |
|---|---|---|
| AC01: tarea multiactividad sin categoría manual | Conservado; se propone agrupar en cuatro bloques sin perder los detalles siguientes (P1). | 3/6/7: trabajo mixto con detalle automático. |
| AC02: acciones prospectivas, IDs y límites; también sin edición | Conservado; las marcas no sustituyen la evidencia de acciones. | 2/3: cobertura de herramientas y explicaciones sin archivo. |
| AC03: categoría automática y procedencia Kev | Cambio propuesto P2: marca declarada + reglas explícitas, con procedencia separada del consumo observado. | 3/7: contrastar declaración, trabajo observable y cobertura. |
| AC04: respuesta una sola vez; enlace verificable y acciones completas | Conservado; ni etiqueta ni coincidencia temporal justifican exclusividad. | 2/3/7: relación y cobertura por unidad; §5.3. |
| AC05: mixto, sin atribuir y código sin subtipo | Conservado en el reporte. P3 propone una condición más estricta solo para el caso final de aceptación. | 3/7/8: incertidumbre visible, nunca prorrateada. |
| AC06: conciliación y sobrecarga sin repartir | Conservado: una fuente por unidad y estados excluyentes. | 5/7: suma sin duplicación, incluida instrumentación; §5.6. |
| AC07: duración de actividad/herramienta separadas; activo unknown | Conservado, D3 recuperada. | 6/7: límites, unión de intervalos y activo unknown. |
| AC08: USD solo con evidencia directa atribuible | Conservado, sin nuevo cálculo monetario ni precios. Si no hay evidencia utilizable en el ámbito, unknown. | 6/7: sin reparto del cargo de tarea, sin atribuir gasto de Kev al agente. |
| AC09: histórico JSON/texto y revisiones compatibles | Conservado y explicitado en §6.1 (R-OTEL-02). | 4–7: dos tareas, nueva revisión y snapshot anterior intacto. |
| AC10: Kev local automático, abstención y no bloqueo | Sustitución propuesta P2: registrador local sin Kev; falta de señal o error degrada medición, no el chat. | 2/3/7: automatismo y degradación. |
| AC11: evidencia mínima privada y ámbito autorizado | Conservado; no hace falta el resumen efímero para Kev en esta ruta. | 2/7: filtrado previo y aislamiento del ámbito. |
| AC12: evaluación real del clasificador Kev | Sustitución propuesta P2: demostrar marcas, reglas y enlace real. T14 no se declara PASS ni se traslada su corpus/umbrales. | 3/8: evidencia de integración y correspondencia de categorías, no API simulada. |
| AC13: piloto real, conciliado y sin etiquetas manuales | Conservado; P3 añade condición explícita de cierre al caso acotado. | 2/3/8: captura completa demostrada y aceptación de §10. |
| D01: acciones + Kev + contadores | Sustitución propuesta solo de la fuente de clasificación; se conserva atribución conservadora y reutilización del observador. | P2 antes de habilitar pasos 1–3; sin reabrir cierres previos. |

**Organización P1 aprobada, conservada en v1.2:**

| Bloque | Detalle que debe conservarse | Regla funcional |
|---|---|---|
| Análisis | Análisis/planificación; explicación cuando la acción sea explicar al usuario | Analizar internamente no se etiqueta como explicación. La explicación no requiere editar archivos. |
| Desarrollo | Nueva función (`feature`), corrección (`bug`) o implementación sin subtipo | El propósito explícito y las acciones justifican el subtipo; una edición sola no distingue feature/fix. |
| Pruebas | `test` | Preparar o ejecutar pruebas según el objetivo y la evidencia; reparar producto vuelve a Desarrollo/bug. |
| Documentación | `documentation` | Elaborar o actualizar documentación según la acción, no por extensión de archivo. |

Los detalles son desgloses de los bloques, **no otra suma de tokens**. Si una
respuesta mezcla feature y bug, no se adjudica exclusivamente a uno: se conserva
mixta en el detalle; una agrupación Desarrollo solo es posible con evidencia
completa de que todas sus acciones pertenecen a ese bloque. Si mezcla bloques,
va al estado mixto general. Análisis/planificación es visibilidad nueva propuesta,
sin recategorizar registros anteriores. Marcas de bloque y detalle, si son
necesarias, las emite el flujo/agente; nunca las ingresa el usuario tarea por tarea.

**Decisiones P1–P3 aprobadas el 2026-09-28 (contenido conservado):**

- **P1 — presentación:** aprobar las cuatro agrupaciones y conservar el detalle
  anterior, incluida la distinción análisis/explicación. Así no se pierde el
  histórico solicitado al cambiar de enfoque.
- **P2 — clasificación:** aprobar sustituir Kev por marcas automáticas y reglas
  verificables. Se mide trabajo asociado a bloques declarados contrastados con
  acciones observables, no la intención de cada token de razonamiento. Una marca
  sola nunca certifica la cobertura. La alternativa necesita aprobación propia;
  no hereda la de D01/AC03/AC10/AC12.
- **P3 — aceptación acotada:** confirmar la exigencia original de este candidato:
  cero tokens mixtos/sin atribuir o con detalle requerido desconocido en el caso
  final autorizado, además de captura completa demostrada. Es más estricta que
  AC05; no garantiza separación perfecta en futuros trabajos. Primera llamada,
  transiciones y sobrecarga nativa se incluyen en el ámbito fijado de antemano;
  no se recorta después para aprobar. Si no se cumple, no hay cierre completo.

No se solicita nuevamente decidir USD ni tiempo activo: se recuperan las reglas
aprobadas. No se reabren P1–P3. El alcance de cada futura ejecución necesita su
autorización específica; la aceptación de un plan no es permiso de ejecución.

### 1.2. P4 — organizar las tareas de cada slice por categoría

**Decisión aceptada:** el usuario propuso dividir las tareas por categorías al
crear slices y respondió «Dale, hazlo» a incorporarlo al plan existente. Se
registra la aprobación de esa organización y de esta edición documental, no un
review técnico de v1.2 ni permiso para implementar o repetir el piloto.

Una slice mantiene su resultado funcional completo. Quiver propone dentro de
ella bloques de una actividad y detalle P1, con objetivo y condición de cierre.
No se crean slices independientes de documentación o pruebas si eso fragmenta
la entrega funcional. El usuario no elige una categoría global ni debe marcar
cada transición. Se pueden repetir bloques y abrir uno de corrección al hallar
un bug durante las pruebas, dentro del alcance de ejecución autorizado.

P4 concreta P2: la categoría se propone al planificar y se contrasta al ejecutar.
**La categoría prevista, la actividad observada y el consumo atribuido son datos
distintos.** Un bloque rotulado no garantiza una respuesta exclusiva ni captura
completa. P3 se conserva: mezcla o falta de evidencia no permiten cerrar el caso
final de aceptación; no se eliminan esas unidades ni se rebaja el criterio.

El detalle propuesto está en §5.2.1; pasos 3–7 incorporan sus comprobaciones.
No exige un mensaje o chat por bloque, otro modelo ni Kev. No resuelve por sí
solo el aislamiento pendiente del contrato OTel v1.2 ni los contadores ausentes.

## 2. Correcciones necesarias a la propuesta anterior

1. **El “80–90 % resuelto” no estaba respaldado por una prueba.** No se utiliza como estimación de avance, dificultad o esfuerzo.
2. **Los ejemplos `qv phase ...` no son comandos existentes comprobados ni la solución final.** Convertirlos en una obligación manual incumpliría la clasificación automática requerida.
3. **La tabla anterior era ilustrativa, no una medición.** Además, no corresponde sumar nuevamente los tokens de razonamiento cuando ya están incluidos en la salida. La documentación de OpenAI muestra ese desglose dentro de `output_tokens_details`. [S5]
4. **No basta con cruzar cualquier métrica con una hora.** Si un dato agrega varias llamadas, no contiene identificadores suficientes o llega después del cambio de actividad, el cruce puede atribuir consumo al bloque equivocado. Por eso se exige conservar la granularidad y la identidad de la operación.
5. **No se adopta `tool_tokens` como un sumando universal.** El contrato usará únicamente campos reales cuya semántica se haya comprobado.
6. **No se presupone compatibilidad directa Codex → Langfuse.** Esa integración no fue probada y no hace falta para cumplir esta entrega.

## 3. Evidencia disponible y límites de esa evidencia

Las referencias completas están en la sección 13. “Documentado” no significa “probado en tu instalación”.

| Elemento | Qué se verificó documentalmente | Qué falta demostrar localmente |
|---|---|---|
| Telemetría de Codex | Hay exportación OTel y eventos relacionados con uso, herramientas y duración. [S1] | Qué señales emite tu versión y cómo llegan al receptor. |
| Configuración | Existen ajustes separados para exportar logs, trazas y métricas. [S2] | La configuración efectiva de tu sesión y la posibilidad de acotarla al proyecto. |
| Contadores de tokens | El código oficial consultado registra entrada, salida, caché, razonamiento y total en determinadas trazas de respuestas completadas. [S3] | Identificadores, cobertura y significado exacto de esos campos en la versión instalada. |
| Métricas de turno | El catálogo incluye `codex.turn.token_usage` y `codex.turn.e2e_duration_ms`. [S1, S4] | Si su granularidad sirve para separar bloques dentro del mismo turno. |
| Hooks nativos | La documentación contempla eventos de sesión, turno y herramientas; describe identificadores y observación de herramientas locales, incluida `update_plan`. [S6] | Disponibilidad, comportamiento y correlación con la telemetría en tu entorno. |
| Collector | Recibe, procesa y exporta telemetría. [S7] | Configuración mínima, filtrado y funcionamiento local. |
| Exportación a archivos | Existe File Exporter; su documentación declara nivel alpha para logs, trazas y métricas. [S8] | Aceptabilidad para esta integración y prueba de persistencia con versión fijada. |
| Entrega de telemetría | OTLP reconoce la posibilidad de datos duplicados y no garantiza por sí solo toda la entrega extremo a extremo. [S9] | Deduplicación y detección de faltantes en nuestra ruta. |

**No se encontró en estas fuentes una garantía de clasificación nativa en Análisis, Desarrollo, Pruebas y Documentación.** La propuesta es aportar esa relación desde el flujo de Quiver, siempre que pueda observarse de manera inequívoca.

El código enlazado en `main` puede diferir del ejecutable instalado. Durante la auditoría se deberá identificar la versión aplicable y guardar referencias a su etiqueta o commit, cuando estén disponibles.

## 4. Datos pendientes: cómo resolverlos sin inventarlos

Estos pendientes no impiden entregar el plan. Sí impiden dar por configurada o aprobada una implementación que todavía no se probó.

| ID | Dato o decisión | Cómo se resuelve | Qué no hacer |
|---|---|---|---|
| D1 | Versión y configuración efectivas de Codex, y forma real de lanzamiento desde herdr. | Inspección de solo lectura en el entorno del usuario. | Suponer que coincide con la documentación actual. |
| D2 | Cómo representa Quiver los bloques y sus cambios. | Leer el flujo, las instrucciones y el código existentes. | Inventar que ya hay eventos, hooks, archivos o comandos propios. |
| D3 | Recuperado de AC07: duración transcurrida y de herramienta separadas; activo unknown. | Aplicar §5.5; verificar límites disponibles en el piloto. No volver a pedir esta decisión. | Calcular tiempo activo por resta de esperas o equipararlo a inferencia. |
| D4 | Evidencia real de agrupaciones, detalles y procedencia; P1/P2/P4 ya están aprobadas. | Demostrar en paso 3 que las marcas, acciones y cobertura producen la categoría aprobada; no volver a pedir P1/P2/P4. | Confundir decisión aprobada con viabilidad probada, clasificar por palabras sueltas o extensión de archivo. |
| D5 | Evidencia de primera llamada/transiciones y cumplimiento de P3, ya aprobada. | Demostrar enlace y cobertura en el caso acotado; sin ellos queda sin atribuir y no permite cierre completo. | Volver a pedir P3, asignarlo todo a Análisis o recortar el intervalo tras medir. |
| D6 | Persistencia, ejecución local del Collector y lugar del reporte. | Reutilizar mecanismos existentes; exponer cualquier dependencia o archivo adicional antes de introducirlo. | Elegir silenciosamente Docker, SQLite, un servicio permanente o un nuevo comando. |
| D7 | Cobertura de “todo el consumo” de la ejecución. | Identificar operaciones auxiliares reales y cualificar en paso 2 la referencia/mecanismo de completitud de §5.6. | Dar por cubierta toda la ejecución porque concilian las filas recibidas. |

**Regla de resolución:** primero inspeccionar lo que pueda resolver el propio entorno. Después presentar juntos únicamente los puntos que necesiten una decisión del usuario. No volver a preguntar por restricciones ya establecidas.

## 5. Contrato mínimo de medición

Esta sección define las reglas aprobadas P1–P4 que deberá recoger la futura
especificación y las condiciones técnicas aún no demostradas. Describir una
condición aquí no prueba su viabilidad ni autoriza implementarla. D1/D2/D4–D7
son faltantes de evidencia o integración, no decisiones humanas pendientes; no
se vuelven a solicitar P1–P4.

### 5.1. Bloque, turno y llamada no son lo mismo

Un **bloque** es una porción del trabajo identificada con una de las cuatro actividades. Un turno del chat puede contener varios bloques. Una llamada al modelo es una unidad de consumo que la fuente puede informar por separado.

**Ejemplo conceptual, no comportamiento ya comprobado:** dentro de una respuesta a tu pedido, Codex analiza un error, modifica código, ejecuta pruebas y actualiza documentación. Medir únicamente el total del turno no alcanza para repartirlo entre esas actividades.

No se impondrá un orden rígido. El flujo puede volver de Pruebas a Desarrollo, repetir Análisis o terminar sin Documentación si la tarea no la requiere. No se crearán actividades artificiales para llenar el reporte.

La medición será del trabajo correspondiente a un bloque observable. No se presentará como identificación de qué actividad representa cada token del razonamiento interno del modelo.

### 5.2. Cómo se identificarán automáticamente las actividades

**Ruta preferida en v1.2:** organizar los bloques al planificar cada slice (§5.2.1) y reutilizar una señal de inicio/cierre verificable del flujo actual. Paso 0 no encontró productor automático de recibos; hoy existen componentes que reciben datos de un llamador, no esa integración viva. El plan declarado no reemplaza la señal observada.

**Si ese estado no existe:** presentar una instrumentación mínima del flujo actual para emitir una marca automática cuando cambia el bloque. La marca la debe producir el flujo o el agente que ya trabaja, no el usuario mediante comandos manuales. No se implementará hasta mostrar qué instrucción o mecanismo se modifica y qué consumo adicional podría introducir.

Como candidato de observación se probará el mecanismo nativo de hooks, sin convertirlo en un nuevo orquestador. [S6]

Cada marca deberá poder relacionarse con una sesión, un bloque y una posición inequívoca en la secuencia de trabajo. Los nombres de esos campos serán parte del contrato propio; no se presume que Codex los exporte directamente.

Una etiqueta declarada por el agente es evidencia de la **actividad declarada**, no una demostración automática de que toda su conducta corresponde a ella. La prueba contrastará marcas y trabajo observable. No se añadirá un segundo modelo para clasificar ni auditar.

#### Candidato concreto para el piloto cuando no exista otra señal

Si el flujo ya utiliza `update_plan` y su uso está permitido en el modo de trabajo actual, probar esta instrumentación mínima:

1. Identificar la actividad de cada paso mediante una marca explícita acordada, por ejemplo `[ACT:desarrollo] Corregir la validación`. Ese prefijo sería una convención nuestra, no una categoría nativa de Codex.
2. Cuando el agente actualice el plan, observar la actualización exitosa y leer el paso `in_progress`. El esquema consultado contiene `step` y `status`; no añadirle parámetros inventados. [S11]
3. Traducir solo los prefijos de bloque y detalles acordados en P1; registrar el cambio con la identidad de sesión y operación disponible. La convención se precisará antes del piloto sin inventar campos nativos. Si falta marca, detalle o hay varios pasos activos, no adivinar.
4. Aplicar el cambio a partir del límite comprobado. No reasignar retroactivamente la generación que produjo la marca sin una regla aprobada y evidencia suficiente.

**Restricción concreta:** el código oficial consultado rechaza `update_plan` en Plan mode. No se puede adoptar este candidato como solución universal ni obligarte a abandonar ese modo para medir. Se comprobará su aplicabilidad en la versión y el flujo reales; si no aplica, la fuente debe provenir del estado explícito de Quiver o quedar como bloqueo de integración. [S10]

Este candidato no cambia la preferencia por reutilizar una señal existente y no demuestra por sí solo la separación de llamadas mixtas.

**No son métodos aceptables:** buscar “test” en el comando, asumir que todo `apply_patch` es Desarrollo, deducir Documentación por un archivo `.md`, ni estimar la actividad desde silencios o tokens de razonamiento.

#### 5.2.1. Contrato propuesto de bloques dentro de una slice — P4

**Ejemplo de planificación, sin mediciones ni slices nuevas formalizadas:**

| Bloque previsto | Agrupación / detalle P1 | Resultado que delimita el trabajo |
|---|---|---|
| Entender la recuperación de contraseña | Análisis / análisis-planificación | Recorrido y cambio necesario comprendidos |
| Implementar la recuperación | Desarrollo / feature | Comportamiento implementado para comprobar |
| Comprobar la recuperación | Pruebas / test | Resultados de las comprobaciones pertinentes |
| Corregir un error descubierto, solo si ocurre | Desarrollo / bug | Corrección concreta lista para repetir la prueba |
| Repetir la comprobación afectada, si corresponde | Pruebas / test | Resultado posterior a la corrección |
| Documentar el uso, si lo requiere la entrega | Documentación / documentation | Guía actualizada |
| Explicar el resultado al usuario | Análisis / explanation | Explicación entregada, aunque no edite archivos |

No todos los trabajos requieren todos los bloques. La descomposición no agrega
documentación ni pruebas sin necesidad; permite retornos sin una secuencia fija.
Una explicación o tarea pequeña sin slice formal conserva bloques vinculados a
la tarea; la referencia de slice queda no aplicable, no se inventa ni obliga a
crear una slice para medir. Los registros históricos no reciben bloques nuevos.
Análisis significa trabajo observable con ese objetivo, no leer razonamiento
interno. Crear este plan también puede consumir tokens: no se excluye la primera
llamada ni se le atribuye retrospectivamente una categoría sin evidencia.

**Información mínima propuesta, no API implementada:** vínculo proyecto/tarea,
slice y versión de su plan; identidad estable del bloque previsto; agrupación y
detalle, objetivo, entrada necesaria y condición de cierre. Cada ejecución o
reanudación tiene identidad propia, estado, límites observados y referencias a
las unidades de consumo y acciones cubiertas. Se conserva el vínculo con sesión
y respuesta reales. No se guardan prompts, contenidos, argumentos ni secretos.
La spec futura fijará nombres/formato; estos campos no se presentan como campos
nativos de Codex ni como extensión ya admitida por los recibos actuales.

**Recorrido automático previsto:**

1. Quiver propone los bloques desde el objetivo de la slice y sus criterios.
   La categoría prevista no certifica actividad ni consume un presupuesto ficticio.
2. El agente/flujo registra el inicio mediante un mecanismo verificable antes
   del trabajo atribuible. En el recorrido secuencial hay un solo bloque activo;
   si aparecen varios o falta el inicio, no se elige uno por conveniencia.
3. Solo se atribuye una unidad completa con identidad y cobertura de acciones
   suficientes para esa categoría y detalle. Los contadores incluyen el contexto
   que la fuente cobra a esa unidad; no se intenta repartirlo por su origen.
4. Antes de cambiar de categoría se registra el cierre/interrupción del bloque
   y el inicio del siguiente. Una marca dentro de una respuesta no divide sus
   tokens: si la respuesta cruza categorías queda mixta; si falta relación o
   cobertura queda sin atribuir. Un dato tardío conserva su relación original,
   no se adjudica al bloque activo al llegar ni se duplica al cerrar bloques.
   Si abarca dos bloques de la misma categoría, la categoría puede ser conocida
   con cobertura completa, pero el reparto entre bloques sigue sin desglosar;
   se conserva una sola unidad enlazada a ambos, nunca dos cargos exclusivos.
   Esa unidad tiene como propietario contable el agregado compartido de la
   categoría (`shared_within_category` como estado de calidad propuesto, no como
   actividad nueva). Cada bloque muestra solo una referencia no aditiva a la
   misma unidad y su parte permanece `unknown`; ningún subtotal de bloque la suma.
5. Si una prueba descubre un bug, se finaliza/interrumpe ese bloque y se propone
   una ejecución de Desarrollo/bug antes de volver a Pruebas. La transición la
   registra el agente, sin pedir etiquetas. Esto no amplía el alcance autorizado
   ni elimina aprobaciones materiales. Si solo se descubre después de una
   respuesta mixta, se conserva esa mezcla en lugar de inventar límites pasados.
6. Un bloque finalizado, fallido o cancelado conserva el consumo observado. Una
   interrupción sin límite comprobado no se cierra con la hora de reanudación:
   queda incompleta y la reanudación abre otra ejecución vinculada. El cierre
   funcional no certifica que ya llegaron todos los contadores; §5.6 gobierna
   completitud y revisiones por entregas tardías.

Si falla el registro, el chat continúa y la medición se degrada explícitamente.
No se fuerza un turno por categoría, una llamada extra solo para separar cifras
ni un cambio de modo. La eficacia de separar trabajo en bloques sigue pendiente
de comprobar: respetar el plan no prueba por sí solo exclusividad del consumo.

**Integración mínima prevista:** extender el contrato existente y los reportes
con referencias a slice/bloque/ejecución y procedencia prevista/observada, sin
reemplazar los módulos reutilizables. La categoría final procede del contraste
con acciones; una discrepancia visible no se resuelve copiando la prevista.
Cambiar un bloque del plan crea una nueva versión para trabajo futuro; corregir
una atribución con evidencia crea una revisión del reporte, sin mover tokens
por una mera edición del título ni sobrescribir resultados históricos (§6.1).

**Regla contable única — R-OTEL-P4-02:** cada unidad nativa tiene exactamente
un propietario aditivo dentro de una revisión: una ejecución de bloque cuando
la exclusividad está demostrada; `mixed`/`unassigned` según §5.3; o el agregado
`shared_within_category` cuando pertenece de forma indivisible a dos o más
bloques de la misma categoría. Sus referencias desde los bloques llevan la
misma identidad y son siempre no aditivas. JSON y texto distinguen `exclusive`
de `shared_reference`; consultar por bloque no convierte una referencia en uso
propio ni modifica el propietario al cambiar el plan.

La conciliación por categoría aplica:

```text
total de categoría = suma de unidades exclusivas de sus bloques
                   + unidades compartidas de esa categoría contadas una vez
```

El detalle por bloques informa aparte el consumo compartido no desglosable y
no pretende que sus subtotales exclusivos igualen por sí solos el total de la
categoría. El total general cuenta cada identidad nativa una vez. Para tiempo,
los límites propios de cada bloque se conservan y cualquier total transversal
usa la unión de intervalos de §5.5; la referencia compartida no añade duración.

**Incertidumbre que bloquea implementación dependiente:** falta un productor
automático que pruebe límite, identidad y cobertura real. La comprobación mínima
de Paso 3, posterior al PASS de captura de Paso 2 y con autorización propia,
contrastará el recorrido previsto con acciones y unidades de consumo, incluyendo
una transición y una explicación sin edición. Éxito: enlace verificable sin
etiquetas manuales; fallo: unidad indivisible, marca sin cobertura o enlace
ausente quedan visibles y bloquean el cierre P3. Fixtures solo verifican reglas.

### 5.3. Límite de precisión que hay que resolver primero

Una unidad de consumo se asignará exclusivamente a un bloque/detalle solo con
relación verificable a la respuesta nativa **y evidencia de cobertura completa
de sus acciones**, conforme a AC04. Los límites temporales pueden corroborar
esa relación, pero no reemplazan identidad ni cobertura. El piloto deberá
mostrar cómo detecta acciones fuera del observador, incluidas explicaciones;
un booleano declarado por el agente no basta para demostrar completitud.

Si una llamada abarca varias actividades y la fuente solo entrega un total indivisible:

- No dividir los tokens proporcionalmente por tiempo, herramientas, texto generado o porcentajes inventados.
- No atribuir todo al bloque activo cuando llegó el dato.
- Conservar el consumo observado como mixto; sin enlace/cobertura queda sin atribuir. Código sin propósito suficiente conserva implementación sin subtipo. Estos estados no son actividades adicionales ni permiten forzar P3.

Si se propone una convención contable —por ejemplo, asignar una llamada completa al bloque que la inició— deberá explicarse y aprobarse. **Una convención reproducible no equivale a una separación exacta de trabajo mixto.**

No se resolverá esta limitación obligándote a abrir otra sesión, enviar un mensaje por fase o reemplazar el chat por ejecuciones automáticas separadas.

Si la prueba no permite satisfacer la precisión requerida sin esas modificaciones, no se aprobará esa ruta. Se entregará la evidencia concreta del bloqueo, sin rebajar el requerimiento.

### 5.4. Contabilización de tokens

Seleccionar **una fuente contable principal por unidad de consumo**. Las otras señales podrán servir para contraste, pero no sumarse otra vez.

Con la semántica de uso documentada por OpenAI, la entrada cacheada se presenta como desglose de entrada y el razonamiento como desglose de salida. No se suman de nuevo al total. [S5]

```text
Total de tokens = entrada + salida
Caché y razonamiento = desgloses, no sumandos adicionales
```

**Prueba sintética:** entrada 1.000, salida 400, de los cuales 600 son entrada cacheada y 150 son razonamiento. El total esperado es **1.400**, no 2.150. Estos números son datos de prueba, no consumo real tuyo.

Reglas adicionales:

- Un campo ausente se representa como no disponible, no como cero.
- No confundir tamaño del contexto con consumo acumulado.
- No sumar un contador acumulado en cada lectura. Si hay que obtener diferencias, comprobar el ámbito y los reinicios del contador.
- Contar una repetición real de la petición como consumo nuevo cuando tenga su propio uso; no confundirla con la retransmisión del mismo evento.
- Mantener trazabilidad del uso confirmado en operaciones interrumpidas; no inventar el uso que la fuente no informó.

### 5.5. Medición del tiempo

Se recupera D3 de AC07; no se propone cambiar la definición aprobada:

| Magnitud | Definición | Condición para informarla |
|---|---|---|
| Transcurrido del bloque | Fin observable menos inicio observable. | Ambos límites disponibles. |
| Espera identificada | Intervalos de espera con inicio y fin explícitos. | No deducirlos de la ausencia de eventos. |
| Duración de herramienta | Fin menos inicio de la herramienta observada. | Se muestra separada del bloque; no se suma a su duración. |
| Tiempo activo de IA | Desconocido (`unknown`). | No se calcula restando esperas, ni se presenta como tiempo pensando. |

Usar la hora de ocurrencia del evento, no la de recepción de un lote. Comprobar el orden entre relojes de distintas fuentes. Para duraciones locales, utilizar un reloj monotónico cuando esté disponible.

No sumar duración del turno, duración de sus llamadas y duración de sus herramientas: pueden describir intervalos superpuestos. Cuando se necesite un total temporal sin duplicación, calcular la unión de intervalos.

Una sesión abierta sin trabajo no implica actividad continua. Si un bloque queda interrumpido sin cierre verificable, mostrarlo como incompleto; no prolongarlo hasta la siguiente vez que se abra Codex.

### 5.6. Integridad y cobertura

El reporte deberá permitir comprobar:

```text
Tokens observados = tokens atribuidos a las cuatro actividades
                   + tokens observados pendientes de atribución
                   + sobrecarga nativa separable por evidencia
```

“Pendiente de atribución” es un **estado de calidad del dato**, no una quinta actividad funcional ni una forma de considerar terminado el requerimiento.

Cada unidad aparece una sola vez en esa ecuación. La sobrecarga inseparable ya
está dentro de la unidad observada y no se añade otra vez. La vista por detalles
P1 concilia por separado con el mismo total, incluyendo sus propios mixtos/sin
subtipo; no se suman entre sí las vistas por bloque y por detalle.

También se distinguirá **captura completa demostrada**, **incompleta** (faltante
observado) y **no verificada** (sin prueba suficiente). Que todo lo recibido tenga
etiqueta no demuestra que se haya recibido todo lo consumido.

**Contrato de completitud — R-OTEL-03.** En paso 2, antes de construir sobre la
captura, se cualificará una referencia del mismo ámbito o un mecanismo con
evidencia equivalente: límites prospectivos de inicio/fin, identidad de ejecución,
unidades esperadas o totales de origen comparables y prueba de finalización de la
entrega. Un manifiesto cerrado por el emisor o contadores de origen podrían servir
solo si su semántica/cobertura se demuestra; no se presume que Codex los ofrezca.
Debe permitir detectar una unidad omitida y distinguir un último evento aún en
tránsito de un cierre final. Un total calculado sobre los mismos eventos recibidos,
un receptor sin errores, un timeout o un intervalo silencioso no son prueba de
completitud. La referencia no se suma al ledger ni se usa para rellenar faltantes.

Registrar origen, versión, ámbito, regla de comparación y condición de entrega
final de esa evidencia. Si requiere un acceso adicional, exponerlo y obtener el
permiso acotado antes; no abrir un segundo canal ni leer sesiones por defecto.
Sin referencia/mecanismo cualificado: captura no verificada, sin avance a la
integración completa ni cierre. Con discrepancia: incompleta. Solo puede seguir
un subalcance independiente expresamente autorizado, sin declararlo entrega total.
Una entrega tardía genera una nueva revisión cuando se verifica; no modifica el
reporte anterior ni convierte el mero paso del tiempo en éxito.

La cobertura de captura y la de acciones por respuesta son pruebas diferentes:
la primera acredita consumo recibido; la segunda habilita atribución exclusiva.
Mixtos, sin atribuir y sobrecarga identificable participan una sola vez en la
conciliación. La instrumentación inseparable no se resta ni reparte por estimación.

La deduplicación usará identificadores reales de operación o una clave reproducible cuya unicidad se demuestre. Dos operaciones con los mismos contadores no son necesariamente duplicadas. [S9]

## 6. Arquitectura mínima propuesta

```text
EXPERIENCIA DEL USUARIO — SIN REEMPLAZOS

Terminal → herdr → Codex CLI interactivo
                         │
                         ├── Telemetría de consumo y tiempos
                         │             │
                         │             ▼
                         │     Collector local + filtrado
                         │             │
                         └── Marcas automáticas del flujo
                                       │
                                       ▼
                            Registrador de Quiver
                                       │
                                       ▼
                         Persistencia local + reporte textual
```

Las marcas y la telemetría podrán llegar por caminos diferentes. El punto de unión será su identidad y orden comprobados, no una variable global con “la fase actual”.

**Reutilizar antes de crear:** si Quiver ya tiene persistencia, lectura de eventos o presentación textual, se extenderá ese mecanismo. No se abrirá otro proyecto ni se añadirá otra base de datos por defecto.

### 6.1. Histórico y compatibilidad — R-OTEL-02

Inspección de solo lectura del 2026-09-28: existen
`scripts/lib/plan_usage.py::snapshot_activity_report`, `activity_history_report`
y `render_activity_history_text`; conservan `project_id`, `work_id`, revisiones
y estados de reportes faltantes/desactualizados. `scripts/lib/work_activity.py`
define las cinco categorías, mixto y sin atribuir. Son puntos reutilizables;
el adaptador OTel y la producción automática de marcas siguen siendo propuestos,
no componentes cuya integración se haya probado.

El resultado exigido es un histórico **proyecto → tarea (`work_id`) → slice (si existe) y
versión del plan → bloque previsto → ejecución del bloque → sesión/unidad de consumo**,
con referencias a la ejecución de la tarea, consultable en JSON y texto con la misma
semántica. La captura solo incorpora trabajo nuevo del binding prospectivo.
El reporte por ejecución es un detalle del histórico, no su sustituto.

La extensión será opt-in y versionada; spec fijará el identificador de formato
sin reutilizar una versión existente para otra semántica. Las salidas y snapshots
v1/v2 permanecen legibles e intactos, sin migración destructiva, recategorización
retroactiva ni importación de sesiones pasadas. Se pueden seguir consultando los
registros ya guardados, pero no reinterpretarlos como bloques de la nueva ruta.
Vistas de contratos distintos identifican su versión y no suman dos veces una
misma unidad nativa.

Dentro de la nueva versión, la identidad de la unidad y su propietario contable
de §5.2.1 gobiernan todas las vistas. Una unidad `shared_within_category` aparece
una vez en el agregado aditivo de su categoría; los bloques relacionados exponen
referencias no aditivas. JSON y texto deben coincidir en propietario, referencias,
estado no desglosable y totales. Reprocesar o cambiar la versión del plan no
puede convertir esas referencias en copias ni elegir después un bloque arbitrario.

Una reclasificación crea una revisión nueva con versión de reglas/marcas y
referencia a la evidencia; no cambia los contadores de origen ni sobrescribe
la revisión anterior. Una entrega tardía puede añadir uso realmente observado
en otra revisión, indicando esa diferencia; no se confunde con reclasificar.
Cada consulta usa una sola revisión consistente por ejecución; si falta o está
desactualizada, lo muestra. Las sumas de proyecto/tarea excluyen revisiones
anteriores del agregado actual, no del historial consultable.

USD conserva el contrato aprobado: solo cargo directo atribuible con evidencia,
sin repartir importes globales, consultar facturas ni calcular precios. Ausencia
de evidencia produce `unknown`; conservar un cargo previo no certifica su factura.
Tiempo activo permanece `unknown`. Se preservan campos/modelo/tier/modalidad
desconocidos cuando no haya evidencia, sin inferirlos desde catálogo o lanzamiento.

Para el piloto, File Exporter es un candidato concreto de salida local, no una dependencia definitiva aprobada. Su formato requiere fijar versión y comprobar compatibilidad. También debe evitarse el truncado accidental: su documentación indica `append: false` por defecto y restricciones al combinar append con rotación. [S8]

No se presupone que el Collector sea indispensable para cualquier solución posible. Aquí se propone para reutilizar recepción y filtrado OTel en lugar de desarrollar un receptor desde cero. [S7]

## 7. Paso a paso de ejecución

**Secuencia:** auditoría → decisiones mínimas → prueba de captura → prueba de atribución automática → especificación → implementación acotada → validación → entrega.

Cada paso tiene una salida verificable. Un paso que no cumple su condición de avance no habilita a compensarlo ampliando el alcance.

Esta secuencia es futura y condicionada: la corrección documental actual termina
antes de ejecutarla. Los criterios cubiertos y sus pruebas están en §1.1. Paso 0
requiere permiso de auditoría; paso 1 recibe su inventario y las decisiones P1–P3;
pasos 2–3 requieren contrato/permisos concretos del piloto; paso 4 recibe evidencia
aprobatoria de ambos; pasos 5–6 requieren spec y autorización de implementación;
pasos 7–8 comprueban esa integración y el caso real específicamente autorizado.

### Paso 0 — Auditar el entorno sin modificarlo

**Objetivo:** conocer el punto de integración real.

1. Identificar la copia de Quiver en la que se trabajará y las instrucciones aplicables.
2. Registrar cambios locales existentes para no sobrescribir trabajo ajeno.
3. Identificar el ejecutable y la versión de Codex usados por herdr. Los comandos `codex --version` y `codex --help` son comprobaciones iniciales; verificar que se consulte el mismo ejecutable que lanza herdr.
4. Leer únicamente la configuración relevante: telemetría, hooks, límites de permisos y mecanismos de lanzamiento. No volcar credenciales ni archivos de autenticación.
5. Localizar cómo se expresa el estado de las actividades en el proyecto. Registrar “no encontrado” si no existe.
6. Identificar persistencia y salida textual reutilizables.

**Salida:** inventario con evidencia, archivos reales implicados y pendientes D1–D7 actualizados.

**Condición de avance:** entender qué se modificaría y dónde. Todavía no instalar dependencias, cambiar configuración ni iniciar otras sesiones para medir la actual.

### Paso 1 — Definir el piloto y resolver sus decisiones imprescindibles

**Objetivo:** evitar una prueba que parezca exitosa porque cambió el requerimiento.

1. Elegir una tarea pequeña, autorizada y representativa para el piloto; puede ser un caso aislado que no toque código productivo.
2. Definir el alcance de la ejecución y las sesiones que se medirán. No leer todo el historial del usuario.
3. Registrar P1–P3 sin asumirlas aprobadas; recuperar D3/AC07 y AC08 sin volver a pedir decisiones de tiempo activo o USD. Fijar ámbito, primera llamada, transiciones y cierre antes de medir.
4. Presentar el cambio mínimo de instrumentación, dependencias, archivos y configuración, junto con su reversión.
5. Elegir cómo se inicia y termina el componente local sin alterar el lanzamiento habitual ni introducir un servicio permanente por defecto.
6. Registrar el consumo de las pruebas como pruebas de esta implementación; no ocultar que un ensayo real puede consumir tokens.

**Salida:** contrato breve del piloto y lista cerrada de cambios autorizados.

**Condición de avance:** no quedan decisiones implícitas que alteren la experiencia o el significado de los resultados. Las decisiones desconocidas se consultan juntas, no en una cadena de confirmaciones innecesarias.

### Paso 2 — Probar la captura real, todavía sin clasificar

**Objetivo:** demostrar qué datos se obtienen del Codex interactivo existente.

1. Preparar un receptor OTel local con versiones identificadas y solo las señales necesarias.
2. Definir una lista permitida de campos antes de persistir: identificadores técnicos, marcas temporales, actividad cuando exista y contadores.
3. Aplicar únicamente el cambio de configuración aprobado. Conservar la configuración previa; no reemplazar archivos completos.
4. Realizar una interacción autorizada desde terminal → herdr → Codex, usando el mismo modo de autenticación y de trabajo.
5. Inspeccionar una muestra reducida: identificador de sesión, de turno y de llamada cuando existan; inicio y fin; uso informado; duplicados y demora de entrega.
6. Comprobar si varias llamadas del mismo turno pueden distinguirse. Conservar el ejemplo desidentificado que lo demuestre.
7. Cualificar la referencia o mecanismo de completitud de §5.6: misma ejecución/ventana, unidades o totales comparables y entrega final verificable. Documentar qué pérdida puede detectar. Sin esa evidencia, informar captura no verificada.

**Salida:** muestra real mínima, mapa de campos disponible/no disponible/no verificado y contrato de completitud con evidencia o bloqueo explícito.

**Condición de avance:** fuente contable con identidad y granularidad suficientes y mecanismo de completitud cualificado para el ámbito autorizado. Ni un total general ni una suma interna correcta habilitan paso 3 o integración completa. Si falta completitud, solo podría continuar un subalcance independiente expresamente autorizado, sin declaración de cumplimiento completo.

**Si falla:** revisar una incompatibilidad concreta de versión o configuración. Si exige otra tecnología o un cambio de experiencia, informarlo; no reemplazar silenciosamente la arquitectura.

### Paso 3 — Probar la atribución automática de las cuatro actividades

**Objetivo:** validar la parte crítica antes de construir el registrador completo.

**Entrada:** Paso 2 PASS con captura completa y contrato de atribución
específicamente autorizado. P4 se planifica ahora, no adelanta esta ejecución.

1. Conectar la fuente de estado encontrada en Quiver. Si no existía, usar solo la instrumentación automática expresamente aprobada en el paso 1.
2. Probar el enlace entre cada marca y la sesión/operación correspondiente. Un hook que dispara correctamente no demuestra por sí solo esa relación.
3. Usar una tarea organizada en bloques de slice según §5.2.1, con categorías propuestas por Quiver y cambios automáticos. Recorrer las cuatro actividades en el chat nativo, sin comandos manuales de fase ni un mensaje por etapa. Conservar por separado plan y ejecución observada.
4. Revisar especialmente la primera llamada, los cambios dentro de un turno y el consumo al cerrar una actividad.
5. Verificar qué ocurre cuando se vuelve de Pruebas a Desarrollo y después a Pruebas, cuando ese recorrido sea parte del caso aprobado.
6. Comparar bloques y detalles P1 con trabajo observable y cobertura completa de acciones por respuesta, incluidas las que no editan archivos. Una marca declarada no demuestra exclusividad.
7. Registrar los casos de consumo indivisible o sin marca; no rellenarlos mediante estimaciones. Contrastar desvíos frente al bloque previsto; probar cierre, interrupción y reanudación sin atribución retroactiva.

**Salida:** secuencia de bloques, operaciones y consumo asociado, con los casos no resueltos visibles.

**Condición de avance:** clasificación automática, cobertura de acciones y relación uso→bloque/detalle demostradas sin modificar el modo de trabajar. Se comprueba la viabilidad de P3 con el alcance previamente aprobado; si quedan unidades indivisibles o sin enlace, se conserva la evidencia del bloqueo, no se avanza a integración completa para intentar ocultarlo.

**Fallo decisivo:** si la única forma de aprobar es marcar fases manualmente, forzar una actividad por turno o convertir Codex en un proceso headless, esta ruta no cumple el requerimiento. El resultado debe describir el bloqueo concreto, no declarar éxito parcial como entrega terminada.

### Paso 4 — Cerrar la especificación con lo aprendido

**Objetivo:** implementar sobre un contrato probado, no sobre expectativas.

1. Incorporar fuentes y versiones verificadas, definición de tiempo y reglas de actividad.
2. Especificar el vínculo de §6.1, incluyendo slice/versión y bloque previsto frente a su ejecución observada, reutilizando `project_id`, `work_id` y binding. Fijar cómo se reconoce una misma unidad al consultar formatos distintos; no exigir ni reconstruir esos campos en históricos v1/v2.
3. Documentar la fuente contable, desgloses, deduplicación, tratamiento de interrupciones y criterio de completitud.
4. Fijar el histórico JSON/texto de §6.1, versión opt-in, selección de revisiones y preservación v1/v2, junto con los archivos que se podrán tocar.
5. Dividir la implementación en tres partes pequeñas: lectura y persistencia; asociación y cálculo; reporte y validación.

**Salida:** especificación y criterios de aceptación consolidados en la estructura documental existente. No crear una jerarquía documental nueva si el proyecto ya tiene una.

**Condición de avance:** los pasos 2 y 3 tienen evidencia aprobatoria. No iniciar la integración completa con el punto central todavía sin demostrar.

### Paso 5 — Implementar el registro persistente mínimo

**Objetivo:** que cada dato utilizado pueda revisarse y reprocesarse sin duplicación.

1. Implementar el adaptador de la fuente comprobada, usando el lenguaje y las convenciones del proyecto.
2. Conservar únicamente campos permitidos y una referencia reproducible a su origen.
3. Guardar identidad de proyecto, tarea, ejecución, unidad, sesión y bloque/detalle, tiempos, contadores, versiones y estados de calidad de captura/atribución por separado. Esto es un esquema propio propuesto, no campos nativos garantizados.
4. Asociar el consumo a la actividad por la relación comprobada en el piloto.
5. Reprocesar solo los datos autorizados de la captura prospectiva sin duplicar. Crear revisiones para evidencia posterior o reclasificación según §6.1, conservando snapshots anteriores y contadores de origen; no importar trabajo pasado.
6. Proteger la lectura frente a registros parcialmente escritos y conservar el punto de recuperación.
7. Separar los datos por ejecución y sesión para que otra conversación no cambie la fase de esta.

**Salida:** registro local versionado, aislado por proyecto/tarea, que reconstruye el piloto y conserva reportes v1/v2.

**Condición de avance:** misma evidencia y revisión producen los mismos totales tras reiniciar; nueva clasificación no cambia consumo, snapshots anteriores siguen intactos y las revisiones no duplican el agregado actual.

No se promete recuperar eventos que nunca fueron emitidos o conservados. Cuando no haya una fuente comprobada para recuperarlos, el resultado debe permanecer incompleto. No se añadirá un segundo canal de captura sin necesidad demostrada y cambio explícito del plan.

### Paso 6 — Implementar cálculos y reporte textual

**Objetivo:** obtener la respuesta requerida, sin una interfaz nueva.

1. Calcular entrada, salida y total exclusivo por bloque; presentar caché y razonamiento como desgloses cuando existan. Mostrar aparte referencias compartidas no aditivas y el agregado `shared_within_category` que las contabiliza una sola vez.
2. Calcular el tiempo conforme a D3, evitando intervalos superpuestos.
3. Ofrecer histórico acumulado por proyecto y tarea, detalle por ejecución y bloque, y resumen de las cuatro agrupaciones con detalles P1. Mostrar repeticiones cuando se retoma una fase. Los detalles y referencias compartidas no se suman otra vez a los bloques o a la categoría.
4. Incorporar el estado de cobertura y, cuando corresponda, consumo sin atribución o datos faltantes.
5. Extender los puntos existentes de histórico JSON/texto de §6.1. Elegir una revisión consistente por ejecución, mostrar faltantes/desactualizados y conservar la consulta de revisiones anteriores. No sustituir el histórico por un archivo aislado de la última tarea.
6. Generar el reporte mediante código, sin otra llamada al modelo para redactarlo.

**Salida propuesta, no valores reales:**

| Actividad | Tiempo según contrato | Entrada | Salida | Total | Estado |
|---|---:|---:|---:|---:|---|
| Análisis | Dato medido | Dato medido | Dato medido | Dato medido | Verificado / incompleto |
| Desarrollo | Dato medido | Dato medido | Dato medido | Dato medido | Verificado / incompleto |
| Pruebas | Dato medido | Dato medido | Dato medido | Dato medido | Verificado / incompleto |
| Documentación | Dato medido | Dato medido | Dato medido | Dato medido | Verificado / incompleto |

El total general y cualquier consumo pendiente se mostrarán aparte, con la definición temporal utilizada. Una actividad no realizada se distinguirá de una actividad realizada pero no medible.

La tabla es el resumen de una ejecución seleccionada; el histórico también
identifica proyecto, tarea, revisión, detalles P1, cobertura de captura y
atribución. USD sin evidencia y tiempo activo aparecen como `unknown` en ambas
salidas. La condición P3 del caso de aceptación no suprime estos estados.

**Condición de avance:** cada cifra se explica con registros de origen; JSON y texto coinciden por proyecto/tarea/revisión, preservando v1/v2. Ningún agregado oculta discrepancias o suma revisiones anteriores como consumo nuevo.

### Paso 7 — Validar con pruebas proporcionales

**Objetivo:** cubrir errores que afectarían directamente la medición o tu experiencia.

Usar datos sintéticos y reproducidos para cálculos y fallos. Reservar sesiones reales para demostrar lo que no pueda comprobarse de otra manera.

| Prueba | Resultado esperado |
|---|---|
| Chat nativo e interacción normal | Siguen funcionando conversación, aprobaciones e interrupciones, sin nuevo chat ni comandos de fase. |
| Tarea con las cuatro actividades | Los cambios se registran automáticamente; la primera llamada y las transiciones tienen tratamiento explícito. |
| Vuelta de Pruebas a Desarrollo | Se conserva el recorrido real sin asumir una secuencia única. |
| Tokens con caché y razonamiento | El ejemplo de la sección 5 produce 1.400; los desgloses no inflan el total. |
| Evento repetido y operaciones distintas con igual uso | El primero no duplica; las segundas sí cuentan por separado. |
| Dato retrasado al cambiar de fase | Se asigna por identidad y secuencia original, no por hora de recepción. |
| Intervalos y espera | No hay doble suma; solo se descuentan esperas identificadas. |
| Interrupción y reanudación | No se inventa un cierre ni se cuenta todo el tiempo entre sesiones como trabajo. |
| Consumo mixto o faltante | Se informa la limitación; no se prorratea ni se convierte un ausente en cero. |
| R-OTEL-01: marca sin cobertura; feature/fix y explicación sin archivo | La marca sola no atribuye tokens. El detalle P1 se conserva solo con evidencia suficiente; mezcla e incertidumbre siguen visibles. |
| P4: slice multiactividad y retorno test→bug→test | Bloques propuestos automáticamente, ejecuciones distintas y detalle conservado; sin categorías manuales, otra sesión o doble suma. |
| P4: bloque previsto documentation con acciones de feature; respuesta que cruza bloques | La etiqueta del plan no fuerza la categoría final; discrepancia visible, mixto o sin atribuir según cobertura/identidad. |
| P4: bloque cerrado con contadores tardíos; marca ausente o dos bloques activos | Identidad original preservada, captura no se declara completa al cerrar el bloque, sin asignación por hora de llegada ni elección arbitraria. |
| P4: fallo/cancelación, reanudación y cambio de versión del plan | Uso observado conservado; sin tiempo ficticio ni recategorización por editar el plan; nueva ejecución/revisión y snapshot previo intacto. |
| R-OTEL-P4-02: dos bloques de Pruebas y una respuesta indivisible enlazada a ambos | JSON/texto muestran una unidad `shared_within_category` contada una vez en Pruebas; ambos bloques referencian la misma identidad como no aditiva, sus subtotales exclusivos no la incluyen y total de categoría/general concilia sin duplicación. |
| R-OTEL-02: dos tareas del mismo proyecto y revisión posterior | Consultas JSON/texto separan tareas; reclasificar una no altera sus tokens ni la otra tarea; agregado usa solo una revisión por ejecución. |
| R-OTEL-02: snapshot v1/v2 anterior y reprocesado | Snapshot y salida previa intactos, sin recategorización/importación de pasado; ninguna unidad se cuenta dos veces entre formatos. |
| R-OTEL-03: omitir una unidad en un registro reproducido con referencia completa | Aunque las filas recibidas concilien, la comparación detecta pérdida, marca incompleta y bloquea cierre. Sin referencia, marca no verificada, nunca completa. |
| R-OTEL-03: última unidad retrasada al solicitar cierre | No se cierra por silencio/timeout. Tras llegada y comprobación de entrega final, nueva revisión concilia; la anterior permanece incompleta/no verificada y no hay duplicación. |
| AC07/AC08: límites y evidencia monetaria ausentes | Duración desconocida sin límites, activo unknown siempre; USD unknown sin cargo directo atribuible y sin repartir cargos globales. |
| Otra sesión ajena a la ejecución | No contamina la actividad ni los totales; puede comprobarse con registros reproducidos. |
| Collector o registrador no disponible | Codex conserva su funcionamiento; el reporte no afirma cobertura completa. |
| Datos sensibles | No quedan prompts, código, salidas completas, correos ni credenciales en los archivos generados por la medición. |

Comprobar también las operaciones auxiliares que se hayan encontrado en D7. No introducir compactaciones, agentes o concurrencia artificiales si no forman parte del flujo que se decidió soportar. Las nuevas pruebas reproducidas verifican cálculo y detección de fallos, no prueban integración viva. No repetir gates de S01–S03/H01/H02/A01–A03: solo regresiones directamente afectadas al implementar. No reutilizar el corpus Kev como oráculo de esta ruta ni ejecutar T14.

**Salida:** resultados reproducibles y evidencia de fallos corregidos o bloqueos abiertos.

**Condición de avance:** pasan las pruebas aplicables. No se exige una regresión general del producto, pruebas de carga empresariales ni un proyecto de seguridad separado.

### Paso 8 — Validación final, entrega y reversión

**Objetivo:** demostrar el resultado en el entorno real y dejarlo mantenible.

1. Ejecutar el caso integrado aprobado en la versión real de Codex, a través de herdr.
2. Revisar los cuatro bloques y detalles realmente ejercitados, el histórico por proyecto/tarea/revisión y la conciliación con evidencia de completitud cualificada en paso 2. Aplicar P3 sin excluir primera llamada, transiciones o sobrecarga de manera retrospectiva.
3. Comprobar que la medición no añadió aprobaciones, mensajes de fase, nuevas sesiones ni cambios de modelo.
4. Registrar el impacto observable del componente de medición. Si introduce latencia o llamadas adicionales, informarlas y contrastarlas con el criterio acordado; no afirmar impacto cero.
5. Documentar activación, desactivación, archivos modificados y ubicación de los registros.
6. Probar la reversión: retirar únicamente la instrumentación añadida, detener el componente correspondiente y conservar el trabajo y los datos previos.

**Salida:** código acotado, configuración versionada, evidencia, reporte real e instrucciones de uso y reversión.

**Condición de terminado:** se cumplen todos los criterios de la sección 10. Si falta evidencia de atribución o completitud, entregar el estado real y el bloqueo; no marcar la funcionalidad como finalizada.

## 8. Reglas de operación y protección del flujo

### El registrador no puede tomar decisiones por vos

Los puntos de observación se configurarán para no autorizar herramientas, denegarlas, reescribir sus argumentos, cancelar trabajo ni provocar continuaciones. Deben devolver la respuesta neutral adecuada al contrato de cada evento, con ejecución acotada. La documentación distingue comportamientos entre hooks; no se supondrá que todos aceptan la misma salida. [S6]

Si falla la medición, debe degradarse la medición, no el chat. Eso implica reportar incompletitud, no bloquear Codex para forzar una contabilidad perfecta.

### Privacidad antes de persistir

`otel.log_user_prompt = false` no se tratará como garantía de que cualquier otra señal esté libre de contenido: la documentación también describe resultados de herramientas con fragmentos de salida. [S1, S2]

La implementación conservará solo los campos necesarios, filtrados antes de escribirlos. Se acotará al proyecto y a las sesiones autorizadas. No se subirán registros a terceros ni se recopilará el historial global.

### Sin gasto oculto de instrumentación

No habrá otro modelo encargado de estimar tokens, tiempo o categorías. Si la marca automática exige nuevas instrucciones o llamadas de herramienta del agente existente, ese cambio se expondrá y su consumo formará parte de la medición. No se prometerá ahorro ni costo cero sin medirlo.

## 9. Cómo aplicar Workflow Driven Development y Spec Driven Development

Estas metodologías organizan la implementación; no autorizan a reconstruir tu forma de usar Codex.

**Workflow Driven Development:** describir el recorrido real de las actividades, sus retornos y sus límites observables. Instrumentar únicamente esos puntos. No agregar etapas para simplificar los gráficos.

**Spec Driven Development:** fijar significado de los datos, fórmulas, atribución, restricciones y criterios antes de implementar la integración completa.

Para cada parte pequeña de la implementación se registrará: alcance permitido, archivos afectados, criterio de aceptación, evidencia, resultado y siguiente paso. Reutilizar los documentos de estado existentes. No convertir esto en otro sistema de tickets, orquestación o documentación paralela.

## 10. Criterios de terminado

- [ ] Se mantiene terminal → herdr → chat interactivo nativo de Codex.
- [ ] Las actividades se identifican automáticamente, sin comandos manuales de fase.
- [ ] P4: cada slice conserva su entrega funcional con bloques pertinentes propuestos por Quiver; categoría prevista y actividad observada se distinguen, con límites/enlace comprobados y sin forzar un turno por categoría.
- [ ] P1–P3 están aprobadas para esta versión; feature, bug, test, explicación y documentación conservan detalle, sin duplicar los totales de las cuatro agrupaciones.
- [ ] Se respetan pausas, permisos, aprobaciones y decisiones existentes.
- [ ] Se usan contadores reales, con su semántica verificada y sin doble conteo.
- [ ] El tiempo tiene una definición explícita y límites observables.
- [ ] Duración de bloque/herramienta separadas; tiempo activo unknown y USD unknown cuando falta evidencia directa atribuible, sin nuevos precios ni reparto.
- [ ] Primera llamada, cambios de bloque y actividades mixtas tienen tratamiento comprobado y aceptado.
- [ ] Se concilia el consumo de la ejecución; no se oculta uso sin atribución ni faltantes.
- [ ] Captura completa demostrada mediante §5.6; pérdida selectiva y entrega final retrasada no producen falso cierre. La cobertura de acciones habilita por separado la exclusividad de atribución.
- [ ] Reprocesar datos no duplica resultados y una interrupción no produce tiempos ficticios.
- [ ] El reporte funciona sin interfaz nueva ni otra IA para calcularlo.
- [ ] Histórico JSON/texto por proyecto/tarea/ejecución, revisiones preservadas y una sola revisión consistente en el agregado; v1/v2 intactos, sin importar pasado.
- [ ] Cada unidad tiene un solo propietario aditivo; una unidad compartida entre bloques iguales se cuenta una vez en su categoría y solo se referencia, sin sumarse, desde los bloques. JSON, texto, detalle y totales coinciden.
- [ ] Los registros están acotados, filtrados y son revisables.
- [ ] Hay evidencia sobre la versión real instalada, no solo sobre documentación o `main`.
- [ ] La reversión deja intactos el chat, su configuración previa y el trabajo del usuario.

**Condición P3 aprobada, conservada:** para declarar cumplimiento
completo, el caso de aceptación debe cubrir los cuatro bloques con correspondencia
verificada de los detalles ejercitados, captura completa demostrada y cero tokens
mixtos/sin atribuir o con detalle requerido desconocido dentro del ámbito acordado
antes de medir. No es una garantía de separar cada token interno ni todo trabajo
futuro. Si P3 falla, registrar el bloqueo antes de proponer cambiar
el criterio; no dar por aprobada una relajación. El mecanismo mantiene mixtos,
sin atribuir e incompletitud cuando falte evidencia en cualquier ejecución.

## 11. Control de cambios de alcance

Ante un descubrimiento, clasificarlo antes de actuar:

| Tipo | Tratamiento |
|---|---|
| Ajuste interno que mantiene comportamiento, precisión y dependencias aprobadas | Documentarlo y continuar con la prueba mínima correspondiente. |
| Dependencia nueva, modificación del flujo, regla de atribución nueva o cambio de precisión | Exponer necesidad, impacto y alternativa dentro del alcance; obtener decisión antes de implementarlo. |
| Imposibilidad demostrada de una ruta bajo las restricciones | Registrar evidencia y bloquear esa ruta; no sustituirla por otro producto. |
| Mejora no necesaria para tokens y tiempo por actividad | Dejar fuera; no implementarla. |

No usar “es más fácil así” como justificación para cambiar de interfaz, convertir la clasificación en manual o rebajar la exactitud prometida.

## 12. Estado vigente y siguiente acción — plan OTel v1.3

| Elemento | Estado al entregar esta edición |
|---|---|
| Fuentes públicas | Evidencia documental previa conservada; no revalidada en esta edición. No hay nueva afirmación de capacidad del host. |
| OTel v1.1 / R-OTEL-01–03 | Review APROBADO y P1–P3 aprobadas; hash histórico `e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`. No se reabren. |
| P4 / plan OTel v1.3 | Organización aprobada; R-OTEL-P4-01/02 corregidos, pendiente de revisión dirigida de esas correcciones. |
| Pasos 0–1 | Completados; no se repiten. |
| Paso 2 / Etapa C | BLOCKED: captura sin identidad/contadores completos, conciliación fallida y aislamiento insuficiente. Reintento v1.1 detenido antes de la tarea. |
| Contrato de aislamiento OTel v1.2 | Documento distinto de este plan; INFORMACIÓN INSUFICIENTE. F12-01–05/H-C1–5 conservados, sin nuevo ensayo autorizado. |
| Paso 3 / atribución automática | No ejecutado; depende de captura PASS y evidencia de marcas/acciones. P4 no evita esa dependencia. |
| Componentes anteriores | S01–S03/H01/H02/A01–A03 cerrados; recibos, cálculo e histórico reutilizables, sin integración automática OTel demostrada. |
| Spec, nuevas slices e implementación OTel | No formalizadas/ejecutadas por esta edición. |

**Próxima acción única:** revisar el plan OTel v1.3 aplicando
`04_REVISAR_PLAN.md`, únicamente sobre R-OTEL-P4-01/02 y los efectos directos de
sus correcciones. El contrato de aislamiento v1.2 es una dependencia pendiente;
la revisión no debe convertirlo en aprobado ni autorizar un ensayo. No se inicia
otra ronda en este encargo de planificación. P1–P4 ya están aprobadas y no se
vuelven a solicitar; el review técnico no equivale a permiso de implementación.

**Recorrido condicionado para implementar P4**, integrado en los pasos existentes:

| Bloque de trabajo futuro | Entrada / criterios | Cambio mínimo y resultado | Comprobación / condición de finalización |
|---|---|---|---|
| Revisar correcciones documentales | Plan v1.3, findings P4 y evidencia; AC04/06/09 | Verificar únicamente aprobaciones consistentes y propietario contable único | Cerrar o mantener R-OTEL-P4-01/02 por evidencia, sin revisar de nuevo los cierres ajenos |
| Resolver captura (Paso 2) | Contrato de aislamiento revisado, viabilidad y permiso propio; AC02/06/11 | Comprobación acotada de aislamiento y luego captura, sin clasificar | Identidad, contadores, conciliación, pérdida y reversión PASS; bloqueo explícito si falta evidencia |
| Probar bloques (Paso 3) | Captura PASS, contrato de marcas y permiso propio; AC01–05/10/12/13 | Conectar productor mínimo con secuencia prevista/observada | Transición y acciones completas enlazadas; sin esa prueba no cerrar spec dependiente |
| Formalizar (Paso 4) | Evidencia de pasos 2–3 y alcance aprobado; AC09 | Definir campos/versiones y slices de implementación, sin migrar pasado | Contrato compatible que distingue plan, ejecución y revisión |
| Integrar y validar (Pasos 5–7) | Spec y autorización de implementación; AC01–13 según §1.1 | Extender productor/recibos/reportes existentes y pruebas afectadas | Conciliación, fixtures P4, histórico preservado; simulación no sustituye integración |
| Aceptar (Paso 8) | Validación previa y caso autorizado antes de medir; P3/AC13 | Comprobar entrega habitual completa, sin etiquetas manuales | Todos los criterios §10 con evidencia; mezcla/faltantes no se eliminan para pasar |

**Incertidumbre crítica:** P4 simplifica la intención conocida de cada bloque,
pero todavía no demuestra límites de consumo separables ni cobertura completa.
Si una respuesta cruza actividades, su total sigue mixto. Si el host no aporta
identidad/cobertura, se bloquea el alcance dependiente. No se añade un turno por
categoría ni se asignan tokens según la etiqueta para forzar P3.

**Routing documental:** N2 por contrato de medición; hereda BALANCED / Medium,
fallback del catálogo canónico. Switch Benefit LOW para esta edición acotada;
configuración efectiva unknown. Revisión dirigida: estrategia de review vigente
en STATE. No se cambia modelo, router ni launcher.

**Cambios v1.2 → v1.3:** D4/D5 y §5 reconocen P1–P4 ya aprobadas; §5.2.1 fija
propietario contable único, estado compartido no aditivo y tratamiento temporal;
§6.1/paso 6 conservan esa semántica en histórico/JSON/texto; paso 7 y §10 agregan
la comprobación dirigida. No cambian categorías, P3, dependencias ni alcance de
implementación. Criterios, reviews, contratos de piloto y cierres históricos
quedan intactos. R-OTEL-01–03 permanecen cerrados para v1.1.

### Instrucción para continuar

> En Quiver, revisá únicamente el plan OTel v1.3 de Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md aplicando 04_REVISAR_PLAN.md, limitado a R-OTEL-P4-01, R-OTEL-P4-02 y los efectos directos de sus correcciones. Verificá que D4/D5 y §5 conserven P1–P4 ya aprobadas, y que una unidad indivisible compartida entre bloques iguales tenga un solo propietario aditivo y coincida en JSON, texto, detalle y totales. Leé PROJECT_STATE.md y STATE.md, OTEL_PLAN_REVIEW.md, EVIDENCE.md y HANDOFF.md de project-work-activity-attribution. Conservá R-OTEL-01–03 cerrados y todos los cierres anteriores. Considerá OTEL_PILOT_CONTRACT_v1.2.md como dependencia pendiente, sin darlo por aprobado. Registrá el resultado y una única siguiente acción. No corrijas el plan, implementes, formalices slices, ejecutes pilotos, leas sesiones o credenciales, instales dependencias, delegues ni cambies configuración, router o launcher. No publiques ni hagas commit.

## 13. Fuentes primarias

Consultadas el **26 de septiembre de 2026**. Las direcciones de la documentación de Codex consultadas redirigen actualmente a ChatGPT Learn. Las referencias de código en `main` son evidencia documental, no fijan la versión de tu instalación.

**[S1] OpenAI — Advanced Configuration.** Secciones de observabilidad, eventos y catálogo de métricas.  
`https://developers.openai.com/codex/config-advanced/`

**[S2] OpenAI — Configuration Reference.** Ajustes de exportadores OTel y registro de prompts.  
`https://developers.openai.com/codex/config-reference/`

**[S3] OpenAI — Código de telemetría de sesiones.** Campos de uso registrados al completar respuestas.  
`https://github.com/openai/codex/blob/main/codex-rs/otel/src/events/session_telemetry.rs`

**[S4] OpenAI — Nombres de métricas en Codex.** Constantes de tokens y duración de turno.  
`https://github.com/openai/codex/blob/main/codex-rs/otel/src/metrics/names.rs`

**[S5] OpenAI — Reasoning models.** Objeto `usage` y desglose de razonamiento dentro de los tokens de salida.  
`https://developers.openai.com/api/docs/guides/reasoning`

**[S6] OpenAI — Hooks.** Eventos soportados, identificadores, herramientas observables, respuestas y diferencias entre la documentación de versión y esquemas en `main`.  
`https://developers.openai.com/codex/hooks/`

**[S7] OpenTelemetry — Collector.** Responsabilidades del componente y diferencias de madurez entre componentes.  
`https://opentelemetry.io/docs/collector/`

**[S8] OpenTelemetry Collector — File Exporter.** Escritura a archivos, estabilidad declarada, append y rotación.  
`https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/main/exporter/fileexporter/README.md`

**[S9] OpenTelemetry — OTLP Specification.** Alcance de las garantías de entrega y posibilidad de duplicados.  
`https://opentelemetry.io/docs/specs/otlp/`


**[S10] OpenAI — Implementación de la herramienta de plan.** Restricción de `update_plan` en Plan mode en el código consultado.  
`https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/handlers/plan.rs`

**[S11] OpenAI — Esquema de la herramienta de plan.** Campos `step`, `status` y estados del paso.  
`https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/src/tools/handlers/plan_spec.rs`

---

**Decisión de diseño central:** observar el trabajo que ya realizás y agregar únicamente la instrumentación indispensable. Primero demostrar captura y atribución automática; después integrar persistencia y reporte. Nunca cambiar el requerimiento para hacer que la prueba dé bien.
