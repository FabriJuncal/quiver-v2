# Publish plan — requiere autorización explícita

## Identidad

- Rama a subir: `release/2.3.0-rc.2`.
- Commit candidato/tag target: `6048e545253de63827145e7cd5faa2c50342f530`.
- Tag anotado: `v2.3.0-rc.2`.
- Título: `AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview`.
- Tipo GitHub Release: prerelease.
- Notas: `docs/releases/v2.3.0-rc.2.md` del commit candidato.
- Assets públicos: ZIP y `zip.sha256`. Bundle/ARTIFACTS quedan como evidencia local
  salvo decisión explícita de adjuntarlos.

## Secuencia autorizable

1. Push de rama `release/2.3.0-rc.2` al origin confirmado.
2. Esperar CI macOS/Linux; si falla, detener, diagnosticar y no taggear/publicar.
3. Revisar commit remoto/CI. Integrar a main mediante PR siguiendo el patrón de rc.1.
4. Crear tag anotado `v2.3.0-rc.2` apuntando exactamente a `6048e545...` o, si el
   merge exige otro target, regenerar/probar artefactos antes de cambiarlo. No improvisar.
5. Push del tag y GitHub prerelease con notas/ZIP/SHA verificados.
6. Verificar URL, assets y hashes remotos; actualizar estado de publicación.

La autorización debe cubrir explícitamente operaciones externas. La opción recomendada
es autorizar primero push + PR/CI; tag/release se ejecutan únicamente después del PASS
y de reconciliar el target exacto, sin mover tags existentes.
