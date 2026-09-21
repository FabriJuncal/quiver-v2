# Pruebas preparadas — plan T2 offline

Matriz aprobada de escenarios. Implementación y resultados actuales se registran en
IMPLEMENTATION_EVIDENCE.md; EVIDENCE.md conserva el baseline de preparación.
No confundir recorridos documentales M19/M20 con prueba de obediencia de un modelo.
T2 por compatibilidad, paths, estado y recuperación; no performance ni pruebas con
modelos en esta fase. Datos sintéticos, directorios temporales y Codex simulado.

## Fixture propuesto

Proyecto original con `src/example.txt`, un archivo modificado por el usuario,
`PROJECT_STATE.md` y un requirement/slice. Copia descartable en un directorio hermano,
no dentro del original. Baseline fuera del alcance declarado al ayudante; runtime
debe impedir que lo altere antes del ensayo vivo. Un hash no autentica su autoría.
Dos manifests del conjunto completo de la copia, evidencia de detención sintética
etiquetada como tal y entrega ligada a attempt/base. Sin claves reales ni red.

## Matriz de escenarios

| ID | Entrada / acción simulada | Resultado esperado | AC / slice |
|---|---|---|---|
| M01 | Proyecto inline sin runs | Comportamiento previo, cero writes | 01,07 / S01,S02 |
| M02 | V1 histórica válida; v2 usa política nueva | V1 preservada; v2 validada por su contrato, sin migración | 07 / S02 |
| M03 | Política desconocida o v2 sin opt-in/riesgo aprobado | Rechazo, nunca autorización inferida del plan | 01,02 / S02 |
| M04 | Campo enforced=true basado solo en instrucción/hash | No certifica enforcement; evidencia/estado insuficiente visible | 02,10 / S02 |
| M05 | Copia idéntica antes/después | Sin diferencias observadas; nunca «garantía read-only» | 03,10 / S03 |
| M06 | Crear, modificar y borrar archivo en copia | Cada diferencia reportada; entrega rechazada | 04 / S03 |
| M07 | Cambiar permiso o archivo por directorio/enlace | Diferencia o rechazo seguro, no lectura del enlace | 03,04 / S03 |
| M08 | Path con espacios, .., absoluto, symlink o hardlink | Espacios válidos; escapes/enlaces rechazados sin acceder al destino | 03 / S03 |
| M09 | Archivo ilegible o mutación durante inventario | Error/observación incompleta, nunca resultado limpio | 03,10 / S03 |
| M10 | Se altera y restaura contenido entre snapshots | Sin diferencia final; límite explícito, no afirmar ausencia de actividad | 10 / S03,S04 |
| M11 | Cambio humano en original durante trabajo | No integrar ni restaurar; conservar ambas versiones y reconciliar | 04,05 / S03,S04 |
| M12 | Hijo DONE sin entrega, stop o validación del padre | No aceptación ni cierre de slice | 05 / S02 |
| M13 | Entrega de intento anterior/base obsoleta o repetida | Rechazo/reconciliación o no-op; no aplicar dos veces | 05 / S02 |
| M14 | Incidente en copia con stop confirmado | failed con evidencia; copia no reutilizable; original intacto | 04,05 / S02,S03 |
| M15 | Cancelación/caída sin stop observado | unknown, cupo ocupado, no retry ni reasignación | 05,06 / S02 |
| M16 | Segundo hijo, recursión declarada o intento 3/reset de ID | Rechazo de contrato; no garantía de bloqueo del runtime | 06 / S02 |
| M17 | Propuesta contiene comando, path externo o cambia STATE | No ejecución; rechazar alcance indebido | 03,05 / S02,S03 |
| M18 | Falta protección del original/externos/recursión | Diagnóstico no apto para piloto aunque documentos sean válidos | 02,09 / S01,S04 |
| M19 | Resultado válido + siguiente slice autorizada | Estado mantiene acción; walkthrough continúa, no cierre prematuro | 08 / S01,S04 |
| M20 | Modelo/costo/progreso no observados | unknown, sin porcentajes ni identidad inferida | 08,10 / S01,S04 |
| M21 | Revisar selección con .env y secreto sintético en nombre inocuo | Exclusión/revisión requerida; filename filter no prueba sanitización | 03,10 / S03 |
| M22 | Modificar evidencia de aceptación, manifest o hash | Checker rechaza inconsistencia; no autentica evidencia falsificada coherente | 02,05 / S02 |
| M23 | Ejecutar checker/doctor/auditor dos veces | Sin escrituras, installs, modelo, red, publicaciones ni efectos duplicados | 07,09 / S02–S04 |

M19/M20 incluyen walkthrough documental: no afirmar obediencia de un modelo mediante
unit tests. M04/M18 validan representación de límites, no ejecutan restricciones.
M09/M10 no demuestran inmunidad a cambios concurrentes o evasión maliciosa.

## Reutilización

Reutilizar los tests actuales de dependencias/ciclos, attempts, stop, aceptación,
symlinks, scope, opt-in, unknown, observación de modelo e idempotencia. Añadir solo
variantes v2 y auditoría faltantes; no copiar la suite entera ni crear un segundo checker.

Comandos existentes para baseline y futura regresión (Python >=3.11):

```bash
python3.14 -B -m unittest discover -s tests
bash scripts/check-release.sh
python3.14 -I -B scripts/lib/check_execution.py --project examples/guided-delegation/project
```

Comandos de snapshot/compare implementados y ejecutados en
examples/supervised-multiagent/README.md. CI sigue usando discovery y valida ambos
ejemplos. No hay tests skipped presentados como éxito.

## Piloto vivo futuro — NO AUTORIZADO / NOT RUN

Antes: revisión de riesgos y del diff crítico; permiso separado para un ayudante y
un intento sobre material sintético, sin cambios personales ni publicación.
Verificar protección de original/baseline/configuración, control de acciones externas,
recursión y observación/fin. Instrucción de no escribir en copia se declara supervisada.
Si no se pueden verificar los controles restantes, no lanzar: explicar cuál falta.
Después de autorización y preflight suficiente: comparar inventarios, comprobar
entrega con criterios y evidencia, registrar tiempo/retrabajo/consumo observable,
sin afirmar costo o ahorro desconocidos. Cancelación real requiere prueba posterior
específica; una simulación no prueba detención de un proceso.
