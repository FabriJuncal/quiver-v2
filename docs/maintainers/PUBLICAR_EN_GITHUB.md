# Publicar en GitHub

## Antes de publicar

Confirmar con el mantenedor el repositorio destino; `git remote -v` muestra la configuración local pero no prueba que sea la publicación correcta. No cambiar remotes ni publicar sin autorización. README y Quick Start permiten instalar desde una carpeta obtenida del repositorio/release confirmado.

## Inicializar

```bash
git status --short
git diff --stat
```

Revisar los archivos exactos a incluir antes de crear un commit. No commitear automáticamente cambios ajenos. Seguir RELEASE_CHECKLIST.md y verificar desde un checkout limpio de la revisión elegida.

## Recomendación

No marcar este repo como Template Repository.

AI Software Factory se instala una vez.

Un futuro starter de SaaS sí puede ser un GitHub Template separado.

## Release

Preparar una candidata no autoriza por sí mismo push, tags ni publicación. Target de esta guía:

```text
v2.3.0-rc.2
```

Antes de crear el tag, generar desde el commit revisado:

```bash
git status --porcelain
git archive --format=zip --output=../ai-software-factory-v2.3.0-rc.2.zip HEAD
```

El primer comando debe estar vacío y el commit debe contener todos los archivos probados, incluidos scripts/config/skills. Probar el ZIP extraído en un directorio temporal. `.gitattributes` excluye material histórico del export.

Solo tras autorización explícita para publicar, subir el tag al destino confirmado y crear la release. No reutilizar un tag publicado para contenido diferente.

Antes, resolver [RELEASE_CHECKLIST](RELEASE_CHECKLIST.md) y el alcance de
[las notas RC](../releases/v2.3.0-rc.2.md). No promover multiagente operativo sin
piloto aceptado; una preview offline requiere aprobación explícita como tal.
