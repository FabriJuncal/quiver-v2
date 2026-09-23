# Modelo persistente del proyecto

## PROJECT_PROFILE.md

Responde:

> ¿Qué es este proyecto?

Contiene:

- tipo;
- negocio;
- stack;
- infraestructura;
- capacidades existentes;
- restricciones.

En un repositorio con variantes, el proyecto/familia no se confunde con HEAD. El
perfil puede referenciar un mapa externo revisado y un target por defecto, pero cada
tarea debe conservar ref completa y OID. Un documento del worktree es overlay local;
solo describe otros snapshots si existe evidencia explícita.

## CAPABILITY_MAP.md

Responde:

> ¿Qué tiene, qué necesita y qué hacemos con cada capacidad?

## PROJECT_STATE.md

Responde:

> ¿Dónde estamos ahora y qué sigue?

No es historial.

Representa el presente operativo.

## Requirement STATE.md

Responde:

> ¿Dónde está este ticket y cuál es la próxima acción?

Todo estado activo debe contener:

- fase;
- trabajo completado;
- trabajo en curso;
- próxima acción;
- motivo;
- `User action required`;
- `Expected output`;
- `After this`;
- bloqueos;
- instrucción de reanudación.
