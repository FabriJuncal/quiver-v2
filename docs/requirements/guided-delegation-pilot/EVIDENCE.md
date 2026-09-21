# Evidencia de la etapa de diseño

Histórico del diseño. Resultados posteriores de P01–P04 en
[IMPLEMENTATION_EVIDENCE.md](IMPLEMENTATION_EVIDENCE.md); STATE contiene vigencia actual.

Fecha: 2026-09-20. Entorno local macOS; Python 3.14; distribución 2.2.2 sin Git.
No inferencia adicional, ejecución de workers, modificaciones personales ni publicación.

## Entregables

| Criterio de diseño | Evidencia |
|---|---|
| D01 | 00_REQUIREMENT delimita autorización/baseline; scripts, config y templates no modificados |
| D02 | EXECUTION_CONTRACT C01–C10; referencias a contratos/catalogo existentes, sin activar reglas nuevas |
| D03 | 01_ACCEPTANCE_CRITERIA: AC01–AC12 → P01–P04 → V01–V23; slices propuestas, no creadas |
| D04 | 04_PLAN_REVIEW; self review, una corrección dirigida GDP-F01–F03, sin independencia ficticia |
| D05 | STATE y PROJECT_STATE: próximo boundary de aprobación, no cierre falso ni autorización de workers |

## Comprobaciones realizadas

| Verificación | Resultado / alcance |
|---|---|
| `bash scripts/check-release.sh` | PASS; contrato estático de distribución, sin cambio de versión |
| `python3.14 -B -m unittest discover -s tests -v` | 44 tests OK; ejecución inicial en 18,243 s y repetición tras correcciones en 18,645 s; suite existente, no tests de delegación |
| `bash scripts/doctor.sh --project .` | Exit 0, OK WITH WARNINGS; diagnóstico de instalación/metadata, no garantía de runtime |
| Invocación directa de Doctor.state sobre ambos estados | Falló inicialmente por `none` con explicación añadida (GDP-F03); tras corrección PASS |
| Diff de PROJECT_STATE, FILE_INDEX y ARCHITECTURE contra baseline temporal | Revisado; estado/índice y referencia canónica, sin reemplazo de decisiones ni publicaciones |
| Enlaces/IDs/trazabilidad/estado final | PASS: 9 documentos, enlaces locales existentes, 12 criterios, 23 escenarios referenciados, 4 slices propuestas y estados sincronizados |
| Comparación scripts/templates/config/workflow/skills con checkout de publicación | Sin diferencias de contenido operativo; solo archivos .DS_Store locales ajenos, preservados; checkout de publicación sin cambios |

La comprobación documental se ejecutó con Python 3.14 sin bytecode: resolución de
enlaces Markdown locales, conjuntos AC01–AC12/V01–V23, correspondencia de slices
P01–P04 y parser Doctor.state real. Verificó que el puntero Active requirement
selecciona este STATE, que los campos operativos de ambos estados coinciden y que
no existe una carpeta slices activa prematuramente. Exit 0. No mide semántica del modelo.

La suite utiliza HOME/directorios temporales y Codex simulado. V01–V23 son escenarios
propuestos, NO ejecutados. Los 44 tests no certifican esos escenarios ni conducta del modelo.

## Diagnóstico que se conserva sin modificar el entorno

- Bloque global sin versión actualizada y perfiles opcionales ausentes.
- La distribución no contiene AGENTS/PROJECT_PROFILE/CAPABILITY_MAP propios; doctor
  --project no puede declararla una capa de proyecto adoptada. No crear esos archivos
  artificialmente para silenciar advertencias.
- Registro histórico publish-v2.2.1 activo en esta copia. Doctor emite CONTINUAR para
  él; no autoriza repetir una publicación. Reconciliación propuesta en P01 con evidencia.
- Tamaño global observado: 11.041 bytes. No afirmar truncamiento efectivo.

## Recuperabilidad

Antes de editar se copiaron los tres documentos existentes a un directorio temporal
privado de trabajo. Se revisaron con `git diff --no-index`; su exit 1 indica diferencias,
no error de validación. No se realizó commit porque esta carpeta no tiene repositorio Git.
La nueva carpeta del requirement conserva el trabajo de diseño. No borrar ni reemplazar
estado si después aparecen cambios del usuario; rollback de hunks propios solamente.

## Límites y siguiente acción

No se verificó soporte efectivo de agentes, aislamiento, cancelación de procesos,
modelos disponibles, costo ni eficiencia. Documentación oficial consultada en C10
del contrato; no sustituye prueba de ejecución.

Presentar plan v1 y solicitar su aprobación/implementación offline. El experimento
vivo y una nueva release requieren alcance separado. No cambiar v2.2.2 ni sus tags.
