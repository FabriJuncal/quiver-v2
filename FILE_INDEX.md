# File Index

AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview

## Supervised Delegation Preview

- `docs/releases/v2.3.0-rc.2.md` — candidata local, routing reforzado y ayudante deshabilitado
- `docs/guides/ASSISTANT_INTEGRATION.md` — integración inactiva y controles pendientes
- `docs/guides/UPGRADE_2_2_2_TO_2_3_0.md` — upgrade conservador
- `config/assistant-proposal/` — TOML inactivo, no instalado
- `scripts/lib/check_assistant_proposal.py` — exit 2 no equivale a aptitud viva
- `tests/test_release_candidate.py` — RC, upgrade y propuesta
- `docs/guides/CONTEXT_ECONOMY_TEXT_HELPER.md` — selector, reutilización, RUN v3 y walkthroughs offline
- `scripts/lib/context_economy.py` — primitivas offline; ningún SDK o transporte real incorporado
- `tests/test_context_economy.py` — regresión CE-v1 con transporte sintético

## Runtime Guardrails conservados

- `docs/guides/RUNTIME_GUARDRAILS.md`
- `docs/guides/SESSION_PREFLIGHT.md`
- `docs/guides/ASF_LAUNCHER.md`
- `docs/guides/UPGRADE_2_2_1_TO_2_2_2.md`
- `docs/troubleshooting/PREMATURE_STOP.md`
- `docs/troubleshooting/PROFILE_MISMATCH.md`
- `docs/references/OPENAI_CODEX_MODEL_ROUTING.md`
- `scripts/asf` / `scripts/asf.sh`
- `scripts/lib/runtime_doctor.py`
- `scripts/check-release.sh` / `.github/workflows/ci.yml`
- `tests/test_runtime_guardrails.py`

## Primeros pasos

- `README.md`
- `QUICK_START.md`
- `FACTORY_VERSION.md`

## Configuración

- `config/MODEL_CATALOG.md`

## Conceptos

- `docs/concepts/ARCHITECTURE.md`
- `docs/concepts/DECISION_BOUNDARIES.md`
- `docs/concepts/NEW_VS_EXISTING.md`
- `docs/concepts/PROJECT_MODEL.md`
- `docs/concepts/SOURCE_OF_TRUTH.md`
- `docs/concepts/TESTING_PROFILES.md`
- `docs/concepts/RISK_AND_WORKFLOW.md`

## Guías

- `docs/guides/CONFIGURACION_CODEX.md`
- `docs/guides/PROYECTO_EXISTENTE.md`
- `docs/guides/PROYECTO_NUEVO.md`
- `docs/guides/GUIDED_MODE.md`
- `docs/guides/SKILLS_Y_ROUTING.md`
- `docs/guides/GIT_WORKFLOW.md`
- `docs/guides/HERRAMIENTAS_DE_CONOCIMIENTO.md`
- `docs/guides/ARGENTINA_Y_PROVEEDORES.md`
- `docs/guides/AI_MODEL_ROUTING.md`
- `docs/guides/UPGRADE_2_1_TO_2_2.md`

## Workflow

- `workflow/00_SHARED_CONTRACT.md`
- `workflow/01_CAPTURE_REQUIREMENT.md`
- `workflow/02_ACCEPTANCE_AND_OPTIONS.md`
- `workflow/03_DECISION.md`
- `workflow/04_PLAN.md`
- `workflow/05_PLAN_REVIEW.md`
- `workflow/06_CREATE_SLICES.md`
- `workflow/07_EXECUTE_SLICE.md`
- `workflow/08_IMPLEMENTATION_REVIEW.md`
- `workflow/09_CLOSURE.md`
- `workflow/10_RESUME.md`

## Scripts

- `scripts/install.sh`
- `scripts/doctor.sh`
- `scripts/uninstall.sh`
- `scripts/init-project.sh`
- `scripts/adopt-project.sh`
- `scripts/discover-variants.sh` / `scripts/lib/branch_discovery.py` — inventario,
  comparación y contexto por OID para repositorios con variantes
- `tests/test_scripts.py` — regresiones de filesystem y lifecycle
- `tests/test_branch_discovery.py` — fixtures Git anónimos y controles de vigencia

## Skills

- `skills/core/`
- `skills/THIRD_PARTY_CATALOG.md`
- `skills/PROJECT_SKILLS_GUIDE.md`

## Templates

- `templates/`


## Guided Model Routing

- `config/MODEL_CATALOG.md`
- `config/codex-profiles/`
- `docs/guides/AI_MODEL_ROUTING.md`
- `docs/guides/GUIDED_MODEL_GATES.md`
- `docs/guides/CODEX_MODEL_PROFILES.md`
- `docs/guides/UPGRADE_2_2_TO_2_2_1.md`
- `skills/core/model-router/SKILL.md`
- `scripts/configure-model-profiles.sh`

## Mantenimiento

- `docs/guides/GUIDED_DELEGATION.md` — contrato operativo opt-in
- `templates/slice/RUN.schema.json` — schema v1/v2 worker y v3 API, no scheduler
- `scripts/lib/check_execution.py` — validación read-only de registros
- `tests/test_delegation_contract.py` — fixtures y regresiones offline
- `examples/guided-delegation/README.md` — ejemplo sintético y recorridos guiados
- `scripts/lib/audit_workspace.py` — inventario/comparación read-only; no sandbox ni restauración
- `tests/test_supervised_delegation.py` — contrato v2 y compatibilidad v1
- `tests/test_workspace_audit.py` — filesystem temporal, diferencias y límites de snapshots
- `examples/supervised-multiagent/README.md` — ejemplo v2 sintético y comandos reproducibles
- `MANIFEST.json` — manifest único de versión y componentes
- `docs/maintainers/RELEASE_CHECKLIST.md`
- `docs/requirements/` — evidencia de desarrollo, excluida del paquete instalable
- `docs/archive/` — historia excluida de releases, nunca fuente de instrucciones actuales
