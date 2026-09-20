# Session Preflight

REQUESTED PROFILE = perfil recomendado por Factory.
EFFECTIVE SESSION CONFIG = modelo y reasoning realmente usados por Codex; **unknown por defecto**.
Archivos/perfil/launcher describen intención o configuración de inicio, no prueban ejecución real.
No persistir el modelo activo como verdad del proyecto ni pedir introspección al agente.

Si la fase es normal y no requiere configuración concreta, continuar sin interrupción. Usar
preflight únicamente cuando el workflow dependa materialmente de ella, con Switch Benefit HIGH
y confirmación suficiente aún ausente en esta sesión/fase. No repetir por cada slice.

Ejemplo para una tarea que realmente dependa de BALANCED:

```text
AI SESSION PREFLIGHT

Perfil requerido:
BALANCED

Modelo esperado:
GPT-5.6 Terra
gpt-5.6-terra

Reasoning:
Medium

QUÉ HACER
1. ejecutá:
   /status
2. si muestra GPT-5.6 Terra / Medium:
   escribí:
   continuar
3. si muestra otra configuración:
   copiá o pegá el resultado de /status

ACCIÓN DEL USUARIO: requerida
```

Si `/status` no expone reasoning, no inferirlo: pedir `/model`, indicar modelo/reasoning exactos
y `continuar`; si tampoco puede verificarse una capacidad material, registrar
`unavailable-runtime-capability` y acción concreta. No pedir credenciales ni logs completos.
Confirmación del usuario vale para ese gate en esa sesión, no para aprobar plan/criterios.

Ante diferencia: evaluar suficiencia y costo real; Terra/High no demuestra BALANCED/Medium, pero
tampoco requiere detener trabajo normal. Para inicio exacto recomendar `asf balanced`;
para cambiar la sesión actual: `/model` → GPT-5.6 Terra (`gpt-5.6-terra`) → Medium → `continuar`.
Si el modelo no aparece, seguir fallback del catálogo con disponibilidad/costo explícitos.

Un gate material pendiente pone `User action required: true`. Sin gate ni otro impedimento,
el Finalization Gate obliga a continuar. Falta de modelo requerido se registra como runtime
limitation, nunca como bug del producto.
