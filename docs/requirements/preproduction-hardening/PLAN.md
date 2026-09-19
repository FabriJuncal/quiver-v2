# Plan aprobado — versión 1

## Alcance y aceptación

1. F01–F03: rechazar marcadores ambiguos, symlinks y tipos inválidos; temporales exclusivos, backups únicos y permisos preservados. Sin pérdida de contenido ajeno.
2. F05/F11/F14: doctor distingue configuración estática de runtime, detecta overrides y TOML inválido cuando existe parser; argumentos estrictos y dry-run sin escrituras; reinstalación estable.
3. F04/F07: estado inicial ejecutable, aprobación humana y autorización separadas, reanudación segura y todos los boundaries considerados.
4. F06/F08/F09: política canónica de routing, confirmación por fase, fallback por suficiencia/costo y review con alcance verificable y límite de correcciones.
5. F12/F13: ruta compacta por riesgo, documentación coherente, material antiguo fuera del recorrido activo y checklist de publicación reproducible.
6. F10: regresiones dirigidas en CI/macOS/Linux; revisión del diff y evidencia antes del cierre.

## Validación

Pruebas temporales: instalación/reinstalación/uninstall; perfiles existentes/force; marcadores corruptos; symlinks; permisos; backups; paths con espacios; overrides; configuración inválida; adopción con código propio; dry-run y argumentos inválidos. Revisar escenarios A–H de Guided Mode sin simular éxito de inferencias remotas.

No modificar configuración personal, instalar servicios ni publicar. Conservar el ZIP histórico fuera del recorrido de instalación y sin sobreescribirlo. La URL pública definitiva y publicación de una revisión Git requieren contexto/autoridad adicionales; preparar instrucciones sin inventar un destino.

## Rollback

Los cambios de código se revisan por diff; no usar reset sobre el working tree preexistente. Scripts: backups únicos de archivos regulares modificados; abortar ante rutas o bloques ambiguos.
