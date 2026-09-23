# STATE — Branch-aware discovery

- **Status:** in-progress
- **Current phase:** preparación de commit y PR autorizada.
- **Current slice:** none
- **Completed:** F0–F6; lector Git offline, integración optativa, 153 tests, check-release, self review y piloto privado de solo lectura con integridad preservada.
- **Pending:** crear commit enfocado, publicar la rama y abrir el PR; merge y publicación quedan excluidos.
- **Risk level:** N2; integridad del contexto entre variantes y compatibilidad del discovery existente.
- **Acceptance criteria:** inventario completo del alcance Git, lectura sin checkout, procedencia por OID, contexto acotado por tarea, validación stale, fallos explícitos, integración optativa y piloto de solo lectura.
- **Plan version:** 1.
- **Plan review:** APROBADO CON NOTAS por autorrevisión; plan v1 aprobado por el usuario el 2026-09-23.
- **Implementation review:** APROBADO CON NOTAS; self review N2, una ronda dirigida, tres hallazgos cerrados.
- **Human plan approval:** plan v1 aprobado explícitamente el 2026-09-23.
- **Execution authorization:** MVP F0–F6 autorizado explícitamente el 2026-09-23. Preparación de commit y PR autorizada el 2026-09-23; sin merge ni publicación.
- **Selected option:** Git plumbing, matriz de variantes y contexto por tarea; capacidad optativa y sin servicios nuevos.
- **Test profile:** T2 reforzado; 153 tests PASS, check-release/dry-run/diff PASS; sin builds de aplicaciones cliente.
- **Next action:** crear el commit de branch-aware discovery, verificar el staging y abrir un PR contra `main`.
- **Why this is next:** el MVP está cerrado y el usuario autorizó explícitamente preparar commit y PR.
- **User action required:** false
- **Decision required:** none
- **Expected output:** PR abierto, con SHA y evidencia registrados; sin merge ni publicación.
- **After this:** esperar review y autorización separada para cualquier merge o publicación.
- **Blocked by:** none
- **Runtime limitation:** none
- **Resume instruction:** revisar este STATE, `docs/PRs/BRANCH_AWARE_DISCOVERY.md` y `docs/guides/BRANCH_AWARE_DISCOVERY.md`. Continuar la preparación de commit/PR; preservar artefactos privados y trabajo ajeno; no mergear ni publicar.

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
