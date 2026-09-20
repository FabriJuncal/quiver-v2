# ASF Launcher

Desde la carpeta de Factory, configurá esta terminal:

```bash
ASF_ROOT="$(pwd -P)"
export PATH="$ASF_ROOT/scripts:$PATH"
asf balanced
```

Para nuevas terminales agregá en tu configuración de shell la misma línea `export PATH` con
la ruta absoluta entre comillas. Install no modifica tu shell ni `config.toml`.
También podés ejecutar `"$ASF_ROOT/scripts/asf" balanced` sin configurar PATH.

| Comando | Modelo solicitado | Reasoning |
|---|---|---|
| `asf economical` | GPT-5.6 Luna (`gpt-5.6-luna`) | Low |
| `asf balanced` | GPT-5.6 Terra (`gpt-5.6-terra`) | Medium |
| `asf advanced` | GPT-5.6 Sol (`gpt-5.6-sol`) | High |
| `asf exceptional` | GPT-6 Astra (`gpt-6-astra`) | High |

Exceptional conserva su uso excepcional. High es determinista y evita suponer soporte XHigh;
solo seleccionar XHigh manualmente si el runtime lo soporta y la tarea lo justifica.

El launcher usa `--model ID --config 'model_reasoning_effort="medium"'` (según perfil), la capa
de mayor precedencia documentada. No usa `--profile`, no edita configuración ni salta permisos.
No cambia provider/auth ni garantiza disponibilidad. Políticas administradas y capacidades del
runtime siguen vigentes; Plan mode puede tener su propio reasoning, ver referencia oficial.

```bash
asf balanced --dry-run
asf balanced --cd "/ruta/proyecto con espacios" --no-alt-screen -- "Continuá REQ-123."
```

Admite `--cd/-C`, `--add-dir`, `--image/-i` (un archivo por flag), `--sandbox/-s`,
`--ask-for-approval/-a`, `--search`, `--no-alt-screen`, `--help`, `--version` y un prompt.
Preserva literalmente espacios y metacaracteres, sin eval. Opciones desconocidas y overrides
`--model`, `--profile`, `--config`, provider/remote se rechazan antes de lanzar: usar `codex`
directamente para configuraciones distintas. Subcomandos se tratan como prompt, no se ejecutan.

`--dry-run` verifica CLI en PATH y muestra argumentos; no inicia inferencia ni prueba acceso al
modelo. Si Codex devuelve error se conserva stderr y exit code, se muestra selección manual
exacta y cómo reanudar. Si el cliente sigue abierto mostrando un error del servidor, consultá
`/model` allí; el wrapper solo puede detectar errores que el proceso devuelva al salir.

Alternativa (perfiles previamente instalados): `codex --profile asf-balanced`. El proyecto puede
prevalecer sobre ese perfil, por lo que no ofrece la misma precedencia del launcher.
