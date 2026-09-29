# Execution Brief — S03

## AI Execution Profile

Inherit: `../../STATE.md` → AI Strategy / S03. ADVANCED — GPT-5.6 Sol
(`gpt-5.6-sol`) / High; fallback GPT-5.6 Terra (`gpt-5.6-terra`) / High.
La configuración efectiva de la sesión es NO VERIFICADA. La fuente concreta y los
oráculos deterministas son suficientes para preparar un binding reversible; Switch
Benefit MEDIUM para esta preparación. Reabrir diagnóstico antes de un cambio material
o review crítico; no inferir cambio efectivo de modelo.

## Objective

Preparar ahora una frontera válida para el próximo turno; completar T13 y cierre
solo después de la tarea habitual del usuario.

## Ordered steps

1. Inspeccionar únicamente metadatos/IDs/forma de contadores de la fuente indicada.
2. Corregir el rechazo de turnos raíz sucesivos en el mismo thread, con opt-in S03.
3. Validar el ajuste con fixtures artificiales y regresión afectada.
4. Crear un ledger privado fuera del worktree y registrar binding y frontera.
5. Esperar una tarea habitual nueva. Al terminar, refresh, conciliación T13, review
   y cierre de S03; conservar unknowns sin evidencia.

## Constraints

- Una sola fuente, intervalo desde binding hasta refresh final.
- No leer conversaciones, prompts, código ni herramientas de la fuente.
- No importar uso anterior al binding ni persistir ruta/IDs reales en el repositorio.
- No ejecutar T13 ni cerrar S03 antes de la tarea habitual.

## Required tests

- Turnos raíz sucesivos mismo thread; fork/child thread distinto excluido.
- T13 real prospectivo y suite offline reciente después de la tarea.

## Definition of done

- Binding registrado antes del siguiente turno con fuente/versión/identidad válidas.
- Tras el trabajo, comparación fuente/reporte y no escritura del original demostradas.
- Review y estado final sin findings obligatorios; cierre solo con evidencia real.
