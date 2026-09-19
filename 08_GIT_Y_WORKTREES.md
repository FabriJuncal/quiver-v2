# Git profesional sin complejidad

## Default

```text
main
 ├─ feat/TICKET-descripcion
 ├─ fix/TICKET-descripcion
 └─ chore/TICKET-descripcion
```

## Flujo

```text
ticket → branch → commits pequeños → tests → PR → preview → review → merge
```

## Worktrees

No crear uno por defecto.

Usar cuando:

- se necesita mantener otra rama activa;
- hay trabajo paralelo independiente;
- se quiere aislar un experimento;
- otro agente va a modificar el mismo repo en paralelo.

## Parallel agents

No usar por defecto.

Permitir solo cuando:

- hay 2+ tareas independientes;
- no comparten estado;
- no modifican los mismos archivos;
- el costo adicional se justifica.
