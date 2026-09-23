# Release Checklist

Target: AI Software Factory v2.3.0-rc.2 — Supervised Delegation Preview. No confundir validación local con publicación.

Esta checklist es para autorización final, no una declaración de checks ejecutados.
Resultados reales viven en el requirement de release. Piloto NOT RUN: no publicar
como multiagente operativo. La preview offline necesita aprobación explícita de alcance.

- [ ] Controles efectivos del hijo verificados antes del primer spawn; piloto 1/1 aceptado si se anuncia operativo.
- [ ] Configuración del ayudante permanece inactiva; instalador no la copia ni cambia config.toml.
- [ ] Chequeo de propuesta exit 2 esperado, nunca presentado como live-ready.
- [ ] Prerelease RC reconocida por doctor y estable posterior sin downgrade.
- [ ] No copiar trials locales, credenciales ni evidence privada a Git/ZIP.

- [ ] `bash scripts/check-release.sh`: versiones, archivos, mappings, instrucciones y rutas.
- [ ] Launcher: cuatro dry-runs, argv literal, espacios, Codex ausente y modelo rechazado simulado.
- [ ] Doctor: activo sin next action falla; activo/false/con next action pasa; no escrituras.
- [ ] Metadata init/adopt 2.3.0-rc.2; capa 2.2.1 detectada, sin upgrade silencioso.
- [ ] routing-v1 aplicado: verificabilidad, ruta rápida, diagnóstico previo y evidencia revisable.
- [ ] Tamaños AGENTS/override/cap configurable y conflictos de configuración verificados.
- [ ] Finalization Gate/invariants y Review Loop Guard canónicos referenciados.
- [ ] Upgrade conserva criterios, decisiones, código y slices cerradas.
- [ ] Prueba manual real de continuidad S04 → S05 y `/status`, separada de tests estáticos.

- [ ] `FACTORY_VERSION.md` actualizado.
- [ ] `config/MODEL_CATALOG.md` actualizado/revisado.
- [ ] AI Policy / AI Strategy / AI Execution Profile validados.
- [ ] `CHANGELOG.md` actualizado.
- [ ] Destino público confirmado; onboarding sin URL inventada ni placeholders de propietario.
- [ ] No existen rutas personales.
- [ ] No existen secrets.
- [ ] `for script in scripts/*.sh scripts/lib/*.sh; do bash -n "$script"; done`.
- [ ] `python3 -B -m unittest discover -s tests -v` en macOS y Linux.
- [ ] CE-v1: selector/reutilización/RUN v3/transporte falso pasan; ningún SDK, red o credencial usados.
- [ ] `./scripts/install.sh --dry-run`.
- [ ] instalación probada en HOME temporal.
- [ ] instalación idempotente.
- [ ] uninstall probado.
- [ ] doctor probado.
- [ ] proyecto nuevo probado.
- [ ] proyecto existente probado.
- [ ] AGENTS existente preservado.
- [ ] ZIP/release generado.
- [ ] Scripts, skills, configuración y docs incluidos en la revisión Git; no publicar desde un HEAD que omita archivos untracked.
- [ ] `git status --porcelain` vacío en checkout; revisión probada identificada. Tag solo tras nueva autorización.
- [ ] `git archive` excluye `docs/archive/`, `docs/requirements/` y estado de desarrollo; no ZIP antiguo.
- [ ] Probar instalación desde el archivo exportado, no solo desde el working tree de desarrollo.


## Model routing

- [ ] MODEL_CATALOG tiene GPT-5.6 Luna / Terra / Sol y GPT-6 Astra.
- [ ] IDs exactos correctos.
- [ ] No hay recomendaciones ambiguas `GPT-5.6` sin variante.
- [ ] Guided Model Gate documentado.
- [ ] model-router skill presente.
- [ ] perfiles Codex validados.
- [ ] `configure-model-profiles.sh --dry-run` ejecutado.
