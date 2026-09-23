# Obsidian, Graphify y Codebase Memory

## Fuente de verdad

Siempre:

```text
Git + Markdown del repositorio
```

## Obsidian

Recomendado como interfaz humana opcional.

Puede abrir directamente `docs/`.

No crear una segunda copia de la documentación.

## Graphify

Útil para:

- discovery de un proyecto desconocido;
- visualizar código/docs;
- mapas bajo demanda.

No requerido en proyectos nuevos o pequeños.

## Codebase Memory MCP

Útil para:

- monorepos;
- legacy grande;
- polyglot;
- trabajo continuo;
- impacto/call graph;
- cross-repo.

No requerido para todos los repos.

## Regla

Elegir:

```text
none | graphify | codebase-memory
```

No activar Graphify + Codebase Memory por defecto.

Para repositorios con variantes por rama, empezar con el lector Git determinista de
[Branch-aware discovery](BRANCH_AWARE_DISCOVERY.md). Solo evaluar un índice estructural
si consultas medidas siguen sin resolverse. El índice debe aislar snapshots por OID y
no reemplaza confirmación de cliente, deployment o comportamiento runtime.
