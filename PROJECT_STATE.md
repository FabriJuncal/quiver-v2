# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.1 — Supervised Delegation Preview
- **Status:** awaiting-approval
- **Current phase:** routing mejorado en fuente local; decisión de candidata offline pendiente
- **Active requirement:** docs/requirements/release-2-3-0-rc-1/STATE.md
- **Last completed requirement:** docs/requirements/model-routing-precision/STATE.md
- **Current slice:** none
- **Completed:** S01–S04 offline y 111 tests previos preservados. Prueba nueva codex sandbox 0.155.1: 22/22 casos, configuración temporal, sin agentes/modelos adicionales. Protección de archivos ficticios observada; evidencia en docs/requirements/sandbox-isolation-probe/REPORT.md. Config habitual preservada, sin release nueva.
- **Pending:** decisión de alcance preview offline o integración runtime antes de publicar funcionalidad viva.
- **Next action:** revisar/aprobar alcance de release según su STATE; mantener piloto deshabilitado por RC-F02.
- **Why this is next:** routing concluido con 47 tests dirigidos OK; la decisión de release no fue autorizada por este trabajo.
- **User action required:** true
- **Decision required:** preview offline explícita o continuación de integración runtime; no autorización de publicación vigente.
- **Expected output:** decisión concreta de alcance; no cierre falso de capacidad multiagente.
- **After this:** ejecutar solo opción aprobada; reconciliar fuente/candidata antes de una publicación autorizada.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability
- **Runtime limitation detail:** solo piloto: controles efectivos del hijo no verificables según STATE de release. Routing no tiene pendientes ni limitación runtime.
- **Resume instruction:** leer docs/requirements/release-2-3-0-rc-1/STATE.md, EVIDENCE.md y review. Routing completado en docs/requirements/model-routing-precision/; candidata ZIP previa e instalación canónica no incluyen automáticamente ese diff. Piloto NOT RUN; no publicar sin autorización nueva.

## Mejora local de routing — 2026-09-23

Verificabilidad, ruta rápida, diagnóstico antes de escalar y obligación auditable en
planning/ejecución/review. 25 tests runtime + 22 lifecycle OK; check-release OK.
Rama: improve/model-routing-precision. Evidencia: docs/requirements/model-routing-precision/EVIDENCE.md.
Sin cambios globales, modelos nuevos ni mediciones de ahorro. La evidencia previa de
la candidata se conserva para su ZIP original; no certifica una candidata con este diff.

## Publicación v2.2.2

- **Commit/tag:** `20ea27ac33f92928f2e8ebe7a0c0cf4f14bd8a67` / `v2.2.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.2
- **Assets:** `ai-software-factory-v2.2.2.zip` y `.sha256`; ZIP digest `30b2ff08d6e6c5f5b47bbe94b493309f9367a36b38284ae622505e0dc2cd098a`.
- **CI:** Validate y Factory v2.2.2 Runtime Guardrails completados exitosamente el 2026-09-20.
