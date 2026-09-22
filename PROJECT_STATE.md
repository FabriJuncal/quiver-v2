# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.1 — Supervised Delegation Preview
- **Status:** awaiting-approval
- **Current phase:** candidata offline validada; piloto NOT RUN por controles pendientes
- **Active requirement:** docs/requirements/release-2-3-0-rc-1/STATE.md
- **Last completed requirement:** docs/requirements/sandbox-isolation-probe/STATE.md
- **Current slice:** none
- **Completed:** S01–S04 offline y 111 tests previos preservados. Prueba nueva codex sandbox 0.155.1: 22/22 casos, configuración temporal, sin agentes/modelos adicionales. Protección de archivos ficticios observada; evidencia en docs/requirements/sandbox-isolation-probe/REPORT.md. Config habitual preservada, sin release nueva.
- **Pending:** decisión de alcance preview offline o integración runtime antes de publicar funcionalidad viva.
- **Next action:** revisar/aprobar alcance final según STATE del requirement; mantener piloto deshabilitado por RC-F02.
- **Why this is next:** 117 tests OK desde ZIP y upgrade real 2.2.2 probado; configuración efectiva del hijo no verificable con esta interfaz.
- **User action required:** true
- **Decision required:** preview offline explícita o continuación de integración runtime; no autorización de publicación vigente.
- **Expected output:** aprobación concreta de siguiente alcance; no cierre falso de capacidad multiagente.
- **After this:** ejecutar solo opción aprobada; push/tag/publicación requieren autorización nueva.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability
- **Runtime limitation detail:** piloto: esta interfaz no permite seleccionar rol/permisos ni verificar ausencia de recursión/herramientas mutantes del ayudante. Preparación offline continúa.
- **Resume instruction:** leer docs/requirements/release-2-3-0-rc-1/STATE.md, EVIDENCE.md y review. Candidata offline lista para revisión en .release-candidates/2.3.0-rc.1/; piloto NOT RUN, cero intentos. No activar por los PASS estáticos ni publicar sin aprobación nueva.

## Publicación v2.2.2

- **Commit/tag:** `20ea27ac33f92928f2e8ebe7a0c0cf4f14bd8a67` / `v2.2.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.2
- **Assets:** `ai-software-factory-v2.2.2.zip` y `.sha256`; ZIP digest `30b2ff08d6e6c5f5b47bbe94b493309f9367a36b38284ae622505e0dc2cd098a`.
- **CI:** Validate y Factory v2.2.2 Runtime Guardrails completados exitosamente el 2026-09-20.
