# Propuesta v2 — medir actividades dentro de cada trabajo

**Estado:** propuesta inicial desarrollada en [plan v2](03_PLAN.md) a pedido
del usuario el 2026-09-25. Para la decisión actual usar plan, criterios y D01.
La categoría
primaria del binding v1 permanece para compatibilidad, pero no debe usarse como
desglose exclusivo de la tarea en la vista v2.

## Comportamiento propuesto

1. El usuario indica solo la tarea nueva y el proyecto. La IA registra
   automáticamente tramos de actividad al trabajar: cambio de código, prueba,
   documentación o explicación. Un trabajo puede contener varios tramos y
   categorías; no se pide al usuario una etiqueta global.
2. Cada tramo conserva inicio/fin observables, identificadores de respuestas y
   evidencia mínima de acciones: tipo de operación y rutas de archivos afectadas,
   sin guardar contenidos, prompts ni argumentos. Pruebas y explicaciones sin
   edición también deben producir un tramo.
3. Las rutas y acciones permiten reconocer documentación y pruebas; distinguir
   una función nueva de un bugfix requiere además el objetivo del cambio o una
   señal equivalente. Si esa evidencia no existe, mostrar `implementación sin
   subtipo`, no adivinar. Kev podría sugerir el subtipo desde un resumen breve
   local, con confianza y sin afectar contabilidad exacta.
4. Tokens: asociar el contador nativo de una respuesta a un tramo solo cuando
   esa respuesta pertenece inequívocamente a uno. Si una misma respuesta mezcla
   código y documentación, conservar sus tokens en `mixto/no atribuible` hasta
   contar con un contador más granular. No dividirlos por líneas, bytes, cantidad
   de archivos ni porcentajes inventados. Mostrar cobertura de atribución.
5. Tiempo: medir duración de pared entre límites explícitos del tramo y, cuando
   exista, duración de la operación de herramienta. No llamar a ninguno de esos
   valores `tiempo activo de la IA`. Tramos paralelos o superpuestos se informan
   sin sumarlos como tiempo único.
6. USD: conservar `unknown` por categoría salvo evidencia de cargo directo
   atribuible a ese tramo. Un cargo total del trabajo no se reparte
   proporcionalmente; puede mostrarse aparte como total declarado del trabajo.

Ejemplo artificial: una tarea de nueva funcionalidad contiene un tramo de
código, otro de pruebas y otro de documentación. Los tres aparecen en el mismo
trabajo, cada uno con sus contadores observados. Una respuesta que edita código
y guía a la vez aparece como `mixto/no atribuible`, sin sumar dos veces tokens.

## Cambio de alcance y decisión

El observador actual registra tokens por respuesta y una categoría por binding;
no tiene contadores por archivo ni tiempos de pensamiento por edición. Esta
propuesta exige agregar telemetría prospectiva de tramos y reglas de atribución,
con pruebas artificiales de acciones simples, mixtas, reintentos, solapamientos y
ausencia de evidencia. No se activará ni leerá una fuente real durante el diseño.

**Continuidad:** el usuario pidió preparar el plan, y ese trabajo quedó
completado. La decisión pendiente ahora es aprobar [plan v2](03_PLAN.md) y
autorizar A01–A03 offline; v1 permanece cerrado.
