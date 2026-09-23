# Model routing: precisión y costo proporcional

- **Status:** completed
- **Current phase:** closure
- **Current slice:** none
- **Pending slices:** none
- **Completed:** S01; AC1–AC6; 47 tests dirigidos OK, check-release y diff --check OK. Ver EVIDENCE.md.
- **Implementation review:** approved; self review en 05_IMPLEMENTATION_REVIEW.md
- **Risk level:** N2 — reglas compartidas de workflow, sin cambios de permisos ni ejecución de modelos.
- **Acceptance criteria:** approved; 01_ACCEPTANCE_CRITERIA.md
- **Selected option:** mejora incremental del router existente.
- **Test profile:** T1 dirigido: instalación/adopción aislada, consistencia del catálogo y escenarios de política; regresión de scripts afectados.
- **Plan version:** 1
- **Plan review:** approved; self review en 04_PLAN_REVIEW.md
- **Human plan approval:** approved — petición «Ok, me parece bien apliquemoslo», sobre el paquete inicial del plan anterior.
- **Execution authorization:** approved — misma petición; fuente local, sin publicación, instalación global ni piloto multiagente.
- **Next action:** ninguna dentro de este requirement; proyecto retoma decisión de release-2-3-0-rc-1.
- **Why this is next:** alcance implementado, revisado y validado; no quedan slices.
- **User action required:** false
- **Decision required:** none
- **Expected output:** cierre consultable; publicación/instalación no forman parte de este alcance.
- **After this:** PROJECT_STATE remite a la decisión de release; su aprobación no se infiere de este cierre.
- **Blocked by:** none
- **Runtime limitation:** none
- **Resume instruction:** requirement completo; consultar EVIDENCE.md y 06_CLOSURE.md. Para el trabajo pendiente leer PROJECT_STATE y release-2-3-0-rc-1/STATE.md; no activar piloto ni publicar.

## AI Strategy

- Planning / implementation / review: BALANCED / Medium como recomendación; catálogo config/MODEL_CATALOG.md, fecha 2026-09-20. Modelo preferido GPT-5.6 Terra (gpt-5.6-terra), fallback GPT-5.6 Sol (gpt-5.6-sol) / Medium.
- Routing decision: BALANCED/Medium; selección por política; reglas y diff verificables con casos y pruebas de instalación; contexto revisado en catálogo, skills, workflows, templates e instalador; Switch Benefit LOW; sin necesidad material de verificar configuración de sesión.
- Effective session config: unknown; esta estrategia no prueba ejecución ni cambio de modelo.
- Escalation triggers: contradicción material en gates/permisos o cambio de alcance runtime.
- Downgrade: no interrumpir cierres/documentación cortos.
- Review mode: self review del diff y escenarios; no se afirma independencia ni un ensayo de comportamiento del modelo.
- No se incorporan controladores, modelos nuevos, benchmarks pagos, telemetría automática ni otro catálogo.
