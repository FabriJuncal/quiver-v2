# 04 — Plan técnico

Generar:

```text
03_PLAN.md
```

Basarse en:

- requirement;
- criterios aprobados;
- decisión aprobada;
- AI Strategy;
- contexto verificado.

Incluir:

- objetivo;
- alcance;
- componentes/áreas afectadas;
- pasos;
- dependencias;
- estados/errores;
- validación;
- riesgos;
- rollback cuando aplique;
- slices propuestas.

## IA

Para cada slice propuesta indicar provisionalmente:

- perfil;
- reasoning;
- motivo.

Antes de planning, evaluar su perfil con model-router. Un planning N3 también puede necesitar un Model Gate HIGH: resolverlo antes del trabajo crítico. No postergar automáticamente todos los gates hasta implementación.

Para slices futuras dejar recomendaciones provisionales; reevaluar beneficio y confirmación de sesión al ejecutarlas. Referenciar AI Strategy en STATE en lugar de duplicarla.

Después continuar automáticamente a Plan Review.
