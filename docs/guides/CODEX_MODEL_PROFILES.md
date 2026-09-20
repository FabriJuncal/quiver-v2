# Perfiles opcionales de Codex

AI Software Factory incluye configuraciones opcionales para iniciar sesiones con un perfil conocido.

No son obligatorias.

Para fijar la configuración de inicio por encima de overrides del proyecto, usar
[asf balanced](ASF_LAUNCHER.md). Un perfil representa REQUESTED PROFILE, no prueba
EFFECTIVE SESSION CONFIG. [Session Preflight](SESSION_PREFLIGHT.md) es condicional.

Requieren **Codex >= 0.134.0**, versión que adoptó archivos de perfil separados. Comprobar con `codex --version`; `doctor.sh` detecta clientes anteriores. [Documentación oficial](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles).

## Instalar

```bash
./scripts/configure-model-profiles.sh
```

Esto crea, si no existen:

```text
~/.codex/asf-economical.config.toml
~/.codex/asf-balanced.config.toml
~/.codex/asf-advanced.config.toml
~/.codex/asf-exceptional.config.toml
```

No modifica `~/.codex/config.toml`.

## Usar

### ECONOMICAL

```bash
codex --profile asf-economical
```

Solicita (sujeto a precedencia):

**GPT-5.6 Luna (`gpt-5.6-luna`) / Low**

### BALANCED

```bash
codex --profile asf-balanced
```

Solicita (sujeto a precedencia):

**GPT-5.6 Terra (`gpt-5.6-terra`) / Medium**

y configura review con:

**GPT-5.6 Sol (`gpt-5.6-sol`)**

### ADVANCED

```bash
codex --profile asf-advanced
```

Solicita (sujeto a precedencia):

**GPT-5.6 Sol (`gpt-5.6-sol`) / High**

### Exceptional

```bash
codex --profile asf-exceptional
```

Solicita (sujeto a precedencia):

**GPT-6 Astra (`gpt-6-astra`) / High**

Usarlo únicamente si está disponible y se justifica.

---

# Si preferís seguir usando solo `codex`

Perfectamente válido.

La Factory funcionará con Model Gates.

Para convertir BALANCED en tu default personal, podés configurar manualmente en `~/.codex/config.toml`:

```toml
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
review_model = "gpt-5.6-sol"
```

Antes de editarlo:

- revisar si ya existen esas claves;
- no duplicarlas;
- hacer backup.

Factory no cambia este archivo automáticamente porque es una preferencia personal del usuario.

---

# Prioridad de configuración

Orden completo verificado: CLI/`--config` > proyecto confiable (más cercano) > archivo de
perfil > config usuario > defaults cloud > sistema > defaults integrados. Ver
[referencia oficial y límites](../references/OPENAI_CODEX_MODEL_ROUTING.md).

Los flags CLI pueden sobrescribir perfiles.

Ejemplo:

```bash
codex --profile asf-balanced --model gpt-5.6-sol
```

La selección explícita de CLI tiene prioridad.

La configuración `.codex/config.toml` de un proyecto confiable también puede prevalecer sobre el perfil. Verificar selección efectiva con `/status` y disponibilidad con `/model`. Un perfil no garantiza acceso al modelo en todas las cuentas.

`review_model` selecciona modelo de review, no verifica su reasoning. Factory no inventa una configuración de reasoning de review no documentada; declara NO VERIFICADO si el runtime no lo expone.

---

# Disponibilidad

Si un perfil usa un modelo que no aparece en tu cuenta:

- iniciar con otro perfil disponible;
- usar `/model`;
- seguir el fallback de `config/MODEL_CATALOG.md`.

El perfil no debe bloquear el proyecto.

Si tampoco está disponible el fallback, seguir el gate del catálogo y no ejecutar trabajo crítico con capacidad insuficiente. Respetar boundaries de costo material. Perfiles existentes se conservan; `--force` crea backup único, pero rechaza symlinks. Uninstall conserva estos archivos y lo informa.
