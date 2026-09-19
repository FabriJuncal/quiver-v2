# 03 — Persistir decisión

Cuando el usuario elige alternativa/testing y aprueba criterios:

actualizar:

```text
02_DECISION.md
```

Incluir:

- criterios aprobados;
- opción seleccionada;
- motivo;
- alternativas descartadas brevemente;
- testing seleccionado;
- **AI Strategy aprobada**;
- decisiones explícitas.

## AI Strategy aprobada

Persistir:

- Planning profile;
- Implementation default profile;
- Review profile;
- reasoning recomendado;
- triggers de escalamiento;
- oportunidades de downgrade.

La estrategia normativa vive en `STATE.md`; aquí registrar su aprobación y referencia, sin duplicar el bloque completo. Los modelos/IDs son recomendaciones resueltas con fecha, nunca modelo activo ni reemplazo del perfil aprobado.

Los modelos concretos se resuelven desde:

```text
config/MODEL_CATALOG.md
```

o configuración local equivalente.

No reanalizar lo aprobado.

No detenerse aquí.

Continuar automáticamente a Plan.
