# 02 — Criterios, opciones, testing y estrategia IA

Analizar proporcionalmente.

Entregar:

1. clasificación de riesgo;
2. incertidumbre;
3. criterios verificables;
4. preguntas bloqueantes mínimas;
5. alternativas solo si existen trade-offs reales;
6. explicación no técnica;
7. tiempo relativo;
8. complejidad;
9. consumo IA relativo;
10. trade-off;
11. recomendación;
12. perfiles T1/T2/T3 aplicables;
13. testing recomendado;
14. **AI Strategy recomendada**.

## AI Strategy

Aplicar `model-router`.

Resolver:

- Planning profile;
- modelo completo + ID;
- reasoning;
- fallback;
- Implementation default profile;
- Review profile;
- dedicated review policy;
- escalation triggers;
- switch threshold;
- posibles downgrade boundaries.

Mostrar siempre nombres completos:

- GPT-5.6 Luna (`gpt-5.6-luna`)
- GPT-5.6 Terra (`gpt-5.6-terra`)
- GPT-5.6 Sol (`gpt-5.6-sol`)
- GPT-6 Astra (`gpt-6-astra`)

No asumir el modelo activo.

Persistir el borrador en:

```text
01_ACCEPTANCE_CRITERIA.md
```

y actualizar `STATE.md` con AI Strategy propuesta.

Este es un Decision Boundary si quedan criterios o decisiones materiales sin aprobar. Registrar aprobaciones ya explícitas; no pedirlas de nuevo ni convertir una recomendación de testing sin trade-off en una elección obligatoria. Para N0/N1 usar la ruta compacta del contrato.

Permitir respuesta corta:

```text
B + T2 + aprobar criterios
```

El usuario no necesita elegir manualmente la AI Strategy salvo que quiera modificarla.
