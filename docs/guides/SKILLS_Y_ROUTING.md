# Skills y routing

## Core incluido

Factory instala solamente sus skills core.

No instala automáticamente skills externas.

## Routing recomendado

| Tarea | Skill |
|---|---|
| adoptar proyecto | `project-discovery` |
| mantener estado | `requirement-state` |
| buscar contexto | `context-scout` |
| analizar impacto | `impact-analysis` |
| definir tests | `test-strategy` |
| revisar plan | `plan-reviewer` |
| ejecutar slice | `slice-executor` |
| revisar implementación | `implementation-reviewer` |
| cerrar con evidencia | `closure-evidence` |

## Skills externas recomendables

Instalar solo si aportan valor.

### Bugs

`systematic-debugging`

### APIs/versiones actuales

`source-driven-development`

### Contratos

`api-and-interface-design`

### Decisiones arquitectónicas

`architecture-decision-framework`

### UI

Impeccable + browser testing.

### Seguridad

`security-best-practices` cuando corresponda.

### Contexto/costo

`token-optimization` cuando existe un problema real.

## No default

No poner por defecto:

- TDD rígido;
- performance audit;
- accessibility audit completo;
- parallel agents;
- worktrees;
- security audit;
- architecture review.

Son contextuales.

## Skill propia

Crear una skill local cuando capture conocimiento que el modelo no puede obtener de una guía genérica:

```text
.agents/skills/
├── project-business-rules/
├── project-api-conventions/
├── project-database-rules/
└── legacy-migration/
```
