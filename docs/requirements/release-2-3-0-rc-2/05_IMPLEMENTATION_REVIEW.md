# Implementation review — v2.3.0-rc.2

- Fecha: 2026-09-23.
- Alcance: diff `v2.3.0-rc.1..6048e545253de63827145e7cd5faa2c50342f530`,
  metadata rc.2, routing-v1, tests, ZIP/bundle/hashes y exclusiones.
- Modalidad: self review N2; misma sesión, sin afirmar independencia.
- Veredicto: **APROBADO CON NOTAS para publicación como preview offline**.

## Trazabilidad

- RC2-AC1/2: versión y routing-v1 comprobados por check-release, tests y entradas ZIP.
- RC2-AC3: notas/README/propuesta mantienen delegación deshabilitada y piloto NOT RUN.
- RC2-AC4/5: 139 tests + check-release desde ZIP final; exclusiones y permisos comprobados.
- RC2-AC6: ARTIFACTS, hashes, tree, bundle y commit coherentes.
- RC2-AC7: commit candidato limpio; rama/tag remoto rc.2 ausentes.
- RC2-AC8: evidencia en EVIDENCE.md; CI/review independiente pendientes declarados.

## Hallazgos

- RC2-F01 — OBLIGATORIO, cerrado: texto exportado «local/no publicada» quedaría
  obsoleto después del release y un ejemplo declaraba versión 2.2.2. Se reemplazó por
  estado estable de prerelease/preview y se regeneraron todos los artefactos/hashes.
- RC2-F02 — NOTA: una invocación focalizada de unittest usó nombres incompatibles
  con imports locales. Se registró; discovery correcto pasó 25/25.
- RC2-F03 — NOTA de publicación: CI macOS/Linux y review independiente no ejecutados.
  La rama debe subirse y CI debe pasar antes de tag/release.
- RC-F02 — límite heredado, abierto: impide anunciar/activar multiagente operativo,
  pero no bloquea la preview offline con ayudante deshabilitado.

No quedan hallazgos obligatorios de preparación. Tag objetivo debe apuntar al commit
probado `6048e545...`; el commit posterior de evidencia no debe cambiar ese target.
