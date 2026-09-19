# Crear un proyecto nuevo

## 1. Directorio

```bash
mkdir mi-proyecto
cd mi-proyecto
```

## 2. Inicializar Factory

```bash
/ruta/ai-software-factory/scripts/init-project.sh --git-init
```

## 3. Discovery

```bash
codex
```

Prompt:

```text
Quiero crear un proyecto nuevo usando AI Software Factory.

Comenzá por Project Discovery.

No implementes todavía.

Definí:
- problema;
- usuarios;
- producto;
- mercado;
- restricciones;
- capacidades necesarias;
- opciones importantes.
```

## 4. SaaS

Si es SaaS, activar solo las capacidades necesarias.

No instalar automáticamente:

- Stripe;
- Supabase;
- Clerk;
- Mercado Pago;
- Sentry;
- analytics.

El proveedor se decide según mercado, país, entidad legal, requerimientos y stack.

Un starter SaaS puede existir en otro repositorio Template, pero no forma parte obligatoria de Factory.
