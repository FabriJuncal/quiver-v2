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

Prefer existing project patterns over generic redesign.

If a code graph is available, use it only when it reduces exploration.
