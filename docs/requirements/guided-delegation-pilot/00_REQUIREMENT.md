# Guided Delegation Pilot — diseño

## Petición y autorización

2026-09-20: después de la auditoría del proyecto, el usuario indicó «avanza con los
pasos recomendados». El próximo paso recomendado fue especificar y revisar un
piloto de delegación acotada sobre los contratos existentes, sin habilitar todavía
escritores paralelos ni automatización persistente.

Esta etapa autoriza análisis, documentos, revisión y comprobaciones locales. No
autoriza por sí sola ejecutar workers, cambiar configuración personal, publicar,
crear un scheduler o aprobar anticipadamente el plan detallado producido aquí.

## Objetivo

Definir una extensión mínima donde la IA elija inline o delegación, conserve la
responsabilidad de aceptación y guíe al usuario sin exigir conocimiento de agentes.
No organizar la Factory alrededor de developers permanentes ligados a modelos.

## Baseline inspeccionado

Distribución 2.2.2; esta carpeta no tiene Git. El nombre de carpeta no determina
versión. No confundir distribución, checkout de publicación, instalación y sesión.

| ID | Evidencia existente | Necesidad del piloto |
|---|---|---|
| AUD-01 | `workflow/00_SHARED_CONTRACT.md`: Finalization Gate documental | No prometer supervisión durable; verificar eventos antes de avanzar |
| AUD-02 | `templates/requirement/STATE.md`: Current slice singular; SPEC con dependencias textuales | Mantener secuencial; validar referencias y elegibilidad |
| AUD-03 | `skills/core/slice-executor/SKILL.md`: actualiza STATE y continúa slices | Solo coordinador escribe estado central y elige siguiente trabajo |
| AUD-04 | Dos jerarquías en ARCHITECTURE/SOURCE_OF_TRUTH; publicación antigua activa solo en esta distribución | Una referencia canónica; reconciliar vigencia sin repetir publicaciones |
| AUD-05 | Doctor: bloque global antiguo/sin versión y perfiles opcionales ausentes | Preflight por capacidad material, sin reinstalar silenciosamente |
| AUD-06 | Catálogo, launcher y perfiles existentes; sin registro de intentos | Reutilizar routing; distinguir intención de observación |
| AUD-07 | Context Scout carga contexto mínimo, pero no identifica una entrega por revisión | Context manifest referenciado desde el brief |
| AUD-08 | Review con findings/evidencia; sin vínculo explícito intento/base/integración | Aceptación por coordinador sobre revisión identificada |

La publicación histórica no se reabre. En la auditoría se observó estado completed
en el checkout de publicación y un registro in-progress en esta distribución;
reconciliar requiere conservar esa procedencia y verificar evidencia, no elegir
automáticamente la copia que habilita ejecutar.

## Alcance del diseño

- Contrato propuesto de asignación, contexto, entrega, aceptación y recuperación.
- Inline y delegación secuencial opt-in con un worker como máximo.
- Ownership central, estados mínimos, presupuesto de intentos y UX de overrides.
- Plan de implementación, slices propuestas y matriz de pruebas offline.
- Diferenciar criterios de diseño satisfechos de comportamiento aún no implementado.

## Fuera de alcance

Escritura directa del worker en el proyecto durante el primer piloto, paralelismo,
worktrees automáticos, agentes recursivos, daemon, backend, colas, UI propia, nuevos
modelos hardcodeados, cambios globales, inferencia paga, release y publicación.
Fases posteriores requerirán evidencia del piloto y alcance nuevo.

## Riesgo

N2 para el contrato propuesto: afecta autorización, evidencia y continuidad. Los
cambios de esta etapa son documentales y reversibles. La recomendación es T2
focalizado para la implementación futura, no una auditoría de seguridad completa.
