# Publish plan — requiere autorización explícita

## Identidad

- Rama publicada: `release/2.3.0-rc.2`.
- PR: [#2](https://github.com/FabriJuncal/quiver-v2/pull/2), CI Ubuntu/macOS PASS.
- Commit candidato probado: `b193a39620c4c951ff5fbea2e68c5be49280f19b`.
- Tag target definitivo: merge commit de PR #2, después de regenerar y revalidar.
- Tag anotado: `v2.3.0-rc.2`.
- Título: `AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview`.
- Tipo GitHub Release: prerelease.
- Notas: `docs/releases/v2.3.0-rc.2.md` del commit candidato.
- Assets públicos: ZIP y `zip.sha256`. Bundle/ARTIFACTS quedan como evidencia local
  salvo decisión explícita de adjuntarlos.

## Secuencia autorizable

1. Completado: push de rama, PR #2 y CI macOS/Linux.
2. Con autorización explícita, mergear PR #2 mediante merge commit como rc.1.
3. Actualizar `main`, regenerar ZIP/bundle/manifest desde el merge commit y repetir
   check-release, suite completa, checksums, exclusiones y bundle verify.
4. Si todo pasa, crear tag anotado `v2.3.0-rc.2` apuntando exactamente al merge commit.
5. Push del tag y GitHub prerelease con notas/ZIP/SHA verificados.
6. Verificar URL, assets y hashes remotos; actualizar estado y cerrar el requirement.

La preparación, push, PR y CI ya están completos. La autorización pendiente debe cubrir
merge y publicación. La regeneración/validación posterior al merge es obligatoria y
detiene el flujo ante cualquier fallo; nunca se mueve ni reutiliza un tag existente.
