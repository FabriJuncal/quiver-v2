# Decisión propuesta — Tarea del benchmark

Estado: **pendiente de aprobación humana**.

## Alternativas

| Opción | Tarea | Tiempo | Complejidad | Consumo IA | Principal trade-off |
|---|---|---:|---:|---:|---|
| A — recomendada | Diseñar una migración sin código para llevar la integración de notificaciones push de `IOS_SIBLING` desde la API anterior a la API usada por `CURRENT`, preservando diferencias propias de la variante. | Medio, 4–6 h para tres pares y scoring | Media | Medio: seis respuestas comparables | Tiene answer key estático fuerte; no prueba que el SDK funcione en dispositivo. |
| B | Diseñar la incorporación del flujo de eliminación de cuenta en una variante que no lo contiene usando precedentes existentes. | Bajo/medio, 2–4 h | Baja/media | Bajo/medio | 72 tips contienen el flujo y 10 no; la activación y contrato backend siguen desconocidos. |
| C | Auditar paridad funcional completa entre `CURRENT` y `IOS_SIBLING`. | Alto, 1–2 días | Alta | Alto | La pareja difiere en 51 rutas; mezcla demasiadas causas y puede agotar contexto sin aislar el valor del router. |

## Recomendación

Seleccionar **A**. El snapshot muestra tres generaciones incompatibles de la API de
notificaciones: 55 tips usan `setAppId`, 10 usan `startInit` y 17 usan `initialize`.
La pareja elegida comparte generación Angular pero difiere en plugin/API; cuatro de los
cinco archivos acotados son distintos. Esto produce hechos verificables, omisiones
observables y errores de atribución claros bajo un presupuesto pequeño.

La tarea exacta será:

> Producir un plan de cambio sin editar código para migrar las notificaciones push de
> `IOS_SIBLING` a la API moderna observada en `CURRENT`; identificar archivos afectados,
> incompatibilidades, valores que no deben copiarse, validaciones necesarias, límites de
> evidencia y rollback.

## Decisiones de diseño

- Comparar contexto, no calidad de implementación: no se instala ni ejecuta la app.
- Usar aliases públicos; refs/OID exactos quedan en evidencia privada.
- Separar answer key, prompts, respuestas y mapa ciego.
- Usar tres pares; una sola respuesta no alcanza para evaluar variabilidad del modelo.
- No exigir ahorro de tokens. El éxito primario es mayor precisión/cobertura con el mismo
  límite de bytes; costo y tokens son métricas secundarias cuando sean observables.

## AI Strategy propuesta

- Planificación: **ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High**.
- Ejecución mecánica: **BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium**;
  fallback **GPT-5.6 Sol (`gpt-5.6-sol`) / Medium**.
- Review N2: **ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High**; fallback
  **GPT-5.6 Terra (`gpt-5.6-terra`) / High o XHigh**.
- No usar GPT-6 Astra sin insuficiencia demostrada.

`REQUESTED PROFILE` no prueba `EFFECTIVE SESSION CONFIG`; esta última se registra por
corrida solo si el runtime la expone.
