# Cierre — observador de uso por plan v1

Fecha: 2026-09-25. Estado: **CERRADO CON NOTAS**. S01 y S02 permanecen cerradas;
S03 validó prospectivamente la primera integración real acotada. No hubo commit,
publicación, dependencia nueva, delegación ni cambio de router/launcher/configuración.

## Resultado y criterios

- AC-01: el observador se invocó explícitamente desde CLI sobre un ledger privado;
  modo off sin lectura de fuente y flujo sin cambios cubiertos por fixtures.
- AC-09: una sola fuente autorizada, lectura selectiva de metadatos, IDs y
  contadores; ningún prompt, mensaje o argumento conservado. Directorio `0700`,
  ledger `0600`; no se persistieron ruta ni IDs reales de la fuente en el repo.
- AC-11: binding anterior a la tarea, checkpoint byte `3365161`; refresh posterior
  a la explicación de la guía. Seis respuestas/254927 tokens del intervalo
  concuerdan exactamente entre fuente y reporte; cero duplicados o excluidos.
  Siete registros del turno de binding quedaron fuera. El observador solo leyó el
  original; identidad y hashes de prefijo verificados.
- AC-12: el opt-in S03 conserva session/thread, excluye turno de binding y rechaza
  thread ajeno; suite offline reciente 35/35 PASS. No apareció thread ajeno en
  este intervalo real.
- AC-02/03/04: regresiones afectadas de binding, dedup y persistencia PASS en la
  misma suite. Los resultados de S01/S02 no se reabrieron.

El reporte v2 quedó persistido como revisión 1 en el ledger privado; después se
deshabilitó el binding, conservando los seis registros. El resultado
de importación es `provisional`; la vista v2 es `incomplete` por fin técnico no
observado y seis respuestas sin precio. Modelo, tier, modalidad de pago, USD y
tiempos no observables quedan unknown. No se usaron tarifas comerciales.

## Verificaciones y review

- T13: comparador independiente de registros fuente/ledger por ID y seis contadores;
  coincidencia exacta, identidad/prefijo estables. Versión/host allowlisted:
  CLI 0.156.1, `codex-tui`, `cli`.
- `python3.14 -I -B tests/test_plan_usage.py`: 35/35 PASS.
- Revisión N2 inline en [05_IMPLEMENTATION_REVIEW](05_IMPLEMENTATION_REVIEW.md):
  APROBADO CON NOTAS, sin hallazgos obligatorios ni ronda de corrección S03.
- `git diff --check`, doctor de estados, enlaces y barrido dirigido de privacidad:
  PASS. CI remoto y otros hosts no verificados.

## Límites y continuidad

El intervalo contiene el turno de aclaración anterior y la tarea de revisar la
guía; los 254927 tokens no se atribuyen exclusivamente a la tarea. La respuesta
final y el cierre documental posteriores al refresh no están incluidos. No hubo
evento lifecycle de inicio/fin ni aceptación explícita registrada, por lo que
duración y estado de aceptación siguen unknown/pending. T13 demuestra una
integración acotada, no cobertura de otras sesiones ni costos facturados.

AI Execution Record: perfil ADVANCED/High recomendado para S03 y review; modelo
y reasoning efectivos NO VERIFICADOS. Hubo un ajuste previo para turnos raíz
sucesivos, cuatro pruebas dirigidas PASS, y cero rondas de corrección en review.
Consumo medido del intervalo: 254927 tokens; USD real unknown.

**Siguiente acción única:** esperar un nuevo requirement del usuario. No reabrir
el binding ni ampliar el intervalo sin autorización nueva.
