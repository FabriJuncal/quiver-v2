# Upgrade 2.2.0 → 2.2.1

Guía histórica de esa transición. Para llegar a la versión actual, aplicar después
[2.2.1 → 2.2.2](UPGRADE_2_2_1_TO_2_2_2.md) sin perder metadata ni estados existentes.

La versión 2.2.1 corrige y completa AI Model Routing.

## Cambios

- nombres completos de modelos;
- AI Model Gates;
- Switch Benefit;
- Switch Threshold;
- reasoning separado;
- fallbacks;
- review dedicado;
- model-router skill;
- perfiles opcionales de Codex.

## Actualizar Factory

Reemplazar con la versión nueva y ejecutar:

```bash
./scripts/install.sh
./scripts/doctor.sh
```

Opcional:

```bash
./scripts/configure-model-profiles.sh
```

## Proyecto ya existente

En Codex:

```text
Actualizá únicamente la metadata de AI Software Factory de este proyecto para Guided Model Routing 2.2.1.

No modifiques código ni decisiones aprobadas.

1. Actualizá PROJECT_PROFILE.md AI Policy:
   - default GPT-5.6 Terra (gpt-5.6-terra) / Medium
   - switch threshold HIGH
   - downgrade phase-boundary-only
   - critical review GPT-5.6 Sol (gpt-5.6-sol)

2. Actualizá AI Strategy de requirements activos con:
   - modelo completo + ID + reasoning
   - fallback
   - dedicated review policy
   - Switch Benefit

3. Actualizá EXECUTION_BRIEF de slices pendientes con:
   - Preferred model full name
   - Model ID
   - Reasoning
   - fallback
   - Switch Benefit
   - Model Gate required
   - catalog date

No agregues current model al estado persistente.

Después continuá hasta el próximo Decision Boundary.
```

No reescribir slices cerradas solo por metadata histórica.
