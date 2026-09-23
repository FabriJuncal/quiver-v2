# Release candidate 2.3.0-rc.2

- **Status:** awaiting-approval
- **Current phase:** candidata local validada; publicación externa pendiente
- **Current slice:** none
- **Pending slices:** none
- **Completed:** preparación rc.2; commit `6048e545...`; ZIP final 139 tests OK; check-release/hashes/exclusiones/bundle PASS.
- **Risk level:** N2; preview offline. Activación de delegación sigue fuera de alcance/N3.
- **Acceptance criteria:** approved; 01_ACCEPTANCE_CRITERIA.md
- **Selected option:** rc.2 offline preview; 02_DECISION.md
- **Test profile:** T2 reforzado; 03_PLAN.md
- **Plan version:** 1
- **Plan review:** approved; self review en 04_PLAN_REVIEW.md
- **Human plan approval:** approved — «continua» tras recomendación explícita de preparar rc.2.
- **Execution authorization:** approved para preparación local; no push/tag/GitHub Release.
- **Next action:** obtener autorización para push de rama + PR/CI según PUBLISH_PLAN.md.
- **Why this is next:** candidata y artefactos están completos; CI remota requiere una escritura externa autorizada.
- **User action required:** true
- **Decision required:** autorizar push de rama y creación de PR para ejecutar CI; tag/release solo después de PASS y target reconciliado.
- **Expected output:** rama/PR remotos y CI macOS/Linux observable, sin tag ni release prematuros.
- **After this:** si CI pasa, presentar target final y ejecutar publicación solo bajo la autorización aplicable; si falla, diagnosticar/corregir/regenerar.
- **Blocked by:** none
- **Runtime limitation:** none para preparación; RC-F02 impide activar/anunciar delegación viva.
- **Runtime limitation detail:** controles efectivos del hijo continúan no verificados; piloto NOT RUN.
- **Resume instruction:** leer EVIDENCE.md, 05_IMPLEMENTATION_REVIEW.md y PUBLISH_PLAN.md. Respuesta exacta para avanzar: `Autorizar push y PR de rc.2`. No crear tag/release antes del CI PASS y target reconciliado.

## AI Strategy

- Planning/implementation: BALANCED / Medium, GPT-5.6 Terra (`gpt-5.6-terra`), fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- Review: ADVANCED / High recomendado para publicación material; preparación local usa self review N2 y deja review/CI independiente como limitación declarada.
- Routing decision: `routing-v1`, basis policy. Verificación determinística amplia y artefacto reproducible; contexto suficiente en diff, manifests y release previa. Switch Benefit LOW para preparación actual.
- Effective session config: unknown; no se infiere ni persiste.
