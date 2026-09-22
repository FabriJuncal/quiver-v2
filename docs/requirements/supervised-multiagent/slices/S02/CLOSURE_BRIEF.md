# S02 — cierre offline

RUN.schema acepta versiones explícitas v1/v2, sin reinterpretar v1; v2 requiere
supervision, aprobación de riesgo, revisión de contexto, controles y auditorías.
Checker rechaza incidentes en entregas, contratos mezclados, manifests sin base y
aceptación sin evidencia. Unknown conserva advertencia, no READY de runtime.

Validación: 34 tests de contrato existente OK (1.341 s); 17 tests v2 OK (1.777 s).
Ejemplo v2 STATIC PASS con NO APTO PARA PILOTO. No modelos ni runtime vivo.
Corrección durante implementación: import de módulo hermano bajo Python -I;
testeado por CLI y doctor. Schema agrega solo oneOf/not para separar versiones.

La utilidad de comparación de S03 se incorporó como dependencia mínima de S02;
su verificación filesystem dedicada continúa en S03. No cambia orden de aceptación.
Continúa S03 autorizada, sin intervención humana.
