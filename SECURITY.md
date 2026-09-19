# Security

AI Software Factory incluye instrucciones, skills y scripts que pueden ser utilizados por agentes con acceso a tu repositorio.

## Recomendaciones

- Revisá cualquier skill de terceros antes de instalarla.
- No ejecutes scripts descargados desde repositorios desconocidos sin inspeccionarlos.
- Mantené secretos fuera de Markdown, prompts, logs y Git.
- Utilizá sandbox/approvals cuando estén disponibles.
- No otorgues permisos de producción a un agente si no son necesarios.
- Para Browser/Computer Use, preferí perfiles aislados.
- No conectes MCPs solamente porque estén disponibles.

## Scripts de Factory

Los scripts oficiales de este repositorio:

- no deben eliminar proyectos;
- no deben reemplazar silenciosamente un `AGENTS.md` existente;
- no deben borrar skills que no pertenezcan a Factory;
- no deben instalar MCPs automáticamente.

## Reportar un problema

Abrí un Security Advisory privado en GitHub si el repositorio tiene habilitada esa función.

No publiques secretos, tokens ni credenciales en Issues.
