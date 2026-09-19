# Guided Model Gates

Un Model Gate es un **Decision Boundary operacional**.

No es una decisión de producto.

Existe para que el usuario pueda cambiar la configuración de Codex sin perder el hilo del workflow.

## Cuándo aparece

Solo si Switch Benefit = HIGH y la configuración suficiente para la fase todavía no está confirmada en esta sesión. Un riesgo que exige mayor capacidad o un ahorro material en una fase extensa pueden justificar HIGH; una nueva slice no lo justifica por sí sola.

El review dedicado tiene su propio Review Gate en `workflow/08_IMPLEMENTATION_REVIEW.md`; no exige cambiar el modelo del chat.

## Model Gate de escalamiento

Siempre debe decir:

1. qué viene;
2. por qué el perfil actual puede ser insuficiente;
3. nombre completo del modelo;
4. ID exacto;
5. reasoning;
6. fallback;
7. comando `/status` si hay duda;
8. comando `/model`;
9. qué seleccionar;
10. qué escribir después.

## Nunca

```text
Te recomiendo cambiar de modelo.
```

sin explicar cómo hacerlo.

## Estado

No persistir `current model`.

Persistir únicamente la recomendación requerida para la tarea.

## Confirmation token

Por defecto:

```text
continuar
```

Si el gate es review:

```text
continuar con review
```

La Factory debe reconocer esos mensajes y retomar desde el estado persistido.

La confirmación solo satisface el gate presentado en esa sesión; no reemplaza otras aprobaciones. No repetir gates entre slices de una fase ya confirmada. Las sesiones nuevas no heredan una afirmación sobre el modelo activo.

Consultar `config/MODEL_CATALOG.md` para política canónica de duración, beneficio y fallback. Si no hay ningún modelo suficiente disponible, pedir `/model` y respuesta `Disponibles: ...`, explicar qué trabajo crítico se bloquea y continuar solo lo independiente ya autorizado.
