# Evidence — v2.3.0-rc.2 preparation

Fecha: 2026-09-23. Plataforma local: macOS, Python 3.14. Preparación inline;
sin agentes, inferencia, credenciales de API, instalación global real ni cambios de
configuración personal. Delegación deshabilitada y piloto NOT RUN.

## Identidad publicada

- Commit merge probado, exportado y taggeado: `930f67b7c05761edaa59b702320d31535a64c639`.
- Tree: `97a46973eee7fd6231e1eddd445c7f31b60d27cd`.
- Candidato previo al merge: `b193a39620c4c951ff5fbea2e68c5be49280f19b`.
- Rama de preparación: `release/2.3.0-rc.2`.
- PR: [#2](https://github.com/FabriJuncal/quiver-v2/pull/2), MERGED.
- Tag remoto anotado: `v2.3.0-rc.2`; objeto tag `14a271dbe9a07840e9f1ee790c5d5d0c21bfd35e`, dereference al merge commit.
- Release: [AI Software Factory v2.3.0-rc.2](https://github.com/FabriJuncal/quiver-v2/releases/tag/v2.3.0-rc.2), prerelease pública.
- `v2.3.0-rc.1` permanece intacta y no se reutiliza.

## Verificación de fuente

| Comprobación | Resultado |
|---|---|
| `python3.14 -B -m unittest discover -s tests -v` antes del commit candidato | 139 tests OK, 57.871 s. |
| `bash scripts/check-release.sh` sobre commit candidato | PASS. |
| `scripts/install.sh --dry-run` | PASS; sin escrituras, destino/configuración informados. |
| `scripts/configure-model-profiles.sh --dry-run` | PASS; cuatro perfiles, sin escrituras. |
| `git diff --check` | PASS. |
| Escaneo dirigido de rutas personales/claves privadas/tokens fuera de requirements/archive | Sin coincidencias. No equivale a secret scanner exhaustivo. |

Durante review se eliminó estado transitorio «local/no publicada» de archivos exportados
y se reemplazó por prerelease/preview offline. También se corrigió un ejemplo que aún
decía que la distribución era 2.2.2. Al observar CI se detectó además que el nombre
visible del workflow seguía fijado a rc.1; se cambió por `Factory Release Validation`
para evitar metadata obsoleta en candidatas futuras. Después de esas correcciones:

| Comprobación | Resultado |
|---|---|
| `test_release_candidate.py` por discovery | 6 tests OK, 3.739 s. |
| `test_supervised_delegation.py` por discovery | 19 tests OK, 3.262 s. |
| `check-release.sh` | PASS. |

Un intento previo de invocar esos dos módulos como nombres `tests/...py` produjo dos
ImportError porque sus imports esperan discovery con `-s tests`; no ejecutó tests ni
indicó un defecto de producto. Se repitió con la forma correcta y pasó 25/25.

## Artefactos finales

Directorio local ignorado por Git: `.release-candidates/2.3.0-rc.2/`.

| Archivo | Bytes | SHA-256 |
|---|---:|---|
| `ai-software-factory-v2.3.0-rc.2.zip` | 262652 | `cd30e9f4c84ebe34046358c40828091ecb88a06919416a4df29caa025d756f13` |
| `ai-software-factory-v2.3.0-rc.2.bundle` | 404795 | `b5ecc03a9d2bc1eb108356f86c83ed5cd33bd500f4c1341367d90bc480a99117` |

`ARTIFACTS.json` enlaza versión, commit, tree, tamaños, hashes y estado
`publication_authorized=true`, `delegation=disabled`, `pilot=NOT RUN`.
Los dos `.sha256` pasaron `shasum -a 256 -c`; el bundle pasó `git bundle verify`
y contiene historia completa con la referencia `main` publicada.

## Verificación del ZIP final

ZIP generado con `git archive` desde el commit exacto y prefijo
`ai-software-factory-v2.3.0-rc.2/`. Extraído en directorio temporal:

| Comprobación | Resultado |
|---|---|
| `bash scripts/check-release.sh` dentro del ZIP | PASS. |
| `python3.14 -B -m unittest discover -s tests -v` dentro del ZIP final | **139 tests OK, 24.706 s**. |
| `scripts/install.sh --dry-run` dentro del ZIP final | PASS. |
| `scripts/configure-model-profiles.sh --dry-run` dentro del ZIP final | PASS. |
| Entradas obligatorias | Manifest/version, catálogo, skill router y notas rc.2 presentes. |
| Permisos | `install.sh`, `asf.sh` y `doctor.sh` conservan ejecutable. |
| Exclusiones | Sin PROJECT_STATE raíz, `docs/requirements` raíz, docs/archive, .git ni .release-candidates; los requirements bajo proyectos de ejemplo se conservan intencionalmente. |
| Hash/manifest | ZIP, bundle y ARTIFACTS.json coherentes con commit final. |

El ZIP final fue regenerado después del merge desde el commit exacto del tag. El checksum
público usa solo el nombre del archivo, por lo que funciona en el directorio de descarga.

## CI remota

Commit `b193a396...`, ocho jobs exitosos entre eventos push y pull_request:

- Validate push: [run 35865739220](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865739220).
- Factory Release Validation push: [run 35865739242](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865739242).
- Validate PR: [run 35865746105](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865746105).
- Factory Release Validation PR: [run 35865746120](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865746120).

Cada workflow pasó en `ubuntu-latest` y `macos-latest`.

El merge commit `930f67b7...` también pasó ambos workflows en `main`:

- Validate: [run 35867124857](https://github.com/FabriJuncal/quiver-v2/actions/runs/35867124857).
- Factory Release Validation: [run 35867124791](https://github.com/FabriJuncal/quiver-v2/actions/runs/35867124791).

## Verificación remota de publicación

- GitHub reportó la release como `isDraft=false`, `isPrerelease=true`.
- Assets públicos: ZIP de 262652 bytes y checksum de 102 bytes, ambos `uploaded`.
- GitHub informó digest del ZIP `sha256:cd30e9f4...`.
- Se descargaron ZIP y checksum desde la release; `shasum -a 256 -c` pasó.
- `cmp` confirmó igualdad byte a byte entre ZIP remoto y artefacto local.
- `git ls-remote` confirmó tag anotado y dereference a `930f67b7...`.

## Cobertura y límites

- RC2-AC1–AC7 satisfechos para preparación, integración y publicación.
- RC2-AC8 satisfecho con self review N2 y límites declarados.
- CI remota macOS/Linux: PASS para candidato, PR y merge commit en `main`.
- Review independiente: NOT RUN; self review real, no se afirma independencia.
- GitHub API, tag, prerelease, assets y descarga remota verificados.
- No se midió ahorro de routing ni obediencia interna de modelos.
- RC-F02 sigue abierto: no activar ni anunciar delegación viva.
