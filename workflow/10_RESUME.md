# 10 — Resume

Reanudar sin depender del chat.

Aplicar la jerarquía de [Source of Truth](../docs/concepts/SOURCE_OF_TRUTH.md) y el
[Finalization Gate e invariants](00_SHARED_CONTRACT.md#finalization-gate--canónico).
Leer primero STATE; comparar después Conversation Recap. Una contradicción se registra en
STATE y se ignora el recap. Nunca inferir «sin pendientes» si existe una slice activa.
Verificar `Runtime limitation`, conservar pendiente/reanudación y limpiarla solo con evidencia
de resolución. No confundir límites del runtime con blockers del producto.

## 1. Estado general

Leer:

```text
PROJECT_STATE.md
```

## 2. Requirement

Si hay uno activo:

```text
docs/requirements/<ticket>/STATE.md
```

## 3. Determinar

- fase;
- progreso;
- próxima acción;
- `User action required`.

## 4. Contexto mínimo

Cargar únicamente artefactos necesarios para la próxima acción.

Contrastar STATE con decisiones/aprobaciones, Git diff y evidencia reciente de la slice. Si hay una interrupción, no repetir pasos destructivos ni asumir que una acción en progreso terminó. Diferenciar aprobación del reviewer, aprobación humana de la versión del plan y autorización de ejecución. Si falta prueba de autorización, pedir exactamente la aprobación faltante.

Si PROJECT_STATE y el requirement discrepan, reconciliar con artefactos verificables; no elegir automáticamente el indicador que permite continuar. Un blocker real o aprobación pendiente prevalece sobre `User action required: false`.

Las confirmaciones de modelo pertenecen a la sesión; una nueva sesión conserva la recomendación pero verifica configuración solo si la próxima tarea material lo requiere. No repetir gates en cada slice de una fase ya confirmada. Recuperar evidencia persistida del review antes de cerrar.

## Guided Resume

Mostrar brevemente:

```text
ESTADO ACTUAL

Fase:
Requirement:
Slice:
Próximo paso:
Acción del usuario:
```

Si:

```text
User action required: false
```

indicar:

```text
ACCIÓN DEL USUARIO: ninguna
```

y **continuar inmediatamente**.

No terminar solamente mostrando la próxima acción.

Si requiere decisión, explicar estado, motivo, acción exacta, comando/opción cuando aplique y texto de reanudación; presentar solo alternativas materialmente diferentes. Si no hay trabajo pendiente, esperar una nueva petición sin inventar alcance.

Después de ejecutar, actualizar estados.

La interacción ideal debe permitir:

```text
Continuá PROJ-123.
```
