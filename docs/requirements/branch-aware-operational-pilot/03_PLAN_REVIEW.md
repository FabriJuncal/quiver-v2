# Plan review — Branch-aware operational pilot v1

- **Fecha:** 2026-09-23.
- **Modalidad:** self review crítica en la misma sesión; no independiente.
- **Riesgo:** N2.
- **Alcance:** plan y protocolo; no se ejecutó el benchmark.
- **Review profile recomendado:** ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High.
- **Effective session config:** unknown; no se infiere.

## Trazabilidad

| Criterio | Paso | Validación prevista |
|---|---|---|
| AC1, AC3, AC4 | P2 construye A/B desde prompt congelado y scope por OID. | Hash del prompt, manifests, procedencia y bytes serializados. |
| AC2, AC11 | P1 captura integridad; P6 repite. | Igualdad de HEAD, refs, status, diffs, índice y untracked. |
| AC5 | P3 ejecuta `AB`, `BA`, `AB` mediante procesos efímeros. | Seis JSONL, seis respuestas y ausencia de tool calls. |
| AC6 | P2 fija answer key antes de P3. | Hash SHA-256 y timestamp anterior a las respuestas. |
| AC7, AC8 | P4 calcula rubric; P5 revisa. | Scoring por corrida, errores por severidad y repetibilidad. |
| AC9, AC10 | P2–P4 registran recursos separadamente. | Measurements JSON con bytes, blobs, tiempos y unknowns. |
| AC12 | P5/P6 limitan el veredicto. | Review N2 y reporte con uno de tres resultados permitidos. |

## Findings y corrección dirigida

### PR-01 — OBLIGATORIO — cerrado

- **Problema:** “sesiones nuevas” no definía un aislamiento ejecutable y podía terminar
  como seis turnos contaminados del mismo chat.
- **Corrección:** P3 usa `codex exec --ephemeral`, directorios aislados, sandbox read-only,
  prompt+evidencia solamente y JSONL auditado. Una tool call invalida la corrida. Falta de
  capacidad detiene el piloto como runtime limitation.
- **Evidencia:** `codex-cli 0.155.1` expone `exec`, `--ephemeral`, `--sandbox`, `--cd`,
  `--json` y `--output-last-message`. Disponibilidad de modelos permanece no verificada.

### PR-02 — OBLIGATORIO — cerrado

- **Problema:** una tarea de menú/capacidad habría requerido backend e instalación activa,
  sin answer key estático confiable.
- **Corrección:** se seleccionó migración de API push con versiones, blobs y llamadas
  observables. Runtime/backend quedan como unknowns obligatorios, no hechos a inferir.

### PR-03 — OBLIGATORIO — cerrado

- **Problema:** más contexto podía confundirse con mejor modelo o presupuesto desigual.
- **Corrección:** mismo prompt, límite total de 131072 bytes, configuración solicitada
  igual por par, orden alternado, sesiones independientes y scoring firmado.

### PR-04 — OPCIONAL — aceptado

- **Nota:** el scorer puede inferir el modo por la riqueza del contenido, aunque no conozca
  el mapa A/B. El plan declara cegado de labels, no doble ciego.
- **Trade-off:** un evaluador externo adicional aumentaría costo y coordinación sin eliminar
  completamente esa inferencia en este primer piloto.

### PR-05 — OPCIONAL — aceptado

- **Nota:** seis respuestas consumen más IA que un smoke test de un par.
- **Trade-off:** tres pares son el mínimo elegido para no basar una decisión de release en
  una única salida variable. El scope de cinco paths limita el costo.

Una ronda dirigida cerró los tres findings obligatorios. No quedan correcciones bloqueantes.

## AI Strategy review

- ADVANCED/High está justificado en planning/review por privacidad, diseño experimental y
  riesgo de atribución.
- Ejecución usa BALANCED/Medium porque el prompt y la evidencia están congelados.
- P0–P2 y P4 son deterministas y no requieren inferencia; se eliminó uso innecesario de IA.
- GPT-6 Astra no está justificado.
- Tokens/costo y configuración efectiva no se inventan.

## Veredicto

**APROBADO CON NOTAS.** El plan es ejecutable, proporcional y trazable. La aprobación del
reviewer no reemplaza la aprobación humana ni autoriza las seis corridas. La conclusión
del futuro piloto solo será válida para tareas que requieren evidencia de otra variante.
