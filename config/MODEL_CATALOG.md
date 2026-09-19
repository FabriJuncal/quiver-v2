# Model Catalog

> Catálogo canónico de modelos para AI Software Factory.
>
> **Regla de UX:** en mensajes al usuario escribir siempre **nombre completo + ID exacto**.
>
> Ejemplo correcto:
>
> `GPT-5.6 Terra (gpt-5.6-terra)`
>
> Evitar recomendaciones ambiguas como:
>
> `GPT-5.6`
>
> porque `gpt-5.6` es un alias y la Factory quiere que el usuario sepa exactamente qué variante seleccionar.

---

## Estado del catálogo

- **Last verified:** 2026-09-19
- **Target:** Codex CLI / Codex local
- **Named profiles:** Codex >= 0.134.0; modelos disponibles dependen además de cuenta, proveedor y runtime
- **Availability source of truth:** selector `/model` del runtime actual

La disponibilidad puede variar por:

- plan;
- autenticación;
- rollout;
- workspace;
- versión del cliente.

Si un modelo preferido no aparece en `/model`, utilizar la política de fallback de este documento.

---

# Perfiles canónicos

| Factory profile | Modelo preferido | ID exacto | Reasoning recomendado | Fallback |
|---|---|---|---|---|
| ECONOMICAL | **GPT-5.6 Luna** | `gpt-5.6-luna` | Low | **GPT-5.6 Terra** (`gpt-5.6-terra`) / Low |
| BALANCED | **GPT-5.6 Terra** | `gpt-5.6-terra` | Medium | **GPT-5.6 Sol** (`gpt-5.6-sol`) / Medium |
| ADVANCED | **GPT-5.6 Sol** | `gpt-5.6-sol` | High | **GPT-5.6 Terra** (`gpt-5.6-terra`) / High o XHigh |
| Exceptional Override | **GPT-6 Astra** | `gpt-6-astra` | High o XHigh | **GPT-5.6 Sol** (`gpt-5.6-sol`) / XHigh |

`Exceptional Override` **no es un cuarto perfil normal**.

Solo se usa cuando una tarea supera razonablemente el perfil ADVANCED normal.

---

# ECONOMICAL

## Modelo

**GPT-5.6 Luna**

ID:

```text
gpt-5.6-luna
```

Reasoning inicial:

```text
Low
```

## Usar para

- documentación mecánica;
- transformaciones repetitivas;
- resúmenes;
- handoffs ya decididos;
- cambios N0;
- renombres;
- edición de templates;
- tareas de alto volumen con resultado claro.

## Fallback

Si GPT-5.6 Luna no aparece:

**GPT-5.6 Terra (`gpt-5.6-terra`) + Low**

---

# BALANCED

## Modelo

**GPT-5.6 Terra**

ID:

```text
gpt-5.6-terra
```

Reasoning inicial:

```text
Medium
```

## Es el default de Factory

Usar para:

- Project Discovery;
- Product Discovery;
- desarrollo cotidiano;
- requirements N1/N2;
- frontend;
- APIs comunes;
- tests;
- investigación documental;
- debugging reproducible;
- planificación normal.

## Fallback

Si GPT-5.6 Terra no aparece:

**GPT-5.6 Sol (`gpt-5.6-sol`) + Medium**

No bloquear por una diferencia menor dentro del presupuesto autorizado. Si el aumento puede tener costo material o superar una restricción aprobada, presentar ese Decision Boundary antes de usar el fallback.

---

# ADVANCED

## Modelo

**GPT-5.6 Sol**

ID:

```text
gpt-5.6-sol
```

Reasoning inicial:

```text
High
```

## Usar para

- autorización;
- seguridad;
- aislamiento multi-tenant;
- integridad de datos;
- migraciones críticas;
- arquitectura difícil de revertir;
- concurrencia;
- pagos/billing crítico;
- debugging ambiguo;
- múltiples restricciones en conflicto;
- review crítico N2/N3.

## Fallback

Si GPT-5.6 Sol no aparece:

**GPT-5.6 Terra (`gpt-5.6-terra`) + High o XHigh**

Si el riesgo es excepcional y GPT-6 Astra está disponible, la Factory puede recomendar Astra en lugar de reducir capacidad.

Terra/High no es equivalente garantizado de Sol/High. Comprobar suficiencia para el riesgo. Si la capacidad resulta materialmente insuficiente, bloquear el trabajo crítico y proponer reducir alcance, revisión humana o esperar disponibilidad. No relajar criterios ni testing para acomodar un modelo.

---

# Exceptional Override

## Modelo

**GPT-6 Astra**

ID:

```text
gpt-6-astra
```

Reasoning:

```text
High
```

o:

```text
XHigh
```

## Solo cuando

- GPT-5.6 Sol + High/XHigh resultó insuficiente;
- la tarea es extraordinariamente difícil;
- existen múltiples sistemas/restricciones complejas;
- el beneficio esperado justifica latencia/consumo;
- un error tiene un costo material alto.

No utilizar GPT-6 Astra como default de Factory.

---

# Modelo y reasoning son decisiones diferentes

Antes de cambiar de modelo, preguntar:

> ¿Necesitamos realmente más capacidad de modelo o solamente más profundidad de razonamiento?

Ejemplo de escalamiento suave:

```text
GPT-5.6 Terra / Medium
→ GPT-5.6 Terra / High
```

Ejemplo de escalamiento fuerte:

```text
GPT-5.6 Terra / Medium
→ GPT-5.6 Sol / High
```

Escalamiento excepcional:

```text
GPT-5.6 Sol / XHigh
→ GPT-6 Astra / High o XHigh
```

---

# Escala conceptual

```text
GPT-5.6 Luna / Low
        ↓
GPT-5.6 Terra / Medium
        ↓
GPT-5.6 Terra / High
        ↓
GPT-5.6 Sol / High
        ↓
GPT-5.6 Sol / XHigh
        ↓
GPT-6 Astra / High o XHigh
```

No recorrer esta escala mecánicamente.

Elegir el salto mínimo suficiente.

---

# Política inicial

| Trabajo | Perfil inicial |
|---|---|
| Project Discovery | BALANCED — GPT-5.6 Terra / Medium |
| Product Discovery | BALANCED — GPT-5.6 Terra / Medium |
| Requirement N0 | ECONOMICAL — GPT-5.6 Luna / Low |
| Requirement N1 | BALANCED — GPT-5.6 Terra / Medium |
| Requirement N2 planning | BALANCED — GPT-5.6 Terra / Medium |
| Requirement N2 implementation | BALANCED — GPT-5.6 Terra / Medium |
| Requirement N2 critical review | ADVANCED — GPT-5.6 Sol / High |
| Requirement N3 planning | ADVANCED — GPT-5.6 Sol / High |
| Requirement N3 implementation | ADVANCED — GPT-5.6 Sol / High |
| Requirement N3 review | ADVANCED — GPT-5.6 Sol / High |
| Documentación mecánica | ECONOMICAL — GPT-5.6 Luna / Low |
| Bug simple reproducible | BALANCED — GPT-5.6 Terra / Medium |
| Bug difícil | ADVANCED — GPT-5.6 Sol / High |
| Arquitectura material | ADVANCED — GPT-5.6 Sol / High |
| UI común | BALANCED — GPT-5.6 Terra / Medium |
| Investigación externa | BALANCED — GPT-5.6 Terra / Medium |

---

# Switch Benefit

Antes de mostrar un AI Model Gate, clasificar el beneficio:

## LOW

Otro perfil sería teóricamente más barato o más rápido, pero el cambio no compensa la interrupción.

**No generar gate.**

## MEDIUM

El cambio puede aportar valor, pero la sesión actual sigue siendo razonablemente adecuada.

Normalmente:

- continuar;
- registrar recomendación para el próximo cambio de fase.

## HIGH

El modelo/reasoning actual puede ser materialmente insuficiente, o el ahorro esperado de una fase larga justifica el cambio.

**Generar AI Model Gate si falta confirmar la configuración suficiente en esta sesión.**

---

# Switch Threshold

Generar un Model Gate solo si Switch Benefit = HIGH y la configuración suficiente aún no está confirmada para la fase en esta sesión.

No generar gates por cada slice. El riesgo que exige capacidad adicional cuenta como HIGH; un Review Gate se gobierna por separado en workflow 08.

## Confirmación y duración de fase

Una fase agrupa trabajo con necesidades de capacidad similares; una slice nueva no es una fase nueva por sí sola. Mantener la configuración suficiente confirmada durante esa fase. No repetir un gate si el usuario ya confirmó la configuración requerida en esta sesión y no hay evidencia de cambio, insuficiencia o costo material nuevo.

`Model Gate required` persistido representa una recomendación de la tarea, no prueba de un gate pendiente. Reevaluar contra la confirmación de esta sesión. Un `continuar` solo confirma el gate al que responde; no equivale a aprobar criterios, plan o review.

En una sesión nueva no inferir el modelo activo del proyecto ni reconstruirlo del historial. Conservar las recomendaciones y pedir verificación solo antes de trabajo material que realmente dependa de esa configuración. Mientras tanto, continuar inspección segura autorizada.

---

# Escalamiento

Escalar inmediatamente ante:

- autorización/seguridad crítica;
- aislamiento de datos;
- pérdida potencial de datos;
- migración destructiva;
- arquitectura material N3;
- múltiples hipótesis fallidas;
- comportamiento difícil de reproducir;
- contradicciones que cambian la solución.

Para incertidumbre moderada sin riesgo alto, preferir primero:

**mismo modelo + reasoning mayor**.

---

# Downgrade

Un downgrade no debe interrumpir por tareas pequeñas.

No mostrar gate para:

- actualizar un `STATE.md`;
- completar `CLOSURE.md`;
- una edición corta;
- uno o dos pasos mecánicos restantes.

Mostrar optimización de downgrade únicamente si:

- comienza una fase nueva; y
- queda trabajo mecánico sustancial; y
- Switch Benefit = HIGH.

Considerar también el siguiente trabajo conocido: no bajar para volver a subir en la fase inmediatamente posterior si el ahorro no compensa ambas interrupciones. No usar un cambio de slice como excusa para downgrade. MEDIUM se reevalúa al final de la fase sin interrumpir.

---

# Disponibilidad

La Factory nunca debe decir:

> "Tenés que usar GPT-6 Astra"

si no confirmó que aparece en el runtime.

Debe decir:

```text
Modelo preferido:
GPT-6 Astra (gpt-6-astra)

Si no aparece en /model:
usar GPT-5.6 Sol (gpt-5.6-sol) / XHigh.
```

`/model` es la referencia final de disponibilidad en la sesión actual.

Si tampoco aparece el fallback: indicar `/model`, pedir que el usuario informe los IDs disponibles y responda `Disponibles: ...`. Continuar solo trabajo seguro independiente. Si Sol ya resultó insuficiente, no retornar a Sol como fallback de Astra sin un cambio concreto de alcance o mitigación aprobada. No imponer costos materiales ni rebajar calidad silenciosamente.

Los perfiles son capas de configuración, no garantías de selección efectiva: configuración del proyecto y flags CLI pueden prevalecer. `/status` ayuda a verificar la sesión. Compatibilidad oficial de perfiles separados desde 0.134.0: [OpenAI profiles](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles).

---

# Estado de sesión

No persistir como verdad de proyecto:

```text
Current model: ...
```

El modelo activo pertenece a la sesión y puede quedar obsoleto.

Persistir:

- perfil recomendado;
- reasoning recomendado;
- modelo preferido;
- fallback;
- fecha/catálogo usado.

La confirmación del cambio vive en la conversación/sesión actual.

---

# Review

Review dedicado se gobierna aparte del modelo principal.

Política:

- N0: self verification.
- N1: self review; `/review` opcional.
- N2: `/review` recomendado cuando el diff/riesgo sea material.
- N3: review dedicado requerido cuando sea técnicamente posible.
- Si es técnicamente imposible, documentar causa y aprobar una alternativa de review antes de cerrar; no degradar a self review silenciosamente.

Modelo recomendado para review crítico:

**GPT-5.6 Sol (`gpt-5.6-sol`)**

Si el usuario configura `review_model`, Codex puede utilizarlo sin cambiar manualmente el modelo principal.

Esa clave no demuestra el reasoning del reviewer. High es una recomendación: comprobarlo cuando el runtime lo exponga y declarar NO VERIFICADO si no. Política de alcance, evidencia, excepciones y límite de corrección: `workflow/08_IMPLEMENTATION_REVIEW.md`.

---

# Regla de costo

Optimizar costo total por tarea:

```text
planning
+ implementation
+ validation
+ review
+ retries
+ retrabajo
+ intervención humana
```

No optimizar únicamente precio por token.
