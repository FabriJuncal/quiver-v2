# Explicación completa del proyecto

## Qué es AI Software Factory

AI Software Factory es un método reutilizable para trabajar con IA sobre cualquier proyecto de software. Puede ayudar a crear proyectos nuevos y a adoptar proyectos existentes con stacks y modelos de negocio diferentes.

No es un framework, un SaaS starter obligatorio ni una plataforma multi-agent.

Su núcleo es:

```text
Repositorio + Markdown + Codex + Skills + Git + verificaciones
```

## Qué conserva del diseño original

Se mantiene todo el flujo diseñado al principio:

- clasificación proporcional;
- criterios de aceptación;
- opciones comparables;
- selección de testing;
- plan técnico;
- Plan Reviewer independiente;
- slices;
- implementation reviewer;
- evidencia de cierre;
- `STATE.md` como memoria operativa;
- selección de perfiles de IA por etapa;
- reducción de tokens mediante contexto progresivo.

## Dos modos

### NEW PROJECT

La Factory puede recomendar defaults sencillos, starters y capability packs.

### EXISTING PROJECT

La Factory hace discovery y conserva lo existente salvo que haya una razón concreta para cambiarlo.

## Tipos de proyecto soportados

- SaaS.
- Aplicaciones web.
- Aplicaciones móviles.
- APIs y backends.
- Sistemas internos.
- E-commerce.
- Plataformas/marketplaces.
- Automatizaciones.
- Productos de IA.
- Data/ETL/reporting.
- Desktop.
- Juegos.
- IoT.
- Legacy.

## Las tres memorias del sistema

### 1. Memoria permanente del proyecto

```text
PROJECT_PROFILE.md
CAPABILITY_MAP.md
docs/architecture/
docs/decisions/
```

### 2. Estado actual

```text
PROJECT_STATE.md
```

### 3. Estado del requerimiento

```text
docs/requirements/<ticket>/STATE.md
```

El chat no es fuente de verdad.

## Jerarquía de verdad

1. Código y datos reales.
2. Requirements aprobados.
3. ADR/decisiones aprobadas.
4. PROJECT_PROFILE.
5. PROJECT_STATE.
6. Documentación del repositorio.
7. Índices derivados como Graphify/Codebase Memory.
8. Memoria del modelo.
9. Chat.

## Skills

La Factory distingue:

- skills globales de desarrollo;
- skills propias de la Factory;
- skills específicas del proyecto;
- capability packs.

Una skill propia solo se crea si captura un procedimiento o regla que se repite. No se crea para explicar una tecnología genérica.

## MCP y herramientas

Skill = sabe cómo trabajar.

MCP/Tool = puede consultar o hacer algo externo.

Ejemplos:

```text
api-interface-design + GitHub MCP
Impeccable + Browser DevTools
billing rules + Stripe/MercadoPago
DB safety + DB MCP
```

## Starter SaaS

Existe como opción para nuevos SaaS. No forma parte del core de la Factory y nunca se aplica a un proyecto existente.

## Argentina

La Factory no obliga a usar proveedores no disponibles localmente. Los pagos se deciden según mercado y situación legal. La región de infraestructura se decide según usuarios y datos, no solo según ubicación del desarrollador.

## Principio de simplicidad

> Agregar complejidad únicamente después de observar una necesidad concreta.
