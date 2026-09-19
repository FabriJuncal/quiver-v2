# AGENTS.md

Instrucciones específicas del proyecto para agentes que trabajan con AI Software Factory.

Mantener este archivo corto y enfocado en reglas persistentes del repositorio.

Las reglas específicas del proyecto tienen prioridad sobre recomendaciones genéricas de AI Software Factory cuando no existe conflicto con una instrucción explícita del usuario.

---

## 1. Fuente de verdad

Priorizar:

1. código y datos reales;
2. requirements aprobados;
3. ADRs y decisiones persistidas;
4. `PROJECT_PROFILE.md`;
5. `PROJECT_STATE.md`;
6. `CAPABILITY_MAP.md`;
7. documentación del repositorio;
8. `STATE.md` del requirement activo.

El chat no es una fuente de verdad persistente.

No reconstruir decisiones desde memoria cuando ya existen artefactos en el repositorio.

---

## 2. Inicio de una tarea

Antes de realizar cambios significativos:

1. leer `PROJECT_STATE.md` si existe;
2. identificar el requirement activo;
3. leer `docs/requirements/<ticket>/STATE.md` si existe;
4. cargar únicamente el contexto necesario;
5. revisar skills específicas de `.agents/skills/` cuando correspondan;
6. respetar decisiones ya aprobadas.

No volver a analizar el proyecto completo por defecto.

---

## 3. Guided Mode

Este proyecto utiliza **Guided Mode**.

El agente debe guiar el trabajo hasta el próximo **Decision Boundary**.

Antes de detenerse con trabajo pendiente:

1. identificar la fase actual;
2. determinar el siguiente paso concreto;
3. comprobar si requiere una decisión humana;
4. continuar automáticamente si no requiere decisión;
5. actualizar el estado persistente.

No preguntar genéricamente:

- "¿Cómo continuamos?"
- "¿Qué querés hacer ahora?"
- "¿Cuál es el siguiente paso?"

cuando exista una próxima acción derivable.

### Cuando no requiere intervención

Indicar:

`ACCIÓN DEL USUARIO: ninguna`

y continuar con el siguiente paso permitido.

### Cuando requiere intervención

Indicar:

`ACCIÓN DEL USUARIO: requerida`

y presentar:

- decisión;
- opciones reales;
- trade-offs;
- recomendación;
- respuesta simple esperada.

Guided Mode no permite saltarse approval gates explícitos.

---

## 4. Estado persistente

Mantener actualizado:

- `PROJECT_STATE.md`;
- `docs/requirements/<ticket>/STATE.md` para requirements activos.

Todo estado activo debe indicar:

- fase;
- próxima acción;
- motivo;
- si requiere al usuario;
- resultado esperado;
- qué viene después;
- bloqueos.

Una nueva sesión debe poder continuar leyendo estos archivos.

---

## 5. Routing de skills

Usar skills bajo demanda.

### Bug, regresión o test fallido

→ `systematic-debugging`

Primero investigar causa raíz.

No aplicar fixes especulativos sucesivos.

### SDK, API externa o framework sensible a versión

→ `source-driven-development`

Consultar fuentes oficiales cuando una decisión dependa de comportamiento actual o versión.

### API, endpoint o contrato

→ `api-and-interface-design`

### Decisión arquitectónica real

→ `architecture-decision-framework`

No utilizar para cambios simples.

### UI

→ Impeccable, si está instalado y aporta valor.

→ browser testing cuando la verificación real de UI/interacción lo justifique.

### Schema o datos

→ `database-change-safety`, si está disponible.

### Legacy o migración funcional

→ `legacy-migration`, si está disponible.

### Seguridad

→ skill/review especializado únicamente cuando el riesgo, alcance o requerimiento lo justifique.

### Tokens

→ `token-optimization` únicamente cuando exista un problema real de contexto, costo o loops.

No ejecutar todas las skills por defecto.

---

## 6. Testing

Aplicar testing proporcional al riesgo y al perfil aprobado.

No exigir automáticamente:

- regresión completa;
- end-to-end;
- performance;
- seguridad;
- carga;
- concurrencia.

Respetar `T1`, `T2` o `T3` cuando exista un perfil aprobado.

No aumentar silenciosamente el nivel de testing.

---

## 7. Evidence Before Completion

No afirmar:

- completado;
- fixed;
- funcionando;
- build OK;
- tests OK;
- listo para merge;
- listo para producción;

sin evidencia reciente.

Antes del cierre:

1. ejecutar las validaciones necesarias cuando sea posible;
2. revisar el resultado real;
3. registrar evidencia relevante;
4. actualizar `CLOSURE_BRIEF`;
5. actualizar `STATE.md`.

La confianza del agente no sustituye evidencia.

---

## 8. Git

Mantener cambios enfocados y revisables.

Preferir:

- branch por trabajo cuando corresponda;
- commits pequeños y coherentes;
- mensajes claros;
- Pull Request para cambios relevantes;
- `main` estable.

No crear worktrees por defecto.

Utilizarlos únicamente cuando el aislamiento o trabajo paralelo aporte valor concreto.

No ejecutar operaciones destructivas sin autorización.

---

## 9. Proyectos existentes

La Factory se adapta al proyecto.

No modificar el proyecto para adaptarlo innecesariamente a la Factory.

Priorizar:

- `KEEP`
- `ADD`
- `WRAP`
- `IMPROVE`
- `REPLACE_LATER`
- `IGNORE`

Integrar antes que migrar.

No reescribir stack, arquitectura, autenticación, base de datos o deployment sin evidencia y decisión aprobada.

---

## 10. Complejidad

No agregar automáticamente:

- dependencias;
- herramientas;
- agentes;
- microservicios;
- queues;
- caches;
- RAG;
- vector databases;
- nuevos proveedores;
- infraestructura;
- abstracciones genéricas;

sin justificar un valor concreto para el requerimiento actual.

Preferir la solución mínima que:

1. cumpla el objetivo;
2. sea mantenible;
3. permita escalar cuando aparezca una necesidad real.
