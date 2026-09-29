# Revisión técnica y funcional — alternativa OTel / bloques

**Resultado vigente:** ronda dirigida del 2026-09-28, **APROBADO** para el plan
condicionado OTel v1.1; R-OTEL-01–03 cerrados documentalmente. Ver el addendum al
final. La revisión inicial siguiente conserva su versión y evidencia histórica.

Fecha: 2026-09-26. Ronda inicial, reviewer inline en la misma conversación;
sin independencia de contexto ni delegación. **VEREDICTO: REQUIERE_AJUSTES.**

## Objeto, versión y autorización

Se revisó [Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md),
propuesta fechada 2026-09-26, sin número de versión, 501 líneas. Identidad SHA-256:
`5a1c949424376f3b010c81357e19d127e617fe922600d0d13fb84690f194a54d`.
No se modificó ese archivo ni se lo convirtió en el plan vigente.

Base: [criterios v2 aprobados](01_ACCEPTANCE_CRITERIA.md),
[D01](02_DECISION.md), [plan v2](03_PLAN.md), [review anterior](04_PLAN_REVIEW.md),
[evidencia](EVIDENCE.md), [review de implementación](05_IMPLEMENTATION_REVIEW.md)
y [estado](STATE.md). HEAD local `2b92c74602bf244e9a3e03829e5c07f2b233e8a4`;
el plan alternativo, el requirement y los módulos del observador tienen trabajo
local sin commit. HEAD por sí solo no identifica la implementación inspeccionada.

Se aplicó `01_POLITICA_COMUN.md` tal como fue incluida por el usuario y el
procedimiento de review solicitado. No hay archivo con ese nombre ni AGENTS.md
en la raíz/ancestros inspeccionados; las instrucciones AGENTS aportadas en la
conversación son aplicables. Procedimiento canónico consultado:
[contrato compartido](../../../workflow/00_SHARED_CONTRACT.md),
[plan-reviewer](../../../skills/core/plan-reviewer/SKILL.md) y
[workflow 05](../../../workflow/05_PLAN_REVIEW.md).
Prevalece la orden explícita de no corregir el plan ni iniciar otra ronda.

**Nivel 2 / N2 confirmado:** cambia contratos de medición, atribución,
persistencia e integración local, con impacto acotado y reversible. No hay
evidencia de cambio de autorización, producción o infraestructura transversal
que justifique N3. La edición documental de esta revisión no equivale a
clasificar como editorial la funcionalidad propuesta.

## Cobertura y orden revisados

| Obligación vigente | Cobertura propuesta | Resultado |
|---|---|---|
| AC01–AC03: cinco actividades, acciones prospectivas y procedencia | §§1, 5.1–5.3; pasos 0–3 | Cuatro bloques declarados constituyen un cambio funcional pendiente de explicitar; R-OTEL-01. |
| AC04–AC06: relación verificable, cobertura completa de acciones, mezclas y conciliación | §§5.3–5.4, 5.6; pasos 2–3, 7 | Conserva no prorratear y no asignar por recepción. Debe precisar si preserva exclusividad por acciones completas; R-OTEL-01. Completitud de captura: R-OTEL-03. |
| AC07–AC08: tiempo observable, activo unknown y USD con evidencia | D3, §5.5, exclusión monetaria | Recuperar decisiones ya aprobadas; cualquier cambio se propone expresamente, R-OTEL-01. |
| AC09: histórico proyecto/tarea/actividad y revisiones compatibles | §6; pasos 4–6 | Reutilización genérica no asegura ese resultado; R-OTEL-02. |
| AC10/AC12: Kev y evaluación real | §1, §5.2 | Sustitución propuesta por marcas y reglas, no cumplimiento de esos criterios; R-OTEL-01. |
| AC11: privacidad y ámbito autorizado | §8; pasos 1–2, 7 | Filtrado previo, permiso acotado y no persistencia de contenido previstos. |
| AC13: integración automática demostrada | pasos 2–3, 8 | Pruebas reales tempranas pertinentes; viabilidad local aún no demostrada. |

El orden auditoría → decisiones → captura → atribución → spec → integración es
ejecutable como investigación condicionada. Los pasos tienen objetivo, salida y
condición de avance. El detalle futuro es suficiente salvo los contratos
señalados abajo. No se exige implementación anticipada ni prototipo durante este
review. La ruta preferida y la restricción de Plan mode ya están reconocidas;
no se reportan como defectos nuevos.

## Evidencia comprobada y límites

- Local: `command -v codex` resolvió `/opt/homebrew/bin/codex`, enlace a la
  distribución Node oficial; `codex --version` devolvió `codex-cli 0.157.0`
  con advertencia de sandbox al crear aliases de PATH. `herdr` existe como
  ejecutable Mach-O en `~/.local/bin/herdr`. Esto **no verifica** el ejecutable,
  configuración ni capacidades efectivamente usados por herdr. No se abrió un
  chat ni se leyó configuración global o contenido de sesiones.
- [Configuración avanzada oficial](https://developers.openai.com/codex/config-advanced/):
  exportación OTel, eventos de consumo y resultados de herramientas documentados.
  [Referencia de configuración](https://developers.openai.com/codex/config-reference/):
  exportadores y control de prompts existen. Su disponibilidad documental no
  prueba una captura local ni ausencia de contenido en otros eventos.
- [Telemetría en rust-v0.157.0](https://github.com/openai/codex/blob/rust-v0.157.0/codex-rs/otel/src/events/session_telemetry.rs),
  líneas 540–575 y 1034–1052, obtenida como fuente pública: registra desgloses de
  uso; `tool_token_count` toma `usage.total_tokens`, no tokens adicionales de
  herramientas. Esas funciones no prueban por sí solas una clave de unión con
  los hooks; no se concluye que otros spans carezcan de ella.
- [Hooks oficiales](https://developers.openai.com/codex/hooks/): herramientas
  locales como `update_plan` tienen observación; las hospedadas como WebSearch
  no siguen ese camino. Hay identidad de sesión/turno/herramienta, pero eso no
  demuestra cobertura de acciones ni enlace al uso. La documentación distingue
  hooks síncronos y efectos de sus respuestas: el límite neutral previsto es pertinente.
- [Handler en rust-v0.157.0](https://github.com/openai/codex/blob/rust-v0.157.0/codex-rs/core/src/tools/handlers/plan.rs),
  líneas 80–89: rechaza `update_plan` en Plan mode.
  [Schema de la misma etiqueta](https://github.com/openai/codex/blob/rust-v0.157.0/codex-rs/core/src/tools/handlers/plan_spec.rs):
  `step` y `status` están definidos; la convención `[ACT:...]` sería propia.
  Se contrastó con la etiqueta coincidente con el CLI del PATH, no con una
  equivalencia binaria ni una ejecución bajo herdr demostradas.
- [Uso de razonamiento](https://developers.openai.com/api/docs/guides/reasoning):
  el desglose de razonamiento está dentro de salida. No sumar nuevamente es correcto.
- [File Exporter](https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector-contrib/main/exporter/fileexporter/README.md):
  madurez alpha, `append: false` por defecto y restricción de append con rotación
  confirmadas. Fijar versión antes del piloto ya está previsto; no se instaló Collector.
- [OTLP, garantías y duplicados](https://opentelemetry.io/docs/specs/otlp/):
  entrega extremo a extremo no garantizada; retransmisión puede duplicar datos.
  La ecuación interna del reporte no demuestra ausencia de pérdidas.
- Reutilización local real: [work_activity.py](../../../scripts/lib/work_activity.py)
  líneas 18–21 define las cinco categorías y estados conservadores;
  [plan_usage.py](../../../scripts/lib/plan_usage.py) líneas 1133–1148 exige
  `manifest_complete`, conserva mixtos y unknown; 1151–1248 contiene snapshots,
  revisiones, `project_id`, `work_id` e histórico. Se inspeccionó código,
  no se reejecutaron gates cerrados.

## Hallazgos obligatorios

### R-OTEL-01 — OBLIGATORIO — cambio del contrato funcional sin transición explícita

**Referencia:** plan alternativo L8, L28, L70–74, L90–129, L158–164 y L429;
criterios v2 AC01, AC03–AC08, AC10, AC12; D01 aprobada.

**Evidencia:** el objetivo vigente distingue feature, bug, test, explanation y
documentation. El candidato propone Análisis/Desarrollo/Pruebas/Documentación,
declara bloques en lugar de inferir categorías por acciones y elimina Kev.
Excluye cálculo monetario, ofrece activo observable como candidato y exige
cero consumo pendiente en el caso final. Los criterios vigentes conservan
mixtos/sin atribuir, activo unknown y USD solo con evidencia directa.

**Problema:** el cambio de enfoque está propuesto, pero no hay correspondencia
que diga qué resultados se conservan, sustituyen o dejan fuera, ni cuáles
requieren decisión humana. D4 sobre casos mixtos no resuelve la desaparición
del desglose feature/fix o la clasificación de explicaciones. Una marca de
bloque no satisface automáticamente AC04 sobre acciones completas.

**Consecuencia:** dos implementaciones pueden aprobar el documento y producir
históricos con significado distinto; la aprobación anterior de v2 podría
aplicarse incorrectamente a este contrato nuevo. También podría exigirse una
separación perfecta adicional no acordada, o relajar la exclusividad anterior.

**Corrección mínima:** añadir una tabla de cambios frente a AC01–AC13 y D01,
con resultado conservado/propuesto y validación. Resolver expresamente la
taxonomía, medición por bloque declarado frente a acción observada, tratamiento
de mezcla y alcance del cierre sin pendientes. Mantener USD y tiempo activo
según decisiones vigentes salvo propuesta explícita de cambio; no hace falta
añadir cálculo de precios. Identificar que la alternativa necesita aprobación
propia y que A04 no se considera aprobada por dejar de usar Kev.

### R-OTEL-02 — OBLIGATORIO — falta el contrato de histórico y compatibilidad

**Referencia:** plan alternativo L210, L292–316, L324–342 y L414–429;
AC09; `plan_usage.py` L1151–1248.

**Evidencia:** existe histórico por proyecto/tarea con snapshots versionados.
El plan describe persistencia por ejecución/sesión y un reporte por bloques;
no exige consulta acumulada por proyecto/tarea, revisiones al reclasificar,
ni conservación de reportes v1/v2 como criterio de terminado.

**Problema:** reutilizar lo existente es una intención, pero un reporte aislado
por ejecución también cumpliría los pasos 5–6 redactados. Reprocesar sin
duplicación no demuestra compatibilidad ni inmutabilidad de snapshots previos.

**Consecuencia:** puede terminarse el nuevo registrador sin entregar el histórico
solicitado o alterando el significado de datos ya cerrados.

**Corrección mínima:** fijar en pasos 4–6 y aceptación la identidad
proyecto→trabajo→ejecución, histórico JSON/texto y política de revisiones,
conservando salidas previas y sin importar trabajo pasado. Referenciar los
puntos reutilizables reales sin diseñar todavía un schema detallado. Añadir
regresión dirigida con dos trabajos y una revisión posterior, más un snapshot
legacy preservado; no reabrir íntegramente S01–S03/H01/H02/A01–A03.

### R-OTEL-03 — OBLIGATORIO — completitud exigida sin evidencia de cierre definida

**Referencia:** plan alternativo L174–185, L262–266, L294, L318, L352–367,
L375–384 y L422–429; OTLP, apartados Protocol Details y Known Limitations.

**Evidencia:** la comparación con una fuente del mismo ámbito es condicional
(«cuando exista»/«si está disponible»), mientras que el cierre exige conciliación
de la ejecución sin faltantes. El avance de captura comprueba identidad y
granularidad, pero no fija qué evidencia permitirá declarar captura completa.
La validación incluye duplicados y caída del receptor, no una pérdida selectiva
que deje coherentes los datos recibidos.

**Problema:** todas las filas recibidas pueden sumar correctamente y aun faltar
una respuesta completa. La reconciliación interna y la ausencia de errores no
descartan esa pérdida. El plan reconoce el riesgo, pero deja abiertas dos
interpretaciones del criterio de cierre.

**Consecuencia:** se puede declarar cumplimiento completo sin demostrar todo
el consumo del ámbito autorizado, o descubrir recién al final que no existe
forma de demostrarlo.

**Corrección mínima:** definir, al cualificar la fuente en paso 2, qué referencia
del mismo ámbito o mecanismo verificable de completitud se usará y qué ocurre
si falta. Sin esa evidencia, captura incompleta/no verificada y sin cierre
completo; puede continuar solo el subalcance explícitamente independiente.
Añadir un caso reproducido con una unidad omitida y otro con entrega final
retrasada, verificando que no producen un falso cierre. No exige segundo canal
de captura ni lectura de sesiones en esta revisión.

No se agregan notas opcionales: los límites restantes ya están tratados como
decisiones o condiciones futuras en el propio plan.

## Evidencia previa y validación proporcional

F01–F04 de implementación y cierres S01–S03/H01/H02/A01–A03 se conservan; no se
reabren. F06/F07 pertenecen a A04 y no bloquean técnicamente una auditoría OTel
independiente, pero tampoco se cierran por proponer otra ruta.
La muestra histórica de 176445.453 ms no prueba una latencia estable ni, sin
presupuesto acordado, inviabilidad absoluta. No se repitió T14. Además,
`tests/work_activity_kev_dataset.py` L11–24 produce el mismo texto para distintas
etiquetas y comparte textos entre desarrollo/evaluación: no reutilizar ese corpus
como oráculo de precisión de la nueva ruta. Se registra como contexto verificado,
sin autorizar cambios al corpus congelado.

Ajustes necesarios: únicamente las comprobaciones de R-OTEL-02/03 y adaptar la
validación al contrato que resulte de R-OTEL-01. Los casos de caché, duplicados,
esperas, interrupción, privacidad y degradación ya previstos son pertinentes.
No se requieren benchmark Kev, regresión general, pruebas de carga ni prototipo
adicional para emitir este review. El cero-pendientes de L429 requiere decisión
explícita frente al contrato conservador previo; no se lo elimina por iniciativa
del reviewer para facilitar el éxito.

## Conclusión y siguiente acción

**Plan completo: REQUIERE_AJUSTES**, por R-OTEL-01–03. La ausencia de prueba local
no demuestra fallo; impide confirmar viabilidad de la integración. Faltan:
ejecutable/configuración efectivos bajo herdr, señal de bloques aplicable al
modo real, vínculo uso→bloque con cobertura y evidencia de completitud.
Resolverlo corresponde a los pasos 0–3 acotados, no a experimentos en este review.

**Subalcance independiente: Paso 0 APROBADO técnicamente como auditoría de solo
lectura.** Inventario de versión, señales y componentes reutilizables no necesita
elegir taxonomía ni instalar Collector. No habilita pasos 1–8 ni prueba la
viabilidad por extensión. No se ejecutó la auditoría completa ni se solicita
aprobación para un segundo frente: la siguiente tarea sigue siendo la corrección.

Siguiente acción única: corregir el mismo plan mediante `03_PLANIFICAR.md`,
limitada a R-OTEL-01–03; no reemplazar el enfoque ni implementar. Ese nombre
designa el procedimiento solicitado por el usuario, no un ejecutable comprobado
en este checkout. No se inicia otra ronda por cuenta propia. Solo después de
resolver obligatorios corresponde pedir aprobación del plan concreto y registrar
la decisión con el procedimiento `09_REGISTRAR_APROBACION.md`; la aprobación v2
anterior no se vuelve a pedir y no se transfiere a esta alternativa.

Routing: se aplica `routing-v1` y el catálogo canónico v2.2.2 consultado hoy.
Review N2 recomendado ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High; fallback
GPT-5.6 Terra (`gpt-5.6-terra`) / High o XHigh. Switch Benefit MEDIUM: la
inspección documental y de contratos permite esta revisión inline sin nuevo
gate. Configuración efectiva NO VERIFICADA. Corrección documental dirigida:
BALANCED / Medium según estrategia vigente; no se cambió modelo ni configuración.

Validación de esta entrega: SHA-256 del plan original sin cambios, 23 enlaces
locales de los tres documentos resueltos, findings/referencias de estado y
espacios finales del review PASS; `git diff --check` PASS. El primer comprobador
documental falló al exigir el ID completo donde el estado usa el rango
`R-OTEL-01–03`; se corrigió el comprobador y pasó, sin cambiar el contrato.
Pruebas de producto, sesiones, Collector y Kev NO EJECUTADOS. Solo se editaron
este review, STATE.md y PROJECT_STATE.md. Sin instalaciones, commits ni publicación.

## Ronda dirigida — OTel v1.1 — 2026-09-28

**VEREDICTO: APROBADO. Sin observaciones accionables pendientes en el alcance
revisado.** Se cierra esta revisión técnica; no se inicia otro ciclo.

### Objeto y límites

[Plan OTel v1.1](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md),
SHA-256 `e3aeaed403d38402471644b5d3f1e024679b57819bc4a106f4fbd4c0cd1c95d3`,
corrección del 2026-09-28. Se verificó ese hash antes de revisar. Modalidad:
review inline de un plan corregido en esta misma conversación, sin independencia
de contexto ni delegación. Nivel **N2 confirmado**, sin cambio del efecto local
sobre contratos, atribución y persistencia.

Autorización: pedido explícito de revisar solo R-OTEL-01–03 y efectos directos,
registrando el resultado, sin código ni pilotos. Procedimientos aplicados:
[04_REVISAR_PLAN.md](../../../../workflow_verificable/04_REVISAR_PLAN.md),
[política común](../../../../workflow_verificable/01_POLITICA_COMUN.md) y skill
canónica [plan-reviewer](../../../skills/core/plan-reviewer/SKILL.md).
No se reabrió la auditoría general ni las slices cerradas.

### Resolución de obligatorios

Las líneas citadas corresponden al hash v1.1 indicado, no a la versión inicial.

| ID / resultado | Evidencia de corrección | Consecuencia y comprobación de efectos directos |
|---|---|---|
| **R-OTEL-01 — CERRADO** | §1.1, L43–106: matriz AC01–AC13/D01 y P1–P3; §5.3, L195–206: enlace y acciones completas; §5.5, L237–250: activo unknown; §6.1, L356–361: USD con evidencia; §10, L601–608: aceptación acotada. | El cambio de taxonomía/clasificador ya no hereda aprobación anterior. Cuatro grupos conservan los detalles, incluidas explicación sin archivo y feature/fix. Mezclas internas del mismo bloque permanecen mixtas en el detalle; las vistas no se suman entre sí (L79–85, L264–267). P3 es propuesta humana explícita y no garantía universal. No se debilitó AC04 ni se cerró A04 por sustituir Kev. No requiere otra corrección documental. |
| **R-OTEL-02 — CERRADO** | §6.1, L325–361; pasos 4–6, L449–503; pruebas L524–525; criterio L596. | Histórico proyecto/tarea/ejecución en JSON/texto, extensión versionada opt-in y snapshots v1/v2 preservados son resultados exigidos. Reclasificación conserva contadores; datos tardíos crean revisión distinta. El agregado elige una revisión consistente sin borrar las anteriores. Se cubren dos tareas, revisión posterior y legacy; no se exige repetir gates cerrados. No requiere otra corrección documental. |
| **R-OTEL-03 — CERRADO** | §5.6, L269–296; paso 2, L419–423; paso 3, L441; pruebas L526–527; pasos 8/aceptación, L544 y L593. | Ya no es opcional demostrar completitud para avanzar a integración/cierre. Origen, ámbito, comparación y entrega final deben cualificarse. Se distinguen captura incompleta/no verificada y cobertura de acciones. Pérdida selectiva o evento tardío impiden falso cierre, aun si las filas recibidas suman bien. No presume señales nativas ni autoriza otro canal. No requiere otra corrección documental. |

La evidencia local pertinente se contrastó por lectura en
`scripts/lib/plan_usage.py`: exclusividad/unknown L1133–1148,
`snapshot_activity_report` L1151–1173 e histórico L1189–1253. Confirma puntos
reutilizables; no se afirma que la extensión OTel, las nuevas vistas ni todas
las garantías propuestas estén implementadas. Las afirmaciones sobre APIs que
no cambiaron conservan la evidencia fechada del review inicial; no se efectuó
una nueva certificación de versiones ni disponibilidad del host.

### Validación y viabilidad

**Ajustes adicionales de validación: ninguno.** Las pruebas añadidas responden
a los tres riesgos y son proporcionales. El caso real de pasos 2–3 cualifica la
integración; los casos reproducidos de paso 7 prueban lógica y fallos, sin
confundir ambos tipos de evidencia. No se pide otro prototipo para aprobar la
corrección ni un benchmark Kev. Las pruebas están previstas, NO ejecutadas.

No falta evidencia para concluir sobre estas correcciones documentales. **Sí
falta evidencia para declarar viable o implementada la integración:** ejecutable
y configuración efectivos bajo herdr, señal automática enlazable con acciones
completas, referencia del mismo ámbito y condición de entrega final. El propio
plan las convierte en condiciones tempranas de avance (pasos 0–3); si fallan,
no habilitan spec/integración dependientes ni cierre completo.

El veredicto aprueba el **plan como recorrido condicionado de comprobación e
integración**, no una implementación ya viable. Paso 0 sigue siendo independiente;
su revisión favorable no se extiende como validación de pasos 2–8. La marca
`PLAN_CON_INCERTIDUMBRE_CRITICA` del documento describe esa incertidumbre técnica
y no contradice el cierre del review. El plan permanece intacto; su texto de
estado es el snapshot presentado al reviewer, con resultado vigente en STATE.

Routing heredado para review N2: ADVANCED / High según catálogo canónico v2.2.2
contrastado; alcance acotado y evidencia suficiente para revisión inline.
Switch Benefit MEDIUM, sin gate nuevo. Modelo/reasoning efectivos NO VERIFICADOS.

### Decisión humana pendiente y siguiente acción

Según [09_REGISTRAR_APROBACION.md](../../../../workflow_verificable/09_REGISTRAR_APROBACION.md):
objeto **OTel v1.1, hash arriba, P1–P3**; decisión real **PENDIENTE**.
El pedido actual autoriza review/registro, no aprobación del plan. Las
aprobaciones v2 anteriores siguen vigentes en su alcance y no se vuelven a pedir.

Siguiente acción única: solicitar aprobación concreta de OTel v1.1 y sus
decisiones P1 (cuatro bloques con detalles conservados), P2 (marcas/reglas en
lugar de Kev con atribución verificable) y P3 (caso de aceptación acotado sin
consumo mixto/sin atribuir ni detalle requerido desconocido, con captura completa).
USD con evidencia y activo unknown ya estaban decididos y se conservan.

La aprobación permite formalización documental dentro de las dependencias del
plan; no permite implementar, instalar, cambiar configuración ni ejecutar
pilotos o leer sesiones. En particular, la spec definitiva del paso 4 sigue
condicionada a evidencia de pasos 2–3. No se solicitan permisos extra ni se
ejecuta Paso 0 por extensión en esta ronda. Sin publicación ni commit.

Validación de registro de esta ronda: comparación de integridad de 451 archivos
confirma cambios solo en este review, STATE.md y PROJECT_STATE.md; plan y código
intactos. 37 enlaces locales/anclas y referencias de veredicto PASS;
`git diff --check` PASS. No se ejecutaron pruebas de producto ni pilotos.

## Ronda dirigida — plan OTel v1.2 / P4 — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.** La organización por bloques es coherente con
el objetivo, pero quedan dos ambigüedades obligatorias antes de formalizar spec
o slices. P1–P4 continúan aprobadas como decisiones humanas; R-OTEL-01–03 y los
cierres S01–S03/H01/H02/A01–A03 no se reabren.

### Nivel, objeto y límites

Nivel **N2**, por efecto acotado sobre el contrato de atribución, el histórico y
la conciliación. Objeto revisado: [plan OTel v1.2](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md),
SHA-256 `53ae25ef657d8549b54f325af34ba15073bb56d131d423f6572e2cba726deb64`,
solo P4 (§1.2/§5.2.1) y sus efectos directos en §6.1, pasos 3–7 y §10.

Se aplicaron [04_REVISAR_PLAN.md](../../../../workflow_verificable/04_REVISAR_PLAN.md),
[01_POLITICA_COMUN.md](../../../../workflow_verificable/01_POLITICA_COMUN.md) y
la skill `plan-reviewer`. Revisión inline, sin delegación. No se revisó otra vez
el diseño completo ni se implementó, formalizó o ejecutó el recorrido futuro.

### Trazabilidad revisada

| Criterio/decisión | Plan | Validación prevista | Resultado del review |
|---|---|---|---|
| AC01/P4: tarea multiactividad sin categorías manuales | §1.2; §5.2.1; paso 3 | tarea con cuatro actividades y retorno test→bug→test | Cubierto: Quiver propone bloques y el agente registra transiciones sin intervención del usuario. |
| AC04/AC05: exclusividad, mezcla y falta de enlace | §5.2.1 puntos 2–5; §5.3 | discrepancia plan/acción, cruce de bloques, marca ausente | Cubierto a nivel de categoría; queda ambigua la presentación por bloque cuando una unidad pertenece a dos bloques iguales (R-OTEL-P4-02). |
| AC06: una unidad contada una sola vez | §5.2.1 punto 4; §5.6; paso 6 | transiciones, datos tardíos y no duplicación | La intención está definida; falta una regla aditiva inequívoca para el detalle por bloque (R-OTEL-P4-02). |
| AC09: histórico y revisiones | §5.2.1; §6.1; pasos 4–7 | cambio de versión, reanudación y snapshot previo | Cubierto, condicionado a resolver R-OTEL-P4-02. No migra ni recategoriza históricos previos. |
| AC13/P3: recorrido real completo | pasos 2–3/8; §10 | primera llamada, transiciones, captura y atribución completas | Correctamente condicionado: P4 no sustituye la captura ni permite cerrar por simulación. |

El orden sigue siendo ejecutable como recorrido condicionado: captura PASS antes
de atribución; atribución real antes de spec dependiente; integración y aceptación
después. [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md) continúa como
dependencia pendiente con INFORMACIÓN INSUFICIENTE. No se extiende este veredicto
a H-C1–H-C5 ni se autoriza una sesión o piloto.

### R-OTEL-P4-01 — OBLIGATORIO — decisiones aprobadas todavía figuran como pendientes

**Referencia precisa:** plan v1.2 L166–184, especialmente D4/D5 y la apertura de
§5; frente a L50, L93–119 y STATE, que registran P1–P4 aprobadas.

**Evidencia:** D4 indica “Resolver P1/P2”, D5 “Resolver P3” y §5 declara que las
decisiones pendientes de §4 no se consideran aprobadas. En la misma versión,
P1–P3 constan aprobadas y P4 aceptada.

**Problema o ambigüedad:** el plan distingue bien evidencia técnica pendiente,
pero esas frases vuelven a presentar como decisión humana pendiente algo ya
resuelto.

**Consecuencia:** una ejecución válida podría detenerse para pedir nuevamente
P1–P4 o tratar su contrato funcional como no decidido, contrariando el estado.

**Corrección mínima:** actualizar D4/D5 y la apertura de §5 para decir que las
decisiones están aprobadas y que lo pendiente es demostrar señales, primera
llamada, transiciones y cobertura. No cambiar el contenido de P1–P4 ni solicitar
otra aprobación.

### R-OTEL-P4-02 — OBLIGATORIO — falta una regla única para consumo compartido entre bloques iguales

**Referencia precisa:** plan v1.2 L270–272; jerarquía del histórico L447–451;
cálculo y detalle por bloque L597–620; pruebas P4 L640–643; AC04/AC06/AC09.

**Evidencia:** el plan conserva una unidad indivisible enlazada a dos bloques de
la misma categoría y prohíbe crear dos cargos exclusivos. A la vez exige calcular
tokens por bloque y mostrar detalle por cada ejecución. El código reutilizable
actual agrega cada `response_id` una sola vez por categoría
(`plan_usage.py` L1133–1148) y todavía no tiene dimensión de bloque.

**Problema o ambigüedad:** no se define si esa unidad se muestra en ambos bloques,
solo en el agregado de categoría o en un estado compartido no aditivo. Tampoco se
define qué suma puede usar el histórico para evitar repetirla.

**Consecuencia:** dos implementaciones compatibles con el texto pueden producir
detalles distintos o duplicar tokens al sumar bloques, aunque el total por
categoría sea correcto.

**Corrección mínima:** fijar que cada unidad tiene un único propietario contable
en cualquier agregado. Si no puede separarse entre bloques de la misma categoría,
debe mostrarse como compartida/no desglosable y las referencias desde ambos
bloques deben ser no aditivas; el plan puede elegir otra representación con la
misma garantía. Añadir un caso dirigido con dos bloques iguales y una respuesta
indivisible que verifique JSON/texto, detalle y total sin duplicación.

### Validación y evidencia faltante

Los únicos ajustes de validación son los de R-OTEL-P4-02 y la consistencia
documental de R-OTEL-P4-01. Las pruebas ya previstas para transiciones,
discrepancias, datos tardíos, interrupciones, revisiones y snapshots son
proporcionales. No hacen falta nuevas pruebas generales, benchmark Kev ni piloto
para corregir el plan.

No falta evidencia para emitir este veredicto documental. Sí falta para declarar
viable la implementación: aislamiento H-C1–H-C5, contadores completos, identidad
de respuesta y productor automático con cobertura de acciones. Esa incertidumbre
ya está separada y bloquea pasos 2–3, no la corrección de estos dos hallazgos.

Routing de review conservado: ADVANCED / High para N2; Switch Benefit MEDIUM,
sin Model Gate nuevo. Configuración efectiva NO VERIFICADA. No se cambió modelo,
router, launcher o configuración.

### Siguiente acción única

Corregir el mismo plan con `03_PLANIFICAR.md`, exclusivamente para
R-OTEL-P4-01 y R-OTEL-P4-02. No iniciar otra ronda de revisión, spec, slices,
piloto o implementación. Las aprobaciones P1–P4 siguen vigentes y no se vuelven
a solicitar.

Validación de registro: el plan conserva SHA-256
`53ae25ef657d8549b54f325af34ba15073bb56d131d423f6572e2cba726deb64` y el
contrato de aislamiento v1.2 conserva SHA-256
`98c85652b24c86b68fddb8dbe20cca8d00f334d8f53dec05888b47f875a1692a`.
Review, STATE, PROJECT_STATE y HANDOFF coinciden en veredicto, hallazgos y
siguiente acción; `git diff --check` PASS y no se encontraron espacios finales
inválidos en esos documentos. Pruebas de producto y pilotos: NO EJECUTADOS.

## Ronda dirigida — plan OTel v1.3 / cierre P4 — 2026-09-28

**VEREDICTO: APROBADO. Sin observaciones accionables.**

### Nivel y alcance efectivamente revisado

- **Nivel:** N2, revisión inline del contrato de atribución y de su contabilidad.
- **Objeto:**
  [Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md),
  versión OTel v1.3, SHA-256
  `48827d6014612796b42cd5982bb640c229fad1f524e2cfbefa82590a576d2209`.
- **Límite aplicado:** únicamente R-OTEL-P4-01, R-OTEL-P4-02 y los efectos
  directos de sus correcciones en D4/D5, §5, histórico, cálculo, validación y
  condición de cierre. No se reabrieron P1–P4, R-OTEL-01–03 ni los cierres
  S01–S03/H01/H02/A01–A03.
- **No incluido:** revisión o aprobación de
  [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md), implementación,
  spec, slices, sesiones, pilotos o pruebas de producto.

### Cierre de hallazgos

| ID | Estado | Evidencia verificada | Resultado y efecto directo |
|---|---|---|---|
| R-OTEL-P4-01 | CERRADO | D4/D5 L178–179 y apertura de §5 L187–191 | P1/P2/P4 y P3 figuran como aprobadas. El texto separa correctamente esas decisiones de las señales, transiciones, cobertura e integración todavía no demostradas, y prohíbe volver a solicitarlas. |
| R-OTEL-P4-02 | CERRADO | Regla de bloque compartido L277–283; propietario único y conciliación L308–328; histórico L494–499; cálculo L637–639; prueba dirigida L684; condición final L759 | Una unidad indivisible compartida por bloques iguales tiene un solo propietario aditivo, `shared_within_category`. Los bloques conservan la misma identidad solo como referencia no aditiva. JSON, texto, detalle, categoría y total general deben coincidir sin duplicación. |

La corrección también conserva el límite de P3: la parte individual de cada
bloque compartido permanece `unknown`, y L764–771 impide declarar cumplimiento
completo cuando un detalle requerido siga desconocido. Por lo tanto, la regla
contable evita duplicar consumo sin convertir una falta de desglose en un PASS.

### Validación y dependencias

No hacen falta ajustes adicionales de validación para estos dos hallazgos. El
caso dirigido de L684 comprueba la misma identidad, el único propietario, las
referencias no aditivas y la conciliación en JSON/texto, detalle y totales. La
condición de cierre de L759 exige el mismo resultado.

La aprobación documental de v1.3 no demuestra la integración viva. El contrato
de aislamiento v1.2 conserva SHA-256
`98c85652b24c86b68fddb8dbe20cca8d00f334d8f53dec05888b47f875a1692a`,
estado INFORMACIÓN INSUFICIENTE y sus gates H-C1–H-C5 pendientes. Contadores
completos, identidad de respuesta, aislamiento y productor automático siguen
siendo evidencia necesaria antes de captura/atribución real. No se aprueban por
extensión.

No se corrigió el plan ni se ejecutaron código, sesiones, pilotos o pruebas. El
review cierra R-OTEL-P4-01/02 para el hash indicado; P1–P4 y los cierres previos
se conservan.

### Siguiente acción única

Revisar `OTEL_PILOT_CONTRACT_v1.2.md` de forma dirigida, limitada a F12-01–F12-05
y H-C1–H-C5, sin abrir una sesión ni ejecutar un piloto. Esa revisión requiere
autorización separada porque el alcance actual termina con el plan OTel v1.3.

## Ronda dirigida — contrato OTel v1.2 / aislamiento — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.**

### Nivel y alcance efectivamente revisado

- **Nivel:** N2, por aislamiento de configuración, autenticación y reversión.
- **Objeto:** [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md),
  SHA-256 `98c85652b24c86b68fddb8dbe20cca8d00f334d8f53dec05888b47f875a1692a`.
- **Límite:** F12-01–F12-05, H-C1–H-C5 y sus efectos directos. No se revisaron
  otra vez P1–P4, R-OTEL-01–03, R-OTEL-P4-01/02 ni cierres anteriores.
- **Comprobaciones permitidas:** ayuda y versión locales, documentación oficial
  y evidencia ya sanitizada. No se abrió Codex/herdr, no se leyó autenticación,
  no se ejecutó piloto y no se modificó el contrato o la configuración.

### Resultado por hecho y gate

| Elemento | Resultado de la revisión |
|---|---|
| F12-01 | La escritura de trust y el bloqueo v1.1 siguen siendo evidencia histórica válida para Codex 0.157.1. El ejecutable actual del PATH informa 0.158.0; la ayuda conserva `--no-daemon`, `--strict-config`, `-c`, `--profile` y `CODEX_HOME`, pero el comportamiento de la versión nueva no fue observado. |
| F12-02 | CONFIRMADO: la documentación oficial vigente conserva los perfiles como capa sobre la configuración base; no son aislamiento. |
| F12-03 | PARCIALMENTE REFORZADO: la documentación oficial ahora afirma que el estado local vive bajo `CODEX_HOME`, incluidos configuración, autenticación por archivo, historial, logs y cachés. Falta demostrar el proceso 0.158.0 lanzado por herdr. |
| F12-04 | CONFIRMADO COMO RIESGO: la documentación distingue almacenamiento `file`, `keyring`, `auto` y `ephemeral`; ninguno aporta por sí solo una credencial. El contrato todavía no tiene una fuente de autenticación aprobada. |
| F12-05 | CONFIRMADO EN SU LÍMITE: `herdr agent start --help` 0.8.0 no documenta variables de entorno por agente. La ausencia de esa opción no prueba que el proceso hijo herede correctamente una variable preparada en la pane. |
| H-C1/H-C2 | NO DEMOSTRADOS. La documentación vuelve plausible la raíz temporal, pero no prueba su propagación ni uso efectivo bajo herdr. |
| H-C3 | NO DEMOSTRADO. Almacenamiento efímero y fuente de autenticación son problemas distintos. |
| H-C4 | INCOMPLETO COMO ORÁCULO. El hash/stat de `config.toml` no detecta por sí solo acceso o escritura a otros estados personales. |
| H-C5 | BIEN CONSERVADO COMO LÍMITE DEL EVENTUAL PILOTO; no fue ejecutado ni aprobado por esta revisión. |

Fuentes oficiales vigentes contrastadas: [configuración avanzada de
Codex](https://developers.openai.com/codex/config-advanced), [referencia de
configuración](https://developers.openai.com/codex/config-reference) y
[autenticación](https://developers.openai.com/codex/auth).

### R-OTEL-C12-01 — OBLIGATORIO — baseline ejecutable desactualizado

**Referencia precisa:** contrato L32–41 y L92–95.

**Evidencia:** el contrato fija Codex 0.157.1. La lectura actual
`codex --version` informa `codex-cli 0.158.0`; `herdr --version` continúa en
0.8.0. La ayuda nueva conserva los flags relevantes, pero no demuestra que trust,
estado y autenticación se comporten igual.

**Problema:** F12-01/F12-03/F12-04 mezclan evidencia histórica de 0.157.1 con el
ejecutable que usaría una comprobación futura.

**Consecuencia:** el contrato podría aprobar o bloquear una ruta apoyándose en
un comportamiento de otra versión.

**Corrección mínima:** conservar 0.157.1 como antecedente y agregar un baseline
de solo lectura para 0.158.0: ruta/versión efectivas, flags pertinentes y
referencias oficiales aplicables. Exigir repetir ese baseline si vuelve a cambiar
la versión antes de cualquier comprobación viva.

### R-OTEL-C12-02 — OBLIGATORIO — fuente y almacenamiento de autenticación no están separados

**Referencia precisa:** contrato L34–35, H-C3 L65–67 y §5 L79–88.

**Evidencia:** la documentación oficial vigente permite guardar credenciales en
archivo bajo `CODEX_HOME`, keyring del sistema, modo automático o memoria
efímera. `ephemeral` evita persistir una credencial ya obtenida; no la crea ni
autoriza reutilizar una credencial global.

**Problema:** el contrato exige llegar autenticado, pero no enumera una fuente
permitida ni define qué alternativa requiere decisión del usuario. La frase
“autenticación segura” puede interpretarse como almacenamiento efímero, reutilizar
el keyring global o iniciar un login, con efectos diferentes.

**Consecuencia:** una comprobación podría pedir un secreto, reutilizar estado
global o quedar bloqueada después de abrir la pane.

**Corrección mínima:** separar en una tabla cerrada fuente de autenticación,
almacenamiento, autorización necesaria, evidencia permitida y condición STOP.
Si ninguna fuente cumple sin leer/copiar secretos ni iniciar login no autorizado,
declarar H-C3 bloqueado antes de lanzar herdr.

### R-OTEL-C12-03 — OBLIGATORIO — propagación e inmutabilidad admiten un falso PASS

**Referencia precisa:** H-C1/H-C2/H-C4 L59–69 y comprobación mínima L79–83.

**Evidencia:** la comprobación propuesta observa prompt normal, ausencia de
pedido de credenciales y hash/stat de `config.toml`. La documentación oficial
ubica además autenticación por archivo, historial, logs y cachés bajo
`CODEX_HOME`; herdr no expone una inyección de entorno documentada.

**Problema:** llegar al prompt sin cambiar `config.toml` no prueba que el proceso
hijo recibió la raíz temporal ni que evitó otros estados de `~/.codex` o el
almacén del sistema.

**Consecuencia:** H-C1, H-C2 o H-C4 podrían marcarse PASS aunque Codex haya usado
la raíz personal sin tocar ese único archivo.

**Corrección mínima:** exigir evidencia filtrada del ejecutable hijo y de su
`CODEX_HOME`, creación esperada de estado solo en la raíz temporal y comparación
pre/post de metadatos de los estados personales pertinentes, sin abrir ni hashear
contenido de credenciales. Definir la reversión y STOP para cualquier acceso o
escritura fuera de la raíz temporal.

### Ajustes de validación y evidencia faltante

No hacen falta pruebas de producto ni un piloto para corregir el documento. La
validación del contrato corregido debe comprobar que cada H-C tenga observación,
oráculo de PASS/STOP y orden previo a abrir herdr. La comprobación viva seguirá
requiriendo otra autorización.

Falta evidencia esencial para declarar viable la ruta: proceso Codex 0.158.0
bajo herdr con raíz temporal efectiva, fuente de autenticación autorizada y
ausencia verificable de uso del estado personal. Esa falta no invalida los
cierres previos; bloquea únicamente el próximo ensayo y Paso 3.

### Siguiente acción única

Corregir `OTEL_PILOT_CONTRACT_v1.2.md` con `03_PLANIFICAR.md`, exclusivamente
para R-OTEL-C12-01, R-OTEL-C12-02 y R-OTEL-C12-03. No iniciar otra revisión,
sesión, piloto, login, spec, slices o implementación.

## Ronda dirigida — contrato OTel v1.2-r1 / seguimiento — 2026-09-28

**VEREDICTO: REQUIERE_AJUSTES.**

### Nivel y alcance efectivamente revisado

- **Nivel:** N2, seguimiento limitado a R-OTEL-C12-01/02/03 y efectos directos.
- **Objeto:** [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md),
  revisión v1.2-r1, SHA-256
  `5647887786d52a22ef8056c25e9109b5ebcebfb92ba9865369424f5889d98a5d`.
- **Preservado:** P1–P4, R-OTEL-01–03, R-OTEL-P4-01/02 y cierres
  S01–S03/H01/H02/A01–A03.
- **No ejecutado:** correcciones, D12-AUTH, procesos, login, sesiones, piloto,
  lectura de credenciales/configuración o pruebas de producto.

### Resultado de los hallazgos anteriores

| ID | Estado | Evidencia y efecto directo |
|---|---|---|
| R-OTEL-C12-01 | CERRADO | §2 separa 0.157.1 histórico de PATH/resolución/0.158.0 actuales; B0 repite el baseline y produce STOP ante cualquier deriva antes de herdr. No reutiliza evidencia de una versión para aprobar otra. |
| R-OTEL-C12-02 | ABIERTO | §4 separa fuente y almacenamiento, pero A0 permite elegir “ninguna” y avanzar si Codex “llega listo”. H-C3/B1/B3 no exigen un indicador no secreto de autenticación efectiva. |
| R-OTEL-C12-03 | ABIERTO | H-C1/H-C2 agregan artefacto temporal y H-C4 agrega metadatos; todavía no se define cómo atribuir al proceso hijo el uso de `CODEX_HOME` ni cómo detectar cambios dentro de árboles existentes de sesiones/logs/cachés. |

### R-OTEL-C12-02 — OBLIGATORIO PENDIENTE — A0 puede producir un falso PASS de autenticación

**Referencia precisa:** contrato v1.2-r1 L79–96, H-C3 L111–114, B1 L143–152
y B3 L165–176.

**Evidencia:** A0 declara fuente “Ninguna” y puede considerarse válida si Codex
llega listo. D12-AUTH permite elegir A0 y B1 habilita B2 con una opción
“verificable”. H-C3 solo exige coincidencia con la opción elegida, almacenamiento
esperado y ausencia de secretos; no exige una señal sanitizada de autenticación
válida.

**Problema:** interfaz lista y autenticación efectiva no son equivalentes. Con A0,
el contrato puede satisfacer sus observaciones sin haber demostrado una fuente
de autenticación.

**Consecuencia:** B3 podría marcar H-C3 PASS y habilitar la solicitud de piloto,
para fallar recién al enviar una tarea o usar sin identificar una fuente global.

**Corrección mínima:** convertir A0 en control negativo que siempre deja H-C3
BLOCKED. Para A1–A3, exigir antes del PASS una señal no secreta y definida de
autenticación efectiva y método esperado, sin identidad, token o contenido; si no
puede obtenerse dentro del permiso otorgado, STOP antes de solicitar el piloto.

### R-OTEL-C12-03 — OBLIGATORIO PENDIENTE — el oráculo no cubre hijo y árboles mutables

**Referencia precisa:** H-C2 L106–110, H-C4 L115–127, B2–B4 L154–187 y caso
de validación L201–203.

**Evidencia:** H-C2 observa la variable en la pane y un artefacto temporal, pero
no define la evidencia que vincula ese artefacto con el proceso hijo exacto. H-C4
habla de “rutas fijas” y metadatos de sesiones/logs/cachés; un archivo ya
existente puede cambiar dentro de esos árboles sin alterar de manera suficiente
el metadato del directorio padre.

**Problema:** la comprobación no demuestra de forma inequívoca que el hijo heredó
la raíz ni detecta todas las escrituras pertinentes dentro de árboles existentes.

**Consecuencia:** H-C1/H-C2/H-C4 podrían marcarse PASS aunque herdr quite o
cambie `CODEX_HOME`, o Codex modifique un log/caché/sesión personal existente.

**Corrección mínima:** definir una evidencia no secreta que vincule PID/ejecutable
del hijo con un artefacto creado por ese proceso bajo la raíz temporal, sin volcar
el resto del entorno. Para estado personal, usar un inventario recursivo o un
oráculo equivalente que compare por entrada ruta protegida en forma digerida,
inode, tamaño y tiempos, sin conservar nombres, contenido o hashes de
credenciales/sesiones. Ausencia de esa evidencia deja el gate BLOCKED.

### Validación y evidencia faltante

R-OTEL-C12-01 no requiere más cambios. Las pruebas documentales de deriva,
`ephemeral` sin fuente, login inesperado y prompt sin artefacto siguen siendo
proporcionales. Deben agregarse dos casos dirigidos: A0 nunca autentica por sí
solo, y modificación de un archivo existente dentro de un árbol personal debe
fallar aunque el directorio padre parezca estable.

No falta evidencia para este veredicto. Sí falta evidencia viva para declarar
viabilidad, pero continúa fuera del alcance y no justifica abrir procesos ahora.

### Siguiente acción única

Corregir el mismo contrato con `03_PLANIFICAR.md`, exclusivamente para los
pendientes R-OTEL-C12-02 y R-OTEL-C12-03. No reabrir R-OTEL-C12-01, resolver
D12-AUTH, iniciar otra revisión, abrir procesos ni ejecutar login o piloto.

## Ronda dirigida — contrato OTel v1.2-r2 / cierre C12 — 2026-09-28

**VEREDICTO: APROBADO. Sin observaciones accionables.**

### Nivel y alcance efectivamente revisado

- **Nivel:** N2, seguimiento limitado a R-OTEL-C12-02/03 y efectos directos.
- **Objeto:** [OTEL_PILOT_CONTRACT_v1.2.md](OTEL_PILOT_CONTRACT_v1.2.md),
  revisión v1.2-r2, SHA-256
  `943444f2a1b3c1e12ec0df06562333cb3a02dd18df089067d4ab8c0a8f7f946b`.
- **Preservado:** R-OTEL-C12-01, P1–P4, R-OTEL-01–03,
  R-OTEL-P4-01/02 y cierres S01–S03/H01/H02/A01–A03.
- **No ejecutado:** correcciones, D12-AUTH, procesos, login, sesiones, piloto,
  lectura de credenciales/configuración o pruebas de producto.

### Resultado de los hallazgos anteriores

| ID | Estado | Evidencia y efecto directo |
|---|---|---|
| R-OTEL-C12-02 | CERRADO | §4 convierte A0 en control negativo no elegible para PASS. A1–A3 requieren `AUTH_OK` efectivo, sanitizado, con método esperado y referencia al mismo hijo; interfaz lista, presencia de secreto, código de salida o ausencia de error no sustituyen la señal. Si el verificador no existe o no está autorizado, H-C3 queda BLOCKED. |
| R-OTEL-C12-03 | CERRADO | H-C2 exige la cadena `herdr → PID hijo → ejecutable/versión → artefacto temporal` sin volcar entorno. H-C4 compara recursivamente cada entrada pertinente mediante identificadores HMAC efímeros y metadatos, sin abrir contenido ni seguir symlinks. B2 bloquea antes de la pane si el host no puede producir esa evidencia. |

### Efectos directos comprobados

- B1 ya no habilita B2 con A0 ni con una credencial meramente presente: requiere
  A1–A3, almacenamiento autorizado y una clase exacta de verificador.
- B2 comprueba que la cadena del hijo y el inventario sanitizado puedan producirse
  sin ampliar permisos o dependencias antes de abrir el proceso.
- B3 exige que propagación, `AUTH_OK` e inventario correspondan al mismo recorrido;
  un artefacto sin vínculo al hijo queda BLOCKED.
- B4 compara entrada por entrada, destruye la clave HMAC y detiene cualquier
  reparación global hasta contar con autorización específica.
- §7 cubre los dos negativos exigidos por el review anterior: A0 nunca autentica
  y un cambio interno falla aunque el directorio padre parezca estable. También
  cubre señal discordante, artefacto sin vínculo, symlink y recorrido incompleto.

### Validación y evidencia faltante

La validación documental es suficiente y proporcional; no se agregan pruebas de
producto, sesiones o pilotos a esta ronda.

La aprobación confirma que el contrato evita falsos PASS. No demuestra que exista
un verificador `AUTH_OK` utilizable para la opción que elija el usuario, que el
host pueda producir la cadena al hijo o que el inventario funcione en vivo. Esas
son dependencias operativas posteriores: D12-AUTH debe elegir A1, A2, A3 o
mantener el bloqueo, y cualquier comprobación viva necesita autorización propia.

### Siguiente acción única

Resolver D12-AUTH sin abrir procesos: elegir A1, A2, A3 o mantener el bloqueo y
definir para la opción elegida la clase admisible de `AUTH_OK`, almacenamiento,
efectos externos y STOP. No ejecutar todavía login, preflight, piloto o Paso 3.
