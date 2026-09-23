# Requirement State

## Identificación

- **Ticket / slug:**
- **Title:**
- **Status:** draft | defining | approved | planning | ready-for-execution | in-progress | review | blocked | completed
- **Phase:**
- **Risk level:** N0 | N1 | N2 | N3
- **Last updated:**

## Decisiones

- **Acceptance criteria:** pending | approved
- **Selected option:**
- **Test profile:** T1 | T2 | T3 | not-selected
- **Plan version:**
- **Plan review:** pending | approved | approved-with-notes | requires-adjustments
- **Human plan approval:** pending | approved (incluir versión aprobada, fecha y referencia a la decisión del usuario)
- **Execution authorization:** pending | approved (alcance y versión autorizados; puede provenir de la petición original)
- **Workflow size:** compact | full (ver docs/concepts/RISK_AND_WORKFLOW.md en Factory)

## Ejecución

- **Current slice:**
- **Completed slices:**
- **Pending slices:**
- **Pending required findings:**
- **Implementation review:** pending | approved | approved-with-notes | requires-adjustments
- **Review scope/evidence:** base/HEAD o diff identificado, fecha, validaciones y resultado; no afirmar revisión sin evidencia
- **Directed correction rounds:** 0 (máximo 1 antes de escalar si quedan obligatorios)

## AI Strategy

> Estrategia normativa del requirement. Los IDs son una recomendación resuelta contra el catálogo indicado, nunca el modelo activo. Decisión y plan referencian esta sección; slices registran solo excepciones útiles.

### Planning

- **Profile:** ECONOMICAL | BALANCED | ADVANCED
- **Preferred model:**
- **Model ID:**
- **Reasoning:** low | medium | high | xhigh
- **Fallback:**

### Implementation default

- **Profile:** ECONOMICAL | BALANCED | ADVANCED
- **Preferred model:**
- **Model ID:**
- **Reasoning:** low | medium | high | xhigh
- **Fallback:**

### Review

- **Profile:** ECONOMICAL | BALANCED | ADVANCED
- **Preferred model:**
- **Model ID:**
- **Reasoning:** low | medium | high | xhigh
- **Dedicated review:** none | optional | recommended | required

### Switch policy

Aplicar `routing-v1` de config/MODEL_CATALOG.md de la Factory. Una decisión breve
por fase suficiente; heredar por referencia sin repetirla en cada slice. No prueba
configuración efectiva. N0/consultas siguen las excepciones compactas del catálogo.

- **Routing decision / reference:** fase, perfil/reasoning, motivo observable, verificación y límite, contexto suficiente/faltante; o referencia vigente que ya los contenga.
- **Selection basis:** policy | measured (measured requiere referencia comparable; no inventar ahorro).

- **Switch threshold:** HIGH
- **Current phase switch benefit:** LOW | MEDIUM | HIGH
- **Escalation triggers:**
- **Downgrade opportunities:**
- **Why these profiles:**
- **Estimated AI consumption:** low | medium | high | unknown
- **Catalog verified date:**

## Progreso

### Completed
-

### In progress
-

### Pending
-

## Próxima acción

- **Next action:**
- **Why this is next:**
- **User action required:** true | false (resolver todos los boundaries antes de completar)
- **Decision required:** none | decisión concreta pendiente
- **Expected output:**
- **After this:**
- **Blocked by:** none
- **Runtime limitation:** none
- **Runtime limitation detail:** none; si ocurre, causa/evidencia, pendiente y reanudación exacta.

## Decision Boundary

- **Decision needed:**
- **Available options:**
- **Recommended option:**
- **Simple response format:**

## Reanudación

- **Resume instruction:**

## Bloqueos

### Blocking
-

### Non-blocking
-

## Evidencia relevante

-

> Evitar `Next action: revisar qué hacer`.
> Validar Finalization Gate e invariants del contrato canónico: slice activa implica Next action.
