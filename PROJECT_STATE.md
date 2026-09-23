# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** in-progress
- **Current phase:** preparación local de candidata rc.2 autorizada
- **Active requirement:** docs/requirements/release-2-3-0-rc-2/STATE.md
- **Last completed requirement:** docs/requirements/model-routing-precision/STATE.md
- **Current slice:** RC2-S01
- **Completed:** S01–S04 offline y 111 tests previos preservados. Prueba nueva codex sandbox 0.155.1: 22/22 casos, configuración temporal, sin agentes/modelos adicionales. Protección de archivos ficticios observada; evidencia en docs/requirements/sandbox-isolation-probe/REPORT.md. Config habitual preservada, sin release nueva.
- **Pending:** construir y validar rc.2; publicación requiere autorización final separada.
- **Next action:** completar metadata rc.2, crear commit limpio y validar ZIP exportado.
- **Why this is next:** usuario autorizó continuar con la preparación recomendada; rc.1 no puede reutilizarse.
- **User action required:** false
- **Decision required:** none durante preparación local.
- **Expected output:** commit y artefactos rc.2 revisables con evidencia fresca.
- **After this:** presentar hashes, tests y límites; pedir autorización concreta para push/tag/release.
- **Blocked by:** none
- **Runtime limitation:** none para preparación; unavailable-runtime-capability sigue aplicando al piloto vivo.
- **Runtime limitation detail:** RC-F02 no bloquea preview offline, pero impide activar/anunciar delegación operativa.
- **Resume instruction:** leer docs/requirements/release-2-3-0-rc-2/STATE.md y 03_PLAN.md. Continuar preparación local; no push/tag/publicación sin autorización final.

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
