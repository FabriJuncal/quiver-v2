# Decision

Preparar v2.3.0-rc.2 como prerelease/preview offline. Es el siguiente identificador
inmutable porque v2.3.0-rc.1 ya existe en el remoto y apunta al commit anterior.

No promover 2.3.0 estable: RC-F02 continúa abierto para delegación viva. No reutilizar
rc.1 ni cambiar su tag. No incluir requirements/estado de desarrollo en el ZIP.

Impacto: metadata y distribución Factory; consumidores obtienen instrucciones de
routing más precisas al instalar/actualizar e iniciar una sesión nueva. Sin migración
de proyectos, datos, permisos o configuración personal.
