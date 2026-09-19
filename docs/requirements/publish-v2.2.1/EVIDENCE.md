# Evidencia de publicación v2.2.1

Fecha: 2026-09-19.

## Resultado externo verificado

- Repositorio: https://github.com/FabriJuncal/quiver-v2 — visibilidad **PRIVATE** preservada.
- Usuario autenticado por gh y SSH: `FabriJuncal`.
- Transporte Git: alias `github-personal` configurado con la identidad solicitada; sin cambiar configuración personal ni force-push.
- Revisión publicada: `db1eb677c6b067751fbe66cb013fea0a79ebe688`.
- Tag anotado: `v2.2.1`; objeto `e1c106e5334efa64c6cac987f85aef52f297d614`, resuelto remotamente a esa revisión.
- [Release publicada](https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.2.1): `isDraft=false`, `isPrerelease=false`, publicación `2026-09-19T21:04:14Z`.
- Adjuntos: `ai-software-factory-v2.2.1.zip` (131820 bytes) y `ai-software-factory-v2.2.1.sha256`.
- SHA-256 del ZIP: `7153759f8c5ec9b989dba6c6ccd81c099e75d148e3941025969bfbbb966ad54d`.

## Verificaciones ejecutadas

| Verificación | Resultado |
|---|---|
| `gh auth status`, `ssh -o BatchMode=yes -T git@github-personal` | Ambas identidades FabriJuncal. SSH retorna 1 porque GitHub no ofrece shell, junto con autenticación exitosa. |
| `git fetch origin`, consulta de main y releases | Base remota `2c72d1c`, sin divergencia ni release/tag previos. |
| Inventario del diff y búsqueda dirigida de credenciales/rutas personales en archivos activos | 126 archivos de la versión/reorganización de Factory; sin coincidencias del scan. No es garantía de ausencia de todo secreto posible. |
| `git diff --cached --check` | Exit 0 antes del commit. |
| `python3 -B -m unittest discover -s tests -v` con Python 3.14 local | 22 tests OK. |
| `git archive --format=zip --prefix=ai-software-factory-v2.2.1/` sobre db1eb67; extracción y misma suite | 22 tests OK sobre el contenido exportado, sin depender de archivos untracked; ZIP histórico excluido. |
| `git push origin main` | Fast-forward `2c72d1c..db1eb67`, sin force. |
| [Validate de la revisión publicada](https://github.com/FabriJuncal/quiver-v2/actions/runs/35469237298) | Success: Ubuntu y macOS, sintaxis, recursos requeridos y 22 tests en cada job. |
| `git push origin refs/tags/v2.2.1` | Nuevo tag publicado sin reemplazar otros. |
| `gh release create ... --verify-tag` | Release publicada y dos adjuntos subidos. |
| `gh release view`, `git ls-remote` | Release no draft, assets uploaded, tag resuelve al commit probado. |
| `gh release download`, `shasum -a 256 -c`, `cmp` contra el ZIP original | Checksum OK; archivo descargado idéntico byte por byte. |

Se verificó una instalación real en fixtures desde el paquete, no se instaló Factory en el HOME personal. No hubo inferencia paga ni review independiente remoto. Las limitaciones de la auditoría sobre disponibilidad efectiva por cuenta/reasoning siguen vigentes.

Este cierre documental se registra en un commit posterior: `main` puede avanzar sin modificar el tag ni los adjuntos de v2.2.1. El artefacto y su checksum corresponden exclusivamente a `db1eb67`.
