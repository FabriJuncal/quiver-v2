# P01 — Execution Brief

## AI Execution Profile

Inherit: [STATE → AI Strategy](../../STATE.md). Sin inferir modelo activo.

## Objective / Ordered steps

1. Leer SPEC y sección P01 del plan aprobado.
2. Reglas opt-in, referencias canónicas, ownership y reconciliación histórica.
3. Verificar criterios con pruebas/evidencia offline; actualizar estado y continuar.

## Constraints

No lanzar workers reales, no publicar, no cambiar configuración personal.
Solo coordinador actualiza STATE. No habilitar opt-in de delegación para este requirement.

## Required tests / Definition of done

Escenarios asociados en VALIDATION; registrar resultados reales en CLOSURE_BRIEF.
No afirmar conducta del runtime a partir de fixtures. Aplicar Finalization Gate.
