# D01 — clasificación automática con atribución conservadora

**Aprobada junto al plan v2 el 2026-09-25.** La autorización de ejecución cubrió
solo A01–A03 offline; A04/A05 mantienen permisos propios.

Combinar un productor prospectivo de evidencia de acciones, el clasificador Kev
local y un agregador que reconcilia contadores nativos. Cada componente responde
una pregunta distinta: qué ocurrió, a qué actividad pertenece y cuánto consumo
puede vincularse. La categoría puede ser inferida aunque el contador sea observado.

Reutilizar binding, ledger privado, lock, transacciones y snapshots del observador.
Agregar modo histórico por actividades sin categoría global obligatoria. Conservar
el contrato de `suggest-kind` v1 y añadir un clasificador multiactividad separado.
No reemplazar router ni launcher ni introducir servicios remotos.

| Alternativa | Decisión |
|---|---|
| D01: acciones prospectivas + Kev + contadores por ID | Recomendada: permite tareas mixtas y expone cobertura real. |
| Clasificar una sola vez la tarea | Rechazada por el usuario: oculta documentación y pruebas dentro de una feature. |
| Repartir tokens según probabilidades de Kev o líneas editadas | Rechazada: confunde clasificación con medición. |
| Clasificar todo el log retrospectivamente | Excluida: contradice alcance prospectivo y permisos. |
| Usar solo extensión de archivo | Insuficiente: un mismo archivo puede recibir una feature o un fix; explicación no necesita archivo. |

Kev es parte del diseño objetivo; su aprobación operativa depende de la evaluación
A04. Mientras esté ausente o sin validar, reglas explícitas pueden reconocer
acciones inequívocas y el resto queda sin clasificar. Eso es funcionamiento
degradado, no evidencia de que Kev esté integrado o sea preciso.

Persistir IDs/digests y resultados estructurados, no texto de conversación ni
diffs. El resumen breve del objetivo/acción se genera durante la ejecución futura
por el agente que ya conoce la tarea, se trata como evidencia declarada y no se
extrae de logs históricos. Las rutas se proyectan a roles para la consulta Kev.

La fuente real y la disponibilidad de eventos vinculables del host siguen sin
verificar. Si no existen eventos utilizables en el flujo local permitido, detener
la integración viva y presentar esa limitación; no inventar hooks ni IDs.

## D12-AUTH — A2 seleccionada para el preflight OTel v1.2-r2

**Aprobación humana:** 2026-09-28, mediante la instrucción explícita «selecciono
A2 para D12-AUTH del contrato OTel v1.2-r2» con las condiciones siguientes.

- **Fuente:** login interactivo realizado directamente por el usuario dentro del
  mismo Codex temporal iniciado bajo herdr.
- **Almacenamiento:** `ephemeral`; las credenciales permanecen únicamente en
  memoria durante la vida de ese proceso.
- **Comprobación:** `/usage` dentro de ese mismo Codex, sin enviar una tarea. La
  evidencia persistida se reduce al `AUTH_OK` permitido por el contrato:
  versión, A2, clase `interactive_ephemeral`, `authenticated=true`, referencia
  digerida del hijo, instante y clase de verificador.
- **Datos excluidos:** identidad, cuenta, plan, límites, importes, consumo,
  respuesta del servicio, credenciales y valores de entorno.
- **Efectos externos admitidos solo en una ejecución posterior autorizada:**
  navegador de login, red de autenticación de OpenAI y consulta de uso. No se
  autoriza inferencia, tarea, fixture o piloto; USD permanece `unknown`.
- **STOP:** proceso de login separado, credencial o `auth.json` en disco, fuente
  distinta, propagación no demostrada, `/usage` no autenticado, exposición de
  datos excluidos, cambio del estado personal o imposibilidad de reversión.

A1 y A3 quedan no seleccionadas; A0 conserva su función de control negativo y A4
sigue prohibida. Esta decisión resuelve D12-AUTH, pero no autoriza abrir pane,
Codex, navegador, login o red. El preflight H-C1–H-C4 requiere una autorización
de ejecución explícita y separada. P1–P4, la AI Strategy vigente y todos los
hallazgos y cierres anteriores permanecen intactos.
