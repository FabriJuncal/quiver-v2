# AI Software Factory v2.2.2 — Runtime Guardrails

El [contrato compartido](../../workflow/00_SHARED_CONTRACT.md) es la única fuente canónica
del Finalization Gate, las cuatro State Consistency Invariants y Runtime limitation.
Templates y skills lo referencian; no mantienen variantes del gate.

## Continuidad

Una slice cerrada seguida de otra activa exige ejecutar la próxima acción autorizada.
`ACCIÓN DEL USUARIO: ninguna` comunica continuidad en una actualización y debe ir seguida
de ejecución en el mismo turno. No es una respuesta final válida con trabajo viable pendiente.
Se permite finalizar por entrega completa o un boundary/impedimento real del contrato.

## Estado y runtime

Leer PROJECT_STATE para localizar el requirement y luego su STATE. El estado del requirement
prevalece sobre el resumen de proyecto; ambos se contrastan con evidencia real. Conversation
Recap es auxiliar: si contradice STATE, registrar la inconsistencia e ignorarlo, sin editar recap.

`Runtime limitation` distingue contexto, herramientas, permisos y disponibilidad de modelos
de un blocker funcional. Registrar causa, pendiente, próxima acción, intervención y reanudación.
Si falla la escritura, explicitar qué archivo no pudo actualizarse y entregar el texto de recuperación.

## Diagnóstico

```bash
"$ASF_ROOT/scripts/doctor.sh" --project .
```

Doctor no escribe. Con Python >= 3.11 inspecciona estados, metadata, configuración y tamaño de
instrucciones. Sin parser informa NO VERIFICADO. El umbral de advertencia de tamaño es 80%:
deja margen para separadores y reglas locales. Es una heurística de aviso, no un límite de Codex.
32 KiB es el default oficial actual de `project_doc_max_bytes`, configurable. Doctor estima la
cadena global + raíz Git → directorio indicado, con overrides/fallbacks observados. No suma
todas las instrucciones de subdirectorios que Codex no cargaría desde esa ubicación.

La selección efectiva puede depender de perfil, confianza, CLI o políticas administradas no
observables. Por eso superar solo el default produce WARN; ERROR por tamaño se limita a una
cadena de proyecto que supera todos los límites explícitos observados y el límite de usuario
(o default si no lo define), como condición estática,
sin afirmar truncamiento efectivo. Para comprobar otro cwd: `doctor.sh --project ruta/al/subdirectorio`;
la validación de metadata espera un proyecto en ese directorio y puede indicar ausencias.

Estos guardrails son instrucciones y validación estática, no un supervisor del runtime. No pueden
impedir físicamente un cierre del cliente, caída del proceso o incumplimiento del modelo. El
caso real S04 → S05 debe comprobarse en una sesión con el proyecto; las pruebas locales verifican
el contrato y los diagnósticos, no garantizan la conducta de cada inferencia.

Ver [reanudación tras cierre prematuro](../troubleshooting/PREMATURE_STOP.md),
[preflight](SESSION_PREFLIGHT.md), [launcher](ASF_LAUNCHER.md) y [upgrade](UPGRADE_2_2_1_TO_2_2_2.md).
