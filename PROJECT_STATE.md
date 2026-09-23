# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** completed
- **Current phase:** branch-aware discovery integrado en `main` y verificado
- **Active requirement:** none
- **Last completed requirement:** docs/requirements/branch-aware-discovery/STATE.md
- **Current slice:** none
- **Completed:** rc.2 publicada; branch-aware discovery F0–F6 implementado y validado; PR #3 integrado en `dd59081`; checks Ubuntu/macOS PASS.
- **Pending:** none dentro de branch-aware discovery. No hay release nueva autorizada; RC-F02 continúa fuera del alcance de este trabajo.
- **Next action:** si se desea distribuir branch-aware discovery en una versión, abrir un requirement separado de release y definir su alcance.
- **Why this is next:** la capacidad ya está integrada en `main`; versionado y publicación son decisiones separadas sin autorización vigente.
- **User action required:** true
- **Decision required:** decidir si y cuándo preparar una nueva versión publicable.
- **Expected output:** feedback de uso o una autorización futura y concreta de release.
- **After this:** no ejecutar publicación automáticamente; iniciar el flujo de release solo bajo autorización.
- **Blocked by:** none
- **Runtime limitation:** none
- **Runtime limitation detail:** comportamiento productivo/backend de clientes y configuración efectiva de modelos no fueron parte de la validación; no bloquean el MVP cerrado.
- **Resume instruction:** branch-aware discovery está integrado en `main` por PR #3. Leer docs/requirements/branch-aware-discovery/STATE.md y preservar evidencia privada y codex-skills-optimization. No publicar sin autorización explícita.

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
