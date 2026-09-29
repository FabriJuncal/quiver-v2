# Plan técnico v1 — histórico de trabajo por proyecto

**Estado: aprobado y ejecutado el 2026-09-25.** Fuente: petición de
implementación del 2026-09-25, elección prospectiva y USD real solo con evidencia;
Kev propuesto para categorizar. Criterios [H-01–H-10](01_ACCEPTANCE_CRITERIA.md).

## Alcance y contrato

Extender el ledger privado opt-in de `scripts/lib/plan_usage.py` sin migrar
bindings existentes. `bind` acepta `work_kind` y `work_id` juntos; valores ausentes
conservan contrato v1 y quedan fuera del histórico prospectivo. `work_id` es opaco,
sin título/prompt. Un mismo trabajo puede tener varios bindings con categorías
distintas, cada uno con su propia frontera explícita.
El histórico lee solo el ledger, filtra por `project_id`, usa una revisión v2
persistida (la última) por binding y agrupa por `work_id` y categoría. Revisiones
anteriores siguen consultables, pero no se vuelven a sumar.

Tokens: conservar seis contadores nativos y respuestas; `reasoning_output_tokens`
es subconjunto de output. Reportar número de bindings sin snapshot y estados
incompletos. Tiempo: sumar únicamente `elapsed_seconds`/`unpaused_seconds`
derivados de límites explícitos, con subtotal y conteo unknown; los intervalos
superpuestos no son tiempo activo único. `active_time` sigue unknown.

USD: comando explícito para adjuntar importe directo en USD a un binding marcado,
con ID de evidencia opaco único, referencia de comprobante sin ruta/URL sensible,
`complete_for_binding` y Decimal textual. Se conserva el origen como declaración
del usuario: el comando valida integridad/formato y unicidad, no inspecciona ni
certifica el comprobante. Sin evidencia o con cobertura parcial, total USD
unknown y subtotal conocido separado; sin inferencia desde tarifas sintéticas.

Kev: comando `suggest-kind` opcional, solo `http://127.0.0.1`/`localhost`, resumen
breve por stdin y respuesta `choice` validada entre cinco categorías. Devuelve
sugerencia/probabilidades, sin escribir el ledger ni confirmar etiqueta. No
instalar Kev, modelos, servidor ni dependencias; fixture de transporte artificial.
No leer conversaciones ni sesiones reales. El flujo manual funciona sin Kev.

## Pasos y slices

1. **H01 — captura y agregación:** metadatos prospectivos de binding, histórico
   JSON/texto, cobertura de tokens/tiempo y compatibilidad v1/v2. Fixtures
   de proyectos, categorías, revisiones y unknowns.
2. **H02 — evidencia USD y Kev opcional:** declaración directa de costos sin
   duplicados, sugerencia local sin atribución automática, guía, CLI y fixtures.
3. Review N2 del diff y cierre con estado. Sin acceso a fuente real; no publicar.

## Validación y rollback

- T2: tests de agregación exacta, reimport/revisión, proyecto cruzado, legacy,
  unknowns, costo declarado duplicado/parcial, errores de Kev, privacidad y CLI.
- Regresiones afectadas de `plan_usage`; sintaxis/esquema, enlaces, estado y
  `git diff --check`. No repetir gates S01–S03 ni tocar sus fuentes.
- Rollback: no invocar comandos nuevos; los metadatos adicionales son opt-in y
  los reportes v1/v2 existentes permanecen compatibles. Conservar ledger.
- Parar ante evidencia de corrupción, migración necesaria, acceso real no
  autorizado o requisito de facturación externa.

AI Strategy: [STATE](STATE.md#ai-strategy). Plan N2 y ejecución BALANCED,
review crítico ADVANCED recomendado; modelo efectivo no verificado.
