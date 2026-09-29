# Requirement State — project-work-activity-attribution

## Identificación

- **Title:** Atribución de tokens, tiempo y USD por actividad dentro de una tarea
- **Status:** blocked
- **Phase:** contrato OTel v1.2-r3 corregido; revisión dirigida H-C2/H-C4 pendiente
- **Risk level:** N2 — contrato de atribución, privacidad y contabilidad
- **Last updated:** 2026-09-29

## Decisiones

- **Acceptance criteria:** base v2 conservada, con transición de §1.1 de OTel v1.1/P1–P3 aprobada el 2026-09-28; no se reescriben cierres anteriores
- **Selected option:** OTel P2 + P4; D12-AUTH selecciona A2 y v1.2-r3 la conserva: login interactivo dentro del mismo Codex temporal, credenciales `ephemeral` y `/usage` sanitizado como verificador sin tarea.
- **Test profile:** T2 A01–A03 ejecutado — 11/11 nuevas y 46/46 regresiones afectadas PASS; timeout corregido y 11/11 regresiones afectadas PASS; T14 sigue bloqueada sin muestra válida. Etapa C/Paso 2: privacidad sanitizada PASS y conciliación/completitud/aislamiento BLOCKED. Preflight A2: B0/H-C3 PASS, H-C1/H-C2 BLOCKED, H-C4 FAIL y B4 operativo PASS con igualdad personal FAIL.
- **Plan version:** plan OTel v1.3 — corrección dirigida P4; distinto del contrato de aislamiento v1.2. OTel v1.1/P1–P3 y P4 aprobados conservados.
- **Plan review:** APROBADO para v1.3 en [ronda dirigida](OTEL_PLAN_REVIEW.md#ronda-dirigida--plan-otel-v13--cierre-p4--2026-09-28); R-OTEL-P4-01/02 cerrados. Review v1.2 REQUIERE_AJUSTES e histórico v1.1 conservados; R-OTEL-01–03 cerrados.
- **Isolation contract review:** v1.2-r3 pendiente de revisión dirigida H-C2/H-C4. v1.2-r2 conserva su [cierre histórico](OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12-r2--cierre-c12--2026-09-28); R-OTEL-C12-01/02/03 permanecen cerrados y ningún nuevo preflight está autorizado.
- **Isolation contract version:** v1.2-r3, SHA-256 `ac685955886ba10a1171a5f7787c0d0195613661215f2cd400ded35097da60ad`; corregido para raíces completas y supervisor externo, todavía no revisado ni aprobado. A2 autenticó históricamente, pero el aislamiento completo no quedó demostrado.
- **Alternative plan review:** APROBADO — [ronda dirigida 2026-09-28](OTEL_PLAN_REVIEW.md#ronda-dirigida--otel-v11--2026-09-28), R-OTEL-01–03 cerrados; plan condicionado, no viabilidad demostrada. El review inicial queda histórico para su hash anterior.
- **Alternative version:** [plan OTel v1.3](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md), 2026-09-28; R-OTEL-P4-01/02 corregidos y cerrados por review.
- **Alternative SHA-256:** `48827d6014612796b42cd5982bb640c229fad1f524e2cfbefa82590a576d2209` — plan v1.3 actual; hashes v1.1/v1.2 conservados en los registros históricos.
- **Alternative authorization:** corrección exclusiva R-OTEL-P4-01/02 autorizada con «Apruebo» y finalizada; review dirigido posterior autorizado y completado. Sin spec, slices ni implementación autorizadas.
- **Alternative human plan approval:** APROBADO — mensaje del usuario del 2026-09-28 «Apruebo los 3 puntos indicados», en respuesta a la solicitud de aprobar OTel v1.1 con P1–P3. No incluye ejecución
- **Human plan approval:** P1–P3/v1.1 y organización P4 aceptadas; v1.3 corrige el texto sin reabrir esas decisiones y su review técnico está APROBADO. No implica permiso de ejecución.
- **Execution authorization:** A01–A03 aprobadas con fixtures; preparación aislada, A04, corrección de timeout y diagnóstico local autorizados y ejecutados. Pasos 0–1 OTel y una ejecución de Etapa C fueron autorizados y ejecutados el 2026-09-28; Etapa C terminó BLOCKED. La autorización de una sola ejecución del preflight A2 H-C1–H-C4 fue consumida y cerró FAIL/BLOCKED el 2026-09-28; H-C5/Paso 3 continúan sin autorización.
- **Workflow size:** full

## Ejecución

- **Current slice:** none; preflight A2 cerrado y entorno temporal revertido
- **Completed slices:** A01 recibos; A02 clasificación; A03 historia/conciliación — probadas con fixtures, no prueba de captura automática OTel.
- **Pending slices:** ninguna nueva formalizada. v1.2-r3 requiere revisión dirigida antes de otra ejecución; Paso 3 bloqueado, A04 sin cierre y A05 no ejecutada.
- **Pending required findings:** ninguno reabierto. R-OTEL-C12-01/02/03, R-OTEL-P4-01/02 y R-OTEL-01–03 están cerrados; la corrección H-C2/H-C4 de v1.2-r3 espera review. F06/F07 de A04 conservan su estado.
- **Implementation review:** requires-adjustments — addendum A04 en `05_IMPLEMENTATION_REVIEW.md`, self review inline N2
- **Relation:** project-work-history v1 complete-with-notes; H01/H02 conservadas

## AI Strategy

- **Planning recommendation:** BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium; fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- **Implementation recommendation:** A01–A05 provisionalmente BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium; mismo fallback.
- **Critical review recommendation:** ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High; fallback GPT-5.6 Terra (`gpt-5.6-terra`) / High o XHigh. Modalidad N2 inline declarada; sin delegación autorizada.
- **Routing decision:** routing-v1, base policy; catálogo canónico v2.2.2 consultado 2026-09-25, last verified 2026-09-20. N2 local/reversible, contexto suficiente para plan y fixtures con oráculos exactos; capacidad de enlace del host y precisión Kev requieren evidencia posterior, no más reasoning por sí solos. Switch Benefit MEDIUM; Model Gate no requerido ahora.
- **Effective configuration:** NO VERIFICADA. Recomendación no prueba modelo/reasoning activos ni disponibilidad de cuenta.
- **Escalation triggers:** pérdida/corrupción de datos, atribución cruzada difícil de reproducir, acceso a contenido no autorizado o rediseño material. Diagnosticar evidencia/entorno antes de escalar modelo.
- **Downgrade opportunity:** documentación mecánica sustancial después del cierre; no interrumpir una edición breve ni bajar antes de review crítico.
- **Alternative review routing:** 2026-09-26, N2 inline, routing-v1/catalog v2.2.2 comprobado; ADVANCED / High recomendado para contratos e integridad. Switch Benefit MEDIUM, sin cambio de modelo ni gate nuevo. Corrección dirigida BALANCED / Medium. Runtime efectivo NO VERIFICADO; detalle en OTEL_PLAN_REVIEW.md.
- **Correction routing:** 2026-09-28, model-router/routing-v1; hereda BALANCED / Medium para corrección documental N2 limitada a findings concretos, verificable por comparación y trazabilidad. Catálogo local consultado, sin cambios de modelo/configuración; Switch Benefit LOW, sin gate. No hubo nueva revisión; runtime efectivo NO VERIFICADO.
- **Directed review routing:** 2026-09-28, hereda ADVANCED / High para review N2 acotado; catálogo v2.2.2 contrastado y componentes pertinentes leídos. Switch Benefit MEDIUM, sin gate nuevo ni delegación. Modalidad inline en la misma conversación; sin independencia ni configuración efectiva verificada.

## Progreso

- **Completed:** criterios/D01/plan aprobados; A01–A03 implementadas: recibos privados, binding sin categoría global, señales Kev artificiales con abstención, historial v2 y CLI. T2 11/11 y regresiones 46/46 PASS; dataset artificial A04 preparado. Kev local oficial respondió `/v1/models` como `jaredpalmer/kev-4b`, MLX/MPS `bfloat16`. La corrección cambió solo `KEV_TIMEOUT_SECONDS` de 5 a 180 y sus 11 regresiones afectadas pasaron. El diagnóstico confirmó una respuesta sintética de 176445.453 ms y que Metal procesa una solicitud por vez.
- **In progress:** none; corrección H-C2/H-C4 terminada sin ejecución viva. A05/Paso 3 fuera de alcance.
- **Pending:** revisión dirigida de v1.2-r3 antes de cualquier repetición. P1–P4 permanecen aprobadas.

## P4 — planificación por bloques aceptada e incorporada 2026-09-28

**Objeto:** organización de tareas por categoría dentro de cada slice; plan OTel
v1.2 §1.2/§5.2.1 y efectos en §6.1/pasos 3–7/§10. **Decisión:** APROBADO para
incorporar esa organización al plan, según «Dale, hazlo», respuesta a la propuesta
concreta. No es una aprobación técnica del delta ni permiso de implementación.
No se vuelve a solicitar esta decisión. P1–P3 y todos los cierres siguen vigentes.

La edición concreta distingue categoría prevista/observada/consumo, propone
inicio/cierre automáticos, retornos y ejecuciones de bloque, conserva mixtos/sin
atribuir y el histórico. No hay cambio de significado de tokens, USD o tiempo
activo ni obligación de una sesión/turno por bloque. Trabajo sin slice no necesita
inventar una para medir. La captura y el productor automático siguen pendientes.

**Estado:** PLAN_CON_INCERTIDUMBRE_CRITICA. Revisión dirigida del delta pendiente;
no se ejecutó una ronda ni pruebas de producto. Contratos/reviews anteriores
intactos, incluido OTEL_PILOT_CONTRACT_v1.2.md; no se deduce aislamiento resuelto.
Evidencia y validación documental en [EVIDENCE.md](EVIDENCE.md).

**Routing:** model-router/routing-v1, catálogo v2.2.2 consultado; hereda
BALANCED / Medium para planificación N2 acotada, verificable documentalmente.
Switch Benefit LOW, sin gate ni cambio de modelo. Configuración efectiva unknown.
La siguiente revisión conserva estrategia de review, sin delegación autorizada.

## Review dirigido del plan OTel v1.2/P4 — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.** Objeto: plan SHA-256
`53ae25ef657d8549b54f325af34ba15073bb56d131d423f6572e2cba726deb64`,
solo P4 y efectos directos. Resultado completo en
[OTEL_PLAN_REVIEW.md](OTEL_PLAN_REVIEW.md#ronda-dirigida--plan-otel-v12--p4--2026-09-28).

- **R-OTEL-P4-01:** D4/D5 y la apertura de §5 todavía presentan P1–P3 como
  pendientes, aunque P1–P4 están aprobadas. Debe corregirse el texto sin volver
  a pedir decisiones.
- **R-OTEL-P4-02:** una unidad indivisible asociada a dos bloques de la misma
  categoría carece de propietario contable único para el detalle/histórico.
  Debe fijarse una representación no aditiva y su prueba dirigida.

P4 es coherente como organización funcional; el review no la rechaza ni reabre
su aprobación. Tampoco reabre P1–P3, R-OTEL-01–03 o cierres anteriores. El
contrato de aislamiento v1.2 sigue pendiente con INFORMACIÓN INSUFICIENTE; no
fue revisado ni aprobado por extensión. Sin sesiones, pilotos, código o tests.

## Corrección dirigida del plan OTel v1.3 — 2026-09-28

Autorizada mediante «Apruebo» como respuesta a la única acción registrada tras
el review v1.2. Se modificó exclusivamente
[el plan](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md),
SHA-256 `48827d6014612796b42cd5982bb640c229fad1f524e2cfbefa82590a576d2209`:

- **R-OTEL-P4-01 corregido:** D4/D5 y §5 distinguen P1–P4 ya aprobadas de la
  evidencia técnica aún pendiente. No vuelven a solicitar decisiones resueltas.
- **R-OTEL-P4-02 corregido:** cada unidad tiene un único propietario aditivo.
  Si abarca dos bloques de la misma categoría, suma una vez en
  `shared_within_category`; los bloques solo conservan referencias no aditivas.
  JSON/texto, detalle y totales deben conciliar mediante una prueba dirigida.

La regla compartida es un estado de calidad, no una actividad nueva. No reparte
tokens, no adjudica el total a un bloque arbitrario y no duplica duración. P3,
USD con evidencia, tiempo activo unknown, históricos v1/v2 y todos los cierres
se conservan. El contrato de aislamiento v1.2 no se modificó ni aprobó.

**Estado:** PLAN_CON_INCERTIDUMBRE_CRITICA, listo para revisión dirigida solo de
R-OTEL-P4-01/02 y efectos directos. No se inicia esa ronda en esta corrección.
Sin código, spec, slices, sesiones, pilotos, pruebas de producto o dependencias.

## Review dirigido del plan OTel v1.3 — 2026-09-28

**VEREDICTO: APROBADO.** R-OTEL-P4-01/02 quedan cerrados para el plan SHA-256
`48827d6014612796b42cd5982bb640c229fad1f524e2cfbefa82590a576d2209`.
[Resultado completo](OTEL_PLAN_REVIEW.md#ronda-dirigida--plan-otel-v13--cierre-p4--2026-09-28).

D4/D5 y §5 conservan P1–P4 como decisiones aprobadas y dejan pendiente solo su
demostración técnica. Cada unidad indivisible compartida entre bloques iguales
tiene un único propietario aditivo en la categoría; los bloques la referencian
sin sumarla. La misma regla rige JSON, texto, detalle, histórico y totales. Si
el desglose individual requerido sigue `unknown`, P3 no permite un falso cierre.

Sin observaciones accionables ni ajustes adicionales de validación. No se
modificó el plan ni se ejecutaron pruebas, sesiones, pilotos, código o slices.
R-OTEL-01–03 y todos los cierres previos siguen vigentes.

El contrato de aislamiento v1.2 permanece separado, pendiente y con INFORMACIÓN
INSUFICIENTE; este review no aprueba F12-01–F12-05 ni H-C1–H-C5. La única
siguiente acción es su revisión dirigida de solo lectura, con autorización
separada y sin abrir otra sesión o piloto.

## Review dirigido del contrato OTel v1.2 — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.** Objeto: contrato SHA-256
`98c85652b24c86b68fddb8dbe20cca8d00f334d8f53dec05888b47f875a1692a`,
solo F12-01–F12-05, H-C1–H-C5 y efectos directos. Resultado completo en
[OTEL_PLAN_REVIEW.md](OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12--aislamiento--2026-09-28).

- **R-OTEL-C12-01:** el baseline del contrato es Codex 0.157.1, pero el PATH
  actual informa 0.158.0. Debe separar antecedente y ejecutable futuro.
- **R-OTEL-C12-02:** falta separar fuente de autenticación de su lugar de
  almacenamiento y definir decisión/STOP sin leer o copiar secretos.
- **R-OTEL-C12-03:** prompt normal más hash/stat de `config.toml` no prueba que
  herdr propagó `CODEX_HOME` ni que el resto del estado personal quedó intacto.

La documentación oficial refuerza a `CODEX_HOME` como raíz del estado local,
pero no demuestra su uso bajo herdr. H-C1–H-C4 continúan sin prueba; H-C5 se
conserva como límite del eventual piloto. P1–P4, R-OTEL-01–03,
R-OTEL-P4-01/02 y todos los cierres previos quedan intactos.

No se modificó el contrato ni se abrió Codex, herdr, pane, sesión, piloto o
login. No se leyeron credenciales, sesiones o valores de configuración.

## Corrección dirigida del contrato OTel v1.2-r1 — 2026-09-28

Autorizada mediante «Continua con la accion siguiente» y limitada a
R-OTEL-C12-01/02/03. El contrato corregido conserva su archivo y queda
identificado como v1.2-r1, SHA-256
`5647887786d52a22ef8056c25e9109b5ebcebfb92ba9865369424f5889d98a5d`.

- **R-OTEL-C12-01 corregido:** separa el antecedente 0.157.1 del baseline actual
  0.158.0 y detiene cualquier preflight si vuelve a cambiar ruta/versión/flags.
- **R-OTEL-C12-02 corregido:** D12-AUTH distingue fuente, almacenamiento,
  autorización, evidencia y STOP. No selecciona una opción ni autoriza secretos.
- **R-OTEL-C12-03 corregido:** H-C1–H-C4 y B0–B4 exigen evidencia atribuible en
  la raíz temporal, metadatos globales intactos y reversión; el prompt no basta.

**Estado:** PLAN_CON_INCERTIDUMBRE_CRITICA. D12-AUTH y H-C1–H-C4 siguen sin
demostración viva, pero el documento está listo para review dirigido. No se
inicia esa ronda automáticamente. Sin procesos interactivos, sesión, login,
piloto, credenciales, configuración, dependencias, implementación o slices.

## Review dirigido del contrato OTel v1.2-r1 — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.** Objeto: SHA-256
`5647887786d52a22ef8056c25e9109b5ebcebfb92ba9865369424f5889d98a5d`,
solo R-OTEL-C12-01/02/03 y efectos directos. Resultado completo en
[OTEL_PLAN_REVIEW.md](OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12-r1--seguimiento--2026-09-28).

- **R-OTEL-C12-01 CERRADO:** baseline histórico/actual separados y STOP ante
  deriva antes de abrir herdr.
- **R-OTEL-C12-02 ABIERTO:** A0 puede avanzar sin demostrar autenticación; falta
  una señal no secreta de autenticación efectiva para A1–A3.
- **R-OTEL-C12-03 ABIERTO:** falta vincular el proceso hijo con el artefacto
  temporal y detectar cambios dentro de árboles personales existentes.

P1–P4, R-OTEL-01–03, R-OTEL-P4-01/02 y todos los cierres previos permanecen
intactos. No se modificó el contrato, resolvió D12-AUTH ni abrió Codex/herdr,
pane, sesión, login o piloto.

## Reintento aislado OTel v1.1 — autorización y preflight 2026-09-28

Autorizado una sola vez conforme a §9. `codex --strict-config ... --help`
aceptó `--no-daemon`, el override efímero de trust y los cinco overrides OTel
con exit `0`. El hash y stat del TOML global quedaron iguales y la tarea todavía
no se envió. Receptor y fixture temporales v1.1 quedaron preparados para el
preflight vivo obligatorio.

## Reintento aislado OTel v1.1 — BLOCKED en preflight 2026-09-28

Proceso, `--no-daemon` y ausencia de diálogo de trust pasaron, pero el control
obligatorio previo a la tarea detectó que Codex había persistido la ruta v1.1 en
`~/.codex/config.toml`. Hash y stat cambiaron respecto del baseline. La pane se
cerró externamente y la tarea no se envió; no se leyó ninguna sesión, no se creó
referencia y no se ejecutó la prueba negativa.

G-C1 y G-C7 quedan BLOCKED por la configuración; G-C2 es solo parcial y G-C3–G-C6
no se ejecutaron. Pane, Codex, receptor, puerto y árbol temporal sí quedaron
revertidos. El bloque persistido no se editó porque el contrato exige autorización
específica. Evidencia completa en [EVIDENCE.md](EVIDENCE.md#reintento-aislado-otel-v11--blocked-antes-de-la-tarea-2026-09-28).

### Reparación dirigida completada

Con autorización posterior se creó un backup privado `0600` y se eliminó solo
la tabla exacta de trust v1.1. La ruta tiene cero coincidencias; hash actual
`536f8d4b5fba477f17f0a3857c5d58b304798fa71fed609ffd0c37c8877b96ce`.
No se normalizaron cuatro bytes restantes frente al baseline ni se abrió Codex;
no había parser TOML independiente instalado. El residuo quedó resuelto, pero
los gates del reintento no se recalifican y Paso 3 continúa bloqueado.

## OTel v1.2 — contrato de viabilidad preparado 2026-09-28

La investigación autorizada fue solo de lectura. Perfiles de Codex quedan
descartados porque cargan la configuración personal como base. `CODEX_HOME` es
una candidata reconocida por el binario, pero no hay evidencia de que herdr la
propague ni de que Codex pueda autenticarse con esa raíz sin leer o copiar
credenciales. No se inició Codex/herdr de forma interactiva; no hubo sesión,
piloto ni cambio de configuración.

El nuevo [contrato v1.2](OTEL_PILOT_CONTRACT_v1.2.md) concluye **INFORMACIÓN
INSUFICIENTE** y define H-C1–H-C5. Está listo para revisión dirigida; no prepara
otro comando de piloto ni autoriza Paso 3.

## Etapa C/Paso 2 OTel — BLOCKED 2026-09-28

La lista cerrada §9 se ejecutó una vez. Herdr abrió una pane nueva con Codex
`0.157.1`, sandbox `read-only`, overrides efímeros y una tarea artificial. La
referencia permitida registró 2 respuestas y 46.398 tokens. OTel guardó 40
eventos sanitizados, incluidos 5 `response.completed`, pero ninguno contenía
`response_id`; solo quedaron contadores cached/cache-write y aparecieron dos
`conversation.id`. Uno corresponde a la sesión piloto y el otro no se identificó
ni se abrió. La captura con daemon compartido no quedó aislada.

Conciliación y prueba negativa terminaron `incomplete` con exit `2`; identidad,
contadores, coincidencia exacta y detección de pérdida no quedaron cualificados.
El saneamiento no mostró contenido del fixture/tarea ni credenciales en lo
persistido. Codex agregó transitoriamente confianza para la ruta temporal; se
retiró solo ese bloque y se verificó su ausencia. Pane, procesos y configuración
de proyecto quedaron cerrados. Evidencia y hashes en
[EVIDENCE.md](EVIDENCE.md#etapa-cpaso-2-otel--ejecución-blocked-2026-09-28).

No se ejecutó Paso 3, no se clasificaron actividades y USD, tier, modalidad de
pago y tiempo activo continúan `unknown`. Routing solicitado BALANCED/Medium;
Codex mostró GPT-5.6 Terra/medium en el piloto, pero ese dato no certifica
facturación, tier ni selección efectiva de esta sesión coordinadora.

## Corrección documental OTel v1.1 — 2026-09-28

El usuario autorizó únicamente corregir el contrato para un eventual reintento,
sin ejecutar sesión o piloto. [OTEL_PILOT_CONTRACT.md](OTEL_PILOT_CONTRACT.md)
v1.1 incorpora `--no-daemon`, trust por override efímero, hashes/stat del TOML
antes de pane/tarea y después del cierre, y cierre externo ante cualquier diálogo
de confianza. El proceso, trust y configuración deben pasar antes de consumir la
única tarea.

El saneamiento ahora usa nombres exactos observados (`cached_token_count`,
`cache_write_token_count`) y esperados, conserva IDs solo como digest y evalúa
campos numéricos antes del descarte textual. G-C1–G-C7 exigen aislamiento,
privacidad, `response_id`, seis contadores completos, conciliación exacta, pérdida
detectable y reversión. La prueba negativa solo se ejecuta después de un original
PASS. `conversation.id`, secuencia y tiempo no sustituyen identidad.

No se creó el árbol temporal, no se abrió Codex/herdr, no se leyó ninguna sesión
y no se modificaron configuración, router, launcher, código o dependencias. El
resultado BLOCKED de v1 permanece como evidencia; v1.1 no afirma viabilidad.

## Paso 1 OTel completado — 2026-09-28

El usuario indicó «Continua con el siguinte paso», referencia inequívoca a la
única acción persistida tras Paso 0: preparar el contrato documental de Paso 1.
Se creó [OTEL_PILOT_CONTRACT.md](OTEL_PILOT_CONTRACT.md) v1 con tarea, sesión,
campos permitidos, fuentes, completitud, cambios, reversión y gates cerrados.

La decisión mínima es usar para Etapa C una sesión nueva bajo herdr, OTel activado
solo mediante argumentos CLI, receptor Python temporal en loopback y conciliación
contra metadatos/contadores de esa sesión. No se usa configuración OTel local al
proyecto porque la documentación oficial indica que Codex la ignora. No se usa
Collector/Docker porque `otelcol` no está instalado y el piloto no necesita añadir
dependencias. Hooks/marcas quedan fuera de Etapa C y requieren su propia autorización
en Paso 3 después de demostrar identidad/captura.

Routing de Paso 1: BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium;
fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium; Switch Benefit LOW, sin Model Gate.
Configuración efectiva `unknown`. No se inició Codex, herdr agent, receptor o
piloto; no se leyó ninguna sesión ni valor de configuración y no se tocó código,
configuración global, router o launcher. Evidencia en [EVIDENCE.md](EVIDENCE.md#paso-1-otel--contrato-documental-del-piloto-2026-09-28).

## Aprobación humana registrada — 2026-09-28

- **Objeto:** OTel v1.1, SHA-256 `e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`, §1.1 P1–P3.
- **Decisión real:** APROBADO.
- **Referencia:** mensaje «Apruebo los 3 puntos indicados», respuesta a la solicitud concreta de aprobación posterior al review APROBADO.
- **P1:** cuatro bloques con detalle de feature/bug/test/explicación/documentación y análisis diferenciado.
- **P2:** marcas automáticas y reglas verificables sustituyen Kev en la ruta futura; conservan cobertura de acciones, procedencia y atribución conservadora.
- **P3:** caso de aceptación acotado con captura completa y cero consumo mixto/sin atribuir o detalle requerido desconocido; sin garantía universal ni recorte retrospectivo.
- **Alcance habilitado:** registro y formalización documental conforme a dependencias del plan; no autoriza ejecutar Paso 0, pilotos o implementación. La spec definitiva sigue condicionada a evidencia de pasos 2–3.

Registro conforme a [09_REGISTRAR_APROBACION.md](../../../../workflow_verificable/09_REGISTRAR_APROBACION.md).
No se vuelve a solicitar P1–P3. USD solo con evidencia y tiempo activo unknown
continúan vigentes. A04/T14 deja de ser dependencia de la nueva ruta aprobada;
esto no convierte sus pruebas en PASS ni cierra A04/A05 anteriores. S01–S03,
H01/H02 y A01–A03 conservan sus cierres. Plan y review permanecen intactos como
objetos versionados; sus menciones históricas a aprobación pendiente se resuelven
por este registro. No se ejecutó auditoría ni se generó una spec sin evidencia.

## Paso 0 OTel completado — 2026-09-28

**Alcance ejecutado:** auditoría exclusivamente de lectura, autorizada en el
mensaje del usuario de esta ronda. Sin sesiones, conversaciones, credenciales,
instalaciones, dependencias, pilotos, código, router, launcher, configuración,
publicación ni commit.

**Resultado:** `herdr --version` informó `0.8.0`; el `codex` resuelto por PATH
en esta auditoría es `/opt/homebrew/bin/codex`, que informó `codex-cli 0.157.1`.
El binario de herdr no declara una ruta alternativa de Codex en su configuración
pertinente, así que esta evidencia no prueba aún qué ejecutable lanza una sesión
gestionada. `herdr integration status` informó que el hook de estado de `codex`
no está instalado. Las configuraciones pertinentes fueron válidas y no mostraron
una clave OTel/telemetría; se registraron solo nombres de claves, no valores.
La lista de features expuso `runtime_metrics` como experimental y desactivada;
por su nombre y estado no prueba exportación, identidad ni contadores de uso.

Quiver ya ofrece `plan_usage.py` con binding prospectivo, ledger privado,
recibos con `response_id`/acciones/límites observables y reportes de historial
por `project_id`/`work_id` en JSON y texto. `work_activity.py` clasifica solo
recibos entregados por un llamador; la búsqueda acotada no halló un productor
automático ni hook OTel que los alimente. Por ello hay piezas de persistencia y
presentación reutilizables, pero no fuente de captura completa ni vínculo
automático uso→actividad demostrado. Evidencia y D1–D7 en [EVIDENCE.md](EVIDENCE.md#paso-0-otel--auditoría-de-solo-lectura-2026-09-28).

La diferencia respecto de la nota histórica de CLI `0.157.0` es una observación
actual de PATH, no una afirmación de cambio de comportamiento ni de runtime bajo
herdr. El hash del plan permanece
`e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`.

## Revisión dirigida cerrada — 2026-09-28

**VEREDICTO: APROBADO**, N2, limitado a R-OTEL-01–03 y efectos directos de
OTel v1.1. [Resolución y evidencia](OTEL_PLAN_REVIEW.md#ronda-dirigida--otel-v11--2026-09-28).
Sin observaciones accionables pendientes ni ajustes adicionales de validación.
Se cierran los tres hallazgos documentales; no se declaran pruebas de producto
aprobadas ni integración viable. Plan revisado conservado con el mismo hash.

La incertidumbre crítica de integración sigue vigente: identidad efectiva bajo
herdr, enlace automático con acciones completas y prueba de completitud requieren
los pasos de comprobación previstos y permisos acotados. La aprobación técnica
del recorrido condicionado no elimina esas condiciones ni aprueba P1–P3 por el
usuario. No hubo implementación, pilotos, sesiones, dependencias ni commit.

## Corrección dirigida — 2026-09-28

**ESTADO: PLAN_CON_INCERTIDUMBRE_CRITICA.** Corrección documental terminada;
no es evidencia de viabilidad ni nuevo veredicto. Se aplicaron los archivos reales
[03_PLANIFICAR.md](../../../../workflow_verificable/03_PLANIFICAR.md) y
[01_POLITICA_COMUN.md](../../../../workflow_verificable/01_POLITICA_COMUN.md).
La instrucción de workflow/04 de continuar a review no se aplica: el usuario
prohibió expresamente otra ronda en este encargo.

En el mismo [plan OTel v1.1](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md):
R-OTEL-01 → §1.1 y §§5.3–5.5/10; R-OTEL-02 → §6.1 y pasos 4–7/10;
R-OTEL-03 → §5.6 y pasos 2/3/7/8/10. Registro de cambios en §12.
El review del 2026-09-26 queda intacto y aplica a su hash original.

Decisiones funcionales propuestas, no aprobadas: P1 cuatro agrupaciones con
detalle feature/bug/test/explicación/documentación y análisis diferenciado;
P2 sustituir Kev por marcas/reglas con cobertura verificable;
P3 cero consumo mixto/sin atribuir o detalle requerido desconocido en el caso
final de aceptación, sin recortes retrospectivos del ámbito. USD con evidencia
directa y tiempo activo unknown se conservan, no se vuelven a consultar.

La relación real uso→bloque y la evidencia de completitud siguen sin demostrar;
bloquean la integración dependiente, no la preparación documental. No se
ejecutaron pilotos, tests de producto, spec/slices ni otra revisión. Sin sesiones,
dependencias, delegación, configuración, publicación o commit.

Validación documental: comparación de integridad de 451 archivos del worktree
confirma cambios solo en el plan, este STATE y PROJECT_STATE; review previo,
código y fixtures intactos. 21 enlaces locales resueltos, referencias AC01–AC13
y R-OTEL-01–03 presentes; `git diff --check` PASS. Son comprobaciones de edición,
no una revisión técnica ni evidencia de integración.

## Revisión alternativa — 2026-09-26

[Resultado completo y evidencia](OTEL_PLAN_REVIEW.md). N2; revisión documental
sin modificar el plan ni código. R-OTEL-01 exige transición explícita frente a
AC01–AC13/D01; R-OTEL-02 preservación del histórico/revisiones; R-OTEL-03 evidencia
de completitud. Codex del PATH reportó 0.157.0; su uso efectivo por herdr y el
enlace real uso→bloque siguen no verificados. Fuentes oficiales y código público
contrastados; sin sesiones, Collector, Kev ni pruebas de producto.

La latencia anterior corresponde a una muestra, no certifica inviabilidad
absoluta. El corpus Kev tiene entradas idénticas con etiquetas diferentes y
solapamiento entre splits (review, evidencia previa); sigue intacto. No se
reactiva T14 ni se alteran cierres previos.

## Corrección dirigida del contrato OTel v1.2-r2 — 2026-09-28

Se aplicó `03_PLANIFICAR.md` únicamente a R-OTEL-C12-02/03. El contrato actual,
SHA-256 `943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`,
convierte A0 en control negativo siempre bloqueante y exige para A1–A3 una señal
`AUTH_OK` sanitizada, efectiva y vinculada al mismo proceso hijo.

H-C2 exige una cadena verificable entre herdr, el hijo, el ejecutable y un
artefacto temporal. H-C4 reemplaza las rutas fijas por un inventario recursivo de
metadatos con identificadores HMAC efímeros, sin abrir contenido ni persistir
nombres personales. La falta de cualquiera de esas evidencias produce BLOCKED o
STOP; no se rescata por llegar al prompt o conservar solo `config.toml`.

R-OTEL-C12-01 permanece cerrado. R-OTEL-C12-02/03 están corregidos pero no
cerrados hasta el review. D12-AUTH sigue sin resolverse. No se abrió proceso,
sesión, login o piloto ni se leyó configuración, credenciales o sesiones.

## Review dirigido del contrato OTel v1.2-r2 — 2026-09-28

**VEREDICTO: APROBADO. Sin observaciones accionables.** Objeto SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
[Resultado completo](OTEL_PLAN_REVIEW.md#ronda-dirigida--contrato-otel-v12-r2--cierre-c12--2026-09-28).

R-OTEL-C12-02 cierra porque A0 nunca puede pasar H-C3 y A1–A3 requieren
`AUTH_OK` efectivo, sanitizado y vinculado al mismo hijo. R-OTEL-C12-03 cierra
porque H-C2 exige la cadena al proceso exacto y H-C4 compara recursivamente el
estado personal sin abrir contenido ni persistir nombres reales.

La aprobación valida el contrato, no la integración. La existencia real del
verificador, la cadena del host y el inventario vivo continúan sin demostrar y
quedan bloqueados hasta resolver D12-AUTH y autorizar una comprobación separada.
No se modificó el contrato ni se abrió proceso, sesión, login o piloto.

## Investigación de viabilidad de A2 — 2026-09-28

**Resultado:** CAMINO_SUSTENTADO_CON_PRUEBA_PENDIENTE. A2 fue seleccionada para
D12-AUTH por instrucción explícita del usuario; la comprobación viva permanece pendiente.

La documentación oficial y Codex CLI 0.158.0 permiten una ruta acotada: el login
interactivo debe completarse dentro del mismo Codex que herdr inicia con raíz
temporal, `--no-daemon` y almacenamiento `ephemeral`. En esa misma sesión,
`/usage` puede actuar como comprobación sin tarea porque requiere autenticación
ChatGPT. La evidencia debe reducir su resultado al `AUTH_OK` permitido y
descartar identidad, plan, límites, importes y contenido.

Un `codex login` ejecutado como proceso anterior no sirve: `ephemeral` conserva
credenciales solo durante la vida del proceso que las recibió. La expresión
«login separado» de A2 solo es viable como etapa separada dentro del mismo
proceso. No se modificó el contrato aprobado.

herdr documenta variables para la pane y argumentos del agente, y el wrapper
local de Codex transmite el entorno al binario. Todavía no está comprobada en
vivo la cadena completa, la aceptación real de `ephemeral`, el login, `/usage`
autenticado o el estado personal intacto. Eso requiere una autorización futura
para una pane, un Codex, login de navegador, red de OpenAI y una consulta
`/usage`, siempre sin tarea y con H-C1–H-C4/STOP vigentes.

No se abrió Codex/herdr, pane, sesión, login o piloto; no se leyó configuración,
sesiones o credenciales; no se instalaron dependencias ni se cambió contrato,
router, launcher o configuración. P1–P4 y todos los hallazgos y cierres previos
se conservan.

## Registro histórico D12-AUTH y preparación del preflight — 2026-09-28

D12-AUTH queda resuelta con A2 y registrada en [02_DECISION.md](02_DECISION.md).
La fuente es el login interactivo del usuario dentro del mismo Codex temporal;
el almacenamiento exigido es `ephemeral`; `/usage` en ese mismo proceso es la
comprobación sin tarea, reducida al `AUTH_OK` del contrato. A1/A3 quedan no
seleccionadas, A0 conserva el control negativo y A4 sigue prohibida.

En ese punto, esta decisión todavía no era autorización de ejecución. El texto
entonces preparado limitaba el preflight a una pane herdr, un Codex
0.158.0 con `--no-daemon`, raíz temporal privada, login de navegador realizado
por el usuario, una consulta `/usage`, H-C1–H-C4 y reversión. Excluye tarea,
fixture, inferencia, H-C5/Paso 3, lectura de sesiones/credenciales, dependencias y
cambios globales. La ejecución posterior y su resultado vigente están en el
cierre de este documento y en [HANDOFF.md](HANDOFF.md).

## Próxima acción

- **Next action:** autorizar la revisión dirigida de OTel v1.2-r3, limitada a H-C2, H-C4 y efectos directos, sin repetir el preflight
- **Why this is next:** la corrección fija las raíces y separa el supervisor, pero todavía debe verificarse su coherencia y suficiencia antes de aprobarla
- **User action required:** true — autorizar la revisión documental acotada
- **Decision required:** aceptar o no que el contrato corregido pase al review técnico
- **Expected output:** veredicto formal sobre H-C2/H-C4 y efectos directos, sin ejecución viva
- **After this:** si el review cierra, solicitar aprobación del contrato concreto antes de cualquier nuevo preflight
- **Blocked by:** v1.2-r3 corregido pero todavía no revisado ni aprobado
- **Runtime limitation:** none
- **Resume instruction:** Autorizar únicamente la revisión dirigida de v1.2-r3 preparada en HANDOFF.md; no corregir el contrato ni repetir login, preflight, H-C5 o Paso 3.

## Cierre del preflight A2 H-C1–H-C4 — 2026-09-28

La única ejecución autorizada terminó y fue revertida. B0 PASS confirmó Codex
0.158.0, herdr 0.8.0 y el hash aprobado. H-C3 PASS confirmó A2 dentro del mismo
proceso mediante `/usage` y persistió solo el `AUTH_OK` permitido. No apareció
`auth.json` y no se conservaron identidad, valores de uso, plan, límites o
contenido.

H-C2 quedó BLOCKED tras 13.130 observaciones sin un vínculo directo entre el
proceso exacto y un artefacto temporal. H-C4 terminó FAIL: 1.244 entradas antes
y después, cero errores y cero symlinks, con tres identificadores HMAC cambiados.
No se leyeron rutas ni contenidos, por lo que la causa queda sin atribuir. H-C1
queda BLOCKED por depender de esa atribución. B4 cerró proceso/pane/workspace y
eliminó la raíz temporal, pero la igualdad personal no pasó.

Resultado global: FAIL/BLOCKED. No hubo tarea, prompt, fixture, inferencia,
H-C5 ni Paso 3. P1–P4 y todos los hallazgos y cierres anteriores se conservan.

## Diagnóstico dirigido H-C2/H-C4 — 2026-09-29

**Alcance:** solo implementación local accesible y documentación oficial, sin
abrir Codex, herdr, pane, login o red autenticada; sin leer sesiones,
credenciales, rutas personales cambiadas o valores de configuración. El contrato
v1.2-r2 no se modificó y conserva SHA-256
`943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.

**H-C2 — diagnóstico:** Codex 0.158.0 admite una raíz SQLite separada que toma
`CODEX_SQLITE_HOME` cuando existe y, si no, `CODEX_HOME`. El wrapper entrega el
entorno heredado completo al binario nativo. A la vez, `lsof` solo lista archivos
abiertos y el grabador de una sesión nueva difiere la creación/apertura de su
archivo hasta una persistencia explícita. Por eso cero coincidencias durante un
preflight sin tarea no distinguen entre propagación fallida, estado SQLite fuera
del árbol temporal o un artefacto que aún no estaba abierto. Es posible demostrar
el vínculo, pero no con el oráculo actual.

**H-C4 — diagnóstico:** el inventario global se tomó mientras la sesión Codex
controladora permanecía activa. Codex mantiene bases SQLite y rollouts
persistentes; por tanto esa sesión puede cambiar el árbol personal observado
durante la ventana. El control queda contaminado por su propio observador. Esto
no demuestra que la controladora ni una raíz SQLite heredada hayan causado los
tres cambios HMAC del intento fallido.

**Corrección mínima propuesta, todavía no aplicada:**

1. Fijar en una sola raíz temporal `CODEX_HOME`,
   `CODEX_SQLITE_HOME`/`sqlite_home` y `log_dir`, con historial desactivado y
   autenticación `ephemeral`; autocomprobar la consulta `lsof` y exigir selección
   AND entre el PID nativo exacto y un descriptor SQLite/log conocido.
2. Ejecutar el próximo inventario y la coordinación desde un supervisor externo
   revisado, con todos los clientes que usan el estado personal cerrados. Una
   sesión Codex posterior solo puede leer el resultado sanitizado.

**Evidencia faltante:** no se conservó la raíz SQLite/log efectiva del hijo, la
identidad de los tres caminos cambiados ni el predicado exacto usado por el
sondeo. Tampoco se ha validado todavía el supervisor externo ni el vínculo con
las raíces fijadas. Obtener esas pruebas requiere primero corregir y revisar el
contrato y, después, otra autorización de ejecución. Las trazas de filesystem
disponibles localmente requieren privilegios administrativos y no son la opción
mínima ni están autorizadas.

## Corrección dirigida del contrato OTel v1.2-r3 — 2026-09-29

Se modificó únicamente
[OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md) para resolver H-C2,
H-C4 y sus efectos directos. El contrato resultante se identifica como v1.2-r3,
SHA-256
`ac685955886ba10a1171a5f7787c0d0195613661215f2cd400ded35097da60ad`.

- **H-C2:** `CODEX_HOME`, `CODEX_SQLITE_HOME`/`sqlite_home` y `log_dir` deben
  quedar dentro de una sola raíz temporal. El supervisor autocomprueba el
  observador con un descriptor centinela y controles negativos; el PASS exige
  selección AND entre el PID nativo exacto y un descriptor SQLite/log de una
  allowlist cerrada. Un rollout no materializado no sirve como único oráculo.
- **H-C4:** antes del baseline debe haber cero procesos Codex. Durante la ventana
  solo se admite el árbol exacto iniciado por un supervisor externo revisado;
  ese supervisor inventaría, coordina, cierra, elimina el temporal y compara
  antes de que otra sesión Codex pueda leer el resultado sanitizado.
- **Conservado:** A2/D12-AUTH, P1–P4, R-OTEL-C12-01/02/03,
  R-OTEL-P4-01/02, R-OTEL-01–03 y todos los cierres anteriores.

La corrección no atribuye los tres cambios HMAC del intento fallido ni demuestra
que la nueva topología funcione en vivo. No se abrió proceso, pane, sesión,
login o red; no se leyó sesión, credencial, ruta personal cambiada o valor de
configuración; no se ejecutó preflight, H-C5/Paso 3 ni se cambió router,
launcher o configuración global.

**Estado:** PLAN_CON_INCERTIDUMBRE_CRITICA, listo únicamente para revisión
dirigida de H-C2, H-C4 y efectos directos. El review v1.2-r2 permanece histórico;
v1.2-r3 todavía no está revisado ni aprobado.
