---
name: project-discovery
description: Use when adopting an existing repository into AI Software Factory or defining a new Factory project before implementation. Produces a minimal PROJECT_PROFILE, CAPABILITY_MAP and PROJECT_STATE without changing application code.
---

# Project Discovery

## Goal

Understand the project before changing it.

## Existing project

Inspect proportionally:

- purpose/business;
- stack and versions;
- architecture;
- DB;
- auth;
- APIs;
- testing;
- deployment;
- integrations;
- Git conventions;
- existing docs.

Do not modify application code.

Classify capabilities:

`KEEP | ADD | WRAP | IMPROVE | REPLACE_LATER | IGNORE`

Prefer integration over migration.

## New project

Clarify:

- problem;
- users;
- market;
- product type;
- constraints;
- required capabilities.

Avoid choosing infrastructure before requirements.

## AI Policy

Al finalizar Discovery, proponer una política general simple:

- default profile: BALANCED salvo evidencia contraria;
- prioridades: quality / speed / cost;
- reasoning por defecto;
- reglas de escalamiento;
- independencia de review para N2/N3.

Persistirla en `PROJECT_PROFILE.md`.

No elegir todavía un único modelo para todo el proyecto.

## Outputs

Update/create:

- `PROJECT_PROFILE.md`
- `CAPABILITY_MAP.md`
- `PROJECT_STATE.md`

Set an explicit next action.


## Initial AI Policy

Al completar Discovery, establecer:

- Default profile: BALANCED
- Preferred model: GPT-5.6 Terra (`gpt-5.6-terra`)
- Default reasoning: Medium
- Switch threshold: HIGH
- Downgrade: phase-boundary-only
- N3 review: dedicated required; ante imposibilidad técnica documentada, aprobar alternativa antes del cierre

No pedir al usuario elegir modelos durante Discovery salvo restricción explícita.

En adopción, revisar el snippet de AGENTS si existe: integrar reglas compatibles dentro de la autorización de adopción, registrar «ya cubierto» si no agrega nada o presentar un conflicto concreto. No dejar una fusión vaga pendiente. Finalizar con estado completo y continuar el siguiente paso autorizado; si falta una decisión, dar la respuesta exacta para reanudar.
