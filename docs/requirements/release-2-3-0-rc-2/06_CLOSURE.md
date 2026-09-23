# Release closure

La preparación, integración y publicación de v2.3.0-rc.2 están completas. El tag anotado
apunta al merge commit `930f67b7...`; ZIP, checksum, bundle y manifest son coherentes.
El ZIP final pasó 139 tests, check-release y dry-runs; CI de `main` pasó en Ubuntu/macOS.
RC2-F01 y RC2-F04 fueron corregidos antes del artefacto final.

PR #2 fue integrado y la prerelease está disponible en:
https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.3.0-rc.2

Los assets remotos se descargaron y verificaron contra el hash local. Requirement
cerrado. RC-F02 sigue impidiendo activar/anunciar delegación viva y queda fuera de
esta preview offline.
