## Problema

¿Qué problema resuelve?

## Cambio

¿Qué se modificó?

## Por qué pertenece al core

¿Por qué no debería ser solo documentación/skill opcional?

## Validación

- [ ] `for script in scripts/*.sh scripts/lib/*.sh; do bash -n "$script"; done`
- [ ] `python3 -B -m unittest discover -s tests -v` (fixtures aislados)
- [ ] `./scripts/doctor.sh`
- [ ] Docs actualizadas
- [ ] No agrega complejidad innecesaria
