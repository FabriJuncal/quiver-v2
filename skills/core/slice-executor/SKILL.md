---
name: slice-executor
description: Use in AI Software Factory projects to implement one approved slice. Keeps scope narrow, activates relevant skills, runs required validation, and records evidence before moving on.
---

# Slice Executor

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
