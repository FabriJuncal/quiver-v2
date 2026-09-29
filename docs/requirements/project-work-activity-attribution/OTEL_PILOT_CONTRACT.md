# Contrato de piloto OTel v1.1

**Requirement:** project-work-activity-attribution  
**Fecha:** 2026-09-28  
**Estado:** BLOCKED; residuo de trust reparado, reintento v1.1 no aprobado  
**Plan gobernante:** OTel v1.1, SHA-256
`e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`

## 1. Propósito y límite

El piloto comprobará, en dos etapas y con autorizaciones separadas, si el Codex
interactivo iniciado desde herdr puede:

1. entregar consumo y tiempos con identidad y completitud comprobables (Paso 2);
2. enlazar ese consumo con Análisis, Desarrollo, Pruebas y Documentación sin que
   el usuario marque fases ni envíe un mensaje por actividad (Paso 3).

No es implementación productiva, migración de datos ni importación histórica. No
modifica el router, el launcher habitual, la autenticación, el modelo, los precios
o el comportamiento permanente de Codex/herdr. Cada etapa se detiene en su propio
gate; autorizar Paso 2 no autoriza Paso 3.

## 2. Decisiones ya cerradas

- P1: cuatro bloques de presentación, conservando el detalle de feature, bug,
  test, explicación y documentación sin duplicar totales.
- P2: marcas automáticas y reglas verificables; Kev no participa.
- P3: el caso final acotado exige captura completa y cero consumo mixto, sin
  atribuir o con detalle requerido desconocido. Si falla, no se recorta el caso.
- Tiempo transcurrido y duración de herramienta se muestran separados; tiempo
  activo permanece `unknown`.
- USD, tier y modalidad de pago permanecen `unknown` sin evidencia directa. No se
  consultan facturas ni se usan precios comerciales.

## 3. Evidencia técnica que condiciona el piloto

La [configuración oficial de Codex](https://developers.openai.com/codex/config-reference)
indica que las claves `otel` en `.codex/config.toml` del proyecto son ignoradas;
la telemetría debe configurarse a nivel de usuario o mediante overrides de una
ejecución. Se eligen overrides CLI porque son temporales y no editan la
configuración global.

La [configuración avanzada](https://developers.openai.com/codex/config-advanced)
documenta exportación OTLP/HTTP, redacción del prompt con
`otel.log_user_prompt = false`, metadatos de conversación/versión y contadores en
eventos `response.completed`. También aclara que el envío es asíncrono y se vacía
al terminar el proceso.

Los [hooks oficiales](https://developers.openai.com/codex/hooks) ofrecen identidad
de sesión/turno y eventos de herramientas. También declaran que herramientas
alojadas y algunos caminos especializados pueden quedar fuera. Por eso sirven
para comprobar acciones en Paso 3, pero no son por sí solos una prueba de todo el
consumo ni de todas las acciones.

Auditoría local de Paso 0: herdr `0.8.0`, Codex del PATH `0.157.1`, hooks estables
y activos, integración de estado herdr→Codex no instalada, OTel no configurado,
`otelcol` no instalado, Python 3.9.6 disponible. Docker existe pero queda fuera
de este piloto.

La ejecución v1 demostró dos límites que gobiernan v1.1: el daemon compartido
exportó dos `conversation.id` y `response.completed` no entregó `response_id` ni
todos los contadores necesarios. Además, el diálogo de confianza persistió la
ruta temporal. v1.1 no supone resueltos esos límites: los convierte en gates
previos y de aceptación. Usar `--no-daemon` solo prueba aislamiento si el proceso
y los eventos observados lo confirman.

## 4. Estructura cerrada del piloto

### Etapa C — reintento aislado (Paso 2, ejecutado hasta el preflight)

- **Sesiones:** exactamente una sesión Codex nueva y dedicada.
- **Inicio:** una pane temporal de herdr; `herdr agent start --kind codex` con
  `--no-daemon`, sandbox `read-only` y argumentos de una sola ejecución. No se
  toca el comando habitual ni se conecta al daemon compartido.
- **Proyecto:** fixture artificial bajo
  `/private/tmp/quiver-otel-capture-v1-1/fixture`, sin archivos del usuario,
  secretos, dependencias o red adicional.
- **Trust:** la confianza de esa ruta se declara solo mediante un override CLI.
  Antes de enviar la tarea, herdr debe confirmar que no existe diálogo de
  confianza y el hash de `~/.codex/config.toml` debe seguir intacto. Si aparece
  el diálogo, se cierra la pane externamente sin enviar teclas ni tarea.
- **Tarea exacta:** leer `PILOT_INPUT.txt`, que tendrá tres líneas no vacías, y
  responder en una frase cuántas contiene. No editar archivos.
- **Cierre:** salir de Codex para forzar el flush documentado, detener el receptor
  y cerrar únicamente la pane temporal.
- **Lectura de referencia:** solo metadatos e informes de uso de esa sesión nueva;
  no prompts, respuestas, argumentos, resultados, otras sesiones ni historial.

Esta etapa prueba captura, aislamiento, identidad, varias respuestas del mismo
turno cuando existan, deduplicación, entrega final y detección de una unidad
eliminada sobre una copia sanitizada. No clasifica actividades. La tarea no se
envía si falla cualquier preflight de proceso, trust, configuración o privacidad.

### Etapa A — atribución automática (Paso 3, reservada)

Solo se prepara si Etapa C pasa y recibe autorización propia.

- **Sesiones:** otra sesión Codex nueva y dedicada; no reutiliza la de captura.
- **Proyecto:** fixture artificial aislado, con módulo Python, tests y README.
- **Tarea exacta del usuario:** agregar `normalize_labels`, corregir el caso
  artificial de duplicados, ejecutar las pruebas, actualizar el README y explicar
  el resultado. El usuario envía una sola tarea y no selecciona categorías.
- **Recorrido esperado:** Análisis → Desarrollo(feature/bug) → Pruebas →
  Desarrollo si hay fallo → Pruebas → Documentación → Explicación.
- **Marcas:** automáticas, emitidas por el flujo del agente; el primer bloque se
  abre antes de la primera llamada. Un hook observa las acciones y evidencia los
  huecos, pero no inventa categorías desde nombres de herramientas o extensiones.
- **Gate:** cualquier acción fuera de una marca completa, llamada indivisible,
  transición sin identidad o consumo no conciliado deja el resultado mixto/sin
  atribuir y hace fallar P3.

La definición del emisor de marcas y el trust exacto del hook se cerrarán después
de Etapa C usando los identificadores realmente observados. No se instala ahora
la integración global de herdr ni se usa `--dangerously-bypass-hook-trust`.

## 5. Instrumentación autorizable para Etapa C

### Receptor temporal

Se preparará con Python estándar, sin instalar paquetes, y escuchará solo en
`127.0.0.1:4318`. Antes de iniciar, el puerto y la ruta v1.1 deben estar libres;
si no lo están, la etapa se detiene y no elige otro destino silenciosamente.

Archivos temporales previstos:

- `/private/tmp/quiver-otel-capture-v1-1/receiver.py`;
- `/private/tmp/quiver-otel-capture-v1-1/fixture/PILOT_INPUT.txt`;
- `/private/tmp/quiver-otel-capture-v1-1/sanitized-events.jsonl`;
- `/private/tmp/quiver-otel-capture-v1-1/reference-ledger.json`.

El receptor se identifica por SHA-256 antes de ejecutarse. Procesa OTLP/HTTP JSON
en memoria y persiste únicamente la allowlist. No guarda el payload crudo.

### Proceso y configuración efímeros de Codex

El lanzamiento propuesto incorpora estos argumentos, sin editar `config.toml`:

```text
--no-daemon
--strict-config
-C /private/tmp/quiver-otel-capture-v1-1/fixture
-s read-only
-a never
--no-alt-screen
-c 'projects."/private/tmp/quiver-otel-capture-v1-1/fixture".trust_level="trusted"'
-c 'otel.environment="quiver-otel-capture-v1-1"'
-c 'otel.exporter={otlp-http={endpoint="http://127.0.0.1:4318/v1/logs",protocol="json"}}'
-c 'otel.log_user_prompt=false'
-c 'otel.metrics_exporter="none"'
-c 'otel.trace_exporter="none"'
```

La clave `projects.<ruta>.trust_level` reproduce como override efímero la forma
observada en el TOML durante v1; no se la considera viable hasta que
`--strict-config` la acepte y herdr muestre el prompt normal sin diálogo de trust.
Ese preflight no envía una tarea. Se registra el hash y `stat` del TOML antes de
crear la pane y se repite antes de enviar la tarea y después del cierre. Cualquier
cambio detiene el piloto; no se intenta corregirlo silenciosamente.

El proceso inspeccionado por herdr debe contener el binario nativo, `--no-daemon`
y exactamente los overrides declarados. No se configuran headers, claves, TLS,
destinos remotos ni exportadores adicionales. No se usa
`--dangerously-bypass-hook-trust` ni se acepta una pantalla de confianza.

### Allowlist persistida y normalización observada

El receptor admite solo nombres exactos; no conserva una clave por contener las
palabras `token`, `duration` o `id`. Primero valida tipo/clave permitida y luego
aplica el descarte sensible, para no volver a perder un contador numérico de
reasoning.

- evento: `event.name`, `event.kind`, hora, `service.name`, `service.version`,
  ambiente, éxito y duración numérica;
- identidad: `conversation.id` y `response.id`/`response_id`, transformados a
  SHA-256 antes de escribir. Turn/request/operation IDs solo si están en la lista
  cerrada del comprobador y también se persisten como digest;
- esquema OTel observado/aceptado: `cached_token_count` y
  `cache_write_token_count`;
- esquema OTel requerido si aparece en el reintento: `input_token_count`,
  `output_token_count`, `reasoning_output_token_count` y `total_token_count`;
- forma canónica de referencia: `input_tokens`, `cached_input_tokens`,
  `cache_write_input_tokens`, `output_tokens`, `reasoning_output_tokens` y
  `total_tokens`;
- hashes de fixture, receptor, argumentos efectivos y reporte.

| Campo OTel exacto | Campo canónico |
|---|---|
| `input_token_count` | `input_tokens` |
| `cached_token_count` | `cached_input_tokens` |
| `cache_write_token_count` | `cache_write_input_tokens` |
| `output_token_count` | `output_tokens` |
| `reasoning_output_token_count` | `reasoning_output_tokens` |
| `total_token_count` | `total_tokens` |

`event.name=codex.sse_event` más `event.kind=response.completed` identifica una
unidad candidata; no se toma `conversation.id` como identidad de respuesta. Se
descartan antes de escribir prompt, respuesta, razonamiento textual, snippets,
salida o argumentos de herramientas, comandos, parches, contenidos de archivos,
`transcript_path`, credenciales, headers, variables de entorno y cualquier clave
no allowlisted. Una ausencia se registra como `unknown`, nunca como cero.

## 6. Fuente contable y completitud

- **Fuente principal:** eventos OTel `response.completed` recibidos y sanitizados.
- **Referencia independiente:** `session_meta` y registros de uso de la única
  sesión piloto. La ruta se busca por nombre exacto usando el `conversation.id`
  mantenido solo en memoria; no se listan ni abren otras sesiones. El parser
  descarta líneas que no sean `session_meta` o `token_usage_record` antes de
  decodificarlas. Solo persiste el digest; la ruta y el ID crudo no se conservan
  en el reporte.
- **Acciones:** eventos de herramienta se usan como contraste de cobertura; no se
  suman como tokens.
- **Final de entrega:** salida del proceso Codex + cierre correcto de la entrega
  OTLP + conciliación contra la referencia. Un timeout o silencio no cierra.
- **Prueba negativa:** se ejecuta solo después de que el original alcance PASS.
  Quitar exactamente una respuesta de una copia sanitizada debe producir
  `incomplete` e identificar el digest faltante; el original no se modifica.

La referencia canónica conserva seis contadores por `response_id`; OTel debe
entregar y conciliar la misma unidad y los mismos seis valores. No se compensa un
campo ausente con totales temporales, secuencia, `conversation.id` ni reparto. Si
la versión instalada no entrega identidad o contadores suficientes, la captura
queda `not_verified`; no se avanza a Paso 3.

## 7. Criterios de resultado de Etapa C

**PASS** requiere todos los gates, en orden:

1. **G-C1 Aislamiento y trust:** proceso efectivo con `--no-daemon`; un único
   `conversation.id` cuyo digest coincide con `session_meta`; cero eventos de
   otra conversación; sin diálogo de confianza; hashes/stat de configuración
   global iguales antes de la pane, antes de la tarea y después del cierre.
2. **G-C2 Privacidad:** prompt, respuesta, contenidos, argumentos, resultados,
   credenciales, headers y rutas de sesión no aparecen en persistencia.
3. **G-C3 Identidad:** cada `response.completed` contiene un `response_id` no
   vacío, único y con igualdad exacta de conjuntos contra la referencia. Un
   `conversation.id` o una posición temporal no reemplazan este gate.
4. **G-C4 Contadores completos:** cada respuesta posee los seis contadores
   canónicos. Son enteros no negativos; cached no excede input, reasoning no
   excede output y total coincide con input + output. `cache_write_input_tokens`
   debe estar presente, pero su relación tarifaria permanece no cualificada.
5. **G-C5 Conciliación:** OTel y referencia coinciden respuesta por respuesta y
   en totales; no hay duplicados, unidades extra, `unknown` ni conflictos.
6. **G-C6 Final y pérdida:** salida de Codex y flush establecen entrega final;
   recién entonces, la copia con una respuesta eliminada cambia de PASS a
   `incomplete` e identifica la unidad ausente.
7. **G-C7 Reversión:** pane, proceso, receptor y árbol temporal ausentes; puerto
   libre; launcher/router/configuración del usuario/proyecto sin cambios.

**BLOCKED/FAIL:** falta de identidad o referencia, contadores incompatibles,
pérdida no detectable, más de una conversación, contenido sensible persistido,
diálogo o persistencia de trust, necesidad de leer otras sesiones, cambiar
experiencia, instalar dependencias o modificar configuración global. Un resultado
parcial se conserva como evidencia y no habilita Paso 3.

## 8. Reversión y evidencia

Al terminar, se detienen receptor y sesión, se elimina solo el árbol temporal
creado para el piloto después de calcular sus hashes y se conserva en el
requirement únicamente el reporte sanitizado, comandos/exit codes, versiones,
conteos y conclusión. No se borra ninguna sesión existente ni se cambia la
configuración del usuario.

La reversión compara hashes/stat de la configuración; no restaura desde una copia
con secretos ni edita automáticamente el TOML. Si cambia, se detiene, preserva
solo evidencia no sensible del cambio y requiere una autorización específica
para cualquier reparación. La pane se cierra externamente ante un diálogo de
trust; no se envían `esc`, `enter`, números o comandos que puedan aceptar una
opción por defecto.

El consumo de la sesión piloto se informa como consumo de validación. No se suma
a una feature real y no se le calcula USD sin evidencia directa.

## 9. Lista cerrada para solicitar el reintento de Paso 2

Permitido únicamente con una autorización posterior propia:

1. comprobar puerto/ruta libres y registrar hash/stat de la configuración sin
   leer ni mostrar sus valores;
2. crear y ejecutar receptor/fixture v1.1 bajo la ruta temporal indicada, con la
   allowlist corregida y hashes previos;
3. abrir una pane herdr con una sesión Codex nueva, `--no-daemon`, sandbox
   `read-only`, override efímero de trust y los cinco overrides OTel;
4. antes de la tarea, verificar argv/proceso, ausencia del diálogo de trust y
   configuración intacta. Cualquier fallo cierra la pane y detiene el reintento;
5. enviar la tarea exacta una sola vez;
6. cerrar Codex para flush, detener el receptor y leer solo `session_meta` y
   `token_usage_record` de la sesión cuyo digest coincide exactamente;
7. evaluar G-C1–G-C5. Ejecutar la eliminación controlada solo si todos pasan;
8. evaluar G-C6–G-C7, limpiar solo el árbol creado y actualizar `EVIDENCE.md`,
   `STATE.md`, `PROJECT_STATE.md` y este contrato con PASS/BLOCKED.

Quedan excluidos Paso 3, hooks/marcas de actividad, código productivo, pruebas
históricas, otras sesiones, dependencias, Docker, red externa, router, launcher,
configuración global, publicación y commit.

## 10. Routing de ejecución propuesto

- **Perfil:** BALANCED.
- **Modelo:** GPT-5.6 Terra (`gpt-5.6-terra`) / Medium.
- **Fallback:** GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- **Switch Benefit:** LOW; sin Model Gate.
- **Motivo:** piloto N2 estrecho, reversible, con oráculos de identidad,
  privacidad y conciliación definidos. La configuración efectiva permanece
  `unknown` y no condiciona el inicio.
- **Review:** inline dirigido para Etapa C; review dedicado antes de integrar si
  la evidencia abre cambios de contrato o integridad.

## 11. Resultado de Etapa C — BLOCKED

La lista §9 se ejecutó una vez con el fixture artificial y terminó **BLOCKED**:

- herdr inició una pane nueva con Codex `0.157.1`, sandbox `read-only`, los cinco
  overrides efímeros y una única tarea; la pane volvió al shell y fue eliminada;
- el receptor persistió 40 eventos sanitizados. No se encontraron el nombre o
  contenido del fixture, el texto de la tarea, credenciales ni headers;
- la referencia permitida de la sesión piloto contiene 2 respuestas, un solo
  session/thread/turn y 46.398 tokens: 46.271 entrada, 33.280 cached input,
  127 salida y 14 reasoning output;
- OTel produjo 5 eventos `response.completed`, 0 con `response_id`, con solo
  `cached_token_count` y `cache_write_token_count`, y dos `conversation.id`;
- uno de esos identificadores coincide con la sesión piloto. El segundo no se
  identificó ni se abrió: demuestra contaminación del ámbito por el daemon
  compartido y queda registrado únicamente mediante digest opaco;
- la conciliación original resultó `incomplete`: 5 eventos OTel frente a 2
  respuestas de referencia, identidad y contadores incompletos, coincidencia
  exacta falsa. La copia con una unidad eliminada también quedó `incomplete`;
  como el original ya fallaba, la detección de pérdida no quedó cualificada;
- Codex persistió transitoriamente confianza para la ruta del fixture. Se retiró
  únicamente ese bloque y se verificó que la ruta ya no aparece en el TOML del
  usuario. No quedó configuración de proyecto, receptor, proceso o pane activa.

Hashes de evidencia antes de limpiar el árbol temporal:

- fixture: `4fdbc441ea7b546100e086ac1e4fc5ae6749b7314311c99db05be450eca12996`;
- receptor inicial: `6ec006007131a85984e7033580d5f8fdfa817942aa82b39df72b8673c2ac230b`;
- comprobador corregido: `9514efb746cd40c4b58587eb4279597b3e9c2937d72f02978e22b103e06de494`;
- eventos sanitizados: `4ac42088a364ab274e5ee9e17e27214ce51a029e51b37557df9c433c0c563297`;
- referencia permitida: `8cfbe0f2cc8ccbe1820c44c31805d1148dc4dd5aaf1c6e5d2d4ad763e4cd4f41`.

No se ejecutó Paso 3, no se clasificaron actividades y no se habilita
integración. El consumo pertenece exclusivamente a validación; USD, tier,
modalidad de pago y tiempo activo permanecen `unknown`.

## 12. Autorización del reintento v1.1

El usuario autorizó una sola ejecución de §9 el 2026-09-28. Esa autorización se
consumió al abrir la pane para el preflight vivo; la tarea artificial no se envió.

## 13. Resultado del reintento v1.1 — BLOCKED en preflight

La validación estática aceptó `--no-daemon`, el override de trust y los cinco
overrides OTel con exit `0`, sin modificar el TOML. El receptor quedó listo en
loopback y herdr abrió `wT:p7` con el binario nativo Codex 0.157.1. La inspección
del proceso confirmó todos los argumentos y `herdr agent explain` informó
`trust_directory.matched=false` y ningún blocker visible.

Antes de enviar la tarea, el tercer control obligatorio detectó que
`~/.codex/config.toml` había cambiado y contenía una coincidencia de la ruta
v1.1. El hash pasó de
`0e0bf7bb5e168f884d9b613b88838cf5b77141fac1644c939c78994517ddc7ab`
a `00ebc16f41deb7f2daa67f17f31d5dbb93e8b313651bf9443ee5984fad6ba7e9`;
el stat también cambió. Conforme a §9.4, la pane se cerró externamente sin enviar
teclas ni tarea y el receptor se detuvo. No se leyó ninguna sesión ni se creó la
referencia. La prueba negativa no se ejecutó.

El inicio produjo 12 eventos sanitizados antes del corte, incluido un
`response.completed`; se conservaron solo claves allowlisted y digests durante
la comprobación. Cero coincidencias dirigidas con el fixture, tarea o patrones
de credenciales. Hashes antes de limpiar: receptor
`4486cd78c918f126a9e8d66381f4d00136b492f643a519358dab3394c103fde5`,
fixture `87a3c52b88cf5eeec4bff79b5f65de20adbdb2d79a7f78d93f996a319c42ff5f`,
argv `a34030ced3e0c62bdfe8e7ef7fbb0da4ce272ec45db470cbd681b4667e7af72b`
y eventos `6426344cf903283778424f4e2a9d244fcbaf0e1bd68e92d9bef81367c1592b59`.

G-C1 falla por persistencia de trust. G-C2 solo tiene evidencia parcial del
saneamiento previo a la tarea. G-C3–G-C6 no se ejecutaron. G-C7 queda BLOCKED:
pane, procesos, receptor, puerto y árbol temporal fueron revertidos, pero la
coincidencia de configuración continúa presente. No se corrige automáticamente
porque §8 exige autorización específica ante un cambio del TOML. Paso 3 sigue
no autorizado y bloqueado.

### Reparación posterior autorizada

El usuario autorizó la reparación dirigida. Se creó un backup privado `0600`
del TOML mutado, SHA-256
`00ebc16f41deb7f2daa67f17f31d5dbb93e8b313651bf9443ee5984fad6ba7e9`,
y se eliminó únicamente la tabla exacta de la ruta v1.1 después de comprobar que
contenía solo `trust_level="trusted"`. La ruta quedó con cero coincidencias y el
TOML resultante tiene SHA-256
`536f8d4b5fba477f17f0a3857c5d58b304798fa71fed609ffd0c37c8877b96ce`.

La eliminación exacta no reprodujo el hash histórico: el archivo resultante es
cuatro bytes mayor que el baseline, por lo que no se normalizaron ni editaron
otros bytes. No había parser TOML independiente instalado; la comprobación fue
estructural y por hashes, sin ejecutar Codex. Esto cierra el residuo operativo,
pero no convierte G-C1/G-C7 en PASS ni autoriza otro intento.

## 14. Siguiente acción única

Preparar y revisar un contrato v1.2 que demuestre, sin abrir otra sesión, una
ruta de confianza temporal que no pueda persistir en configuración global. No
repetir el piloto hasta aprobar ese mecanismo.
