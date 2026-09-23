# 05 — Plan Reviewer

Revisar el plan separadamente de la implementación. Declarar la modalidad real: self review del plan o reviewer dedicado. No afirmar independencia de contexto si la misma sesión realiza ambas tareas.

No rediseñar por iniciativa propia.

Validar trazabilidad interna:

```text
Acceptance Criterion
→ Implementation Step
→ Validation
```

También validar la **AI Strategy** únicamente en términos de proporcionalidad:

- ¿existe decisión de routing-v1 o referencia vigente, con motivo, verificación y contexto?;

- ¿se propone ADVANCED sin necesidad real?;
- ¿se propone ECONOMICAL para una tarea de riesgo/ambigüedad material?;
- ¿el review crítico tiene suficiente independencia/capacidad?;
- ¿existen tareas mecánicas que deberían hacer downgrade?;
- ¿la estrategia parece optimizar costo total por tarea y no solo precio por llamada?

No convertir preferencias de modelo en hallazgos bloqueantes salvo que el perfil propuesto sea materialmente insuficiente para el riesgo.

Si falta evidencia de routing, completar la evaluación antes de aprobar, sin exigir
registro duplicado ni gate de usuario por el trámite. Aplicar excepciones N0/consultas
del catálogo. Una referencia obsoleta no satisface la obligación.

Hallazgos:

- `OBLIGATORIO`;
- `OPCIONAL`.

Estados:

- `APROBADO`;
- `APROBADO CON NOTAS`;
- `REQUIERE AJUSTES`.

Si existen ajustes obligatorios que no cambian una decisión humana, permitir una única corrección dirigida y volver a verificar.

Si siguen abiertos, detenerse con IDs pendientes, evidencia y propuesta concreta; solicitar `Aprobar plan corregido` o la decisión material necesaria. No pedir aprobación de un plan conocido como defectuoso ni repetir el ciclo indefinidamente. Hallazgos opcionales no bloquean.

Cuando el plan quede revisado, detenerse para aprobación humana del plan.

Si el usuario ya aprobó explícitamente este plan y autorizó ejecutar dentro del mismo alcance, registrar ambas aprobaciones y continuar. No confundir el veredicto del reviewer con aprobación humana. N0/N1 siguen la ruta compacta.

Presentar:

```text
ACCIÓN DEL USUARIO: requerida
RESPUESTA SIMPLE: "Aprobar plan" o indicar cambio.
```

Si el usuario quiere implementación inmediata puede responder:

```text
Aprobar plan y ejecutar.
```
