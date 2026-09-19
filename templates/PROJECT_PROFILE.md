# PROJECT_PROFILE

## Identidad

- Name:
- Mode: new | existing
- Type:
- Business model:
- Primary users:
- Primary market:

## Stack actual

### Frontend
-

### Backend
-

### Mobile/Desktop
-

### Database
-

### Infrastructure / Deployment
-

### Authentication
-

### Payments / Billing
-

## Architecture

-

## Constraints

-

## Existing conventions

-

## AI / Factory

- Factory version: 2.2.1 — Guided Model Routing
- Knowledge tooling: none | graphify | codebase-memory
- Notes:

## AI Policy

> Política general. No fija un único modelo para todo el proyecto y no registra el modelo activo de una sesión.

- **Default profile:** BALANCED
- **Default preferred model:** GPT-5.6 Terra (`gpt-5.6-terra`)
- **Default reasoning:** Medium
- **Quality priority:** low | medium | high
- **Speed priority:** low | medium | high
- **Cost priority:** low | medium | high
- **Escalation enabled:** true
- **Switch threshold:** HIGH
- **Downgrade policy:** phase-boundary-only
- **N2 dedicated review:** optional | recommended
- **N3 dedicated review:** required; si es técnicamente imposible, documentar causa y obtener aprobación de una alternativa antes del cierre
- **Critical review preferred model:** GPT-5.6 Sol (`gpt-5.6-sol`)
- **Exceptional override:** GPT-6 Astra (`gpt-6-astra`) only when justified and available
- **Model catalog:** canonical Factory `config/MODEL_CATALOG.md`
- **Project overrides:** none

### Important

Do not persist:

```text
Current model: ...
```

The active model belongs to the Codex session, not project state.
