# Plan de ejecución — v1

Alcance autorizado por la petición del 2026-09-21. N2/T2 para preparación offline;
activación real sería N3 y requiere controles/review pertinentes. No se activa aquí.

1. Reusar evidencia de S01–S04 y sandbox; contrastar docs oficiales y CLI 0.155.1.
2. Integrar propuesta de ayudante inactiva y chequeo estático fail-closed, sin dispatcher.
3. Preparar 2.3.0-rc.1 en rama local: metadata, soporte prerelease en doctor, guías nuevas/upgrade y notas.
4. Validar suite, ejemplos, CLI solo parser y artefacto exportado en HOME temporal.
5. Revisar diff, preservar evidencia y estado; entregar candidata sin push/tag/publicación.

## Criterios

- C1: inline default; ninguna instalación habilita ayudantes o cambia config.toml.
- C2: configuración genérica sin IDs personales; validador no ejecuta modelos y nunca confunde sintaxis con aptitud viva.
- C3: metadata prerelease consistente; doctor compara estable/RC correctamente sin downgrade automático.
- C4: paquete excluye trials y evidencia local; instalación/upgrade temporal preservan código/configuración.
- C5: piloto máximo 1/1 exclusivamente sintético si controles previos verificables; de lo contrario NOT RUN y bloqueo concreto, nunca falsa aceptación.
- C6: ningún push/tag/publicación; cierre con tests reales y aprobación final explícita pendiente.

## Límite y rollback

Sin runtime alternativo, dispatcher nuevo, cambios a permisos habituales, recursión,
paralelismo ni debilitamiento de controles. La integración mínima es una plantilla
inactiva, protocolo y comprobador; no prometer ayudante operativo sin piloto aceptado.
Snapshot previo separado y rama local. No restaurar ni borrar trabajo humano.
La evidencia del sandbox de comandos no certifica herramientas/herencia del ayudante.

## Review del plan

Self review N2: proporcional mientras la integración siga inactiva. No lanzar un
reviewer real usando el único permiso del piloto. Review independiente del diff
recomendado antes de publicación; no puede sustituir los controles runtime faltantes.
