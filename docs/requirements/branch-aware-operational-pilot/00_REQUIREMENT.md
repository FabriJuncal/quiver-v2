# Requirement — Branch-aware operational pilot

Fecha: 2026-09-23. Riesgo: **N2**.

## Problema

Branch-aware discovery está implementado, validado e integrado en `main`, pero todavía
no existe evidencia de que mejore una tarea real frente a analizar solamente `HEAD`.
Las pruebas actuales demuestran integridad del lector; no demuestran precisión relativa,
tiempo de trabajo, contexto utilizado, tokens ni costo operativo.

## Objetivo

Diseñar un benchmark reproducible con dos ejecuciones independientes de la misma tarea:

- **A — HEAD-only:** contexto limitado al snapshot actual.
- **B — branch-aware:** inventario, comparación y contexto de variantes seleccionadas.

El benchmark debe medir calidad, cobertura, atribución, contexto, esfuerzo e integridad
sin modificar el repositorio piloto ni convertir estimaciones en mediciones reales.

## Restricciones aprobadas para planificación

- Repositorio piloto privado exclusivamente en lectura.
- Sin checkout, fetch, pull, worktree, commits, configuración ni escritura en `.git`.
- Output del benchmark fuera del worktree piloto.
- Misma tarea, criterios, snapshot, presupuesto y configuración IA en A/B.
- Sesiones independientes para evitar contaminación.
- Tokens, costo, modelo efectivo y latencia de inferencia son `unknown` salvo evidencia
  directa del runtime.
- Sin ejecutar el benchmark completo, modificar Quiver, commit, push, PR, merge, tag o
  release durante esta fase.

## Alcance

Incluye diseño del experimento, selección de tarea, métricas, controles, criterios de
aceptación, rollback y autorrevisión del plan. Excluye implementación en aplicaciones,
builds móviles, llamadas a backend y decisión de release.

## Evidencia de discovery

El snapshot privado de planificación obtuvo cobertura completa de 95 refs y 82 tips,
cero errores y preservación exacta de HEAD, refs, índice, status, diffs y archivos
untracked. Los nombres, OID y rutas privadas se conservan fuera del árbol versionable en
`.git/private-evidence/branch-aware-operational-pilot/`.
