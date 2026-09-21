# Upgrade a 2.3.0-rc.1 — opt-in, sin activar delegación

La candidata es local y no publicada. No reemplazar la instalación estable para
producción antes de revisar sus límites. Primero puede probarse en HOME temporal.
Si venís de 2.2.1, aplicar también los campos de
[Runtime Guardrails](UPGRADE_2_2_1_TO_2_2_2.md), sin volver a publicar versiones previas.

## Instalación nueva o actualización de Factory (solo al aprobarla)

Extraé el paquete verificado en una carpeta nueva permanente. Desde esa carpeta:

```bash
ASF_ROOT="$(pwd -P)"
bash scripts/check-release.sh
bash scripts/install.sh --dry-run
bash scripts/install.sh
bash scripts/doctor.sh
export PATH="$ASF_ROOT/scripts:$PATH"
```

El instalador actualiza el bloque gestionado y crea backups si cambia. No escribe
config.toml ni instala `assistant-proposal`. Skills ya enlazadas a otra instalación
se preservan: si doctor las señala, detener y revisar procedencia; no borrar skills.
Conservar carpeta vieja para rollback revisado. No hay migración de código.

Perfiles opcionales, sin sobrescribir los personalizados:

```bash
bash "$ASF_ROOT/scripts/configure-model-profiles.sh" --dry-run
bash "$ASF_ROOT/scripts/configure-model-profiles.sh"
```

No usar --force para resolver diferencias sin revisar backup y personalizaciones.
Iniciar desde la carpeta del proyecto: `asf balanced`; alternativa con perfiles
instalados: `codex --profile asf-balanced`. `/status` cuando el workflow dependa
materialmente de la configuración, no una interrupción en cada tarea.

## Proyecto existente

Actualizar Factory no actualiza silenciosamente la capa del proyecto. En Codex,
desde el proyecto, copiar este prompt:

> Actualizá únicamente la capa AI Software Factory de este proyecto a 2.3.0-rc.1
> siguiendo docs/guides/UPGRADE_2_2_2_TO_2_3_0.md de la instalación canónica.
> Leé AGENTS, PROJECT_PROFILE, PROJECT_STATE y STATE activos antes de editar.
> Preservá código, arquitectura, criterios, decisiones aprobadas y slices cerradas.
> Integrá el AGENTS template como capa mínima sin reemplazar mis instrucciones;
> actualizá metadata Factory solo después de integrar la capa correspondiente.
> Conservá próxima acción, autorizaciones y runtime limitations. No migres runs
> v1 a v2 ni modifiques evidencia histórica. Delegación sigue deshabilitada/inline;
> no agregues opt-in ni copies configuración del ayudante. Validá con doctor.sh
> --project . desde la instalación canónica y explicá el próximo paso concreto.

Esto sirve también para `nuevo-proyecto`; ejecutarlo desde su carpeta. Nunca
reemplazar estados reales por templates vacíos ni cerrar trabajo activo por upgrade.

## Revertir

Revisar backups y reinstalar desde la carpeta estable verificada, conservando skills
ajenas y cambios posteriores. El rollback de capa del proyecto requiere revisión;
no borrar metadata ni deshacer decisiones de producto automáticamente.
