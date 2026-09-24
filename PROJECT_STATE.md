# PROJECT_STATE

- **Project:** AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview
- **Status:** idle
- **Current phase:** cierres documentales archivados en rama local; sin requirement activo
- **Active requirement:** none
- **Last completed requirement:** docs/requirements/branch-aware-operational-pilot/STATE.md
- **Last closed requirement:** docs/requirements/branch-aware-operational-pilot-v2/STATE.md — cancelled; experimento inconcluso
- **Current slice:** none
- **Completed:** rc.2 publicada; discovery integrado; benchmark v1 cerrado; v2.1/T2 aprobado; P0–P2 completadas con key cerrado, paquetes A/B seguros y sello previo validado. Los cierres de v1, v2.1 y recurrencia de Skills quedaron en commits documentales locales separados.
- **Pending:** P3–P6 de v2.1 canceladas sin ejecución; RC-F02 sigue fuera de alcance. No hay push ni PR para los commits documentales. La evidencia privada de discovery y el trabajo preexistente de optimización de Skills permanecen fuera de esos commits.
- **Next action:** decidir si se revisa y publica la rama documental mediante un PR acotado; mantener los documentos privados fuera de Git hasta una decisión separada sobre derivados sanitizados.
- **Why this is next:** los commits locales preservan los cierres aptos para versionar sin mezclar la evidencia privada; publicarlos o preparar derivados adicionales son decisiones distintas.
- **User action required:** true
- **Decision required:** autorizar o descartar push/PR de la rama documental; cualquier saneamiento de los grupos excluidos requiere alcance propio.
- **Expected output:** decisión sobre la rama documental o nueva petición independiente.
- **After this:** si se autoriza, revisar el diff final y abrir solo el PR documental; no reabrir el benchmark automáticamente.
- **Blocked by:** none; E-SENS-01 quedó excluido de los paquetes derivados.
- **Runtime limitation:** none
- **Runtime limitation detail:** ninguna. La configuración efectiva de P2 permanece `unknown`; las verificaciones se sustentan en artefactos y comandos reproducibles.
- **Resume instruction:** revisar la rama local `docs/archive-closed-requirements-2026-09-24`, sus commits y el diff contra `origin/main`. No usar `git add .`: los archivos privados de discovery y el trabajo de optimización de Skills siguen untracked. No hacer push ni PR sin decisión explícita. El benchmark v2.1 permanece cancelado; los antiguos prompts de P3 no están vigentes.

## Archivo documental local — 2026-09-24

La rama `docs/archive-closed-requirements-2026-09-24` conserva, en commits separados,
el resultado v1 (`9ee3d5f`), el cierre v2.1 (`b07d9f8`) y la investigación de
recurrencia de Skills (`0ca946c`). No incluye inventarios, refs/OID o rutas
específicas ni el informe detallado del piloto; tampoco incluye
`codex-skills-optimization/`. La inspección de privacidad fue por patrones y
revisión dirigida, no una garantía exhaustiva.
El PR quedó diferido. No se hizo push, merge, tag ni release.

Validación del archivo local: 34 archivos documentales/estado en cuatro commits;
`git diff --check origin/main...HEAD` PASS; enlaces relativos del cierre v2.1
resueltos; SHA-256 de `BENCHMARK_REPORT.md` igual al sidecar; cero matches de
identificadores privados conocidos, firmas comunes de credenciales o JWT en el
contenido commiteado. No hay código en el diff. Permanecen 72 archivos untracked
de discovery y optimización de Skills, sin stage ni commit. La ausencia de matches
no certifica que el contenido sea publicable sin revisión humana final.

## Benchmark operativo branch-aware — plan v2

v2.1 y T2 reforzado sustituyen v2/T3 para la continuación. El contrato conserva un key
cerrado, tres pares y scoring independiente, con métricas y evidencia reducidas a lo
necesario. P0–P2 se registraron como PASS; su evidencia se conserva. El usuario cerró
el benchmark por priorización antes de P3. P3–P6 canceladas; resultado inconcluso, sin
demostración de beneficio ni decisión de release.

## Benchmark operativo branch-aware — plan v1

Tarea recomendada: planificar migración de notificaciones push entre dos snapshots
relacionados bajo aliases privados. Tres pares HEAD-only/branch-aware, mismo presupuesto,
scoring ciego y review N2. El discovery de planificación preservó el repo piloto.

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

## Mantenimiento de catálogo global de Skills — 2026-09-23

El requirement `docs/requirements/codex-skills-context-budget-recurrence/` quedó
cerrado. C01 confirmó que el override de Vercel en `config.toml` no controla el
catálogo curated del host y fue revertida de forma dirigida. No quedan
deshabilitaciones nuevas activas; investigar el mecanismo del host requiere un
requirement separado.

## Publicación v2.2.2

- **Commit/tag:** `20ea27ac33f92928f2e8ebe7a0c0cf4f14bd8a67` / `v2.2.2` anotado.
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.2
- **Assets:** `ai-software-factory-v2.2.2.zip` y `.sha256`; ZIP digest `30b2ff08d6e6c5f5b47bbe94b493309f9367a36b38284ae622505e0dc2cd098a`.
- **CI:** Validate y Factory v2.2.2 Runtime Guardrails completados exitosamente el 2026-09-20.
