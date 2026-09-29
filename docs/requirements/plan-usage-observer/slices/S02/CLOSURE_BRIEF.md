# Closure Brief — S02

## Criteria to verify

- AC-04, AC-05, AC-06, AC-07, AC-08 y AC-10.

## Evidence to record

- Diff acotado de S02 y compatibilidad explícita del reporte v1.
- Fixtures artificiales de lifecycle, clock, fallos/retries/cancelación, revisiones
  tardías y tarifas sintéticas.
- Salidas JSON/texto versionadas, snapshots previos preservados y unknowns comprobados.
- Resultado de pruebas, sintaxis, esquema, enlaces y whitespace.

Evidencia implementada:

- `scripts/lib/plan_usage.py`: eventos lifecycle explícitos/idempotentes, timestamps
  con zona, cruce de outcomes con registros, cálculo temporal sin heurística, snapshots
  tarifarios `synthetic` inmutables y revisiones atómicas preservadas;
- reporte v2 JSON/texto con identidad, lifecycle, tiempos, outcomes, costo/naturaleza,
  revisión, unknowns y anomalías; API v1 y esquema v1 preservados explícitamente;
- `tests/test_plan_usage.py`: clase S02 con fixtures temporales artificiales;
- `docs/guides/PLAN_USAGE.md`: comandos y límites; HANDOFF contiene wireframe actualizado.

Cobertura de criterios:

- AC-04: lock, fallos antes de replace y preservación/retry de revisiones;
- AC-05: fallo, retry y cancelación; afirmación de uso contrastada por response ID;
- AC-06: cierre técnico/aceptación separados, eventos tardíos y revisiones preservadas;
- AC-07: límites explícitos, pausa/resume y reloj regresivo; actividad/espera/agente unknown;
- AC-08: Decimal, identidad/tier/tarifa, cambio no resuelto, snapshot inmutable,
  subtotal sintético y billed USD unknown;
- AC-10: superficies v1/v2, JSON/texto y CLI versionada.

## Tests to report

- `python3.14 -I -B tests/test_plan_usage.py PlanUsageS02 -v`: 13/13 OK —
  T04–T07, T11/T12 con fixtures artificiales;
- comando focalizado de seis regresiones S01 afectadas: 6/6 OK — privacidad/conteo,
  superficie v1, crash antes/después de replace, modo off y CLI;
- `python3.14 -B -m py_compile scripts/lib/plan_usage.py tests/test_plan_usage.py`: PASS;
- parseo JSON de `MEASUREMENT.schema.json` y `MEASUREMENT.v1.schema.json`: PASS;
- `git diff --check`: PASS.

## Deviations

- Review inline, no independiente, porque delegación estaba prohibida y el review N2
  dedicado es recomendado. F05–F07 se cerraron en una ronda dirigida.
- T08/T09 cerrados de S01 no se repitieron completos; se ejecutaron solo privacidad,
  persistencia, reporte y CLI afectados por cambios nuevos.
- Python 3.11 local y CI remoto no se ejecutaron; Python 3.14.4 pasó.
- Modelo/reasoning efectivos y consumo de esta implementación no fueron observables.

## Risks / pending

- S03 e integración con una sesión habitual siguen fuera de alcance.
- Sin datos reales, costos y tiempos de uso habitual permanecen no verificados.
- Un subtotal sintético no es factura, gasto de suscripción ni modalidad de pago.
