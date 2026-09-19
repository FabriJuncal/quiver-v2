# Publicación v2.2.1

- **Status:** in-progress
- **Phase:** release verification
- **Risk level:** N1
- **Workflow size:** compact
- **Authorization:** usuario confirmó https://github.com/FabriJuncal/quiver-v2 y pidió publicarlo usando gh y su alias SSH personal; 2026-09-19.
- **Scope:** versión local completa de Factory auditada/corregida, incluyendo su reorganización preexistente. Sin cambios de visibilidad, credenciales, force-push ni reescritura de tags.
- **Acceptance criteria:** main contiene la versión completa; CI termina correctamente; release v2.2.1 tiene ZIP instalable y checksum; URLs y estado verificables.
- **Plan approval / execution authorization:** petición explícita del usuario; ejecución autorizada dentro de ese alcance.
- **Plan review:** self review; el destino coincide con origin y la identidad es FabriJuncal. Repositorio privado, main sin protección, Actions habilitado, sin releases ni tags existentes al comenzar.

## Plan breve

1. Verificar identidad, remoto, cambios y material sensible; conservar permisos privados.
2. Actualizar onboarding con el destino confirmado y registrar autorización.
3. Validar los archivos y crear commit local revisado; exportar y probar esa revisión limpia.
4. Subir main mediante SSH personal y comprobar CI con gh.
5. Crear tag y release con gh, adjuntar ZIP y checksum verificados.
6. Comprobar referencias/artefactos y persistir resultado, sin volver a publicar ni tocar tags existentes.

## Estado

- **Completed:** autenticación gh/SSH, remoto y main comprobados; inventario de cambios y búsqueda dirigida de secrets/rutas personales sin coincidencias en archivos activos.
- **Pending:** pruebas de revisión, commit/push, CI, tag/release y comprobación final.
- **Next action:** ejecutar suite local y comprobar la revisión exacta que se va a publicar.
- **Why this is next:** el HEAD inicial no contiene scripts/configuración/skills nuevos; publicar ese HEAD omitiría la versión auditada.
- **User action required:** false
- **Expected output:** revisión versionada y validada lista para push.
- **After this:** publicar y comprobar CI/release con gh.
- **Blocked by:** none
- **Resume instruction:** consultar Git y gh para saber qué operaciones se completaron; no asumir estado externo desde el chat ni recrear una release/tag ya existente.

La validación de modelos/reasoning en una sesión con inferencia paga sigue fuera de esta publicación; no declarar ese soporte como comprobado por los tests de filesystem.
