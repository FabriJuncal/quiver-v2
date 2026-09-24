# Decisión aprobada — Diseño del benchmark v2

Estado: **aprobada por el usuario el 2026-09-23**. Ejecución no autorizada.

## Decisión

Mantener la tarea conceptual acotada de v1 —planificar sin código una migración de
notificaciones push entre `CURRENT` e `IOS_SIBLING`—, pero ejecutar un experimento nuevo.
No se reutilizan respuestas, puntajes ni conclusiones de v1. El scope real, refs y evidencia
se capturan nuevamente después de autorizar ejecución; si ya no soportan la tarea, P1 se
detiene y vuelve a decisión humana en lugar de forzar el benchmark.

## Diseño elegido

- tres pares independientes con orden `AB`, `BA`, `AB`;
- presupuesto máximo de 131072 bytes por corrida;
- answer key cerrado y validado antes de respuestas;
- respuesta estructurada con claims atómicos;
- hash chain local desde scope hasta scoring;
- scoring ciego por un agente nuevo, solo si la delegación se autoriza por separado;
- review N2 independiente posterior, con una sola ronda dirigida;
- perfil de testing aprobado **T3** por el fallo contractual previo, la privacidad y la
  necesidad de probar condiciones negativas/recuperación. El riesgo funcional sigue N2.

## Alternativas descartadas

| Alternativa | Motivo |
|---|---|
| Re-puntuar v1 | El key no puede cerrarse retroactivamente sin observar las respuestas. |
| Usar prosa libre y segmentarla al puntuar | Permite que el denominador de precisión dependa del scorer. |
| Confiar solo en mtimes | No liga criptográficamente el contenido y no prueba orden temporal independiente. |
| Cambiar de tarea ahora | Ampliaría el alcance sin evidencia fresca del piloto y reduciría comparabilidad conceptual. |

## AI Strategy — routing-v1

- **Planning v2 solicitado:** ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High.
- **Fallback solicitado:** GPT-5.6 Terra (`gpt-5.6-terra`) / High o XHigh.
- **Motivo observable:** el fallo de v1 fue difícil de detectar antes del scoring y afecta
  la validez completa del experimento; el costo de un segundo protocolo inválido es alto.
- **Verificación prevista:** trazabilidad criterio → paso → validación, fórmulas cerradas,
  casos borde y self review documental. Esto no confirma identidad del runtime.
- **Contexto:** suficiente para planificar a partir del cierre v1 y contratos locales; no se
  leyó el piloto porque esa acción pertenece a P1 y no está autorizada ahora.
- **Switch Benefit:** HIGH para esta fase crítica; el usuario solicitó la configuración.
- **Base:** `policy`, no `measured`.
- **Effective session config:** `unknown`; el runtime no expone prueba verificable.

Perfiles futuros propuestos, sujetos a aprobación y preflight de cada fase:

- P0–P3 y P4 mecánico: BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium;
- P5 review crítico: ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High; fallback GPT-5.6
  Terra (`gpt-5.6-terra`) / High o XHigh;
- GPT-6 Astra: no justificado.

El perfil de planning pedido no autoriza cambiar el modelo ni demuestra que el cambio haya
ocurrido. Cualquier mismatch efectivo dentro de un par invalida ese par si no puede repetirse.
