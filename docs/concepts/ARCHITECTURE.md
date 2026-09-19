# Arquitectura de AI Software Factory

AI Software Factory se divide en tres niveles.

```text
NIVEL 1 — Usuario
~/.codex/AGENTS.md
~/.agents/skills/

NIVEL 2 — Factory
workflow/
templates/
skills/
docs/

NIVEL 3 — Proyecto
AGENTS.md
PROJECT_PROFILE.md
PROJECT_STATE.md
CAPABILITY_MAP.md
docs/requirements/
```

## Responsabilidades

### Configuración global

Contiene reglas mínimas y routing.

No debe contener toda la documentación de Factory.

### Factory

Es reutilizable.

No se copia completa dentro de cada repo.

### Proyecto

Contiene exclusivamente:

- estado;
- negocio;
- arquitectura real;
- requirements;
- decisiones;
- skills específicas.

## Fuente de verdad

Orden recomendado:

1. código/datos reales;
2. requirements aprobados;
3. ADRs;
4. `PROJECT_PROFILE.md`;
5. `PROJECT_STATE.md`;
6. `CAPABILITY_MAP.md`;
7. documentación;
8. code graph derivado;
9. memoria del modelo;
10. chat.

El code graph ayuda a descubrir.

No reemplaza el código.

Obsidian ayuda a navegar.

No reemplaza Git.


## AI Model Routing

La selección de IA también sigue la jerarquía de contexto:

```text
PROJECT_PROFILE → AI Policy
Requirement STATE → AI Strategy
Slice EXECUTION_BRIEF → AI Execution Profile
config/MODEL_CATALOG.md → modelo concreto actual
```

La Factory persiste perfiles para evitar acoplar documentación histórica a modelos específicos.


---

## Guided Model Routing

La capa de routing no es un orquestador de modelos.

```text
Project AI Policy
      ↓
Requirement AI Strategy
      ↓
Slice AI Execution Profile
      ↓
Switch Benefit
      ↓
AI Model Gate si realmente corresponde
```

La selección activa del runtime sigue perteneciendo a Codex.

Factory persiste recomendaciones, no el modelo activo.
