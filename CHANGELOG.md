# Changelog

## 2.3.0-rc.2 — Supervised Delegation Preview (candidate)

- Model routing `routing-v1`: verificabilidad y costo de comprobar errores como señales de selección.
- Ruta rápida para heredar una decisión vigente sin reclasificar cada slice ni repetir gates.
- Diagnóstico de entorno, contexto y requisitos antes de escalar capacidad o reasoning.
- Reintentos requieren evidencia, hipótesis o enfoque nuevos y una comprobación discriminante.
- Decisión o referencia de routing auditable en planning, ejecución y review, con excepciones proporcionales N0/consultas.
- Catálogo central como fuente del mapping; menos duplicación entre skill, contrato y templates.
- Preview multiagente continúa inactiva: piloto NOT RUN y controles runtime de RC-F02 pendientes.

## 2.3.0-rc.1 — Supervised Delegation Preview (tagged)

- Contratos de delegación secuencial opt-in v1 y supervisada v2; contexto mínimo,
  ownership del coordinador, intentos acotados y aceptación basada en evidencia.
- Inventarios y auditoría de copia/original; rechazo de incidentes sin restaurar trabajo humano.
- Ejemplos sintéticos, validación de runs y regresiones offline; no prueban conducta viva.
- Propuesta de ayudante inactiva, sin instalación automática ni dispatcher; checker
  devuelve exit 2 incluso con STATIC PASS: controles efectivos NO VERIFICADOS.
- Doctor reconoce RC y ordena correctamente RC/estable; actualización de capa conservadora.
- Paquete excluye evidencia de desarrollo y trials locales; guías de instalación y upgrade.
- Piloto NOT RUN: interfaz evaluada no enlaza el rol/permisos del hijo ni verifica
  bloqueo de recursión/herramientas externas. No anunciar multiagente operativo.

## 2.2.2 — Runtime Guardrails

- Finalization Gate canónico impide cierres con trabajo autorizado ejecutable; cuatro invariants de estado.
- Prioridad evidencia → STATE → proyecto → artifacts/docs → recap/chat; recuperación explícita de contradicciones.
- Runtime limitations separadas de blockers funcionales, con pendiente y reanudación exacta.
- Requested profile separado de effective session config unknown; Session Preflight condicional.
- Launcher `asf` con overrides CLI de modelo/reasoning, dry-run, argumentos seguros y fallos guiados.
- Precedencia Codex y límite AGENTS verificados oficialmente; doctor de tamaños, conflictos, versiones y estados.
- Upgrade conservador 2.2.1 → 2.2.2; metadata versionada en proyectos y AGENTS.
- Bloque global reducido, Review Loop Guard con IDs estables y presupuesto existente justificado.
- Pruebas temporales ampliadas y CI macOS/Linux; sin servicios, orquestación ni switching invisible.

## 2.2.1 — Guided Model Routing

### Fixed

- Hardening de preproducción: marcadores validados, destinos sin symlinks, temporales exclusivos, backups únicos y permisos preservados.
- Dry-run sin escrituras, argumentos estrictos, reinstalación estable y desinstalación que conserva bloques de otra instalación.
- Doctor detecta override global, clientes anteriores a 0.134.0 y TOML inválido cuando dispone de Python 3.11+; declara runtime no verificado.
- Estados iniciales reanudables, aprobaciones separadas, gates por fase, review con límite de corrección y ruta compacta N0/N1.
- Regresión aislada de scripts en CI macOS/Linux y documentación de publicación coherente.
- El catálogo usa siempre nombres completos: **GPT-5.6 Luna**, **GPT-5.6 Terra**, **GPT-5.6 Sol** y **GPT-6 Astra**.
- Se evita el alias ambiguo `gpt-5.6` en recomendaciones de Factory.
- La Factory ya no supone conocer el modelo activo de la sesión.
- Modelo y esfuerzo de razonamiento se tratan como decisiones diferentes.
- Los downgrades ya no interrumpen por tareas cortas o mecánicas.
- El review dedicado ya no se confunde con cambiar de modelo dentro del mismo hilo.

### Added

- **AI Model Gate** guiado con instrucciones exactas `/status` → `/model` → `continuar`.
- **Switch Benefit**: LOW / MEDIUM / HIGH.
- **Switch Threshold** para evitar cambios de modelo constantes.
- Escalamiento suave de reasoning antes de cambiar de modelo cuando es suficiente.
- Fallbacks explícitos por disponibilidad.
- Política de review: N0/N1 self-review, N2 `/review` selectivo/recomendado, N3 `/review` requerido.
- Skill core `model-router`.
- Perfiles Codex opcionales:
  - `asf-economical`
  - `asf-balanced`
  - `asf-advanced`
  - `asf-exceptional`
- Script `scripts/configure-model-profiles.sh`.
- Guía `GUIDED_MODEL_GATES.md`.
- Guía `CODEX_MODEL_PROFILES.md`.
- Upgrade guide 2.2.0 → 2.2.1.

### Design rule

AI Software Factory recomienda y gobierna perfiles, pero no afirma que el runtime cambió de modelo hasta que el usuario lo confirme o el runtime lo exponga de manera verificable.

## 2.2.0 — AI Model Routing

### Added

- `config/MODEL_CATALOG.md`.
- AI Policy en `PROJECT_PROFILE.md`.
- AI Strategy por requirement.
- AI Execution Profile por slice.
- reglas de escalamiento y downgrade.
- registro liviano de perfiles usados en Closure.

### Changed

- Project Discovery define política IA general, no un modelo único.
- Requirements recomiendan perfiles de planning/implementation/review.
- Slices pueden usar perfiles diferentes dentro del mismo requirement.
- La Factory no afirma cambios de modelo que el runtime no haya realizado.
- Optimización orientada a costo total por tarea, no solo precio por llamada.

## 2.1.0 — Guided Mode

### Added

- Guided Mode.
- Decision Boundaries.
- `Next action`, `User action required`, `Expected output` y `After this` en estados.
- Reanudación desde estado persistente.
- Instalador idempotente.
- `doctor.sh`.
- Desinstalador seguro.
- Inicialización de proyectos nuevos.
- Adopción no destructiva de proyectos existentes.
- Skills core instalables globalmente.
- Documentación pública para GitHub.

### Changed

- El workflow avanza hasta el próximo Decision Boundary en lugar de detenerse por cada micro-etapa.
- Plan Review e Implementation Review permanecen separados.
- La Factory deja de asumir que todos los proyectos son SaaS.
- SaaS pasa a ser un capability pack opcional.

## 2.0.0

- Project Discovery.
- New Project / Existing Project.
- `PROJECT_PROFILE.md`.
- `PROJECT_STATE.md`.
- `CAPABILITY_MAP.md`.
- Requirements persistentes.
