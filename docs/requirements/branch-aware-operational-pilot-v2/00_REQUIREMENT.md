# Requirement — Branch-aware operational pilot v2

Fecha: 2026-09-23. Riesgo: **N2**. Estado: **criterios, plan v2 y T3 aprobados;
ejecución no autorizada**.

## Problema

El benchmark v1 terminó como `beneficio no probado`: preservó integridad y aislamiento
operativo, pero su answer key no fijó denominadores cerrados ni unidades contables para
recall, precisión y omisiones. Completar esos datos después de ver las respuestas habría
contaminado la medición.

## Objetivo

Diseñar un experimento v2 nuevo que compare:

- **A — HEAD-only:** evidencia del snapshot actual;
- **B — branch-aware:** la misma evidencia base más evidencia atribuida de otra variante.

La comparación debe producir métricas recalculables, mantener el repositorio piloto en
solo lectura y demostrar que el answer key y todos los insumos quedaron sellados antes de
generar cualquier respuesta nueva.

## Alcance autorizado ahora

- criterios de aceptación;
- decisión de diseño;
- contrato del answer key y del formato de respuesta;
- definiciones y denominadores de scoring;
- protocolo temporal y de integridad;
- plan P0–P6 y self review del plan;
- actualización de estado.

## Fuera de alcance ahora

- ejecutar P0–P6;
- leer o modificar el repositorio piloto para obtener evidencia nueva;
- generar respuestas P3;
- reutilizar, reetiquetar o re-puntuar las seis respuestas de v1;
- poblar el answer key concreto con evidencia privada;
- modificar código de Quiver;
- delegar scoring o review;
- commit, push, PR, merge, tag, release o publicación.

## Invariantes

1. v1 permanece cerrada e inmutable como antecedente; no es una muestra de v2.
2. El experimento v2 usa directorios, manifest y respuestas nuevos.
3. El repositorio piloto permanece exclusivamente en lectura y sin operaciones Git que
   cambien worktree, índice, configuración, refs o `.git`.
4. La evidencia privada queda fuera del repositorio piloto y fuera del contenido
   versionable de Quiver.
5. Hechos medidos, inferencias y `unknown` se registran por separado.
6. Una recomendación de perfil no prueba el modelo/reasoning efectivos del runtime.

## Resultado de esta fase documental

Plan v2 revisado y aprobado por el usuario el 2026-09-23. La misma instrucción negó
expresamente P0–P6, respuestas, scoring, delegación y publicación.
