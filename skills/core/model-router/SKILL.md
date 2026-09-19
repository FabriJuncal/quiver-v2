---
name: model-router
description: Use in AI Software Factory projects to select or reassess model and reasoning recommendations. Applies the canonical catalog, switch thresholds and guided gates without assuming the runtime model.
---

# Model Router

## Goal

Recommend the minimum sufficient AI configuration while preserving quality and Guided Mode.

Never choose a model only because it is "better".

## Canonical mapping

- ECONOMICAL → GPT-5.6 Luna (`gpt-5.6-luna`) / Low
- BALANCED → GPT-5.6 Terra (`gpt-5.6-terra`) / Medium
- ADVANCED → GPT-5.6 Sol (`gpt-5.6-sol`) / High
- Exceptional Override → GPT-6 Astra (`gpt-6-astra`) / High or XHigh

Read `config/MODEL_CATALOG.md` when resolving exact current recommendations.

## Inputs

Consider:

- risk level;
- uncertainty;
- reversibility;
- task type;
- security/auth/data impact;
- debugging evidence;
- amount of remaining work;
- current phase;
- review needs.

## Selection

Start from the requirement profile.

Then refine per slice.

### Escalation soft

If extra depth is useful but the current model family is adequate:

increase reasoning before changing model.

### Escalation hard

Use ADVANCED for:

- authorization/security;
- data integrity/loss;
- critical migration;
- material architecture;
- difficult debugging;
- critical review.

### Exceptional

Recommend GPT-6 Astra only if ADVANCED is insufficient or the task is extraordinary.

## Switch Benefit

Classify:

- LOW
- MEDIUM
- HIGH

Only produce an AI Model Gate for HIGH when sufficient configuration is not yet confirmed for this phase/session. Mandatory risk escalation counts as HIGH; a separate review requirement is not a reason to switch the main chat model.

## Downgrade

Do not interrupt for short cleanup.

Downgrade only at meaningful phase boundaries when substantial mechanical work remains.

## Runtime model

Never infer the active model as project truth.

If a gate requires verification:

guide the user:

1. `/status` if unsure;
2. `/model` if change needed;
3. exact full model name;
4. exact ID;
5. reasoning;
6. fallback;
7. tell user to write `continuar`.

## Review

- N0 self verification
- N1 self review
- N2 dedicated `/review` when material
- N3 dedicated review required when technically possible; otherwise require an explicitly approved alternative before closure

For critical review recommend GPT-5.6 Sol (`gpt-5.6-sol`).

## Output

Return:

- profile;
- full model name;
- model ID;
- reasoning;
- fallback;
- switch benefit;
- gate required yes/no;
- reason;
- review mode if relevant.

If gate = no and no other Decision Boundary is pending:
`ACCIÓN DEL USUARIO: ninguna` and continue the authorized work.

If gate = yes:
provide exact Guided Model Gate steps.

Apply the session confirmation, fallback and downgrade rules in [the canonical catalog](../../../config/MODEL_CATALOG.md). Reuse a sufficient confirmed configuration throughout a phase, including consecutive slices. A saved gate recommendation is not proof of an unsatisfied gate. A new session must not infer active configuration from project state.

Keep review scope, evidence and correction limits governed by [workflow 08](../../../workflow/08_IMPLEMENTATION_REVIEW.md), not by model selection alone.
