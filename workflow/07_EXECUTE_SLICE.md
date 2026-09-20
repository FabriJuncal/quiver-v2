# 07 — Ejecutar slice

1. leer `PROJECT_STATE.md`;
2. leer requirement `STATE.md`;
3. leer `EXECUTION_BRIEF.md`;
4. cargar contexto mínimo;
5. activar skills por routing;
6. comprobar aprobación humana del plan y autorización de ejecución; evaluar AI Execution Profile;
7. ejecutar Guided Model Gate solo si corresponde;
8. implementar;
9. ejecutar testing aprobado;
10. registrar evidencia;
11. actualizar estado.

## AI Model Gate

`Model Gate required` es una recomendación persistida, no un bloqueo eterno. Reevaluar antes de actuar: si la configuración suficiente ya fue confirmada en esta sesión y fase, continuar sin repetir el gate. Si falta confirmación necesaria y el beneficio es HIGH:

- no asumir el modelo activo;
- mostrar Guided Model Gate completo;
- indicar `/status` si el usuario no sabe;
- indicar `/model`;
- indicar nombre completo + ID;
- indicar reasoning;
- indicar fallback;
- pedir `continuar`;
- detenerse.

Cuando el usuario escriba `continuar` en respuesta a ese gate, considerar confirmada su acción para esa fase/sesión, sin afirmar introspección del runtime. No usar un `continuar` genérico en sesión nueva como aprobación de plan o cierre de review. Persistir el avance de trabajo, no el modelo activo.

## Sin gate

Si no hay Model Gate pendiente **ni otro Decision Boundary**:

```text
ACCIÓN DEL USUARIO: ninguna
```

y continuar.

No mencionar optimizaciones de modelo de beneficio LOW.

## Downgrade

No interrumpir para cierres cortos.

Solo proponer downgrade al comenzar una fase sustancial y mecánica con Switch Benefit HIGH.

## Cierre de slice

No declarar terminado sin evidencia.

Si quedan slices aprobadas y no existe Decision Boundary, continuar.

Aplicar Finalization Gate de `00_SHARED_CONTRACT.md`: activar la siguiente slice autorizada
y ejecutar su Next action en el mismo turno. Un cierre de slice no habilita cierre prematuro
del turno. Si el runtime lo impide, registrar limitación real y reanudación exacta.
