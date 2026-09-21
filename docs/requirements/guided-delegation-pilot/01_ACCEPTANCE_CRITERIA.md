# Criterios — propuesta v1

Aprobados con plan v1 el 2026-09-20 para implementación y verificación offline.
El texto de diseño debajo conserva su contexto original; resultados y distinción
entre contrato estático y comportamiento vivo en IMPLEMENTATION_EVIDENCE.md.

Los entregables de diseño D01–D05 derivan de la petición autorizada. Los criterios
funcionales AC01–AC12 son una propuesta para aprobar con el plan v1; no se declaran
implementados por existir este documento.

## Entrega de esta etapa

- D01: baseline y límites documentados sin modificar código/configuración personal.
- D02: contrato de ejecución acotada, contexto y estados consistente con v2.2.2.
- D03: cada criterio funcional tiene slice propuesta y escenario de validación.
- D04: self review del plan explícito; findings y límites reales registrados.
- D05: STATE/proyecto enlazados, próxima acción concreta y permiso de ejecución separado.

## Criterios funcionales del piloto futuro

| ID | Resultado exigido | Slice propuesta | Escenarios en VALIDATION.md |
|---|---|---|---|
| AC01 | Inline sigue funcionando sin archivos de intentos ni capacidades de subagentes | P01, P03 | V01, V02 |
| AC02 | Un coordinador y un worker máximo; solo coordinador acepta y escribe estado/proyecto | P01, P02, P03 | V03, V04 |
| AC03 | No despachar sin autorización, dependencias aceptadas, base y contexto identificados | P02, P03 | V05, V06, V07 |
| AC04 | Contexto mínimo trazable, sin transcript completo por defecto ni secretos en registros | P01, P03 | V08, V09 |
| AC05 | Entrega incluye alcance, propuesta, validaciones y pendientes; DONE no cierra una slice | P02, P03 | V10, V11 |
| AC06 | Aceptación valida revisión/base, diff aplicado y criterios; dependencias se liberan después | P02, P03 | V06, V11, V12 |
| AC07 | Reinicio, cancelación y entrega duplicada/obsoleta no causan doble ejecución o aceptación | P02, P03 | V13, V14, V15 |
| AC08 | Dos intentos máximo por encargo/versionado aprobado; sin recursión ni reset por cambio de modelo | P02, P03 | V16, V17 |
| AC09 | Routing reutiliza catálogo y registra solicitado/resuelto/observado sin inferir el modelo activo | P01, P03 | V18, V19 |
| AC10 | Guided Mode continúa, espera con mecanismo real o presenta boundary y reanudación exacta | P03 | V02, V14, V20 |
| AC11 | Override manual conserva permisos, criterios, dependencias y evidencia; no inventa slash commands | P03 | V05, V20 |
| AC12 | Validación estática distingue aprobado/invalidado/NO VERIFICADO; piloto opt-in no modifica proyectos viejos | P02, P04 | V21, V22, V23 |

## Medición sin prometer ahorro

Comparar una tarea acotada inline y delegada solo en un experimento autorizado
posterior, con el mismo alcance y criterios. Registrar revisión, resultados, tiempo
humano observado, duración, intentos, retrabajo y consumo expuesto. Si no hay datos,
usar unknown. Una comparación aislada es señal exploratoria, no prueba estadística
de eficiencia. No aprobar expansión si aumenta riesgo o no hay beneficio concreto.
