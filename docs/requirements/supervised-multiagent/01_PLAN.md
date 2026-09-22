# Plan técnico v1 — aprobado para implementación offline

Plan y S01–S04 aprobados el 2026-09-21 por petición explícita del usuario.
Sin agentes reales, configuración habitual ni publicación. Orden S01 → S02 → S03 → S04.
Crear SPEC/EXECUTION_BRIEF/CLOSURE de las slices al autorizar ejecución, reutilizando
templates existentes, no otro sistema de tareas. Criterios en 00_SCOPE_AND_DECISION.md;
trazabilidad y entradas/salidas verificables en 02_TEST_PLAN.md.

## S01 — Contrato de supervisión y límites

- Extender `docs/guides/GUIDED_DELEGATION.md` como fuente operativa canónica con
  política `supervised-audited-v1`; referencias breves en workflow 00/07/10 y skills
  context-scout, requirement-state y slice-executor solo donde cambie el procedimiento.
- Conservar política estricta histórica. Explicar qué garantía se reemplaza y cuáles
  siguen obligatorias. No declarar compatibilidad del runtime usando pruebas estáticas.
- Mantener catálogo/model-router: elegir delegación por beneficio, modelo por tarea;
  control solicitado distinto del observado. Sin nuevos nombres de perfiles.
- Añadir UX para informe limpio, incidente, desconocido y fallback inline, respetando
  ownership: no continuar sobre archivos compartidos si podría quedar un hijo activo.
- Salida: contrato revisable; AC01, AC02, AC06, AC08, AC09, AC10.

## S02 — Evolución compatible del registro y checker offline

- Extender `templates/slice/RUN.schema.json` y `scripts/lib/check_execution.py`;
  preservar lectura/validación v1. Proponer v2 explícita para política nueva; seleccionar
  versión sin ampliar innecesariamente el subconjunto JSON Schema del validador.
- V2: policy, aceptación del riesgo de supervisión referenciada, refs de manifest
  inicial/final, informe de auditoría e incidentes. Controles separados: exigencia,
  mecanismo declarado, observación y evidencia; unknown explícito. Los nombres
  definitivos se fijan en schema durante S02, no duplicar contratos aquí.
- Base/project_write_scope vacío y no_recursion true siguen expresando límites,
  NO prueba de capacidades. No usar booleans authored por el hijo como permisos reales.
- Evidencia relativa al proyecto y hasheada; ubicaciones temporales de la copia se
  registran solo en evidencia local, no autorizan lecturas arbitrarias por el checker.
- Checker comprueba coherencia de datos; no crea copias, aplica patches, ejecuta
  entregas ni despacha. Validación de registros no emite READY para runtime.
- Reutilizar integración doctor y estados existentes. Versiones desconocidas se
  rechazan explícitamente; registros v1 no se reescriben.
- Salida: contrato compatible y tests unitarios dirigidos; AC01, AC02, AC05–AC07, AC09.

## S03 — Auditoría local y casos sintéticos

- Añadir utilidad stdlib pequeña de inventario/comparación, sin proceso persistente,
  con CLI de solo lectura y salida por stdout. Nombre propuesto:
  `scripts/lib/audit_workspace.py`. El coordinador persiste evidencia, no el ayudante.
- Comparar paths/tipos/hash/permisos, incluyendo archivos nuevos; rechazar entradas
  ambiguas, symlinks/hardlinks, rutas fuera de raíz y fallos de lectura; no seguir
  enlaces ni ejecutar contenido. Detectar cambios durante lectura cuando sea posible;
  no prometer snapshot atómico ni defensa completa frente a carreras hostiles.
- Tests crean copias sintéticas con directorios temporales; no copiar automáticamente
  proyectos reales. Registrar manifest exacto; secretos requieren revisión de contenido,
  no solo blacklist de nombres. Sin filtros vendidos como detector completo.
- Reutilizar `tests/delegation_fixture.py`, extender
  `tests/test_delegation_contract.py` y añadir tests de auditoría si mejora legibilidad.
  Preservar ejemplo v1 y añadir ejemplo v2 sintético separado, no evidencia viva falsa.
- Salida: detección reproducible y rechazo de entregas contaminadas; AC03–AC05, AC07, AC10.

## S04 — Integración, documentación y cierre offline

- Doctor distingue datos válidos, incidente y controles vivos no verificados. No lee
  ubicaciones externas por referencias arbitrarias ni modifica el proyecto inspeccionado.
- README, FILE_INDEX y ejemplo explican estado experimental/no validado en vivo;
  CLI/AGENTS global/model profiles no se activan ni cambian. Sin bump/tag/release.
- Integrar tests rápidos en CI existente solo si no quedan ya cubiertos por unittest
  discover; no exigir servicios ni agentes para CI.
- Ejecutar matriz, regresión y review del diff: self review identificada, no fingir
  independencia. Revisión dedicada del control crítico antes de piloto, separadamente
  autorizada; si se reclasifica N3, aplicar workflow de review sin rebajar requisitos.
- Entregar propuesta futura de piloto sintético con gates pendientes concretos, no
  desbloquearlo por completar estas slices. AC01–AC10.

## Fronteras de autorización

1. Ahora: documentos + diseño de pruebas + baseline existente; aprobado.
2. S01–S04: cambios offline descritos; aprobación y ejecución otorgadas el 2026-09-21.
3. Piloto vivo: permiso separado, una ejecución sintética y controles restantes
   verificados en ese runtime; si alguno falta, delegación sigue deshabilitada.
4. Release: validaciones operativas, paquete y autorización de publicación separados.

Si solo se dispone de instrucciones para impedir acciones externas o recursión,
S01–S04 pueden completarse offline, pero el piloto no puede lanzarse bajo este alcance.
No proponer Full Access ni otro cambio personal para forzar el resultado.
