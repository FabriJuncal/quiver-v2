# Closure Brief — S01

## Criteria to verify

- AC-01, AC-02, AC-03, AC-04, AC-09, AC-10 y AC-12.
- Gate previo de fuente autorizado y compatible, registrado sin contenido sensible.

## Evidence to record

- Baseline, aprobación limitada de S01 y versión de los documentos aprobados.
- Resultado mínimo del gate: host, versión, formato y presencia/ausencia de E-N1–E-N4;
  nunca prompts ni una copia del log.
- Diff acotado, fixtures sintéticas, resultados de pruebas, digest de artefactos y
  comprobaciones de privacidad.

Gate `S01-GATE-01`, ejecutado el 2026-09-24 sobre una única fuente indicada y
autorizada expresamente por el usuario; la ruta privada no se persiste aquí:

- archivo regular, no symlink, 6.467.802 bytes; SHA-256
  `4ead70b80522f9f188d56f52f98b61148b319ba07e40d0c3b0930f5acd1b62bf` antes y
  después; tamaño, inode y mtime sin cambios durante la lectura;
- JSONL declarado por el sistema: 1.006 líneas, 4 vacías y 8 inválidas;
- `session_meta.cli_version`: `0.149.0`, anterior al contrato `0.156.1` revisado;
- 137 eventos `token_count`, con contadores enteros no negativos en
  `last_token_usage` y `total_token_usage`;
- cero objetos `token_usage_record`; los 137 `token_count` carecen de
  `response_id`, `thread_id`, `turn_id`, `session_id` y `root_turn_id`;
- resultado: **INCOMPATIBLE** con E-N1–E-N4 para atribución por respuesta. No se
  extrajeron valores de conversaciones, prompts, código, herramientas ni IDs.

Selección `S01-CANDIDATE-02`, ejecutada el 2026-09-24 bajo autorización
metadata-only; las rutas no se persisten:

- 84 JSONL inspeccionados solo por nombre/stat y `session_meta.cli_version`;
  84 declararon versión y seis fueron aparentemente compatibles con `>=0.156.1`;
- se seleccionó un único archivo regular de 21.707.940 bytes, con versión
  `0.156.1`; no se leyeron contadores, conversaciones, prompts, código,
  herramientas ni otros valores del registro;
- este resultado solo propone una fuente. No es un gate aprobado ni evidencia de
  compatibilidad: requiere autorización explícita y separada para `S01-GATE-02`.

Gate `S01-GATE-02`, intentado el 2026-09-24 y **NO ACEPTADO**:

- entre la selección y el gate, el tamaño pasó de 21.707.940 a 21.920.467 bytes y
  cambió su mtime; durante cada lectura individual permaneció estable, pero no a
  través de la frontera de selección/gate;
- el intento observó CLI `0.156.1`, registros por respuesta con los cinco IDs
  requeridos y contadores enteros no negativos. También observó líneas JSON no
  válidas, que serían anomalías manejables de S01, no uso atribuible;
- por drift de identidad/frescura, esos datos no cualifican el archivo como fuente
  de S01. No se importó, sumó, copió ni persistió ningún consumo ni contenido.

Selección `S01-CANDIDATE-03`, ejecutada el 2026-09-24 bajo autorización
metadata-only reforzada; las rutas no se persisten:

- 84 JSONL inspeccionados solo por nombre, `session_meta.cli_version` y dos `stat`
  separados; 84 declararon versión, seis fueron aparentemente compatibles con
  `>=0.156.1` y cinco permanecieron estables tras excluir el candidato que derivó;
- se propuso un único archivo regular, alias `S01-CANDIDATE-03`, con CLI `0.156.1`,
  22.548.201 bytes y dos `stat` coincidentes; no se leyeron contadores,
  conversaciones, prompts, código, herramientas ni otros valores del registro;
- la estabilidad por metadatos no prueba E-N1–E-N4. Requiere autorización explícita
  y separada para `S01-GATE-03` y no habilita implementación.

Gate `S01-GATE-03`, detenido el 2026-09-24 **antes de leer contadores**:

- el primer `stat` del gate informó 24.469.346 bytes, frente a 22.548.201 bytes
  registrados al seleccionar `S01-CANDIDATE-03`;
- la condición autorizada exigía detenerse si el archivo cambiaba respecto del
  baseline. No se inspeccionaron formato, contadores, identificadores ni contenido;
- resultado: **NO EJECUTADO POR DRIFT**. La evidencia indica que dos `stat` cercanos
  solo probaron una pausa breve de escritura, no que la fuente estuviera cerrada;
- no se implementó código. El plan v1 ya contempla una lectura incremental hasta un
  tamaño capturado y detección de reescritura del prefijo; usar esa regla para esta
  fuente requiere una autorización nueva porque el gate 03 exigía inmovilidad desde
  la selección.

Gate `S01-GATE-04`, ejecutado el 2026-09-24 y **APROBADO**:

- se capturó un prefijo de 24.888.278 bytes; la identidad del archivo y el hash del
  mismo prefijo coincidieron antes y después, aunque la fuente pudiera seguir anexando;
- CLI `0.156.1`, un `session_meta` y 403 `token_usage_record` observados;
- cero errores de parseo/versión, identificadores o forma de contadores;
- cada registro presentó `response_id`, `thread_id`, `turn_id`, `session_id` y
  `root_turn_id`; los bloques de uso separaron input, cached input, output,
  reasoning, cache-write y total;
- no se persistieron ruta, hash, IDs ni valores de consumo del archivo real. No se
  importó historial ni se leyó contenido conversacional, código o herramientas.

## Implementation evidence

- `scripts/lib/plan_usage.py`: binding previo, modo off/on, lectura por prefijo,
  normalización, deduplicación, ledger/checkpoint atómicos, lock y reporte JSON/texto;
- `templates/usage/MEASUREMENT.schema.json`: contrato del reporte S01;
- `docs/guides/PLAN_USAGE.md`: recorrido y límites;
- `tests/test_plan_usage.py`: fixtures exclusivamente sintéticas.

Cobertura de criterios:

- AC-01: activación/disable explícitos; disabled no abre la fuente;
- AC-02: binding de proyecto, requirement, plan digest, ejecución, intento, slice y
  sesión antes del uso; sesión compartida rechazada;
- AC-03: semántica input/cache/output/reasoning/cache-write sin doble conteo;
- AC-04: dedup, reimportación, lock, crash antes/después de replace y dos planes;
- AC-09: ledger privado 0600, symlinks/worktree rechazados y canarios no persistidos;
- AC-10: reporte JSON/texto con procedencia, anomalías y unknowns;
- AC-12: forks/children, formato/versiones no soportadas y truncado fallan cerrados.

## Tests to report

- `python3.14 -I -B tests/test_plan_usage.py -v`: 20/20 OK — T01–T04,
  T06, T08–T10 y recorrido CLI sintético;
- `python3.14 -I -B tests/test_context_economy.py`: 19/19 OK;
- `python3.14 -B -m unittest discover -s tests -v`: 173/173 OK;
- `bash scripts/check-release.sh`: PASS;
- compilación Python, esquema JSON, privacidad dirigida y `git diff --check`: PASS.

## Deviations

- Dos intentos iniciales del scanner selectivo informaron cero registros por una
  expresión demasiado literal. No se interpretaron como fallo del contrato; no
  persistieron contenido y el prefijo siguió estable. El selector corregido produjo
  los conteos y controles del gate 04 indicados arriba.
- Los gates 01–03 no fueron reutilizados como evidencia positiva; el gate 04 resolvió
  la fuente activa mediante la frontera incremental ya prevista por el plan.
- La revisión fue inline y no independiente porque delegación y otra sesión estaban
  fuera de alcance; veredicto APROBADO CON NOTAS en `../../05_IMPLEMENTATION_REVIEW.md`.
- La configuración efectiva de modelo/reasoning y el consumo de esta implementación
  no fueron observables; permanecen unknown.

## Risks / pending

- S01 está completa solo como recorrido offline. No demuestra captura real del flujo
  habitual ni permite atribuir retroactivamente el consumo observado en el gate.
- S02/S03, precios, lifecycle y recorrido real permanecen fuera de alcance.
- Python 3.11 no estaba instalado localmente; Python 3.14.4 pasó. CI mantiene Python
  3.11 como entorno declarado, pero no se ejecutó CI remoto.
