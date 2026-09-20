# Codex: verificación oficial de configuración

Verificado el 2026-09-20 contra páginas oficiales abiertas, independientemente de afirmaciones previas de Factory.

## Precedencia (mayor → menor)

1. Flags CLI y `--config`.
2. `.codex/config.toml` de proyectos confiables, raíz → cwd; el más cercano prevalece.
3. Perfil elegido con `--profile nombre`: `$CODEX_HOME/nombre.config.toml`.
4. Usuario `$CODEX_HOME/config.toml` (default `~/.codex/config.toml`).
5. Defaults administrados en la nube cuando existen.
6. Sistema, `/etc/codex/config.toml` en Unix.
7. Defaults integrados.

Las restricciones administradas en `requirements.toml` se aplican aparte; no son eludibles
por el launcher. Proyectos no confiables omiten la capa de proyecto.
[Fuente oficial: Config basics](https://developers.openai.com/codex/config-basic/).

## Flags, perfiles y reasoning

`--model` selecciona modelo; `-c`/`--config` acepta clave=valor TOML, por ejemplo
`--config 'model_reasoning_effort="medium"'`. El orden relativo entre overrides duplicados
no es necesario para el launcher y queda **NO VERIFICADO** aquí.
[Overrides oficiales](https://learn.chatgpt.com/docs/config-file/config-advanced#one-off-overrides-from-the-cli).

Desde Codex 0.134.0, named profiles son archivos separados con claves top-level, no tablas
`[profiles.nombre]` ni selector `profile` dentro de config.toml. Proyecto y CLI prevalecen.
[Profiles oficiales](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles).

`model_reasoning_effort` aplica cuando el modelo lo soporta. La referencia también define
`plan_mode_reasoning_effort`: Plan puede tener una política distinta. El launcher fija el
inicio normal; no afirma que todos los modos o el review usen ese reasoning.
`review_model` tampoco demuestra reasoning del reviewer.
[Config reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Instrucciones

Codex elige AGENTS.override.md antes que AGENTS.md, global y por directorio; admite fallback
names configurados. Combina la cadena de raíz del proyecto a cwd. `project_doc_max_bytes`
tiene default **32 KiB (32768 bytes)**, configurable. Doctor estima esa cadena y distingue
riesgo estático de truncamiento observado.
[AGENTS oficial](https://developers.openai.com/codex/guides/agents-md/).

## Evidencia y límites

- CLI local: `codex --version` → `codex-cli 0.155.1`; `codex --help` confirma `--model`,
  `--config`, `--profile` y ruta del perfil. Ambos exit 0, con aviso del sandbox sobre aliases PATH.
- Launcher: argv y fallos simulados, sin inferencia paga. Ver EVIDENCE del requirement.
- Precedencia: verificada oficialmente; selección de una sesión con inferencia real
  **NO VERIFICADA** aquí. Terra/High por override de proyecto es una causa posible,
  no diagnóstico probado de la sesión original.
- Modelo/reasoning activo de esta conversación y disponibilidad por cuenta: **NO VERIFICADOS**.
- Obediencia del modelo al Finalization Gate: **NO VERIFICABLE** con tests estáticos.
  Probar continuidad S04 → S05 en sesión real del proyecto.
