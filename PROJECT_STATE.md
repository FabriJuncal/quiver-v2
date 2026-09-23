# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** awaiting-approval
- **Current phase:** candidata rc.2 validada; push/PR/CI pendientes
- **Active requirement:** docs/requirements/release-2-3-0-rc-2/STATE.md
- **Last completed requirement:** docs/requirements/model-routing-precision/STATE.md
- **Current slice:** none
- **Completed:** candidata local rc.2 en `6048e545...`; ZIP final con 139 tests OK; check-release, hashes, exclusiones y bundle verificados. El trabajo offline previo y la prueba sandbox permanecen documentados en sus requirements.
- **Pending:** CI remota y publicación externa; RC-F02 sigue bloqueando activación viva.
- **Next action:** obtener autorización para push de `release/2.3.0-rc.2` y PR/CI.
- **Why this is next:** commit/ZIP final validados; CI requiere escritura remota y no existe rama/tag rc.2 en origin.
- **User action required:** true
- **Decision required:** autorizar push + PR para CI; no implica anunciar multiagente operativo.
- **Expected output:** rama/PR remotos con CI macOS/Linux; tag/release esperan PASS y target final.
- **After this:** si CI pasa, completar publicación autorizada según PUBLISH_PLAN; si falla, corregir y regenerar.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability solo para piloto; ninguna para preview offline.
- **Runtime limitation detail:** RC-F02 impide activar/anunciar delegación operativa; CI remota pendiente por boundary de escritura, no por fallo runtime.
- **Resume instruction:** leer docs/requirements/release-2-3-0-rc-2/{STATE,EVIDENCE,05_IMPLEMENTATION_REVIEW,PUBLISH_PLAN}.md. Para avanzar: `Autorizar push y PR de rc.2`.

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
