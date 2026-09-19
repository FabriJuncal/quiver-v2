# Guía para comenzar

Esta guía está escrita para usar AI Software Factory sin tener que entender toda la arquitectura desde el primer día.

## 1. Elegí el escenario

### A. Proyecto nuevo

Usá este camino cuando todavía no existe un repositorio o querés crear un producto nuevo desde cero.

Decile a Codex:

```text
Inicializá AI Software Factory para un proyecto nuevo.
Preguntame solamente lo necesario para definir producto, usuarios, mercado, capacidades y restricciones.
No selecciones herramientas innecesarias.
```

Codex debería generar como mínimo:

```text
PROJECT_PROFILE.md
PROJECT_STATE.md
CAPABILITY_MAP.md
PRODUCT.md            # si existe producto/UX
DESIGN.md             # si existe UI y se define identidad visual
```

Después se decide si corresponde utilizar un starter. Para un SaaS web nuevo puede usarse un starter SaaS; para una API, app móvil o automatización, no hace falta.

### B. Proyecto existente

No copies un starter encima del proyecto.

Decile a Codex:

```text
Inicializá AI Software Factory en este proyecto existente.
No cambies arquitectura, stack ni código.
Primero analizá el proyecto y generá PROJECT_PROFILE.md, CAPABILITY_MAP.md y PROJECT_STATE.md.
Clasificá cada capacidad como KEEP, ADD, WRAP, IMPROVE, REPLACE_LATER o IGNORE.
```

La regla es:

> Integrar antes que migrar.

## 2. Cómo trabajar un ticket

Cuando aparezca un requerimiento nuevo:

```text
Creá un requirement para <TICKET> usando AI Software Factory.
```

Se crea:

```text
docs/requirements/<TICKET>/
├── STATE.md
├── 00_REQUIREMENT.md
├── 01_ACCEPTANCE_CRITERIA.md
├── 02_DECISION.md
├── 03_PLAN.md
├── 04_PLAN_REVIEW.md
├── slices/
├── 05_IMPLEMENTATION_REVIEW.md
└── 06_CLOSURE.md
```

No todos los niveles necesitan todos los archivos. Nivel 0/1 puede usar una ruta compacta.

## 3. Flujo normal

```text
Requirement
  ↓
Criterios de aceptación
  ↓
Opciones de desarrollo
  ↓
Elegir opción + testing
  ↓
Plan técnico
  ↓
Plan Review
  ↓
Slices
  ↓
Implementación
  ↓
Pruebas / Browser si corresponde
  ↓
Implementation Review
  ↓
Closure + evidencia
```

## 4. Testing

- `T1`: mínimo suficiente y dirigido.
- `T2`: reforzado con casos límite e integración relevante.
- `T3`: alta garantía para riesgo alto.

No usar TDD como obligación universal. Para bugs, sí es recomendable reproducir y, cuando sea viable, crear una prueba que falle antes del fix.

## 5. Skills automáticas recomendadas

Usar por contexto, no todas juntas:

- Bug/test fallido → `systematic-debugging`.
- Framework/SDK/API externa sensible a versión → `source-driven-development`.
- API/contrato → `api-and-interface-design`.
- Decisión arquitectónica real → `architecture-decision-framework`.
- UI → Impeccable si el proyecto lo usa.
- UI con comportamiento real → browser testing si aporta evidencia.
- Cambio de datos/schema → `database-change-safety`.
- Migración legacy → `legacy-migration`.

## 6. Antes de cerrar

Nunca declarar "terminado", "funciona", "tests OK" o "build OK" sin evidencia actual.

Actualizar siempre:

```text
CLOSURE_BRIEF
STATE.md
PROJECT_STATE.md     # si cambia estado general
```

## 7. Reanudar otro día

No pegues el chat anterior.

Decile a Codex:

```text
Continuá <TICKET>. Leé primero PROJECT_STATE.md y luego docs/requirements/<TICKET>/STATE.md. Cargá solo el contexto necesario para la próxima acción.
```

## 8. Qué no hacer

- No instalar todas las skills por defecto.
- No usar parallel agents para tareas dependientes.
- No crear worktree para cada ticket.
- No crear RAG/Vector DB sin necesidad real.
- No migrar un stack existente solo para ajustarlo a la Factory.
- No crear un CLI/orquestador propio todavía.
