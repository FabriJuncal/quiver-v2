# Git simple y profesional

Default:

```text
main
 ├── feat/TICKET-descripcion
 ├── fix/TICKET-descripcion
 └── chore/TICKET-descripcion
```

Flujo:

```text
ticket
→ branch
→ commits pequeños
→ tests
→ push
→ PR
→ review
→ merge
```

## Worktrees

No usar por defecto.

Usarlos cuando:

- necesitás aislamiento real;
- trabajás en dos tickets simultáneos;
- un agente paralelo modifica otro dominio;
- necesitás mantener otra branch ejecutándose.

## Commits

Ejemplos:

```text
feat: add organization invitations
fix: handle expired authorization token
test: cover tenant permission checks
docs: document billing flow
```
