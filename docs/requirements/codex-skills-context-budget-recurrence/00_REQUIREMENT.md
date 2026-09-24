# Recurrencia del warning de Skills context budget

## Problema observado

El usuario informó nuevamente el warning:

> Skill descriptions were shortened to fit the skills context budget.

La revisión anterior había cerrado sin reproducción estable. Esta recurrencia es
evidencia nueva y habilita un diagnóstico N2 separado.

## Objetivo

Capturar una línea base previa, reproducir una sola vez con Codex CLI, comparar
configuración, catálogo, procesos y metadata de plugins, y preparar únicamente
una corrección mínima reversible si la causa queda atribuida.

## Límites autorizados

- Diagnóstico de lectura y una reproducción controlada.
- Se pueden crear artefactos de evidencia en este requirement.
- No modificar Skills, `~/.codex/config.toml`, plugins ni backups.
- No aplicar una corrección sin aprobación humana posterior.

## Criterios

1. Captura previa completa antes de la reproducción.
2. Una sola reproducción y salida preservada en forma resumida, sin secretos.
3. Comparación antes/después por hash, mtime, conteo y catálogo.
4. Hechos separados de inferencias.
5. Candidato de corrección solo si existe causa atribuida y reproducible.
