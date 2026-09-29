# Decisión técnica propuesta — D01 / v1

**Estado: D01 aprobada por el usuario el 2026-09-24, para plan v1.**
La aprobación documental no autoriza ejecución. Criterios:
[v1](01_ACCEPTANCE_CRITERIA.md); registro de versión/alcance en [STATE](STATE.md).

## Opción recomendada

Observador local invocado bajo demanda desde la sesión habitual, fuente nativa
por respuesta enlazada explícitamente, Python stdlib ya presente en el tooling,
ledger JSON privado con reemplazo atómico y exclusión de escritor. No daemon,
servidor, SDK, gateway, nuevo entorno Python ni cambio del launcher/router.

El primer valor es conocer tokens atribuibles y faltantes. USD puede seguir
desconocido en sesiones donde no existe evidencia de modelo/tarifa/pago aplicable.
No se presenta un equivalente API como gasto de suscripción ni como factura.

## Por qué y alternativas

| Alternativa | Trade-off / resolución propuesta |
|---|---|
| D01: ledger JSON único por almacén privado + lock local | Sigue patrones existentes; uso y checkpoint en un único snapshot. Reescribe estado y necesita límites explícitos; suficiente para piloto acotado de medición, sin benchmark |
| SQLite stdlib | Transacciones/índices útiles a mayor escala; agrega esquema/migraciones y operación no necesarios todavía. Diferir si tamaño/concurrencia reales exceden contrato JSON |
| App Server o exec JSON como flujo obligatorio | Datos nativos útiles, pero no demuestran captura de la sesión habitual y pueden cambiar experiencia/arranque. No seleccionar |
| ccusage como contabilidad principal | Historial amplio, fallbacks y semántica distinta; no liga aceptación del plan. No seleccionar |
| genai-prices instalado desde el primer slice | Compatible con Python, pero trae dependencias y matching automático. Diferir; snapshot explícito mínimo con procedencia para S02 |

## Límites de la decisión

La compatibilidad real sigue abierta, no el diseño completo. Cualificar contrato y
campos de una fuente real autorizada al inicio de S01, antes de implementar, sin
atribuir uso pasado; validar el recorrido prospectivo completo en S03. Si falla, detener ese hito y
presentar evidencia concreta; no construir otro backend silenciosamente. Sin
fuente real compatible, no cerrar la primera entrega como medición integrada.

Un único almacén privado seleccionado es el dominio de unicidad de bindings;
no se promete coordinación entre almacenes separados o hosts. Primer adaptador
sin forks/subagentes, formatos comprimidos ni compatibilidad histórica general.

## Testing, estrategia y autorizaciones

T2 reforzado aprobado; [STATE → AI Strategy](STATE.md#ai-strategy) es la única
resolución normativa de perfiles. No configuración efectiva ni medición de ahorro.
La petición del usuario autoriza auditoría/plan/handoff y comprobaciones compatibles.
Criterios v1, D01, T2 reforzado y plan v1: aprobación humana registrada en STATE.
Implementación S01–S03, acceso a fuente real, delegación y publicación: no autorizados.
