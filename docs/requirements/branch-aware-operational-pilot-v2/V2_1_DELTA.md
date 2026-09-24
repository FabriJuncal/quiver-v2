# Delta documental aprobado — Benchmark branch-aware v2.1

Fecha: 2026-09-23. Estado: **aprobado por el usuario el 2026-09-23; ejecución no autorizada**.

Este delta simplifica v2 sin ejecutar P2–P6. Los documentos v2 permanecen como historial;
este archivo es el contrato normativo para la continuación. P0/P1 se
conservan como evidencia histórica y deben pasar un control focalizado de frescura antes de
ser usados nuevamente.

## 1. Pregunta y alcance mínimo

Pregunta única:

> ¿La evidencia estática de otra variante mejora, de manera repetible, un plan de migración
> sin código frente a usar solamente el snapshot actual?

Se mantienen dos modalidades, tres pares nuevos en orden `AB`, `BA`, `AB`, el mismo prompt,
formato, límite máximo de 131072 bytes y configuración solicitada dentro de cada par. Las
respuestas v1 quedan excluidas de inputs, scoring y baseline cuantitativo.

Se retiran como requisitos: inventario/cohortes globales dentro de los paquetes, segundo
recall, disciplina de unknown como métrica separada, retrabajo estimado, tiempo humano,
deduplicación, medianas/rangos obligatorios y ahorro de tokens/costo. Estos valores solo se
informan si ya son observables y útiles; nunca son gates.

## 2. Criterios de aceptación aprobados

| ID | Criterio observable |
|---|---|
| V21-AC01 | Se usan seis respuestas nuevas; ningún contenido, puntaje o conclusión de v1 entra al experimento. |
| V21-AC02 | Antes de continuar P2, los dos manifests de contexto pasan `check` y HEAD, refs/OID y overlay coinciden con el baseline P1. Si fallan, se detiene y se refresca P1; no se repite el inventario global cuando no hay drift. |
| V21-AC03 | A y B contienen solo fragmentos derivados relevantes. Cada fragmento registra alias, OID, ruta, blob/hash fuente, selección, regla de derivación, hash derivado y bytes. Los paquetes no contienen E-SENS-01 ni otro material detectado como sensible. |
| V21-AC04 | El answer key sellado antes de P3 define un conjunto cerrado y no vacío de hechos atómicos `F`, unknowns requeridos y claims prohibidos; `K = |F|` es el único denominador de cobertura/omisiones. |
| V21-AC05 | A/B usan exactamente el mismo prompt, rubric, schema de respuesta, presupuesto y configuración solicitada dentro de cada par; A solo recibe `CURRENT` y B recibe `CURRENT` más `IOS_SIBLING`. |
| V21-AC06 | Las corridas son independientes, se ejecutan `AB`, `BA`, `AB`, no reciben respuestas previas y tienen cero tool calls; cualquier violación invalida la corrida. |
| V21-AC07 | Cada respuesta separa `evidence_claims[]`, `inferences[]`, `unknowns[]` y `actions[]`; cada claim es una unidad atómica contable y cubre como máximo un fact ID. |
| V21-AC08 | El scorer independiente conserva por respuesta los numeradores, denominadores, fact IDs cubiertos/omitidos, clasificación de cada claim, errores graves y evidencia de penalizaciones. El mapa A/B se abre solo después de cerrar y hashear el scoring. |
| V21-AC09 | Un único `PRE_RESPONSE_SEAL` liga scope, derivaciones, key, prompt, rubric, schema y paquetes antes de cualquier respuesta. Cada corrida referencia el sello; no se requiere encadenar una corrida con la anterior. |
| V21-AC10 | Los tres pares cumplen frescura, integridad y presupuesto; los umbrales se aplican sin redondear ni imputar valores `unknown`. |
| V21-AC11 | Un review N2 independiente recalcula una muestra A/B y un par completo, revisa privacidad, integridad, scoring y conclusión, y deja cero findings obligatorios antes del cierre. |
| V21-AC12 | El resultado queda limitado a esta tarea y es exactamente `beneficio observado`, `beneficio no observado` o `inconcluso`; no constituye decisión de release. |
| V21-AC13 | El piloto permanece en solo lectura; código, respuestas selladas y key no se modifican. Delegación, P3–P6 y publicación requieren autorización separada. |

## 3. Protocolo simplificado

### 3.1 Frescura focalizada

Antes de retomar P2:

1. ejecutar `check` sobre los dos manifests privados de P1;
2. comparar HEAD, refs/OID, status, diffs, índice y hashes de untracked contra el baseline;
3. continuar solo si todo coincide;
4. ejecutar nuevamente el inventario completo únicamente ante drift o evidencia de que la
   tarea dejó de estar soportada.

El PASS histórico de P1 no se presenta como frescura actual.

### 3.2 Resolución de E-SENS-01 mediante fragmentos derivados

Los manifests originales se preservan en evidencia privada. Los paquetes A/B se construyen
desde copias derivadas externas, nunca desde cambios al piloto.

Cada entrada de `DERIVATION_MANIFEST.json` debe registrar:

```text
evidence_id
source_alias, source_oid, source_path, source_blob, source_sha256
selected_byte_spans[]
derivation_rule_id
sensitive_disposition: excluded-by-selection | replaced
replacement_count
derived_sha256, derived_bytes
```

Reglas:

- seleccionar mediante allowlist solo spans necesarios para la tarea;
- si E-SENS-01 queda fuera de esos spans, registrar `excluded-by-selection`;
- si un span necesario lo contiene, reemplazar únicamente esa ocurrencia por
  `<REDACTED:E-SENS-01>` y registrar `replacement_count = 1`;
- verificar que todos los demás bytes seleccionados permanecen iguales;
- escanear derivados y paquetes antes del sello;
- el key no puede citar, describir ni puntuar el literal excluido;
- un hash derivado prueba el derivado, no identidad byte a byte con el blob fuente.

La clasificación definitiva del literal sigue `unknown`; el benchmark no intenta validarlo.

### 3.3 Key y respuesta

Sea `F` el conjunto sellado de required facts con `score=true`, `K = |F|` y `C_r` los
fact IDs únicos correctamente cubiertos por una respuesta. `KEY_VALIDATION` falla si `K=0`,
hay IDs duplicados, evidencia inexistente, unidades compuestas o conjuntos requeridos vacíos.

El formato se mantiene:

```text
evidence_claims[]: claim_id, subject, predicate, object, evidence_refs[]
inferences[]: inference_id, statement, basis_refs[]
unknowns[]: unknown_id, statement, missing_evidence
actions[]: step_id, action, target, validation, rollback
```

Un claim es correcto solo si su proposición completa está soportada y su alias/OID/ruta
coincide con la evidencia derivada. Un `unknown` legítimo no es error factual; puede dejar
un fact ID sin cubrir. Una afirmación de runtime sin evidencia o una atribución a otro
target es error grave.

### 3.4 Métricas centrales

| Métrica | Definición exacta |
|---|---|
| Cobertura de hechos | `|C_r ∩ F| / K` |
| Omisiones | `K - |C_r ∩ F|` |
| Precisión | claims correctos y soportados / `|evidence_claims[]|` |
| Errores graves | cantidad de claims con target/provenance equivocado o runtime afirmado sin evidencia |
| Contexto | bytes serializados del input completo; debe ser `<= 131072` |

Claims repetidos cuentan en precisión, pero un fact ID suma una sola vez en cobertura.
Sin claims, precisión es `unknown` y el par no puede ser favorable. Fracciones y numeradores
se preservan; los gates usan la fracción exacta. Tokens/costo/modelo efectivo/latencia se
mantienen `unknown` salvo evidencia directa.

### 3.5 Cegado y sello

El scorer recibe key, rubric, definiciones y seis respuestas anonimizadas; no recibe mapa,
orden, estados, v1 ni conclusiones. El coordinador valida estructura y aritmética sin puntuar,
hashea el scoring y recién entonces abre el mapa.

`PRE_RESPONSE_SEAL.json` incluye hashes y tamaños de scope, derivation manifest, key,
validación del key, prompt, rubric, schema y paquetes, más la constatación de que no existen
respuestas. Cada manifest de corrida referencia este hash. SHA-256 prueba consistencia del
contenido, no autoría ni timestamp externo.

## 4. Umbrales y resultados

Se conservan los umbrales cuantitativos ya aprobados; cambia la nomenclatura y se eliminan
gates secundarios.

Un par es favorable a B si simultáneamente:

1. `cobertura_B >= 0.90`;
2. `cobertura_B - cobertura_A >= 0.25`, o B reduce al menos tres omisiones;
3. `precisión_B` y `precisión_A` son conocidas y `precisión_B >= precisión_A`;
4. B tiene cero errores graves;
5. ambos lados cumplen frescura, integridad y presupuesto.

Resultado global:

- **beneficio observado:** los tres pares son válidos y al menos dos son favorables a B;
- **beneficio no observado:** los tres pares son válidos y menos de dos son favorables;
- **inconcluso:** falta un par válido, una métrica gate es `unknown`, hay drift/integridad
  fallida, key/sello inválido, contaminación o el review conserva un finding obligatorio.

No hay resultado `release candidate`. Cualquier decisión de producto/release requiere otra
evaluación y autorización.

## 5. Testing aprobado

Perfil aprobado para v2.1: **T2 reforzado**, en reemplazo del T3 aprobado para v2. Se
justifica porque el benchmark no cambia producto ni datos y los riesgos
materiales se cubren con controles dirigidos, scoring independiente y review N2.

Validaciones requeridas:

- PASS de frescura/integridad focalizada antes de P2 y después de P3;
- key con denominador no cero, IDs únicos y evidence refs existentes;
- derivación reproducible, un solo cambio autorizado por reemplazo y scan sensible PASS;
- hashes de prompt/schema/paquetes/sello y presupuesto;
- negativos: ID duplicado, evidencia ausente, cero claims, target equivocado, runtime sin
  evidencia, hash roto, respuesta previa al sello, respuesta v1 reutilizada y tool call;
- scoring ciego con muestra recalculada por review N2.

Se retiran del T3 anterior la cadena de recuperación entre intentos y las categorías que
solo respaldaban métricas eliminadas. Permanece sin verificar el comportamiento real de
dispositivo, backend, instalaciones activas, autenticidad temporal externa y enforcement
técnico del sandbox; no forman parte de la conclusión.

## 6. Routing y boundaries

- Delta/key/privacidad y review crítico: ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High;
  fallback GPT-5.6 Terra (`gpt-5.6-terra`) / High o XHigh.
- Paquetes, corridas, aritmética e informe: BALANCED — GPT-5.6 Terra
  (`gpt-5.6-terra`) / Medium; fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- Effective session config: `unknown`; las recomendaciones no prueban ejecución real.

Este delta y T2 reforzado fueron aprobados por el usuario el 2026-09-23. Esa aprobación no
autoriza P2–P6, sanitización, respuestas, scoring, delegación ni publicación. La P2 ajustada
necesita autorización separada.

## 7. Mapeo desde v2

| v2 | v2.1 aprobado |
|---|---|
| AC1, AC2, AC4, AC6, AC8–AC10, AC14, AC16 | Se conservan con redacción acotada en V21-AC01, AC04–AC08, AC11 y AC13. |
| AC3 y AC12 | Se reemplaza repetición amplia por `check` e integridad focalizada; drift reactiva P1. |
| AC5 y AC11 | Un único denominador de cobertura; se eliminan segundo recall, unknown score y retrabajo. |
| AC7 | Un sello previo común; cada corrida referencia el sello sin cadena entre corridas. |
| AC13 | Bytes siguen obligatorios; tiempo/tokens/costo solo informativos si son observables. |
| AC15 | `beneficio observado`, `beneficio no observado` o `inconcluso`; sin recomendación de release. |
| T3 | T2 reforzado aprobado con negativos dirigidos y review N2. |
