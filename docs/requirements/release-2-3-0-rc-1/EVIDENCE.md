# Evidencia — candidata local, 2026-09-21

## Alcance y autorización

Preparación de v2.3.0-rc.1 e integración mínima inactiva. Un único piloto condicional
autorizado; **NOT RUN, cero ayudantes y cero intentos**. No push/tag/publicación.
No se cambió configuración habitual. No se solicitó Full Access.

## Controles previos y resultado

| Control | Evidencia reutilizada/nueva | Decisión |
|---|---|---|
| Escritura en copia | Política supervisada v2 aprobada previamente; auditoría offline | No prometer solo lectura garantizada |
| Original/baseline/configuración | Ensayo previo codex sandbox: 22/22 operaciones sintéticas | Verificado solo para comandos; herencia al hijo NO VERIFICADA |
| No subdelegación | Schema de spawn_agent de esta sesión no acepta rol/config/tool policy; runtime permite hijos recursivos | No verificable para ayudante: obligatorio pendiente |
| No acciones externas mutantes | Sandbox oficial gobierna comandos, no Apps/MCP/browser; no inventario efectivo del hijo disponible | Obligatorio pendiente |
| Identidad/detención | Herramientas de listado/espera/interrupción existen, pero no prueba de fin de toda actividad | Efectividad del hijo NO VERIFICADA |
| Registro persistente | Escritura del coordinador disponible; no preparar run para un dispatch rechazado | Preflight bloqueado, no se lanzó nada |

Falta un vínculo verificable entre custom role y creación del ayudante, su inventario
efectivo y mecanismo de detención. No afirmar que Codex en general no lo soporta:
la interfaz de esta sesión no expone esa selección. Dar instrucciones no sustituye
los controles que el usuario mantuvo obligatorios. No se instaló runtime alternativo.

## Verificación oficial y local

- [Subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents), consultado
  hoy: roles TOML y agents.enabled; overrides vivos del padre reaplicados al hijo.
- [Permisos](https://learn.chatgpt.com/docs/permissions#scope-and-enforcement), consultado
  hoy: límites de comandos no gobiernan servicios externos/Apps/MCP/browser.
- `codex --version`: **codex-cli 0.155.1**.
- `gh api repos/FabriJuncal/quiver-v2/tags --jq '.[].name'`: v2.2.2 y v2.2.1;
  no v2.3.0-rc.1. Consulta read-only; no tag reservado en remoto.
- Configuraciones propuestas evaluadas como overrides con `codex ... features list`
  en HOME/CODEX_HOME/TMPDIR temporales: ambos parsers exit 0; agents.enabled con tipo
  inválido rechazado exit 1 en ambos. No sesión/inferencia ni selección real de rol.
- Ayudante: shell_tool=false, apps/hooks/remote_plugin=false; unified_exec=true pese
  al override false. Discrepancia, no prueba por sí misma de herramienta o escape.
- Salida completa y harness local: `/private/tmp/asf-release-candidate.lV4Sv6/PARSER_RESULT.json`
  y `probe_config.py`; excluidos de distribución.

## Pruebas hasta la revisión del artefacto

| Comando | Resultado real |
|---|---|
| `bash scripts/check-release.sh` | PASS |
| `python3.14 -B -m unittest discover -s tests -v` (inicial) | 117 tests; 1 fallo de exportación |
| mismo comando después de corrección | **117 tests OK, 24.475 s** |
| `python3.14 -I -B scripts/lib/check_execution.py --project examples/guided-delegation/project` | STATIC PASS, 1 run; runtime NO VERIFICADO |
| mismo checker con `examples/supervised-multiagent/project` | STATIC PASS, 1 run; NO APTO PARA PILOTO |
| `git diff --check` en candidata | exit 0 |

La suite incluye instalación/dry-run/reinstalación/doctor/uninstall en HOME temporal,
perfiles preservados, launchers simulados y cuatro dry-runs, init/adopt sin cambios
de código, invariants, v1/v2, auditoría de archivos, versiones RC y upgrade desde
capa 2.2.2 sintética. No es ejecución de modelos. ZIP de prueba instala correctamente.

## Configuración habitual

SHA-256 antes/después coincidentes en comprobación selectiva:

- config.toml: `95f3580c0289d8b36421e1250852f6e05b574db414325e09b13f8f537764a1f0`
- AGENTS.md: `6e9835f7f514656c337ef3590ca902f7301fddc9bd73792d7a2228f091e1d881`

No certifica todos los logs del cliente. No se copian credenciales ni IDs de plugins
personales a la propuesta pública; se preservan trials originales solo en copia local.

## Artefacto y verificaciones finales

- Código preparado en commit local `c1e9f2402d6c2c2d955fee01a7e22a54357e01fe`.
- Suite en checkout de ese commit: **117 OK, 27.187 s**.
- ZIP generado por `git archive` y extraído con unzip en carpeta con versión RC:
  **117 OK, 25.657 s**, mismo comando unittest dentro del directorio extraído.
- `bash scripts/check-release.sh` desde ZIP: PASS; ejemplos v1/v2 STATIC PASS;
  checker de propuesta exit 2, DISABLED/NOT RUN, como se exige.
- Smoke adicional `upgrade_smoke.py`: instaló la **2.2.2 real del checkout publicado**,
  adoptó proyecto sintético y actualizó con el ZIP RC en HOME temporal. PASS:
  dry-runs/reinstall/perfiles/doctor/uninstall; configuración, perfil personalizado y
  proyecto conservados; capa antigua y enlaces a skills viejas avisados. No agentes.
- Evidencia completa del smoke: `/private/tmp/asf-release-candidate.lV4Sv6/UPGRADE_RESULT.json`.
- Escaneo dirigido de patrones de claves/tokens privados sobre candidata: sin
  coincidencias (rg exit 1). No equivale a garantía de ausencia de todo secreto.
- `git diff --cached --check` detectó cuatro líneas vacías finales heredadas en
  briefs cerrados S01–S04; se preservaron sin reescribir evidencia histórica.
  `git -c core.whitespace=-blank-at-eof diff --cached --check`: exit 0.
- Source local no tenía Git: rama creada en clon separado, sin alterar checkout
  de publicación previo. Cambio ajeno de publish-v2.2.1 preservado solo en source.
- `config.toml` y `AGENTS.md` habituales nuevamente idénticos a hashes iniciales.

Paquete/sha256/bundle final se guardan en `.release-candidates/2.3.0-rc.1/`
(ignorado por Git). Su ARTIFACTS.json identifica revisión y hashes sin ciclo de
autorreferencia. El commit de cierre modifica solo evidencia/estado excluidos del
ZIP; comparar contenido y permisos de cada entrada contra el ZIP que pasó tests.

CI remota macOS/Linux y review independiente NO ejecutados. No se probó continuidad
viva S04→S05, modelo efectivo ni comportamiento de ayudante. Publicación no autorizada.
