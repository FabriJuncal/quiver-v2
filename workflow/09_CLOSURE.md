# 09 — Closure

Cerrar únicamente con evidencia.

Actualizar:

```text
06_CLOSURE.md
requirement/STATE.md
PROJECT_STATE.md
```

Registrar:

- criterios verificados;
- tests/validaciones reales;
- resultados;
- desviaciones;
- pendientes;
- riesgos residuales;
- métricas disponibles;
- **AI Execution Record** cuando exista información.

## AI Execution Record

Registrar de forma liviana:

- planning profile;
- implementation profiles usados;
- review profile;
- escalations/downgrades;
- retries/rework observado;
- tokens/costo real si la herramienta los expone.

No inventar tokens ni costos.

Estos datos sirven para mejorar el routing futuro.

No afirmar lo que no fue verificado.

Dejar siempre una próxima acción a nivel proyecto aunque el requirement quede cerrado.

Retirar el requirement cerrado de `Active requirement` y seleccionar el siguiente ya priorizado. Continuar si su próxima acción está autorizada; si necesita decisión, explicar cuál y la respuesta exacta. Si no existe trabajo pendiente, registrar `Next action: esperar un nuevo requirement del usuario`, `User action required: true` y `Expected output: nueva petición`; no inventar tareas para prolongar el flujo.
