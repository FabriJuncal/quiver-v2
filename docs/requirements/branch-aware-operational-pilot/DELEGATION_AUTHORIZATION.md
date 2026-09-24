# Autorización de delegación P4-P5

Fecha: 2026-09-23.

## Alcance autorizado

- Fuente: autorización explícita del usuario de 2026-09-23 para completar P4, P5 y P6
  del plan v1 y para delegar scoring ciego P4 y review independiente N2 P5.
- Modalidad: secuencial, con un máximo de un agente delegado activo.
- Escritura: el coordinador es el único escritor y responsable de estado, aceptación,
  hashes, integridad, cálculos y conclusión.
- Workers: no pueden editar archivos, ejecutar acciones externas, modificar Git,
  subdelegar ni aceptar/cerrar el requirement.
- Contexto: cada worker debe comenzar sin heredar la conversación y consultar solamente
  la allowlist expresa de su encargo.

## Mecanismo real y límites

- El runtime permite crear un agente nuevo con contexto no heredado, observar su identidad,
  recibir su resultado y confirmar su estado final.
- Las prohibiciones de escritura, acciones externas, subdelegación y acceso fuera de la
  allowlist se transmiten como instrucciones. No existe una reducción verificable de
  permisos por agente ni una allowlist de lectura impuesta técnicamente.
- El filesystem es compartido. La independencia conversacional no equivale a aislamiento
  de filesystem, proceso, red o credenciales.
- Estos controles se registran como `instruction`; su enforcement técnico es `unknown`.
  El coordinador compara estado, hashes e integridad antes y después.
- La configuración efectiva de modelo/reasoning permanece `unknown` salvo exposición
  directa del runtime.

## Ejecución secuencial e incidentes

- P4 ya estaba cerrado al iniciar esta autorización: un scorer efímero previo trabajó con
  labels anonimizados y mapa separado, terminó sin tool calls y produjo `unscorable`.
  No se repite P4 ni se abre un segundo scorer.
- La desviación conocida es que el coordinador P3 había abierto una vez la respuesta
  original de `run-01-A`; por eso no actuó como scorer. No hay evidencia de que el scorer
  haya recibido el mapa antes del cierre.
- El scorer previo está finalizado: no aparece como agente activo ni como proceso P4
  identificable al preflight de esta continuación.
- P5 se ejecuta con un agente nuevo y distinto, después de consolidar P4.
- Incidentes nuevos: ninguno al preparar esta nota.
