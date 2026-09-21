# Próximo experimento propuesto — NO AUTORIZADO / NOT RUN

P01–P04 no autorizan este experimento. Inline continúa default; no hay trabajo vivo
pendiente que deba iniciarse por leer STATE o esta propuesta.

Objetivo: comprobar si un handoff acotado aporta evidencia utilizable, no demostrar
ahorro general ni habilitar implementación paralela.

- Tarea: un worker lee únicamente el ejemplo sintético de guided-delegation y devuelve
  hasta tres inconsistencias, cada una con archivo, evidencia y criterio. Sin editar.
- Contexto: brief/SPEC, criterios y archivos del ejemplo, reglas obligatorias y refs
  del contrato pertinentes. No chat completo, secretos, configuración personal ni red mutante.
- Control: coordinador único; máximo un worker y un intento, sin retries/escalamiento
  automático. Perfil propuesto por catálogo y disponibilidad, nunca identidad inferida.
- Preflight previo al spawn: demostrar restricciones read-only, sin mutaciones externas
  ni subdelegación, observar ID/resultado, interrumpir y reconciliar. Si el cliente no
  ofrece controles suficientes, registrar limitación y no lanzar.
- Checkpoint de supervisión: cinco minutos como momento de inspección, no garantía de
  hard timeout. Si el usuario requiere tope monetario duro y el runtime no puede imponerlo,
  no despachar. Consumo real se registra solo si es observable.
- Aceptación: resultado ligado a base, evidencia contrastada por coordinador, fin
  confirmado, cero cambios en archivos y próxima acción clara. Registrar duración,
  revisión humana, intentos, retrabajo y consumo disponible; unknown donde falten datos.
- Cancelación y recuperación: validar en una fase posterior separada y autorizada;
  no simular fallos del proceso ni cerrar sesiones ajenas en este primer ensayo.

Prompt de autorización acotada, solo si el usuario decide avanzar:

> Autorizo el primer experimento de LIVE_PILOT_PROPOSAL.md: un worker read-only,
> un intento y sin publicación. Verificá primero las restricciones reales del runtime;
> si no podés imponerlas, no lo lances y registrá la limitación.

Esto no autoriza publicar, instalar perfiles, ampliar permisos ni modificar código.
