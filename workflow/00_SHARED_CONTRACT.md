# Contrato compartido de AI Software Factory

Este contrato define las reglas comunes para todos los prompts, skills y etapas de AI Software Factory.

Su objetivo es mantener el trabajo **guiado, proporcional, verificable y simple**, sin convertir cada tarea en un proceso burocrático.

---

## 1. Fuente de verdad

El repositorio del proyecto actual es la fuente de verdad sobre:

- código;
- arquitectura;
- requerimientos;
- decisiones aprobadas;
- estado del trabajo;
- reglas de negocio;
- convenciones del proyecto.

El historial del chat no es una fuente de verdad persistente.

Toda decisión, aprobación, cambio de alcance, hallazgo bloqueante o resultado de ejecución que deba sobrevivir a la sesión debe quedar persistido en el repositorio.

---

## 2. Principios generales

- Trabajar proporcionalmente al alcance, riesgo e incertidumbre.
- Cargar únicamente el contexto que pueda cambiar una decisión o implementación.
- No inventar archivos, componentes, contratos, reglas o comportamientos no verificados.
- No agregar requirements nuevos sin una decisión explícita.
- No reabrir decisiones aprobadas salvo nueva evidencia material.
- Integrar antes que migrar en proyectos existentes.
- Respetar el stack, arquitectura y convenciones existentes salvo requerimiento contrario.
- Preferir la solución mínima suficiente.
- No introducir dependencias, proveedores, infraestructura, abstracciones o agentes sin valor concreto.
- Nunca declarar éxito sin evidencia actual.

---

## 3. Guided Mode

AI Software Factory utiliza **Guided Mode** por defecto.

El usuario no debe tener que descubrir manualmente qué paso sigue.

Antes de finalizar una ejecución con trabajo pendiente, el agente debe:

1. identificar la fase actual;
2. identificar qué se completó;
3. determinar el siguiente paso concreto;
4. determinar si ese paso necesita intervención humana;
5. continuar automáticamente si no existe un Decision Boundary;
6. actualizar el estado persistente correspondiente.

No finalizar una ejecución únicamente con un resumen si todavía existe trabajo permitido dentro del alcance aprobado.

---

## 4. Decision Boundaries

Un **Decision Boundary** es un punto donde continuar automáticamente podría cambiar el alcance, asumir una preferencia material, introducir riesgo relevante o ejecutar una acción que debe decidir el usuario.

### Continuar automáticamente cuando corresponda

No solicitar intervención humana únicamente para:

- leer documentación;
- inspeccionar código;
- analizar el repositorio;
- localizar implementaciones existentes;
- buscar patrones o convenciones ya usadas;
- investigar fuentes verificables;
- comparar código existente;
- preparar matrices;
- detectar dependencias;
- identificar casos de uso;
- generar artefactos previamente aprobados;
- actualizar `PROJECT_STATE.md`;
- actualizar el `STATE.md` de un requirement;
- ejecutar validaciones previamente aprobadas;
- avanzar entre tareas que no cambien alcance, costo o riesgo material.

### Detenerse y pedir decisión cuando corresponda

Solicitar intervención humana ante decisiones materiales sobre:

- alcance;
- criterios de aceptación;
- alternativa de implementación con trade-offs reales;
- perfil de testing;
- arquitectura difícil de revertir;
- proveedor externo relevante;
- costo significativo;
- seguridad;
- manejo de datos sensibles;
- migración destructiva;
- pérdida potencial de datos;
- despliegue;
- operación irreversible;
- cambio material respecto de una decisión aprobada.

### Los approval gates siguen vigentes

Guided Mode **no elimina aprobaciones explícitas**.

Si una etapa o requirement exige aprobación humana, detenerse en ese punto aunque técnicamente sea posible continuar.

---

## 5. Cómo detenerse correctamente

No preguntar de forma genérica:

- "¿Cómo continuamos?"
- "¿Qué querés hacer ahora?"
- "¿Cuál es el siguiente paso?"

cuando el siguiente paso pueda derivarse del estado del proyecto.

Al detenerse, informar de forma breve:

### Estado

- Fase actual:
- Qué se completó:
- Próximo paso:
- Por qué sigue ese paso:
- Resultado esperado:

### Acción del usuario

Usar exactamente una de estas opciones:

`ACCIÓN DEL USUARIO: ninguna`

o:

`ACCIÓN DEL USUARIO: requerida`

Si la acción del usuario es `ninguna`, continuar con el siguiente paso permitido en la misma ejecución.

---

## 6. Cómo presentar una decisión

Cuando exista una decisión real, presentar únicamente opciones materialmente diferentes.

Formato recomendado:

```text
DECISIÓN NECESARIA

Opción A
Qué se hará, explicado de forma simple.
Tiempo relativo:
Complejidad:
Consumo IA:
Trade-off principal:

Opción B
...

RECOMENDACIÓN:
...

RESPUESTA SIMPLE:
A + T2
```

No crear alternativas artificiales.

Si solo existe una solución razonable, explicar la decisión necesaria sin inventar opciones.

---

## 7. Ruta guiada del proyecto

En proyectos nuevos, al cambiar de fase puede mostrarse una ruta corta de progreso.

Ejemplo:

```text
[✓] Discovery
[✓] Producto
[▶] Investigación
[ ] Flujo
[ ] Arquitectura
[ ] Backlog
[ ] Implementación
[ ] Release
```

No repetir esta ruta en cada respuesta.

Mostrarla principalmente cuando:

- se inicializa el proyecto;
- cambia la fase;
- el usuario pregunta por el estado;
- se alcanza un Decision Boundary.

---

## 8. Estado persistente

Todo proyecto adoptado por AI Software Factory debe mantener, cuando corresponda:

- `PROJECT_PROFILE.md`
- `PROJECT_STATE.md`
- `CAPABILITY_MAP.md`

Todo requirement activo debe mantener:

`docs/requirements/<ticket-o-slug>/STATE.md`

Después de una acción significativa:

- actualizar el estado;
- registrar una próxima acción concreta;
- indicar si requiere al usuario;
- registrar el resultado esperado;
- indicar qué viene después.

Una nueva sesión debe poder continuar sin depender del chat.

---

## 9. Implementación y etapas

No implementar código antes de que existan las aprobaciones requeridas por el workflow.

Una vez aprobado el alcance necesario para ejecutar una etapa:

- avanzar automáticamente por las acciones no decisionales de esa etapa;
- no pedir confirmaciones intermedias innecesarias;
- detenerse al siguiente Decision Boundary.

La unidad de interacción deja de ser:

> una etapa por respuesta

y pasa a ser:

> avanzar hasta el próximo Decision Boundary.

---

## 10. Testing

La estrategia de testing debe ser proporcional al riesgo.

No exigir automáticamente:

- regresión completa;
- end-to-end;
- performance;
- seguridad;
- carga;
- concurrencia;

si no existe un riesgo concreto relacionado.

Cuando exista un perfil de testing aprobado (`T1`, `T2`, `T3`), respetarlo.

No aumentar silenciosamente el perfil aprobado.

---

## 11. Evidence Before Completion

Nunca declarar que algo está:

- terminado;
- corregido;
- funcionando;
- compilando;
- aprobado;
- con tests exitosos;

sin evidencia reciente que lo demuestre.

Antes de cerrar una implementación:

1. identificar qué evidencia demuestra cada afirmación;
2. ejecutar las verificaciones requeridas cuando el entorno lo permita;
3. revisar el resultado real;
4. registrar la evidencia;
5. actualizar el estado.

La confianza del agente no sustituye evidencia.

---

## 12. Simplicidad

AI Software Factory existe para reducir complejidad.

No introducir por defecto:

- microservicios;
- event-driven architecture;
- nuevas bases de datos;
- RAG;
- vector databases;
- multi-agent orchestration;
- worktrees;
- nuevos proveedores cloud;
- abstracciones genéricas;
- sistemas de plugins;
- caches;
- queues;
- observabilidad avanzada;
- migraciones tecnológicas.

Incorporar complejidad únicamente cuando exista una necesidad real y verificable.
