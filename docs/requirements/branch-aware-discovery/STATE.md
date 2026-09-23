# STATE — Branch-aware discovery

- **Status:** awaiting-review
- **Current phase:** PR #3 abierto y pendiente de review.
- **Current slice:** none
- **Completed:** F0–F6; lector Git offline, integración optativa, 153 tests, check-release, self review, piloto privado preservado, commit `96fa624` y PR #3 abierto.
- **Pending:** review del PR #3 y resolución de hallazgos; merge y publicación quedan excluidos de la autorización vigente.
- **Risk level:** N2; integridad del contexto entre variantes y compatibilidad del discovery existente.
- **Acceptance criteria:** inventario completo del alcance Git, lectura sin checkout, procedencia por OID, contexto acotado por tarea, validación stale, fallos explícitos, integración optativa y piloto de solo lectura.
- **Plan version:** 1.
- **Plan review:** APROBADO CON NOTAS por autorrevisión; plan v1 aprobado por el usuario el 2026-09-23.
- **Implementation review:** APROBADO CON NOTAS; self review N2, una ronda dirigida, tres hallazgos cerrados.
- **Human plan approval:** plan v1 aprobado explícitamente el 2026-09-23.
- **Execution authorization:** MVP F0–F6 autorizado explícitamente el 2026-09-23. Preparación de commit y PR autorizada el 2026-09-23; sin merge ni publicación.
- **Selected option:** Git plumbing, matriz de variantes y contexto por tarea; capacidad optativa y sin servicios nuevos.
- **Test profile:** T2 reforzado; 153 tests PASS, check-release/dry-run/diff PASS; sin builds de aplicaciones cliente.
- **Next action:** revisar https://github.com/FabriJuncal/quiver-v2/pull/3 y decidir si requiere cambios o queda aprobado.
- **Why this is next:** commit, push y apertura del PR autorizados ya están completados; el merge requiere una decisión humana nueva.
- **User action required:** true
- **Decision required:** aprobar el PR, solicitar cambios o dejarlo abierto.
- **Expected output:** review trazable y, si corresponde, autorización explícita de merge.
- **After this:** resolver findings; mergear solo con autorización explícita y mantener la publicación como acción separada.
- **Blocked by:** none
- **Runtime limitation:** none
- **Resume instruction:** revisar este STATE, `docs/PRs/BRANCH_AWARE_DISCOVERY.md` y el PR #3. Preservar artefactos privados y trabajo ajeno; no mergear ni publicar sin autorización explícita.

## Entrega

- **Branch:** `improve/branch-aware-discovery`.
- **Feature commit:** `96fa624` (`Add branch-aware discovery`).
- **Pull request:** https://github.com/FabriJuncal/quiver-v2/pull/3

## Límites y privacidad

El piloto confirmó el comportamiento sobre decenas de refs y tips distintos sin
modificar el repositorio analizado. No verificó instalaciones, backend/runtime de
clientes ni tokens/costo IA.

El inventario, los nombres de ramas, las rutas locales y el informe detallado del
piloto son evidencia privada. Se preservan localmente y se excluyen deliberadamente
del commit y del PR. El PR contiene solamente métricas agregadas necesarias para la
revisión técnica.

## AI Strategy

F0/F1/F3/F5: ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High.
F2/F4/F6: BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium.
El perfil solicitado no prueba la configuración efectiva. El trabajo determinista de
Git no necesita inferencia IA.
