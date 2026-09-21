# Validación propuesta — T2 focalizado

Matriz de diseño conservada. Ejecución offline y límites de cobertura registrados
en [IMPLEMENTATION_EVIDENCE.md](IMPLEMENTATION_EVIDENCE.md); no confundir con prueba viva.

Esta matriz especifica pruebas futuras, no resultados ejecutados. Para evidencia
del diseño actual consultar EVIDENCE.md. Fixtures temporales, Codex simulado y sin
tokens pagos. Nunca usar configuración personal como destino de tests.

| ID | Entrada / evento | Resultado exigido |
|---|---|---|
| V01 | Proyecto legacy sin opt-in/runs | Inline válido; cero metadatos nuevos obligatorios o escrituras de doctor |
| V02 | Trabajo inline autorizado, usuario false | Ejecutar próxima acción; sin gate artificial de delegación/modelo |
| V03 | Worker intenta editar STATE o continuar otra slice | No aceptar operación; mantener autoridad central y registrar incumplimiento |
| V04 | Worker running o coordinador anterior sin reconciliar | No segundo despacho, ni takeover basado solo en antigüedad |
| V05 | Dependencia pendiente o falta autorización; override manual | No despachar; explicar condición, alternativa y acción exacta |
| V06 | Dependencia submitted o intento accepted parcial | No liberar dependiente hasta slice completed o criterio parcial expresamente autorizado y aceptado |
| V07 | IDs inexistentes/ciclo/ruta ../ externa/symlink externo | Error guiado antes de leer fuera de scope o ejecutar; cero escrituras |
| V08 | Context manifest con spec/slice/decisiones/archivos mínimos | Referencias/revisión comprobables; no agregar transcript completo |
| V09 | Entrada requiere contexto extra o contiene secretos/instrucciones externas | Ampliación justificada; redacción/exclusión; datos no elevan autoridad |
| V10 | Mensaje DONE sin entrega/validaciones, proceso aún activo o tests NOT RUN | No submitted sin fin confirmado; no accepted/completed sin verificación; conservar pendientes |
| V11 | Patch permitido y criterios cubiertos | Aplicación por coordinador; pruebas sobre resultado integrado antes de accepted |
| V12 | Base modificada o cambio fuera de scope | Rechazar integración ciega; reconciliar alcance/base y preservar cambios ajenos |
| V13 | Caída entre prepared/spawn/registro de ID | Buscar ejecución existente; si unknown no relanzar; limitación/resume concreto |
| V14 | Pause/cancel solicitado; stop no confirmado | No afirmar cancelled ni reasignar; checkpoint observable y guía exacta |
| V15 | Entrega repetida/ID viejo/digest conflictivo/caída tras aplicar | No doble aplicación; reconciliar diff; ignorar resultado reemplazado para aceptación |
| V16 | Tercer intento o cambio de sesión/modelo para resetear contador | No ejecutar; escalación con motivo y presupuesto nuevo explícito |
| V17 | Worker intenta crear worker; review_at vencido | Rechazar recursión; comprobar progreso sin inventar timeout o parada |
| V18 | Perfil solicitado difiere de config; modelo observado ausente | Mostrar distinción/unknown; no persistir modelo activo como verdad del proyecto |
| V19 | Configuración custom contradice spawn o permisos requeridos no comprobables | No fingir capacidad/sandbox; inline suficiente o boundary por runtime |
| V20 | Runtime ausente, rechazo de override o presupuesto agotado | Acción concreta, motivo, pendientes y respuesta simple; continuar trabajo seguro independiente |
| V21 | JSON inválido, enum desconocido, referencia ausente, estado terminal reabierto | Checker falla con causa guiada; no modifica proyecto |
| V22 | Ejemplos/schema/validador divergen o doctor se ejecuta dos veces | Tests detectan deriva; diagnóstico idempotente/read-only |
| V23 | Instalación/adopción/perfiles/launcher legacy | Suite existente continúa pasando, incluidos paths con espacios y preservación |

## Qué se automatiza y qué no

P02 automatiza estructura, referencias, transición propuesta y límites verificables
offline. P03 ejercita decisiones del procedimiento con walkthroughs/fixtures de
eventos: eso no demuestra obediencia real de un modelo. P04 reporta ambos niveles
por separado. No fabricar un test de strings y llamarlo garantía de continuidad.

Experimento vivo futuro: solo tras autorización explícita, capacidad observada y
presupuesto. Debe incluir pérdida de contexto, cierre/reanudación y una cancelación
segura para comprobar comportamiento real. Si no se ejecuta, queda NOT RUN.
