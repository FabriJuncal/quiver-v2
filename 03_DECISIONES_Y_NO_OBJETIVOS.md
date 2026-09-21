# Decisiones y no objetivos

## Decisiones

- El core funciona sin Obsidian, Graphify, CBM, Stripe o Supabase.
- Skills globales: pocas y de alto retorno.
- Skills del proyecto: capturan reglas propias, no tutoriales.
- Worktrees y parallel agents son opt-in.
- Delegación guiada secuencial: opt-in separado, un worker read-only/proponente y
  coordinador único; [contrato](docs/guides/GUIDED_DELEGATION.md). Inline sigue default.
  Implementar/probar ese soporte offline no autoriza lanzar workers reales.
- TDD no es una regla universal.
- Verification-before-completion se absorbe como regla del core.
- Code review externo no se instala si duplica Implementation Reviewer.
- Documentation/ADRs se absorbe en la arquitectura documental del core.

## No objetivos de V2

- Crear un CLI `factory`.
- Construir un orquestador multi-agent.
- Crear RAG/Vector DB propios.
- Crear una plataforma de memoria.
- Reemplazar GitHub/Linear/Jira.
- Crear un sistema de billing propio.
- Crear un framework de abstracciones para todos los proveedores.
- Reescribir proyectos existentes.
