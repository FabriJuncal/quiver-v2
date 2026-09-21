# AI Software Factory

AI Software Factory v2.3.0-rc.1 — Supervised Delegation Preview

Candidata local, **no publicada ni lista para activar ayudantes**. Incluye contratos
y pruebas offline; piloto vivo NOT RUN por controles runtime pendientes.
Ver [estado y notas de la candidata](docs/releases/v2.3.0-rc.1.md).

Inicio determinista desde la carpeta de Factory:

```bash
ASF_ROOT="$(pwd -P)"
./scripts/install.sh
export PATH="$ASF_ROOT/scripts:$PATH"
asf balanced
```

Alternativa con perfiles instalados: `codex --profile asf-balanced` (la configuración del
proyecto puede prevalecer). Ver [Quick Start](QUICK_START.md) para instalación, init/adopt y
[upgrade de proyectos](docs/guides/UPGRADE_2_2_2_TO_2_3_0.md).

Conserva Runtime Guardrails: continuidad obligatoria, prioridad de STATE sobre recap y diagnóstico
de configuración/estado. `ACCIÓN DEL USUARIO: ninguna` exige ejecución en el mismo turno.
El [contrato canónico](workflow/00_SHARED_CONTRACT.md) define excepciones reales; las instrucciones
no pueden garantizar obediencia del modelo ni evitar que el runtime interrumpa un proceso.

**AI Software Factory** es un workflow liviano y reutilizable para crear y evolucionar software con agentes de IA sin convertir cada repositorio en una colección de prompts, documentos y automatizaciones difíciles de mantener.

Trabajo local aún no publicado: [piloto de delegación guiada](docs/guides/GUIDED_DELEGATION.md),
con contrato, ejemplos sintéticos y validador offline. Incluye la modalidad
[Factory multiagente supervisada](examples/supervised-multiagent/README.md): auditoría
de copias y rechazo de incidentes, **sin garantía de solo lectura ni piloto vivo validado**.
Inline sigue siendo default. La [integración mínima del ayudante](docs/guides/ASSISTANT_INTEGRATION.md)
incluye configuración inactiva y chequeo fail-closed; no incluye dispatcher operativo.
Instalar/configurar perfiles no habilita workers ni modifica config.toml.

La implementación offline [CE-v1](docs/guides/CONTEXT_ECONOMY_TEXT_HELPER.md) añade
selección mínima de contexto, reutilización de evidencia y contrato para un ayudante
textual opcional de un intento. Sigue deshabilitado: no instala SDK, usa credenciales
ni realiza llamadas.

Alcance inicial aprobado del ayudante: **revisar Specs/Slices y sugerir pruebas**;
sin implementar, ejecutar comandos ni aplicar cambios. Las demás capacidades quedan
postergadas; el piloto sigue condicionado a verificar los controles efectivos.

Funciona con:

- proyectos nuevos;
- proyectos existentes;
- SaaS;
- aplicaciones web o móviles;
- APIs;
- backoffice;
- sistemas internos;
- legacy;
- automatizaciones;
- productos con IA;
- stacks diferentes.

La Factory aporta **método, estado persistente, planificación proporcional, revisión y skills reutilizables**. El proyecto conserva su stack, arquitectura, negocio y convenciones.

## Principios

1. **La Factory se adapta al proyecto.**
2. **El repositorio es la fuente de verdad.**
3. **El chat no es memoria persistente.**
4. **Guided Mode:** avanzar hasta el próximo Decision Boundary.
5. **Integrar antes que migrar.**
6. **Testing proporcional al riesgo.**
7. **Evidence Before Completion.**
8. **Skills bajo demanda, no todas por defecto.**
9. **Complejidad solo cuando una necesidad real la justifica.**

## Instalación rápida

Requisitos: Bash, Git y Codex CLI **>= 0.134.0** para los perfiles incluidos. Python >= 3.11 habilita diagnóstico completo de TOML, estados y tamaños; no es necesario para instalar ni lanzar.

Repositorio: [FabriJuncal/quiver-v2](https://github.com/FabriJuncal/quiver-v2). Si tenés acceso al repositorio, podés obtenerlo con GitHub CLI:

```bash
gh repo clone FabriJuncal/quiver-v2
cd quiver-v2
```

El clon remoto no contiene necesariamente esta candidata local. Para evaluarla, usá
el paquete local entregado; para uso estable consultá las [releases publicadas](https://github.com/FabriJuncal/quiver-v2/releases).
Dentro de la carpeta extraída, comprobá FACTORY_VERSION.md antes de instalar:

```bash
ASF_ROOT="$(pwd -P)"
./scripts/install.sh --dry-run
./scripts/install.sh
./scripts/doctor.sh
```

Doctor verifica archivos/configuración estática. La disponibilidad real de modelos y el reasoning efectivo se comprueban en Codex con `/model` y `/status`. `AGENTS.override.md` tiene prioridad: resolverlo explícitamente si doctor lo señala; Factory no lo reemplaza.

Después elegí uno de los dos caminos:

### Tengo un proyecto existente

```bash
cd "/ruta/al/proyecto"
"$ASF_ROOT/scripts/adopt-project.sh"
```

Luego abrí Codex y decí:

```text
Adoptá este proyecto existente usando AI Software Factory.
Comenzá con Project Discovery.
No modifiques código de aplicación durante el discovery inicial.
```

### Quiero crear un proyecto nuevo

```bash
mkdir mi-proyecto
cd mi-proyecto

"$ASF_ROOT/scripts/init-project.sh" --git-init
```

Luego abrí Codex y decí:

```text
Quiero crear un proyecto nuevo usando AI Software Factory.
Comenzá por Project Discovery.
No implementes todavía.
```

`codex` abre la sesión; pegá el mensaje indicado para iniciar Discovery. Las carpetas de proyecto contienen un estado inicial reanudable, no un Discovery ya realizado.

## Actualizar, retirar y diagnosticar

Desde una copia actualizada y verificada de Factory, ejecutar `./scripts/install.sh` y `./scripts/doctor.sh`; los archivos del proyecto se actualizan mediante la [guía de upgrade](docs/guides/UPGRADE_2_2_TO_2_2_1.md), preservando decisiones.

Para retirar la integración global: `./scripts/uninstall.sh --dry-run` y luego `./scripts/uninstall.sh`. Se conservan proyectos, backups y perfiles opcionales porque pueden contener preferencias personales. Dejá de seleccionar `--profile asf-...` si ya no querés usarlos.

Para diagnosticar un proyecto: `"$ASF_ROOT/scripts/doctor.sh" --project .`. Ver [troubleshooting](docs/troubleshooting/INSTALLATION.md).

## Qué instala

La instalación global agrega únicamente:

- un bloque administrado dentro de `~/.codex/AGENTS.md`;
- symlinks de las **skills core** a `~/.agents/skills/`.

No instala automáticamente:

- MCPs;
- servicios cloud;
- Stripe;
- Supabase;
- Vercel;
- Graphify;
- Codebase Memory;
- Obsidian;
- skills de terceros.

## Arquitectura

```text
~/.codex/AGENTS.md
        │
        ▼
      CODEX
        │
        ├── ~/.agents/skills/       skills globales
        │
        ▼
PROYECTO ACTUAL
├── AGENTS.md
├── PROJECT_PROFILE.md
├── PROJECT_STATE.md
├── CAPABILITY_MAP.md
├── .agents/skills/                 skills específicas
└── docs/requirements/
        │
        ▼
AI SOFTWARE FACTORY
├── workflow/
├── templates/
├── skills/
├── docs/
└── examples/
```

## Documentación

Empezá por:

- [`QUICK_START.md`](QUICK_START.md)
- [`docs/concepts/ARCHITECTURE.md`](docs/concepts/ARCHITECTURE.md)
- [`docs/guides/CONFIGURACION_CODEX.md`](docs/guides/CONFIGURACION_CODEX.md)
- [`docs/guides/PROYECTO_EXISTENTE.md`](docs/guides/PROYECTO_EXISTENTE.md)
- [`docs/guides/PROYECTO_NUEVO.md`](docs/guides/PROYECTO_NUEVO.md)
- [`docs/guides/SKILLS_Y_ROUTING.md`](docs/guides/SKILLS_Y_ROUTING.md)

## Estado del proyecto

Esta versión corresponde a:

**AI Software Factory v2.3.0-rc.1 — Supervised Delegation Preview**

Ver [`FACTORY_VERSION.md`](FACTORY_VERSION.md).

Destino de publicación: `FabriJuncal/quiver-v2`. El acceso depende de la visibilidad y permisos del repositorio; publicar una release no cambia esos permisos. Para nuevas versiones, seguir el [checklist de release](docs/maintainers/RELEASE_CHECKLIST.md). Los paquetes de `docs/archive/` son históricos y no deben instalarse sobre esta versión.

## Licencia

MIT. Ver [`LICENSE`](LICENSE).


## Guided Model Routing

Factory no cambia silenciosamente el modelo de Codex.

Default recomendado:

**GPT-5.6 Terra (`gpt-5.6-terra`) / Medium**

Cuando un cambio de modelo o reasoning aporta valor material, muestra un **AI Model Gate** con instrucciones exactas:

```text
/status
/model
→ modelo exacto
→ reasoning exacto
→ volver y escribir "continuar"
```

Modelos canónicos:

- ECONOMICAL → **GPT-5.6 Luna (`gpt-5.6-luna`) / Low**
- BALANCED → **GPT-5.6 Terra (`gpt-5.6-terra`) / Medium**
- ADVANCED → **GPT-5.6 Sol (`gpt-5.6-sol`) / High**
- Exceptional Override → **GPT-6 Astra (`gpt-6-astra`) / High o XHigh**

Ver:

- `docs/guides/AI_MODEL_ROUTING.md`
- `docs/guides/GUIDED_MODEL_GATES.md`
- `docs/guides/CODEX_MODEL_PROFILES.md`
