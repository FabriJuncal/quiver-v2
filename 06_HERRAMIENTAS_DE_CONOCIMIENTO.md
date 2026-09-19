# Obsidian, Graphify y Codebase Memory

## Obsidian

Recomendado como interfaz humana opcional sobre `docs/`.

No duplicar documentos en un vault aparte. Abrir la carpeta del repo como vault o sub-vault.

Git sigue siendo la fuente de verdad.

## Graphify

Usar bajo demanda para discovery de proyectos desconocidos, especialmente cuando ayuda visualizar relaciones de código y documentación.

No es obligatorio en proyectos pequeños o nuevos.

## Codebase Memory MCP

Usar como infraestructura persistente de code intelligence cuando el proyecto sea grande, legacy, monorepo, polyglot o multi-repo y la exploración repetida sea costosa.

## No usar ambos por defecto

Configurar un solo proveedor de code intelligence:

```yaml
code_intelligence:
  provider: none | graphify | codebase-memory
```

## Regla

- Proyecto pequeño/nuevo → ninguno.
- Proyecto desconocido → Graphify opcional.
- Proyecto grande frecuente → probar Codebase Memory.
- Medir antes de estandarizar.
