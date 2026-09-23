---
name: model-router
description: Use in AI Software Factory projects to select or reassess model and reasoning recommendations. Applies the canonical catalog, switch thresholds and guided gates without assuming the runtime model.
---

# Model Router

## Goal

Recommend the minimum sufficient AI configuration while preserving quality and Guided Mode.

Never choose a model only because it is "better".

## Canonical policy

Apply before planning or implementing a phase. Read
[`config/MODEL_CATALOG.md`](../../../config/MODEL_CATALOG.md) for mappings and
`routing-v1` (Selección proporcional y registro de routing). Do not maintain another
model table here. Reuse a current resolution/decision within its scope.

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
- review needs;
- verifiability: how errors will be detected, cost and limits of that check;
- context sufficiency/freshness and the observed bottleneck.

## Selection

Start from the requirement profile.

Use the catalog's fast path: inherit when scope, risk, evidence and checks remain
covered; reassess only material changes. No extra classifier call or routine user gate.
Keep the brief routing decision (or a valid reference) in existing STATE/brief evidence.
Missing evidence is repaired before dependent work, not manufactured retrospectively.

### Escalation soft

First distinguish environment, missing/stale context, pending product decisions and
analysis failures using the catalog's diagnosis table. Increase reasoning only when
input is sufficient and analysis depth is the issue. Recalculate effort on model change.
Retries require a new hypothesis/evidence or approach and a discriminating check.

### Escalation hard

Use ADVANCED for:

- authorization/security;
- data integrity/loss;
- critical migration;
- material architecture;
- difficult debugging;
- critical review.

### Exceptional

Use Exceptional Override from the catalog only if ADVANCED is insufficient or the task
is extraordinary. Do not force failed attempts through every reasoning level.

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

For opted-in delegation, keep requested profile, resolved configuration and observed
configuration separate per attempt under [Guided Delegation](../../../docs/guides/GUIDED_DELEGATION.md).
Reuse this catalog, not a developer-1/developer-2 mapping. Custom agent configuration
may override spawn intent; missing effective observations remain unknown. Delegation
Benefit does not replace Switch Benefit. Historical observations never set project runtime truth.

Distinguish REQUESTED PROFILE (Factory recommendation) from EFFECTIVE SESSION CONFIG
(model/reasoning actually used, **unknown by default**). Do not introspect or infer runtime
identity from config files, launch intent, project state or your own generated text.

Recommend `asf balanced` (or the resolved profile) for deterministic startup overrides;
see `../../../docs/guides/ASF_LAUNCHER.md`. This does not establish model availability.
Use `../../../docs/guides/SESSION_PREFLIGHT.md` only when configuration materially affects
the next task; normal work continues without interruption. Reuse confirmed configuration
within the same session/phase, never store it as project truth.

Missing required capability/model is a runtime limitation, not a product blocker. Follow
the canonical contract for evidence, pending work and exact resume instructions. A HIGH
Switch Benefit gate with unresolved material need sets user action true; otherwise apply
the Finalization Gate and execute the next authorized action in the same turn.

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

Resolve the critical review recommendation from the catalog; review policy remains in workflow 08.

## Output

For a new/material decision, record in existing STATE/brief (a valid inherited reference
suffices otherwise; follow the catalog's N0/consultation exceptions):

- profile;
- full model name;
- model ID;
- reasoning;
- fallback;
- switch benefit;
- gate required yes/no;
- reason;
- verification and its limits, context sufficient/missing, selection basis policy/measured;
- review mode if relevant.

Keep routine LOW decisions out of user-facing updates. Give the full actionable output
only for a material recommendation/gate; do not narrate routing at every turn.

If gate = no and no other Decision Boundary is pending:
`ACCIÓN DEL USUARIO: ninguna` and continue the authorized work.

If gate = yes:
provide exact Guided Model Gate steps.

Apply the session confirmation, fallback and downgrade rules in [the canonical catalog](../../../config/MODEL_CATALOG.md). Reuse a sufficient confirmed configuration throughout a phase, including consecutive slices. A saved gate recommendation is not proof of an unsatisfied gate. A new session must not infer active configuration from project state.

Keep review scope, evidence and correction limits governed by [workflow 08](../../../workflow/08_IMPLEMENTATION_REVIEW.md), not by model selection alone.
