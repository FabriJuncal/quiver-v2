# Criterios de aceptación — v1 aprobados

**Estado: aprobado el 2026-09-25 y verificado en H01/H02.** Fuente: pedido del usuario del
2026-09-25 y respuesta «solo trabajos nuevos». La taxonomía solicitada comprende
`feature`, `bug`, `test`, `explanation` y `documentation`.

| ID | Resultado observable | Verificación propuesta |
|---|---|---|
| H-01 | Cada trabajo nuevo queda ligado explícitamente a un proyecto y categoría antes de medir; un trabajo sin marca no recibe categoría inferida | Fixture de binding válido, inválido y previo sin marca |
| H-02 | La consulta histórica muestra trabajos y totales por categoría de un proyecto, sin mezclar proyectos | Dos proyectos y categorías con oráculo exacto |
| H-03 | Cada binding aporta solo su última revisión persistida; revisiones anteriores y consultas repetidas no duplican tokens, USD ni tiempo | Dos revisiones del mismo binding y dos intentos del mismo trabajo |
| H-04 | Tokens respetan contadores nativos y reportan cobertura incompleta o faltante; no se imputa consumo previo ni de otra sesión | Fixture con totales/cache/reasoning e incompleto |
| H-05 | Tiempo se presenta solo desde límites lifecycle explícitos, con unidad y etiqueta de tiempo transcurrido/no pausado; actividad real sigue unknown | Inicio/cierre, pausa, ausencia de límites y solapamiento |
| H-06 | USD reales aparecen solo con un importe directo y una referencia de evidencia explícitos; si faltan, `null`/unknown. No se usa el subtotal `synthetic` como gasto real | Sin evidencia, evidencia duplicada, importe inválido y declaración completa/parcial |
| H-07 | Consultar el histórico lee solo el ledger privado, sin abrir fuentes de sesiones ni guardar prompts, respuestas, código o argumentos | Fuente inaccesible después de snapshot; canarios y permisos |
| H-08 | La CLI ofrece JSON y texto con semántica coincidente, errores comprensibles e historial vacío explícito | Golden fixture y recorrido CLI |
| H-09 | El contrato S01–S03 permanece compatible y sus bindings previos no se recategorizan ni importan como trabajo nuevo | Regresiones afectadas y fixture legacy |
| H-10 | Kev puede sugerir una categoría desde un resumen breve enviado solo a un endpoint local; la categoría registrada requiere confirmación explícita y el histórico funciona sin Kev | Respuesta Kev artificial, endpoint no local rechazado, ausencia del servidor |

## Decisiones aplicadas

- **Granularidad:** el usuario propuso Kev para categorizar. D01 fija una
  categoría primaria por tarea/binding con sugerencia local opt-in de Kev y
  confirmación humana; la clasificación automática no asigna consumo por sí sola.
- **USD:** el usuario eligió USD real solo con evidencia; cuando falta, unknown.
  D01 fija un registro separado de importe directo declarado con referencia
  opaca de comprobante y cobertura explícita. No se consultan facturas ni se
  infieren costos de suscripción o tarifas comerciales.

## Testing ejecutado

T2 dirigido con fixtures artificiales y regresiones afectadas del observador:
46/46 pruebas `test_plan_usage.py` PASS el 2026-09-25. No
acceder a sesiones reales para implementar ni probar esta funcionalidad. No hay
benchmark, importe comercial ni prueba de facturación en este alcance.
