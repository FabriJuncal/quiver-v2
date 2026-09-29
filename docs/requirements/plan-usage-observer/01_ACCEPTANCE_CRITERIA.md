# Criterios de aceptación — propuesta v1

**Aprobados por el usuario el 2026-09-24 para la entrega futura.** No se consideran
cumplidos por esta aprobación documental. Fuente: [00_REQUIREMENT](00_REQUIREMENT.md);
registro de alcance/version en [STATE](STATE.md).

## Clasificación y supuestos

N2, ruta completa: contratos de identidad, persistencia privada y experiencia guiada;
impacto material recuperable. No cobro, cambio de permisos ni modificación del runtime.
Integridad/concurrencia justifican capacidad ADVANCED en los slices críticos, no
convertir automáticamente todo el requirement en N3. Reclasificar si aparece riesgo
de pérdida de originales, escritura en datos ajenos o billing real.

Supuestos a validar: intérprete Python >=3.11 disponible; sistema local macOS/Linux;
rollout JSONL plano de una versión cualificada y raíz inline explícitamente enlazada.
En esta copia se verificó Python 3.14.4 con `python3.14`; `python3` es 3.9.6.
Elegir explícitamente el intérprete compatible, sin instalar ni modificar PATH global.
El host habitual puede no coincidir con el CLI instalado. No hay bloqueo documental;
la compatibilidad mínima es gate previo a implementar S01 y el recorrido real
prospectivo completo es gate de cierre S03.

| ID | Resultado observable | Evidencia requerida / slice |
|---|---|---|
| AC-01 | Activación explícita reversible; sin cambiar launcher, modelos, auth, permisos o forma de conversar; apagado no lee logs | Pruebas off/on/error y walkthrough; S01/S03 |
| AC-02 | Proyecto + requirement + revisión de plan + ejecución/intento enlazados antes del uso; slice opcional real; IDs runtime solo si existen | Binding fechado con digest del plan y frontera de captura; rechazar sesión compartida/ambigua; S01 |
| AC-03 | Contar una sola vez cada respuesta atribuible; conservar semántica nativa y campos desconocidos | Fixtures con input/cache/output/reasoning/cache-write, acumulados contrastados y IDs; S01 |
| AC-04 | Reimportar/reanudar no duplica ni pierde eventos ya confirmados; no cruce entre planes; uso/checkpoint coherentes | Fallos inyectados antes/después de replace, dos importadores, truncado, conflicto de IDs; S01/S02 |
| AC-05 | Fallos, retries, cancelaciones e interrupciones conservan uso observado; falta de eventos genera advertencia/incompleto | Fixtures con respuestas fallidas con/sin uso; no cierre falso por EOF; S02 |
| AC-06 | Cierre técnico, aceptación del trabajo y estado de datos independientes; eventos tardíos crean revisión explícita | Reporte antes/después, referencia de aceptación; S02 |
| AC-07 | Tiempo transcurrido con límites explícitos; pausas registradas; actividad/espera/tiempo-agente unknown si no observables | Reloj controlado, pausa/resume y solapamiento; no heurística de silencio ni tokens/segundo; S02 |
| AC-08 | USD exactos solo con contadores, identidad y tarifa aplicables; faltantes no cero; subtotal no total | Tarifa sintética marcada, Decimal, cambio de tier/modelo, snapshot inmutable, no revaloración; S02 |
| AC-09 | Metadatos mínimos privados; no prompts/código/args/credenciales, ni logs ajenos o subidas | Canarios sintéticos, rutas/symlinks fuera de alcance rechazados, salida sanitizada; S01/S03 |
| AC-10 | JSON y vista textual muestran identidad, revisión, uso, tiempos, naturaleza de USD, procedencia, versiones, anomalías y faltantes | Golden fixtures y salida guiada; sin porcentaje inventado de cobertura; S01/S02 |
| AC-11 | Integración real separada del éxito offline, en el flujo habitual y con evidencia autorizada | Una ejecución enlazada desde antes de la frontera, refresh final en lectura, comparación fuente/reporte; S03 |
| AC-12 | Fuentes no soportadas, forks y subagentes no se suman ni ocultan; consumo desconocido declarado | Fixtures child/replay/legacy/comprimido/versión nueva; estado incompleto y límite del reporte; S01/S03 |

## Testing propuesto

**T2 reforzado**: recorrido vertical offline, recuperación, concurrencia, privacidad,
regresión del flujo apagado y un hito real autorizado antes de declarar integración.
T1 no detectaría atribución cruzada/caídas; T3 amplio multi-host/multi-proveedor sería
prematuro. Review N2 dedicado recomendado para la implementación material; no se
autoriza delegación ni otra sesión de review en este encargo. Resolver su alcance
real antes del cierre futuro conforme a workflow/08.

Matriz de casos/commands en [03_PLAN](03_PLAN.md#matriz-de-pruebas-t2-reforzado).
No thresholds de ahorro/precisión: no es un benchmark ni un predictor.
Sin estimación cuantitativa validada de tokens, USD o duración de los slices.
