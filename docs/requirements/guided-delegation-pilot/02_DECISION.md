# Decisión — plan v1 y ejecución offline aprobados

## Selección

La instrucción «avanza con los pasos recomendados» acepta avanzar con el diseño
gradual: inline por defecto, un coordinador responsable y ejecutores temporales.
No equivale a aprobación humana anticipada del contrato/plan v1 aún no presentado.

| Alternativa | Tiempo/complejidad/consumo relativo | Trade-off |
|---|---|---|
| A. Piloto secuencial opt-in, workers entregan análisis o propuestas; coordinador aplica | Menor que B; algo mayor que continuar solo inline | Permite estudiar delegación sin escritores concurrentes; aún requiere supervisión de sesión |
| B. Scheduler durable y escritores paralelos ahora | Mayor en las tres dimensiones | Mayor autonomía potencial, riesgos de aislamiento/recuperación sin baseline medido |
| C. Mantener solo inline | Menor costo inmediato | No permite evaluar empíricamente los beneficios de delegación |

Recomendación para implementación futura: A. B está fuera del alcance aprobado;
C permanece como fallback completo, no como error del sistema.

## Límites propuestos

- Un worker por vez y ninguna delegación recursiva.
- El worker no modifica el proyecto: devuelve análisis o propuesta de patch.
- El coordinador valida y aplica mediante herramientas existentes; no hace eval de texto recibido.
- Sin backend ni supervisor propio. No prometer ejecución después de cerrar la sesión.
- No instalar custom agents ni cambiar configuraciones globales por defecto.
- Reutilizar perfiles y modelo/reasoning del catálogo; AI Strategy normativa en STATE.
- T2 futuro: validación offline de contratos/estados, escenarios de errores y regresión existente.
- No inferencia paga ni experimento vivo sin autorización específica adicional.

## Compatibilidad

El no objetivo vigente de construir un orquestador propio se mantiene. El futuro
opt-in propondrá una excepción acotada para delegación nativa supervisada, no una
autorización general a agentes. La documentación de este requirement no activa esa
excepción ni tiene prioridad sobre instrucciones vigentes.

No modificar retrospectivamente slices cerradas ni metadatos de release. No asignar
nueva versión hasta que exista una implementación verificable y alcance de release.

## Registro de aprobaciones

- Diseño/revisión documental: autorizado por el usuario, 2026-09-20.
- Criterios funcionales/contrato detallado v1: aprobados, 2026-09-20.
- Plan detallado v1: aprobado, 2026-09-20.
- Implementación P01–P04: autorizada por «Aprobar plan v1 y ejecutar P01–P04, sin lanzar workers reales ni publicar.»
- Ejecución real de workers/publicación: excluida de la aprobación P01–P04.
