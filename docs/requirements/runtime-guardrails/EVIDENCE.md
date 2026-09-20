# Evidencia — Runtime Guardrails v2.2.2

Fecha: 2026-09-20. Entorno local macOS, Bash, Python 3.14.4 y Codex CLI 0.155.1.
La distribución original no tiene .git. Se comparó con una copia temporal previa a los cambios;
los tests de packaging/adopción crean repositorios Git propios y aislados.

## Resultados ejecutados

| Comando / escenario | Resultado observado |
|---|---|
| `bash scripts/check-release.sh` | PASS; sintaxis bash, archivos, versiones, mappings, gate, rutas y selecciones sin alias ambiguo |
| `python3.14 -B -m unittest discover -s tests -v` | 44 tests, 17.646 s, OK; exit 0 |
| `install --dry-run`, install, reinstall, doctor, uninstall, uninstall repetido | PASS dentro de suite; snapshots comprueban idempotencia y preservación |
| `configure-model-profiles --dry-run`, install, preservación y force con backup | PASS; conserva perfiles personales y config.toml |
| Launcher cuatro perfiles dry-run | PASS en fixture y CLI local; sin inferencia |
| Launcher con ruta/argumentos con espacios y metacaracteres | PASS; argv literal, sin eval ni escrituras a config |
| Codex ausente / modelo rechazado simulado | PASS; exit 127 / 42, error original y pasos guiados |
| `init-project --git-init` | PASS; metadata 2.2.2, Guided Mode, Finalization Gate y runtime limitation |
| `adopt-project` sobre Git + AGENTS + código + docs existentes | PASS; snapshot conserva todos los originales, repetición idempotente |
| Requirement activo + S05 activa + Next action vacío | FAIL esperado del doctor, test PASS |
| Requirement activo + S05 activa + usuario false + Next action | PASS; doctor indica CONTINUAR y no escribe |
| Requirement completed con slice active o referencia activa obsoleta | FAIL esperado del doctor, test PASS |
| Capa proyecto/AGENTS 2.2.1 | WARN esperado + prompt exacto de upgrade; snapshot idéntico |
| Tamaño AGENTS, cap explícito, override/nesting y perfil no seleccionado | PASS; warning/errores diferenciados, sin asumir configuración efectiva |
| ZIP temporal por git archive | PASS; incluye launcher ejecutable y CI, instalación/perfiles/doctor/uninstall funcionan |
| `bash scripts/doctor.sh` sobre instalación real | exit 0, OK WITH WARNINGS: bloque global antiguo y perfiles opcionales ausentes |
| `codex --version`, `codex --help` | exit 0; 0.155.1 y flags presentes; aviso sandbox de aliases PATH |
| `bash scripts/asf.sh balanced --help` | exit 0; CLI real acepta invocación; no prueba selección con inferencia |
| `git diff --no-index --check` contra baseline | sin diagnósticos whitespace; exit 1 indica diferencias en modo no-index |

Primer intento de check-release usó Python 3 del sistema sin tomllib y falló antes de la suite.
Se corrigió resolución a Python >= 3.11 con error guiado si falta; ejecuciones posteriores PASS.
Las suites intermedias de 40 y 43 tests también terminaron OK; la evidencia final es la de 44.

## Qué demuestran

Fixtures ejecutan scripts reales con HOME/CODEX_HOME temporales (solo entorno de procesos hijos).
Codex simulado permite comprobar argv y errores sin llamadas pagas. Las comprobaciones de
contrato demuestran presencia/coherencia de reglas, no obediencia garantizada del modelo.
Se preservaron código/decisiones de proyectos; no se ejecutó upgrade sobre nuevo-proyecto.

AGENTS global real medido: 11.041 bytes; default oficial 32.768. No evidencia de truncamiento
actual en ese archivo. Bloque nuevo generado < 3.000 bytes en fixture; texto personal externo
al bloque permanece intacto. La instalación global se entrega como comandos al usuario.

## Verificación externa

Precedencia y límite comprobados en páginas oficiales abiertas de OpenAI, con fecha y enlaces
en [referencia](../../references/OPENAI_CODEX_MODEL_ROUTING.md). La skill OpenAI Docs llevó a
verificar estas fuentes antes de fijar el launcher. Context Scout limitó lecturas a áreas afectadas.
Implementation Reviewer y Closure Evidence exigieron diff/pruebas actuales y registro de límites.

## No verificado / fuera del alcance

- Inferencia real y disponibilidad de modelos/reasoning en la cuenta; no se afirma modelo activo.
- Continuidad S04 → S05 en sesión real: prueba operativa posterior a instalar/actualizar proyecto.
- GitHub Actions remoto y ejecución Linux: workflow preparado, no publicado/ejecutado remotamente.
- No release/tag/commit de distribución, cambio de shell/config personal ni upgrade de nuevo-proyecto.
- Metadatos .DS_Store cambiaron durante la sesión por el entorno; excluidos de revisión funcional,
  no modificados intencionalmente ni eliminados.

## Resultado

READY para instalar y realizar la prueba operativa indicada. No equivale a publicación ni
garantía de comportamiento del runtime. No quedan findings obligatorios abiertos.

## Publicación posterior

Autorizada y realizada el 2026-09-20: commit/tag anotado `v2.2.2` en
`20ea27ac33f92928f2e8ebe7a0c0cf4f14bd8a67`; release con ZIP y checksum.
GitHub reportó el digest del ZIP como
`sha256:30b2ff08d6e6c5f5b47bbe94b493309f9367a36b38284ae622505e0dc2cd098a`, igual al generado.
CI Validate y Factory v2.2.2 Runtime Guardrails: success. Esto no verifica inferencia real.
