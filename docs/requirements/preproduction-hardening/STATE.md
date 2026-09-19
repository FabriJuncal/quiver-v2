# Pre-production hardening

- **Status:** completed
- **Phase:** closure
- **Risk level:** N2
- **Acceptance criteria:** approved — corregir los findings obligatorios F01–F13 de la auditoría del 2026-09-19.
- **Plan version:** 1
- **Plan review:** approved-with-notes — cambios localizados; sin rediseño ni dependencias de producción obligatorias.
- **Human plan approval:** approved — usuario: «aplica los ajustes».
- **Execution authorization:** approved — plan mínimo de corrección presentado en la auditoría.
- **Test profile:** T2 — fixtures de filesystem, lifecycle macOS/Linux y consistencia documental.
- **Current slice:** none
- **Completed:** F01–F14; scripts/diagnóstico, estados/routing/review, onboarding/distribución, tests y CI; 22 pruebas macOS y 22 Linux OK.
- **Implementation review:** approved-with-notes — self review, ver 05_IMPLEMENTATION_REVIEW.md; no review independiente remoto.
- **Directed correction rounds:** 1
- **Pending:** ninguno dentro del plan local; publicación y validación remota no ejecutadas.
- **Next action:** esperar autorización de publicación con URL del repositorio destino, si el usuario desea publicar.
- **Why this is next:** el alcance aprobado termina en las correcciones verificadas; no autoriza commitear cambios preexistentes ni publicar.
- **User action required:** true
- **Decision required:** solo para iniciar publicación: confirmar destino y autorizar preparar la release.
- **Expected output:** petición «Preparar publicación en [URL del repositorio]», o un nuevo requirement.
- **After this:** revisar el conjunto Git y seguir docs/maintainers/RELEASE_CHECKLIST.md; no asumir autorización de push.
- **Blocked by:** none
- **Resume instruction:** leer EVIDENCE.md y el estado del proyecto. Las correcciones locales están cerradas; no repetir instalación personal ni publicar sin autorización adicional.

El working tree contenía cambios extensos antes de esta tarea. No descartar, commitear ni publicar esos cambios automáticamente.
