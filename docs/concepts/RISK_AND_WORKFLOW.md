# Riesgo y tamaño del workflow

Riesgo, testing y capacidad del modelo son dimensiones distintas. Clasificar por consecuencias, alcance, reversibilidad e incertidumbre; no por cantidad de archivos ni por el modelo elegido. Ante evidencia de mayor riesgo, reclasificar explicando qué cambió.

| Nivel | Criterio orientativo | Ruta |
|---|---|---|
| N0 | Cambio mecánico, local y reversible, sin cambio funcional: typo, texto o formato. | Compacta; verificación dirigida. |
| N1 | Comportamiento local bien comprendido, bajo impacto y reversión simple. | Compacta salvo decisión material; self review. |
| N2 | Contratos compartidos, varias áreas o integración con impacto material pero recuperable. | Completa; evaluar review dedicado según diff/riesgo. |
| N3 | Autorización/seguridad crítica, posible pérdida de datos, migración destructiva o arquitectura difícil de revertir. | Completa; review dedicado requerido si es técnicamente posible. |

## Ruta compacta N0/N1

Para trabajo que necesita persistencia, usar un único `docs/requirements/<slug>/STATE.md` con: petición, alcance, criterios, autorización, riesgo, validación, resultado y próxima acción. Registrar un plan breve y su self review dentro de ese mismo archivo; no generar siete documentos ni tres archivos por slice. Una tarea N0 ejecutada en un solo turno puede registrar evidencia y resultado en el estado del proyecto sin crear carpeta propia.

Si la petición ya define y autoriza el cambio, la aceptación/plan breve y T1 dirigido se derivan de ella: persistir esa fuente y continuar sin pedir aprobación repetida. Si criterios, alcance o alternativas materiales no están acordados, presentar exactamente esa decisión. No fabricar opciones ni forzar elegir T1/T2/T3 cuando no hay trade-off real.

Secuencia: petición autorizada → plan breve/self review → implementación → validación → self review según riesgo → evidencia/estado. Plan Review e Implementation Review son comprobaciones distintas aunque compartan archivo.

## Ruta completa N2/N3

Usar workflows 01–10 y templates de requirement/slice. Criterios y plan necesitan aprobación humana, que puede existir ya en una instrucción explícita; registrar versión, alcance y referencia. La autorización de ejecución se registra por separado. No duplicar gates aprobados.

El perfil T1/T2/T3 depende del riesgo concreto y decisiones del proyecto. ADVANCED no implica T3. N1 no implica T3. No reducir validación necesaria solo porque se use un modelo más capaz.

Una imposibilidad de review N3 no autoriza cerrar automáticamente: documentar la limitación, proponer revisión humana/equivalente y solicitar aprobación de esa alternativa con respuesta exacta.
