# Upgrade 2.2.1 → 2.2.2 — Runtime Guardrails

Actualizar la distribución no actualiza automáticamente proyectos. Doctor solo diagnostica;
no sobreescribe nada. Mantener la ruta canónica existente aunque su carpeta se llame v2.2.1:
la versión se toma de FACTORY_VERSION.md. No renombrar por estética ni romper enlaces.

## Instalación

Con la distribución v2.2.2 verificada en la carpeta canónica:

```bash
ASF_ROOT="$(pwd -P)"
"$ASF_ROOT/scripts/install.sh" --dry-run
"$ASF_ROOT/scripts/install.sh"
"$ASF_ROOT/scripts/configure-model-profiles.sh" --dry-run
"$ASF_ROOT/scripts/configure-model-profiles.sh"
"$ASF_ROOT/scripts/doctor.sh"
export PATH="$ASF_ROOT/scripts:$PATH"
```

Install reemplaza solo su bloque con backup y preserva el texto personal; no puede retirar
automáticamente duplicaciones fuera del bloque. Si el AGENTS personal es extenso, revisar
reglas no gestionadas, conservar decisiones únicas y mover detalle a docs/skills. No borrar
texto personal por parecer redundante. Configuración global reducida: contrato + referencias.
Perfiles existentes se preservan; `--force` es opcional, reemplaza con backup tras revisar diff.

## Proyecto (incluye nuevo-proyecto)

Entrá al directorio real del proyecto, iniciá `asf balanced` y pegá:

```text
Actualizá únicamente la capa AI Software Factory de este proyecto a v2.2.2 siguiendo
docs/guides/UPGRADE_2_2_1_TO_2_2_2.md de la instalación canónica.
Leé primero AGENTS.md, PROJECT_PROFILE.md, PROJECT_STATE.md y STATE de requirements activos.
Preservá código, decisiones aprobadas, criterios, arquitectura e información existente.
Integrá Finalization Gate, invariants, Source of Truth y runtime limitations mediante
referencias al contrato canónico, conservando reglas propias. No reemplaces documentos
completos por templates. No modifiques slices cerradas para completar metadata.
Actualizá Factory version a 2.2.2 en PROJECT_PROFILE y la capa AGENTS solo después de integrarla.
Completá PROJECT_STATE y STATE activos con próxima acción, motivo, usuario requerido,
resultado, después, runtime limitation y reanudación; revisá slices activas/pendientes
solo si contienen instrucciones contradictorias. STATE prevalece sobre Conversation Recap.
Revisá el diff. Desde el directorio del proyecto ejecutá el script doctor.sh de la
Factory canónica con --project .; no cambies cwd a Factory. Continuá el trabajo ya
autorizado si no hay Decision Boundary real.
Esta actualización de metadata/instrucciones está autorizada; no amplía el alcance funcional.
```

Procedimiento: inventariar estado y autorización → patch mínimo → comparar diff → doctor →
registrar evidencia y continuar. No inicializar Git ni reinstalar stack para actualizar metadata.
Guardar diff/backup si no hay Git. Si falla una integración, conservar versión anterior y
registrar el punto pendiente. Rollback restaura únicamente los hunks de este upgrade, nunca
descarta otros cambios de usuario. No ejecutar init/adopt sobre el proyecto como sustituto del upgrade.

Versiones anteriores: completar primero el upgrade correspondiente solo en campos faltantes,
conservar información y aplicar esta guía al estado activo. Si una convención propia contradice
el template, adaptarlo al proyecto; preguntar únicamente por una decisión material real.
