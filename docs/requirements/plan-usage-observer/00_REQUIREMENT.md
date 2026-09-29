# Medición observable por plan

- **Ticket:** plan-usage-observer
- **Date:** 2026-09-24
- **Source:** encargo del usuario «QUIVER V2 — AUDITORÍA, PLAN, HANDOFF Y CONTINUIDAD GUIADA».
- **Estado del documento:** elaborado; propuesta funcional, no autorización de implementación.

## Problema y valor

Quiver necesita saber cuánto uso observable corresponde a ejecutar un plan hasta
su aceptación. Sin esa base, una predicción de tokens, USD o duración no tendría
una referencia confiable para evaluarse. La primera entrega propone registrar y
explicar consumo, faltantes y procedencia; no promete ahorro ni precisión predictiva.

## Alcance de esta sesión

Auditar la copia local, preparar criterios, decisión propuesta, plan por slices,
self review y handoff. Se permite documentación y comprobaciones locales revisadas;
no implementación. Las propuestas se preparan juntas por petición expresa, aunque
criterios, alternativa y plan todavía necesitan aprobación antes de ejecución.

## Primera entrega propuesta

Observador local opt-in, sin cambiar el launcher ni la sesión habitual: vincular
plan/revisión/intento a una fuente explícita, normalizar uso, persistirlo con
trazabilidad, informar tokens, tiempos observables y USD cuando exista base válida.
Separar cierre técnico, calidad de datos y aceptación del trabajo.

## Exclusiones

No predictor, router automático, presupuesto restrictivo, panel, servidor, gateway,
instalaciones, llamadas pagas de prueba, agentes nuevos, cambios globales ni publicación.
No leer historial personal indiscriminadamente ni credenciales. No reabrir benchmarks,
no acceder al repositorio piloto ni alterar los 72 untracked preexistentes.
La futura implementación y el acceso a una muestra real necesitan autorización propia.

## Fuentes canónicas

[STATE](STATE.md) controla progreso y permisos; [AUDIT](AUDIT.md) contiene evidencia;
[criterios](01_ACCEPTANCE_CRITERIA.md), [decisión propuesta](02_DECISION.md),
[plan v1](03_PLAN.md), [self review](04_PLAN_REVIEW.md) y [handoff](HANDOFF.md).
No existe un segundo plan en PLAN.md ni otro estado operativo en el wireframe.
