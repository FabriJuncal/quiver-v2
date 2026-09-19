---
name: impact-analysis
description: Use in AI Software Factory projects when a change may affect shared behavior, APIs, data, multiple modules, or legacy consumers. Maps realistic dependencies and blast radius proportionally.
---

# Impact Analysis

Determine:

- direct component;
- callers/consumers;
- contracts;
- shared state;
- persistence;
- tests;
- legacy consumers;
- deployment implications.

For trivial changes, keep this minimal.

For high-risk changes, expand to data/security/integrations.

Do not invent hypothetical dependencies.

Output only impact that can change the plan or validation strategy.
