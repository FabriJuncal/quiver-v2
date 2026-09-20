# Contributing

Gracias por contribuir a AI Software Factory.

## Antes de proponer una nueva capacidad

Preguntá:

1. ¿resuelve un problema repetido?
2. ¿reduce errores, decisiones repetitivas o tiempo?
3. ¿podría ser documentación en lugar de una skill?
4. ¿puede ser opcional?
5. ¿agrega complejidad permanente?

La Factory prioriza **simplicidad y proporcionalidad**.

## Pull Requests

Todo PR debería:

- explicar el problema;
- explicar por qué la solución pertenece al core;
- mantener compatibilidad con proyectos existentes;
- evitar dependencias nuevas salvo necesidad;
- actualizar docs si cambia UX;
- ejecutar con Python >= 3.11 (en macOS puede llamarse `python3.14`):

```bash
bash scripts/check-release.sh
python3 -B -m unittest discover -s tests -v
./scripts/doctor.sh
```

La suite usa HOME/directorios temporales y Codex simulado; no prueba inferencia ni toca
configuración personal. El doctor final usa instalación real y puede informar warnings de
actualización. No interpretar esos warnings como disponibilidad verificada de modelos.

## Skills

No vendorear skills de terceros en el core salvo revisión de licencia, seguridad y necesidad.

Preferimos:

```text
pocas skills de alto valor
+
skills específicas del proyecto
```

antes que catálogos enormes activos.


## Cambios de Model Routing

Todo cambio de mapping debe:

- usar nombre completo + ID;
- mantener fallback;
- actualizar `Last verified`;
- evitar el alias ambiguo `gpt-5.6` como selección;
- mantener Guided Model Gate;
- pasar `doctor.sh`.
