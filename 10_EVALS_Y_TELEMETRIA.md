# Evals y telemetría

## Qué medir

Por requirement:

```text
tipo
nivel
modelo usado
perfil de testing
tokens/créditos si existen
tiempo
número de revisiones
hallazgos reales
retrabajo
intervención humana
bugs posteriores
```

## Evals prioritarios

Evaluar solo skills críticas:

- project-discovery.
- plan-reviewer.
- implementation-reviewer.
- systematic-debugging.
- legacy-migration.

## Ejemplo de eval legacy-migration

Comprobar:

- encontró implementación legacy;
- identificó reglas;
- detectó diferencias;
- evitó inventar comportamiento;
- evitó cambios fuera de alcance.

## Token optimization

Optimizar `tokens por tarea`, no `tokens por request`.

Primero medir; luego comprimir contexto, evitar lecturas repetidas, cargar referencias bajo demanda y usar modelos más baratos solo cuando la calidad lo permite.
