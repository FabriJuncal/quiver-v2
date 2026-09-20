# Cierre prematuro con trabajo pendiente

Síntoma: S04 cerrada, S05 activa, respuesta final «ACCIÓN DEL USUARIO: ninguna» o recap sin pendientes.

En el proyecto ejecutá `"$ASF_ROOT/scripts/doctor.sh" --project .`. Luego en Codex pegá:

```text
Reanudá desde PROJECT_STATE.md y el STATE del requirement activo.
Contrastá con evidencia real. Si Conversation Recap dice sin pendientes pero hay una slice
activa, ignorá el recap y registrá la inconsistencia. Aplicá Finalization Gate del contrato
canónico y ejecutá Next action en este mismo turno si está autorizada y el runtime lo permite.
Si existe una limitación real, persistí tipo, causa, pendiente y reanudación exacta.
```

No editar el recap del runtime ni declarar cierre por su contenido. Si el agente no puede escribir
estado, pedir el patch de recuperación y aplicarlo tras revisar. Ver [Runtime Guardrails](../guides/RUNTIME_GUARDRAILS.md).
