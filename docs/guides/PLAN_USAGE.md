# Medición offline de uso por plan

`scripts/lib/plan_usage.py` implementa el recorrido offline de S01/S02. Es opt-in:
primero crea un binding entre proyecto, requirement, revisión de plan, ejecución,
intento y una sesión raíz dedicada; después importa únicamente registros nativos
`token_usage_record` posteriores a esa frontera.

El ledger debe ser un JSON privado fuera del worktree. La fuente es de solo lectura.
El observador conserva identificadores y contadores permitidos, evita duplicados por
respuesta y actualiza eventos y checkpoint en un único reemplazo atómico protegido
por un lock local. No guarda prompts, respuestas, código ni argumentos de herramientas.

S02 agrega eventos lifecycle explícitos, tiempo de pared derivado de límites provistos,
revisiones persistidas y subtotales con snapshots tarifarios marcados `synthetic`.
No infiere actividad desde silencios, tokens por segundo o timestamps de la fuente.

## Recorrido base

Usar Python 3.11 o posterior. Los valores siguientes son ilustrativos; no reutilizar
IDs ni rutas sin un binding real explícito:

```text
python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json bind \
  --project-id proyecto --requirement-ref docs/requirements/ejemplo/STATE.md \
  --plan-version v1 --plan-digest SHA256 --execution-id execution-01 \
  --attempt-id attempt-01 --slice-id S01 --source /ruta/privada/rollout.jsonl \
  --source-version 0.156.1 --session-id SESSION --thread-id THREAD \
  --root-turn-id ROOT_TURN

python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json refresh \
  --binding-id BINDING_ID

python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json report \
  --binding-id BINDING_ID --format text
```

`disable` apaga el binding antes de abrir la fuente. Un error de medición devuelve
exit 2 y no debe encadenarse como condición de éxito del trabajo observado.

Para una validación prospectiva S03 en una sesión con varios turnos raíz, el binding
puede agregar `--allow-root-turn-change`. Ese modo conserva la sesión y el thread
dedicados, omite el turno en que se crea el binding y admite los turnos raíz posteriores
del mismo thread. Un thread distinto sigue excluido. Activarlo solo para una fuente
real autorizada y con una tarea futura identificada; no importa uso anterior.

## Lifecycle y tiempos observables

Los timestamps deben incluir zona horaria. `technical_closed` y `accepted` son eventos
separados; `accepted` exige una referencia relativa canónica. Pausa/reanudación ajustan
`unpaused_seconds`, pero ese valor no se llama actividad. `active_time_seconds`,
`wait_time_seconds` y `agent_time_seconds` permanecen `null`/unknown porque no existe
una fuente que los observe. Intervalos paralelos tampoco se suman como trabajo total.

```text
python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json lifecycle \
  --binding-id BINDING_ID --event-id start-01 --kind started \
  --at 2026-09-24T10:00:00-03:00

python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json lifecycle \
  --binding-id BINDING_ID --event-id close-01 --kind technical_closed \
  --at 2026-09-24T10:10:00-03:00

python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json lifecycle \
  --binding-id BINDING_ID --event-id accept-01 --kind accepted \
  --at 2026-09-24T10:12:00-03:00 \
  --reference docs/requirements/ejemplo/STATE.md
```

`failed`, `retry` y `cancelled` registran outcomes explícitos. `failed`/`retry`
requieren `--response-id`; `--usage-observed` confirma que existe el registro de uso y
`--usage-unknown` deja advertencia/incompleto. Un evento agregado fuera de orden se
marca tardío y debe materializarse en una nueva revisión, sin sobrescribir la anterior.

## Tarifas sintéticas y revisiones

El archivo de tarifas se selecciona explícitamente y solo acepta `kind: synthetic`,
USD por millón de tokens y decimales textuales. Ejemplo artificial:

```json
{
  "snapshot_id": "fixture-rates-v1",
  "kind": "synthetic",
  "currency": "USD",
  "unit": "per_1m_tokens",
  "rates": [{
    "effective_model": "fixture-model",
    "service_tier": "fixture-tier",
    "input_tokens": "1",
    "cached_input_tokens": "0.5",
    "output_tokens": "2"
  }]
}
```

```text
python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json register-rates \
  --rates-file /ruta/fixture-rates.json

python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json snapshot \
  --binding-id BINDING_ID --rate-snapshot-id fixture-rates-v1 --format json
```

El cálculo usa `Decimal`: input no cacheado, cached input y output. Reasoning es un
subset de output y no se suma otra vez. Un cache-write sin tarifa aplicable deja esa
respuesta sin precio. Si solo algunas respuestas coinciden, `amount` es un subtotal
sintético y `usd` continúa unknown; `billed_amount` siempre es unknown. La serie de
revisiones fija su snapshot tarifario y conserva snapshots anteriores.

`report --report-version 1` conserva el contrato S01. La CLI muestra v2 por defecto;
`snapshot` persiste una revisión v2 y `report --revision N` recupera una anterior.

## Límites vigentes

- fuente soportada: JSONL plano con contrato `0.156.1` cualificado;
- sesión raíz inline y dedicada; forks, children, sesiones compartidas y formatos
  comprimidos quedan excluidos e incompletos;
- el reporte conserva modelo efectivo, tier, modalidad de pago, USD o tiempo como
  unknown cuando falta evidencia allowlisted/aplicable;
- las tarifas comerciales, facturas, conciliación y precios online están rechazados
  por contrato; un subtotal sintético no representa gasto ni modalidad de cobro;
- el éxito de fixtures no demuestra integración con el flujo habitual. Esa prueba
  pertenece a S03 y necesita autorización separada.

El esquema vigente v2 está en `templates/usage/MEASUREMENT.schema.json`; el contrato
preservado v1 está en `templates/usage/MEASUREMENT.v1.schema.json`.

## Histórico prospectivo por proyecto y tipo de trabajo

Para trabajos nuevos, agregar a `bind` una categoría confirmada y un ID opaco:
`--work-kind feature --work-id feature-123`. Las categorías permitidas son
`feature`, `bug`, `test`, `explanation` y `documentation`. Ambos argumentos deben
estar presentes o ausentes. Un trabajo mixto puede usar el mismo `work-id` en
bindings separados por categoría; no se reparte consumo dentro de una respuesta.
Los bindings anteriores sin estas marcas no aparecen en el histórico y no se
recategorizan. El historial se arma desde la **última revisión v2 persistida**
de cada binding marcado; ejecutar `snapshot` después de `refresh` y de los
eventos lifecycle pertinentes.

```text
python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json history \
  --project-id proyecto --format text
```

`history --format json` ofrece trabajos, categorías, totales observados y
cobertura. Lee solo el ledger, no la fuente JSONL. Tokens sin snapshot no se
suman y se informan como faltantes; un `refresh` o evento lifecycle posterior al
último snapshot aparece como `stale_reports` hasta persistir una nueva revisión.
El tiempo muestra segundos transcurridos y
no pausados solo si existen límites explícitos; no equivale a actividad y la
suma de intervalos simultáneos no es tiempo único de proyecto.

El campo USD real permanece unknown salvo una declaración **directa por binding**
con ID opaco de comprobante, SHA-256 del comprobante e importe textual positivo.
El comando no abre ni verifica el comprobante: registra una afirmación del usuario
con procedencia `user_attested_direct_charge`, evita reutilizar el mismo ID y
conserva el importe inmutable. `--complete-for-binding` afirma que el cargo cubre
todo ese binding; sin esa bandera el importe es solo subtotal conocido. Si algún
binding carece de evidencia completa, el total USD sigue unknown.

```text
python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json record-usd \
  --binding-id BINDING_ID --amount 1.25 --evidence-id invoice-line-1 \
  --evidence-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  --complete-for-binding
```

Kev es opcional. Con un servidor Kev local ya disponible, `suggest-kind` lee
un resumen breve desde stdin, pregunta por una opción entre las cinco categorías
y devuelve una sugerencia con probabilidades. No guarda el resumen ni escribe
una categoría en el ledger; confirmar la etiqueta al ejecutar `bind`. Solo acepta
HTTP en loopback con puerto explícito y no instala ni descarga Kev.

```text
printf 'Actualizar la guía de uso' | python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json suggest-kind \
  --endpoint http://127.0.0.1:8009
```

## Histórico automático por actividad (v2 offline)

Para un trabajo que combine desarrollo, tests y documentación, crear un binding
con `--activity-mode --work-id trabajo-123`, sin `--work-kind`. La categoría ya
no se solicita a la persona que inicia el trabajo. El ejecutor local emite un
recibo mínimo al terminar cada acción soportada: ID de respuesta, ID de operación,
tipo de acción, roles de archivo, límites temporales, outcome y la marca de que
el manifest de acciones está completo. No contiene rutas absolutas, diffs,
prompts, resúmenes, argumentos de comandos ni contenido de archivos.

Después de importar la respuesta, el recibo se puede entregar por stdin a
`activity-record`; el ejemplo es artificial y no corresponde a una sesión real:

```text
python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json bind \
  --project-id proyecto --requirement-ref docs/requirements/ejemplo/STATE.md \
  --plan-version v2 --plan-digest SHA256 --execution-id execution-01 \
  --attempt-id attempt-01 --slice-id A01 --source /ruta/privada/rollout.jsonl \
  --source-version 0.156.1 --session-id SESSION --thread-id THREAD \
  --root-turn-id ROOT_TURN --activity-mode --work-id trabajo-123

printf '%s\n' '{"activity_id":"docs-1","operation_id":"op-docs-1","response_id":"RESPONSE","actions":[{"kind":"documentation","file_roles":["guide"]}],"manifest_complete":true,"started_at":"2026-09-25T10:00:00Z","ended_at":"2026-09-25T10:00:05Z","outcome":"completed","tool_seconds":2}' | \
  python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json activity-record \
  --binding-id BINDING_ID

python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json activity-snapshot \
  --binding-id BINDING_ID --format text

python3.11 -I -B scripts/lib/plan_usage.py \
  --project-root /ruta/proyecto --ledger /ruta/privada/usage.json activity-history \
  --project-id proyecto --format text
```

Una respuesta se cuenta una sola vez. Si está vinculada a varias actividades,
va a `mixed`; si no tiene recibo completo o no existe relación exacta con su
ID nativo, va a `unassigned`. Kev puede devolver indicadores automáticos para
una actividad de código, pero la inferencia queda marcada `unvalidated` hasta
A04. Sus probabilidades no reparten tokens y sus propios tokens no se suman al
consumo del agente. El tiempo es de pared por actividad; tiempo activo de IA y
USD por actividad permanecen unknown sin evidencia directa. A01–A03 no prueban
que el host emita estos recibos automáticamente ni que Kev clasifique bien en
un servidor real: esas verificaciones son A04 y A05.
