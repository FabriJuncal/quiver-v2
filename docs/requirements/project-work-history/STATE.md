# Requirement State — project-work-history

## Identificación

- **Ticket / slug:** project-work-history
- **Title:** Histórico de tokens, USD y tiempo por tipo de trabajo en un proyecto
- **Status:** complete-with-notes
- **Phase:** cierre H01/H02
- **Risk level:** N2 — extensión del contrato de medición y agregación con integridad recuperable
- **Last updated:** 2026-09-25

## Decisiones

- **Acceptance criteria:** approved v1 — `01_ACCEPTANCE_CRITERIA.md`, respuesta explícita del usuario del 2026-09-25
- **Selected option:** D01 aprobada — marca por binding, histórico prospectivo, USD directo con evidencia opaca y Kev como sugeridor local opt-in
- **Test profile:** T2 ejecutado — 46/46 pruebas afectadas PASS con fixtures artificiales
- **Plan version:** v1 aprobada — `03_PLAN.md`
- **Plan review:** approved-with-notes — self review en `04_PLAN_REVIEW.md`
- **Human plan approval:** approved — `Aprobar plan v1 y ejecutar`, respuesta explícita del usuario del 2026-09-25
- **Execution authorization:** approved — petición inicial de implementación y aprobación del plan v1 del 2026-09-25
- **Workflow size:** full

## Ejecución

- **Current slice:** none
- **Completed slices:** H01 captura y agregación; H02 evidencia USD y Kev opcional
- **Pending slices:** none
- **Pending required findings:** none
- **Implementation review:** approved-with-notes — `05_IMPLEMENTATION_REVIEW.md`, self review inline N2
- **Directed correction rounds:** 0

## AI Strategy

- **Planning:** BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium; fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- **Implementation default:** BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium; fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- **Review:** ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High; dedicated review recomendado si el diff o riesgo material lo justifican.
- **Routing decision:** `routing-v1`, catálogo v2.2.2 verificado 2026-09-20; base policy. Contrato local y pruebas discriminantes disponibles; granularidad y USD quedaron fijados en D01. Switch Benefit MEDIUM; ningún Model Gate ahora. El modelo/reasoning efectivos de esta sesión no están verificados.
- **Escalation triggers:** posible corrupción de ledger, pérdida de datos, atribución cruzada entre proyectos o semántica de USD facturado.

## Progreso

- **Completed:** observador v1 cerrado conservado; criterios/D01/plan v1 aprobados; H01/H02 implementadas; T2 46/46 PASS; review N2 inline sin findings obligatorios; cierre documentado en `06_CLOSURE.md`.
- **In progress:** none.
- **Pending:** primera captura prospectiva con una fuente real, solo si se autoriza por separado; fuera de este cierre.

## Próxima acción

- **Next action:** en el próximo trabajo nuevo que se quiera medir, autorizar una fuente concreta y crear un binding marcado antes de iniciarlo.
- **Why this is next:** H01/H02 están cerradas; la primera medición real exige una fuente y frontera prospectiva explícitas.
- **User action required:** true — elegir un trabajo nuevo y autorizar la fuente exacta.
- **Decision required:** fuente e identidad de trabajo nuevo.
- **Expected output:** primer histórico real acotado, con unknowns preservados.
- **After this:** refresh, lifecycle, snapshot y consulta history de ese trabajo, según autorización.
- **Blocked by:** none
- **Runtime limitation:** none
- **Runtime limitation detail:** Python 3.14 disponible; ninguna fuente real requerida para fixtures.
- **Resume instruction:** leer PROJECT_STATE.md, este STATE, 06_CLOSURE.md y la guía PLAN_USAGE.md; conservar plan-usage-observer S01–S03 cerrado y el worktree sucio. No acceder a sesiones reales sin nueva autorización precisa.

## Decision Boundary

El usuario eligió alcance prospectivo y USD real solo con evidencia, propuso Kev
para categorizar y aprobó explícitamente D01/criterios/plan v1 y ejecución el
2026-09-25. Kev queda como sugeridor opcional, con categoría confirmada antes de
medir. H01/H02 se cerraron con fixtures; no se autorizó una fuente real para
medir el próximo trabajo.
