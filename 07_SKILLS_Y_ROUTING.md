# Skills y routing

## Globales recomendadas

Instalar una sola vez en `~/.agents/skills/`:

```text
systematic-debugging
source-driven-development
api-and-interface-design
architecture-decision-framework
token-optimization
using-git-worktrees
security-best-practices
```

Solo las primeras tres deberían aparecer con frecuencia. Las demás son toolbox.

## No instalar por defecto

- test-driven-development.
- code-review-and-quality.
- performance-optimization.
- accessibility-audit.
- parallel-agents.
- documentation-and-adrs.
- ai-system-architecture.

No porque sean malas, sino porque son contextuales o duplican el core.

## Reglas absorbidas por la Factory

### Verification before completion

Siempre activa como regla, no como skill separada.

### Code review

Cubierto por Implementation Reviewer proporcional.

### Documentation/ADRs

Cubierto por `docs/architecture` y `docs/decisions`.

## Routing

```text
BUG / TEST FAILURE
    → systematic-debugging

FRAMEWORK / SDK / API EXTERNA VERSIONADA
    → source-driven-development

ENDPOINT / CONTRATO / INTERFAZ
    → api-and-interface-design

DECISIÓN ARQUITECTÓNICA REAL
    → architecture-decision-framework

UI
    → Impeccable si está instalado
    → browser testing si hace falta runtime real

SCHEMA / MIGRACIÓN / DATOS
    → database-change-safety

LEGACY / PARIDAD / MIGRACIÓN FUNCIONAL
    → legacy-migration

TAREA NORMAL
    → workflow estándar
```

## Regla para crear una skill nueva

Crear skill solo si:

1. el procedimiento se repite;
2. no cabe mejor en AGENTS.md;
3. no es simple documentación;
4. reduce decisiones o errores;
5. puede evaluarse con ejemplos.
