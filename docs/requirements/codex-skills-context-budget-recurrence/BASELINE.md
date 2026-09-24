# Línea base previa a la reproducción

Fecha: `2026-09-23T18:13:18-0300`.

## Configuración y runtime

- Codex CLI: `0.156.1`.
- `~/.codex/config.toml`: SHA-256
  `a9ade1651f376fa349af4d827061a7cc461b5a41cb45be3f77ebe341d1a93ad0`.
- mtime/ctime: epoch `1790196077` (`2026-09-23 17:41:17 -0300`).
- Tamaño: 13.699 bytes.
- Se observaron múltiples procesos Codex concurrentes; el snapshot filtrado contó
  10 líneas de procesos principales coincidentes.

## Catálogo fuente estimado

| Origen | Entradas activas estimadas | Caracteres de descripción |
| --- | ---: | ---: |
| Plugins | 118 | 32.134 |
| Sistema | 6 | 2.064 |
| Skills personales | 22 | 3.519 |
| AI Software Factory | 10 | 1.805 |
| **Total** | **156** | **39.522** |

El cálculo parte de 187 `SKILL.md` en los roots expuestos y descuenta los 31
overrides de Skills deshabilitadas en `config.toml`. Es un catálogo fuente
estimado; la reproducción debe medir el catálogo realmente expuesto por la CLI.

Comparación histórica: H01 expuso 49 entradas y 10.029 caracteres de descripción.
La presión potencial actual está concentrada en plugins: 118 de 156 entradas y
32.134 de 39.522 caracteres estimados.

## Metadata de plugins

- 19 archivos `.codex-remote-plugin-install.json`.
- Hash del snapshot ordenado de contenido, mtime, ctime, tamaño y ruta:
  `5ebc4760f43e5dd1faa50988fd31c3be79e9784f4de8ac5dd95d964af8926d98`.
- Los 19 archivos tenían mtime/ctime epoch `1790197477` al capturar la línea base.

No se invocó `codex debug prompt-input` antes de completar esta captura.
