# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.1 — Supervised Delegation Preview
- **Status:** in-progress
- **Current phase:** preparando candidata local e integración inactiva
- **Active requirement:** docs/requirements/release-2-3-0-rc-1/STATE.md
- **Last completed requirement:** docs/requirements/sandbox-isolation-probe/STATE.md
- **Current slice:** none
- **Completed:** S01–S04 offline y 111 tests previos preservados. Prueba nueva codex sandbox 0.155.1: 22/22 casos, configuración temporal, sin agentes/modelos adicionales. Protección de archivos ficticios observada; evidencia en docs/requirements/sandbox-isolation-probe/REPORT.md. Config habitual preservada, sin release nueva.
- **Pending:** validar candidata, artefacto exportado y diff; piloto condicionado a controles.
- **Next action:** ejecutar regresiones offline y verificación del artefacto local.
- **Why this is next:** preparación autorizada; no habilitar piloto sin controles efectivos.
- **User action required:** false
- **Decision required:** none para el trabajo completado.
- **Expected output:** candidata con evidencia y límite de activación explícito.
- **After this:** entregar para revisión/aprobación final; no publicar.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability
- **Runtime limitation detail:** piloto: esta interfaz no permite seleccionar rol/permisos ni verificar ausencia de recursión/herramientas mutantes del ayudante. Preparación offline continúa.
- **Resume instruction:** leer docs/requirements/release-2-3-0-rc-1/STATE.md y PLAN.md. Un único piloto sintético condicional autorizado, todavía no lanzado; no push/tag/publicación ni cambios de configuración habitual.

## Publicación v2.2.2

- **Commit/tag:** `20ea27ac33f92928f2e8ebe7a0c0cf4f14bd8a67` / `v2.2.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.2
- **Assets:** `ai-software-factory-v2.2.2.zip` y `.sha256`; ZIP digest `30b2ff08d6e6c5f5b47bbe94b493309f9367a36b38284ae622505e0dc2cd098a`.
- **CI:** Validate y Factory v2.2.2 Runtime Guardrails completados exitosamente el 2026-09-20.
