# Configuración global de Codex para AI Software Factory

> Guía para conectar **AI Software Factory** con Codex de forma reutilizable en todos tus proyectos, sin copiar toda la Factory dentro de cada repositorio.

---

# 1. Objetivo

AI Software Factory debe vivir como un proyecto reutilizable separado de los proyectos reales.

La arquitectura recomendada es:

```text
HOME
│
├── .codex/
│   └── AGENTS.md
│
├── .agents/
│   └── skills/
│
└── Projects/
    │
    ├── ai-software-factory/
    │
    ├── proyecto-a/
    │
    ├── proyecto-b/
    │
    └── ...
```

Responsabilidades:

```text
~/.codex/AGENTS.md
→ reglas globales de trabajo con Codex

~/.agents/skills/
→ skills reutilizables disponibles desde cualquier proyecto

~/Projects/ai-software-factory/
→ metodología, templates, documentación, starters, prompts y fuente de las skills

cada proyecto/
→ código, decisiones, estado, requirements y skills específicas
```

La regla principal es:

> **AI Software Factory se reutiliza. No se copia completa dentro de cada proyecto.**

---

# 2. Ubicación recomendada

Se recomienda mantener AI Software Factory en una ruta fija:

```bash
~/Projects/ai-software-factory
```

Por ejemplo:

```text
/Users/tu_usuario/Projects/ai-software-factory
```

Si actualmente está en otro lugar, puede mantenerse allí. Lo importante es evitar moverla constantemente.

Para comprobar la ruta real:

```bash
cd ~/Projects/ai-software-factory
pwd
```

Guardar la ruta mostrada.

---

# 3. Crear la configuración global de Codex

Crear el directorio global de Codex:

```bash
mkdir -p ~/.codex
```

Comprobar su contenido:

```bash
ls -la ~/.codex
```

---

# 4. Revisar si existe AGENTS.override.md

Antes de crear `AGENTS.md`, comprobar:

```bash
ls -la ~/.codex/AGENTS*
```

Si no existe ningún archivo, continuar.

Si existe:

```text
~/.codex/AGENTS.override.md
```

y no se utiliza intencionalmente, realizar una copia antes de continuar:

```bash
mv ~/.codex/AGENTS.override.md ~/.codex/AGENTS.override.md.backup
```

No eliminar configuraciones anteriores sin revisarlas.

---

# 5. Crear ~/.codex/AGENTS.md

Con VS Code:

```bash
code ~/.codex/AGENTS.md
```

Si el comando `code` no está disponible:

```bash
nano ~/.codex/AGENTS.md
```

En Nano:

```text
Ctrl + O
Enter
Ctrl + X
```

---

# 6. Contenido recomendado de ~/.codex/AGENTS.md

Antes de pegarlo, reemplazar:

```text
/Users/TU_USUARIO/Projects/ai-software-factory
```

por la ruta real de AI Software Factory.

```md
# Global Development Instructions

## AI Software Factory

Utilizo un sistema reutilizable de desarrollo llamado **AI Software Factory**.

Su directorio principal es:

`/Users/TU_USUARIO/Projects/ai-software-factory`

AI Software Factory contiene metodología, templates, documentación, workflows, capability packs, ejemplos y recursos reutilizables para trabajar con proyectos nuevos y existentes.

No copies automáticamente toda la Factory dentro de cada proyecto.

Carga únicamente los recursos de la Factory necesarios para la tarea actual.

---

## Principio principal

La Factory debe adaptarse al proyecto.

El proyecto no debe modificarse innecesariamente para adaptarse a la Factory.

### Proyectos existentes

- respetar el stack actual;
- respetar la arquitectura existente;
- respetar las convenciones actuales;
- integrar antes que migrar;
- no reemplazar tecnologías que funcionan sin evidencia concreta;
- no introducir SaaS, multi-tenancy, billing u otras capacidades si el negocio no las necesita.

### Proyectos nuevos

- preferir soluciones simples;
- comenzar con arquitectura mínima suficiente;
- evitar infraestructura prematura;
- incorporar complejidad únicamente cuando exista una necesidad comprobada.

---

## Fuente de verdad

El repositorio del proyecto actual es siempre la fuente de verdad sobre:

- código;
- arquitectura;
- requerimientos;
- decisiones aprobadas;
- estado del trabajo;
- reglas de negocio;
- convenciones específicas.

AI Software Factory proporciona procedimientos y templates, pero no debe sobrescribir silenciosamente decisiones específicas del proyecto.

El historial del chat no es fuente de verdad persistente.

Las decisiones que deban sobrevivir a una sesión deben quedar documentadas en el repositorio correspondiente.

---

## Al trabajar en un proyecto

Antes de realizar cambios significativos, buscar cuando existan:

1. `AGENTS.md`
2. `PROJECT_PROFILE.md`
3. `PROJECT_STATE.md`
4. `CAPABILITY_MAP.md`
5. documentación relevante dentro de `docs/`
6. `docs/requirements/<ticket>/STATE.md` cuando exista un requirement activo
7. skills específicas dentro de `.agents/skills/`

No leer documentación innecesaria.

Cargar únicamente el contexto que pueda cambiar la decisión o implementación actual.

---

## AI Software Factory en proyectos existentes

Si un proyecto existente todavía no fue adoptado por AI Software Factory, no modificar código durante el discovery inicial.

Primero comprender:

- propósito del producto o sistema;
- modelo de negocio;
- stack;
- arquitectura;
- repositorio;
- base de datos;
- APIs;
- autenticación;
- testing;
- deployment;
- integraciones;
- convenciones;
- capacidades existentes.

Cuando corresponda, generar o actualizar:

- `PROJECT_PROFILE.md`
- `PROJECT_STATE.md`
- `CAPABILITY_MAP.md`
- `AGENTS.md`

Clasificar capacidades mediante:

- `KEEP`
- `ADD`
- `WRAP`
- `IMPROVE`
- `REPLACE_LATER`
- `IGNORE`

No proponer reescrituras completas salvo que exista evidencia concreta que las justifique.

---

## Requirements

Los trabajos que requieran planificación deben persistirse bajo:

`docs/requirements/<TICKET-O-SLUG>/`

El flujo general de AI Software Factory es:

Requirement  
→ Acceptance Criteria  
→ Decision  
→ Technical Plan  
→ Plan Review  
→ Slices  
→ Implementation  
→ Implementation Review  
→ Closure

Aplicar este flujo proporcionalmente.

Cambios triviales no deben recibir la misma documentación ni testing que cambios críticos.

---

## Skills

Las skills globales reutilizables se encuentran en:

`~/.agents/skills/`

Las skills específicas de cada proyecto pueden encontrarse en:

`.agents/skills/`

Usar skills bajo demanda.

No cargar ni ejecutar todas las skills disponibles por defecto.

Priorizar cuando correspondan:

- debugging sistemático para bugs, regresiones y fallos;
- desarrollo basado en fuentes oficiales cuando una decisión dependa de versiones actuales de frameworks, SDKs o APIs;
- diseño de APIs cuando se creen o modifiquen contratos;
- análisis arquitectónico únicamente cuando exista una decisión arquitectónica real;
- seguridad especializada cuando el riesgo o requerimiento lo justifique;
- análisis de tokens únicamente cuando exista un problema real de costo o contexto.

Las skills específicas del proyecto tienen prioridad para procedimientos propios de ese proyecto.

---

## Debugging

Ante bugs, regresiones, tests fallidos o comportamiento inesperado:

1. investigar la causa raíz;
2. reproducir cuando sea posible;
3. reunir evidencia;
4. revisar cambios recientes;
5. formular una hipótesis;
6. probar el cambio mínimo;
7. corregir la causa y no solamente el síntoma.

No realizar cambios especulativos sucesivos sin evidencia.

---

## Testing

La estrategia de pruebas debe ser proporcional al riesgo y alcance.

No exigir automáticamente:

- regresión completa;
- end-to-end;
- performance;
- seguridad;
- carga;
- concurrencia;

si no existe un riesgo concreto relacionado.

Cuando el proyecto o requirement defina un perfil de testing aprobado, respetarlo.

---

## Evidence Before Completion

Nunca declarar que algo está:

- terminado;
- corregido;
- funcionando;
- compilando;
- aprobado;
- con tests exitosos;

sin evidencia reciente que respalde la afirmación.

Antes de finalizar una implementación:

1. identificar qué validación demuestra que el trabajo funciona;
2. ejecutar las verificaciones necesarias cuando el entorno lo permita;
3. revisar sus resultados;
4. registrar evidencia relevante;
5. actualizar el estado correspondiente.

La confianza del agente no sustituye evidencia.

---

## Git

Mantener el trabajo enfocado y revisable.

Preferir:

- una branch por trabajo cuando corresponda;
- commits pequeños y coherentes;
- mensajes de commit descriptivos;
- Pull Requests para cambios relevantes;
- `main` estable.

No crear worktrees por defecto.

Usarlos únicamente cuando el aislamiento o el trabajo paralelo aporte valor real.

No realizar operaciones Git destructivas sin necesidad y autorización correspondiente.

---

## Simplicidad

Evitar sobreingeniería.

No introducir automáticamente:

- microservicios;
- event-driven architecture;
- nuevas bases de datos;
- nuevas dependencias;
- RAG;
- vector databases;
- multi-agent orchestration;
- nuevos proveedores cloud;
- abstracciones genéricas;
- sistemas de plugins;
- caches;
- queues;

si el problema actual no los necesita.

Preferir la solución mínima que:

1. cumpla el requerimiento;
2. mantenga una base mantenible;
3. permita escalar cuando aparezca una necesidad real.

---

## Herramientas externas

Distinguir:

**Skill**
= define cómo realizar correctamente un procedimiento.

**MCP / Tool**
= permite consultar o actuar sobre sistemas externos.

Usar herramientas externas para verificar información cuando aporten evidencia real.

No introducir un MCP o servicio solamente porque esté disponible.

---

## Prioridad de instrucciones

Seguir esta prioridad:

1. instrucciones específicas del usuario para la tarea actual;
2. instrucciones específicas del proyecto;
3. decisiones y requirements aprobados del proyecto;
4. skills específicas del proyecto;
5. estas instrucciones globales;
6. recomendaciones genéricas de AI Software Factory.

Cuando una recomendación genérica contradiga una convención válida del proyecto existente, respetar la convención del proyecto salvo que el requerimiento exija cambiarla.
```

---

# 7. Verificar el archivo

Mostrar el contenido:

```bash
cat ~/.codex/AGENTS.md
```

Mostrar solo el inicio:

```bash
head -30 ~/.codex/AGENTS.md
```

Verificar que no esté vacío:

```bash
wc -c ~/.codex/AGENTS.md
```

---

# 8. Reiniciar Codex

Si Codex estaba abierto, cerrar la sesión y volver a iniciarla.

Ejemplo:

```bash
cd ~/Projects/algun-proyecto
codex
```

---

# 9. Verificar que Codex reconoce AI Software Factory

Dentro de Codex preguntar:

```text
Resumí las instrucciones globales de desarrollo que tenés cargadas.
No modifiques ningún archivo.
```

Debería mencionar conceptos como:

- AI Software Factory;
- PROJECT_PROFILE;
- PROJECT_STATE;
- CAPABILITY_MAP;
- requirements;
- evidence before completion;
- simplicidad;
- skills bajo demanda.

Después realizar una prueba adicional:

```text
¿Dónde está ubicada AI Software Factory y qué deberías revisar antes de modificar este proyecto?
No realices cambios.
```

Codex debería:

1. conocer la ubicación de AI Software Factory;
2. priorizar el proyecto actual;
3. buscar los archivos de contexto del proyecto;
4. no copiar toda la Factory al repositorio.

---

# 10. Configuración opcional: variable de entorno

Esta parte es opcional.

Para evitar repetir una ruta absoluta en scripts futuros, se puede registrar:

```bash
echo 'export AI_SOFTWARE_FACTORY_HOME="$HOME/Projects/ai-software-factory"' >> ~/.zshrc
```

Aplicar:

```bash
source ~/.zshrc
```

Verificar:

```bash
echo $AI_SOFTWARE_FACTORY_HOME
```

Debería devolver:

```text
/Users/tu_usuario/Projects/ai-software-factory
```

## ¿Es obligatorio?

No.

Para comenzar, una ruta fija dentro de `~/.codex/AGENTS.md` es suficiente.

La variable se recomienda principalmente si:

- la Factory va a ser utilizada por scripts;
- se automatizará instalación de skills;
- se crearán comandos propios más adelante;
- se quiere evitar hardcodear paths en distintos lugares.

---

# 11. Skills globales

Las skills reutilizables deberían estar disponibles desde:

```text
~/.agents/skills/
```

Ejemplo:

```text
~/.agents/skills/
├── systematic-debugging/
├── source-driven-development/
├── api-and-interface-design/
├── architecture-decision-framework/
├── token-optimization/
├── using-git-worktrees/
├── project-discovery/
├── requirement-state/
├── context-scout/
├── impact-analysis/
├── test-strategy/
├── plan-reviewer/
├── slice-executor/
├── implementation-reviewer/
└── closure-evidence/
```

No todas deben ejecutarse siempre.

Codex debe utilizarlas según la tarea.

---

# 12. Fuente de las skills

Se recomienda que las skills mantenidas por AI Software Factory vivan originalmente en:

```text
~/Projects/ai-software-factory/skills/
```

Ejemplo:

```text
ai-software-factory/
└── skills/
    ├── project-discovery/
    ├── plan-reviewer/
    └── requirement-state/
```

Para evitar duplicados, se pueden utilizar enlaces simbólicos desde:

```text
~/.agents/skills/
```

hacia las skills de la Factory.

Ejemplo:

```bash
mkdir -p ~/.agents/skills
```

Luego:

```bash
ln -s \
"$HOME/Projects/ai-software-factory/skills/project-discovery" \
"$HOME/.agents/skills/project-discovery"
```

Y lo mismo para las demás.

## Antes de crear un symlink

Comprobar si ya existe:

```bash
ls -la ~/.agents/skills/project-discovery
```

No sobrescribir archivos existentes sin revisarlos.

---

# 13. Skills específicas del proyecto

Las reglas particulares de cada proyecto deben vivir dentro del propio repositorio:

```text
proyecto/
└── .agents/
    └── skills/
```

Ejemplo:

```text
micam/
└── .agents/
    └── skills/
        ├── project-business-rules/
        ├── project-api-conventions/
        └── legacy-migration/
```

Estas skills contienen conocimiento que no tiene sentido aplicar globalmente.

Ejemplos:

- reglas de negocio;
- convenciones particulares de APIs;
- proceso de releases propio;
- restricciones de una base legacy;
- flujos de migración;
- compatibilidad con clientes anteriores.

---

# 14. Qué debe quedar dentro de cada proyecto

AI Software Factory completa no debe copiarse dentro de cada repositorio.

La capa recomendada es:

```text
proyecto/
│
├── AGENTS.md
├── PROJECT_PROFILE.md
├── PROJECT_STATE.md
├── CAPABILITY_MAP.md
│
├── .agents/
│   └── skills/
│       └── skills específicas, si existen
│
├── docs/
│   ├── architecture/
│   ├── decisions/
│   └── requirements/
│
└── código del proyecto
```

---

# 15. Adopción de un proyecto existente

Abrir el proyecto:

```bash
cd ~/Projects/proyecto-existente
codex
```

Luego indicar:

```text
Inicializá AI Software Factory en este proyecto existente.

No modifiques código ni arquitectura durante esta etapa.

Realizá Project Discovery y genera, cuando corresponda:

- AGENTS.md
- PROJECT_PROFILE.md
- PROJECT_STATE.md
- CAPABILITY_MAP.md

Respetá el stack y las convenciones existentes.
Integrá antes que migrar.
```

El objetivo es entender primero y modificar después.

---

# 16. Creación de un proyecto nuevo

Abrir el directorio donde se creará:

```bash
cd ~/Projects
codex
```

Indicar:

```text
Quiero crear un proyecto nuevo usando AI Software Factory.

Comenzá por Product/Project Discovery.

No implementes todavía.

Necesito primero definir:

- tipo de proyecto;
- problema;
- usuarios;
- mercado;
- capacidades;
- restricciones;
- stack recomendado;
- nivel de complejidad inicial.
```

Si corresponde utilizar un starter, AI Software Factory puede consultarlo desde su directorio central.

---

# 17. Trabajo diario con requirements

Cuando existe un ticket:

```text
PROJ-123
```

el proyecto puede persistirlo como:

```text
docs/requirements/PROJ-123/
├── STATE.md
├── 00_REQUIREMENT.md
├── 01_ACCEPTANCE_CRITERIA.md
├── 02_DECISION.md
├── 03_PLAN.md
├── 04_PLAN_REVIEW.md
├── slices/
├── 05_IMPLEMENTATION_REVIEW.md
└── 06_CLOSURE.md
```

No todos los cambios necesitan todos los archivos.

Aplicar proporcionalidad.

Para cambios triviales o muy pequeños, utilizar una versión compacta.

---

# 18. Reanudar trabajo sin depender del chat

En una sesión nueva:

```bash
cd ~/Projects/proyecto
codex
```

Luego:

```text
Continuá PROJ-123.

Leé primero:

- PROJECT_STATE.md
- docs/requirements/PROJ-123/STATE.md

Después cargá únicamente el contexto necesario para continuar desde la próxima acción pendiente.
```

No es necesario pegar la conversación anterior.

---

# 19. Qué no debe hacer esta configuración

No utilizar AI Software Factory como excusa para:

- migrar proyectos;
- reescribir sistemas;
- agregar frameworks;
- instalar herramientas;
- crear microservicios;
- crear agentes;
- incorporar SaaS;
- cambiar bases de datos;
- aumentar testing;

sin una necesidad real.

La Factory existe para reducir complejidad, no para agregarla.

---

# 20. Arquitectura final recomendada

```text
                         TU MAC
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
 ~/.codex/AGENTS.md   ~/.agents/skills   AI Software Factory
          │                │                │
          │                │        metodología/templates
          │                │        skills/starters/docs
          │                │                │
          └────────────────┼────────────────┘
                           │
                         CODEX
                           │
                           ▼
                    PROYECTO ACTUAL
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          AGENTS.md   PROJECT_STATE   Requirements
              │            │            │
              └────────────┼────────────┘
                           ▼
                     implementación
```

---

# 21. Principios que no deberían cambiar

## 1. La Factory se adapta al proyecto

Nunca al revés.

## 2. El repositorio es la fuente de verdad

El chat no reemplaza documentación persistente.

## 3. Las skills se cargan bajo demanda

No ejecutar todas por defecto.

## 4. La evidencia está antes que la afirmación

No declarar trabajo terminado sin verificarlo.

## 5. Integrar antes que migrar

Especialmente en proyectos existentes.

## 6. Complejidad bajo demanda

No diseñar hoy para problemas hipotéticos de mañana.

## 7. Un único lugar para cada responsabilidad

- reglas globales → `~/.codex/AGENTS.md`
- procedimientos reutilizables → `~/.agents/skills/`
- metodología → `ai-software-factory/`
- conocimiento del proyecto → repositorio del proyecto
- estado de una tarea → `docs/requirements/<ticket>/STATE.md`

---

# 22. Checklist final de instalación

```text
[ ] AI Software Factory está en una ubicación permanente.
[ ] ~/.codex/ existe.
[ ] ~/.codex/AGENTS.md fue creado.
[ ] La ruta de AI Software Factory es correcta.
[ ] Codex reconoce las instrucciones globales.
[ ] ~/.agents/skills/ existe.
[ ] Las skills globales necesarias están disponibles.
[ ] Las skills de Factory no están duplicadas innecesariamente.
[ ] Los proyectos almacenan solamente su contexto específico.
[ ] Un proyecto existente puede adoptarse sin modificar su stack.
[ ] Una nueva sesión puede reanudar requirements sin depender del chat.
```

---

# 23. Siguiente paso recomendado

Después de configurar `~/.codex/AGENTS.md`, el siguiente paso es instalar o enlazar las skills globales de AI Software Factory dentro de:

```text
~/.agents/skills/
```

Luego probar la Factory sobre:

1. un proyecto existente;
2. un proyecto nuevo pequeño.

No automatizar más cosas hasta comprobar qué partes del workflow realmente ahorran tiempo.
