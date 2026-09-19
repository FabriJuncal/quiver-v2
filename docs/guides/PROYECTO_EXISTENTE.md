# Adoptar un proyecto existente

## Objetivo

Agregar la capa de AI Software Factory sin migrar ni reescribir el proyecto.

## 1. Entrar

```bash
cd /ruta/al/proyecto
```

## 2. Scaffold

```bash
/ruta/ai-software-factory/scripts/adopt-project.sh
```

El script:

- no modifica código;
- no cambia dependencias;
- no cambia DB;
- no cambia deployment;
- preserva `AGENTS.md` existente;
- crea templates faltantes.

## 3. Project Discovery

Abrir Codex:

```bash
codex
```

Prompt:

```text
Adoptá este proyecto existente usando AI Software Factory.

Comenzá por Project Discovery.

No modifiques código ni arquitectura.

Generá o completá:
- PROJECT_PROFILE.md
- CAPABILITY_MAP.md
- PROJECT_STATE.md

Clasificá capacidades con:
KEEP / ADD / WRAP / IMPROVE / REPLACE_LATER / IGNORE.
```

## 4. Herramientas de conocimiento

Proyecto pequeño:
- ninguna adicional.

Proyecto desconocido:
- Graphify opcional.

Monorepo/legacy grande:
- Codebase Memory MCP opcional.

No uses ambos por defecto.
