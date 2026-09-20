# Quick Start

AI Software Factory v2.2.2 — Runtime Guardrails

Esta guía busca llevarte de cero a un proyecto funcionando con AI Software Factory en pocos minutos.

---

## 1. Requisitos

Necesitás:

- Git;
- Bash/zsh;
- Codex CLI >= 0.134.0 para usar los perfiles incluidos;
- Python >= 3.11 recomendado para diagnóstico completo de TOML, estados y tamaño AGENTS (install/launcher no lo requieren).

Comprobar:

```bash
git --version
codex --version
```

Si `codex` no está instalado, podés igualmente revisar y usar los templates, pero el flujo automatizado está diseñado alrededor de Codex.

---

## 2. Obtener Factory

Con acceso a [FabriJuncal/quiver-v2](https://github.com/FabriJuncal/quiver-v2), cloná usando GitHub CLI:

```bash
gh repo clone FabriJuncal/quiver-v2
cd quiver-v2
```

Alternativamente, usá una distribución v2.2.2 verificada de las [releases publicadas](https://github.com/FabriJuncal/quiver-v2/releases). Comprobá FACTORY_VERSION.md; esta guía no afirma que el tag ya esté publicado. Conservá su ruta en esta terminal:

```bash
ASF_ROOT="$(pwd -P)"
```

---

## 3. Ver antes de instalar

Opcional pero recomendado:

```bash
./scripts/install.sh --dry-run
```

Mostrará qué archivos/configuraciones tocaría.

---

## 4. Instalar

```bash
./scripts/install.sh
export PATH="$ASF_ROOT/scripts:$PATH"
```

El instalador:

- crea `~/.codex/` si hace falta;
- preserva las instrucciones existentes;
- administra solamente un bloque marcado de AI Software Factory;
- enlaza las skills core en `~/.agents/skills/`;
- no instala servicios externos.

---

## 5. Verificar

```bash
./scripts/doctor.sh
```

El resultado ideal termina con:

```text
STATUS: OK
```

Eso verifica archivos y configuración estática, no inferencia ni disponibilidad de modelos. Los warnings indican comprobaciones incompletas, por ejemplo ausencia de un parser TOML. Si aparece `AGENTS.override.md`, revisá las reglas que querés conservar y resolvé explícitamente su prioridad antes de instalar. Factory no altera ese archivo.

---

# Elegí tu camino

## A — Proyecto existente

Entrá al proyecto:

```bash
cd ~/Projects/mi-proyecto
```

Ejecutá:

```bash
"$ASF_ROOT/scripts/adopt-project.sh"
```

Después:

```bash
codex
```

Mensaje inicial:

```text
Adoptá este proyecto existente usando AI Software Factory.

Realizá Project Discovery.
No modifiques código ni arquitectura durante el discovery inicial.

Generá o completá:
- PROJECT_PROFILE.md
- PROJECT_STATE.md
- CAPABILITY_MAP.md

Respetá el stack y las convenciones existentes.
Integrá antes que migrar.
Resolvé el snippet de AGENTS como integrado, ya cubierto o conflicto concreto; no dejes una fusión ambigua pendiente.
```

---

## B — Proyecto nuevo

```bash
mkdir mi-proyecto
cd mi-proyecto
```

Inicializar:

```bash
"$ASF_ROOT/scripts/init-project.sh" --git-init
```

Abrir Codex:

```bash
codex
```

Mensaje:

```text
Quiero crear un proyecto nuevo usando AI Software Factory.

Comenzá por Project Discovery.

No implementes todavía.

Definí primero:
- problema;
- usuarios;
- tipo de producto;
- mercado;
- capacidades necesarias;
- restricciones;
- alternativas importantes.
```

---

# Trabajo diario

Cuando aparezca un ticket:

```text
Tengo este requerimiento:

[TICKET o texto]

Capturalo usando AI Software Factory y guiame hasta el próximo Decision Boundary.
```

Para reanudar otro día:

```text
Continuá PROJ-123.
```

Codex debe leer primero el estado persistido, no pedirte reconstruir el chat. Si recap contradice
STATE, STATE prevalece. Con trabajo autorizado ejecutable, Finalization Gate exige continuar:
`ACCIÓN DEL USUARIO: ninguna` nunca es frase de cierre. Una limitación real exige pendiente y reanudación exacta.

---

# Diagnóstico

Si algo parece mal:

```bash
"$ASF_ROOT/scripts/doctor.sh" --project .
```

Troubleshooting:

[`docs/troubleshooting/CODEX_NO_DETECTA_FACTORY.md`](docs/troubleshooting/CODEX_NO_DETECTA_FACTORY.md)


## Perfiles de IA

Factory utiliza `ECONOMICAL`, `BALANCED` y `ADVANCED`.

No necesitás elegir modelos al crear el proyecto. Discovery define una política general y cada requirement/slice afina el perfil.

Ver: `docs/guides/AI_MODEL_ROUTING.md`.


---

# Configuración opcional de modelos

Inicio recomendado con overrides CLI (superan la configuración del proyecto):

```bash
asf balanced --dry-run
asf balanced
```

No modifica config.toml ni presupone acceso al modelo. La selección efectiva solo se comprueba
con [Session Preflight](docs/guides/SESSION_PREFLIGHT.md) cuando la tarea dependa materialmente.
Para otras terminales, configurá PATH según [ASF Launcher](docs/guides/ASF_LAUNCHER.md).

La Factory funciona usando simplemente:

```bash
codex
```

Si querés iniciar con un perfil conocido:

```bash
"$ASF_ROOT/scripts/configure-model-profiles.sh"
```

Después:

```bash
codex --profile asf-balanced
```

El perfil recomienda (la configuración del proyecto y flags pueden prevalecer):

**GPT-5.6 Terra (`gpt-5.6-terra`) / Medium**

Durante el trabajo, Guided Model Routing solo te interrumpirá si un cambio de perfil tiene beneficio material.

## Actualizar y desinstalar

Actualizá la carpeta Factory desde una release/revisión verificada y ejecutá:

```bash
"$ASF_ROOT/scripts/install.sh"
"$ASF_ROOT/scripts/doctor.sh"
```

Seguí la [guía de upgrade 2.2.1 → 2.2.2](docs/guides/UPGRADE_2_2_1_TO_2_2_2.md) para metadata de proyectos existentes, sin reemplazarla con templates vacíos. Si cambiaste de carpeta, actualizá ASF_ROOT y revisá los enlaces que doctor marque como pertenecientes a otra copia.

Para desinstalar la integración global:

```bash
"$ASF_ROOT/scripts/uninstall.sh" --dry-run
"$ASF_ROOT/scripts/uninstall.sh"
```

Se conservan proyectos, backups y perfiles opcionales. Iniciá Codex sin `--profile asf-...` para dejar de usarlos. Revisá esos archivos antes de retirarlos manualmente.
