# Release candidate 2.3.0-rc.1

- **Status:** completed (preparación rc.1; publicación GitHub no verificada aquí)
- **Current slice:** none
- **Pending slices:** none
- **Next action:** none; rc.2 reemplaza esta candidata para cambios posteriores.
- **Why this is next:** rc.1 fue integrada en main y el tag remoto existe; su preparación histórica está cerrada.
- **User action required:** false
- **Decision required:** none para rc.1; RC-F02 permanece como límite transversal de activación.
- **Expected output:** estado histórico reconciliado, sin mover/reutilizar su tag.
- **After this:** seguir docs/requirements/release-2-3-0-rc-2/STATE.md.
- **Blocked by:** none
- **Runtime limitation:** unavailable-runtime-capability
- **Runtime limitation detail:** solo piloto: spawn_agent actual no selecciona rol/config/permisos ni deshabilita recursión; controles efectivos del hijo no verificables. Preparación offline sí viable.
- **Resume instruction:** estado histórico; leer EVIDENCE.md y 05_IMPLEMENTATION_REVIEW.md. Para trabajo actual usar release-2-3-0-rc-2/STATE.md. Piloto NOT RUN; RC-F02 sigue abierto.

Entregables: `.release-candidates/2.3.0-rc.1/` en source local (ZIP/SHA256/bundle y
ARTIFACTS.json); rama `release/2.3.0-rc.1` en clon separado de preparación.
Reconciliación 2026-09-23: el tag remoto `v2.3.0-rc.1` existe y apunta a `022476862af268e32d6741036ff0f5a821f34d97`; no moverlo. La existencia de GitHub Release no se verificó con las credenciales disponibles. La evidencia técnica no cierra RC-F02.

Autorización humana: petición actual aprueba candidata e integración mínima; un
piloto condicional, sin configuración habitual ni publicaciones. No autoriza otros
agentes de coding/review. Política supervised-audited-v1; no hay dispatch autorizado
por este documento mientras falte un control. No se crea run prepared sin preflight.
