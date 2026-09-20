# Release Checklist

Target: AI Software Factory v2.2.2 — Runtime Guardrails. No confundir validación local con publicación.

- [ ] `bash scripts/check-release.sh`: versiones, archivos, mappings, instrucciones y rutas.
- [ ] Launcher: cuatro dry-runs, argv literal, espacios, Codex ausente y modelo rechazado simulado.
- [ ] Doctor: activo sin next action falla; activo/false/con next action pasa; no escrituras.
- [ ] Metadata init/adopt 2.2.2; capa 2.2.1 detectada, sin upgrade silencioso.
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
- [ ] `git status --porcelain` vacío en el checkout de release; el tag apunta a la revisión probada.
- [ ] `git archive` excluye `docs/archive/` y no incluye el ZIP antiguo.
- [ ] Probar instalación desde el archivo exportado, no solo desde el working tree de desarrollo.


## Model routing

- [ ] MODEL_CATALOG tiene GPT-5.6 Luna / Terra / Sol y GPT-6 Astra.
- [ ] IDs exactos correctos.
- [ ] No hay recomendaciones ambiguas `GPT-5.6` sin variante.
- [ ] Guided Model Gate documentado.
- [ ] model-router skill presente.
- [ ] perfiles Codex validados.
- [ ] `configure-model-profiles.sh --dry-run` ejecutado.
