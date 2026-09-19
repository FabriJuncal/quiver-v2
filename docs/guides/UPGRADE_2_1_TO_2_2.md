# Upgrade 2.1 → 2.2 — AI Model Routing

La versión 2.2 agrega routing de modelos por perfiles sin cambiar el workflow base.

## 1. Actualizar Factory

Reemplazar/actualizar el repositorio y volver a ejecutar:

```bash
./scripts/install.sh
./scripts/doctor.sh
```

El instalador actualiza solamente el bloque administrado de `~/.codex/AGENTS.md` y mantiene el resto.

## 2. Proyectos nuevos

No requieren migración.

`init-project.sh` ya crea `PROJECT_PROFILE.md` con `AI Policy`.

## 3. Proyectos existentes ya adoptados

No reemplazar sus archivos con templates vacíos.

Abrir Codex en el proyecto y usar:

```text
Actualizá únicamente la capa de AI Software Factory de este proyecto para adoptar AI Model Routing 2.2.

No modifiques código de aplicación, arquitectura, producto, criterios aprobados ni decisiones existentes.

Conservá toda la información actual.

Agregá/completá:

1. En PROJECT_PROFILE.md:
   - AI Policy
   - default profile
   - priorities quality/speed/cost
   - default reasoning
   - escalation policy
   - review independence

2. En cada requirement activo STATE.md:
   - AI Strategy
   - planning profile/reasoning
   - implementation default profile/reasoning
   - review profile/reasoning
   - escalation triggers
   - downgrade opportunities

3. En slices pendientes/no ejecutadas:
   - AI Execution Profile dentro de EXECUTION_BRIEF.md
   - profile
   - reasoning
   - why
   - escalate if
   - downgrade after

No reescribas slices ya cerradas solamente para completar metadata histórica.

Resolvé perfiles concretos utilizando el catálogo actual de AI Software Factory.

Después mostrame:
- AI Policy del proyecto;
- AI Strategy del requirement activo;
- perfiles sugeridos para slices pendientes.
```

## 4. Verificación

En Factory:

```bash
./scripts/doctor.sh
```

En proyecto:

```bash
/ruta/ai-software-factory/scripts/doctor.sh --project .
```

## 5. Qué NO cambia

- Guided Mode;
- Decision Boundaries;
- T1/T2/T3;
- aprobación de criterios;
- Plan Review;
- Implementation Review;
- SOURCE OF TRUTH;
- stack del proyecto.

AI Model Routing es una capa de recomendación y persistencia, no un orquestador automático.
