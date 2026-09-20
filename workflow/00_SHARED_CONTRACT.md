# Contrato compartido de AI Software Factory

## Fuente de verdad

El repositorio del proyecto es la fuente de verdad.

El chat no es memoria persistente.

Jerarquía canónica: [Source of Truth](../docs/concepts/SOURCE_OF_TRUTH.md).
STATE prevalece sobre Conversation Recap; el recap es contexto auxiliar y nunca prueba de cierre.

## Principios

- proporcionalidad al alcance/riesgo;
- contexto mínimo necesario;
- no inventar archivos/contratos;
- no agregar requirements silenciosamente;
- no reabrir decisiones aprobadas sin nueva evidencia;
- integrar antes que migrar;
- solución mínima suficiente;
- evidencia antes de afirmar éxito.

## Guided Mode

El agente guía hasta el próximo **Decision Boundary**.

Antes de detenerse:

1. identificar fase;
2. identificar progreso;
3. determinar próxima acción;
4. determinar si necesita al usuario;
5. continuar si no requiere decisión;
6. actualizar estado.

## Finalization Gate — canónico

Antes de emitir cualquier respuesta final, evaluar contra estado y evidencia:

```text
requirement activo
AND (slice activa OR próxima acción pendiente)
AND User action required = false
AND no blocker real
AND próxima acción dentro del alcance aprobado
AND runtime permite continuar
=> PROHIBIDO FINALIZAR: ejecutar Next action en el mismo turno.
```

Cerrar una slice no cierra el requirement: activar y ejecutar la siguiente autorizada.
También continuar acciones autorizadas de discovery o proyecto sin requirement creado.
No basta anunciar «continúo»: debe seguir una acción efectiva, herramientas o elaboración
del artefacto requerido, antes de evaluar otra vez este gate.

Solo finalizar por requirement completado (sin otro trabajo autorizado pendiente),
Decision Boundary real, `User action required = true`, blocker real, próxima acción
fuera de alcance, limitación real del runtime u operación irreversible que requiere aprobación.
No inventar límites, blockers ni decisiones para justificar un cierre.

`ACCIÓN DEL USUARIO: ninguna` es una instrucción de continuidad, no una frase de cierre.
Usarla en actualizaciones seguidas de ejecución; para un cierre por limitación usar el
estado explícito siguiente, nunca esa frase como última línea.

## State Consistency Invariants — canónicas

1. **INVARIANT 1:** si `requirement.status != completed` y existe trabajo activo/pendiente,
   `Next action` MUST existir y ser concreta.
2. **INVARIANT 2:** si `User action required = false`, el agente MUST ejecutar `Next action`,
   registrar un blocker real o registrar una runtime limitation. Nunca simplemente detenerse.
3. **INVARIANT 3:** si `slice.status = active`, el requirement NO puede declararse sin próximos
   pasos ni completado; reconciliar primero evidencia y estado.
4. **INVARIANT 4:** Conversation Recap nunca sobrescribe estado persistido. Leer STATE antes
   de reanudar; si contradice el recap, ignorar el recap, registrar la inconsistencia en STATE
   y continuar desde STATE contrastado con evidencia. No editar el recap del runtime.

Validar al cambiar fase, cerrar/activar slice y antes de responder. Si falta un campo derivable,
repararlo con evidencia y continuar; preguntar solo por información o autorización material faltante.

## Runtime limitation

Campo explícito separado de `Blocked by` (bloqueo funcional del producto):

`none | context-limit | tool-failure | permission | unavailable-model | unavailable-runtime-capability | other`

Ante una limitación real, persistir tipo, evidencia/causa, trabajo pendiente, `Next action`,
`Resume instruction` con comando/prompt exacto y si requiere intervención humana.
`User action required` refleja la intervención real, no se vuelve true automáticamente.
Si aún queda trabajo autorizado independiente ejecutable, continuarlo antes de finalizar.
Si no se puede escribir STATE, informar archivo/campos pendientes y prompt de recuperación;
no afirmar que se persistió. Una compacción prevista sin impedimento real no autoriza detenerse.

Cierre por limitación: `ESTADO: PAUSADO POR RUNTIME`, tipo y causa, pendiente y pasos exactos.
Si requiere usuario: `ACCIÓN DEL USUARIO: requerida` y acción concreta; si el runtime puede
reanudar solo: `REANUDACIÓN: automática` con el mecanismo real. No prometer automatismos inexistentes.
En la nueva sesión verificar si la limitación sigue vigente, limpiarla si se resolvió y aplicar este gate.

## Decision Boundaries

Continuar automáticamente para:

- leer;
- investigar;
- inspeccionar;
- preparar matrices;
- generar artefactos aprobados;
- actualizar `STATE`;
- ejecutar verificaciones aprobadas.
- realizar review automático permitido dentro del alcance aprobado.

Detenerse para:

- aprobar criterios;
- seleccionar alternativa;
- seleccionar testing cuando exista una decisión material no aprobada;
- aprobar plan;
- cambio de alcance;
- arquitectura difícil de revertir;
- costo material;
- migración destructiva;
- deploy;
- operación irreversible.
- AI Model Gate pendiente con beneficio HIGH;
- review dedicado que requiera intervención;
- blocker real que impida continuar trabajo autorizado.

Guided Mode no elimina approval gates.

`User action required` es true si existe **cualquier** boundary pendiente para la próxima acción. La ausencia de Model Gate no lo convierte en false. Antes de actuar, contrastar el indicador con las decisiones, bloqueos y autorizaciones persistidas. Las autorizaciones explícitas previas siguen vigentes dentro de su alcance; no pedirlas de nuevo.

Clasificar riesgo y elegir ruta compacta/full según [Riesgo y tamaño del workflow](../docs/concepts/RISK_AND_WORKFLOW.md). N0/N1 no requieren todos los artefactos del flujo completo.

## Comunicación

No preguntar:

```text
¿Cómo continuamos?
```

cuando el siguiente paso sea derivable.

Si no necesita usuario:

```text
ACCIÓN DEL USUARIO: ninguna
```

y continuar.

Si necesita usuario:

```text
ACCIÓN DEL USUARIO: requerida
```

presentar opciones reales, trade-offs, recomendación y respuesta corta.

Explicar qué está pasando, por qué se necesita al usuario, qué debe hacer, comando y opción exactos cuando correspondan, y qué debe escribir para reanudar. Si hay una sola acción válida, indicarla sin inventar alternativas. En un bloqueo, identificar el dato/acceso faltante y la acción concreta para resolverlo. No terminar con una recomendación vaga.

## Estado

Todo estado activo debe indicar:

- `Next action`;
- `Why this is next`;
- `User action required`;
- `Decision required`;
- `Expected output`;
- `After this`;
- `Blocked by`;
- `Resume instruction`.
- `Runtime limitation` (por defecto `none`; incluir detalle si no es none).

Persistir por separado aprobación del reviewer, aprobación humana del plan y autorización de ejecución, vinculadas a la versión/alcance correspondiente. Una aprobación no equivale automáticamente a las otras. Puede registrarse autorización de ejecución ya contenida en la petición original.

## Evidence Before Completion

No afirmar:

- terminado;
- corregido;
- funcionando;
- tests OK;
- build OK;

sin evidencia reciente.
## AI Model Routing

AI Software Factory utiliza perfiles abstractos de capacidad:

- `ECONOMICAL`
- `BALANCED`
- `ADVANCED`

Persistir perfiles como estrategia normativa en el STATE del requirement. Los nombres/IDs pueden guardarse como recomendaciones resueltas con fecha de catálogo; no son verdad sobre la sesión. Decisión y plan referencian la estrategia, y las slices registran solo excepciones relevantes.

`REQUESTED PROFILE` es intención de Factory. `EFFECTIVE SESSION CONFIG` es modelo/reasoning
efectivamente usados por Codex, **unknown por defecto**: ni archivos ni launcher prueban ejecución
real. No introspección del agente ni persistencia del modelo activo como verdad de proyecto.
Usar [Session Preflight](../docs/guides/SESSION_PREFLIGHT.md) solo cuando la próxima tarea dependa
materialmente de esa configuración; tareas normales continúan sin interrumpir. Recomendar
[launcher](../docs/guides/ASF_LAUNCHER.md) para inicio determinista de la configuración solicitada.

El mapeo a modelos actuales vive en:

`config/MODEL_CATALOG.md`

Reglas:

- Project Discovery define la política general del proyecto.
- El requirement define la AI Strategy.
- Cada slice define su AI Execution Profile.
- Se puede escalar o hacer downgrade según evidencia.
- No usar ADVANCED por defecto.
- No usar ECONOMICAL cuando el riesgo/ambigüedad material requiera más capacidad.
- No afirmar que se cambió de modelo si el runtime no lo permite.
- Optimizar costo total por tarea, incluyendo reintentos y retrabajo.



---

## Guided AI Model Routing

Cuando una fase o slice tenga perfil de IA recomendado:

1. usar `model-router`;
2. resolver nombre completo, ID y reasoning desde `config/MODEL_CATALOG.md`;
3. calcular `Switch Benefit`;
4. no asumir qué modelo está activo;
5. generar AI Model Gate solo si el beneficio es HIGH y la necesidad no está satisfecha en la sesión; riesgo material insuficientemente cubierto se clasifica HIGH.

### AI Model Gate

Debe incluir:

- próxima tarea;
- perfil;
- nombre completo;
- ID;
- reasoning;
- fallback;
- motivo;
- `/status` si el usuario no sabe qué está activo;
- `/model` si debe cambiar;
- qué seleccionar;
- qué escribir después (`continuar`).

Nunca terminar con una recomendación vaga de modelo.

### Switch Threshold

No interrumpir por optimizaciones pequeñas.

Un downgrade solo debe proponerse al comenzar una fase grande y mecánica.

Una slice nueva no implica una fase nueva. Conservar la configuración suficiente durante la fase; no repetir un gate ya confirmado sin cambio material, ni bajar para volver a subir en el trabajo inmediatamente posterior. La política canónica de confirmación y fallback está en `config/MODEL_CATALOG.md`.

### Review Gate

Para N3:

- `/review` es requerido cuando sea técnicamente posible; si no, documentar causa y obtener aprobación de una alternativa antes de cerrar;
- explicar exactamente qué opción elegir;
- pedir `continuar con review` al finalizar.

Para N2, usar `/review` cuando el riesgo/diff lo justifique.

El alcance y evidencia, la política de una corrección dirigida y la salida ante obligatorios pendientes se definen en `workflow/08_IMPLEMENTATION_REVIEW.md`. No reabrir indefinidamente reviews ni cerrar con hallazgos obligatorios abiertos.

### Full model names

Mensajes de Factory deben usar:

- GPT-5.6 Luna (`gpt-5.6-luna`)
- GPT-5.6 Terra (`gpt-5.6-terra`)
- GPT-5.6 Sol (`gpt-5.6-sol`)
- GPT-6 Astra (`gpt-6-astra`)

No usar `GPT-5.6` a secas para indicar una selección.
