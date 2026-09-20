# Source of Truth

El chat no es fuente de verdad persistente.

Una decisión que deba sobrevivir a una sesión se persiste.

## Jerarquía de evidencia y estado

1. Código / evidencia real.
2. Requirement `STATE.md`.
3. `PROJECT_STATE.md`.
4. Artifacts aprobados.
5. Docs del proyecto.
6. Conversation Recap.
7. Historial del chat.

Esta jerarquía determina hechos y progreso; no convierte código en autorización para cambiar
decisiones aprobadas. Ante una discrepancia con criterios/autorizaciones, reconciliar con evidencia
y conservar los approval gates vigentes. No escoger el estado que permita continuar más fácilmente.

Antes de reanudar leer STATE, después comparar recap. Si contradice STATE, ignorar el recap,
registrar la inconsistencia y continuar desde el estado persistido verificado. Nunca declarar un
requirement completo basándose solo en recap. No intentar editar el recap del runtime.
Si evidencia nueva contradice STATE, corregir STATE y sincronizar PROJECT_STATE antes de continuar.

## Qué persiste dónde

| Información | Ubicación |
|---|---|
| Reglas globales | `~/.codex/AGENTS.md` |
| Procedimientos reutilizables | `~/.agents/skills/` |
| Metodología | Factory |
| Perfil del proyecto | `PROJECT_PROFILE.md` |
| Estado actual | `PROJECT_STATE.md` |
| Capacidad | `CAPABILITY_MAP.md` |
| Decisiones arquitectónicas | `docs/decisions/` |
| Requirement | `docs/requirements/<ticket>/` |
| Estado del requirement | `STATE.md` |
| Evidencia final | `CLOSURE_BRIEF.md` / `06_CLOSURE.md` |
