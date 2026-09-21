# Evidencia de implementación S01–S04 — 2026-09-21

Resultado: **completado offline**, no lanzamiento de ayudantes ni publicación.
Ejecución local macOS/Python 3.14. No prueba Linux/CI remota ejecutada en esta sesión.

## Comandos y resultados reales

| Comando / comprobación | Resultado |
|---|---|
| `python3.14 -B -m unittest discover -s tests` — final | **111 tests OK**, 22.719 s, exit 0 |
| Mismo comando antes de revisión dirigida | 110 tests OK, 22.585 s |
| `python3.14 -B -m unittest discover -s tests -p 'test_delegation_contract.py'` | 34 tests v1 OK, 1.341 s; incluidos otra vez en suite final |
| `python3.14 -B -m unittest discover -s tests -p 'test_supervised_delegation.py'` — dirigido final | 19 tests v2 OK, 2.020 s |
| `python3.14 -B -m unittest discover -s tests -p 'test_workspace_audit.py'` — dirigido final | 14 tests filesystem OK, 0.227 s |
| `bash scripts/check-release.sh` | PASS; sintaxis, recursos, versión 2.2.2, gates, mappings, launcher; no publicación |
| `python3.14 -I -B scripts/lib/check_execution.py --project examples/guided-delegation/project` | 1 registro sintético, STATIC PASS, exit 0 |
| `python3.14 -I -B scripts/lib/check_execution.py --project examples/supervised-multiagent/project` | 1 registro sintético, STATIC PASS y NO APTO PARA PILOTO, exit 0 |
| Comandos snapshot/compare de examples/supervised-multiagent/README.md | exit 0; inventario de src y manifests sintéticos clean |
| quick_validate.py para skills context-scout, requirement-state, slice-executor | Skill is valid en las tres |
| diff contra baseline: ejemplo v1, preflight anterior, config/, FACTORY_VERSION, MANIFEST.json | Sin diferencias |
| Validación final con Doctor.project/ExecutionCheck y comprobación de links/cierres | PASS sin errores; cuatro slices completas, ningún requirement activo, referencias locales válidas |

La comprobación final de estados conserva el warning previo PROJECT FACTORY LAYER
UNKNOWN: esta carpeta de distribución no tiene metadata de proyecto adoptado/AGENTS
propios. No se crearon archivos ficticios ni se modificó instalación personal para
silenciarlo. check-release se repitió tras actualizar cierre/estados: PASS.

Baseline previo conservado en `/tmp/asf-supervised-offline.z6yvqD/baseline` para review
del diff; no Git local ni commits/push/tags. No se leyó/modificó configuración habitual
mediante scripts de instalación. Los tests usan HOME/CODEX_HOME temporales, Codex
simulado y fixture Git descartable para lifecycle/empaquetado; no agentes reales.

## Cobertura del plan T2

| Casos | Evidencia |
|---|---|
| M01–M04 | Tests v2 de versiones, legacy, política, opt-in, aprobación de riesgo y mecanismos; suite v1 intacta |
| M05–M08 | Comparación determinista, altas/bajas/cambios, tipos/permisos, enlaces duros/simbólicos, rutas y CLI con espacios |
| M09 | Fallo de lectura simulado y cambio real inducido durante lectura: no clean falso |
| M10 | Cambio/restauración entre snapshots produce clean: límite demostrado, no garantía de no escritura |
| M11–M14 | Cambio humano preservado, incidente rechaza aceptación, faltan stop/entrega/validación, base/attempt ajenos, auditoría incompleta documentable como fallo |
| M15–M18 | Unknown ocupa cupo; sin retry superpuesto, recursion false inválida, límite 2, comandos de entrega tratados como texto; controles no verificados visibles |
| M19 | Walkthrough documental revisado en ejemplo + Finalization Gate existente; NO prueba viva de continuidad |
| M20 | Test de configuración observada unknown + walkthrough sin progreso/costo inventados |
| M21 | Test existente excluye .env de contexto; test nuevo muestra límite del inventario ante secreto sintético con nombre inocuo; revisión humana del contenido sigue requerida |
| M22–M23 | Evidencia alterada, manifest no cubre input, informes discordantes, estado y paths inválidos; checker/doctor/CLI sin writes incluso ante incidente |

Los 23 escenarios no equivalen a 23 llamadas a modelos: hay 33 nuevos métodos de
test, más 78 existentes. No se instalaron dependencias. unittest discovery los cubre
en CI; se añadió además comprobación explícita del ejemplo v2, sin ejecutar GitHub Actions.

## AC y límites

AC01/02/06/07: contrato y registros compatibles, opt-in separado, sin autorización
implícita; AC03/04/05: inventario, rechazo/reconciliación y aceptación con evidencia;
AC08/09/10: guía UX, ejecución exclusivamente offline y límites visibles.
No afirmar que estos tests comprueban permisos, obediencia, ahorro o cancelación real.

Correcciones durante implementación: carga sibling bajo Python -I; auditoría final
ilegible puede registrarse como failed con incidente, no como comparación limpia;
manifest inicial ligado a read_scope/base. Review formal: F01 (ancestro symlink),
corregido y revalidado en una ronda. Detalle en 05_IMPLEMENTATION_REVIEW.md.

Desviaciones menores: comparación de S03 incorporada como dependencia de S02 antes
de aceptar S03; schema usa oneOf/not mínimos en vez de duplicar el contrato completo.
No desviación de alcance, garantías aprobadas, presupuesto de intentos ni permisos.

Riesgos residuales: snapshots no atómicos, cambios transitorios no observables,
evidencia falsificada coherentemente no autenticable con hashes, protección de
original/externos/recursión y terminación real pendientes. Piloto deshabilitado.
AI Strategy heredada; modelo efectivo, tokens y costo unknown, sin escalamiento observado.
