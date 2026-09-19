# 08 — Implementation Review

Revisar:

- requirement;
- criterios;
- decisión;
- plan;
- diff;
- tests;
- evidencia.

Verificar el diff real y resultados recientes; CLOSURE_BRIEF es una referencia, no prueba suficiente por sí mismo. Comparar criterios con código y validaciones ejecutadas.

## Política de review

### N0

Self verification.

No `/review` por defecto.

### N1

Self review.

`/review` opcional si el cambio es compartido o tiene riesgo material.

### N2

Dedicated `/review` recomendado cuando:

- el diff no es trivial;
- afecta contratos compartidos;
- toca varias áreas;
- el review independiente puede reducir riesgo.

Si se activa:

```text
REVIEW GATE

QUÉ HACER

1. Ejecutá:
   /review

2. Elegí:
   [opción exacta resuelta por el agente y rama/commit exactos, si corresponde]

3. Cuando termine, volvé y escribí:
   continuar con review

ACCIÓN DEL USUARIO: requerida
```

Antes del gate, inspeccionar Git y resolver el alcance. Usar `Review uncommitted changes` solo si contiene toda la implementación pertinente. Si hay commits, indicar `Review against a base branch` con rama base verificada o `Review a commit` con SHA exacto. Si el alcance mezcla commits y cambios locales, cubrir ambos y registrar referencias. Un working tree vacío no demuestra revisión de la implementación. Si no se puede determinar la base, esa es la pregunta concreta que debe resolver el usuario.

### N3

N3 requiere review dedicado cuando sea técnicamente posible. Si no hay Git, herramienta disponible o acceso suficiente, documentar la causa y proponer revisión humana/equivalente; pedir `Aprobar alternativa de review: [alternativa concreta]` antes del cierre. No convertir la excepción en self review silencioso.

Modelo preferido de review:

**GPT-5.6 Sol (`gpt-5.6-sol`)**

Reasoning:

**High**

Si `review_model` está configurado, no exigir cambiar manualmente el modelo principal.

`review_model` solo selecciona modelo: no prueba el reasoning efectivo. High es una recomendación; verificarlo si el cliente lo expone, y registrar `NO VERIFICADO` si no lo hace. No inventar una clave de configuración para reasoning de review. Cambiar el modelo del mismo chat no constituye review independiente.

## Hallazgos

Validar:

- criterios;
- scope;
- regresiones plausibles;
- testing requerido;
- desviaciones.

No reabrir arquitectura aprobada sin evidencia nueva.

Estados:

- APROBADO
- APROBADO CON NOTAS
- REQUIERE AJUSTES

Cuando quede aprobado, continuar a Closure.

## Salida y evidencia

Clasificar hallazgos OBLIGATORIO/OPCIONAL. Corregir obligatorios dentro del alcance autorizado en una única ronda dirigida; repetir pruebas afectadas y revisar solo los cambios/finding pendientes. Si siguen abiertos, o cambia materialmente alcance/arquitectura, detenerse con evidencia y una propuesta concreta para aprobación. No hacer ciclos ilimitados ni cerrar con obligatorios pendientes.

Persistir en `05_IMPLEMENTATION_REVIEW.md` y STATE: alcance (base/HEAD o diff identificado), fecha, modalidad real, findings, pruebas, resultado y ronda. `continuar con review` indica retomar: leer los resultados reales antes de aprobar. Si la sesión nueva no tiene el resultado persistido, recuperar el artefacto o pedir exactamente el resultado faltante; nunca inferir aprobación del token de continuación.
