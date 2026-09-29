# Criterios v2 — atribución por actividad

2026-09-25. Aprobados junto con D01 y plan v2 por respuesta explícita del usuario.
A01–A03 se verificaron offline; AC12/AC13 continúan pendientes de A04/A05.

| ID | Resultado exigido | Slice / prueba |
|---|---|---|
| AC01 | El usuario indica tarea y proyecto; no necesita asignar categoría. Una tarea contiene desarrollo, fix, pruebas, explicación y documentación según sus actividades. | A01–A03 / T01, T05 |
| AC02 | Captura prospectiva de acciones con IDs, límites temporales, resultado y roles de archivos; incluye tests y explicaciones sin edición. No se reconstruye tiempo desde mtime ni cantidad de líneas. | A01 / T01–T03 |
| AC03 | La categoría se decide automáticamente a partir de acción, evidencia mínima y objetivo. Se distingue la medición observada de la categoría inferida por Kev; se conserva su procedencia. | A02 / T06–T08 |
| AC04 | Una respuesta nativa aporta sus seis contadores una sola vez. Solo una relación verificable respuesta→actividad con cobertura de acciones completa permite atribución exclusiva; una sola edición observada o coincidencia temporal no basta. | A01, A03 / T02, T04 |
| AC05 | Respuestas con varias actividades quedan en mixto; sin enlace quedan sin atribuir; código sin propósito suficiente queda implementación sin subtipo. La incertidumbre es visible y no exige una etiqueta del usuario. | A02, A03 / T04–T06 |
| AC06 | Categorías + mixto + sin atribuir + sobrecarga contabilizada concilian con el total observado. No hay reparto por probabilidades, archivos, bytes o líneas. | A03 / T04, T09 |
| AC07 | Duración de actividad y herramienta se muestran separadas. Ausencia de límites produce unknown; solapamientos no inflan tiempo único y tiempo activo de IA permanece unknown. | A03 / T10 |
| AC08 | USD por actividad solo con cargo directo y evidencia atribuible. Un cargo del trabajo no se reparte. Tarifas sintéticas y consumo propio de Kev no se presentan como gasto del modelo desarrollador. | A03 / T11 |
| AC09 | Historial JSON/texto por proyecto, tarea y actividad; última revisión consistente, sin reimportar pasado ni alterar reportes v1/v2 anteriores. Cambiar clasificación crea revisión y no altera contadores. | A03 / T09, T12 |
| AC10 | Kev funciona local y automáticamente por actividad: múltiples indicadores permiten detectar mezcla. Timeout, indisponibilidad o poca evidencia producen abstención; no bloquean la tarea. | A02 / T06–T08 |
| AC11 | Evidencia mínima privada; resumen acotado solo en memoria hacia loopback. Sin logs de conversaciones, contenido de archivos, argumentos ni secretos; no se recorren otras sesiones. | A01–A03 / T03, T08, T13 |
| AC12 | Clasificación automática con Kev requiere evaluación real del checkpoint fijado, umbrales y dataset congelados; fixtures de API no prueban precisión. | A04 / T14 |
| AC13 | La automatización completa requiere un piloto que observe realmente las acciones, enlace contadores y concilie el reporte sin etiquetas manuales. Sin señal del host, declarar parcial; no cerrar por simulación. | A05 / T15 |

T2: fixtures artificiales para A01–A03, evaluación artificial con Kev real para
A04 y piloto acotado autorizado para A05. No repetir gates cerrados S01–S03 ni
H01/H02; ejecutar únicamente sus regresiones directamente afectadas.
