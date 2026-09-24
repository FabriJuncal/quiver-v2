# Contrato de answer key, respuesta y scoring — v2

Este documento define el contrato normativo. El answer key concreto se poblará con evidencia
fresca en P2, solo después de autorizar ejecución, y se sellará antes de P3.

## 1. Answer key cerrado

El archivo privado `ANSWER_KEY.json` se serializa en UTF-8, LF, claves ordenadas
recursivamente, arrays en orden declarado y newline final. Debe contener:

```text
schema_version
experiment_id
scope_manifest_sha256
created_at_utc
required_facts[]
  id, statement, criticality, observable_in[], evidence_ids[], score
required_unknowns[]
  id, statement, applicable_in[], evidence_ids[], severity_if_asserted
forbidden_claims[]
  id, pattern_or_statement, applicable_in[], severity, evidence_ids[]
attribution_targets[]
  alias, oid, path, blob, evidence_id
```

Reglas de cierre:

- cada unidad es atómica y tiene ID estable (`F###`, `U###`, `X###`, `E###`);
- `required_facts` con `score=true`, `required_unknowns` y `forbidden_claims` deben ser no vacíos;
- `observable_in` solo admite `A`, `B` o ambos;
- `applicable_in` solo admite `A`, `B` o ambos;
- toda unidad referencia evidencia incluida en el scope sellado;
- no hay crédito parcial: una unidad compuesta se divide antes del sello;
- el key no contiene respuestas modelo ni texto de v1;
- una modificación posterior al sello invalida el experimento completo; no se crea una
  versión corregida después de ver respuestas.

Un validador determinista produce `KEY_VALIDATION.json` con conteos, IDs duplicados,
referencias faltantes y denominadores. Solo un PASS permite crear el sello.

## 2. Formato de respuesta

Cada modelo devuelve un objeto estructurado con cuatro arrays:

```text
evidence_claims[]: claim_id, subject, predicate, object, evidence_refs[]
inferences[]: inference_id, statement, basis_refs[], confidence_label
unknowns[]: unknown_id, statement, missing_evidence
actions[]: step_id, action, target, validation, rollback
```

Cada objeto de `evidence_claims[]` es una unidad contable. Debe expresar una sola
proposición. Si contiene varias, cuenta como un claim y solo es correcto si todas son
verdaderas y están soportadas. No se divide después y puede cubrir como máximo un fact ID.
Claims repetidos cuentan en precisión, pero un hecho requerido solo suma una vez en recall.

## 3. Denominadores y fórmulas

Sea `F` el conjunto sellado de required facts con `score=true`, `K = |F|`, `F_m` los hechos
observables en modalidad `m`, `K_m = |F_m|`, `U_m` los required unknowns aplicables a `m`,
y `C_r` los IDs únicos correctamente cubiertos por la respuesta `r`.

| Métrica | Fórmula exacta |
|---|---|
| Recall de utilidad | `|C_r ∩ F| / K` |
| Recall acotado a evidencia | `|C_r ∩ F_m| / K_m` |
| Omisiones de utilidad | `K - |C_r ∩ F|` |
| Omisiones evitables | `K_m - |C_r ∩ F_m|` |
| Brecha estructural | hechos de `F \ F_m` no cubiertos; se reportan separados de errores |
| Precisión | claims correctos y soportados / `|evidence_claims[]|` |
| Disciplina de unknown | required unknowns de `U_m` declarados correctamente / `|U_m|` |
| Atribución incorrecta | claims con alias/OID/path/blob equivocado, separados alta/baja |
| Retrabajo | omisiones de utilidad + claims incorrectos/no soportados + required unknowns ausentes |

Un `unknown` correcto no es claim incorrecto y no entra en precisión; puede seguir dejando
una omisión de utilidad. Un hecho no observable para A no es una atribución ni un error de A.
Si no hay `evidence_claims`, precisión es `unknown` y falla el umbral. `K=0`, `K_m=0`,
`|U_m|=0` o un conjunto de forbidden claims vacío hacen fallar `KEY_VALIDATION`.

Los claims incorrectos y las atribuciones usan una sola unidad de retrabajo por claim; la
severidad es etiqueta, no suma adicional. Los minutos de retrabajo quedan `unknown` salvo
medición humana directa.

Se conservan fracción y decimal; los umbrales se comparan con la fracción exacta. Mediana y
rango (`max-min`) se calculan sobre tres valores, sin imputar `unknown`.

## 4. Regla de corrección de claims

Un claim es correcto solo si:

1. sus referencias existen en el paquete recibido por esa modalidad;
2. alias, OID, ruta y blob corresponden al target sellado;
3. la evidencia citada soporta la proposición completa;
4. no convierte una inferencia o un unknown requerido en hecho.

Lo no verificable presentado como hecho cuenta como claim no soportado. Las acciones y
recomendaciones no entran en precisión salvo que incorporen una afirmación factual; el
formato obliga a mover esa afirmación a `evidence_claims[]`.

## 5. Scoring ciego

El scorer recibe únicamente key, rubric, definiciones, seis respuestas anonimizadas y
hashes necesarios. No recibe mapa A/B, orden, STATE, v1, conversación ni conclusiones.
Devuelve por respuesta: denominadores, numeradores, IDs cubiertos/omitidos, clasificación
de cada claim, unknowns, atribuciones, retrabajo y evidencia de penalizaciones.

El coordinador valida estructura y aritmética, hashea el scoring y recién entonces abre el
mapa. No puntúa respuestas. Las restricciones del prompt/allowlist son controles auditados,
no garantías técnicas si el runtime no expone enforcement.

## 6. Enlace temporal

La cadena privada es:

```text
SCOPE_MANIFEST ─┐
ANSWER_KEY ─────┤
RUBRIC ─────────┼─> PRE_RESPONSE_SEAL ─> RUN_01 ─> ... ─> RUN_06 ─> P3_MANIFEST
PROMPT ─────────┤
CONTEXTS A/B ───┘
```

`PRE_RESPONSE_SEAL.json` registra hashes SHA-256, tamaños, timestamps UTC, denominadores,
resultado del validador y ausencia de archivos de respuesta. Cada `RUN_MANIFEST` referencia
el hash del sello, el manifest anterior, el paquete, prompt, eventos y respuesta. El manifest
P3 fija el orden completo.

SHA-256 prueba igualdad y encadenamiento de contenido, no autoría ni tiempo confiable frente
a un tercero. Sin timestamp authority o firma autenticada, esa propiedad queda `unknown`;
el protocolo solo demuestra consistencia interna y orden registrado. Un hash o vínculo que
no coincide detiene el experimento.
