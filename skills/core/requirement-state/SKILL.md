---
name: requirement-state
description: Use in projects using AI Software Factory when a requirement changes phase or work resumes. Keeps project and requirement state actionable.
---

# Requirement State

Only the coordinator/inline executor writes central state. A delegated worker returns
evidence/proposals and never activates other slices. Follow the opt-in contract in
[Guided Delegation](../../../docs/guides/GUIDED_DELEGATION.md) when applicable.
Audited incidents reject delivery, not user changes: preserve evidence and reconcile
before integration. Unknown stop keeps capacity occupied; never restore the original automatically.

Every active state must answer:

1. where are we?
2. what completed?
3. what is in progress?
4. what exactly is next?
5. does it need the user?
6. what output will it create?
7. what happens after?

Required fields:

- Next action
- Why this is next
- User action required
- Decision required
- Expected output
- After this
- Blocked by
- Resume instruction
- Runtime limitation (none by default; type/evidence/pending/resume when present)

Never write:

`Next action: decide what to do`

when a concrete step can be derived.

Guided Mode:
if user action is false, continue until the next Decision Boundary.

Before any final response apply the canonical **Finalization Gate** and all four
**State Consistency Invariants** in `../../../workflow/00_SHARED_CONTRACT.md`.
An active slice requires a concrete Next action. Read persisted STATE before recap;
record contradictions and ignore recap. Never finish with user action false and executable
approved work. Record real runtime limitations separately from product blockers.

## AI Strategy

Cuando el requirement ya fue comprendido, mantener también:

- planning profile/reasoning;
- implementation default profile/reasoning;
- review profile/reasoning;
- escalation triggers;
- downgrade opportunities.

Los perfiles se resuelven a modelos concretos mediante el catálogo central.


## Boundaries y reanudación

Cuando cambie de fase o se reanude:

- mantener perfiles recomendados;
- no persistir el modelo activo;
- mantener dedicated review policy;
- mantener Switch Benefit cuando sea relevante.

`User action required: true` si existe cualquier boundary pendiente: criterios, plan, ejecución no autorizada, testing material, alcance, costo, acción irreversible, review, Model Gate o bloqueo real.

Solo usar false cuando ninguno impide la próxima acción autorizada. La ausencia de Model Gate nunca elimina otros gates. Persistir aprobación humana del plan y autorización de ejecución por separado, con versión/alcance y referencia. Respetar aprobaciones ya otorgadas.

Contrastar estado con diff/evidencia ante interrupciones. Al cerrar, actualizar requirement activo del proyecto y continuar el siguiente trabajo ya autorizado. Consultar workflow/10_RESUME.md para conflictos y sesiones nuevas.
