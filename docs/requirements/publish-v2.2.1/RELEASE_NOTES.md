# AI Software Factory v2.2.1 — Guided Model Routing

Workflow reutilizable para proyectos nuevos y existentes, con Guided Mode, estado persistente en Git/Markdown, testing proporcional y selección guiada de modelos por tarea.

## Cambios principales

- Routing por perfiles ECONOMICAL / BALANCED / ADVANCED, Model Gates de beneficio material y prevención de cambios frecuentes entre slices.
- Aprobaciones separadas de criterios, plan y ejecución; reanudación desde estado y review con evidencia y límite de correcciones.
- Instalación endurecida: marcadores validados, symlinks rechazados, temporales exclusivos, backups únicos, permisos preservados y dry-run sin escrituras.
- Doctor con comprobaciones de versión, overrides y TOML; adopción que preserva código e instrucciones existentes.
- Ruta compacta N0/N1, documentación de onboarding y suite automatizada para macOS/Linux.

## Instalación

Descargar `ai-software-factory-v2.2.1.zip`, comprobar su SHA-256 con el archivo adjunto y extraerlo. Dentro de la carpeta extraída:

```bash
./scripts/install.sh --dry-run
./scripts/install.sh
./scripts/doctor.sh
```

Requisitos: Bash, Git y Codex CLI >= 0.134.0 para perfiles separados. Python >= 3.11 es opcional para la validación TOML de doctor. Ver README y QUICK_START para iniciar o adoptar proyectos.

## Verificación y límites

- 22 pruebas de regresión de filesystem, scripts, adopción y empaquetado; ejecutadas localmente en macOS/Linux y mediante el workflow Validate.
- La disponibilidad de modelos depende de cuenta/runtime. No se hicieron inferencias pagas ni review remoto como parte de esta publicación.
- El ZIP histórico queda fuera del paquete instalable.
- La release conserva la visibilidad del repositorio; no hace público un repositorio privado.
