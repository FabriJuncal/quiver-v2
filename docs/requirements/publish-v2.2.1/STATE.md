# Publicación v2.2.1

- **Status:** completed
- **Phase:** closure
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

- **Completed:** versión completa subida a main; tag v2.2.1 publicado; CI macOS/Ubuntu exitoso; release publicada con ZIP y SHA-256; descarga remota idéntica al paquete probado.
- **Release commit:** db1eb677c6b067751fbe66cb013fea0a79ebe688
- **Release:** https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.1
- **Implementation review:** self review de diff, paquete y resultados externos; sin inferencias remotas ni reviewer independiente.
- **Pending:** none dentro de la publicación autorizada; repositorio privado por decisión de preservar su configuración.
- **Next action:** esperar un nuevo requirement del usuario.
- **Why this is next:** publicación y verificación completadas; nuevas funciones o cambios de visibilidad requieren alcance explícito.
- **User action required:** true, únicamente para iniciar otro trabajo.
- **Expected output:** nueva petición concreta.
- **After this:** capturar y ejecutar el nuevo alcance autorizado.
- **Blocked by:** none
- **Resume instruction:** consultar EVIDENCE.md; no recrear release/tag v2.2.1 ni moverlos. El commit posterior de cierre solo registra evidencia; no altera el contenido de la release.

La validación de modelos/reasoning en una sesión con inferencia paga sigue fuera de esta publicación; no declarar ese soporte como comprobado por los tests de filesystem.
