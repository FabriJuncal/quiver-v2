---
name: context-scout
description: Use in AI Software Factory projects before planning or implementing when project context is needed. Retrieves the minimum relevant code/docs instead of reading the whole repository.
---

# Context Scout

## Principle

Context quality > context quantity.

## Process

1. read project/requirement state;
2. identify the decision/action being performed;
3. inspect directly affected files;
4. inspect direct dependencies;
5. inspect existing tests/patterns;
6. expand only when evidence requires it.

Do not dump the entire repository.

Before suggesting more model capacity, check missing contracts/logs, truncated tool
output, contradictory instructions and stale evidence. Recover only what can change
the next decision; report unresolved gaps to model-router. More reasoning cannot
replace missing evidence. Reuse validated findings only while their scope, dependencies
and instructions remain current; do not reuse another session's runtime confirmation.

Prefer existing project patterns over generic redesign.

If a code graph is available, use it only when it reduces exploration.

For explicitly opted-in delegation, build the brief's context manifest under
[Guided Delegation](../../../docs/guides/GUIDED_DELEGATION.md): relevant criteria,
decisions/findings, files/tests, instruction version and base hashes. No full chat
by default, no secrets. Preserve mandatory rules; expand only with a stated need.
For the audited policy, review selected content, not just filenames; a disposable
copy is not access isolation. Keep baselines/evidence outside the worker's authority.
