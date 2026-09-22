---
name: slice-executor
description: Use in AI Software Factory projects to implement one approved slice. Keeps scope narrow, activates relevant skills, runs required validation, and records evidence before moving on.
---

# Slice Executor

First identify role. The steps below apply to the coordinator/inline executor.
A delegated worker must instead obey its bounded read-only/proposal brief: return
findings/patch proposal and actual evidence; do not apply edits, update STATE, run
mutating tests, continue slices or spawn workers. Reading this skill grants no delegation.
For explicit opt-in use [Guided Delegation](../../../docs/guides/GUIDED_DELEGATION.md).
Read-only intent in the audited policy is not enforcement. The coordinator checks
copy/original manifests and rejects incidents without restoring user work; a clean
comparison never proves permissions or absence of transient/external actions.

Before coding:

1. read project state;
2. read requirement state;
3. read slice EXECUTION_BRIEF;
4. read AI Execution Profile;
5. load minimum context;
6. confirm approved testing.

Apply `../../../workflow/07_EXECUTE_SLICE.md`: verify human plan approval and execution authorization for the current scope/version. Resolve all pending boundaries, not just Model Gates. Inherit strategy from STATE unless this slice needs a material exception; do not repeat a configuration gate already satisfied in this session/phase.

Use the concrete model mapping from the central catalog when available.
Do not claim a model switch unless the runtime actually supports/performs it.

Implement only slice scope.

No opportunistic refactors.

Run required validation.

Record evidence in `CLOSURE_BRIEF.md`.

Update requirement state.

If next approved slice has no Decision Boundary, continue.

Apply the **Finalization Gate** and **State Consistency Invariants** in
`../../../workflow/00_SHARED_CONTRACT.md` before responding finally: completing S04 while
S05 is active requires executing S05 in the same turn when authorized and feasible.
`ACCIÓN DEL USUARIO: ninguna` signals execution, never closure. Real runtime limitations
must preserve pending work and exact resume steps; recap cannot override STATE.
