# Próximo piloto — PROPUESTO, NO AUTORIZADO / NOT RUN

S01–S04 implementan contratos y validación offline, no dispatcher ni configuración
de permisos. Su cierre no activa la copia del preflight anterior ni autoriza workers.

## Próximo paso recomendado antes de lanzar

Revisión dedicada del diff crítico y evaluación del runtime disponible bajo la
política nueva. Evaluar riesgo de activación por separado (N3 si cambia autorizaciones
reales) y aplicar workflow 08. Ningún agente/reviewer se lanza por leer este archivo.

Controles pendientes: proteger original/baseline/configuración habitual, impedir
acciones externas mutantes y subdelegación, observar identidad y fin. Usar evidencia
actual del cliente, no hashes/booleans ni la declaración del hijo. La lectura de código
o documentación puede orientar una propuesta, pero no certifica conducta viva.
La instrucción de no escribir en la copia sí admite supervisión según política v2.

Si algún control restante no puede verificarse, mantener delegación deshabilitada y
explicar el faltante. No pedir Full Access ni repetir preflights sin nueva evidencia.
Seguir inline para trabajo autorizado independiente. No reinterpretar esta propuesta
como aceptación de otro riesgo ni como permiso para modificar configuración habitual.

## Ensayo posterior, solo con autorización específica y preflight suficiente

- Una copia sintética allowlisted, sin secretos/config personal; no el proyecto real.
- Un ayudante, un encargo de análisis, un intento, sin retry ni escalamiento automático.
- Modelo recomendado resuelto con catálogo al ejecutar; efectivo unknown hasta observar.
- Registrar prepared, ID observado, manifest de copia/alcance original y contexto revisado.
- Entrega textual acotada; confirmar fin, inventariar de nuevo, comparar y revisar criterios.
- Si hay incidente, preservar evidencia/rechazar, no restaurar el original ni borrar copia.
- Medir solo tiempo/retrabajo/consumo observable. Nada de porcentajes o ahorro inventados.
- Continuar siguiente acción autorizada; al terminar, indicar resultado y próximo paso.

No probar cancelación hostil, fallos inducidos ni publicación dentro de este primer
ensayo. Un ID o respuesta final no bastan por sí solos para probar detención de toda
actividad externa. No prometer un límite monetario duro no disponible.

Prompt recomendado para la próxima evaluación, todavía sin ayudantes:

> Revisá los controles pendientes para un piloto de Factory multiagente supervisada
> siguiendo LIVE_PILOT_PROPOSAL.md de supervised-multiagent. Reutilizá la evidencia
> existente y buscá solo lo que falta. No lances agentes, no cambies mi configuración
> ni publiques. Indicá si existe una ruta verificable para el piloto y su autorización exacta.

Publicar una release es otra tarea: preparar rama/versión/paquete, excluir la copia
de configuración personal de prueba y validar instalación/CI del artefacto final.
Hasta piloto aceptado, no anunciar multiagente operativo ni ahorro demostrado.
