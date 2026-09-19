# Prompt — Reanudar proyecto o requirement

Utiliza este prompt para continuar trabajo existente sin depender del historial del chat.

El objetivo es que una sesión nueva pueda determinar **dónde está el trabajo, qué sigue y si debe continuar automáticamente**.

---

## Procedimiento

### 1. Leer el estado general

Leer primero:

`PROJECT_STATE.md`

Identificar:

- fase actual;
- foco actual;
- requirement activo;
- slice activa;
- trabajo completado;
- trabajo en curso;
- bloqueos;
- próxima acción.

---

### 2. Leer el requirement activo

Si existe un requirement activo, leer:

`docs/requirements/<ticket-o-slug>/STATE.md`

Identificar:

- estado;
- fase;
- nivel de riesgo;
- decisiones aprobadas;
- perfil de testing;
- versión del plan;
- review del plan;
- slice actual;
- hallazgos pendientes;
- próxima acción;
- si requiere al usuario.

---

### 3. Cargar únicamente contexto necesario

Después de conocer la próxima acción, cargar únicamente los artefactos necesarios para ejecutarla.

Ejemplos:

- requirement original;
- criterios aprobados;
- decisión;
- plan;
- review;
- slice activa;
- `EXECUTION_BRIEF`;
- código directamente afectado;
- documentación o fuentes necesarias.

No volver a leer todo el proyecto por defecto.

No reconstruir decisiones ya persistidas.

---

## Guided Resume

Mostrar inicialmente una síntesis breve:

```text
ESTADO ACTUAL

Fase:
Requirement:
Slice:
Progreso:
Próximo paso:
Acción del usuario: ninguna | requerida
```

Este bloque es orientativo y debe ser corto.

### Si no requiere al usuario

Si el estado indica:

`User action required: false`

o la siguiente acción puede ejecutarse sin una decisión material:

1. informar brevemente qué se hará;
2. mostrar:

`ACCIÓN DEL USUARIO: ninguna`

3. continuar inmediatamente con la acción.

**No finalizar la respuesta después de indicar el siguiente paso.**

---

### Si requiere al usuario

Si el estado indica:

`User action required: true`

o se alcanza un Decision Boundary:

1. explicar qué decisión se necesita;
2. presentar únicamente opciones materialmente diferentes;
3. indicar trade-offs;
4. recomendar una opción;
5. permitir una respuesta corta.

Ejemplo:

```text
DECISIÓN NECESARIA

A — Mantener solución existente
Tiempo: bajo
Complejidad: baja
Consumo IA: bajo

B — Introducir nuevo proveedor
Tiempo: medio
Complejidad: media
Consumo IA: medio

RECOMENDACIÓN:
A, porque cumple el alcance actual sin agregar una nueva dependencia.

RESPUESTA SIMPLE:
A + T2
```

---

## Reglas

- No depender del historial del chat.
- No reabrir decisiones cerradas.
- No volver a planificar trabajo ya aprobado.
- No introducir mejoras opcionales durante una reanudación.
- No cambiar el alcance.
- No inventar trabajo para "mantenerse ocupado".
- No ejecutar acciones irreversibles sin aprobación.
- No preguntar "¿Cómo continuamos?" cuando existe una próxima acción derivable.

---

## Actualización de estado

Después de ejecutar la próxima acción:

1. actualizar `PROJECT_STATE.md` cuando cambie el estado general;
2. actualizar el `STATE.md` del requirement;
3. registrar:
   - qué se completó;
   - nueva próxima acción;
   - por qué sigue;
   - si requiere al usuario;
   - resultado esperado;
   - qué viene después.

---

## Resultado esperado

La interacción ideal debe permitir que el usuario diga solamente:

```text
Continuá PROJ-123.
```

El agente debe poder:

```text
STATE
→ contexto mínimo
→ acción
→ actualización STATE
→ siguiente Decision Boundary
```

sin pedir al usuario que reconstruya la conversación anterior.
