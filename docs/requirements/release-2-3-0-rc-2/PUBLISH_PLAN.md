# Publish record — completado

## Identidad

- Rama publicada: `release/2.3.0-rc.2`.
- PR: [#2](https://github.com/FabriJuncal/quiver-v2/pull/2), MERGED; CI Ubuntu/macOS PASS.
- Commit candidato probado: `b193a39620c4c951ff5fbea2e68c5be49280f19b`.
- Tag target definitivo: `930f67b7c05761edaa59b702320d31535a64c639`.
- Tag anotado: `v2.3.0-rc.2`.
- Título: `AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview`.
- Tipo GitHub Release: prerelease.
- Notas: `docs/releases/v2.3.0-rc.2.md` del commit candidato.
- Assets públicos: ZIP y `zip.sha256`. Bundle/ARTIFACTS quedan como evidencia local
  salvo decisión explícita de adjuntarlos.
- Release: https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.3.0-rc.2

## Secuencia autorizable

1. Completado: push de rama, PR #2 y CI macOS/Linux.
2. Completado: merge commit de PR #2.
3. Completado: ZIP/bundle/manifest regenerados desde el merge; check-release, suite
   completa, dry-runs, checksums, exclusiones y bundle verify PASS.
4. Completado: tag anotado `v2.3.0-rc.2` en el merge commit.
5. Completado: GitHub prerelease con notas, ZIP y SHA.
6. Completado: URL, assets, descarga y hashes remotos verificados.

Publicación completada bajo autorización explícita. No mover ni reutilizar el tag.
