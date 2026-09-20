# AGENTS.md

Este proyecto utiliza AI Software Factory.

Factory version: 2.2.2

Las instrucciones específicas de este repositorio tienen prioridad sobre recomendaciones genéricas de Factory.

## Inicio

Antes de cambios significativos:

1. leer `PROJECT_STATE.md`;
2. identificar requirement activo;
3. leer su `STATE.md`;
4. cargar solo contexto necesario;
5. usar skills específicas si aplican.

Consultar `workflow/00_SHARED_CONTRACT.md` de la instalación canónica indicada en AGENTS
global. Si esa ruta falta, informar la limitación y cómo restaurarla; no buscar otra copia.

## Guided Mode

Avanzar hasta el próximo Decision Boundary.

No preguntar genéricamente "¿Cómo continuamos?" si existe una próxima acción derivable.

Si no necesita al usuario:

```text
ACCIÓN DEL USUARIO: ninguna
```

y ejecutar la próxima acción en el mismo turno. Es continuidad, nunca frase de cierre.

Aplicar **Finalization Gate** y **State Consistency Invariants** del contrato canónico:
trabajo activo autorizado + usuario false + sin impedimento real => PROHIBIDO FINALIZAR.
Registrar runtime limitation explícita cuando corresponda, con pendiente y reanudación exacta.

Si necesita decisión:

```text
ACCIÓN DEL USUARIO: requerida
```

y explicar qué ocurre, por qué requiere al usuario, acción/comando exactos, opción que debe seleccionar y respuesta para retomar. Presentar opciones + recomendación solo cuando existan alternativas materiales.

La ausencia de Model Gate no elimina otros boundaries. Verificar criterios, aprobación humana del plan y autorización de ejecución por separado; no repetir aprobaciones explícitas vigentes ni inferirlas de un `continuar` ajeno a ese gate.

## Estado persistente

Jerarquía de evidencia: código/evidencia real > requirement STATE > PROJECT_STATE >
artifacts aprobados > docs de proyecto > Conversation Recap > historial del chat.
Aplicar `docs/concepts/SOURCE_OF_TRUTH.md`: si recap contradice STATE, ignorar recap,
registrar inconsistencia y continuar desde STATE verificado. No editar recap ni usarlo para cerrar.

Mantener:

- `PROJECT_STATE.md`;
- `docs/requirements/<ticket>/STATE.md`.

Toda próxima acción debe ser concreta. Para N0/N1 aplicar la ruta compacta de `docs/concepts/RISK_AND_WORKFLOW.md` de la Factory: un STATE puede reunir plan breve, criterios y evidencia; no generar todo el paquete por defecto.

## Routing

- bug/regresión → `systematic-debugging` si está disponible;
- fuentes/versiones externas → `source-driven-development` si está disponible;
- APIs/contratos → `api-and-interface-design` si está disponible;
- arquitectura material → skill de arquitectura si está disponible;
- DB/schema → `database-change-safety` si existe;
- legacy → `legacy-migration` si existe;
- UI → herramientas UI si existen.

No activar todo por defecto.

## AI Model Routing

La Factory utiliza perfiles:

- ECONOMICAL
- BALANCED
- ADVANCED

No elegir un único modelo para todo el proyecto.

- Project Discovery define `AI Policy`.
- Cada requirement define `AI Strategy`.
- Cada slice define `AI Execution Profile`.

Resolver modelos concretos desde el catálogo actual de Factory.

No afirmar que se cambió de modelo si el runtime no lo permite.

Escalar o hacer downgrade solo cuando la diferencia sea material.

## Testing

Testing proporcional al perfil aprobado.

## Evidence Before Completion

No afirmar éxito sin evidencia reciente.

## Proyectos existentes

Integrar antes que migrar.

No reescribir stack o arquitectura sin necesidad y decisión aprobada.

## Git

Cambios enfocados y revisables.

No worktrees por defecto.

## Simplicidad

No introducir herramientas o infraestructura sin justificar valor concreto.


---

## Guided AI Model Routing

Antes de una fase/slice, aplicar la estrategia persistida y la skill `model-router` cuando corresponda.

No asumir el modelo activo.

### Default de Factory

BALANCED:

**GPT-5.6 Terra (`gpt-5.6-terra`) / Medium**

### Escalamiento

Para tareas críticas, la Factory puede generar un AI Model Gate hacia:

**GPT-5.6 Sol (`gpt-5.6-sol`) / High**

Exceptional Override:

**GPT-6 Astra (`gpt-6-astra`) / High o XHigh**

solo cuando esté disponible y se justifique.

### Guided Model Gate

Si se necesita cambiar:

1. indicar `/status` si existe duda;
2. indicar `/model`;
3. escribir nombre completo e ID exacto;
4. indicar reasoning;
5. indicar fallback;
6. pedir que el usuario escriba `continuar`.

No dejar al usuario decidir cómo proseguir.

### Switch Threshold

No cambiar de modelo por micro-optimizaciones.

Gate solo con Switch Benefit HIGH y configuración suficiente todavía no confirmada para esta fase/sesión. No repetirlo por cada slice. Persistir recomendaciones, nunca el modelo activo de sesión.

Downgrade únicamente en phase boundary si queda una fase sustancial y mecánica.

### Review

- N0: self verification
- N1: self review
- N2: `/review` cuando sea material
- N3: review dedicado requerido cuando sea técnicamente posible; si no lo es, documentar causa y solicitar aprobación explícita de una alternativa antes del cierre.

No confundir cambiar el modelo del chat con tener un review dedicado.

Resolver alcance/base real del review y verificar sus resultados. Aplicar el límite de correcciones y salida de `workflow/08_IMPLEMENTATION_REVIEW.md` de la Factory; no entrar en ciclos ilimitados.
