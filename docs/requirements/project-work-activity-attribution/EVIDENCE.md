# Evidencia A01–A04 y preparación Kev — 2026-09-25

## Alcance ejecutado

Se implementaron recibos de actividad privados, clasificación automática con
transporte Kev artificial e histórico v2 por actividad. Archivos principales:
`scripts/lib/work_activity.py`, `scripts/lib/plan_usage.py`,
`templates/usage/ACTIVITY_EVENT.schema.json`, `tests/test_work_activity.py` y
`tests/work_activity_kev_dataset.py`. La guía `PLAN_USAGE.md` incluye el flujo
offline. Durante A01–A03 no se abrió ningún JSONL real ni se instaló/ejecutó
Kev; la preparación y el intento A04 posteriores se documentan abajo.

## Validación reciente

| Comprobación | Resultado |
|---|---|
| `python3.14 -I -B tests/test_work_activity.py` | PASS, 11 tests, fixtures artificiales A01–A03 y preparación de dataset A04 |
| `python3.14 -I -B tests/test_plan_usage.py` | PASS, 46 tests, regresiones afectadas de ledger, lifecycle, costo e historial v1 |
| `python3.14 -B -m py_compile scripts/lib/plan_usage.py scripts/lib/work_activity.py tests/test_work_activity.py tests/work_activity_kev_dataset.py` | PASS |
| `git diff --check` | PASS |
| Inspección dirigida de rutas reales, credenciales, canarios y espacios finales | PASS; el único canario está en una aserción negativa de test y no queda en ledger |

Los oráculos prueban que una respuesta mixta no se suma dos veces, que una
relación incompleta termina en `unassigned`, y que `activity-history` sigue
funcionando luego de eliminar la fuente artificial. La colección A04 genera 100
casos de desarrollo y 200 de evaluación con datos sintéticos, pero no se usó
para afirmar precisión de Kev.

## Preparación local de Kev

Con autorización separada, la fuente oficial se clonó en `/private/tmp/kev` y
su entorno aislado instaló Python 3.13.14 y el extra `serve`. Se inició
`jaredpalmer/kev-4b` en loopback. La comprobación read-only
`GET http://127.0.0.1:8009/v1/models` respondió `200 OK` y declaró:

- `run`: `jaredpalmer/kev-4b`;
- base: `Qwen/Qwen3.5-4B-Base`;
- dispositivo/backend: MPS / MLX, `bfloat16`;
- al momento de preparar el endpoint: `batches.requests`: `0` y
  `prefix_cache.cached_states`: `0`.

No se leyó una sesión real y no se cambió ningún archivo de router, launcher ni
configuración global.

## A04 / T14 — bloqueada por timeout

Con la autorización A04 se enviaron exclusivamente estados del corpus sintético
congelado a `http://127.0.0.1:8009`. El cliente real `kev_classify` agotó su
timeout fijo de 5 s en dos intentos: no recibió cuerpo de respuesta, señales ni
`usage`. Una consulta directa de diagnóstico también quedó en cola durante el
calentamiento; el endpoint terminó reportando `batches.count: 2`,
`batches.requests: 3`, `queued: 0`, `prefix_cache.hits: 2` y
`cached_states: 1`. Esto confirma que Kev procesó solicitudes iniciales, pero
no proporciona una respuesta utilizable por el cliente dentro de su contrato.

No se ejecutaron los 100 casos de desarrollo ni los 200 de evaluación: sin una
respuesta recibida no es posible fijar política ni calcular precisión, cobertura,
abstención, matriz de confusión, p50/p95 o consumo propio de Kev. Todos esos
valores permanecen **desconocidos**. T14 no pasó y Kev no queda habilitado.
No se modificó el timeout, el clasificador, umbrales, checkpoint o dataset; no
se ejecutó A05.

## Corrección autorizada — timeout 180 s

Se cambió exclusivamente `KEV_TIMEOUT_SECONDS` de 5 a 180 en
`scripts/lib/work_activity.py`. La regresión afectada
`python3.14 -I -B tests/test_work_activity.py` pasó 11/11 y `py_compile` pasó.
El endpoint siguió declarando `batches.count: 4`, `requests: 4`, `queued: 0`.
La única ejecución de control del mismo caso sintético con el nuevo límite no
emitió una respuesta ni generó un batch nuevo verificable. Por ello no se lanzó
el corpus completo: T14 continúa sin métricas válidas y Kev permanece
deshabilitado. Diagnosticar el proceso/latencia del servidor requiere permiso
propio.

## Límites vigentes

## Diagnóstico autorizado — throughput no viable

La muestra de 5 segundos del PID de Kev mostró el event loop y la hebra del
modelo esperando, no un deadlock. El código local de Kev confirma que en Metal
`probs_batch` procesa una solicitud por vez. Con una sesión persistente, el
cliente Quiver recibió el caso sintético `dev-feature-001` en `176445.453 ms`.
Sus señales quedaron debajo del umbral 0.9: `feature` 0.3911, `bug` 0.4430,
`test` 0.4876, `explanation` 0.3625 y `documentation` 0.3528.

El endpoint posterior declaró `batches.count: 6`, `requests: 6`, `queued: 0`.
A ese ritmo serial, 300 casos requerirían aproximadamente 52,934 s (14.7 h);
es una inferencia de una muestra, no una medición T14. Además,
`kev_classify` no retorna el objeto `usage`, por lo que el consumo propio no
puede medirse sin un cambio adicional no autorizado. No se envió el corpus
completo, no se cambiaron preguntas, umbral, checkpoint ni dataset, y A05 no se
ejecutó.

`kev_inferred` se etiqueta `unvalidated`; sus señales no asignan fracciones de
tokens ni representan tokens del agente. USD y tiempo activo permanecen unknown.
La instrumentación de actividad no prueba que el host real produzca manifests
completos o links respuesta→acción. Eso requiere A04/A05.

## Paso 0 OTel — auditoría de solo lectura 2026-09-28

### Alcance y preservación

Se ejecutó únicamente el Paso 0 autorizado: inspección del entorno herdr/Codex,
de la configuración pertinente por nombres de claves y de los componentes de
Quiver reutilizables. No se abrió, listó ni leyó una sesión o conversación de
Codex; no se leyó `auth.json` ni valores de configuración; no se instalaron
dependencias, no se iniciaron chats/pilotos y no se cambió router, launcher,
configuración, código o datos. Tampoco se publicó ni se hizo commit.

El plan permanece en SHA-256
`e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`.
Los cierres S01–S03, H01/H02 y A01–A03 no se repitieron.

### Inventario observado

| Elemento | Evidencia de lectura | Resultado y límite |
|---|---|---|
| Herdr | `herdr --version`; `herdr config check` | Herdr `0.8.0`; la configuración pertinente es válida. Es un binario nativo y no se alteró. |
| Codex disponible en esta auditoría | resolución de PATH, `codex --version`, inspección del enlace del ejecutable | PATH resolvió `/opt/homebrew/bin/codex`, enlace al paquete local de Codex, versión `0.157.1`. Esto sustituye la observación histórica `0.157.0` solo para esta shell; no prueba qué binario lanza una sesión persistente de herdr. |
| Relación herdr → Codex | `herdr --help`, configuración por nombres de claves, `herdr integration status` | Herdr reconoce integraciones de agentes, pero la configuración no declara una ruta de Codex. La integración de estado `codex` figura como **not installed**. Sin inspeccionar una sesión/proceso vivo no hay evidencia del ejecutable efectivo ni de marcas emitidas. |
| Configuración de telemetría | búsqueda acotada de claves OTel/telemetría en las configuraciones pertinentes; valores omitidos | No se encontró una clave OTel/telemetría configurada. `codex features list` mostró `runtime_metrics` experimental y desactivada; no equivale a exportación de trazas, identidad de respuesta ni contadores. |
| Estado automático de actividades | búsqueda acotada en Quiver y estado de integración de herdr | No se halló productor automático de recibos ni hook de estado Codex instalado. El repositorio contiene el contrato de recibos, no la integración viva que los genera. |
| Persistencia reutilizable | lectura de `scripts/lib/plan_usage.py` y `scripts/lib/work_activity.py` | Hay binding prospectivo, ledger privado, deduplicación, recibos con `response_id`, acciones y límites temporales, `snapshot_activity_report`, `activity_history_report` y salida JSON/texto por `project_id`/`work_id`. `work_activity.py` recibe el recibo desde un llamador; no lo captura del host. |

### Pendientes D1–D7 tras Paso 0

| Pendiente | Estado tras la auditoría | Evidencia o condición restante |
|---|---|---|
| D1 — ejecutable y versión efectivos | Parcial | Se identificaron herdr 0.8.0 y Codex 0.157.1 del PATH, pero falta demostrar el ejecutable que herdr usa dentro del ámbito explícito de un piloto. |
| D2 — representación de bloques | Parcial | Existen recibos y clasificación conservadora, pero no una fuente automática de bloques/cambios. |
| D3 — tiempo | Resuelto en la regla, no observado | El diseño conserva transcurrido y duración de herramienta separados; tiempo activo es `unknown`. Los límites reales se verifican únicamente en piloto. |
| D4 — agrupaciones y procedencia | Resuelto funcionalmente, no integrado | P1/P2 aprobados; las reglas existentes no sustituyen la procedencia automática que falta. |
| D5 — primera llamada, transiciones y cierre | No demostrado | No hay fuente de marcas ni vínculo respuesta→acción probado. |
| D6 — persistencia y salida | Parcial, reutilizables localizados | Ledger y reportes existentes son candidatos. No hay Collector configurado, ni se autorizó elegir dependencia, servicio o cambio de configuración. |
| D7 — cobertura de todo el consumo | No demostrado | No hay referencia/manifiesto de finalización cualificado. No se leyó una sesión para intentar inferirlo. |

### Conclusión de Paso 0

La auditoría cumple su salida de inventario y conserva un límite claro: hay
persistencia y presentación reutilizables, pero todavía no hay fuente demostrada
de captura completa ni de atribución automática. El siguiente bloque requiere
un contrato documental de piloto que fije el ámbito, campos permitidos, criterio
de completitud, cambio mínimo y reversión antes de pedir permiso para medir.

## Paso 1 OTel — contrato documental del piloto 2026-09-28

Se preparó [OTEL_PILOT_CONTRACT.md](OTEL_PILOT_CONTRACT.md), versión v1, sin
iniciar una sesión, receptor o piloto. El contrato fija dos etapas con gates
separados: captura real en Paso 2 y atribución automática en Paso 3. La próxima
autorización solicitada cubre únicamente la primera.

Evidencia nueva de solo lectura:

- OpenAI documenta que `otel` en configuración local al proyecto es ignorado;
  el contrato usa overrides de una sola ejecución y no edita configuración global.
- OTel puede exportar por OTLP/HTTP JSON con prompts redacted, metadatos de
  conversación/versión y contadores en `response.completed`.
- Codex documenta hooks de sesión/turno/herramienta, pero excluye herramientas
  alojadas y admite caminos especializados fuera de cobertura; no se usan como
  prueba única de completitud.
- Herdr 0.8.0 permite iniciar el ejecutable canónico `codex` en una pane y pasar
  argumentos adicionales. No se invocó ese comando.
- No hay `otelcol` local. Python 3.9.6 permite proponer un receptor temporal sin
  dependencias; Docker se detectó pero quedó expresamente excluido.

Fuentes oficiales consultadas el 2026-09-28:

- `https://developers.openai.com/codex/config-reference`
- `https://developers.openai.com/codex/config-advanced`
- `https://developers.openai.com/codex/hooks`

No se leyeron sesiones, conversaciones, credenciales o valores de configuración;
no se modificaron launcher/router/configuración ni código ejecutable. El plan
OTel v1.1 conserva su hash aprobado. Validación de este paso limitada a
consistencia documental; no constituye evidencia de captura o atribución.

## Etapa C/Paso 2 OTel — ejecución BLOCKED 2026-09-28

### Alcance ejecutado

Se ejecutó una sola vez la lista cerrada §9 de
[OTEL_PILOT_CONTRACT.md](OTEL_PILOT_CONTRACT.md): receptor Python temporal en
`127.0.0.1:4318`, fixture artificial de tres líneas, una pane herdr nueva y una
tarea Codex de lectura sin edición. Herdr confirmó inicio, transición de trabajo,
retorno a `idle`, salida al shell y cierre de la pane. El proceso efectivo fue el
binario nativo de Codex bajo `/opt/homebrew/lib/node_modules/@openai/codex/`,
versión `0.157.1`; no se cambió modelo ni se afirma configuración efectiva por
ese dato.

La sintaxis de los cinco overrides pasó `codex --strict-config ... --help` con
exit `0`. El receptor requirió acceso del host para abrir loopback; el primer
intento dentro del sandbox terminó antes de escuchar con `PermissionError`. El
segundo informó `READY 127.0.0.1:4318`. No se usaron Docker, dependencias, hooks,
red adicional, otra tarea o Paso 3.

### Evidencia sanitizada

| Evidencia | Resultado |
|---|---|
| Fixture | 3 líneas; SHA-256 `4fdbc441ea7b546100e086ac1e4fc5ae6749b7314311c99db05be450eca12996` |
| Receptor | SHA-256 inicial `6ec006007131a85984e7033580d5f8fdfa817942aa82b39df72b8673c2ac230b`; comprobador corregido `9514efb746cd40c4b58587eb4279597b3e9c2937d72f02978e22b103e06de494` |
| Exportación | 40 eventos sanitizados, 13.499 bytes; SHA-256 `4ac42088a364ab274e5ee9e17e27214ce51a029e51b37557df9c433c0c563297` |
| Privacidad | Cero coincidencias para nombre/contenido del fixture, texto de la tarea, bearer/authorization o patrones de credencial comprobados. Revisión dirigida, no garantía universal |
| Referencia permitida | 2 respuestas; 1 session, 1 thread, 1 turn y 2 response IDs. SHA-256 `8cfbe0f2cc8ccbe1820c44c31805d1148dc4dd5aaf1c6e5d2d4ad763e4cd4f41` |
| Consumo de validación | entrada 46.271; cached input 33.280; salida 127; reasoning output 14; total 46.398. No se suma a trabajo de producto |
| OTel `response.completed` | 5 eventos; 2 conversation IDs; 0 response IDs; campos de token observados limitados a cached y cache-write |
| Conciliación | exit `2`, `incomplete`: referencia 2, OTel 5, identificadas 0, identidad completa false, contadores completos false, exact match false |
| Prueba negativa | una unidad OTel eliminada en memoria: 4 frente a 2; exit `2`, `incomplete`. No cualifica detección porque el original ya era incompleto |

El comprobador temporal informó inicialmente `counters_complete=true` sobre un
mapa vacío. Se corrigió únicamente esa condición y el alias observado
`cached_token_count`; la repetición sobre los mismos artefactos produjo
`counters_complete=false`. No se abrió otra sesión ni se repitió la tarea.

### Bloqueos observados y reversión

El `conversation.id` de la referencia coincide con uno de los dos identificadores
OTel. El otro se conservó solo como digest
`9367c14f9bf876c1a5774277ddf2f6e521d1d08d85b45145b44f4277ddf2f6e77`:
no se buscó su archivo, no se lo identificó y no se leyó contenido. Esto demuestra
que el daemon compartido contaminó la captura con otra conversación y viola el
aislamiento requerido, aun cuando el saneamiento evitó persistir contenido.

Codex agregó transitoriamente el bloque de confianza de
`/private/tmp/quiver-otel-capture-v1/fixture` al TOML del usuario. Se eliminó solo
ese bloque y la búsqueda exacta posterior no encontró la ruta. La pane, Codex y
el receptor quedaron detenidos; no hay `.codex` de proyecto. El árbol temporal
se elimina después de registrar hashes y resultados.

**Veredicto de Etapa C: BLOCKED.** No hay identidad ni contadores OTel completos,
la referencia no concilia, la pérdida no puede cualificarse y el transporte con
daemon compartido excedió el ámbito de una sesión. Paso 3 permanece no autorizado
y técnicamente bloqueado.

## Reintento aislado OTel v1.1 — BLOCKED antes de la tarea 2026-09-28

### Preflight y corte

La autorización permitía una sola ejecución y exigía detenerse sin consumir la
tarea ante cualquier fallo de proceso, trust o configuración. La comprobación
estática `codex --strict-config ... --help` terminó con exit `0`; hash y stat del
TOML permanecieron iguales en ese punto. Se prepararon receptor Python estándar
y fixture de tres líneas, se abrió loopback `127.0.0.1:4318` y herdr creó una
pane temporal.

El proceso vivo fue Codex 0.157.1 nativo con `--no-daemon`, sandbox `read-only`,
approval `never`, override efímero de trust y los cinco overrides OTel exactos.
`herdr agent explain` informó estado `idle`, sin blocker visible y regla
`trust_directory` no coincidente. El control de configuración previo a la tarea,
sin leer ni mostrar valores, detectó una coincidencia exacta de la ruta temporal:

| Control | Antes de la pane | Antes de la tarea |
|---|---|---|
| SHA-256 de `~/.codex/config.toml` | `0e0bf7bb5e168f884d9b613b88838cf5b77141fac1644c939c78994517ddc7ab` | `00ebc16f41deb7f2daa67f17f31d5dbb93e8b313651bf9443ee5984fad6ba7e9` |
| stat `device:inode:size:mtime:ctime` | `16777234:339462915:14486:1790607370:1790607370` | `16777234:339503166:14574:1790608663:1790608663` |
| coincidencias de ruta v1.1 | 0 | 1 |

La tarea no se envió. La pane se cerró externamente sin teclas, el receptor se
detuvo con 6 requests, 12 registros recibidos/persistidos y cero errores, y no se
invocó el lector de referencia. Por ello no se leyó `session_meta`,
`token_usage_record`, contenido ni otra sesión. La prueba negativa quedó
correctamente no ejecutada.

### Evidencia temporal sanitizada y reversión

| Evidencia | Resultado |
|---|---|
| Receptor | SHA-256 `4486cd78c918f126a9e8d66381f4d00136b492f643a519358dab3394c103fde5` |
| Fixture | 3 líneas no vacías; SHA-256 `87a3c52b88cf5eeec4bff79b5f65de20adbdb2d79a7f78d93f996a319c42ff5f` |
| argv efectivo | SHA-256 `a34030ced3e0c62bdfe8e7ef7fbb0da4ce272ec45db470cbd681b4667e7af72b` |
| Exportación previa a la tarea | 12 eventos / 2.855 bytes; SHA-256 `6426344cf903283778424f4e2a9d244fcbaf0e1bd68e92d9bef81367c1592b59` |
| Allowlist persistida | `conversation_id_sha256`, duración, nombre/tipo de evento, servicio/versión, éxito, timestamp y uso |
| Privacidad dirigida | 0 coincidencias con nombre/contenido del fixture, tarea, bearer/authorization, password, secret, API key o transcript path |
| Referencia | no creada; ninguna sesión leída |
| Prueba negativa | no ejecutada: el original no alcanzó G-C1–G-C5 |

Pane, proceso Codex, receptor y árbol temporal quedaron ausentes; el puerto 4318
está libre. El TOML conserva la coincidencia v1.1 y su hash posterior es
`00ebc16f41deb7f2daa67f17f31d5dbb93e8b313651bf9443ee5984fad6ba7e9`.
No se editó porque el contrato exige autorización específica ante esa mutación.

**Veredicto: BLOCKED.** G-C1 falló antes de la tarea; G-C2 tiene evidencia
parcial de saneamiento; G-C3–G-C6 no se ejecutaron; G-C7 quedó incompleto solo
por la persistencia de trust. No hubo Paso 3, dependencias, Docker, red adicional,
cambios de router/launcher, publicación ni commit.

### Reparación dirigida autorizada

El usuario autorizó la única acción pendiente. Antes de escribir se comprobó
una sola tabla exacta para la ruta v1.1 y que su cuerpo contenía únicamente el
valor de trust esperado. Un intento más estricto se detuvo sin cambios al
comprobar que remover la tabla no reproducía el hash histórico.

Se respaldó el TOML mutado en
`~/.codex/backups/config.toml.quiver-otel-v1-1.20260928T165719Z.bak`, modo `0600`,
SHA-256 `00ebc16f41deb7f2daa67f17f31d5dbb93e8b313651bf9443ee5984fad6ba7e9`.
Después se eliminó atómicamente solo la tabla exacta. Resultado:

| Control | Resultado |
|---|---|
| coincidencias de `/private/tmp/quiver-otel-capture-v1-1/fixture` | 0 |
| SHA-256 actual | `536f8d4b5fba477f17f0a3857c5d58b304798fa71fed609ffd0c37c8877b96ce` |
| stat actual | `16777234:339544660:14490:1790614639:1790614639` |
| diferencia de tamaño frente al baseline | +4 bytes, conservados sin inspección/normalización |
| parser TOML independiente | no disponible localmente |
| Codex/piloto | no ejecutados |
| pane/puerto/árbol temporal | ausentes / libre / ausente |

La validación fue estructural: tabla única, cuerpo cerrado, remoción exacta,
hash del backup y ausencia posterior. No se mostraron otros valores ni secretos.
La configuración no volvió byte por byte al baseline y los gates históricos no
se recalifican. El residuo de trust quedó retirado; el reintento continúa
BLOCKED y consumido sin tarea enviada.

## OTel v1.2 — investigación de solo lectura 2026-09-28

Se investigó únicamente la capacidad de aislar confianza y configuración sin
iniciar Codex o herdr de forma interactiva, crear panes, iniciar sesiones,
leer/copiar credenciales ni instalar dependencias. Codex CLI local continúa en
`0.157.1`; herdr en `0.8.0`.

| Fuente | Hallazgo | Conclusión |
|---|---|---|
| `codex --help` local | `--profile` se describe como una capa `$CODEX_HOME/<nombre>.config.toml` sobre la configuración base. | No sirve para aislar la configuración personal. |
| Configuración avanzada oficial | `--profile` carga primero `~/.codex/config.toml` y luego el perfil. | Confirma que perfiles no resuelven la escritura de trust. |
| Binario Codex instalado, inspección estática | Reconoce `CODEX_HOME`, rutas de logs y referencias a autenticación almacenada o por entorno. | Es una señal de candidato, no prueba de comportamiento ni de autenticación segura. |
| `herdr agent start --help` | Documenta argumentos para el agente, sin una interfaz documentada para variables de entorno por agente. | No demuestra cómo propagar un home temporal desde herdr. |
| Documentación oficial de autenticación | Codex admite inicio con ChatGPT o API key. | Ninguna vía autoriza leer/copiar credenciales ni garantiza autenticación con home temporal. |

No se inspeccionaron archivos de autenticación ni valores de configuración. La
única alternativa candidata es una raíz temporal por `CODEX_HOME`, pero falta
evidencia primaria de tres condiciones: que reemplace la raíz completa, que herdr
la entregue al proceso y que la autenticación no requiera copiar o leer secretos.

El perfil temporal y el override de trust v1.1 quedan descartados. La confianza
global está fuera de alcance. Resultado: **INFORMACIÓN INSUFICIENTE** para otro
piloto. Contrato resultante:
[OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md).


## Plan OTel v1.2 — bloques por categoría dentro de las slices 2026-09-28

**Alcance:** edición del plan y continuidad, aceptada por «Dale, hazlo» como
respuesta a incorporar la organización propuesta. P4 aceptada, sin aprobación
inferida de review, spec, implementación, sesión o piloto. P1–P3 conservadas.

**Entradas verificadas:** estados vigentes, plan v1.1, criterios v2,
`work_activity.py` (recibos recibidos de un llamador; no captura del host),
contrato de aislamiento v1.2 y evidencia de Etapa C. No se consultaron sesiones,
credenciales, configuraciones externas ni fuentes web nuevas.

**Resultado documental:** plan OTel v1.2, SHA-256 `53ae25ef657d8549b54f325af34ba15073bb56d131d423f6572e2cba726deb64`.
§1.2 registra P4; §5.2.1 distingue categoría prevista, actividad observada y
consumo, con inicio/cierre, retornos, interrupciones y cobertura. §6.1/paso 4
vinculan slice/versiones/bloques sin alterar pasado. Pasos 3/7 y §10 incorporan
comprobaciones proporcionadas. §12 ordena dependencias y conserva bloqueos.
No se supone una API, hook ni separación real de contadores por crear bloques.

**Límite de aprobación histórica:** v1.1 revisado y aprobado tenía hash
`e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`.
Su review y R-OTEL-01–03 quedan cerrados para ese objeto; el delta P4 aún no tiene
veredicto. Plan v1.2 y contrato de aislamiento v1.2 son documentos independientes.
Este último permanece intacto y con INFORMACIÓN INSUFICIENTE.

**Continuidad corregida:** HANDOFF apuntaba todavía a ejecutar Etapa C v1 y
WIREFRAME a la ruta Kev. Se sincronizan con los estados y la decisión P4, sin
reactivar ensayos agotados ni declarar automática una integración no probada.

**Pruebas de producto:** no ejecutadas; cambio solo documental. No se repiten
S01–S03/H01/H02/A01–A03, ni T14, Paso 2 o Paso 3. Se comprueban únicamente
integridad de los archivos no editados, referencias locales y formato del diff.

**Estado:** PLAN_CON_INCERTIDUMBRE_CRITICA. Única siguiente acción: revisión
dirigida del delta P4 del plan OTel v1.2; sin abrir una nueva ronda en esta edición.

**Validación documental ejecutada:** PASS. Comparación contra baseline de 476
archivos: solo cambian plan, PROJECT_STATE, STATE, HANDOFF, WIREFRAME y este
registro; los otros 470 quedan intactos. 49 referencias locales resueltas,
cercas Markdown balanceadas y hash del plan coincidente en ambos estados y
evidencia. `git diff --check` PASS; comprobación adicional de whitespace para
los seis documentos, incluidos los no trackeados. No son pruebas de producto
ni un veredicto de revisión técnica.

La comprobación completa contra `/dev/null` señaló espacios dobles de salto
de línea Markdown ya presentes; se conservaron como formato intencional. La
comprobación final distingue esos saltos válidos y pasó sin otros espacios
finales inválidos. No se normalizó texto histórico para silenciar ese aviso.

## Review dirigido del contrato OTel v1.2 — 2026-09-28

Revisión N2 limitada a F12-01–F12-05 y H-C1–H-C5. Contrato revisado intacto,
SHA-256 `98c85652b24c86b68fddb8dbe20cca8d00f334d8f53dec05888b47f875a1692a`.

Evidencia nueva de solo lectura:

- `codex --version` informa `codex-cli 0.158.0`; el contrato había registrado
  0.157.1. La ayuda actual conserva `--no-daemon`, `--strict-config`, `-c`,
  `--profile` y la referencia a `CODEX_HOME`.
- `herdr --version` conserva 0.8.0; `herdr agent start --help` sigue sin una
  opción documentada de entorno por agente.
- La documentación oficial vigente declara que el estado local se guarda bajo
  `CODEX_HOME` y enumera configuración, auth por archivo, historial, logs y
  cachés. También distingue almacenamiento `file`, `keyring`, `auto` y
  `ephemeral`; este último no constituye una fuente de credenciales.

No se abrió Codex/herdr, pane, sesión o login; no se consultó estado de login,
sesiones, credenciales o valores de configuración. No se ejecutó piloto, código
o prueba de producto y no se cambió configuración, router o launcher.

**Resultado:** REQUIERE_AJUSTES. R-OTEL-C12-01 exige rebaselinar la versión
actual; R-OTEL-C12-02 separar fuente y almacenamiento de autenticación;
R-OTEL-C12-03 impedir un falso PASS de propagación/inmutabilidad. Resultado
completo en [OTEL_PLAN_REVIEW.md](OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12--aislamiento--2026-09-28).

## Corrección dirigida del contrato OTel v1.2-r1 — 2026-09-28

Con autorización posterior se corrigieron exclusivamente R-OTEL-C12-01/02/03 en
[OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md). Nueva revisión
identificada como v1.2-r1, SHA-256
`5647887786d52a22ef8056c25e9109b5ebcebfb92ba9865369424f5889d98a5d`.

- R-OTEL-C12-01: 0.157.1 queda como antecedente; el baseline de solo lectura
  registra PATH/resolución y Codex 0.158.0, más STOP ante deriva futura.
- R-OTEL-C12-02: D12-AUTH separa fuente de credencial y almacenamiento. A0–A3
  requieren evidencia o decisión explícita; copiar secretos queda prohibido.
- R-OTEL-C12-03: H-C1–H-C4 y B0–B4 requieren artefacto atribuible en la raíz
  temporal, manifiesto global solo de metadatos y reversión antes de otro piloto.

La corrección no selecciona autenticación ni prueba la viabilidad. D12-AUTH y la
comprobación viva conservan autorización separada. Estado:
PLAN_CON_INCERTIDUMBRE_CRITICA, listo únicamente para review dirigido.

Solo se ejecutaron lecturas de versión/ruta/ayuda ya permitidas y comprobaciones
documentales. No se abrió Codex/herdr de forma interactiva, pane, sesión, login o
piloto; no se leyeron credenciales, sesiones o valores de configuración; no se
instalaron dependencias ni se cambió router, launcher o configuración global.

## Review dirigido del contrato OTel v1.2-r1 — 2026-09-28

Objeto intacto, SHA-256
`5647887786d52a22ef8056c25e9109b5ebcebfb92ba9865369424f5889d98a5d`.
Seguimiento limitado a R-OTEL-C12-01/02/03 y efectos directos.

**Resultado: REQUIERE_AJUSTES.** R-OTEL-C12-01 cierra: baseline histórico y
actual están separados y B0 detiene la ejecución ante deriva. R-OTEL-C12-02
sigue abierto porque A0 puede avanzar sin una señal de autenticación efectiva.
R-OTEL-C12-03 sigue abierto porque pane más artefacto no vinculan de forma
inequívoca el hijo con `CODEX_HOME`, y el manifiesto de rutas fijas puede omitir
cambios dentro de árboles personales existentes.

No se modificó el contrato ni se resolvió D12-AUTH. No se abrió proceso, pane,
sesión, login o piloto; no se leyeron sesiones, credenciales o valores de
configuración. Resultado completo en
[OTEL_PLAN_REVIEW.md](OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12-r1--seguimiento--2026-09-28).

## Corrección dirigida del contrato OTel v1.2-r2 — 2026-09-28

Objeto corregido: [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md),
versión interna v1.2-r2, SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
El cambio se limitó a R-OTEL-C12-02/03; R-OTEL-C12-01 permanece cerrado.

- A0 es ahora un control negativo que siempre deja H-C3 BLOCKED.
- A1–A3 requieren `AUTH_OK`: señal sanitizada de autenticación efectiva para la
  misma raíz, fuente y proceso hijo. Interfaz lista, credencial presente, código
  de salida o ausencia de error no sirven como sustituto.
- H-C2 exige la cadena `herdr → hijo → ejecutable/versión → artefacto temporal`,
  sin volcar el entorno y persistiendo solo referencias digeridas.
- H-C4 exige inventario recursivo entrada por entrada con identificadores HMAC
  efímeros y metadatos; no sigue symlinks, no abre contenido y detecta cambios
  internos aunque el directorio padre parezca estable.
- Los casos documentales cubren A0, señal ausente o discordante, artefacto sin
  vínculo al hijo, cambio interno y recorrido/symlink incompleto.

La corrección no demuestra viabilidad ni elige D12-AUTH. No se abrió Codex,
herdr, pane, sesión, login o piloto; no se leyeron sesiones, credenciales,
valores de configuración ni contenidos personales. No se instalaron dependencias
ni se cambió configuración, router o launcher.

## Review dirigido del contrato OTel v1.2-r2 — 2026-09-28

Objeto revisado intacto: [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md),
SHA-256 `943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
Alcance N2 limitado a R-OTEL-C12-02/03 y efectos directos.

**Resultado: APROBADO. Sin observaciones accionables.**

- R-OTEL-C12-02 CERRADO: A0 nunca puede satisfacer H-C3. A1–A3 requieren
  `AUTH_OK` efectivo, sanitizado, con método esperado y referencia al mismo hijo;
  señales de disponibilidad no lo sustituyen.
- R-OTEL-C12-03 CERRADO: H-C2 vincula herdr, hijo, ejecutable y artefacto
  temporal; H-C4 compara recursivamente entradas personales mediante HMAC efímero
  y metadatos, sin abrir contenido o persistir nombres.
- B1–B4 detienen el recorrido si falta verificador, cadena atribuible, recorrido
  completo, reversión o inmutabilidad.
- §7 contiene los negativos de A0, señal discordante, artefacto sin vínculo,
  cambio interno, symlink y recorrido incompleto.

La evidencia viva sigue pendiente: no se demostró que exista un `AUTH_OK`
utilizable para una opción concreta ni que el host produzca los oráculos en una
ejecución real. Eso no impide aprobar el contrato porque cada ausencia genera
BLOCKED/STOP y no un falso PASS. D12-AUTH continúa sin resolver.

No se modificó el contrato, eligió autenticación, abrió Codex/herdr, pane,
sesión, login o piloto ni se leyó configuración, credenciales o sesiones.
Resultado completo en
[OTEL_PLAN_REVIEW.md](OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12-r2--cierre-c12--2026-09-28).

## Investigación de viabilidad A2 — 2026-09-28

**Alcance:** solo lectura sobre A2, sin seleccionar D12-AUTH y sin modificar el
contrato aprobado. Se contrastaron Codex CLI 0.158.0, herdr 0.8.0, el wrapper
local accesible y documentación oficial. No se abrió pane, proceso interactivo,
sesión, login, red de autenticación o piloto; no se ejecutó `codex login status`
ni se leyeron configuración, sesiones o credenciales.

### Capacidades comprobadas

- La documentación oficial de [autenticación](https://learn.chatgpt.com/docs/auth)
  define `ephemeral` como credenciales conservadas solo en la memoria del proceso
  actual. Por eso un `codex login` independiente no puede entregar ese acceso a
  un Codex posterior bajo herdr.
- La [referencia de comandos](https://learn.chatgpt.com/docs/developer-commands)
  documenta el login interactivo, `codex login status` como comando que termina
  después de informar el método y `/usage` dentro de la sesión. `/usage` requiere
  autenticación ChatGPT y no envía una tarea al modelo.
- La documentación de [app-server](https://learn.chatgpt.com/docs/app-server)
  confirma que Codex dispone internamente de `account/read`,
  `account/login/start`, `account/updated` y `account/usage/read`. Esa interfaz
  prueba que existe una señal oficial de autenticación, pero iniciar un
  app-server aparte cambiaría la topología de un solo Codex exigida por B3 y no
  se adopta como ruta de A2.
- La instalación local resuelve `/opt/homebrew/bin/codex` como
  `codex-cli 0.158.0`. Su ayuda conserva login interactivo y app-server; el
  binario contiene `/usage`, `account/usage/read` y el mensaje de rechazo
  cuando la sesión no está autenticada. Esto demuestra disponibilidad local de
  la señal, no su éxito vivo.
- `herdr 0.8.0` documenta `pane split --env KEY=VALUE` y argumentos para
  `agent start`. El wrapper local
  `/opt/homebrew/lib/node_modules/@openai/codex/bin/codex.js` copia
  `process.env` al binario hijo. Existe por tanto una cadena candidata para
  `CODEX_HOME`; su propagación efectiva bajo herdr sigue pendiente de observación.

### Camino sustentado y límites

A2 es técnicamente plausible solo con esta secuencia: iniciar el Codex final
bajo herdr con raíz temporal privada, `--no-daemon` y almacenamiento
`ephemeral`; el usuario completa el login desde ese mismo Codex; luego se invoca
`/usage` en la misma sesión y se persiste únicamente un `AUTH_OK` sanitizado con
resultado autenticado, método A2, instante y referencia digerida del hijo. No se
conservan identidad, plan, límites, importes, consumo ni respuesta del servicio.

La frase «tras el login separado» de A2 no puede interpretarse como otro proceso:
eso contradice la duración documentada de `ephemeral`. Puede significar una
etapa separada, previa a toda tarea, dentro del mismo proceso. El contrato no se
modificó y D12-AUTH continúa pendiente.

### Supuestos y prueba posterior necesaria

Siguen sin probarse en vivo: que herdr propague la raíz al hijo exacto, que
0.158.0 acepte `ephemeral` en esa ruta, que el login complete sin escribir
credenciales, que `/usage` responda autenticado en el mismo proceso y que el
inventario personal permanezca idéntico.

La comprobación mínima posterior requeriría autorización explícita para una sola
pane herdr, un solo Codex 0.158.0 con raíz temporal y `--no-daemon`, login de
navegador realizado por el usuario, red de autenticación y una consulta `/usage`
sin tarea. Debe ejecutar H-C1–H-C4, descartar la salida de uso tras reducirla a
`AUTH_OK`, cerrar el proceso y borrar la raíz temporal. STOP antes de toda tarea
si aparece otro proceso de login, una credencial en disco, falta de propagación,
respuesta de no autenticado, exposición de identidad/contenido o cambio del
estado personal. No se espera inferencia ni costo de modelo; USD continúa
`unknown` porque no se observó evidencia comercial.

**Resultado:** CAMINO_SUSTENTADO_CON_PRUEBA_PENDIENTE. A2 no fue seleccionada y
D12-AUTH no fue aprobada. P1–P4, R-OTEL-C12-01/02/03, R-OTEL-01–03,
R-OTEL-P4-01/02 y todos los cierres anteriores permanecen intactos.

## Registro de D12-AUTH/A2 — 2026-09-28

El usuario seleccionó explícitamente A2 para D12-AUTH con tres condiciones:
login interactivo dentro del mismo Codex temporal bajo herdr, credenciales solo
en memoria mediante `ephemeral` y `/usage` como comprobación de autenticación sin
tarea. La decisión se registró en [02_DECISION.md](02_DECISION.md).

La selección resuelve la decisión de fuente/almacenamiento/verificador, pero no
autoriza ejecutar el preflight. Se preparó en [HANDOFF.md](HANDOFF.md) el permiso
concreto para una futura corrida H-C1–H-C4: una pane, un Codex 0.158.0,
`--no-daemon`, raíz temporal, login de navegador por el usuario, una consulta
`/usage`, evidencia sanitizada y reversión. H-C5/Paso 3, tarea, fixture,
inferencia, lectura de credenciales/sesiones, dependencias y cambios globales
quedan excluidos.

No se abrió pane, Codex, herdr, navegador, sesión, login o red; no se leyó
configuración, credenciales o sesiones; no se modificó el contrato aprobado. Su
SHA-256 permanece
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
P1–P4 y todos los hallazgos y cierres anteriores se conservan.

## Preflight A2 H-C1–H-C4 — cierre 2026-09-28

**Autorización consumida:** una sola ejecución. **Resultado global:**
`FAIL/BLOCKED`. El contrato aprobado permaneció intacto con SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.

### Baseline y preparación

- B0 PASS: `/opt/homebrew/bin/codex`, wrapper resuelto, `codex-cli 0.158.0`,
  flags `--no-daemon`/`--strict-config`, herdr 0.8.0 y capacidades de pane/args
  coincidieron con el baseline.
- Raíz temporal privada 0700 y configuración conocida 0600. SHA-256 inicial de
  la configuración: `1f17f8030520a75e440f9b74bba9305d68a0f51952a515e0aa54fd1eca4577fd`.
- Inventario personal previo: 1.244 entradas, cero errores, cero symlinks. Los
  identificadores se calcularon con HMAC y la clave permaneció solo en memoria.
- Se creó una sola pane herdr y un solo Codex con `--no-daemon`; el proceso
  nativo exacto quedó representado únicamente por el identificador sanitizado
  `05071611fc9d95400611`.

### Gates observados

- **H-C1 BLOCKED:** la raíz y permisos temporales se observaron, pero su uso
  exclusivo por el proceso exacto no puede cerrarse sin el vínculo requerido
  por H-C2 y con el resultado de H-C4.
- **H-C2 BLOCKED:** el observador realizó 13.130 sondeos mientras el proceso
  permaneció vivo y encontró cero artefactos temporales vinculados directamente
  a ese proceso. No se sustituyó la prueba por la variable de la pane ni por la
  mera existencia de archivos.
- **H-C3 PASS:** el usuario completó el login dentro del mismo Codex temporal y
  `/usage` presentó el menú autenticado esperado, sin marcador de login requerido
  ni fallo. No apareció `auth.json`.
- **H-C4 FAIL:** el inventario posterior tuvo 1.244 entradas, cero errores y
  cero symlinks, pero tres entradas cambiaron. Se conservaron únicamente estos
  identificadores HMAC, sin leer ni persistir nombres o contenidos:
  `685971dd6360a973d202a8a714ebd70cfa374910fc07b0533b86b75e3540ee69`,
  `842b282ea377728a8725633c04d76c107726db79336e5abcd0f03f6464e0f269` y
  `e668885fb26832d87b9dd39f403271cf7deb4911e211bd8c2919744916872696`.

`AUTH_OK` sanitizado persistido:

```text
contract OTel-v1.2-r2
option A2
method_class interactive_ephemeral
authenticated true
child_ref 05071611fc9d95400611
observed_at 2026-09-29T02:02:14.223744+00:00
verifier_class tui_usage_menu
```

No se persistieron identidad, datos de cuenta, plan, importes, límites, valores
de uso ni contenido de la respuesta. La causa de los tres cambios personales no
puede atribuirse con la evidencia permitida; cualquier relación con la sesión
controladora sería solo una hipótesis.

### Reversión y límites

B4 cerró el Codex, la pane y el workspace herdr. La configuración temporal cambió
dentro de su propia raíz a SHA-256
`6b20e164a8f13f047241ca87b24c1ec039c660ad9fcd81416a808a0b8a11619f`;
la raíz contenía 9.365 entradas, cero symlinks y ningún `auth.json`. Después se
eliminó por completo y se verificó la ausencia de la pane, el agente y la raíz.
La clave HMAC dejó de existir con el monitor. La reversión operativa pasó, pero
la igualdad del estado personal falló por los tres cambios.

No se envió tarea, prompt, fixture o inferencia; no se ejecutó H-C5/Paso 3; no se
leyeron sesiones, credenciales, rutas personales cambiadas ni valores de
configuración. Tokens, USD y tiempo de agente no se midieron en este preflight.
P1–P4 y todos los hallazgos y cierres anteriores permanecen intactos.

## Diagnóstico de solo lectura H-C2/H-C4 — 2026-09-29

### Alcance y fuentes

Se inspeccionaron únicamente el contrato/estado ya autorizados, la instalación
local accesible de Codex 0.158.0, ayudas/manpages locales y código o documentación
oficial. No se abrió sesión, proceso interactivo, pane, login o red autenticada;
no se repitió el preflight; no se leyeron sesiones, credenciales, rutas
personales cambiadas o valores de configuración. El contrato quedó intacto con
SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.

Fuentes oficiales decisivas:

- [configuración Codex 0.158.0](https://github.com/openai/codex/blob/rust-v0.158.0/codex-rs/config/src/config_toml.rs): `sqlite_home` usa
  `CODEX_SQLITE_HOME` si existe y, en caso contrario, `CODEX_HOME`; `log_dir`
  predetermina a `$CODEX_HOME/log` y su definición explícita habilita el log TUI.
- [wrapper Codex 0.158.0](https://github.com/openai/codex/blob/rust-v0.158.0/codex-cli/bin/codex.js): copia `process.env` y entrega ese entorno al binario
  nativo. La copia local coincide funcionalmente en líneas 231–244; SHA-256
  `61b0194f3bb6534439c8d26a3ed57d0805f84b884588b761795323eeb92fcf70`.
- [runtime de estado 0.158.0](https://github.com/openai/codex/blob/rust-v0.158.0/codex-rs/state/src/runtime.rs): abre y migra bases SQLite de estado, logs,
  objetivos, memorias y cola bajo la raíz SQLite configurada.
- [grabador de sesiones 0.158.0](https://github.com/openai/codex/blob/rust-v0.158.0/codex-rs/rollout/src/recorder.rs): para sesiones nuevas calcula la ruta pero
  difiere crear/abrir el archivo hasta `persist()`.
- Las manpages locales confirman que `lsof` lista archivos abiertos y que `-a`
  combina los selectores con AND. `fs_usage` y `opensnoop` existen, pero requieren
  privilegios de administrador, no autorizados en este diagnóstico.

### Hechos comprobados

1. `CODEX_HOME` no es la única raíz de escritura configurable. Una variable
   heredada `CODEX_SQLITE_HOME` puede seleccionar una raíz SQLite distinta; el
   wrapper no la elimina al iniciar el binario nativo.
2. El runtime mantiene abiertos archivos SQLite bajo la raíz configurada. Esos
   descriptores ofrecen un vínculo estable que H-C2 puede observar si todas las
   raíces se fijan en el árbol temporal.
3. `lsof` es una fotografía de descriptores abiertos, no un historial de
   creaciones. El archivo de una sesión nueva puede no existir ni estar abierto
   antes de una persistencia explícita. El preflight no envió tarea.
4. El inventario H-C4 abarcó el mismo estado personal que una sesión Codex
   controladora activa puede actualizar mediante rollouts y bases SQLite. Por
   ello la topología no permite atribuir una diferencia exclusivamente al hijo
   observado.

### Hipótesis que la evidencia no autoriza a convertir en causa

- Una raíz `CODEX_SQLITE_HOME` heredada pudo dirigir bases del hijo fuera de la
  raíz temporal y explicar parte de las cero coincidencias de H-C2.
- La sesión controladora o una base SQLite pudo producir una o más de las tres
  diferencias HMAC de H-C4.

No se leyó ni conservó el valor efectivo de esas raíces ni la identidad de los
tres caminos. En consecuencia, ninguna de estas hipótesis se atribuye al intento
fallido.

### Evidencia faltante

- raíz SQLite/log efectiva del hijo fallido;
- identidad de las tres entradas cambiadas, deliberadamente no mapeada;
- predicado exacto del sondeo `lsof`, no persistido en la evidencia anterior;
- validación en frío de que las raíces fijadas producen descriptores atribuibles;
- prueba de que un supervisor externo puede tomar/comparar el inventario con
  todos los clientes del estado personal cerrados y revertir de forma segura.

### Corrección mínima propuesta

- **H-C2:** fijar en un único árbol temporal `CODEX_HOME`,
  `CODEX_SQLITE_HOME`/`sqlite_home` y `log_dir`; mantener historial desactivado y
  credenciales `ephemeral`; autocomprobar el observador; exigir una consulta
  `lsof` que combine con AND el PID nativo exacto y un descriptor SQLite/log
  conocido. Persistir solo booleanos, versión y referencias digeridas.
- **H-C4:** sacar el inventario de toda sesión Codex activa. Un supervisor
  externo revisado toma el baseline con todos los clientes personales cerrados,
  inicia y coordina únicamente el hijo temporal, compara/revierte y persiste el
  resultado sanitizado. Una sesión posterior puede leer ese resultado.

No se propone ignorar rutas mutables ni descontar cambios de la controladora:
eso debilitaría el gate. La corrección debe quedar primero en v1.2-r3 y pasar una
revisión dirigida antes de pedir otro preflight. H-C5/Paso 3 permanecen fuera de
alcance. P1–P4 y todos los hallazgos y cierres anteriores se conservan.

## Corrección documental OTel v1.2-r3 — 2026-09-29

**Objeto:** [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md), limitado
a H-C2, H-C4 y efectos directos del diagnóstico. SHA-256 resultante:
`ac685955886ba10a1171a5f7787c0d0195613661215f2cd400ded35097da60ad`.

### Cambios verificables

- La cabecera identifica v1.2-r3 y declara que la corrección no autoriza
  preflight, login, sesión, piloto, H-C5 o Paso 3.
- F12-03/F12-06 y H-C1/H-C2 fijan `CODEX_HOME`,
  `CODEX_SQLITE_HOME`/`sqlite_home` y `log_dir` dentro del mismo temporal.
- H-C2 exige autocomprobación positiva y negativa del predicado antes de herdr;
  el PASS requiere un descriptor SQLite/log de allowlist ligado mediante AND al
  PID nativo exacto. Un rollout no materializado no decide por sí solo.
- §3.1, H-C4 y B2–B4 eliminan la sesión Codex controladora: exigen cero procesos
  Codex preexistentes y permiten durante la ventana solo el árbol iniciado por
  el supervisor externo. La comparación y reversión terminan antes de que otra
  sesión pueda leer el resultado reducido.
- §7 agrega negativos para raíz fuera del temporal, autocomprobación incapaz de
  discriminar, falta de descriptor estable y proceso Codex ajeno.
- A2/D12-AUTH continúa seleccionada; A1/A3 quedan explícitamente no
  seleccionadas. P1–P4 y los hallazgos/cierres anteriores no se reabren.

### Límites

La edición formaliza una ruta comprobable; no prueba su comportamiento vivo ni
explica los tres cambios HMAC históricos. El supervisor, la propagación de todas
las raíces, el descriptor del PID y la inmutabilidad personal todavía requieren
review y, solo después, una nueva autorización de ejecución.

No se abrió proceso, pane, sesión, login o red autenticada; no se leyó sesión,
credencial, ruta personal cambiada o valor de configuración; no se ejecutó
preflight, H-C5/Paso 3 ni se instaló dependencia. No se cambió router, launcher o
configuración global y no hubo publicación o commit.
