# Configuración de Codex

La forma recomendada es utilizar:

```bash
./scripts/install.sh
```

El instalador administra un bloque marcado dentro de:

```text
~/.codex/AGENTS.md
```

No reemplaza el resto del archivo.

## Verificar

```bash
./scripts/doctor.sh
```

## Bloque administrado

Está delimitado por:

```text
<!-- AI-SOFTWARE-FACTORY:START -->
...
<!-- AI-SOFTWARE-FACTORY:END -->
```

Solo ese bloque pertenece al instalador.

## Skills

Las skills core se enlazan en:

```text
~/.agents/skills/
```

Los symlinks apuntan a:

```text
<factory>/skills/core/
```

Actualizar una skill dentro de Factory actualiza inmediatamente la skill disponible para Codex.

## Configuración del proyecto

Las reglas particulares viven en:

```text
<repo>/AGENTS.md
```

Las skills particulares:

```text
<repo>/.agents/skills/
```

No copies toda la Factory dentro del proyecto.


---

# Modelos

Opcionalmente instalar perfiles:

```bash
./scripts/configure-model-profiles.sh
```

Perfiles:

- `asf-economical` → GPT-5.6 Luna (`gpt-5.6-luna`) / Low
- `asf-balanced` → GPT-5.6 Terra (`gpt-5.6-terra`) / Medium
- `asf-advanced` → GPT-5.6 Sol (`gpt-5.6-sol`) / High
- `asf-exceptional` → GPT-6 Astra (`gpt-6-astra`) / High

Factory no modifica `~/.codex/config.toml` automáticamente.

Si preferís `codex` sin `--profile`, podés configurar manualmente Terra/Medium como default y Sol como `review_model`.

Ver `CODEX_MODEL_PROFILES.md`.
