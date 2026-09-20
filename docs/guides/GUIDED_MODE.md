# Guided Mode

Guided Mode es la experiencia por defecto.

Aplicar [Finalization Gate e invariants](../../workflow/00_SHARED_CONTRACT.md#finalization-gate--canónico)
antes de toda respuesta final. `ACCIÓN DEL USUARIO: ninguna` es una instrucción de continuidad,
no una frase de cierre: debe seguir ejecución real en el mismo turno. Si un límite del runtime
impide avanzar, usar estado explícito y reanudación exacta de [Runtime Guardrails](RUNTIME_GUARDRAILS.md).

La Factory debe:

1. saber dónde está;
2. saber qué completó;
3. saber qué sigue;
4. identificar si necesita al usuario;
5. continuar si no necesita una decisión.

## Estados

### Puede continuar

```text
ACCIÓN DEL USUARIO: ninguna
```

y continúa.

### Necesita decisión

```text
ACCIÓN DEL USUARIO: requerida
```

presenta opciones + recomendación.

### Bloqueado

Explica:

- qué falta;
- por qué es necesario;
- dónde reanudará.
- qué acción/dato concreto debe aportar el usuario, comando/opción si corresponde y texto exacto que debe escribir para continuar.

`User action required` considera cualquier boundary, no solo modelos. Un estado false no autoriza saltar una aprobación pendiente. Reconciliar estado con decisiones y evidencia al reanudar.

## No usar

```text
¿Cómo continuamos?
```

si el siguiente paso se puede derivar de `STATE.md`.


---

# Guided Mode + Model Routing

Un AI Model Gate también es un Decision Boundary.

La UX debe ser explícita.

No:

```text
Te recomiendo usar un modelo más potente.
```

Sí:

```text
Modelo:
GPT-5.6 Sol (gpt-5.6-sol)

Reasoning:
High

QUÉ HACER:
1. /status si no sabés qué está activo
2. /model
3. seleccionar GPT-5.6 Sol
4. seleccionar High
5. volver y escribir "continuar"
```

El usuario nunca debe quedar sin saber el siguiente paso.
