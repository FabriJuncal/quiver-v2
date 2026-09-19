# Troubleshooting de instalación

## `code` no existe

No es necesario para Factory.

Usá:

```bash
nano archivo.md
```

o tu editor habitual.

## Skill ya existe

El instalador no sobrescribe directorios/skills existentes.

Mostrará `WARN`.

Revisá manualmente antes de reemplazar.

## El instalador fue ejecutado dos veces

Está diseñado para ser idempotente.

No duplica el bloque administrado.

## Quiero ver qué hará

```bash
./scripts/install.sh --dry-run
```

## Quiero retirar Factory

```bash
./scripts/uninstall.sh
```

Solo elimina:

- el bloque administrado;
- symlinks de skills que apuntan a esta Factory.

No elimina el repositorio ni proyectos.

También conserva perfiles opcionales y backups. No seguir usando `--profile asf-...` si se quiere retirar su selección; revisar los archivos antes de borrarlos.

## Destino inseguro o bloque ambiguo

Install, uninstall y profiles rechazan symlinks/destinos de tipo inesperado en archivos gestionados. Init/adopt rechazan symlinks en sus directorios de scaffold. Revisar la ruta que muestra el error, resolverla explícitamente y repetir el mismo comando. Los scripts no siguen esos enlaces para escribir contenido ajeno.

START y END deben aparecer una sola vez, en líneas completas y en ese orden. Si falta uno, revisar el contenido y reparar los delimitadores manualmente antes de reintentar. Factory no adivina qué texto es propio. AGENTS debe terminar con salto de línea; si no, agregarlo en el editor antes de instalar.

Las carpetas padre elegidas por el usuario deben ser confiables y no estar siendo modificadas concurrentemente por otro proceso. No ejecutar instaladores simultáneos sobre el mismo destino.

## Doctor y modelos

Codex >= 0.134.0 soporta los perfiles separados. Doctor comprueba versión y, con Python >= 3.11 disponible, sintaxis TOML; sin parser informa NO VERIFICADO. No realiza inferencias ni prueba acceso a modelos. Comprobar `/status` y `/model` en una sesión nueva.

`AGENTS.override.md` global prevalece sobre AGENTS. Factory no lo modifica: integrar/preservar las reglas deseadas y resolver cuál archivo debe quedar activo, luego repetir instalación/doctor.
