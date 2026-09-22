# S02 — Execution Brief

## AI Execution Profile

Inherit: ../../STATE.md → AI Strategy / implementación offline BALANCED.
Switch Benefit LOW; no se cambia el modelo ni se infiere identidad activa.

## Objective

Registros v2 compatibles y checker.

## Ordered steps

1. Leer SPEC y sección S02 del plan aprobado.
2. Modificar únicamente templates/slice/RUN.schema.json; scripts/lib/check_execution.py; tests.
3. Ejecutar Tests de schema, opt-in, controles y compatibilidad v1/v2.
4. Registrar evidencia y continuar próxima slice autorizada.

## Constraints

No workers, configuración personal, red mutante ni publicación. No prometer controles
vivos a partir de validación estática; preservar contrato/registros históricos.

## Definition of done

Criterios AC01, AC02, AC05, AC06, AC07, AC09 cubiertos por implementación/evidencia offline y sin obligatorios pendientes.

