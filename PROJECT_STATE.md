# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** completed
- **Current phase:** v2.3.0-rc.2 publicada y verificada
- **Active requirement:** none
- **Last completed requirement:** docs/requirements/release-2-3-0-rc-2/STATE.md
- **Current slice:** none
- **Completed:** PR #2 integrado; tag `v2.3.0-rc.2` en `930f67b7...`; prerelease pública; CI Ubuntu/macOS PASS; ZIP remoto con 139 tests OK y SHA-256 verificado.
- **Pending:** none para rc.2; RC-F02 sigue bloqueando activación viva.
- **Next action:** recopilar feedback de la preview; abrir un requirement separado antes de cualquier activación de delegación viva.
- **Why this is next:** la publicación rc.2 está cerrada y verificada; la capacidad viva quedó explícitamente fuera de alcance.
- **User action required:** false
- **Decision required:** none
- **Expected output:** feedback trazable sin cambiar las garantías de la preview publicada.
- **After this:** si se decide resolver RC-F02, planificarlo como trabajo N3 con evidencia de controles efectivos.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability solo para piloto; ninguna para preview offline.
- **Runtime limitation detail:** RC-F02 impide activar/anunciar delegación operativa; no bloquea la prerelease offline.
- **Resume instruction:** leer docs/requirements/release-2-3-0-rc-2/{STATE,EVIDENCE,06_CLOSURE}.md. No quedan acciones de publicación pendientes.

## Publicación v2.3.0-rc.2

- **Commit/tag:** `930f67b7c05761edaa59b702320d31535a64c639` / `v2.3.0-rc.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.3.0-rc.2
- **Assets:** `ai-software-factory-v2.3.0-rc.2.zip` y `.sha256`; ZIP digest `cd30e9f4c84ebe34046358c40828091ecb88a06919416a4df29caa025d756f13`.
- **CI:** Validate y Factory Release Validation completados en Ubuntu/macOS para el merge commit.
- **Límite:** preview offline; delegación viva deshabilitada, piloto NOT RUN y RC-F02 abierto.

## Mejora de routing integrada — 2026-09-23

Verificabilidad, ruta rápida, diagnóstico antes de escalar y obligación auditable en
planning/ejecución/review. 25 tests runtime + 22 lifecycle OK; check-release OK.
Origen: improve/model-routing-precision. Evidencia: docs/requirements/model-routing-precision/EVIDENCE.md.
Integrada y publicada en v2.3.0-rc.2. Sin cambios globales, modelos nuevos ni mediciones
de ahorro; esas mediciones continúan fuera del alcance cerrado.

## Publicación v2.2.2

- **Commit/tag:** `20ea27ac33f92928f2e8ebe7a0c0cf4f14bd8a67` / `v2.2.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.2
- **Assets:** `ai-software-factory-v2.2.2.zip` y `.sha256`; ZIP digest `30b2ff08d6e6c5f5b47bbe94b493309f9367a36b38284ae622505e0dc2cd098a`.
- **CI:** Validate y Factory v2.2.2 Runtime Guardrails completados exitosamente el 2026-09-20.
