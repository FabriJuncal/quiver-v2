# Histórico de trabajo — estado y recorrido previsto

2026-09-28. Vista funcional del [plan OTel v1.2](../../../Plan_medicion_automatica_tokens_tiempo_Codex_Quiver.md).
Estado de ejecución: [STATE.md](STATE.md); evidencia: [EVIDENCE.md](EVIDENCE.md).

```text
┌──────────────────────────────────────────────────────────────┐
│ QUIVER · SABER EN QUÉ SE INVIERTE EL TRABAJO DE LA IA          │
├──────────────────────────────────────────────────────────────┤
│ PARA QUÉ                                                     │
│ Ver tokens y duración por proyecto y actividad: desarrollar,  │
│ corregir errores, probar, explicar y documentar.               │
├──────────────────────────────────────────────────────────────┤
│ BASE EXISTENTE · CIERRES CONSERVADOS                          │
│ ● Observador e histórico construidos en etapas anteriores     │
│ ● Reglas y reportes de actividades probados con ejemplos       │
│ ! Falta conectarlos al trabajo habitual de forma comprobada   │
├──────────────────────────────────────────────────────────────┤
│ ORGANIZAR CADA ENTREGA EN BLOQUES             ◀ ESTAMOS ACÁ   │
│ ● Propuesta aceptada e incorporada al plan                    │
│ ● Quiver propondrá las categorías; no tendrás que marcarlas   │
│ ○ Revisar este cambio antes de implementarlo                  │
│                                                             │
│ Ejemplo previsto: recuperar una contraseña                    │
│   Entender → Desarrollar → Probar → Documentar → Explicar      │
│                          ↘ Corregir → Volver a probar         │
│                                                             │
│ ! Son bloques de una misma entrega, según lo que necesite     │
│ ! Nombrar un bloque no demuestra cuánto consumió              │
├──────────────────────────────────────────────────────────────┤
│ RECIBIR LOS DATOS REALES · BLOQUEADO                          │
│ ● Se ensayó la captura y quedaron registrados sus problemas   │
│ ! Faltaron datos para comparar el consumo de forma completa   │
│ ! La prueba no quedó aislada de la configuración habitual     │
│ ○ Demostrar una forma de probar sin afectar ese entorno       │
├──────────────────────────────────────────────────────────────┤
│ RELACIONAR CADA BLOQUE CON SU CONSUMO · PENDIENTE              │
│ ○ Registrar automáticamente inicio, cambio y finalización     │
│ ○ Comparar lo planeado con lo que realmente ocurrió           │
│ ○ Comprobar que no falte consumo ni se cuente dos veces        │
│ ○ Conservar interrupciones, correcciones y reanudaciones      │
├──────────────────────────────────────────────────────────────┤
│ INTEGRAR Y COMPROBAR LA ENTREGA · PENDIENTE                    │
│ ○ Mostrar bloques y actividades en el histórico existente     │
│ ○ Mantener versiones anteriores sin cambiar sus cifras       │
│ ○ Validar una tarea completa con alcance autorizado           │
├──────────────────────────────────────────────────────────────┤
│ REGLAS QUE SE CONSERVAN                                       │
│ • Trabajo mezclado o sin evidencia: visible, sin inventar      │
│ • Dinero sin comprobante atribuible: desconocido              │
│ • Duración observada no equivale a tiempo pensando            │
│ • No necesitás abrir otro chat o enviar un mensaje por bloque │
└──────────────────────────────────────────────────────────────┘
```

El plan conserva cuatro agrupaciones (Análisis, Desarrollo, Pruebas y
Documentación) y el detalle de función nueva, corrección y explicación. No se
suman dos veces las cifras de agrupaciones y detalles. Los trabajos pequeños
sin slice también conservan sus bloques; no hay obligación de formalizar slices.

S01–S03/H01/H02/A01–A03 permanecen cerrados. Los resultados de sus pruebas son
históricos, no pruebas nuevas de automatización. Kev deja de ser dependencia de
la ruta OTel aprobada; sus intentos no se convierten en una evaluación superada.
P3 mantiene un caso final acotado con captura y atribución completas: mostrar
mezcla es honesto, pero no permite aprobar ese caso si debía ser separable.

**Única siguiente acción:** revisión dirigida del delta del plan v1.2/P4. El
contrato de aislamiento v1.2 sigue pendiente; no hay otra sesión autorizada.
