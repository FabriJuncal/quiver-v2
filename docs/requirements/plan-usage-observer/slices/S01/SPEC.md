# Slice Spec — S01

- **Slice ID:** S01
- **Status:** completed — recorrido offline implementado y validado; integración real pendiente en S03

## Goal

Recorrido vertical offline de tokens atribuibles: binding explícito, normalización
con semántica nativa conservada, persistencia privada recuperable y reporte
JSON/texto que conserve los valores desconocidos.

## Scope

Después de cualificar una fuente nativa existente y explícitamente autorizada:

- preparar binding, modo off/on y frontera de captura;
- implementar adaptador, normalización, ledger JSON privado, deduplicación,
  checkpoint y reporte de tokens;
- usar fixtures sintéticas y sin secretos para las pruebas T2 de S01;
- conservar la compatibilidad de CE-v1 y no cambiar launcher, router, permisos,
  autenticación, modelos, configuración global ni el flujo habitual.

La autorización actual no permite leer ni buscar sesiones reales. Por ello no se
puede iniciar la cualificación ni implementar todavía. S02 y S03 están fuera de
alcance.

## Criteria covered

AC-01, AC-02, AC-03, AC-04, AC-09, AC-10 y AC-12 de
[01_ACCEPTANCE_CRITERIA.md](../../01_ACCEPTANCE_CRITERIA.md), con T01–T04,
T06 y T08–T10 de [03_PLAN.md](../../03_PLAN.md#matriz-de-pruebas-t2-reforzado).

## Dependencies

- Criterios v1, D01, T2 reforzado y plan v1 aprobados.
- Autorización de ejecución limitada a S01, recibida el 2026-09-24.
- `S01-GATE-01` ejecutado sobre una fuente autorizada e incompatible: CLI 0.149.0,
  JSONL con líneas inválidas y contadores agregados sin identidad por respuesta.
  Se necesita otra fuente exacta y autorización explícita. Sin prompts, contenido
  de logs ni importación retrospectiva.
- Cualificación satisfactoria de identidad de host, versión, formato y campos
  E-N1–E-N4 antes de escribir código.

## Validation

El gate no se sustituyó por inspección estática ni por fixtures. Tras aprobarse y
pasar, ejecutar las pruebas T2 indicadas, la regresión CE-v1 y los controles de
privacidad/diff definidos en el plan. Las fixtures no probarán integración real;
esa evidencia pertenece a S03, que sigue sin autorizarse.

## AI Profile Recommendation

- **Profile:** ADVANCED
- **Reasoning:** High
- **Reason:** persistencia recuperable, deduplicación, concurrencia y límites de
  privacidad requieren revisión cuidadosa. La configuración efectiva permanece
  no verificada; reevaluar el Model Gate inmediatamente antes de implementación
  si el gate de fuente pasa.
