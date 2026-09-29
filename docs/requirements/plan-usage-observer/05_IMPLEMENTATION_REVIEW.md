# Implementation Review — S01

Fecha: 2026-09-24. Alcance: cambios locales no commiteados de S01 sobre HEAD
`2b92c74602bf244e9a3e03829e5c07f2b233e8a4`; no incluye los 72 archivos
preexistentes de discovery y optimización de Skills.

## Modalidad y evidencia

Review inline del coordinador contra criterios v1, D01, plan v1, diff real y pruebas.
No fue independiente: la delegación y otra sesión de review estaban expresamente fuera
del alcance. Para N2 el review dedicado es recomendado, no obligatorio. La integración
real continúa separada en S03.

Archivos revisados:

- `scripts/lib/plan_usage.py`
- `tests/test_plan_usage.py`
- `templates/usage/MEASUREMENT.schema.json`
- `docs/guides/PLAN_USAGE.md`
- `FILE_INDEX.md`

Validación final revisada:

- `python3.14 -I -B tests/test_plan_usage.py -v`: 20/20 OK;
- `python3.14 -I -B tests/test_context_economy.py`: 19/19 OK;
- `python3.14 -B -m unittest discover -s tests -v`: 173/173 OK;
- `bash scripts/check-release.sh`: PASS;
- compilación Python, sintaxis del esquema, privacidad dirigida y `git diff --check`: PASS.

## Findings y ronda dirigida

| ID | Clase | Hallazgo | Corrección | Estado |
|---|---|---|---|---|
| F01 | OBLIGATORIO | Los symlinks en antecesores de fuente/ledger no se rechazaban | Validación explícita de antecesores y fixture | CERRADO |
| F02 | OBLIGATORIO | JSON con claves duplicadas podía aceptar una interpretación ambigua | Parser fail-closed para fuente y ledger; fixture | CERRADO |
| F03 | OBLIGATORIO | `requirement_ref` no exigía forma relativa canónica | Validación de referencia y fixture | CERRADO |
| F04 | OPCIONAL | Import no utilizado y falta de recorrido CLI en pruebas | Import retirado y prueba CLI completa | CERRADO |

Se utilizó una única ronda dirigida. La re-review focalizada y la suite global no
dejaron findings obligatorios abiertos.

## Veredicto

**APROBADO CON NOTAS.** S01 cumple su recorrido offline y sus criterios asignados.
No demuestra observación del flujo habitual, costos ni tiempos reales; esos hitos
pertenecen a S02/S03. Modelo y razonamiento efectivos permanecen NO VERIFICADOS.

---

# Implementation Review — S02

Fecha: 2026-09-24. Alcance: extensión local de S02 sobre la implementación S01 ya
cerrada; lifecycle, reporte v2, revisiones, snapshots sintéticos, esquema, guía y
fixtures. S03, sesiones reales, precios comerciales y configuración quedan excluidos.

## Modalidad y evidencia

Review inline contra criterios v1, D01, plan v1, artefactos S02 y archivos efectivos.
No fue independiente: el usuario prohibió delegación y autorizó únicamente la ejecución
de S02. Para N2 el review dedicado es recomendado, no obligatorio. La configuración
efectiva de modelo/reasoning permanece NO VERIFICADA.

Validación revisada:

- `python3.14 -I -B tests/test_plan_usage.py PlanUsageS02 -v`: 13/13 OK;
- seis regresiones S01 directamente afectadas: 6/6 OK;
- compilación Python, sintaxis de ambos esquemas y `git diff --check`: PASS;
- inspección dirigida de canarios/rutas/credenciales: solo fixtures sintéticas esperadas.

No se repitieron gates S01, CE-v1, suite global, check-release ni CI remoto porque el
encargo pidió evitar pruebas cerradas salvo regresiones afectadas.

## Findings y ronda dirigida

| ID | Clase | Hallazgo | Corrección | Estado |
|---|---|---|---|---|
| F05 | OBLIGATORIO | Un snapshot sin respuestas tasables producía `0.000000000` | `amount`/naturaleza quedan unknown cuando ninguna respuesta tiene identidad/tarifa aplicable | CERRADO |
| F06 | OBLIGATORIO | El API Python previo de `report()` devolvía v2 por defecto | Default programático v1 preservado; CLI/S02 solicitan v2 y ambos esquemas se verifican | CERRADO |
| F07 | OBLIGATORIO | `usage_observed=true` no se contrastaba con un registro importado | Outcomes cruzados por `response_id`; ausencia queda incompleta y advertida | CERRADO |

Una ronda dirigida cerró F05–F07; la re-review focalizada no dejó obligatorios abiertos.

## Veredicto

**APROBADO CON NOTAS.** S02 cumple el recorrido offline autorizado y los criterios
AC-04–AC-08/AC-10 asignados, con tarifas exclusivamente sintéticas. No verifica tiempos,
identidad, costos ni integración de una sesión habitual; esa evidencia pertenece a S03.

---

# Implementation Review — S03

Fecha: 2026-09-25. Alcance: ajuste local S03 de `bind`/`refresh` para turnos raíz
sucesivos, pruebas y guía sobre S01/S02 cerradas; binding privado, T13 y reporte real.
La base Git continúa en HEAD `2b92c74602bf244e9a3e03829e5c07f2b233e8a4`;
la implementación completa sigue untracked. No se atribuyen cambios preexistentes
de discovery o codex-skills-optimization a este review.

## Modalidad y evidencia

Review inline contra criterios AC-01/09/11/12, plan v1, contrato de privacidad,
código efectivo, fixtures y conciliación independiente de fuente/ledger. No fue
independiente: el usuario prohibió delegar. Para N2 un review dedicado es
recomendado, no obligatorio. Modelo/reasoning efectivos NO VERIFICADOS; el perfil
ADVANCED/High es recomendación normativa, no evidencia de runtime.

- El opt-in conserva session/thread y omite el turno raíz del binding; default S01
  inalterado. El test de thread ajeno y la suite offline pasaron 35/35.
- Fuente `S03-SOURCE-01`: `session_meta` indica CLI 0.156.1, originator `codex-tui`
  y source `cli`; no se inspeccionaron conversaciones ni otras sesiones.
- T13 tras la explicación de la guía: 6 IDs de respuesta y todos los contadores
  iguales fuente/ledger, total 254927; siete registros del turno binding omitidos,
  cero duplicados, cero registros ajenos, sin anomalías de importación.
- El refresh verificó identidad y hash del prefijo anterior; el comparador comprobó
  identidad y hash del checkpoint final. El original fue solo leído por el observador.
- Ledger/directorio privados `0600`/`0700`, revisión v2 n.º 1 persistida;
  sin claves de prompt/contenido/argumentos/credenciales. Off sin lectura de fuente
  cubierto por la suite.

## Findings

| ID | Clase | Hallazgo | Estado |
|---|---|---|---|
| F08 | OPCIONAL | El intervalo contiene la aclaración previa además de la tarea; el reporte no las separa | Límite informado; no atribuir el total solo a la tarea |
| F09 | OPCIONAL | La vista textual concatena `s` a `unknown` y muestra `unknowns` para tiempo sin límites | Cosmético; JSON conserva `null`, sin efecto en T13 |

Sin findings obligatorios ni ronda dirigida de corrección en S03. No se reabrieron
F01–F07 ni los gates cerrados.

## Veredicto

**APROBADO CON NOTAS.** La captura real prospectiva y la conciliación T13 funcionan
en el intervalo/fuente autorizados. El reporte permanece `incomplete` porque no se
observó fin técnico ni tarifa aplicable. Modelo, tier, pago, USD, tiempos y aceptación
no se infieren; no se declara cobertura de otras sesiones, hosts o facturación.
