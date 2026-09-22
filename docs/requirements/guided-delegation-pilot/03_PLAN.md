# Plan técnico v1 — aprobado para implementación offline

Aprobación 2026-09-20: «Aprobar plan v1 y ejecutar P01–P04, sin lanzar workers reales ni publicar.»
Se conserva debajo el diseño presentado; el estado operativo vive en STATE y slices/.

## Objetivo y secuencia

Implementar una extensión opt-in de delegación nativa supervisada, sin motor propio.
Fuente del diseño: [EXECUTION_CONTRACT](EXECUTION_CONTRACT.md). Criterios y trazabilidad:
[01_ACCEPTANCE_CRITERIA](01_ACCEPTANCE_CRITERIA.md). No ejecutar por leer este plan.

Orden propuesto: P01 → P02 → P03 → P04. Son slices propuestas, no activas. Workflow
06 exige aprobación del plan antes de crear sus carpetas SPEC/brief/closure.
La aprobación futura cubre artefactos y pruebas offline, no iniciar workers reales.

## P01 — Coherencia, opt-in y responsabilidades

- Objetivo: una única jerarquía y autoridad de estado; inline sin cambios.
- Archivos: `03_DECISIONES_Y_NO_OBJETIVOS.md`, workflow 00/07/10, skills
  context-scout/requirement-state/slice-executor y templates de slice pertinentes.
- Preservar el no objetivo de orquestador propio y agregar únicamente opt-in supervisado.
- Introducir referencias breves al contrato instalado en `docs/guides/GUIDED_DELEGATION.md`
  (archivo propuesto); no copiar este
  requirement entero a AGENTS global ni tocar configuración personal.
- Reconciliar el registro local histórico de publicación solo contra evidencia
  verificable; conservar historia, sin reejecutar push/tag/release. Si no se dispone
  de evidencia suficiente, registrar discrepancia fuera del trabajo ejecutable.
- Criterios: AC01, AC02, AC04, AC09; validación V01, V03, V08, V09, V18.
- Perfil propuesto: heredar implementación de STATE; contexto transversal, N2.
- Resultado: contrato documentado y opt-in explícito, no workers lanzados.

## P02 — Validación offline del contrato y estados

- Dependencia: P01 aceptada.
- Objetivo: detectar incoherencias sin ejecutar modelos ni escribir proyectos.
- Archivos propuestos: `scripts/lib/check_execution.py`,
  `templates/slice/RUN.schema.json`, `tests/test_delegation_contract.py`; integración
  opt-in en `scripts/lib/runtime_doctor.py`/doctor. Nombres propuestos, aún inexistentes.
- Usar Python stdlib actual; schema legible y validación explícita focalizada, sin
  dependencia JSON Schema nueva. Tests comparan contrato y reglas para evitar deriva.
- Sin run/opt-in: compatibilidad legacy. Con run declarado: validar campos, identidad,
  referencias internas, estado y presupuesto; no interpretar ausencia como éxito.
- Validar contexto/base vigente, dependencias existentes/sin ciclos y evidencia de
  aceptación; límites de inferencia estática siempre visibles. No afirmar que un
  proceso se detuvo ni que un test pasó a partir de un campo escrito por el modelo.
- Criterios: AC02, AC03, AC05–AC08, AC12; escenarios V03–V07, V10–V17, V21–V23.
- Perfil propuesto: heredar STATE; review especial sobre rutas/recuperación.
- Resultado: checker offline y pruebas; no launcher ni supervisor nuevo.

## P03 — Procedimiento guiado y handoff acotado

- Dependencias: P01 y P02 aceptadas.
- Objetivo: conectar encargo → capacidad → entrega → aceptación en la sesión.
- Archivos: skill slice-executor (rama de coordinador y límites del encargo),
  model-router (referencia, no nuevo catálogo), `docs/guides/GUIDED_DELEGATION.md` y ejemplos mínimos de
  EXECUTION_BRIEF, run y CLOSURE_BRIEF.
- Reutilizar capacidades nativas disponibles; no agentes globales permanentes.
- Integrar selección de contexto, gating, checkpoint y reconciliación C01–C09.
- Identificar evidencia de capacidad requerida antes de dispatch. Si falta control
  necesario, inline o boundary explícito; no simular aislamiento con instrucciones.
- Casos UX: ausencia de runtime, override inseguro, pausa sin stop confirmado,
  entrega rechazada, presupuesto agotado y siguiente slice autorizada.
- Criterios: AC01–AC11; escenarios V01–V20 mediante fixtures/manual walkthrough.
- Perfil propuesto: heredar STATE; no cambio de modelo por edición documental.
- Resultado: procedimiento utilizable tras opt-in, sin inferencia real en esta slice.

## P04 — Regresión, evidencia y evaluación de readiness

- Dependencias: P02 y P03 aceptadas.
- Archivos: tests, CI existente, FILE_INDEX y evidencia del requirement.
- Incorporar pruebas offline a unittest/CI existente, sin duplicar workflows.
- Ejecutar suite completa proporcional y comprobar preservación de fixtures viejos.
- Review del diff/criterios/evidencia conforme workflow 08, sin preaprobar resultados.
- Criterios: AC12 y trazabilidad de todos; V01–V23.
- Resultado: readiness para solicitar experimento vivo, no afirmación de eficiencia
  ni disponibilidad real. Proponer tarea de bajo riesgo, capacidades y presupuesto
  concretos para una autorización posterior; no abrir workers automáticamente.

## Cambios realizados durante el diseño (no P01 ejecutada)

Solo documentos de este requirement, puntero/estado del proyecto, índice y una
referencia canónica en ARCHITECTURE. No se activan templates ni políticas operativas.
El resto de P01–P04 sigue pendiente.

## AI Strategy

Heredar [STATE → AI Strategy](STATE.md). Propuestas por slice, no modelo activo.
Escalar si aparece incertidumbre material de permisos/concurrencia; detener esa
ampliación porque escritura paralela y permisos nuevos no pertenecen al piloto.

## Riesgos, rollback y release

- Procedimiento no garantiza scheduler: declararlo en UX y evidencia.
- JSON adicional solo para delegación; no migrar proyectos inline ni slices cerradas.
- Markdown y checker no prueban comportamiento del runtime; experimento posterior separado.
- Preservar cambios locales. Si no hay Git, snapshot de archivos afectados y hashes;
  rollback de hunks propios, no reemplazo completo de estado con trabajo posterior.
- No cambiar versión ni mover tags existentes durante este diseño. Una eventual
  release nueva requerirá alcance de publicación y revisión de compatibilidad.

## Siguiente boundary

Tras self review sin obligatorios pendientes, pedir:

`Aprobar plan v1 y ejecutar P01–P04, sin lanzar workers reales ni publicar.`

Esa respuesta aprueba criterios funcionales, contrato y plan v1, y autoriza su
implementación offline. Luego crear slices según workflow 06 y continuar P01.
