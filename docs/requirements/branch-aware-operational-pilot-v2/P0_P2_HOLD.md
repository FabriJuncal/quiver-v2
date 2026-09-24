# P0–P2 hold — benchmark branch-aware v2

Fecha: 2026-09-23. Estado: **hold resuelto; P2 ajustada completada antes de generar respuestas**.

## Resultado verificable

- P0: autorización P0–P2 registrada, root privado externo creado y ningún agente delegado.
- P1: inventario read-only completo (95 refs; 82/82 tips; cero errores), scope fresco y
  contextos `CURRENT`/`IOS_SIBLING` verificados con `check`.
- Integridad before/after: PASS para HEAD, refs, status, diffs, índice y tres untracked
  preexistentes del piloto.
- P2: detenido antes de crear answer key, prompt congelado, paquetes A/B, sello temporal o
  respuestas.

## Condición de detención E-SENS-01

Uno de los archivos estáticos seleccionados contiene un literal con apariencia de credencial
que no estaba previsto por el plan. No se reproduce en este documento, no se incorporó a un
prompt y no se publicó. Los manifests originales y el incidente redacted se preservan en la
evidencia privada externa.

El detector preexistente de contexto no lo rechazó; eso no autoriza a tratarlo como no
sensible. La clasificación definitiva del literal sigue siendo `unknown`.

## Límite del hold original

No se modificó el repositorio piloto ni Quiver fuera de este requirement/estado. No se
generaron sesiones P3 ni se delegó trabajo. En ese punto se requirió una decisión humana:
autorizar derivados seguros, seleccionar otro scope o dejar detenido el benchmark.

## Resolución P2 ajustada

El usuario autorizó P2 ajustada. Los dos contextos pasaron nuevamente el `check` oficial y
el baseline P1 coincidió en rama, HEAD, refs, índice, status, diffs y archivos no versionados.

E-SENS-01 se resolvió para el benchmark mediante `excluded-by-selection`: la fuente afectada
no aporta bytes a los paquetes, los originales permanecen preservados y el literal no fue
copiado ni validado. Su clasificación real continúa `unknown`.

Resultado final:

- answer key cerrado con `K=10`, cinco unknowns requeridos y cinco claims prohibidos;
- prompt, rubric, schema y paquetes A/B de 10890 y 17630 bytes;
- derivación exacta, scan sensible, key, presupuesto y negativos T2 reforzado: PASS;
- `PRE_RESPONSE_SEAL` SHA-256:
  `4f1ed72a7c8109e0a1f740beb46fa65a67b4bdd0cda770e0568af70d36ebb39e`;
- cero respuestas y cero corridas P3.

Se preservaron los intentos privados previos al sello final. Uno excedió el presupuesto y
otro permitió detectar que los fragmentos se estaban serializando en lugar de conservarse
byte a byte; la validación final confirmó la corrección. P3–P6 siguen sin autorización.
