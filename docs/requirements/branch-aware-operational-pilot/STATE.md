# STATE — Branch-aware operational pilot

- **Status:** completed
- **Current phase:** P6 cerrada; benchmark v1 concluido como `beneficio no probado`.
- **Current slice:** none
- **Completed:** discovery de solo lectura, plan v1, P0–P3 y P4: scorer nuevo y ciego, labels anonimizados, mapa abierto solo después del cierre, cero tool calls e integridad PASS.
- **Pending:** ninguna fase del plan v1. Una release no está autorizada ni sustentada; un plan v2 requiere decisión humana separada.
- **Risk level:** N2; privacidad, aislamiento de corridas, atribución entre variantes e integridad del repositorio piloto.
- **Plan version:** 1
- **Plan review:** APROBADO CON NOTAS por self review no independiente; una ronda dirigida, findings obligatorios cerrados.
- **Human plan approval:** approved, plan v1, 2026-09-23 (user authorization recorded in this turn).
- **Execution authorization:** P0–P4 previamente autorizadas; P5–P6 autorizadas explícitamente el 2026-09-23. Delegación secuencial P4/P5 autorizada; ver `DELEGATION_AUTHORIZATION.md`.
- **Selected option:** A approved, migración/paridad de notificaciones push entre `CURRENT` e `IOS_SIBLING`.
- **Test profile:** T2 reforzado aprobado; tres pares independientes, scoring ciego y review N2.
- **Next action:** esperar decisión humana sobre si preparar un plan v2; no ejecutar nuevas respuestas ni publicación.
- **Why this is next:** el plan v1 está cerrado y no prueba beneficio; cualquier nuevo experimento necesita criterios/key previos y aprobación propia.
- **User action required:** true
- **Decision required:** dejar cerrado el resultado o solicitar únicamente la preparación de un plan v2.
- **Expected output:** nueva petición explícita; no existe acción automática autorizada.
- **After this:** si se pide plan v2, comenzar por criterios y protocolo, sin reutilizar respuestas ni publicar.
- **Blocked by:** none
- **Runtime limitation:** none
- **Runtime limitation detail:** effective scorer model/reasoning permanece unknown porque el JSONL no expone identidad; se solicitó Terra/Medium, no hubo fallback y P4 cerró normalmente. La limitación es del protocolo, no del runtime.
- **Resume instruction:** leer STATE.md, `04_SCORING.md`, `05_IMPLEMENTATION_REVIEW.md`, `BENCHMARK_REPORT.md` y `06_CLOSURE.md`. Para v2, enviar: `Prepará un plan v2 del benchmark branch-aware con un answer key cerrado y firmado antes de nuevas respuestas. No ejecutes P3 ni publiques nada sin mi aprobación.`

## AI Strategy

- Planning: ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High; effective config unknown.
- Execution: BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium; fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- Review N2: ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High; fallback GPT-5.6 Terra (`gpt-5.6-terra`) / High o XHigh.
- Exceptional: GPT-6 Astra no justificado.
- Switch Benefit: execution MEDIUM; review HIGH si la configuración suficiente no está confirmada.

## Evidencia de planning

- Inventario: 95 refs, 82/82 tips, cobertura completa, cero errores.
- Tiempo Git observado: 5,109838 s; no es SLA.
- Integridad before/after: igual para HEAD, refs, status, diffs, índice y untracked.
- Pareja recomendada: 51 rutas diferentes; cuatro de cinco paths del scope cambian.
- Cohortes: 55 `setAppId`, 10 `startInit`, 17 `initialize`.
- Tokens/costo/modelo efectivo: unknown.

## Evidencia P0–P2 — 2026-09-23

- Scope privado: no staged; refs/OID aprobados siguen fijados en `CURRENT` y `IOS_SIBLING`.
- Inventario actualizado: 95 refs, 82/82 tips, cobertura `complete`, cero errores.
- Comparación: 51 paths cambiados; OID `CURRENT` y `IOS_SIBLING` coinciden con el scope aprobado.
- Integridad: snapshots `before`, `after` y verificación posterior iguales para HEAD, refs, status, diffs, índice y hashes de untracked.
- Answer key privado: SHA-256 verificado `eb849870729236b4e5386099928823c461cf8db4b013fa487e2164a448c0ca1b`; precedencia declarada y corroborada por metadata, sin enlace criptográfico por corrida.
- Prompt común congelado: SHA-256 `e1d43c51328175a1286720b1426c448a9eeab38057995578dfa125988fcdf865`.
- Paquetes: `run-01-A`, `run-01-B`, `run-02-B`, `run-02-A`, `run-03-A`, `run-03-B`; cada uno tiene exactamente los seis archivos permitidos. Tamaños serializados A: 43362 bytes; B: 87116 bytes; límite: 131072 bytes.
- Evidencia externa privada y runbook preservados fuera de Git. En este corte P0–P2 todavía no se habían creado respuestas A/B.

## Evidencia P3 — 2026-09-23

- Orden ejecutado: `run-01-A`, `run-01-B`, `run-02-B`, `run-02-A`, `run-03-A`, `run-03-B` (`AB`, `BA`, `AB`).
- Seis procesos registrados con `codex exec --ephemeral`, `--sandbox read-only` y
  `--ignore-user-config`; cada JSONL terminó con `turn.completed`, una respuesta y cero tool
  calls. Los flags están declarados; el enforcement efectivo del aislamiento permanece unknown.
- Perfil solicitado: BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium. Fallback: no usado. Configuración efectiva: unknown; no se infiere del launcher.
- La primera invocación del launcher de `run-01-A` falló antes de completar sesión por permisos del entorno; el retry produjo la única respuesta válida de esa corrida. No se creó una respuesta extra.
- Desviación de cegado: el coordinador P3 abrió `run-01-A` una vez al auditar que la respuesta se hubiera escrito. No la puntuó ni la suministró a sesiones posteriores; P4 requiere un scorer nuevo con labels anonimizados y mapa A/B oculto.
- Integridad posterior: PASS; HEAD, refs, status, diffs, índice y hashes de untracked coinciden con el baseline.
- Manifest privado de ejecución y hashes de respuestas preservado fuera de Git.

## Evidencia P4 — 2026-09-23

- Preflight e integridad posterior: PASS; piloto sin cambios respecto del baseline.
- Answer key: firma SHA-256 verificada antes del scoring; contexts CURRENT/IOS_SIBLING pasaron `check` contra refs/OID fijados.
- Scorer: sesión efímera nueva, labels `X1/Y1`, `X2/Y2`, `X3/Y3`, mapa fuera del directorio del scorer, cero tool calls.
- Routing solicitado: BALANCED — GPT-5.6 Terra (`gpt-5.6-terra`) / Medium; fallback no usado; configuración efectiva unknown.
- Resultado ciego: `unscorable`; recall, omisiones y precisión carecen de denominadores reproducibles en el key firmado. `blind_scoring_closed=true`.
- El mapa A/B se abrió únicamente después del cierre ciego. No se inventaron métricas ni se modificó el key.
- Consecuencia: AC7/AC8 no evaluables; no se permite conclusión `release candidate` ni beneficio probado.
- Resultado, scoring y eventos P4 preservados en evidencia privada fuera de Git.

## Evidencia P5–P6 — 2026-09-23

- Reviewer nuevo y distinto del scorer, sin contexto heredado. Configuración solicitada:
  ADVANCED — GPT-5.6 Sol (`gpt-5.6-sol`) / High; efectiva unknown.
- Review inicial: `REQUIERE CORRECCIÓN`, F01–F04 obligatorios; opcionales ninguno.
- Única ronda dirigida: F01–F04 cerrados; veredicto final `APROBADO CON NOTAS`; cero
  findings obligatorios abiertos.
- Resultado final: `beneficio no probado`; no habilita release candidate.
- Informe sanitizado: `BENCHMARK_REPORT.md`; cierre: `06_CLOSURE.md`.
- Manifest final privado de evidencia firmado con SHA-256 y preservado fuera de Git.
- Durante la validación final cambió concurrentemente contenido ajeno bajo
  `docs/requirements/codex-skills-optimization/` y apareció otro requirement fuera de
  alcance. El coordinador no los modificó, revirtió ni incorporó; el digest inicial de ese
  árbol no puede confirmarse como estable al cierre.
