# Contrato de viabilidad OTel v1.2-r3

**Requirement:** project-work-activity-attribution  
**Fecha:** 2026-09-29  
**Estado:** PLAN_CON_INCERTIDUMBRE_CRITICA; corrección H-C2/H-C4 lista para
revisión dirigida; ningún preflight, piloto, login o sesión v1.2-r3 está autorizado  
**Antecedente:** [OTEL_PILOT_CONTRACT.md](OTEL_PILOT_CONTRACT.md) v1.1,
BLOCKED antes de enviar la tarea  
**Corrección limitada:** H-C2, H-C4 y efectos directos de su diagnóstico;
R-OTEL-C12-01/02/03 permanecen cerrados

## 1. Propósito y límite

Este contrato no ejecuta una captura. Define qué debe demostrarse antes de
considerar otra sesión artificial de OTel: que el proceso exacto de Codex lanzado
por herdr use una raíz temporal, pueda autenticarse mediante una fuente aprobada
y deje intactos la configuración y el estado personal del usuario.

Conserva P1–P4, R-OTEL-01–03, R-OTEL-P4-01/02 y los cierres
S01–S03/H01/H02/A01–A03. En esta fase:

- no se lee, copia, imprime, hashea ni expone contenido de credenciales o sesiones;
- no se abre Codex, herdr, una pane, una sesión o un login;
- no se usa una sesión real, Docker, dependencias, red adicional, router, launcher
  o configuración global;
- no se ejecuta Paso 3, implementa, formaliza slices, publica ni crea commits.

El documento puede terminar con una ruta posterior verificable o un bloqueo. No
declara aislamiento, autenticación o reversión demostrados sin la comprobación
viva separada y expresamente autorizada.

## 2. Baseline separado por versión — R-OTEL-C12-01

### 2.1. Antecedente histórico conservado

Codex CLI 0.157.1 aceptó `--no-daemon`, `--strict-config` y `-c`. El reintento
v1.1 demostró que el override de `projects.<ruta>.trust_level` podía persistir la
ruta en la configuración personal antes de enviar una tarea. Ese resultado sigue
siendo válido para aquel intento; no prueba el comportamiento de otra versión.

### 2.2. Baseline actual de solo lectura

| ID | Evidencia del 2026-09-28 | Consecuencia |
|---|---|---|
| F12-01A | `command -v codex` → `/opt/homebrew/bin/codex`; resolución → `/opt/homebrew/lib/node_modules/@openai/codex/bin/codex.js`; `codex --version` → `codex-cli 0.158.0`. | 0.158.0 es el candidato actual del PATH, no una sesión efectiva bajo herdr. |
| F12-01B | La ayuda 0.158.0 conserva `--no-daemon`, `--strict-config`, `-c`, `--profile` y referencia a `CODEX_HOME`. | La sintaxis candidata existe; su conducta viva no está demostrada. |
| F12-02 | La ayuda y la documentación oficial conservan `--profile` como capa sobre la configuración base. | Los perfiles no aíslan la configuración personal y siguen descartados. |
| F12-03 | Codex usa `CODEX_HOME` para configuración y datos principales, pero `sqlite_home` toma `CODEX_SQLITE_HOME` cuando está definida y, en otro caso, `CODEX_HOME`; `log_dir` también es configurable. | Una raíz temporal no queda aislada si solo se fija `CODEX_HOME`; deben fijarse y conciliarse todas las raíces de escritura. |
| F12-04 | La documentación distingue almacenamiento de credenciales `file`, `keyring`, `auto` y `ephemeral`. | El almacenamiento no aporta ni autoriza por sí mismo una fuente de autenticación. |
| F12-05 | herdr 0.8.0 acepta argumentos del agente, pero `herdr agent start --help` no documenta variables de entorno por agente. | La propagación desde la pane al proceso hijo sigue sin demostrar. |
| F12-06 | El wrapper local 0.158.0 copia el entorno al hijo nativo; el runtime abre bases bajo `sqlite_home`; `lsof` solo muestra descriptores abiertos y el rollout nuevo puede diferir su archivo hasta `persist()`. | La comprobación debe fijar la raíz SQLite/log, usar un descriptor estable y autocomprobar el predicado; cero coincidencias sobre un rollout no materializado no prueban falla de propagación. |

Fuentes oficiales: [configuración avanzada](https://developers.openai.com/codex/config-advanced),
[referencia de configuración](https://developers.openai.com/codex/config-reference)
y [autenticación](https://developers.openai.com/codex/auth).

**Gate de deriva B0:** inmediatamente antes de cualquier comprobación viva se
repiten únicamente ruta resuelta, versión y ayudas pertinentes. Si cambia la ruta,
la versión, un flag necesario o la semántica oficial aplicable, STOP: actualizar
este baseline y revisarlo antes de abrir Codex o herdr. El resultado 0.157.1 no se
usa para declarar PASS de 0.158.0 ni de una versión posterior.

## 3. Opciones conservadas y descartadas

| Opción | Estado | Motivo |
|---|---|---|
| Perfil temporal de Codex | DESCARTADA | Se superpone a la configuración base; no prueba aislamiento. |
| Override `trust_level` de v1.1 | DESCARTADA | Produjo una escritura real en la configuración personal. |
| Confiar globalmente la ruta de prueba | FUERA DE ALCANCE | Modifica configuración personal. |
| Copiar `auth.json` o cualquier credencial | PROHIBIDA | Expone y duplica secretos. |
| Raíz temporal única con `CODEX_HOME`, `CODEX_SQLITE_HOME`/`sqlite_home` y `log_dir` | CANDIDATA CORREGIDA; NO DEMOSTRADA | La documentación respalda las raíces; faltan propagación, vínculo al PID e inmutabilidad observadas bajo la nueva topología. |

La topología candidata no habilita ejecución. Debe pasar la revisión dirigida de
v1.2-r3 y después recibir una autorización nueva de preflight.

### 3.1. Topología de control obligatoria para H-C4

El próximo preflight no puede ser dirigido desde una sesión Codex que use el
estado personal inventariado. Debe usar un supervisor externo previamente
revisado que funcione sin leer contenido y persista solo evidencia sanitizada.
Antes del baseline y hasta terminar la comparación/reversión:

- todos los clientes Codex que usen el estado personal deben estar cerrados;
- si el supervisor no puede demostrar esa ausencia por metadatos de procesos,
  produce STOP antes de crear la pane o abrir login;
- el supervisor toma el inventario inicial, prepara la raíz temporal, inicia y
  observa herdr/Codex, coordina el cierre y compara el inventario final;
- ninguna sesión Codex puede leer resultados durante esa ventana; una sesión
  posterior solo puede abrir el resultado sanitizado después del cierre.

No se excluyen rutas que cambien ni se descuentan escrituras de una controladora.
Una diferencia conserva H-C4 FAIL.

## 4. Decisión de autenticación previa — R-OTEL-C12-02

Fuente y almacenamiento son decisiones separadas. `ephemeral` puede impedir que
una credencial ya obtenida se guarde en disco; no crea una credencial ni autoriza
usar una existente.

| ID | Fuente candidata | Almacenamiento propuesto | Señal efectiva exigida | Estado |
|---|---|---|---|---|
| A0 | Ninguna | Ninguno | No existe señal posible. Es el control negativo: siempre deja H-C3 BLOCKED aunque Codex muestre una interfaz lista o no pida login. | CONTROL NEGATIVO; NO ELEGIBLE PARA PASS |
| A1 | Credencial ya disponible en el keyring del sistema | Keyring existente; nada en la raíz temporal | `AUTH_OK` debe informar método `keyring` desde el proceso exacto o un verificador oficial dirigido a la misma raíz y fuente. También debe existir un oráculo aprobado de no escritura en keyring. | NO SELECCIONADA |
| A2 | Login interactivo realizado directamente por el usuario dentro del mismo Codex temporal | `ephemeral`, observado sin `auth.json` en el preflight anterior | `/usage` debe producir `AUTH_OK` con método `interactive_ephemeral` para la raíz temporal y el proceso exacto, sin enviar tarea. El mensaje de login exitoso por sí solo no alcanza. | SELECCIONADA; H-C3 PASS histórico, requiere nuevo preflight integral |
| A3 | Token o clave de prueba gestionado fuera del agente | `ephemeral`, sujeto a aceptación real de 0.158.0 | `AUTH_OK` debe informar método `managed_ephemeral` para la raíz temporal y el proceso exacto; presencia de variable o secreto no prueba aceptación. | NO SELECCIONADA |
| A4 | Copia desde `~/.codex/auth.json` o secreto pegado en chat/comando visible | Cualquiera | No se define señal porque la fuente está prohibida aunque técnicamente funcione. | DESCARTADA |

**D12-AUTH — A2 seleccionada y conservada:** el usuario eligió login interactivo
dentro del mismo Codex temporal, almacenamiento `ephemeral` y `/usage` como
verificador sin tarea. A0 queda disponible únicamente como prueba negativa;
A1/A3 no están seleccionadas y A4 sigue prohibida. La decisión no autoriza otro
login o preflight: esa ejecución requiere un permiso explícito posterior a la
revisión de v1.2-r3.

Antes de abrir una pane debe existir un registro sin secretos con: opción elegida,
quién la autorizó, almacenamiento esperado, mecanismo previsto para obtener
`AUTH_OK`, posibles efectos externos y STOP.

`AUTH_OK` es una evidencia sanitizada, no una afirmación de la interfaz. Debe
contener exclusivamente versión del contrato, opción A2, clase de método,
`authenticated=true`, referencia digerida del proceso hijo, instante y clase de
verificador. Solo se admite si proviene de un mecanismo oficial documentado que
compruebe una sesión efectiva para esa misma raíz/fuente, o de una comprobación
de autenticación sin tarea expresamente autorizada. No persiste identidad de
cuenta, token, valor de variable, respuesta del servicio ni contenido. Si no se
puede definir y observar ese mecanismo para la opción elegida, H-C3 queda
BLOCKED antes de cualquier tarea.

Una pantalla de login, solicitud de secreto, creación de `auth.json`, acceso a una
fuente distinta, presencia de credencial, código de salida, ausencia de error o
imposibilidad de probar ausencia de escritura global detiene la comprobación
antes de enviar una tarea.

## 5. Gates obligatorios corregidos

Un eventual preflight solo puede solicitarse después de aprobar este contrato y
revalidar que D12-AUTH/A2 conserva sus condiciones. Todos los gates son obligatorios:

1. **H-C1 — raíz aislada observada:** la raíz temporal parte con permisos privados
   y configuración mínima conocida. `CODEX_HOME`, `CODEX_SQLITE_HOME`,
   `sqlite_home` y `log_dir` resuelven dentro del mismo árbol; el historial queda
   desactivado y el almacenamiento de autenticación es `ephemeral`. Codex crea
   su estado atribuible únicamente allí. No basta con que `config.toml` personal
   conserve su hash.
2. **H-C2 — lanzamiento y propagación observados:** se registra una cadena
   sanitizada `herdr → PID hijo nativo → ejecutable/versión → descriptor
   SQLite/log temporal`. Las rutas relativas aceptables del descriptor quedan en
   una allowlist cerrada del supervisor antes de ejecutar. Antes de abrir herdr,
   el supervisor autocomprueba el
   observador con un descriptor centinela propio: el caso positivo debe aparecer
   solo al combinar con AND el PID conocido y la raíz temporal, y los controles
   de PID o raíz incorrectos deben dar cero. Después, la relación padre/hijo
   proviene de metadatos del proceso y `lsof` combina con AND el PID nativo exacto
   con la raíz temporal; al menos un descriptor de la base SQLite o del log
   explícito debe coincidir con una ruta relativa conocida. Un rollout no
   materializado no se usa como único oráculo. La evidencia persiste solo
   booleanos, ejecutable/versión y referencias digeridas de PID/ruta; no vuelca
   entorno, nombres personales ni contenido. Autocomprobación fallida, descriptor
   fuera de la raíz, variable visible sin vínculo, prompt listo o archivo sin
   vínculo al hijo deja H-C1/H-C2 BLOCKED.
3. **H-C3 — autenticación aprobada y acotada:** la fuente coincide con D12-AUTH,
   el almacenamiento observado coincide con lo autorizado, existe `AUTH_OK` para
   el mismo hijo y no aparece contenido de credenciales en salida, comandos,
   evidencias o raíz temporal. A0 siempre bloquea; `ephemeral`, interfaz lista,
   presencia de secreto o ausencia de error no prueban autenticación efectiva.
4. **H-C4 — estado personal intacto y reversión:** el supervisor externo de §3.1,
   con todos los clientes Codex personales cerrados durante toda la ventana,
   compara antes y después un
   inventario recursivo de metadatos para `config.toml`, `auth.json`,
   `history.jsonl` y cada entrada bajo sesiones, logs y cachés. El recolector no
   sigue symlinks ni abre contenido; convierte cada ruta a un identificador HMAC
   con clave efímera antes de emitirla y persiste solo tipo, existencia,
   dispositivo/inode, tamaño y tiempos de alta resolución. La clave se conserva
   solo en memoria hasta comparar pre/post y luego se destruye. Creación, borrado,
   cambio de metadatos, error de recorrido o symlink que escape del árbol produce
   STOP, incluso si el directorio padre parece intacto. Antes del baseline deben
   existir cero procesos Codex; durante la ventana solo se admite el árbol de
   procesos exacto iniciado por el supervisor. Cualquier proceso adicional o una
   ausencia no demostrable deja el gate BLOCKED antes de la pane o FAIL si surge
   después. La raíz temporal debe poder eliminarse por completo al cerrar, y solo
   entonces otra sesión puede leer el resultado.
5. **H-C5 — límites del eventual piloto conservados:** fixture artificial,
   `--no-daemon`, sandbox de solo lectura, receptor local sanitizado y lectura
   posterior limitada a `session_meta` y `token_usage_record` de la sesión exacta.

A1/A3 permanecen como alternativas históricas no seleccionadas. Este contrato no
habilita keyring, token gestionado ni cambio de fuente sin una decisión nueva.

No se sustituye H-C1–H-C5 por perfiles, tiempos de arranque, ausencia de diálogo,
un mensaje de la interfaz, strings del binario o solo el hash de `config.toml`.

## 6. Recorrido futuro condicionado — R-OTEL-C12-03

### Bloque B0 — revalidar el baseline sin abrir procesos interactivos

- **Criterio cubierto:** R-OTEL-C12-01.
- **Entrada:** contrato revisado y una autorización futura de preflight.
- **Cambio mínimo:** ninguno; leer ruta/versión/ayudas.
- **Comprobación:** coincidencia exacta con §2.2.
- **Resultado:** baseline vigente o deriva registrada sin proceso interactivo.
- **Finalización:** PASS habilita B1; cualquier deriva produce STOP documental.

### Bloque B1 — resolver autenticación antes de herdr

- **Criterios cubiertos:** R-OTEL-C12-02 y H-C3.
- **Entrada:** D12-AUTH/A2 ya aprobada por el usuario y contrato v1.2-r3 revisado.
- **Cambio mínimo:** revalidar sin secretos la opción A2, almacenamiento
  `ephemeral`, `/usage` como clase exacta de verificador `AUTH_OK` y STOP. A0
  solo se conserva como control negativo.
- **Comprobación:** la ruta no requiere que el agente lea/copie credenciales ni
  ejecuta un login no autorizado, y el verificador demuestra autenticación
  efectiva en vez de presencia o apariencia de disponibilidad.
- **Resultado:** A2 y su verificador continúan vigentes o se registra deriva.
- **Finalización:** A2 sin deriva habilita B2; A0, otra fuente o ausencia de señal
  válida mantiene INFORMACIÓN INSUFICIENTE sin abrir pane.

### Bloque B2 — preparar aislamiento y baseline de estado

- **Criterios cubiertos:** R-OTEL-C12-03, H-C1 y H-C4 previo.
- **Entrada:** B0/B1 PASS.
- **Cambio mínimo:** fuera de toda sesión Codex, iniciar el supervisor externo
  revisado; demostrar cero procesos Codex preexistentes; crear una raíz
  temporal privada con `CODEX_HOME`, `CODEX_SQLITE_HOME`/`sqlite_home` y
  `log_dir` fijados dentro de ella, historial desactivado y autenticación
  `ephemeral`; preparar una sola pane sin cambiar launcher o globales.
- **Comprobación:** el supervisor autocomprueba el predicado H-C2 con centinela
  positivo y controles negativos, emite el inventario H-C4 digerido y verifica
  que las raíces previstas no escapen del temporal. No vuelca entorno, rutas
  personales ni contenido y no copia configuración, historial, sesiones o
  credenciales personales.
- **Resultado:** entorno temporal y oráculos preparados, o bloqueo previo si el
  host no puede producir esa evidencia sin ampliar permisos/dependencias.
- **Finalización:** entorno preparado; cualquier discrepancia es STOP.

### Bloque B3 — preflight vivo sin tarea

- **Criterios cubiertos:** H-C1, H-C2, H-C3 y H-C4.
- **Entrada:** autorización específica posterior que cubra supervisor, pane,
  proceso, login/red A2; B0–B2 PASS y cero procesos Codex preexistentes.
- **Cambio mínimo:** el supervisor inicia un solo Codex bajo herdr con
  `--no-daemon`; el usuario completa A2 en ese proceso; no se envía tarea,
  fixture o prompt.
- **Comprobación:** cadena completa H-C2 mediante descriptor SQLite/log del PID
  nativo exacto, `AUTH_OK` del mismo hijo y ausencia de todo proceso Codex ajeno
  al árbol iniciado por el supervisor. El inventario final se difiere a B4.
- **Resultado:** gates observados como PASS/BLOCKED/FAIL sin consumir una tarea.
- **Finalización:** H-C1–H-C4 PASS habilita solicitar un piloto separado. Un gate
  BLOCKED/FAIL cierra proceso y pane externamente, revierte el temporal y detiene.

### Bloque B4 — reversión y evidencia reducida

- **Criterios cubiertos:** H-C4 y límite de privacidad.
- **Entrada:** salida controlada de B3, cualquiera sea su resultado.
- **Cambio mínimo:** el mismo supervisor externo cierra pane/proceso, elimina la
  raíz temporal y recién entonces toma el inventario final. Ninguna sesión Codex
  se inicia durante esta secuencia.
- **Comprobación:** inventario final entrada por entrada igual al inicial,
  temporal ausente, ausencia de procesos Codex ajenos sostenida, clave HMAC
  destruida y evidencia limitada a versiones, estados, booleanos, referencias
  digeridas y metadatos permitidos.
- **Resultado:** reversión demostrada o diferencia global bloqueante.
- **Finalización:** reversión PASS y resultado sanitizado cerrado. Una diferencia
  global exige detenerse y pedir autorización específica para diagnosticar; no
  se repara ni abre otra sesión automáticamente. Solo después puede una sesión
  nueva leer el resultado reducido.

Solo después de B0–B4 PASS puede proponerse, con otra autorización, el piloto de
H-C5. Paso 3 continúa fuera de alcance.

## 7. Validación del contrato corregido

La próxima revisión documental debe comprobar exclusivamente:

| Caso | Resultado exigido |
|---|---|
| Deriva de ejecutable o versión | STOP antes de abrir herdr; 0.157.1 queda histórico. |
| A0, interfaz lista o `ephemeral` sin fuente efectiva | H-C3 BLOCKED; nunca habilita una tarea. |
| A1–A3 sin `AUTH_OK`, con método distinto o sin vínculo al hijo | H-C3 BLOCKED y cierre previo a cualquier tarea. |
| Fuente distinta de D12-AUTH o login inesperado | STOP sin pedir ni registrar secreto. |
| Alguna raíz de escritura resuelve fuera del temporal | H-C1/H-C2 BLOCKED antes del login. |
| Autocomprobación positiva/negativa del observador no discrimina PID y raíz | H-C2 BLOCKED antes de abrir herdr. |
| Variable visible o archivo temporal sin descriptor SQLite/log ligado con AND al PID nativo | H-C1/H-C2 BLOCKED; no se presume propagación. |
| Rollout aún no materializado y sin otro descriptor estable | H-C2 BLOCKED; cero coincidencias no prueban propagación fallida. |
| Proceso Codex preexistente, proceso ajeno al árbol controlado o ausencia no demostrable | H-C4 BLOCKED antes de la pane o FAIL si aparece después. |
| Archivo interno personal cambia aunque el directorio padre no | El inventario recursivo produce H-C4 FAIL y reversión controlada. |
| Symlink escapando o recorrido incompleto | H-C4 BLOCKED/FAIL; no se declara inmutabilidad. |
| Estado personal intacto, cadena atribuible y `AUTH_OK` válido | Solo habilita pedir autorización para el piloto H-C5; no lo ejecuta. |

No hacen falta pruebas de producto, sesiones o pilotos para revisar estas reglas.

## 8. Resultado de la corrección

R-OTEL-C12-01/02/03 permanecen cerrados y A2/D12-AUTH continúa seleccionada. La
corrección v1.2-r3 no atribuye los tres cambios HMAC del intento fallido.

H-C2 fija todas las raíces de escritura relevantes, autocomprueba el observador
y exige un descriptor SQLite/log estable ligado mediante AND al PID nativo
exacto. H-C4 traslada baseline, coordinación, comparación y reversión a un
supervisor externo, sin clientes Codex personales activos durante la ventana.

La viabilidad operativa sigue sin demostrarse: H-C1–H-C4 requieren una nueva
comprobación viva con autorización propia después de revisar este contrato.

**ESTADO: PLAN_CON_INCERTIDUMBRE_CRITICA.** Listo para revisión dirigida solo de
H-C2, H-C4 y efectos directos; no habilita sesión, login, preflight, piloto, H-C5
o Paso 3.

## 9. Próxima acción única

Revisar este contrato v1.2-r3 con `04_REVISAR_PLAN.md`, únicamente sobre H-C2,
H-C4 y los efectos directos de la corrección. Verificar raíces temporales,
autocomprobación y vínculo al PID, topología del supervisor, ausencia de clientes
personales, inventario/reversión y casos negativos. No reabrir A2, P1–P4,
R-OTEL-C12-01/02/03 o cierres anteriores, corregir el contrato, abrir procesos,
sesiones, panes o login ni ejecutar preflight, H-C5 o Paso 3 durante la revisión.
