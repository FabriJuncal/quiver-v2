# Slice Spec — S03

- **Slice ID:** S03
- **Status:** closed-with-notes — T13 reconciled 2026-09-25

## Goal

Validar prospectivamente el observador en una tarea habitual autorizada de Quiver,
con binding anterior al trabajo y reconciliación posterior contra una única fuente.

## Scope

- Fuente JSONL e intervalo indicados explícitamente por el usuario; lectura selectiva
  de metadatos, IDs y contadores. Ruta e IDs reales permanecen fuera del repositorio.
- Ajuste acotado del adaptador para permitir turnos raíz sucesivos en el mismo thread
  de la sesión dedicada, excluyendo el turno del propio binding. Forks/children con
  thread distinto permanecen excluidos.
- Binding privado previo al próximo turno, T13, review y cierre con evidencia.

No incluye búsqueda de otras sesiones, importación histórica, tarifas comerciales,
predicción, router/launcher, dependencias, publicación, commit ni delegación.

## Criteria covered

- AC-01, AC-09, AC-11 y AC-12; regresión afectada de AC-02/03/04.

## Dependencies

- S01 y S02 cerradas offline; plan v1 aprobado.
- Autorización S03 y fuente/intervalo exactos del usuario en esta conversación.
- Una tarea habitual nueva después de registrar el binding.

## Validation

- Prueba sintética dirigida de turnos raíz sucesivos y rechazo de thread ajeno.
- T13 real solo después de la tarea y del refresh autorizado.
- Preservación del original, privacidad, suite offline reciente y review N2.

## AI Profile Recommendation

- **Profile:** ADVANCED, heredado de `../../STATE.md` para S03.
- **Reasoning:** High recomendado; configuración efectiva NO VERIFICADA.
- **Reason:** reconciliación y privacidad con fuente real; verificaciones deterministas
  para el ajuste acotado. Reevaluar ante fallo de contrato o capacidad insuficiente.
