---
name: test-strategy
description: Use in AI Software Factory projects when selecting or validating a proportional testing profile for a requirement. Supports T1, T2 and T3 without demanding every test category.
---

# Test Strategy

## T1 — Essential directed

Minimum sufficient evidence for the concrete change.

## T2 — Reinforced

Adds relevant edge cases and affected integrations.

## T3 — High assurance

Adds broader negative/recovery/independent validation where risk justifies it.

Rules:

- risk determines minimum;
- don't add a category without a related risk;
- distinguish required vs optional;
- state what remains unverified;
- never silently upgrade the profile chosen by the user.
