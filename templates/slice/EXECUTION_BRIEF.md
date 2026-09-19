# Execution Brief

## AI Execution Profile

> Recomendación para esta slice. No representa el modelo activo real de la sesión.

Heredar AI Strategy del STATE del requirement. Si no hay excepción relevante, reemplazar los campos repetidos por `Inherit: STATE.md → AI Strategy / Implementation default`. Un gate recomendado debe reevaluarse contra la confirmación de fase en la sesión actual.

- **Profile:** ECONOMICAL | BALANCED | ADVANCED
- **Preferred model full name:**
- **Model ID:**
- **Reasoning:** low | medium | high | xhigh
- **Fallback full name:**
- **Fallback model ID:**
- **Fallback reasoning:**
- **Switch benefit:** LOW | MEDIUM | HIGH
- **Model Gate required:** yes | no
- **Why:**
- **Escalate if:**
- **Downgrade after:**
- **Resolved against catalog date:**

### Guided behavior

If `Model Gate required: yes`, check whether this session already confirmed sufficient configuration for the phase. Do not start critical implementation until that need is satisfied; do not repeat a satisfied gate.

If `Model Gate required: no`, do not interrupt the user just to optimize the model.

Neither value overrides other pending boundaries or grants implementation authorization.

## Objective

-

## Ordered steps

1.

## Constraints

-

## Required tests

-

## Definition of done

-
