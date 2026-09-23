# [branch-aware-discovery] Slice: discovery seguro sobre múltiples ramas

## Resumen
Agrega un lector Git offline que inventaría variantes desde todas las ramas sin hacer
checkout ni modificar el repositorio analizado. Produce inventario, comparaciones y
contextos acotados por tarea, y lo integra de forma optativa al adoption y al doctor.

## Tipo de cambio
- [x] 🚀 Feature
- [ ] 🐛 Bugfix
- [x] 📝 Documentación
- [ ] ♻️ Refactor
- [ ] ⚡ Performance
- [ ] 🔒 Security
- [x] 🧪 Tests

## Slice Definition

### Objetivo
Permitir que Quiver descubra y compare variantes distribuidas entre ramas sin alterar
la rama actual ni mezclar conocimiento entre clientes.

### Incluye
- [x] CLI `discover-variants.sh` con `inspect`, `compare`, `context` y `check`.
- [x] Integración optativa en adoption/doctor, documentación, manifest y skills.
- [x] Fixtures adversos, suite automatizada y piloto real de solo lectura.

### Excluye
- [x] Identificación automática de clientes o instalaciones activas.
- [x] Validación de backend/runtime de las variantes.
- [x] Merge, versionado y publicación de una release.

## Checklist

### Código
- [x] Tests agregados/actualizados
- [ ] Lint pasa sin errores
- [ ] Types sin errores
- [ ] Build pasa correctamente

No existe un comando dedicado de lint, type-check o build para este toolkit. Se
ejecutaron las validaciones propias del repositorio, syntax checks incluidos por la
suite, `git diff --check`, release checker e instalación dry-run.

### Documentación
- [x] README actualizado
- [x] Docs de API actualizadas (si aplica)
- [ ] CHANGELOG actualizado (si aplica)

No se modificó CHANGELOG porque este PR no prepara una versión publicable.

### Despliegue
- [ ] Migraciones creadas (si aplica)
- [x] Variables de entorno documentadas
- [x] Notas de despliegue agregadas

No hay migraciones ni variables obligatorias. La adopción es optativa y la publicación
de una release queda fuera del alcance.

## Cómo Probar (DETTALLADO - OBLIGATORIO)

> **⚠️ IMPORTANTE:** Esta sección debe ser tan detallada que cualquier miembro del equipo pueda probar el feature sin ayuda adicional.

### Precondiciones
Python 3.14, Bash y Git disponibles. Ejecutar desde la raíz de Quiver. Para probar el
CLI manualmente, usar un clon descartable y escribir el output fuera de ese repositorio.

1. **Variables de entorno:**
   ```bash
   # Ninguna variable obligatoria.
   ```

2. **Ejecutar la suite completa:**
   ```bash
   python3.14 -B -m unittest discover -s tests -v
   ```
   Resultado esperado: 153 tests exitosos.

3. **Validar el paquete y el diff:**
   ```bash
   bash scripts/check-release.sh
   bash scripts/install.sh --dry-run
   git diff --check main...HEAD
   ```
   Resultado esperado: los tres comandos finalizan con código 0.

4. **Probar el lector sobre un clon descartable:**
   ```bash
   output_dir="$(mktemp -d)"
   bash scripts/discover-variants.sh inspect \
     --repo /ruta/al/clon-descartable \
     --output "$output_dir"
   bash scripts/discover-variants.sh check \
     --repo /ruta/al/clon-descartable \
     --inventory "$output_dir/BRANCH_INVENTORY.json"
   ```
   Resultado esperado: inventario y matriz fuera del clon; `check` confirma que refs,
   árboles y blobs conservan los OID registrados.

## Problema

El discovery previo observaba solamente el checkout actual. En repositorios donde las
ramas representan clientes o variantes, eso omitía diferencias relevantes o incentivaba
checkouts costosos y riesgosos.

## Por qué pertenece al core

La lectura segura de refs, objetos y árboles define qué contexto puede conocer Quiver.
Centralizarla en el core evita que cada proyecto improvise checkouts o parsers Git y
permite que adoption, doctor y skills compartan el mismo contrato verificable.

## Riesgos

- No determina identidad comercial ni actividad de una instalación; conserva esos
  campos como desconocidos salvo evidencia explícita.
- Un contexto exportado puede contener código; debe almacenarse fuera del worktree y
  distribuirse con los controles del repositorio analizado.
- Rechaza clones parciales y objetos faltantes en vez de completar datos por red.
- El piloto fue de solo lectura y el review fue una autorrevisión N2.

## Evidencia

- Suite final: 153 tests PASS en 36,568 s.
- Release checker, instalación dry-run y `git diff --check`: PASS.
- Piloto: 95 refs, 82 tips distintos, 10 preguntas y estado del repositorio preservado.
- Hallazgos F01–F03 cerrados en una ronda dirigida.
- Inventario, nombres de ramas, rutas y reportes privados del piloto excluidos del PR.

**Recomendación:** ready for review. Revisar especialmente límites de identidad,
captura stale y manejo de objetos faltantes; no mergear ni publicar sin autorización.
