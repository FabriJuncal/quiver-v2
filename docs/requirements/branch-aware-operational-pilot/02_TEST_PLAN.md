# Test plan — Benchmark operativo v1

Perfil propuesto: **T2 reforzado**. El riesgo N2 proviene de contaminación de contexto,
atribución entre variantes y uso de evidencia privada; no se requieren builds móviles ni
pruebas de backend para medir el lector.

## 1. Preflight e integridad

Antes de cada par:

1. resolver `CURRENT` e `IOS_SIBLING` a los OID del scope privado;
2. capturar hashes de refs, HEAD, status porcelain v2, diff worktree, diff cached, índice
   y contenido de archivos untracked regulares;
3. ejecutar `inspect` con output externo;
4. exigir cobertura completa, 82/82 tips y cero errores para el snapshot fijado;
5. abortar si refs u overlay cambiaron respecto del snapshot aprobado.

Al terminar el par, repetir exactamente el snapshot de integridad. Cualquier diferencia
es un fallo del piloto, aunque las respuestas parezcan correctas.

## 2. Answer key privado

Construir antes de las corridas, fuera del worktree piloto y sin exponerlo a A/B:

- refs/OID y blobs de los cinco paths seleccionados;
- versión declarada del plugin en ambos targets;
- API de inicialización y listeners observada en cada target;
- cuatro paths diferentes y un path control sin cambio;
- distribución agregada de las tres generaciones de API entre 82 tips;
- hechos que no pueden probarse: instalación activa, App ID correcto, permisos reales,
  entrega de push, backend y éxito en dispositivo;
- claims prohibidos de severidad alta, por ejemplo atribuir código de `CURRENT` a
  `IOS_SIBLING` o afirmar runtime verificado.

El evaluador firma el answer key con SHA-256 antes de generar respuestas.

## 3. Prompt congelado

Usar el mismo prompt de tarea en A y B. Solo cambia el bloque de evidencia. El prompt
prohíbe escribir código y exige:

- lista de archivos y diferencias relevantes;
- plan de migración ordenado;
- valores/configuración que deben preservarse;
- validación y rollback;
- hechos, inferencias y desconocidos separados;
- citas `alias@OID:ruta` para todo claim de código.

El hash del prompt sin evidencia debe ser idéntico en las seis corridas.

## 4. Contextos comparables

Presupuesto total por corrida: **131072 bytes** serializados, incluyendo instrucciones y
evidencia; registrar el tamaño real.

### A — HEAD-only

- Solo `CURRENT` y sus cinco paths seleccionados.
- Sin nombres/conteos de refs, inventario, comparación, cohortes o contenido del target.
- Debe poder responder `unknown` cuando la evidencia no alcance; no se penaliza una
  limitación legítima como error, pero sí cuenta como omisión frente al answer key.

### B — branch-aware

- `CURRENT` e `IOS_SIBLING` fijados por OID.
- Deltas exactos de los cinco paths y resumen determinista de cohortes.
- Fragmentos mínimos seleccionados por `context`, con procedencia completa.
- Deduplicación por blob y exclusiones explícitas.

Si B excede el presupuesto, reducir fragmentos de forma determinista; nunca ampliar el
límite respecto de A.

## 5. Corridas independientes

Ejecutar tres pares con orden predefinido:

| Par | Orden | Sesiones |
|---|---|---|
| 1 | A → B | dos sesiones nuevas |
| 2 | B → A | dos sesiones nuevas |
| 3 | A → B | dos sesiones nuevas |

Configuración solicitada para las seis respuestas: **GPT-5.6 Terra
(`gpt-5.6-terra`) / Medium**. Registrar el modelo/reasoning efectivos solo si el runtime
los muestra; si no, `unknown`. Si se usa fallback, debe aplicarse a ambos lados del par y
registrarse como desviación; no mezclar modelos dentro de un par.

No reutilizar chat, resumen, respuesta, memoria semántica o archivos de resultado entre
sesiones. El operador conserva comandos/evidencia determinista, no conclusiones del otro
modo.

Cada respuesta se ejecuta con `codex exec --ephemeral`, directorio aislado, sandbox
read-only, configuración explícita y solo prompt+evidencia. Guardar JSONL de eventos e
invalidar cualquier corrida que invoque herramientas. Si el runtime no soporta ese
aislamiento, detener y registrar `unavailable-runtime-capability`; no reemplazar seis
sesiones por seis turnos del mismo chat.

## 6. Scoring ciego

Renombrar respuestas como `X1/Y1`, `X2/Y2`, `X3/Y3`; ocultar el mapa A/B al scorer hasta
terminar la puntuación. Review N2 con **GPT-5.6 Sol (`gpt-5.6-sol`) / High**.

| Métrica | Definición |
|---|---|
| Cobertura de refs | refs/tips inventariados o error explícito sobre el denominador fijado. |
| Recall de evidencia | hechos requeridos correctos y citados / hechos requeridos aplicables. |
| Omisiones | hechos requeridos ausentes; `unknown` correcto se conserva pero cuenta para utilidad. |
| Atribución incorrecta | claim asignado al alias/OID/ruta equivocado; separar severidad alta/baja. |
| Precisión de claims | claims verificables correctos y soportados / total de claims verificables; sin claims, `unknown` y la corrida no satisface el umbral. |
| Tiempo | Git, preparación, humano y modelo separados; `unknown` si no se observa. |
| Pasos manuales | intervenciones humanas desde preflight hasta output final. |
| Contexto | bytes serializados, archivos, fragmentos y blobs únicos enviados. |
| Deduplicación | bytes de ocurrencias seleccionadas menos bytes de blobs únicos; no equivale a tokens. |
| Tokens/costo | input/output/cached/costo del runtime; `unknown` si no se informa. |
| Retrabajo | correcciones necesarias para alcanzar el answer key y minutos humanos asociados. |
| Frescura | manifest `check` PASS y refs/OID/overlay iguales al scope. |
| Integridad | igualdad byte/hash antes-después para los controles definidos. |

## 7. Resultado y umbrales

Recomendar avanzar a una release candidate solo si:

- integridad y frescura pasan en los tres pares;
- B obtiene al menos 90% de recall en dos de tres corridas;
- B mejora al menos 25 puntos porcentuales de recall sobre A, o elimina al menos tres
  omisiones relevantes cuando A declaró límites correctos;
- B tiene cero atribuciones de severidad alta;
- precisión de B no es inferior a A;
- ambas modalidades respetan 131072 bytes;
- el resultado favorable se repite en al menos dos de tres pares.

Si solo mejora cobertura con un costo mayor, el informe presenta el trade-off y no decide
por el usuario. Tokens/costo desconocidos no invalidan el piloto, pero impiden afirmar
ahorro económico.

La conclusión se limita a tareas que requieren otra variante. No generalizar el resultado
a tareas contenidas por completo en HEAD ni a calidad global del modelo.

## 8. Condiciones de detención

Detener sin continuar corridas si:

- cambia cualquier ref/OID u overlay del scope;
- aparece una escritura o cambio de integridad;
- `inspect` queda partial/stale o encuentra objetos faltantes;
- no puede garantizarse aislamiento entre sesiones;
- el modelo efectivo difiere dentro de un par y no puede repetirse;
- el answer key cambia después de ver una respuesta;
- aparece material sensible no previsto en el contexto.

## 9. Rollback y limpieza

El piloto no modifica código. Rollback consiste en descartar el par incompleto, conservar
la evidencia del incidente y borrar únicamente el directorio externo exacto registrado.
Nunca usar globs, `git clean`, reset, checkout o limpieza dentro del repositorio piloto.

## Fuera de alcance

Builds Android/iOS, entrega real de notificaciones, permisos en dispositivo, APIs de
backend, identidad de instalaciones activas, modificación de código y publicación.
