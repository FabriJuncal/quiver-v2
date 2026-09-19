# Evidencia — correcciones de preproducción

Fecha: 2026-09-19. Alcance: plan aprobado v1, findings F01–F14. Base Git: `2c72d1c`; working tree previamente modificado. Esta validación corresponde al contenido local, no a una release publicada ni a un commit nuevo del repositorio real.

## Resultado y entornos

- macOS arm64, Bash 3.2, Python 3.14: **22 tests OK**, exit 0.
- Linux, imagen local `node:20-bullseye`, Python 3.9: **22 tests OK**, exit 0.
- Linux se ejecutó sin red, filesystem del contenedor y repositorio de solo lectura, y un `/tmp` efímero escribible/ejecutable para fixtures.
- `git diff --check`: exit 0.
- No se modificó la configuración personal de Codex ni se publicaron cambios. Cada test usa HOME/CODEX_HOME aislados solo para sus procesos hijos.

## Comandos reproducibles

Desde la raíz de Factory:

```bash
python3 -B -m unittest discover -s tests -v
git diff --check
```

En este macOS se usó `/opt/homebrew/bin/python3` (3.14), porque el `python3` de sistema es 3.9. Linux usó el intérprete incluido en la imagen existente:

```bash
docker run --rm --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --tmpfs /tmp:rw,exec,nosuid \
  -v "$PWD:/factory:ro" -w /factory node:20-bullseye \
  python3 -B -m unittest discover -s tests -v
```

Salida relevante en ambos entornos:

```text
Ran 22 tests
OK
```

La duración depende del equipo; no es un benchmark de latencia o costo de IA.

## Cobertura ejecutada

| Prueba / comandos internos | Resultado observado |
|---|---|
| `bash -n` para cada `.sh` de scripts y lib | Cada archivo verificado individualmente. |
| `install.sh --dry-run`, `install.sh` dos veces, `doctor.sh` | Sin escrituras en dry-run; reinstalación idéntica; bloque único. |
| `configure-model-profiles.sh --dry-run --force`, instalación y `doctor.sh` | Dry-run sin crear directorios; cuatro perfiles; configuración personal conservada. |
| `configure-model-profiles.sh --force` repetido | Backups diferentes aun con timestamp fijo, contenido previo preservado, modo 0600 conservado. |
| `uninstall.sh --dry-run`, uninstall dos veces | Conserva contenido personal, perfiles opcionales y skills ajenas; segunda ejecución sin cambios. |
| Marcadores incompletos, invertidos, duplicados; archivo sin newline | Rechazo sin mutaciones; acción de reparación explícita. |
| Symlinks normales/colgantes, `AGENTS.md.new`, destinos directorio, docs enlazado | Sin sobrescritura del destino ajeno; rechazo previo a escrituras cuando corresponde. |
| `AGENTS.override.md` | Install rechaza y doctor informa fallo sin modificarlo. |
| Codex simulado 0.133.0 / comando de versión fallido | Rechazo de versión incompatible / advertencia explícita NO VERIFICADA. |
| TOML inválido | Error real de parseo con Python 3.14; Linux sin tomllib informa TOML NO VERIFICADO, no validez ficticia. |
| Estado sin próxima acción | `doctor.sh --project` falla con el campo faltante identificado. |
| `init-project.sh --git-init` dos veces | Scaffold, versión 2.2.1, estado inicial accionable y Git; segunda ejecución idéntica. |
| `adopt-project.sh` dos veces sobre Git, AGENTS, código y docs propios | Originales incluidos `.git` preservados; snippet explícito; segunda ejecución idéntica. |
| Argumentos desconocidos en los seis scripts | Error antes de cualquier escritura. |
| Manifest vs recursos | Versión, scripts y diez skills coinciden con archivos distribuidos. |
| `git archive --format=zip HEAD` en copia Git temporal | Excluye paquete histórico; conserva bit ejecutable del instalador; instalación, perfiles, doctor y uninstall desde lo extraído funcionan. No se hizo commit en el repositorio del usuario. |

Los tests usan un stub de `codex --version`, no inferencias remotas. El test de distribución usa Bash para ejecutar los scripts extraídos y comprueba además el permiso ejecutable guardado en el ZIP.

## Fallos encontrados durante la verificación

- Primera corrida macOS: doctor ejecutaba primero el Python de sistema, que creó cachés bajo el HOME temporal. Se priorizaron intérpretes modernos y ejecución aislada `-I -B`; regresión posterior OK.
- Primera corrida Linux: el tmpfs predeterminado era noexec y no permitía ejecutar el stub de Codex (exit 126). Se habilitó exec solo en el temporal del contenedor. Además se corrigió doctor para que un fallo de `codex --version` produzca una advertencia explícita, con test de regresión propio.
- Ninguno de esos fallos se presenta como una corrida exitosa.

## Simulación de Guided Mode A–H

Revisión de contratos y artefactos, no ejecución de un agente remoto:

| Escenario | Próxima acción derivable y control |
|---|---|
| A. Proyecto nuevo | Scaffold probado → `codex` → mensaje Discovery; inspeccionar, no implementar, solicitar solo datos/decisiones faltantes. |
| B. Proyecto existente | Scaffold probado conserva código/AGENTS → Discovery → resolver snippet como integrado, cubierto o conflicto concreto. |
| C. Espera de criterios | `Acceptance criteria: pending` mantiene boundary aunque no haya Model Gate; presentar criterios y respuesta de aprobación. |
| D. Plan aprobado | Verificar versión y autorización separada; continuar si ya existe, o pedir `Ejecutar plan aprobado`. |
| E. Slice interrumpida | Contrastar Git/evidencia con STATE; completar solo lo pendiente sin repetir acciones destructivas ni gates de fase confirmados. |
| F. Nueva sesión | Leer estado y artefactos; no reconstruir del chat ni asumir modelo activo; verificar configuración solo si la próxima tarea material lo exige. |
| G. Blocker | Identificar dato/acceso/decisión exactos y cómo resolverlos; no interpretar `false` o `continuar` como permiso para saltarlo. |
| H. Requirement cerrado | Retirar activo y continuar el siguiente ya priorizado/autorizado; si no lo hay, registrar espera de nueva petición. |

## Trazabilidad de correcciones

- F01–F03: validación previa, archivos temporales exclusivos, reemplazo atómico, backups únicos y permisos conservados.
- F04/F07: boundaries agregados, estado inicial reanudable, aprobación del reviewer/humana/ejecución diferenciadas.
- F05: doctor detecta override, versión y TOML; separa estático de runtime.
- F06: review sobre diff/evidencia real, alcance/base resueltos, excepción técnica N3 aprobada, una ronda dirigida antes de escalar obligatorios persistentes.
- F08/F09: estrategia normativa en STATE, IDs como recomendaciones fechadas, herencia de slices, confirmación por fase/sesión, fallback por suficiencia/costo y antithrashing.
- F10: suite de comportamiento y CI macOS/Linux, sintaxis archivo por archivo, distribución comprobada.
- F11/F14: argumentos estrictos, dry-run sin escrituras, quoting, idempotencia, residuos de uninstall explícitos.
- F12: manifest único, onboarding sin URL inventada, tag documentado v2.2.1, manual antiguo convertido en referencia, ZIP preservado en `docs/archive/` y excluido de releases.
- F13: N0–N3 definidos y ruta compacta N0/N1 sin exigir el paquete completo; riesgo/testing/modelo siguen separados.

## Límites y pendientes externos

- No se ejecutó inferencia paga ni `/review` remoto. Disponibilidad real por cuenta, reasoning efectivo del reviewer y mejora cuantitativa de costo/latencia: **NO VERIFICADOS en esta implementación**. Las verificaciones del catálogo de la auditoría anterior no equivalen a disponibilidad garantizada.
- CI quedó configurado, pero no se afirmó una corrida en GitHub Actions: las corridas fueron locales.
- La revisión de implementación fue self review del código y evidencia; no se presenta como review independiente. Antes de una publicación pública se recomienda un reviewer adicional de las escrituras de filesystem.
- El endurecimiento supone directorios padre confiables y ausencia de escrituras concurrentes. No es una defensa frente a un atacante local que controla esos directorios.
- No hay release publicada: confirmar repositorio destino y revisar/incluir los cambios preexistentes antes de crear el commit/tag definitivo. La prueba de archive es de una copia temporal, no certifica el HEAD actual como distribuible.
