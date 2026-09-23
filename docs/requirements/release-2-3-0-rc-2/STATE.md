# Release candidate 2.3.0-rc.2

- **Status:** awaiting-approval
- **Current phase:** PR #2 abierto y CI remota PASS; merge/publicación pendientes
- **Current slice:** none
- **Pending slices:** none
- **Completed:** candidata `b193a396...`; PR #2; ocho jobs Ubuntu/macOS PASS; ZIP final 139 tests OK; check-release/hashes/exclusiones/bundle PASS.
- **Risk level:** N2; preview offline. Activación de delegación sigue fuera de alcance/N3.
- **Acceptance criteria:** approved; 01_ACCEPTANCE_CRITERIA.md
- **Selected option:** rc.2 offline preview; 02_DECISION.md
- **Test profile:** T2 reforzado; 03_PLAN.md
- **Plan version:** 1
- **Plan review:** approved; self review en 04_PLAN_REVIEW.md
- **Human plan approval:** approved — «continua» tras recomendación explícita de preparar rc.2.
- **Execution authorization:** preparación local y push/PR aprobados y completados; no merge/tag/GitHub Release.
- **Next action:** obtener autorización para mergear PR #2 y publicar rc.2 según PUBLISH_PLAN.md.
- **Why this is next:** candidata, artefactos y CI remota están aprobados; restan escrituras externas no autorizadas.
- **User action required:** true
- **Decision required:** autorizar merge y publicación como prerelease offline; no habilita delegación viva.
- **Expected output:** main integrado, artefactos regenerados/probados desde merge commit, tag anotado y GitHub prerelease verificable.
- **After this:** verificar URL/assets/hashes remotos, cerrar requirement y actualizar PROJECT_STATE.
- **Blocked by:** none
- **Runtime limitation:** none para preparación; RC-F02 impide activar/anunciar delegación viva.
- **Runtime limitation detail:** controles efectivos del hijo continúan no verificados; piloto NOT RUN.
- **Resume instruction:** leer EVIDENCE.md, 05_IMPLEMENTATION_REVIEW.md y PUBLISH_PLAN.md. Respuesta exacta para avanzar: `Autorizar merge y publicación de rc.2`.

## AI Strategy

- Planning/implementation: BALANCED / Medium, GPT-5.6 Terra (`gpt-5.6-terra`), fallback GPT-5.6 Sol (`gpt-5.6-sol`) / Medium.
- Review: ADVANCED / High recomendado para publicación material; preparación local usa self review N2 y deja review/CI independiente como limitación declarada.
- Routing decision: `routing-v1`, basis policy. Verificación determinística amplia y artefacto reproducible; contexto suficiente en diff, manifests y release previa. Switch Benefit LOW para preparación actual.
- Effective session config: unknown; no se infiere ni persiste.
