# Integración mínima del ayudante — candidata inactiva

La Factory integra contratos, selección de contexto, entrega, auditoría y aceptación
supervisada. **Todavía no incluye un dispatcher operativo ni un piloto vivo aceptado.**
Inline sigue siendo la ruta disponible. Instalar esta candidata no habilita agentes.

CE-v1 agrega una alternativa más liviana, textual y también deshabilitada: selección
mínima de contexto, reutilización local y contrato API de un intento. No resuelve los
controles pendientes de un subagente y no los debilita. Ver
[Ahorro de contexto y ayudante textual](CONTEXT_ECONOMY_TEXT_HELPER.md).

## Alcance inicial aprobado

- U01: revisar Specs/Slices proporcionadas y señalar contradicciones o criterios faltantes.
- U02: sugerir casos de prueba con entrada, resultado esperado y criterio cubierto.

El coordinador revisa y acepta/rechaza; el ayudante no implementa ni ejecuta pruebas.
Diagnóstico de código/logs, patches, escrituras, servicios externos y paralelismo
quedan postergados. Una tarea pequeña se resuelve inline si delegarla no compensa.
Primer piloto autorizado: solo U01 sintético, un ayudante/un intento y controles
previos satisfechos. Aprobar U02 no autoriza otro ensayo vivo ni garantiza su calidad.

## Componentes y pasos

1. El coordinador aplica [Guided Delegation](GUIDED_DELEGATION.md), aprueba alcance,
   revisa contexto sintético y reutiliza EXECUTION_BRIEF y RUN.schema.json v2.
2. `config/assistant-proposal/` contiene TOML genérico inactivo, fuera de `.codex`.
   No copiarlo a HOME ni al proyecto: es una propuesta, no una instalación.
3. Comprobar estáticamente con Python >=3.11:

   ```bash
   python3 -I -B scripts/lib/check_assistant_proposal.py
   ```

   Exit **2** significa `STATIC PASS / DISABLED / NOT RUN`, no error de sintaxis
   ni autorización. Exit 1 significa propuesta inválida. No existe exit live-ready.
4. Antes de activar, verificar vínculo del rol/configuración al hijo en el runtime,
   protección del original/baseline/configuración, ausencia de herramientas externas
   mutantes y recursivas, identificación y mecanismo observable de detención.
   Comprobar inventario efectivo: TOML, parser y feature flags no lo certifican.
5. Solo si todos los controles previos están verificados y hay autorización vigente,
   persistir prepared antes del despacho. El primer piloto: **un ayudante, un intento,
   archivos sintéticos**, sin retry ni escalamiento. No iniciar un intento para
   averiguar después si tiene permisos peligrosos.
6. Observar fin, conservar entrega, auditar copia/original, verificar criterios y aceptar
   o rechazar según el contrato. Sin fin confirmado, cupo ocupado; nunca rollback del usuario.

## Compatibilidad y bloqueo conocido

Base de evaluación: Codex CLI **0.155.1**, macOS. No afirmar soporte efectivo para
otras versiones/plataformas por pasar TOML. Los campos de roles y agents.enabled
están documentados; el parser no prueba selección del rol al crear el hijo.

La interfaz de la sesión evaluada permite `spawn_agent(task_name, message,
fork_turns, model, reasoning_effort)` pero no seleccionar rol, sandbox o tool allowlist.
El runtime permite subdelegar. No hay vínculo verificable con `asf_helper.toml`.
Por eso el piloto está **NOT RUN**. No es que Codex en general carezca de roles:
es una limitación de esta interfaz comprobada, no se corrige dando instrucciones.

La prueba previa de comandos sintéticos protegió archivos en 22/22 casos; no prueba
herencia al hijo, control de Apps/MCP ni detención de agentes. No repetirla para
sustituir el control faltante. `unified_exec=true` con override false es una discrepancia
observada, no por sí misma prueba de escape o de herramienta accesible al hijo.

Los TOML solicitan read-only por prudencia. La política v2 solo promete instrucción
y auditoría de no-escritura en copia: no depende de anunciar readonly garantizado.
Las tablas MCP/plugins vacías **no eliminan integraciones heredadas**. Requieren un
entorno temporal separado y configuración efectiva revisada, sin secretos. Resolver
modelo/reasoning mediante MODEL_CATALOG; no duplicar mappings en roles.

## Próxima acción segura

Continuar inline. Para retomar la activación, pedir:

> Verificá, sin lanzar agentes ni cambiar mi configuración habitual, un runtime que
> permita seleccionar asf_helper y observar sus permisos/herramientas efectivos antes
> del primer despacho. Reutilizá la evidencia existente. No amplíes arquitectura ni
> relajes controles. Si no podés probar protección del original/configuración, ausencia
> de subdelegación y acciones externas mutantes, y mecanismo de detención, mantené
> el piloto deshabilitado e indicá el dato o capacidad exactos faltantes.

## Fuentes oficiales verificadas el 2026-09-21

- [Subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents): roles,
  agents.enabled y herencia; overrides vivos del padre pueden prevalecer sobre defaults.
- [Permisos](https://learn.chatgpt.com/docs/permissions#scope-and-enforcement):
  sandbox de comandos no gobierna Apps/MCP/browser ni tráfico del servicio.

No instalar runtimes, ampliar permisos ni habilitar herramientas como atajo.

Inspección adicional del protocolo local 0.155.1 (sin iniciar servidor ni sesión):
`thread/start` admite config/permisos y su respuesta incluye activePermissionProfile;
no equivale a configurar el spawn_agent de esta conversación. `config/read` resuelve
configuración en disco; no certifica herramientas efectivas de un hijo. No se encontró
en el esquema un método de inventario completo de herramientas nativas por hilo.
`dynamicTools: []` no debe interpretarse como deshabilitación de herramientas nativas.
Un adaptador a esta interfaz sería trabajo separado, no un control ya implementado.
