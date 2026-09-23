# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** awaiting-approval
- **Current phase:** PR #2 abierto y CI remota aprobada; merge/publicación pendientes
- **Active requirement:** docs/requirements/release-2-3-0-rc-2/STATE.md
- **Last completed requirement:** docs/requirements/model-routing-precision/STATE.md
- **Current slice:** none
- **Completed:** candidata `b193a396...`; PR #2 abierto; ocho jobs remotos PASS en Ubuntu/macOS; ZIP regenerado con 139 tests OK; check-release, hashes, exclusiones y bundle verificados.
- **Pending:** merge, regeneración desde merge commit, tag y GitHub prerelease; RC-F02 sigue bloqueando activación viva.
- **Next action:** obtener autorización para mergear PR #2 y publicar la prerelease rc.2 según PUBLISH_PLAN.md.
- **Why this is next:** la candidata y CI están aprobadas; merge/tag/release son escrituras externas aún no autorizadas.
- **User action required:** true
- **Decision required:** autorizar merge y publicación de rc.2 como prerelease offline; no implica anunciar multiagente operativo.
- **Expected output:** PR integrado a main, tag anotado `v2.3.0-rc.2` y prerelease con ZIP/SHA verificados.
- **After this:** verificar assets/hashes remotos, cerrar el requirement y registrar la URL pública.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability solo para piloto; ninguna para preview offline.
- **Runtime limitation detail:** RC-F02 impide activar/anunciar delegación operativa; no bloquea la prerelease offline.
- **Resume instruction:** leer docs/requirements/release-2-3-0-rc-2/{STATE,EVIDENCE,05_IMPLEMENTATION_REVIEW,PUBLISH_PLAN}.md. Para avanzar: `Autorizar merge y publicación de rc.2`.

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
