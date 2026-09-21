# Release candidate 2.3.0-rc.1

- **Status:** awaiting-approval
- **Current slice:** none
- **Pending slices:** none
- **Next action:** revisión/aprobación final del alcance preview offline o resolver RC-F02 con un runtime que exponga los controles del hijo antes de aprobar multiagente operativo.
- **Why this is next:** candidata offline y ZIP probados; piloto no lanzado por controles obligatorios pendientes. La petición exige detener piloto y esperar aprobación final.
- **User action required:** true
- **Decision required:** aceptar explícitamente preview offline o continuar integración runtime; publicación requiere autorización separada.
- **Expected output:** decisión concreta de alcance, sin interpretar preparación o tests como aprobación de publicación.
- **After this:** ejecutar únicamente la opción autorizada y mantener ayudante deshabilitado hasta controles verificados.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability
- **Runtime limitation detail:** solo piloto: spawn_agent actual no selecciona rol/config/permisos ni deshabilita recursión; controles efectivos del hijo no verificables. Preparación offline sí viable.
- **Resume instruction:** leer EVIDENCE.md y 05_IMPLEMENTATION_REVIEW.md. Preparación offline terminada, 117 tests OK también desde ZIP, piloto NOT RUN/0 intentos. No repetir sandbox ni lanzar ayudantes por aprobación de preview. Para activar, primero verificar rol/permisos/herramientas/detención del hijo y RC-F02; no push/tag/publicación sin nueva autorización.

Entregables: `.release-candidates/2.3.0-rc.1/` en source local (ZIP/SHA256/bundle y
ARTIFACTS.json); rama `release/2.3.0-rc.1` en clon separado de preparación.
No existe tag nuevo. La evidencia técnica de preparación no cierra el bloqueo runtime.

Autorización humana: petición actual aprueba candidata e integración mínima; un
piloto condicional, sin configuración habitual ni publicaciones. No autoriza otros
agentes de coding/review. Política supervised-audited-v1; no hay dispatch autorizado
por este documento mientras falte un control. No se crea run prepared sin preflight.
