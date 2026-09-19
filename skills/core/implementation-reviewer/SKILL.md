---
name: implementation-reviewer
description: Use in AI Software Factory projects after implementation to review the actual diff, tests and evidence against the approved requirement and plan.
---

# Implementation Reviewer

Inputs:

- requirement;
- criteria;
- decision;
- approved plan;
- real diff;
- executed tests;
- closure evidence.

Check:

- correctness;
- scope;
- acceptance criteria;
- plausible regressions;
- required validation;
- deviations.

Do not reopen approved design decisions without new evidence.

Verdicts:

- APROBADO
- APROBADO CON NOTAS
- REQUIERE AJUSTES

Aplicar [workflow 08](../../../workflow/08_IMPLEMENTATION_REVIEW.md): alcance real incluyendo commits, evidencia identificada, N3 dedicado o alternativa aprobada y una sola ronda de correcciones antes de escalar obligatorios pendientes. Opcionales no bloquean. `continuar con review` no sustituye los resultados reales.
