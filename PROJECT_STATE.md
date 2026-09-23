# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** awaiting-review
- **Current phase:** PR #3 de branch-aware discovery abierto y pendiente de review
- **Active requirement:** docs/requirements/branch-aware-discovery/STATE.md
- **Last completed requirement:** docs/requirements/branch-aware-discovery/STATE.md
- **Current slice:** none
- **Completed:** rc.2 publicada; branch-aware discovery F0–F6 implementado y validado; commit `96fa624`; PR privado #3 abierto contra `main`.
- **Pending:** review del PR #3 y resolución de hallazgos si aparecen; merge y publicación no están autorizados. RC-F02 continúa fuera del alcance de este trabajo.
- **Next action:** revisar https://github.com/FabriJuncal/quiver-v2/pull/3 y decidir si requiere cambios o queda aprobado.
- **Why this is next:** la rama y el PR autorizados ya existen; avanzar a merge requiere review y autorización humana separada.
- **User action required:** true
- **Decision required:** aprobar el PR, solicitar cambios o dejarlo abierto.
- **Expected output:** review trazable del PR #3 y, si corresponde, autorización explícita de merge.
- **After this:** resolver findings; mergear solo con autorización explícita y tratar cualquier publicación como una acción posterior separada.
- **Blocked by:** none
- **Runtime limitation:** none
- **Runtime limitation detail:** comportamiento productivo/backend de clientes y configuración efectiva de modelos no fueron parte de la validación; no bloquean el MVP cerrado.
- **Resume instruction:** leer docs/requirements/branch-aware-discovery/STATE.md, docs/PRs/BRANCH_AWARE_DISCOVERY.md y el PR #3. Preservar evidencia privada y codex-skills-optimization. No mergear ni publicar sin autorización explícita.

## Discovery por variantes — 2026-09-23

Investigación y plan documentados en docs/requirements/branch-aware-discovery/.
Piloto privado analizado: 35 ramas locales y 60 remotas; 95 refs de rama y 82
tips distintos. Solo lectura; sin implementación ni cambios en la aplicación.
Estado de instalaciones activas y comportamiento del backend desconocidos.
La entrega incluye evidencia, alternativas, criterios y modelos por fase.

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
