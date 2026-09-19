# Decision Boundaries

Guided Mode busca reducir interrupciones innecesarias.

La Factory debe avanzar automáticamente mientras no necesite una decisión humana material.

## Continuar automáticamente

Ejemplos:

- leer archivos;
- inspeccionar código;
- investigar documentación oficial;
- crear una matriz;
- actualizar estado;
- generar una slice ya aprobada;
- ejecutar tests aprobados;
- revisar un plan.

## Detenerse

Ejemplos:

- cambiar alcance;
- aprobar criterios;
- seleccionar alternativa;
- seleccionar T1/T2/T3 si existe un trade-off material aún no aprobado;
- aprobar plan;
- cambiar arquitectura difícil de revertir;
- operación destructiva;
- deploy;
- decisión de costo relevante.
- Model Gate HIGH pendiente;
- review dedicado que necesita intervención;
- blocker real.

La ausencia de Model Gate no elimina otros boundaries. No repetir aprobaciones explícitas vigentes dentro del alcance autorizado. La política canónica está en [el contrato](../../workflow/00_SHARED_CONTRACT.md); [riesgo y ruta compacta](RISK_AND_WORKFLOW.md) define las excepciones proporcionales N0/N1.

## UX esperada

No:

```text
Terminé el análisis.
¿Cómo continuamos?
```

Sí:

```text
Próximo paso:
verificar documentación oficial.

ACCIÓN DEL USUARIO: ninguna

Continúo con esa verificación.
```

Cuando existe una decisión:

```text
DECISIÓN NECESARIA

A — ...
B — ...

RECOMENDACIÓN:
A

RESPUESTA SIMPLE:
A + T2
```
