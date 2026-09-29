# Implementation Review — A01–A03

2026-09-25. Modalidad: self review inline N2, sin delegación ni review dedicado.
Alcance revisado: recibos de actividad, extensión opt-in del ledger, cliente Kev
con transporte artificial, historial v2, schema, guía y fixtures. La revisión se
hizo contra archivos locales no commiteados identificados en [EVIDENCE.md](EVIDENCE.md);
el worktree tenía cambios ajenos preservados.

**Veredicto: APROBADO CON NOTAS.** No hay findings obligatorios abiertos ni
rondas de corrección formal. La estrategia heredada BALANCED/Medium fue
proporcional: N2, contratos locales reversibles y oráculos discriminantes. El
modelo/reasoning efectivos siguen no verificados.

| ID | Severidad | Resultado |
|---|---|---|
| F01 | OBLIGATORIO | Cerrado antes del review: la exclusividad ahora exige `manifest_complete`; una edición aislada no absorbe tokens de una respuesta potencialmente mixta. T02/T04 PASS. |
| F02 | OBLIGATORIO | Cerrado antes del review: cada `response_id` se agrega una sola vez; múltiples actividades lo llevan a `mixed`, cobertura incompleta a `unassigned`. T04/T09 PASS. |
| F03 | OBLIGATORIO | Cerrado antes del review: Kev opera con señales `noul` independientes, usa loopback, no guarda resumen y marca la inferencia `unvalidated`. T06–T08/T13 PASS. |
| F04 | OBLIGATORIO | Cerrado antes del review: salida v2 lee ledger privado y deja USD/tiempo activo unknown. Stale revisions, compatibilidad v1 y fuente artificial eliminada cubiertas por T05/T10–T12 y 46 regresiones PASS. |
| F05 | OPCIONAL | A04 podría reemplazar el generador determinista por un archivo materializado de 300 ejemplos. No altera sus cantidades ni digest en A01–A03; diferido hasta el entorno Kev real. |

No se detectó acceso a sesiones reales, instalación, cambio global, publicación o
commit. La capacidad real de eventos del host sigue como hecho no verificado.

## Addendum A04 — 2026-09-25

Modalidad: self review inline N2, sin delegación. Alcance revisado: ejecución
T14 contra el endpoint loopback y corpus artificial autorizado, sin cambios de
código. **Veredicto A04: REQUIERE AJUSTES.**

| ID | Severidad | Resultado |
|---|---|---|
| F06 | OBLIGATORIO para A04 | El timeout pasó de 5 a 180 s y la regresión afectada pasó. Kev entregó un caso en 176445.453 ms, pero Metal procesa una solicitud por vez; el corpus completo se estima en 14.7 h y no es una ejecución T14 operativa. |
| F07 | OBLIGATORIO para A04 | `kev_classify` descarta `usage`. Sin cambiar esa interfaz no puede medirse el consumo propio de Kev exigido por T14. |

La corrección y el diagnóstico autorizados se completaron. Un candidato posterior
debe conservar corpus y umbrales, registrar endpoint/checkpoint y no usar datos
reales. A05 permanece fuera de alcance.
