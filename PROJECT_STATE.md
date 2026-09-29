# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** blocked
- **Current phase:** project-work-activity-attribution — contrato OTel v1.2-r3 corregido; revisión dirigida H-C2/H-C4 pendiente
- **Active requirement:** docs/requirements/project-work-activity-attribution/STATE.md
- **Last completed requirement:** docs/requirements/project-work-history/STATE.md
- **Last closed requirement:** docs/requirements/project-work-history/STATE.md — complete-with-notes
- **Current slice:** none; preflight A2 cerrado y entorno temporal revertido
- **Completed:** atribución por actividad A01–A03 con 11/11 nuevas y 46/46 regresiones PASS; histórico prospectivo H01/H02 con 46/46 pruebas afectadas PASS; S01/S02 del observador validadas offline y S03 reconciliada en una tarea habitual acotada; rc.2 publicada; discovery integrado; benchmark v1 cerrado como `beneficio no probado`; v2.1 cerrado por cancelación tras P2; recurrencia de Skills cerrada; cierres documentales integrados por PR #5.
- **Pending:** revisar documentalmente v1.2-r3 antes de cualquier nueva ejecución. P1–P4 y todos los cierres se conservan; H-C5/Paso 3 siguen fuera de alcance.
- **Next action:** autorizar la revisión dirigida de OTel v1.2-r3, limitada a H-C2, H-C4 y efectos directos, sin ejecutar el preflight
- **Why this is next:** la corrección ya fija todas las raíces de escritura y elimina la sesión controladora del inventario, pero aún debe comprobarse que el contrato sea coherente y ejecutable sin debilitar los gates
- **User action required:** true — autorizar la revisión documental acotada
- **Decision required:** aceptar o no que v1.2-r3 pase a revisión técnica dirigida
- **Expected output:** veredicto APROBADO, APROBADO CON NOTAS, REQUIERE_AJUSTES o INFORMACION_INSUFICIENTE sobre H-C2/H-C4
- **After this:** si el review cierra, solicitar aprobación del contrato concreto antes de preparar cualquier nuevo preflight
- **Blocked by:** contrato v1.2-r3 corregido pero todavía no revisado ni aprobado
- **Runtime limitation:** none
- **Resume instruction:** Autorizar únicamente la revisión dirigida de v1.2-r3 preparada en HANDOFF.md; no corregir el contrato ni repetir login, preflight, H-C5 o Paso 3.

## Corrección contractual OTel v1.2-r3 — 2026-09-29

Se corrigió únicamente H-C2, H-C4 y sus efectos directos conforme al diagnóstico
autorizado. El contrato actual tiene SHA-256
`ac685955886ba10a1171a5f7787c0d0195613661215f2cd400ded35097da60ad`.

H-C2 ahora fija `CODEX_HOME`, `CODEX_SQLITE_HOME`/`sqlite_home` y `log_dir`
dentro de una raíz temporal, exige autocomprobación positiva/negativa del
observador y vincula el PID nativo exacto con un descriptor SQLite/log conocido.
H-C4 exige cero procesos Codex preexistentes y un supervisor externo que tome el
baseline, coordine el preflight, cierre/revierta y compare antes de permitir otra
sesión Codex.

A2/D12-AUTH permanece seleccionada; P1–P4, R-OTEL-C12-01/02/03 y todos los
cierres anteriores permanecen intactos. La corrección no atribuye los tres
cambios HMAC históricos ni demuestra aún viabilidad operativa. No se abrió
proceso, pane, login o red ni se ejecutó preflight, H-C5 o Paso 3.

## Diagnóstico H-C2/H-C4 de solo lectura cerrado — 2026-09-29

H-C2 puede transformarse en una prueba concluyente, pero el contrato vigente no
lo logra. `lsof` solo muestra descriptores abiertos en el instante observado y
Codex 0.158.0 puede demorar la creación del archivo de sesión hasta una
persistencia explícita. Además de `CODEX_HOME`, Codex reconoce una raíz SQLite
separada mediante `CODEX_SQLITE_HOME`/`sqlite_home`; el wrapper 0.158.0 entrega
el entorno heredado completo al binario nativo. El intento no conservó evidencia
del valor efectivo de esa raíz y no corresponde inferir que haya causado el
resultado.

La corrección mínima propuesta fija `CODEX_HOME`, la raíz SQLite y `log_dir`
dentro del mismo árbol temporal y exige una autocomprobación del observador antes
del login. La cadena debe unir el PID nativo exacto con un descriptor SQLite o
log conocido usando selecciones AND, sin volcar entorno, rutas o contenido.

H-C4 no es un oráculo válido mientras la sesión Codex que dirige la prueba siga
activa: esa sesión puede actualizar rollouts y bases de estado dentro del mismo
árbol personal que se compara. Esto demuestra contaminación posible del control,
pero no identifica la causa de los tres HMAC cambiados. La corrección mínima
traslada baseline, coordinación, comparación y reversión a un supervisor externo
revisado, ejecutado con todos los clientes Codex del estado personal cerrados;
una sesión posterior lee únicamente el resultado sanitizado.

No se modificó el contrato, abrió proceso/pane/login/red, leyó sesión, credencial,
ruta personal cambiada o valor de configuración, ni se ejecutó H-C5/Paso 3. El
contrato conserva SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.

## Preflight A2 H-C1–H-C4 cerrado — 2026-09-28

B0 pasó con Codex 0.158.0, herdr 0.8.0 y el contrato aprobado intacto. El login
interactivo se completó dentro del mismo Codex temporal y `/usage` produjo un
`AUTH_OK` sanitizado, por lo que H-C3 pasó sin persistir datos de cuenta,
importes, límites ni contenido.

H-C2 quedó bloqueado: 13.130 observaciones mantuvieron vivo el proceso exacto,
pero ninguna mostró un vínculo directo entre ese proceso y un artefacto de la
raíz temporal. H-C4 falló: el inventario personal conservó 1.244 entradas, cero
errores y cero symlinks, pero registró tres cambios identificados solo mediante
HMAC. No se leyeron sus nombres ni contenidos y no se les atribuye una causa.
Por dependencia, H-C1 queda bloqueado. B4 cerró el proceso y la pane y eliminó
por completo la raíz temporal, pero no puede declarar igualdad del estado
personal.

Resultado global: FAIL/BLOCKED. No se envió tarea, fixture o inferencia; no se
ejecutó H-C5/Paso 3. `auth.json` no apareció. El contrato conserva SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
P1–P4 y todos los hallazgos y cierres anteriores permanecen intactos.

## Investigación de viabilidad A2 — 2026-09-28

La investigación de solo lectura encontró un camino sustentado, todavía no
probado: iniciar el Codex final bajo herdr con raíz temporal, `--no-daemon` y
credenciales `ephemeral`; completar el login dentro de ese mismo proceso; y usar
`/usage` allí como comprobación sin tarea, conservando solo un `AUTH_OK`
sanitizado. Un proceso previo de `codex login` no puede transferir credenciales
`ephemeral` al proceso final.

Codex CLI 0.158.0, herdr 0.8.0, el wrapper local y la documentación oficial
sustentan las piezas. La propagación real, el login, la aceptación de
`ephemeral`, la respuesta autenticada y el estado personal intacto siguen sin
demostrarse y requieren una autorización posterior. A2 fue seleccionada para
D12-AUTH bajo la condición de mismo proceso; el contrato aprobado no fue modificado. No se
abrieron procesos o sesiones ni se leyeron configuración, credenciales o
sesiones. P1–P4 y todos los hallazgos y cierres anteriores permanecen intactos.

## D12-AUTH resuelta con A2 — 2026-09-28

El usuario seleccionó A2: login interactivo dentro del mismo Codex temporal bajo
herdr, credenciales solo en memoria y `/usage` como comprobación sin tarea. La
decisión quedó registrada en
[02_DECISION.md](docs/requirements/project-work-activity-attribution/02_DECISION.md).
No autoriza todavía pane, proceso, navegador, login o red. El permiso concreto
para una única ejecución H-C1–H-C4 quedó preparado en HANDOFF.md.

## Plan OTel v1.2 — bloques por categoría incorporados 2026-09-28

El usuario aceptó «Dale, hazlo» para incorporar al plan la organización de tareas
por categoría dentro de cada slice. P4 registra esa decisión; no autoriza código,
otro piloto ni una nueva revisión en esta edición. P1–P3 conservan su aprobación.

[Plan v1.2](Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md), SHA-256
`53ae25ef657d8549b54f325af34ba15073bb56d131d423f6572e2cba726deb64`: categorías propuestas por Quiver, límites automáticos previstos,
retornos test→bug→test, mezcla verificable, interrupciones e histórico versionado.
La etiqueta prevista no prueba exclusividad de consumo. USD sin evidencia y
activo unknown se mantienen. El contrato de aislamiento v1.2 es otro documento,
continúa con INFORMACIÓN INSUFICIENTE y no se modificó.

Estado: PLAN_CON_INCERTIDUMBRE_CRITICA. Revisión v1.1 válida solo para su hash;
delta P4 pendiente. HANDOFF y WIREFRAME se sincronizaron con el estado, retirando
la reanudación obsoleta que ofrecía repetir Etapa C v1. Evidencia en
[registro del requirement](docs/requirements/project-work-activity-attribution/EVIDENCE.md).
No se ejecutaron pruebas de producto, sesiones ni cambios de código/configuración.

## Review dirigido del plan OTel v1.2/P4 — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.** Se revisó únicamente P4 y sus efectos directos,
contra el plan SHA-256 `53ae25ef657d8549b54f325af34ba15073bb56d131d423f6572e2cba726deb64`.
[Resultado completo](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md#ronda-dirigida--plan-otel-v12--p4--2026-09-28).

R-OTEL-P4-01 exige retirar referencias que tratan P1–P3 como pendientes. P1–P4
siguen aprobadas. R-OTEL-P4-02 exige definir cómo una unidad indivisible enlazada
a dos bloques iguales aparece en el detalle sin duplicarse en las sumas. La
organización propuesta es coherente, pero no debe formalizarse mientras esas dos
lecturas produzcan resultados diferentes.

El contrato de aislamiento OTel v1.2 permanece separado, pendiente y con
INFORMACIÓN INSUFICIENTE. No se revisó ni aprobó por extensión. No hubo código,
piloto, sesión, lectura de credenciales, dependencias, publicación o commit.

## Corrección dirigida del plan OTel v1.3 — 2026-09-28

El usuario autorizó con «Apruebo» la única acción pendiente: corregir
R-OTEL-P4-01/02 sin implementar ni iniciar otra revisión. El plan actual,
SHA-256 `48827d6014612796b42cd5982bb640c229fad1f524e2cfbefa82590a576d2209`,
reconoce P1–P4 como decisiones aprobadas y separa la evidencia técnica pendiente.

Para una medición indivisible compartida entre bloques de la misma categoría,
define un único propietario contable `shared_within_category`; cada bloque solo
la referencia sin volver a sumarla. JSON, texto, detalle y totales deben probar
la misma identidad y conciliación. No es una actividad nueva ni un reparto.

Estado: PLAN_CON_INCERTIDUMBRE_CRITICA, listo para review dirigido de los dos
hallazgos. Contrato de aislamiento v1.2, cierres y código permanecen intactos.
No hubo sesiones, pilotos, pruebas de producto, dependencias, publicación o commit.

## Review dirigido del plan OTel v1.3 — 2026-09-28

**VEREDICTO: APROBADO.** Se revisaron únicamente R-OTEL-P4-01/02 y sus efectos
directos contra el plan SHA-256
`48827d6014612796b42cd5982bb640c229fad1f524e2cfbefa82590a576d2209`.
[Resultado completo](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md#ronda-dirigida--plan-otel-v13--cierre-p4--2026-09-28).

P1–P4 permanecen aprobadas. La evidencia técnica todavía pendiente no vuelve a
presentarse como decisión humana. Una unidad compartida entre bloques iguales
suma una sola vez en la categoría, mientras ambos bloques muestran referencias
no aditivas a la misma identidad; JSON, texto, detalle e histórico deben
conciliar con los totales. El detalle desconocido sigue visible y no puede
satisfacer P3 cuando sea obligatorio.

R-OTEL-P4-01/02 quedan cerrados, junto con R-OTEL-01–03 y los cierres anteriores.
El contrato de aislamiento v1.2 continúa separado, con INFORMACIÓN INSUFICIENTE
y sin aprobación por extensión. No hubo modificaciones al plan, código, spec,
slices, sesiones, pilotos, dependencias, publicación o commit.

## Review dirigido del contrato OTel v1.2 — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.** El contrato conserva SHA-256
`98c85652b24c86b68fddb8dbe20cca8d00f334d8f53dec05888b47f875a1692a`.
[Resultado completo](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12--aislamiento--2026-09-28).

El ejecutable actual informa Codex 0.158.0, mientras el contrato se apoya en
0.157.1. Además, debe separar la fuente de autenticación de su almacenamiento y
reforzar la prueba de que herdr transmite la raíz temporal sin usar otros estados
personales. Quedan abiertos R-OTEL-C12-01/02/03.

No se modificó el contrato ni se abrió Codex/herdr, sesión, piloto o login. No
se leyeron credenciales, sesiones o valores de configuración. P1–P4,
R-OTEL-01–03, R-OTEL-P4-01/02 y cierres anteriores permanecen intactos.

## Corrección dirigida del contrato OTel v1.2-r1 — 2026-09-28

Se corrigieron únicamente R-OTEL-C12-01/02/03. El contrato conserva su ruta,
queda identificado como v1.2-r1 y tiene SHA-256
`5647887786d52a22ef8056c25e9109b5ebcebfb92ba9865369424f5889d98a5d`.

El documento separa Codex 0.157.1 histórico del baseline actual 0.158.0; obliga
a detenerse ante otra deriva. D12-AUTH distingue fuente y almacenamiento de
credenciales sin elegir una opción. H-C1–H-C4 y B0–B4 exigen un artefacto
atribuible en la raíz temporal, metadatos personales intactos y reversión.

Estado PLAN_CON_INCERTIDUMBRE_CRITICA, listo únicamente para review dirigido.
No se abrió Codex/herdr, pane, sesión, login o piloto; no se leyeron secretos o
sesiones ni se modificó configuración, router o launcher.

## Review dirigido del contrato OTel v1.2-r1 — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.** Se revisó el hash
`5647887786d52a22ef8056c25e9109b5ebcebfb92ba9865369424f5889d98a5d`.
[Resultado completo](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12-r1--seguimiento--2026-09-28).

R-OTEL-C12-01 queda cerrado. R-OTEL-C12-02 sigue abierto porque A0 puede avanzar
sin demostrar autenticación efectiva. R-OTEL-C12-03 sigue abierto porque el
contrato no vincula inequívocamente el proceso hijo con la raíz temporal ni
garantiza detectar cambios dentro de árboles personales ya existentes.

No se modificó el contrato ni se resolvió D12-AUTH. No se abrieron procesos,
sesiones, login o piloto ni se leyeron credenciales/configuración. Cierres y
aprobaciones anteriores permanecen intactos.

## Corrección dirigida del contrato OTel v1.2-r2 — 2026-09-28

Se corrigieron únicamente R-OTEL-C12-02/03. El contrato actual tiene SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
A0 ahora es un control negativo que nunca autentica por sí solo; A1–A3 requieren
una señal `AUTH_OK` efectiva, sanitizada y vinculada al proceso exacto.

La propagación exige una cadena entre herdr, el hijo, el ejecutable y un artefacto
temporal. La inmutabilidad personal se compara recursivamente con identificadores
digeridos y metadatos, sin leer contenido ni persistir nombres reales. Una prueba
incompleta bloquea el recorrido.

R-OTEL-C12-01 sigue cerrado; R-OTEL-C12-02/03 esperan review. D12-AUTH no fue
resuelto y no se abrieron procesos, sesiones, login o piloto.

## Review dirigido del contrato OTel v1.2-r2 — 2026-09-28

**VEREDICTO: APROBADO. Sin observaciones accionables.** Objeto SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
[Resultado completo](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12-r2--cierre-c12--2026-09-28).

A0 es siempre bloqueante; A1–A3 requieren `AUTH_OK` efectivo y vinculado al
mismo hijo. La cadena al proceso y el inventario recursivo impiden aprobar el
aislamiento con una señal incompleta. R-OTEL-C12-02/03 quedan cerrados junto con
R-OTEL-C12-01.

La viabilidad viva continúa sin demostrar. D12-AUTH debe resolverse antes de
preparar cualquier comprobación. No se modificó el contrato ni se abrieron
procesos, sesiones, login o piloto.

## Autorización del reintento aislado OTel v1.1 — 2026-09-28

El usuario autorizó una sola ejecución de §9 con `--no-daemon`, trust efímero,
fixture/receptor v1.1 y lectura limitada a `session_meta` y
`token_usage_record` de la sesión exacta. La sintaxis de los overrides pasó con
exit `0`; hash y stat de `~/.codex/config.toml` permanecieron intactos. La tarea
artificial todavía no se envió al registrar este corte.

## Reintento aislado OTel v1.1 — BLOCKED en preflight 2026-09-28

Herdr abrió la pane con Codex 0.157.1, `--no-daemon` y los overrides exactos.
No hubo diálogo de confianza, pero el control previo a la tarea detectó una
mutación del TOML global y una coincidencia de la ruta v1.1. La pane se cerró sin
enviar teclas ni tarea; no se leyó ninguna sesión ni se ejecutaron conciliación
o prueba negativa.

Pane, proceso, receptor, puerto y árbol temporal quedaron ausentes. En ese corte
la ruta persistía y no se editó, conforme al contrato. G-C1/G-C7 BLOCKED;
G-C3–G-C6 no ejecutados. Evidencia en
`docs/requirements/project-work-activity-attribution/EVIDENCE.md`.

### Reparación dirigida completada

El usuario autorizó la reparación. Se guardó un backup privado `0600` del TOML
mutado y se eliminó únicamente la tabla de trust v1.1. La ruta quedó ausente y
el hash actual es
`536f8d4b5fba477f17f0a3857c5d58b304798fa71fed609ffd0c37c8877b96ce`.
No se abrió Codex ni se repitió el piloto. El residuo está cerrado; el veredicto
BLOCKED de v1.1 permanece.

## OTel v1.2 — preparado para revisión 2026-09-28

La exploración fue solo de lectura. La documentación y ayuda local descartan
perfiles porque siempre superponen la configuración sobre `~/.codex/config.toml`.
El binario reconoce `CODEX_HOME`, pero no se demostró que herdr lo propague ni
que Codex pueda autenticarse con una raíz temporal sin leer/copiar credenciales.

Se creó [OTEL_PILOT_CONTRACT_v1.2.md](docs/requirements/project-work-activity-attribution/OTEL_PILOT_CONTRACT_v1.2.md), con veredicto **INFORMACIÓN INSUFICIENTE**,
F12-01–F12-05 y H-C1–H-C5. No se inició Codex o herdr de forma interactiva, no
hubo sesión o piloto y no se cambió configuración. El único siguiente paso es review dirigido del
contrato; no habilita otro reintento ni Paso 3.

## Autorización de Etapa C/Paso 2 — 2026-09-28

El usuario autorizó explícitamente la lista cerrada §9 de
`docs/requirements/project-work-activity-attribution/OTEL_PILOT_CONTRACT.md`:
una única sesión Codex nueva bajo herdr, fixture artificial, receptor temporal
Python en loopback, overrides OTel efímeros y lectura limitada a `session_meta` y
contadores de esa sesión. Paso 3, contenidos, otras sesiones, dependencias,
Docker, red adicional, router, launcher, configuración global, publicación y
commit permanecen fuera de alcance.

## Etapa C/Paso 2 OTel — BLOCKED 2026-09-28

Se ejecutó una sola sesión piloto bajo herdr y una sola tarea artificial. La
referencia permitida produjo 2 respuestas y 46.398 tokens; OTel produjo 5
`response.completed`, ninguno con `response_id`, solo contadores parciales y dos
`conversation.id`. Uno corresponde a la sesión piloto; el otro no se identificó
ni se abrió. El daemon compartido contaminó el ámbito, la conciliación y la
prueba negativa quedaron `incomplete`, y Paso 3 no se habilita.

La persistencia sanitizada no mostró contenido del fixture/tarea ni credenciales.
Codex añadió transitoriamente confianza para la ruta temporal; se retiró solo
ese bloque y se verificó su ausencia. Pane y procesos quedaron cerrados. No se
instalaron dependencias, ejecutó Paso 3, clasificaron actividades, publicaron
cambios ni realizaron commits. Evidencia completa en
`docs/requirements/project-work-activity-attribution/EVIDENCE.md`.

## Corrección documental OTel v1.1 — 2026-09-28

Autorizada y completada sin ejecutar otra sesión. El contrato v1.1 exige
`--no-daemon`, trust por override efímero, configuración del usuario inmutable y
cierre externo antes de la tarea si aparece cualquier diálogo de confianza.
Normaliza solo claves exactas observadas/esperadas y conserva IDs como digest.

Los gates G-C1–G-C7 requieren una conversación aislada, privacidad,
`response_id` por unidad, seis contadores completos, conciliación exacta, prueba
de pérdida posterior a un original PASS y reversión. No se creó receptor o
fixture, no se abrió Codex/herdr, no se leyó ninguna sesión y no se cambió
configuración, código, router, launcher o dependencias. El reintento y Paso 3 no
están autorizados.

## Paso 1 OTel — contrato de piloto 2026-09-28

Completado documentalmente con la autorización «Continua con el siguinte paso».
El contrato v1 está en
`docs/requirements/project-work-activity-attribution/OTEL_PILOT_CONTRACT.md`.
Define Etapa C/Paso 2 de captura y reserva Etapa A/Paso 3 con autorización separada.

La próxima prueba propone una sola sesión nueva, fixture artificial, exportación
OTLP/HTTP JSON a loopback mediante overrides efímeros y conciliación con solo los
metadatos/contadores de esa sesión. No se instaló ni ejecutó nada; Docker, red
externa, hooks de actividad, otras sesiones y configuración global quedaron fuera.
La documentación oficial de OpenAI y el help local de herdr sustentan el contrato;
la viabilidad real permanece pendiente del Paso 2.

## Paso 0 OTel — auditoría de solo lectura 2026-09-28

Completado con la autorización específica del usuario. El inventario quedó en
`docs/requirements/project-work-activity-attribution/EVIDENCE.md#paso-0-otel--auditoría-de-solo-lectura-2026-09-28`.
Se verificaron herdr `0.8.0` y Codex CLI `0.157.1` desde el PATH de esta auditoría;
herdr es un binario nativo y su configuración no declara una ruta de Codex, por lo
que el ejecutable efectivo de una sesión gestionada por herdr sigue por demostrar.
La integración de estado `codex` de herdr figura como no instalada. No se encontró
configuración OTel en los archivos pertinentes ni una fuente automática de recibos
en Quiver; tampoco se abrió una sesión para comprobar emisión real.

Se localizaron como reutilizables el binding, ledger privado, recibos estructurados
y reportes JSON/texto de actividad. La auditoría no demuestra telemetría, cobertura
de captura, transiciones ni relación respuesta→acción. No se modificaron router,
launcher, configuración, código o dependencias; no se leyeron sesiones ni
credenciales, y no hubo piloto, publicación ni commit.

## Aprobación de OTel v1.1/P1–P3 — 2026-09-28

El usuario respondió «Apruebo los 3 puntos indicados» a la solicitud concreta
posterior al review. **APROBADO**, vinculado al hash
`e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`.
[Registro y alcance](docs/requirements/project-work-activity-attribution/STATE.md#aprobación-humana-registrada--2026-09-28).
Se aprueban agrupaciones/detalles, sustitución de Kev y aceptación acotada sin
pendientes; no ejecución, instalación ni pilotos. La aprobación permite
formalización dentro de las dependencias del plan; no elimina la comprobación
previa a la spec definitiva. Se conserva el plan revisado sin modificarlo.

## Revisión dirigida de OTel v1.1 — 2026-09-28

**APROBADO**, N2; R-OTEL-01–03 cerrados tras comprobar las correcciones y sus
efectos directos. [Resultado por referencia](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md#ronda-dirigida--otel-v11--2026-09-28).
Objeto: plan SHA-256 `e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`,
preservado sin cambios. Aprobación técnica del recorrido condicionado, no prueba
de integración ni aprobación humana. P1–P3 pendientes; sin nuevas pruebas,
pilotos, código ni reapertura de slices cerradas.

## Corrección del plan alternativo — 2026-09-28

Se corrigió el mismo [plan OTel v1.1](Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md)
aplicando [03_PLANIFICAR.md](../workflow_verificable/03_PLANIFICAR.md), solo para
R-OTEL-01–03. Incorpora matriz contra criterios/D01, decisiones P1–P3 pendientes,
histórico JSON/texto compatible y evidencia exigida de completitud. Detalle en
§12 y en [STATE](docs/requirements/project-work-activity-attribution/STATE.md).
Sin código, pilotos ni nueva revisión; el review anterior y los cierres permanecen
intactos. **PLAN_CON_INCERTIDUMBRE_CRITICA:** corrección terminada, viabilidad
real pendiente; no se declaran findings cerrados ni alternativa aprobada.

## Revisión de alternativa OTel — 2026-09-26

[Review técnico y funcional](docs/requirements/project-work-activity-attribution/OTEL_PLAN_REVIEW.md):
N2, propuesta SHA-256 `5a1c949424376f3b010c81357e19d127e617fe922600d0d13fb84690f194a54d`,
**REQUIERE_AJUSTES**, tres obligatorios. Paso 0 aprobado técnicamente como
subalcance independiente de solo lectura; sin autorización derivada para
implementación. Plan original intacto. No se ejecutaron pruebas de producto ni
sesiones. La latencia histórica Kev es una muestra, no prueba de inviabilidad
absoluta; el review registra además el problema del corpus artificial. Los
registros históricos siguientes se conservan, pero no gobiernan la próxima acción.

## Atribución por actividad — A01–A03 offline 2026-09-25

El usuario aprobó criterios/D01/plan v2 y autorizó A01–A03 solo con fixtures.
Se implementaron recibos privados, binding sin categoría global, clasificación
Kev artificial con abstención e historial v2 que conserva una respuesta en una
sola categoría, `mixed` o `unassigned`. T2 11/11 y 46/46 regresiones PASS;
review inline aprobado con notas. Kev real, precisión y sesiones siguen sin
verificar. El host Kev local quedó preparado y verificado por `/v1/models`:
`http://127.0.0.1:8009`, `jaredpalmer/kev-4b`, backend MLX/MPS `bfloat16`.
A04 diagnosticó el servidor Kev: no hay deadlock, pero una respuesta sintética
de Kev-4B tardó 176.445 s en MPS/MLX y Metal procesa una solicitud a la vez.
El corpus completo se estima en 14.7 h y el cliente no devuelve `usage`. No hay
métricas T14 válidas ni habilitación Kev. Siguiente acción: decidir un candidato
Kev local operativo.
Ver [evidencia](docs/requirements/project-work-activity-attribution/EVIDENCE.md)
y [wireframe](docs/requirements/project-work-activity-attribution/WIREFRAME.md).

## Histórico de trabajo por proyecto — cierre 2026-09-25

El usuario pidió implementar un histórico de tokens, USD y tiempo por proyecto y
tipo de trabajo. Confirmó alcance prospectivo y USD real solo con evidencia;
propuso Kev para categorizar. Aprobó D01/criterios/plan v1 con `Aprobar plan v1 y
ejecutar` el 2026-09-25. H01/H02 se implementaron y cerraron con 46/46 pruebas
afectadas PASS. No se accedió a sesiones reales ni se instaló Kev. USD declarado
requiere evidencia opaca, sin verificación externa. Ver
[cierre](docs/requirements/project-work-history/06_CLOSURE.md).

## Medición por plan — S03 cerrada con notas 2026-09-25

S03 usó la fuente exacta autorizada y un binding anterior al trabajo habitual.
T13 concilió seis respuestas y 254927 tokens entre fuente y ledger, con original
preservado; 35/35 pruebas offline pasaron y el review inline no dejó obligatorios.
El intervalo contiene también la aclaración previa; no aísla la tarea. El reporte
real conserva lifecycle, tiempos, modelo, tier, pago y USD como desconocidos o
pendientes donde faltó evidencia. Ver [cierre](docs/requirements/plan-usage-observer/06_CLOSURE.md).

## Medición por plan — S02 offline 2026-09-24

S02 cerrada con lifecycle explícito, límites temporales, reporte v2 con revisiones
preservadas y costos Decimal basados solo en snapshots sintéticos. Modelo, tier,
modalidad, USD o tiempo quedan unknown cuando falta evidencia. 13/13 fixtures T2 y
6/6 regresiones S01 afectadas pasaron; F05–F07 cerrados en review inline. No se leyeron
sesiones reales ni se ejecutó S03; no hubo dependencias, configuración, publicación o commit.

## Medición por plan — S01 offline 2026-09-24

[Auditoría](docs/requirements/plan-usage-observer/AUDIT.md),
[plan v1](docs/requirements/plan-usage-observer/03_PLAN.md) y
[handoff](docs/requirements/plan-usage-observer/HANDOFF.md) elaborados.
Self review APROBADO CON NOTAS; criterios/D01/T2/plan v1 y ejecución limitada a S01
aprobados por el usuario el 2026-09-24. S01 tiene SPEC/brief/closure cerrados.
El primer gate autorizado fue incompatible (CLI 0.149.0, sin identidad por respuesta).
El gate 04 cualificó el contrato mediante un prefijo estable. S01 implementó binding,
captura, ledger/checkpoint atómicos, deduplicación y reporte JSON/texto. Sus 20 pruebas
sintéticas, 19 regresiones CE-v1, 173 pruebas globales y check-release pasaron.
Tres slices del plan: S01 tokens atribuibles, S02 costos/lifecycle, S03 validación
del flujo habitual. 19 tests offline existentes OK y launcher dry-run OK; no
se hizo captura real, pendiente de S03. Predictor, routing automático y publicación excluidos.
El historial siguiente y la actualización previa del merge se conservan; esta sesión
no reabrió los benchmarks ni modificó el repositorio piloto.

## Archivo documental integrado — 2026-09-24

El [PR #5](https://github.com/FabriJuncal/quiver-v2/pull/5) integró en `main`
el resultado v1 (`9ee3d5f`), el cierre v2.1
(`b07d9f8`) y la investigación de recurrencia de Skills (`0ca946c`), junto con
el estado documental de la rama. Merge verificado el 2026-09-24T03:32:55Z en
`44dcd3fd914a7344edd26c2c6c10575a2469fa5e`. No incluye inventarios,
refs/OID o rutas específicas ni el informe detallado del piloto; tampoco incluye
`codex-skills-optimization/`. La inspección de privacidad fue por patrones y
revisión dirigida, no una garantía exhaustiva.
Este merge documental no constituye una release; no se hizo tag ni release en este flujo.

Validación previa al merge: 34 archivos documentales/estado en cuatro commits;
`git diff --check origin/main...HEAD` PASS; enlaces relativos del cierre v2.1
resueltos; SHA-256 de `BENCHMARK_REPORT.md` igual al sidecar; cero matches de
identificadores privados conocidos, firmas comunes de credenciales o JWT en el
contenido commiteado. No hay código en el diff. Permanecen 72 archivos untracked
de discovery y optimización de Skills, sin stage ni commit. La ausencia de matches
no certifica que el contenido sea publicable sin revisión humana final.
Verificación posterior: PR #5 `MERGED` y `main` remoto apuntan al mismo merge commit.
La copia local sigue en la rama documental y no se sincronizó durante esta actualización.

## Benchmark operativo branch-aware — plan v2

v2.1 y T2 reforzado sustituyeron v2/T3 durante P2. El contrato conserva un key
cerrado, tres pares y scoring independiente, con métricas y evidencia reducidas a lo
necesario. P0–P2 se registraron como PASS; su evidencia se conserva. El usuario cerró
el benchmark por priorización antes de P3. P3–P6 canceladas; resultado inconcluso, sin
demostración de beneficio ni decisión de release.

## Benchmark operativo branch-aware — plan v1

La tarea evaluada fue planificar una migración de notificaciones push entre dos snapshots
relacionados bajo aliases privados. Tres pares HEAD-only/branch-aware, mismo presupuesto,
scoring ciego y review N2. El discovery de planificación preservó el repo piloto.

## Discovery por variantes — 2026-09-23

Investigación y plan documentados en docs/requirements/branch-aware-discovery/.
Piloto privado analizado: 35 ramas locales y 60 remotas; 95 refs de rama y 82
tips distintos. Solo lectura; sin implementación ni cambios en la aplicación.
Estado de instalaciones activas y comportamiento del backend desconocidos.
La entrega incluye evidencia, alternativas, criterios y modelos por fase.

## Publicación v2.3.0-rc.2

- **Commit/tag:** `930f67b7c05761edaa59b702320d31535a64c639` / `v2.3.0-rc.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.3.0-rc.2
- **Assets:** `ai-software-factory-v2.3.0-rc.2.zip` y `.sha256`; ZIP digest `cd30e9f4c84ebe34046358c40828091ecb88a06919416a4df29caa025d756f13`.
- **CI:** Validate y Factory Release Validation completados en Ubuntu/macOS para el merge commit.
- **Límite:** preview offline; delegación viva deshabilitada, piloto NOT RUN y RC-F02 abierto.

## Mejora de routing integrada — 2026-09-23

Verificabilidad, ruta rápida, diagnóstico antes de escalar y obligación auditable en
planning/ejecución/review. 25 tests runtime + 22 lifecycle OK; check-release OK.
Origen: improve/model-routing-precision. Evidencia: docs/requirements/model-routing-precision/EVIDENCE.md.
Integrada y publicada en v2.3.0-rc.2. Sin cambios globales, modelos nuevos ni mediciones
de ahorro; esas mediciones continúan fuera del alcance cerrado.

## Mantenimiento de catálogo global de Skills — 2026-09-23

El requirement `docs/requirements/codex-skills-context-budget-recurrence/` quedó
cerrado. C01 confirmó que el override de Vercel en `config.toml` no controla el
catálogo curated del host y fue revertida de forma dirigida. No quedan
deshabilitaciones nuevas activas; investigar el mecanismo del host requiere un
requirement separado.

## Publicación v2.2.2

- **Commit/tag:** `20ea27ac33f92928f2e8ebe7a0c0cf4f14bd8a67` / `v2.2.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.2
- **Assets:** `ai-software-factory-v2.2.2.zip` y `.sha256`; ZIP digest `30b2ff08d6e6c5f5b47bbe94b493309f9367a36b38284ae622505e0dc2cd098a`.
- **CI:** Validate y Factory v2.2.2 Runtime Guardrails completados exitosamente el 2026-09-20.
