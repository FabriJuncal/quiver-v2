# Evidence — v2.3.0-rc.2 preparation

Fecha: 2026-09-23. Plataforma local: macOS, Python 3.14. Preparación inline;
sin agentes, inferencia, credenciales de API, instalación global real ni cambios de
configuración personal. Delegación deshabilitada y piloto NOT RUN.

## Identidad candidata

- Commit probado/exportado: `b193a39620c4c951ff5fbea2e68c5be49280f19b`.
- Tree: `d071a322527b414572164ad895714897da2a21af`.
- Rama local: `release/2.3.0-rc.2`.
- Rama remota: `origin/release/2.3.0-rc.2` en el mismo commit candidato.
- PR: [#2](https://github.com/FabriJuncal/quiver-v2/pull/2), abierto contra `main` y mergeable.
- Tag remoto `v2.3.0-rc.2`: ausente al verificar con `git ls-remote`.
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
| `ai-software-factory-v2.3.0-rc.2.zip` | 262652 | `16f7e2ec329b31e3d9ff02ea7c3c7ee653fb4470be4cfe32127a747f469b7f28` |
| `ai-software-factory-v2.3.0-rc.2.bundle` | 399955 | `6198193ee4ec2749df8d983c102df39ed96fc2b094a82bc372b806355856e16c` |

`ARTIFACTS.json` enlaza versión, commit, tree, tamaños, hashes y estado
`publication_authorized=false`, `delegation=disabled`, `pilot=NOT RUN`.
Los dos `.sha256` pasaron `shasum -a 256 -c`; el bundle pasó `git bundle verify`
y contiene historia completa con la rama candidata.

## Verificación del ZIP final

ZIP generado con `git archive` desde el commit exacto y prefijo
`ai-software-factory-v2.3.0-rc.2/`. Extraído en directorio temporal:

| Comprobación | Resultado |
|---|---|
| `bash scripts/check-release.sh` dentro del ZIP | PASS. |
| `python3.14 -B -m unittest discover -s tests -v` dentro del ZIP | **139 tests OK, 25.975 s**. |
| Entradas obligatorias | Manifest/version, catálogo, skill router y notas rc.2 presentes. |
| Permisos | `install.sh`, `asf.sh` y `doctor.sh` conservan ejecutable. |
| Exclusiones | Sin PROJECT_STATE raíz, `docs/requirements` raíz, docs/archive, .git ni .release-candidates; los requirements bajo proyectos de ejemplo se conservan intencionalmente. |
| Hash/manifest | ZIP, bundle y ARTIFACTS.json coherentes con commit final. |

Después de registrar esta evidencia se vuelve a comparar el archive del HEAD documental
con el candidato. Sus diferencias posteriores deben limitarse a `PROJECT_STATE.md` y al
requirement raíz, ambos excluidos del archive; cualquier diferencia exportable invalida
el artefacto y obliga a regenerar.

## CI remota

Commit `b193a396...`, ocho jobs exitosos entre eventos push y pull_request:

- Validate push: [run 35865739220](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865739220).
- Factory Release Validation push: [run 35865739242](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865739242).
- Validate PR: [run 35865746105](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865746105).
- Factory Release Validation PR: [run 35865746120](https://github.com/FabriJuncal/quiver-v2/actions/runs/35865746120).

Cada workflow pasó en `ubuntu-latest` y `macos-latest`.

## Cobertura y límites

- RC2-AC1–AC7 satisfechos para preparación local.
- RC2-AC8 satisfecho con self review N2 y límites declarados.
- CI remota macOS/Linux: PASS para push y PR en el commit candidato.
- Review independiente: NOT RUN; self review real, no se afirma independencia.
- GitHub API y permisos de PR verificados. Tag y GitHub Release todavía no creados.
- No se midió ahorro de routing ni obediencia interna de modelos.
- RC-F02 sigue abierto: no activar ni anunciar delegación viva.
