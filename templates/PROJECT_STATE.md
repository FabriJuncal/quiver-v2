# PROJECT_STATE

> Estado operativo actual del proyecto.
>
> Debe permitir que una nueva sesión comprenda rápidamente dónde está el proyecto y cuál es la próxima acción sin depender del historial del chat.

---

## Identificación

- **Project:**
- **Status:** not-started | active | blocked | paused | completed
- **Current phase:**
- **Current focus:**
- **Active requirement:**
- **Current slice:**
- **Last updated:**

---

## Ruta del proyecto

> Mantener corta. Actualizar cuando cambie de fase.

```text
[ ] Discovery
[ ] Producto / problema
[ ] Investigación externa, si corresponde
[ ] Flujo / reglas
[ ] Arquitectura / decisión técnica
[ ] Backlog / requirements
[ ] Implementación
[ ] Review
[ ] Release
```

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

## Reanudación

- **Resume instruction:**

Ejemplo:

```text
Continuar desde la verificación documental.
Leer primero el STATE del requirement activo y producir la matriz de campos.
No requiere decisión del usuario.
```

---

## Estado de decisiones

### Decisiones cerradas

-

### Decisiones pendientes

-

---

## Bloqueos

### Known blockers

-

### Missing information

-

---

## Contexto operativo relevante

> Incluir únicamente información que afecte el trabajo actual.

-

---

## Últimos cambios relevantes

-

---

## Reglas de mantenimiento

Actualizar este archivo cuando:

- cambie la fase;
- cambie el foco actual;
- se active o cierre un requirement;
- aparezca o desaparezca un bloqueo;
- se alcance una decisión importante;
- cambie la próxima acción.

No convertir este archivo en un historial completo.

El historial detallado pertenece a:

- Git;
- requirements;
- ADRs;
- closure documents.

`PROJECT_STATE.md` debe representar **el presente operativo**.
