# Codex no detecta AI Software Factory

## 1. Ejecutar doctor

```bash
/path/ai-software-factory/scripts/doctor.sh
```

## 2. Ver ruta configurada

```bash
grep -n -i -E "factory|ai-software" ~/.codex/AGENTS.md
```

## 3. Validar Guided Mode

```bash
FACTORY="/ruta/real/ai-software-factory"

grep -n -E "Guided Mode|Decision Bound" \
"$FACTORY/workflow/00_SHARED_CONTRACT.md"

grep -n -E "User action required|Expected output" \
"$FACTORY/templates/PROJECT_STATE.md"
```

## 4. Reiniciar Codex

Las instrucciones globales se leen al iniciar sesión.

Cerrar sesión y abrir una nueva.

## 5. Proyecto antiguo

Actualizar Factory no actualiza automáticamente:

- `AGENTS.md`;
- `PROJECT_STATE.md`;
- requirement `STATE.md`;

de proyectos inicializados anteriormente.

Pedí:

```text
Actualizá únicamente la capa de AI Software Factory de este proyecto
al formato actual de Guided Mode.

Conservá la información existente y no modifiques código de aplicación.
```

## 6. Varias copias

No busques todo `$HOME` con `find ~` si el disco es grande.

Primero revisá la ruta configurada en `~/.codex/AGENTS.md`.

El `doctor.sh` informa la instalación que está ejecutándose.
