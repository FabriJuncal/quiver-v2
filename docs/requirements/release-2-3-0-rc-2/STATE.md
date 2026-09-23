# Release candidate 2.3.0-rc.2

- **Status:** in-progress
- **Current phase:** metadata y preparación de candidata
- **Current slice:** RC2-S01
- **Pending slices:** RC2-S01
- **Risk level:** N2; preview offline. Activación de delegación sigue fuera de alcance/N3.
- **Acceptance criteria:** approved; 01_ACCEPTANCE_CRITERIA.md
- **Selected option:** rc.2 offline preview; 02_DECISION.md
- **Test profile:** T2 reforzado; 03_PLAN.md
- **Plan version:** 1
- **Plan review:** approved; self review en 04_PLAN_REVIEW.md
- **Human plan approval:** approved — «continua» tras recomendación explícita de preparar rc.2.
- **Execution authorization:** approved para preparación local; no push/tag/GitHub Release.
- **Next action:** completar metadata rc.2, validar y crear commit limpio de candidata.
- **Why this is next:** rc.1 ya está taggeada; routing-v1 está cerrado y debe entrar en un identificador nuevo.
- **User action required:** false
- **Decision required:** none durante preparación; publicación será boundary final.
- **Expected output:** commit, ZIP, SHA-256, ARTIFACTS.json y evidencia verificable.
- **After this:** revisión final y solicitud concreta de autorización para publicar rc.2.
- **Blocked by:** none
- **Runtime limitation:** none para preparación; RC-F02 impide activar/anunciar delegación viva.
- **Runtime limitation detail:** controles efectivos del hijo continúan no verificados; piloto NOT RUN.
- **Resume instruction:** leer este STATE y 03_PLAN.md; completar desde Next action. No crear tag, push ni release sin autorización final.

## AI Strategy

- Planning/implementation: BALANCED / Medium, GPT-5.6 Terra (`gpt-5.6-terra`), fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- Review: ADVANCED / High recomendado para publicación material; preparación local usa self review N2 y deja review/CI independiente como limitación declarada.
- Routing decision: `routing-v1`, basis policy. Verificación determinística amplia y artefacto reproducible; contexto suficiente en diff, manifests y release previa. Switch Benefit LOW para preparación actual.
- Effective session config: unknown; no se infiere ni persiste.
