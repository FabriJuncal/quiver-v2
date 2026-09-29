# Auditoría local — medición por plan

Fecha: 2026-09-24. Evidencia estática y pruebas offline expresamente identificadas.
No se midió el consumo de esta auditoría. Tokens, USD y duración de esta sesión:
**no disponibles**. No se infieren desde bytes, tiempo de herramientas o identidad declarada.

## 1. Baseline y alcance

- Repositorio: Quiver V2; distribución local AI Software Factory 2.3.0-rc.2,
  según [FACTORY_VERSION](../../../FACTORY_VERSION.md).
- Rama: `docs/archive-closed-requirements-2026-09-24`.
- HEAD: `2b92c74602bf244e9a3e03829e5c07f2b233e8a4`.
- Antes de esta sesión: PROJECT_STATE.md modificado, 23 adiciones/19 eliminaciones;
  registra el merge documental previo. Ese cambio no pertenece a esta auditoría.
- 72 archivos untracked previos: 24 en branch-aware-discovery y 48 en
  codex-skills-optimization. Solo inventario/hashes para preservación, no reutilización
  de su evidencia privada. Digest agregado de paths y SHA-256, en orden Git:
  `50e4bcd22db6ba653f8d990929d02f5863269374adccabccbfb39bcb58500fdd`.
- SHA-256 inicial de PROJECT_STATE.md:
  `21fe14255097f6900294b52930ac1aee11ef62449e7cdb7871af6d9a6115211f`.
- No fetch, cambio de rama ni dependencia del remoto Quiver. La anotación previa de
  PR #5 mergeado se conserva; no se volvió a verificar ese PR en esta auditoría.
- No AGENTS.md en la raíz ni en los ancestros inspeccionados. Aplican las instrucciones
  globales entregadas por el usuario; los AGENTS de templates/examples no gobiernan
  esta raíz. FILE_INDEX.md es el índice existente; no hay docs/INDEX.md local.
- Alcance de búsqueda: scripts/, tests/, templates/, config/, workflow/, README,
  FILE_INDEX, FACTORY_VERSION, conceptos y guías de ejecución/routing/continuidad.
  No se abrió el repositorio piloto, auth/config personal ni sesiones personales.

Comando de preservación, acotado a los dos grupos preexistentes:

```bash
git ls-files --others --exclude-standard -z docs/requirements/branch-aware-discovery docs/requirements/codex-skills-optimization | xargs -0 shasum -a 256 | shasum -a 256
```

## 2. Gobierno y ejecución realmente observados

La [jerarquía](../../../docs/concepts/SOURCE_OF_TRUTH.md) distingue hechos de
autorizaciones: evidencia/código → STATE del requirement → PROJECT_STATE → artefactos
aprobados → documentación → recap/chat. Código existente no concede permiso.
[Contrato 00](../../../workflow/00_SHARED_CONTRACT.md),
[review de plan 05](../../../workflow/05_PLAN_REVIEW.md) y
[resume 10](../../../workflow/10_RESUME.md) exigen aprobación humana y autorización
de ejecución separadas. Esta sesión está autorizada para elaborar propuestas, no
para aprobarlas. Se usa la metodología de esta distribución, no otra Factory histórica.

Hecho: scripts/asf:4 llama scripts/asf.sh. En asf.sh:11–16 se resuelve la intención
de perfil; :57–64 construye el comando y permite dry-run; :66–72 espera el proceso
Codex y conserva su código de salida. No consume eventos de uso ni liga un plan.
El launcher controla arranque/espera, no las llamadas, turnos o aceptación interna.
También se puede iniciar Codex fuera del launcher; la Factory orienta esa sesión
mediante instrucciones, Skills y documentos. El host efectivo de esta conversación
no se demuestra inspeccionando ese launcher.

Sesión/thread, turno, solicitud y plan no son equivalentes: un turno puede contener
varias respuestas del proveedor; una sesión puede abarcar varios turnos; un plan
puede necesitar sesiones e intentos distintos. Salir de Codex no acepta el plan.
workflow/07_EXECUTE_SLICE.md y workflow/09_CLOSURE.md son el flujo documental de
trabajo/cierre; no hay un reloj contable de pausa/reanudación en las áreas buscadas.

La delegación tiene contratos opt-in v1/v2/v3, no un scheduler activo. RUN.schema.json
contiene requirement_ref, slice_id, assignment_id, attempt_id, plan_version y
refs con hashes (:14–72), configuración solicitada/observada y runtime thread/response.
No representa todas las sesiones inline. No se activaron agentes ni se deduce
paralelismo efectivo de las fixtures o del inventario de agentes del entorno.

## 3. Matriz de capacidades

Los estados describen el alcance declarado, no certificaciones universales.

| CAPACIDAD | ESTADO | EVIDENCIA | BRECHA | ACCIÓN PROPUESTA |
|---|---|---|---|---|
| Gobierno, aprobaciones y continuidad documental | EXISTE Y VERIFICADO | workflow/00,05,06,10; templates/requirement/STATE.md; lectura | Obediencia del runtime no garantizada por documentos | Reutilizar, no duplicar STATE |
| Comando de inicio interactivo en dry-run | EXISTE Y VERIFICADO | scripts/asf.sh:57–64; dry-run ejecutado | Arranque real y disponibilidad no probados | No modificar launcher |
| Control del consumo durante la sesión habitual | NO ENCONTRADO EN EL ALCANCE REVISADO | búsqueda usage/telemetry/token_count/session en scripts, templates, tests y guías | Wrapper no observa turnos ni requests | Observador externo opt-in |
| Identidad requirement/slice/intento delegados | EXISTE PARCIALMENTE | RUN.schema.json:14–72,369–465; check_execution.py:19–26 | Falta identidad contable inline/proyecto/ejecución y binding de sesión | Reusar refs/IDs; agregar solo identidad faltante |
| Aceptación separada del fin de proceso | EXISTE Y VERIFICADO | RUN transitions y workflow/08,09; fixtures verificadas | No unida al uso inline | Referenciar aceptación, no inferirla |
| Normalización input/output/cache/reasoning | EXISTE Y VERIFICADO | context_economy.py:549–584; tests E04 ejecutados | Contrato Responses, no adaptador de rollout; cache-write no soportado | Reusar semántica solo tras mapear y validar fuente |
| Tokens estimados para contexto | EXISTE Y VERIFICADO | context_economy.py:130–162; test E01 | utf8-bytes/4-ceiling no estima consumo de un plan | No utilizar como predictor ni facturación |
| Transporte de ayudante textual | EXISTE, NO VALIDADO | context_economy.py:469–546; tests con transporte falso | No cliente real ni prueba de integración | No habilitar para medir coordinador |
| Escritura local segura | EXISTE PARCIALMENTE | context_economy.py:378–411; guard duradero probado | No ledger, transacción uso/checkpoint ni lock entre importadores | Adaptar patrón; probar concurrencia/recuperación |
| Uso por respuesta del runtime candidato | EXISTE, NO VALIDADO | fuente oficial fijada E-N1/N2/N3 abajo | No se leyó muestra del host habitual | Cualificación previa S01; recorrido real S03 |
| Tokens por plan con deduplicación | NO ENCONTRADO EN EL ALCANCE REVISADO | scripts/lib, RUN y pruebas revisadas | Acumulación y asignación contable inexistentes | S01 |
| Costos observados/estimados aislados | EXISTE PARCIALMENTE | normalize_observations:587–629 | Recibe float externo; no motor de precios, tier, moneda/versionado completo | S02; no usar como libro contable sin adaptar |
| Tarifario reproducible y conciliación | NO ENCONTRADO EN EL ALCANCE REVISADO | búsqueda price/pricing/cost en scripts/config/tests | No snapshots comerciales ni facturas | Snapshot explícito futuro; facturado unknown |
| Duración del plan, actividad y espera | EXISTE PARCIALMENTE | duration_ms externo en normalize_observations | No lifecycle de plan; activo/espera no observados | Límites explícitos; unknown lo demás |
| Modelo/pago efectivos de esta sesión | NO VERIFICABLE / BLOQUEADO | SESSION_PREFLIGHT; no evidencia de runtime autorizada | Intención no prueba backend ni facturación | No introspección; conservar unknown |
| Tests offline y salida guiada | EXISTE Y VERIFICADO | 19 tests CE-v1; guided_status:632–639 | No capturan sesión interactiva | Reutilizar unittest; separar hitos offline/real |
| Predicción y calibración por historial | NO ENCONTRADO EN EL ALCANCE REVISADO | alcance de búsqueda indicado | Aún no hay historial atribuible verificado | Diferir |

## 4. Contratos nativos y versiones

Paquete local en PATH: `@openai/codex` **0.156.1**, obtenido leyendo su package.json
y el symlink del ejecutable, sin iniciar sesión. No demuestra versión del host App,
servidor de esta conversación, modelo efectivo ni modalidad de pago.
Tag público rust-v0.156.1 resuelto por API de lectura a
`b412ff32c417f855c2b2d1581b77058eed87c84b` (tag anotado no firmado según API).
No se verificó equivalencia binaria mediante checksum del proveedor.

Fuentes primarias inspeccionadas, no tests upstream ejecutados:

- **E-N1:** [protocol.rs:2235–2339](https://github.com/openai/codex/blob/b412ff32c417f855c2b2d1581b77058eed87c84b/codex-rs/protocol/src/protocol.rs#L2235): TokenUsage, TokenUsageRecord, TokenUsageInfo.
  Registro por respuesta con IDs de thread/turn/session/root-turn/response, uso de
  esa respuesta y acumulados separados. TokenCountEvent no ofrece la misma identidad.
  SessionMeta (:3117) declara cli_version y filiación; TurnContext (:3287) permite turn_id.
  ThreadSettingsApplied (:2194) contiene modelo/proveedor/tier configurados, no una
  prueba universal de modelo facturado tras rerouting.
- **E-N2:** [serialización](https://github.com/openai/codex/blob/b412ff32c417f855c2b2d1581b77058eed87c84b/codex-rs/history/src/rollout_payload.rs#L21): `token_usage_record` es un tipo persistido; no extraer uso de textos del asistente.
- **E-N3:** [política de persistencia](https://github.com/openai/codex/blob/b412ff32c417f855c2b2d1581b77058eed87c84b/codex-rs/rollout/src/policy.rs#L10) conserva registros de uso y marcadores de turno; [test oficial](https://github.com/openai/codex/blob/b412ff32c417f855c2b2d1581b77058eed87c84b/codex-rs/core/tests/suite/token_usage_rollout.rs) distingue varias respuestas en un turno, resume y una respuesta sin uso. Inspección, no ejecución.
- **E-N4:** [recorder](https://github.com/openai/codex/blob/b412ff32c417f855c2b2d1581b77058eed87c84b/codex-rs/rollout/src/recorder.rs): JSONL, buffering/flush y almacenamiento/compression evolucionables. No asumir que un evento ausente es cero o que EOF equivale a cierre.
- **E-N5:** [modo no interactivo](https://learn.chatgpt.com/docs/non-interactive-mode) documenta salida JSON con usage de turno; [App Server](https://learn.chatgpt.com/docs/app-server) documenta eventos de uso y lifecycle. No se comprobó attach pasivo al host actual. No se eligen para sustituir el flujo interactivo solo por facilidad de medición.

La fuente contable recomendada es **token_usage_record por respuesta en un rollout
explícitamente autorizado y compatible**, no sumar a la vez TokenCount, App Server
y ccusage. Si el formato/host real no lo expone, el gate inicial de S01 impide
implementar y S03 no puede validar integración; no hay fallback
silencioso a acumulados heurísticos, ni obligación de construir otro adaptador.
Una sesión comprimida, efímera, revertida o con historial heredado no soportado debe
advertirse antes de afirmar cobertura. Primera versión: JSONL plano, raíz inline,
sin subagentes ni forks; otras modalidades quedan incompletas/no soportadas.

## 5. Candidatos: decisión acotada

Inspección externa 2026-09-24, sin instalaciones ni ejecución. No se verificaron
precios comerciales vigentes. Una licencia permisiva no prueba compatibilidad funcional.

| Candidato | Función y compatibilidad | Versión/licencia revisada | Costo, riesgos y alternativa | Decisión |
|---|---|---|---|---|
| Contratos nativos Codex | Contadores con identidad; adaptador Python local posible, sin SDK | 0.156.1 / commit E-N1; paquete declara Apache-2.0; revisar notices si se copia código | Mantenimiento por versión; formatos/host distintos. Alternativa App Server supone otra integración | Adaptar contrato, no copiar runtime; candidato principal sujeto a S03 |
| Primitivas Quiver | Normalización, hashes, escritura y estado; Python stdlib ya existe junto a Bash | HEAD local; LICENSE MIT leído | No resuelven ledger ni atomicidad de varios archivos; float no apto para tarifa exacta | Reutilizar/adaptar acotadamente |
| ccusage | Importador/contraste de logs; adaptador revisado es Rust, no biblioteca Python embebible | commit `3fec3672c6a2a98ff3f627f091311bdd7f021613`; apps/ccusage/LICENSE MIT leído | Recorre histories, usa acumulados/fallbacks/modelos y tarifas propias; ampliaría acceso/dependencias. Alternativa contrastar invariantes nativas y fixtures | Diferir instalación; solo referencia secundaria, nunca sumar su total al ledger |
| pydantic/genai-prices | Motor/dataset de tarifas; paquete Python >=3.10 compatible con intérprete del tooling, integración no probada | commit `f3a1cfe5f33db70ceda3149ff86725efd36ee573`; MIT leído; versión por tag, no inferida | Dependencias pydantic/httpx2, matching de aliases y actualización; mantenimiento/licencia del dataset a revisar. Alternativa snapshot mínimo explícito + Decimal stdlib | Diferir dependencia; tomar diseño de tarifas fechadas, sin proveedor automático |

Fuentes ccusage: [parser fijado](https://github.com/ccusage/ccusage/blob/3fec3672c6a2a98ff3f627f091311bdd7f021613/rust/adapters/codex/src/parser.rs), [manifest](https://github.com/ccusage/ccusage/blob/3fec3672c6a2a98ff3f627f091311bdd7f021613/rust/adapters/codex/Cargo.toml), [guía](https://ccusage.com/guide/codex/).
La guía declara soporte experimental; sus fallbacks de precio/configuración no
satisfacen el contrato de unknown de esta propuesta. No se adopta su política.

Fuentes genai-prices: [paquete](https://github.com/pydantic/genai-prices/blob/f3a1cfe5f33db70ceda3149ff86725efd36ee573/packages/python/pyproject.toml), [calc_price](https://github.com/pydantic/genai-prices/blob/f3a1cfe5f33db70ceda3149ff86725efd36ee573/packages/python/genai_prices/__init__.py), [types](https://github.com/pydantic/genai-prices/blob/f3a1cfe5f33db70ceda3149ff86725efd36ee573/packages/python/genai_prices/types.py).
Admite timestamp y Decimal; defaults/matching y tratamiento de faltantes necesitarían
una capa estricta. No se validó cobertura de los modelos del catálogo local.

Si se reutiliza material externo después: fijar revisión, comprobar licencia/notices
de código y datos, conservar atribuciones y pruebas de compatibilidad. Ninguna
actualización online automática ni precio inferido por nombre parecido.

Referencias posteriores, **solo identificadas, no auditadas ni dependencias**:
[Costea](https://github.com/memovai/costea) para historial/comparación;
[agent-cost](https://github.com/devinat1/agent-cost) para experiencia previa;
[agent-cost-bench](https://github.com/aws-samples/sample-agent-cost-bench) para metodología;
[MAPIE](https://github.com/scikit-learn-contrib/MAPIE) para intervalos si hay datos.
Versiones, licencias y beneficios de esas cuatro referencias: pendientes de verificar
solo cuando una decisión posterior lo necesite. Paneles/límites también diferidos.

## 6. Hallazgos por impacto

| ID | Impacto / tipo | Evidencia y conclusión | Tratamiento |
|---|---|---|---|
| H01 | Alto / hecho | No vínculo contable plan ↔ fuente en el código revisado; RUN solo cubre encargos opt-in | S01: binding previo explícito; nunca última sesión/cwd/horario |
| H02 | Alto / hecho e incertidumbre | Existe contrato público por respuesta; disponibilidad en host habitual NO VERIFICADA | Gate de formato antes de implementar S01; S03 prueba prospectiva completa |
| H03 | Alto / hecho | Registro de uso no prueba modelo efectivo/pago; normalize_observations acepta costo externo | Separar identidad/precio/equivalente/facturado; unknown conservador |
| H04 | Alto / inferencia de riesgo | Replays, subagentes, acumulados y dos importadores pueden duplicar | Fuente única, exclusión explícita, unicidad y transacción |
| H05 | Alto / hecho | Rollout puede contener conversación/código; no es log inocuo de contadores | Allowlist de archivo y campos, privado fuera de Git, sin copia de contenido |
| H06 | Medio / hecho | Guard de despacho duradero existe; no ledger transaccional | Reusar patrón, no confundir guard con solución contable |
| H07 | Medio / inferencia | Datos de un solo host/tarea no validan predictor | Diferir estimación y cualquier promesa de precisión |

Hipótesis a refutar: una lectura selectiva del rollout enlazado puede observar el
flujo habitual sin modificarlo. La evidencia estática la hace plausible, no probada.
No hay bloqueo para aprobar el plan; sí cualificación mínima de fuente antes de
implementar S01 y validación prospectiva completa antes de cerrar S03.

## 7. Comprobaciones y límites

Intérpretes observados: `python3` resuelve Python 3.9.6; `python3.14` resuelve
Python 3.14.4 ya instalado. La primera invocación acotada de Doctor.state con
python3 falló al importar tomllib; repetir con python3.14 produjo **State errors: 0**
sobre PROJECT_STATE y STATE de este requirement. Sin instalación ni cambio de PATH.
No confundir este diagnóstico de entorno con un fallo del nuevo observador, aún inexistente.

Ejecutadas: `python3 -I -B tests/test_context_economy.py` — **19 tests OK**;
repetidas con `python3.14 -I -B tests/test_context_economy.py` — **los mismos 19 OK**.
Escrituras de las fixtures en TemporaryDirectory, transporte falso, sin SDK/red.
`bash scripts/asf balanced --dry-run` — **exit 0**, argumentos esperados sin sesión.
`git diff --check` — **PASS** antes de editar; controles documentales finales en HANDOFF.
Git status/diff/baseline y digest de los 72 archivos obtenidos por lectura.

Inspeccionados, no ejecutados: tests runtime guardrails (algunos crean commits en
repos sintéticos), suite completa, check-release, doctor global y tests upstream.
No se ejecutaron porque exceden el control necesario o inspeccionan áreas ajenas;
para el estado nuevo se usa solo Doctor.state sobre los dos archivos canónicos.
La prueba de launcher no acredita disponibilidad/modelo/reasoning efectivos.
Sin pruebas del host real, costos comerciales, facturas, cobertura porcentual ni
estimaciones cuantitativas de slices. No actividad paga creada para obtener muestras.
