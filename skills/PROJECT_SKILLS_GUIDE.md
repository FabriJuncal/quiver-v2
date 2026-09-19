# Crear skills específicas del proyecto

Una skill local vale la pena cuando captura:

- reglas internas;
- convenciones repetidas;
- procedimientos propios;
- restricciones no obvias.

No crear una skill solo para explicar Angular/PHP/SQL.

## Ejemplos útiles

```text
.agents/skills/
├── project-business-rules/
├── project-api-conventions/
├── project-database-rules/
├── legacy-migration/
└── mobile-release/
```

## `$skill-creator`

Usar `$skill-creator` cuando el procedimiento ya se repitió y merece formalizarse.

Prompt sugerido:

```text
Usá $skill-creator para crear una skill local para este proyecto.

Objetivo:
[describir procedimiento]

La skill debe:
- activarse únicamente cuando corresponda;
- reutilizar documentación del proyecto;
- evitar explicar conocimiento genérico;
- contener referencias separadas si el SKILL.md se vuelve largo;
- no introducir herramientas nuevas.
```
