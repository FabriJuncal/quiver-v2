# Execution Brief — S02

## AI Execution Profile

Inherit: `../../STATE.md` → AI Strategy / S02.

- **Profile:** ADVANCED
- **Preferred model full name:** GPT-5.6 Sol
- **Model ID:** `gpt-5.6-sol`
- **Reasoning:** high
- **Fallback full name:** GPT-5.6 Terra
- **Fallback model ID:** `gpt-5.6-terra`
- **Fallback reasoning:** high
- **Switch benefit:** MEDIUM tras reevaluación de sesión: la recomendación sigue
  siendo material, pero el contrato está cerrado, el contexto es suficiente y T2
  ofrece oráculos deterministas.
- **Model Gate required:** no
- **Why:** no hay evidencia de capacidad insuficiente; no se infiere ni persiste el
  modelo efectivo de la sesión.
- **Escalate if:** aparece billing real, migración incompatible, pérdida de datos o
  una ambigüedad no resoluble por fixtures.
- **Downgrade after:** no corresponde dentro de esta slice breve.
- **Resolved against catalog date:** 2026-09-20; disponibilidad por cuenta no verificada.

## Objective

Completar AC-04–AC-08 y AC-10 asignados a S02 sin reabrir S01 ni avanzar S03.

## Ordered steps

1. Fijar lifecycle, tiempo, revisión y tarifa sintética en tests T2 artificiales.
2. Extender el ledger de forma aditiva y conservar compatibilidad explícita del reporte v1.
3. Implementar reporte v2 y snapshot de revisión inmutable.
4. Actualizar esquema, guía/wireframe y artefactos de continuidad.
5. Ejecutar T2 de S02 y regresiones S01 directamente afectadas.
6. Registrar evidencia reciente y cerrar S02; detenerse antes de S03.

## Constraints

- No leer sesiones reales ni usar tarifas comerciales.
- Modelo, tier, modalidad de pago, USD o tiempo permanecen unknown cuando falta evidencia.
- No sumar reasoning además de output ni tiempos/subtotales paralelos.
- No instalar dependencias ni cambiar launcher, router o configuración global.
- No delegar, publicar, commitear ni ejecutar S03.

## Required tests

- T04–T07, T11 y T12 del plan v1 con fixtures artificiales.
- Compatibilidad dirigida del reporte v1, conteo S01 y commit atómico afectados.

## Definition of done

- Lifecycle y tiempos solo muestran observaciones explícitas válidas.
- Los costos usan `Decimal` y snapshots `synthetic` inmutables; billed USD sigue unknown.
- Una revisión nueva no sobrescribe la anterior y los eventos tardíos son visibles.
- T2 requerido pasa y el estado/handoff/cierre/wireframe quedan consistentes.
