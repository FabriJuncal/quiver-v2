# 06 — Crear slices

Solo después de plan aprobado.

Crear slices pequeñas, coherentes y verificables.

Cada slice:

```text
slices/<NN-slug>/
├── SPEC.md
├── EXECUTION_BRIEF.md
└── CLOSURE_BRIEF.md
```

## AI Execution Profile

Usar `model-router` para cada slice.

Heredar AI Strategy de STATE. Si no hay excepción, basta una referencia al perfil de esa fase. Cuando la slice necesite una configuración diferente, persistir en `EXECUTION_BRIEF.md`:

- profile;
- preferred model full name;
- exact model ID;
- reasoning;
- fallback full name;
- fallback ID;
- switch benefit;
- Model Gate required;
- reason;
- escalation trigger;
- downgrade opportunity;
- catalog date.

No asumir el modelo activo.

No generar Model Gate solo porque otra configuración sea ligeramente más óptima.

Model Gate solo si Switch Benefit = HIGH y falta una confirmación suficiente para la fase en esta sesión. Riesgo que exige escalamiento se clasifica HIGH. Review se rige por su Review Gate separado en workflow 08.

Actualizar requirement `STATE.md`.

Si implementación está autorizada, continuar a primera slice.

Si no, persistir `Execution authorization: pending`, explicar que el plan ya está aprobado pero falta permiso de ejecución y pedir exactamente `Ejecutar plan aprobado`. Una autorización anterior dentro del alcance sigue siendo válida.
