# H01 — captura y agregación prospectiva

- **Status:** complete
- **Plan:** `../../03_PLAN.md` v1 aprobado el 2026-09-25.
- **Criterios:** H-01–H-05, H-07–H-09.

Agregar `work_kind` y `work_id` opt-in al binding y una vista histórica JSON/texto
que lee únicamente revisiones v2 persistidas del ledger privado. Agrupar por
proyecto, trabajo y categoría; no contar revisiones anteriores ni bindings legacy.
Tokens nativos exactos, tiempo con límites explícitos y unknowns visibles. No
leer sesiones reales ni modificar launcher/router.
