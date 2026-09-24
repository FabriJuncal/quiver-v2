# Plan técnico — Benchmark operativo v2

Estado: **aprobado por el usuario el 2026-09-23; ejecución no autorizada**.
Perfil de testing aprobado: **T3**.

## Objetivo y límites

Producir una comparación nueva A/B con métricas reproducibles y evidencia encadenada, sin
modificar Quiver ni el repositorio piloto. Todo output privado se guarda en un root exacto,
registrado y no versionable, fuera del piloto. No se reutilizan respuestas v1.

## P0 — Autorización y preflight

1. Registrar aprobación humana de criterios, plan, T3 y autorización de ejecución como
   decisiones separadas.
2. Registrar un `PRIVATE_EVIDENCE_ROOT` nuevo y verificar que no contiene respuestas.
3. Capturar status/diff de Quiver sin tocar cambios ajenos.
4. Verificar disponibilidad real de sesiones independientes; delegación P4/P5 requiere
   opt-in específico, un agente máximo, coordinador único escritor y sin subdelegación.
5. Registrar perfil solicitado y configuración efectiva solo si el runtime la expone.

**Validación:** autorizaciones presentes, root nuevo, cero respuestas y controles reales
documentados. Si falta capacidad independiente, detener antes de P3/P4.

## P1 — Scope fresco e integridad de solo lectura

1. Ejecutar únicamente los controles read-only ya aprobados para refs, OID, HEAD, status,
   diffs, índice y hashes de untracked.
2. Resolver aliases a OID y blobs frescos; generar `SCOPE_MANIFEST` y baseline.
3. Confirmar que la tarea conceptual sigue soportada por la evidencia actual.
4. Generar un manifest con hashes de las respuestas v1, sin copiarlas a paquetes, para
   comprobar que ningún output v2 es una reutilización byte a byte.

**Detención:** drift, escritura, material sensible inesperado o tarea ya no soportada.

## P2 — Key, prompt, paquetes y sello

1. Poblar el key conforme a `02_SCORING_PROTOCOL.md`, con hechos atómicos y procedencia.
2. Ejecutar `KEY_VALIDATION`; corregir solo antes del sello.
3. Congelar rubric, prompt común y schema de respuesta.
4. Construir A y B bajo el mismo límite, medir bytes/archivos/fragmentos/blobs y verificar
   que A no contiene señales de otra variante.
5. Registrar hashes y ausencia de respuestas en `PRE_RESPONSE_SEAL`; calcular su SHA-256.
6. Volver a verificar key, prompt y paquetes por hash.

**Gate duro:** ninguna respuesta puede existir ni iniciarse antes del sello PASS. Cualquier
cambio posterior obliga a descartar el experimento aún no ejecutado y regresar a P1/P2.

## P3 — Seis respuestas nuevas

1. Crear seis sesiones nuevas en orden `A1, B1, B2, A2, A3, B3`.
2. Dar a cada sesión solo prompt, schema, paquete correspondiente y hash del sello.
3. Prohibir acceso a respuestas/resultados v1 y a outputs de otras corridas.
4. Exigir cero tool calls, output estructurado y manifest enlazado por corrida.
5. Invalidar cualquier respuesta cuyo hash coincida con v1, cuyo manifest no enlace el
   sello o cuyo runtime/config difiera dentro del par sin repetición limpia.
6. Repetir integridad del piloto al terminar cada par y al cerrar P3.

No ejecutar esta fase sin una autorización posterior explícita.

## P4 — Scoring ciego

1. Crear labels neutrales y mantener el mapa fuera del paquete del scorer.
2. Usar un scorer nuevo, si la delegación fue autorizada y la capacidad existe.
3. Validar que cada métrica conserva fórmula, numerador, denominador e IDs.
4. Recalcular aritmética determinísticamente; cerrar y hashear el scoring.
5. Confirmar que el scorer terminó y abrir el mapa recién después.
6. Agregar por modalidad/par: valores, medianas, rangos y pares favorables.

**Detención:** acceso prematuro al mapa, scorer activo/desconocido, denominador mutable,
estructura inválida no corregible sin reinterpretar respuestas o aritmética inconsistente.

## P5 — Review N2 independiente

1. Preparar un paquete sanitizado con plan aprobado, hashes, cadena temporal, scoring,
   mapa abierto, cálculos, integridad, desviaciones, draft, unknowns y límites.
2. Un reviewer distinto recalcula al menos una respuesta A, una B y un par completo; revisa
   las seis para atribución alta, privacidad, contaminación y unknowns.
3. Emitir `APROBADO`, `APROBADO CON NOTAS` o `REQUIERE CORRECCIÓN` con findings obligatorios
   u opcionales.
4. Permitir una única corrección dirigida de artefactos derivados; nunca modificar key ni
   respuestas. El mismo reviewer verifica solo los findings corregidos.

**Detención:** findings obligatorios abiertos tras esa ronda o independencia no disponible.

## P6 — Informe y cierre

1. Generar informe sanitizado con comparación por corrida y agregada.
2. Separar mediciones, inferencias y unknowns; no publicar refs/OID, clientes, rutas privadas
   ni secretos.
3. Aplicar los umbrales exactos y registrar un solo resultado permitido.
4. Repetir integridad del piloto y todos los hashes; confirmar respuestas inmutables.
5. Ejecutar validaciones Markdown/documentales, `git diff --check`, inspección de diff y
   comprobación de que no cambió código ni material fuera del requirement.
6. Actualizar STATE y PROJECT_STATE con próxima decisión humana.

## Casos T3 obligatorios

- key con ID duplicado, conjunto vacío o evidencia faltante debe fallar antes del sello;
- respuesta anterior al sello, hash roto o cadena fuera de orden debe detener P3;
- claim compuesto no se divide y debe validarse como unidad completa;
- respuesta sin claims produce precisión `unknown` y no pasa;
- `unknown` correcto de A no se convierte en error factual;
- claim con target correcto pero OID/path incorrecto se clasifica como atribución;
- cambio de key después del sello invalida el experimento, sin reparación retroactiva;
- respuesta v2 con hash de v1 se invalida;
- recuperación solo puede reiniciar desde P1/P2 antes de respuestas o repetir un par
  inválido con paquetes inmutables; nunca se mezcla evidencia de intentos.

## Rollback

No hay rollback de código. Ante fallo, preservar evidencia e incidente, marcar el intento
inválido y detener. Una eventual limpieza solo puede afectar el directorio privado exacto y
requerirá autorización específica; nunca usar globs, reset, checkout o `git clean`.

## Dependencias y unknowns

- autorización humana de criterios, plan y T3;
- autorización posterior de ejecución;
- autorización separada de delegación P4/P5;
- disponibilidad real de sesiones independientes;
- identidad efectiva de modelo/reasoning, enforcement read-only/no-recursion y timestamp
  autenticado: `unknown` salvo evidencia del runtime;
- tokens, costo y latencia: `unknown` hasta medición directa.
