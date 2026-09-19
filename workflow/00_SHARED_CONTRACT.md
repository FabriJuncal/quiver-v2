# Contrato compartido de AI Software Factory

## Fuente de verdad

El repositorio del proyecto es la fuente de verdad.

El chat no es memoria persistente.

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
