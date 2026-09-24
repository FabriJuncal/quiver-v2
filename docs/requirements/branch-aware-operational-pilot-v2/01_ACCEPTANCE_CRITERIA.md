# Acceptance criteria aprobados — Benchmark v2

Aprobados por el usuario el 2026-09-23 junto con el plan v2 y el perfil T3. Esta
aprobación no autoriza ejecución, respuestas, scoring, delegación ni publicación.

| ID | Criterio observable |
|---|---|
| AC1 | Ninguna respuesta, puntuación ni conclusión de v1 se usa como input, muestra o baseline cuantitativo de v2; solo se reutiliza la lección documental del fallo de protocolo. |
| AC2 | A y B usan el mismo prompt base, rubric, formato de respuesta, presupuesto de 131072 bytes y configuración solicitada dentro de cada par; cualquier diferencia se registra e invalida el par si afecta comparabilidad. |
| AC3 | Antes de preparar el key se fija un scope fresco con aliases, OID, blobs y overlay; todo cambio posterior de ref, OID, índice, status, diff o untracked invalida el experimento antes de continuar. |
| AC4 | El answer key concreto contiene conjuntos cerrados y no vacíos de `required_facts`, `required_unknowns` y `forbidden_claims`, IDs estables y procedencia verificable. |
| AC5 | Los denominadores de recall, recall acotado a evidencia, omisiones y disciplina de unknown se derivan solo de los conjuntos sellados del key; no se agregan unidades después de observar respuestas. |
| AC6 | La precisión usa exactamente los objetos de `evidence_claims[]` emitidos por cada respuesta; no se segmenta prosa retrospectivamente. Una respuesta sin claims deja precisión `unknown` y no satisface el umbral. |
| AC7 | El key, rubric, prompt, scope y paquetes quedan ligados en un `PRE_RESPONSE_SEAL` con SHA-256 antes de crear respuestas; cada corrida referencia ese digest y el manifest anterior. |
| AC8 | Las seis respuestas de v2 son nuevas, independientes, sin acceso a outputs de v1 ni de otras corridas, y se ejecutan en orden contrabalanceado `AB`, `BA`, `AB`. |
| AC9 | A recibe solo evidencia permitida de `CURRENT`; B recibe evidencia atribuida de `CURRENT` y `IOS_SIBLING`. Un `unknown` legítimo no es error factual, aunque pueda contar como omisión de utilidad. |
| AC10 | El scoring ciego calcula fracciones exactas y conserva numerador, denominador, IDs cubiertos/omitidos y evidencia de cada penalización; el mapa A/B se abre solo después de cerrar y hashear el scoring. |
| AC11 | Por par y agregado se informan recall de utilidad, recall acotado, omisiones de utilidad/evitables, precisión, atribuciones por severidad, disciplina de unknown y unidades de retrabajo. |
| AC12 | Integridad y frescura pasan antes y después de cada fase; answer key, prompt, paquetes, respuestas, scoring y manifest conservan sus hashes. |
| AC13 | Tiempo, pasos manuales, bytes, archivos, fragmentos, blobs, deduplicación, tokens, costo, modelo efectivo y latencia solo se reportan como medidos cuando existe evidencia directa; de lo contrario quedan `unknown`. |
| AC14 | Un review N2 independiente recalcula una muestra, revisa aislamiento/privacidad, verifica umbrales y deja cero findings obligatorios abiertos antes del cierre. |
| AC15 | El resultado se limita a tareas que necesitan evidencia de otra variante y es exactamente uno de: `release candidate`, `ajustar` o `beneficio no probado`. |
| AC16 | No se modifica código de Quiver ni el repositorio piloto y no se realiza publicación, operación Git de entrega ni delegación sin autorización separada. |

## Umbrales aprobados

Una corrida B es favorable dentro de su par solo si, sin redondeo para decidir:

1. su recall de utilidad es al menos `0.90`;
2. mejora al menos `0.25` sobre A, o reduce al menos tres omisiones de utilidad;
3. tiene cero atribuciones de severidad alta;
4. su precisión es conocida y no inferior a A;
5. ambos lados cumplen presupuesto, frescura e integridad.

`release candidate` requiere al menos dos pares favorables de tres, B con recall `>= 0.90`
en al menos dos corridas y cero findings obligatorios del review. Un valor `unknown` en una
métrica umbral impide `release candidate`; no se reemplaza por cero ni por una inferencia.
