# Requirement State

> Estado operativo de un requirement.
>
> Debe permitir reanudar la tarea sin depender del historial del chat.

---

## Identificación

- **Ticket / slug:**
- **Title:**
- **Status:** draft | defining | approved | planning | ready-for-execution | in-progress | review | blocked | completed
- **Phase:**
- **Risk level:** 0 | 1 | 2 | 3
- **Last updated:**

---

## Decisiones

- **Acceptance criteria:** pending | approved
- **Selected option:**
- **Test profile:** T1 | T2 | T3 | not-selected
- **Plan version:**
- **Plan review:** pending | approved | approved-with-notes | requires-adjustments

---

## Ejecución

- **Current slice:**
- **Completed slices:**
- **Pending slices:**
- **Pending required findings:**
- **Implementation review:** pending | approved | approved-with-notes | requires-adjustments

---

## Progreso

### Completed

-

### In progress

-

### Pending

-

---

## Próxima acción

- **Next action:**
- **Why this is next:**
- **User action required:** false
- **Decision required:** none
- **Expected output:**
- **After this:**
- **Blocked by:** none

---

## Decision Boundary

> Completar únicamente si se necesita intervención humana.

- **Decision needed:**
- **Available options:**
- **Recommended option:**
- **Simple response format:**

Ejemplo:

```text
Decision needed:
Elegir estrategia de persistencia offline.

Available options:
A — IndexedDB directa
B — capa de persistencia especializada

Recommended option:
A para el MVP.

Simple response format:
A + T2
```

---

## Reanudación

- **Resume instruction:**

Ejemplo:

```text
Leer STATE.md y 01_ACCEPTANCE_CRITERIA.md.
Continuar con la verificación de fuentes oficiales.
No requiere acción del usuario.
```

---

## Bloqueos

### Blocking

-

### Non-blocking

-

---

## Evidencia relevante

> Registrar referencias breves. No duplicar `CLOSURE_BRIEF`.

-

---

## Reglas de mantenimiento

Actualizar este archivo después de cada cambio material de estado.

Toda actualización debe dejar explícito:

1. dónde está el requirement;
2. qué se completó;
3. qué sigue;
4. si necesita al usuario;
5. qué resultado se espera;
6. qué viene después.

No utilizar:

`Next action: revisar qué hacer`

cuando el siguiente paso pueda determinarse.

Preferir acciones ejecutables:

`Next action: verificar los campos obligatorios del formulario oficial X y registrar la matriz en DOCUMENT_MATRIX.md`.
