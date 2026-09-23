# Evidence — v2.3.0-rc.2 preparation

Fecha: 2026-09-23. Plataforma local: macOS, Python 3.14. Preparación inline;
sin agentes, inferencia, credenciales de API, instalación global real ni cambios de
configuración personal. Delegación deshabilitada y piloto NOT RUN.

## Identidad candidata

- Commit probado/exportado: `6048e545253de63827145e7cd5faa2c50342f530`.
- Tree: `4d45c3326f90a44cf3c9976b3d35819b61c38a2a`.
- Rama local: `release/2.3.0-rc.2`.
- Tag remoto `v2.3.0-rc.2`: ausente al verificar con `git ls-remote`.
- Rama remota `release/2.3.0-rc.2`: ausente al verificar con `git ls-remote`.
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
decía que la distribución era 2.2.2. Después del amend:

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
| `ai-software-factory-v2.3.0-rc.2.zip` | 262665 | `9e7da94a9782343d6700d2b43e97b88d72b1cdc34c419be5a3c3e30828d95e2d` |
| `ai-software-factory-v2.3.0-rc.2.bundle` | 393303 | `079e00d5c9bc99ede72cb9ad43eaae5b5d300c0b22c099603d01771a3399c264` |

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
| `python3.14 -B -m unittest discover -s tests -v` dentro del ZIP | **139 tests OK, 33.359 s**. |
| Entradas obligatorias | Manifest/version, catálogo, skill router y notas rc.2 presentes. |
| Permisos | `install.sh`, `asf.sh` y `doctor.sh` conservan ejecutable. |
| Exclusiones | Sin PROJECT_STATE raíz, `docs/requirements` raíz, docs/archive, .git ni .release-candidates; los requirements bajo proyectos de ejemplo se conservan intencionalmente. |
| Hash/manifest | ZIP, bundle y ARTIFACTS.json coherentes con commit final. |

Después de registrar esta evidencia, se generó un segundo `git archive` desde el HEAD
documental y se compararon ambos árboles extraídos con `diff -qr`: sin diferencias.
`6048e545..HEAD` contiene únicamente `PROJECT_STATE.md` y archivos del requirement raíz,
todos excluidos del archive; por eso el artefacto probado sigue representando exactamente
la distribución publicable.

## Cobertura y límites

- RC2-AC1–AC7 satisfechos para preparación local.
- RC2-AC8 satisfecho con self review N2 y límites declarados.
- CI remota macOS/Linux: NOT RUN; requiere push autorizado.
- Review independiente: NOT RUN; self review real, no se afirma independencia.
- GitHub API/release: no verificada con credenciales actuales; Git remoto por SSH sí
  permitió consultas read-only de refs.
- No se midió ahorro de routing ni obediencia interna de modelos.
- RC-F02 sigue abierto: no activar ni anunciar delegación viva.
