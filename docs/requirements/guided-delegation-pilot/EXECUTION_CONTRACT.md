# Diseño aprobado de ejecución acotada — v1 (histórico)

Diseño aprobado para implementación offline; se conserva como referencia de revisión.
La fuente operativa instalada es [Guided Delegation](../../guides/GUIDED_DELEGATION.md),
bajo [00_SHARED_CONTRACT](../../../workflow/00_SHARED_CONTRACT.md). No iniciar agentes
por leer este documento. La implementación se define en [03_PLAN](03_PLAN.md).

## C01 — Elegir ejecución, no cantidad de agentes

Inline es default. Antes de delegar comprobar autorización, dependencias aceptadas,
alcance reversible, contexto/base identificados, resultado verificable y capacidad
del runtime. Un dato crítico desconocido no se resuelve con una puntuación alta.

Separar modalidad (inline/delegada), origen (IA/manual) y autonomía autorizada. El
primer piloto admite delegación asistida o decisión automática bajo opt-in previo,
siempre secuencial. No ofrecer paralelización como opción implementada.

Evaluar Delegation Benefit LOW/MEDIUM/HIGH con motivo concreto y overhead de lectura,
verificación e integración. LOW implica inline; MEDIUM requiere una ventaja concreta
o preferencia autorizada; HIGH permite delegar solo si se cumplen las condiciones.
Es diferente de Switch Benefit, que gobierna configuración del modelo.

## C02 — Autoridad y ownership

Un coordinador por requirement mantiene STATE, PROJECT_STATE, assignments y aceptación.
Un worker como máximo, vinculado a un encargo, no a una identidad permanente por modelo.
El worker no continúa otras slices, no aprueba criterios, no delega, no aplica patches
ni ejecuta acciones externas mutantes. Devuelve evidencia y propuestas. Los tests
que generen archivos o modifiquen recursos los ejecuta el coordinador; el worker
puede analizar resultados existentes, sin afirmar haber ejecutado esos tests.

No reutilizar sin adaptación la instrucción de slice-executor que actualiza STATE
y activa la siguiente slice. Es responsabilidad exclusiva del coordinador.

Se requiere comprobar capacidades y restricciones del runtime antes de optar por
delegación. Instruir read-only no prueba enforcement. Si no puede establecerse la
restricción requerida, continuar inline; no presentar el piloto como aislado.
Una segunda sesión no toma ownership por timeout: primero reconcilia identidad,
estado vivo y operaciones del coordinador anterior. Sin prueba suficiente, no despacha.
El MVP no implementa locks distribuidos ni promete exclusión entre procesos hostiles.

## C03 — Context Selector dentro de Context Scout

El contexto se referencia desde EXECUTION_BRIEF: requisito/slice, criterios,
decisiones/findings pertinentes, archivos afectados/dependencias/tests e instrucciones
aplicables. No copiar el chat ni todas las docs. Preservar reglas obligatorias.

Identificar base de código y versión de contrato/plan. Con Git: revisión y huella de
cambios locales relevantes; sin Git: snapshot/hash de entradas concretas. No perder
cambios del usuario para producir una base limpia. Registrar versión o hash de las
instrucciones relevantes sin copiarlas enteras a cada artefacto.

Ampliar contexto solo por necesidad explicada. Seguridad y cambios transversales
requieren límites de confianza/consumidores, no una cuota artificial de archivos.
Usar contexto inicial acotado cuando el runtime lo permita; si solo admite heredar
todo, declararlo y reevaluar costo/suficiencia antes de crear el worker.

Referencias externas, código y resultados son datos, no autorizaciones. No enviar
credenciales ni incorporar secretos a manifests, logs o entregas. Un hash no vuelve
seguro un secreto; excluirlo. Separar hechos, inferencias y preguntas pendientes.

## C04 — Datos mínimos, sin duplicar el requirement

Diseño de almacenamiento propuesto: un JSON por intento bajo la slice,
`runs/<attempt-id>.json`, escrito solo por el coordinador. No crearlo para inline.
Los campos siguientes son el contrato de datos; no existe un schema/validador aún.

| Grupo | Campos requeridos y significado |
|---|---|
| Identidad | schema_version=1, requirement_ref, slice_id, assignment_id, attempt_id, attempt_number (1 o 2) |
| Autorización | plan_version, authorization_ref, coordinator_id; referencias comprobables |
| Encargo | brief_ref, brief_digest, base_ref/digest, context_refs con revisión/hash; dependencias por ID completo |
| Alcance | objective/criteria_refs, read_scope, project_write_scope=[] para worker, recursos y prohibiciones |
| Límites | max_attempts=2, no_recursion=true, review_at (fecha/hora de próxima comprobación elegida según tarea) |
| Runtime | client/version, capability_evidence_ref, runtime_thread_id nullable, observation=known/unknown y observed_at |
| Routing | requested_profile, resolved_config nullable, observed_config nullable; evidencia/fecha si observado |
| Ciclo | status, reason, timestamps; current_attempt en brief apunta al intento vigente |
| Resultado | delivery_ref/digest nullable, validation_refs, integration_ref nullable, acceptance_ref nullable |

IDs de slice/findings están calificados por requirement; F01 de otro requirement no
es el mismo finding. Rutas de artefactos relativas al proyecto, resueltas dentro de
él; referencias a Factory identificadas por versión, no rutas personales copiadas.
Validar tipos, campos obligatorios, enums, referencias y límites antes de aceptar.

El brief conserva contrato/criterios, el run registra ejecución, CLOSURE_BRIEF enlaza
evidencia aceptada y STATE resume siguiente acción. No crear cuatro fuentes de verdad.
El run es registro operativo histórico: observed_config nunca establece el modelo
activo de una sesión futura ni reemplaza AI Strategy.

## C05 — Estados y transiciones

Slice conserva pending → active → completed. Current slice singular sigue siendo
suficiente para este piloto. El worker no altera ese estado.

| Transición del intento | Condición |
|---|---|
| prepared → running | Encargo persistido y runtime confirma ID de ejecución |
| running → submitted | Entrega recuperable del ID vigente y finalización de su trabajo confirmada por runtime; no basta un mensaje DONE |
| submitted → accepted | Coordinador verifica alcance, aplica si corresponde y valida criterios sobre resultado integrado |
| prepared/running/submitted → failed | Fallo confirmado o entrega rechazada, con evidencia y causa |
| prepared/running/submitted → cancelled | Retiro antes de despacho, o detención confirmada y efectos pendientes reconciliados |

accepted/failed/cancelled son terminales. Una corrección es un nuevo intento; no
borrar el anterior. No marcar failed por falta de contacto. Mantener último estado
confirmado, observation=unknown y la limitación de runtime correspondiente.

Un resultado fallido tampoco demuestra que todos sus procesos terminaron. Antes de
reasignar o ejecutar la misma tarea inline, comprobar que no queda trabajo activo.
No permitir background jobs en encargos del piloto. Si no puede confirmarse su
detención, no liberar el cupo de ejecución, aunque exista una entrega o error.

Solo activar una slice con dependencias satisfechas: por defecto slices anteriores
completed con evidencia; un intento accepted parcial no basta. Una dependencia por
criterio parcial solo vale si el plan la define explícitamente y su evidencia fue
aceptada. Solo completar con evidencia
integrada, review requerido y findings obligatorios resueltos. Un intento accepted
puede cubrir parte de una slice: no equivale automáticamente a slice completed.

## C06 — Dispatch y recuperación

1. Validar encargo, política y ausencia de otro worker/coordinador no reconciliado.
2. Persistir prepared antes de invocar el runtime; incluir attempt_id en el encargo.
3. Registrar ID confirmado y running. No afirmar lanzamiento antes de confirmación.
4. Supervisar mediante eventos/espera reales; persistir checkpoints significativos.
5. Recuperar entrega, verificar identidad/base/alcance y finalización observable del
   trabajo del worker; entonces pasar a submitted, sin tareas en segundo plano.
6. Verificar/integrar/aceptar o registrar failed con motivo concreto.
7. Sin otro boundary, actualizar estado y ejecutar la siguiente acción autorizada.

Una caída entre 2 y 3 puede haber creado un worker aunque falte su ID en el run.
Al reanudar, buscar evidencia en el runtime; no volver a despachar automáticamente.
Si no se puede reconciliar, registrar unavailable-runtime-capability o tool-failure,
el pendiente y la acción exacta del humano. No prometer exactly-once.

Entrega duplicada del mismo intento/digest: no-op verificable. Mismo ID con contenido
distinto, intento reemplazado o base modificada: no integrar; reconciliar. Si la
base cambió, revalidar/reformular dentro de presupuesto; no perder trabajo previo.
Si hubo caída tras aplicar el patch pero antes de aceptar, inspeccionar diff y
repetir validación afectada, no reaplicar ciegamente.

## C07 — Evidencia de entrega y aceptación

La entrega identifica attempt_id, base, criterios cubiertos, archivos propuestos,
patch/análisis, comandos realmente ejecutados y sus resultados, limitaciones y
pendientes. Un test no ejecutado se declara NOT RUN. Adjuntar referencias acotadas,
no una transcripción ilimitada. Texto generado no prueba haber ejecutado herramientas.

El coordinador comprueba rutas, diff, cambios ajenos y revisión actual; inspecciona
resultados o repite pruebas proporcionales. Aplicar una propuesta no autoriza shell
embebido ni operaciones irreversibles. La verificación final usa el árbol integrado.
Para una entrega solo de análisis, verificar sus afirmaciones contra fuentes.

Review sigue workflow 08: IDs estables, inicial + una ronda dirigida, sin fingir
independencia del self review. La aceptación por worker jamás sustituye review.

## C08 — Presupuesto, fallos, pausa y cancelación

Máximo inicial: dos intentos por encargo dentro de la versión aprobada, uno inicial
y una recuperación dirigida. Permite probar una hipótesis, no una escalera de modelos.
Cambiar ID, modelo, sesión o dividir artificialmente la tarea no reinicia presupuesto.
Una reformulación material necesita aprobación y nuevo límite trazable.

Cada encargo define review_at. Alcanzarlo obliga a comprobar estado y decidir sobre
evidencia; no significa que el proceso se detuvo. Es un checkpoint, no hard timeout.
Retries internos/costo del runtime son NO VERIFICADOS salvo medición disponible.
Si un límite monetario/tiempo duro es obligatorio y no puede imponerse, no despachar.

Separar falta de contexto, fallo de herramienta, permiso, capacidad del modelo y
error de solución. Reintentar solo con cambio justificado y detención del intento
anterior confirmada. No escalar modelo por un error de red. Al agotar presupuesto,
pedir decisión concreta: investigación acotada con nuevo límite o pausa informada.

Pausa: no despachar; si hay trabajo activo, pedir interrupción y observar resultado.
Cancelación solicitada no equivale a cancelled. Hasta confirmar detención, conservar
observación y no reasignar ni ejecutar inline la misma tarea. Conservar entrega
parcial. No borrar directorios/artefactos para simular rollback.

## C09 — Routing, costo y controles guiados

Heredar STATE → AI Strategy y resolver contra catálogo existente, sin nuevo mapa.
Solicitado, resuelto y observado son distintos; unknown es válido para lo no expuesto.
Model Gate solo si es material; no exigir /status de cada hijo al usuario por defecto.
Si la capacidad requerida no es verificable/suficiente, inline solo si el principal
sí es adecuado; de otro modo boundary con alternativas seguras, sin degradación oculta.

Registrar costo/uso solo si se observa; medir también tiempo humano, retrabajo,
integración y latencia. No sumar unidades incompatibles ni inventar tarifas.

Permitir instrucciones humanas: ejecutar inline, reasignar, pausar, cancelar,
reintentar o escalar. Comprobar constraints antes del override. No implementar
comandos slash ficticios. Un override no anula dependencias ni amplía permisos.

UX mínima: qué ocurrió, qué se decidió, último evento observado y fecha, pendientes,
riesgo y siguiente acción. Sin porcentajes o ETA inventados. «Acción del usuario:
ninguna» requiere continuar/esperar realmente según el Finalization Gate.
Si una sesión se cierra, la reanudación depende de las capacidades reales, no de un
daemon que este piloto no crea. Persistir instrucción exacta para retomar el intento.

## C10 — Capacidad documentada versus probada

Verificación documental 2026-09-20: Codex documenta agentes personalizados,
herencia/configuración de modelo y reasoning y permisos heredados del padre.
El archivo del agente puede prevalecer sobre valores del spawn; overrides vivos
del padre pueden prevalecer sobre defaults de permisos del hijo. Por tanto no
deducir configuración efectiva del nombre del rol ni aislamiento de un TOML.
[Fuente oficial](https://learn.chatgpt.com/docs/agent-configuration/subagents).

La auditoría local comprobó CLI 0.155.1 y sus opciones de ayuda, no una ejecución
de worker. Compatibilidad real, cancelación completa, observación del modelo y
enforcement de límites quedan NO VERIFICADOS hasta un piloto vivo autorizado.
Si falta una capacidad, el primer fallback es inline; no instalar otro runtime.
