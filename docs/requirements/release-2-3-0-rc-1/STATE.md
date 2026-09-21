# Release candidate 2.3.0-rc.1

- **Status:** in-progress
- **Current slice:** none
- **Pending slices:** none
- **Next action:** preparar integración inactiva, versionado y paquete local; ejecutar regresiones y revisar diff.
- **Why this is next:** preparación autorizada; piloto condicionado a controles efectivos, no a PASS documental.
- **User action required:** false
- **Decision required:** none
- **Expected output:** candidata local validada con piloto NOT RUN si falta capacidad y aprobación de publicación pendiente.
- **After this:** entregar evidencia y boundary concreto; no push, tags ni publicación.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability
- **Runtime limitation detail:** solo piloto: spawn_agent actual no selecciona rol/config/permisos ni deshabilita recursión; controles efectivos del hijo no verificables. Preparación offline sí viable.
- **Resume instruction:** leer PLAN.md y evidencia de sandbox-isolation-probe; continuar preparación offline. No lanzar ayudante salvo todos los controles obligatorios verificados antes; máximo uno y un intento sintético.

Autorización humana: petición actual aprueba candidata e integración mínima; un
piloto condicional, sin configuración habitual ni publicaciones. No autoriza otros
agentes de coding/review. Política supervised-audited-v1; no hay dispatch autorizado
por este documento mientras falte un control. No se crea run prepared sin preflight.
