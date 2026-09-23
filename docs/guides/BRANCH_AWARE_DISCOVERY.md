# Branch-aware discovery

Modo optativo para repositorios donde ramas locales/remotas representan variantes
relevantes. Git no define una rama «abierta»: el alcance se expresa mediante refs.

## Inventario

Elegí una salida fuera del repositorio analizado:

```bash
ASF_ROOT="/ruta/a/ai-software-factory"
ANALYSIS_DIR="/ruta/externa/analisis"
"$ASF_ROOT/scripts/discover-variants.sh" inspect \
  --repo "/ruta/al/proyecto" --output "$ANALYSIS_DIR"
```

Genera:

- `BRANCH_INVENTORY.json`: refs, OID, snapshots, cobertura, divergencias y límites;
- `VARIANTS.json`: dimensiones técnicas inferidas y negocio en `unknown`;
- `REPOSITORY_MAP.md`: mapa humano pequeño.

Opera sin checkout, fetch, merge, reset, install ni build. Usa objetos disponibles
localmente y deshabilita lazy fetch. Los clones parciales se rechazan antes de leer
objetos para no provocar descargas implícitas; primero hay que completar el clon de
forma explícita. Un inventario `partial` conserva otros objetos faltantes/errores y no
equivale a cobertura completa. Las referencias se capturan antes/después; un cambio
concurrente devuelve código 3 después de escribir un resultado marcado stale.

## Comparación

```bash
"$ASF_ROOT/scripts/discover-variants.sh" compare --repo "/ruta/al/proyecto" \
  --left refs/heads/cliente-a --right refs/remotes/origin/cliente-b
```

Compara tips por ruta/modo/OID, sin renames. Expone todas las merge bases disponibles.
Usar refs completas evita resolución ambigua. Un ancestro común no demuestra que sea
el núcleo funcional vigente.

## Contexto por tarea

Tarea JSON explícita:

```json
{
  "objective": "revisar el flujo de login",
  "paths": ["src/app/login.ts", "package.json"],
  "required_paths": ["src/app/login.ts"],
  "max_bytes": 131072
}
```

```bash
"$ASF_ROOT/scripts/discover-variants.sh" context --repo "/ruta/al/proyecto" \
  --target refs/heads/cliente-a --task /ruta/externa/task.json \
  --output /ruta/externa/contexto

"$ASF_ROOT/scripts/discover-variants.sh" check --repo "/ruta/al/proyecto" \
  --manifest /ruta/externa/contexto/CONTEXT_MANIFEST.json
```

El manifest contiene el texto solicitado y su repo/ref/OID/ruta/blob, además del
fingerprint del overlay. Se invalida si cambia la ref, HEAD/status o el contenido del
manifest. Rechaza symlinks, binarios, rutas/markers sensibles y exceso de presupuesto.
Revisar el output antes de compartirlo: puede contener código del proyecto.

Doctor puede verificarlo junto al proyecto:

```bash
"$ASF_ROOT/scripts/doctor.sh" --project /ruta/al/proyecto \
  --variant-manifest /ruta/externa/contexto/CONTEXT_MANIFEST.json
```

## Adopción

El flujo existente no escanea snapshots por defecto. Si detecta varias refs muestra
un aviso. Para generar inventario durante adopción:

```bash
"$ASF_ROOT/scripts/adopt-project.sh" \
  --variant-discovery-output /ruta/externa/analisis
```

La identidad de cliente, estado activo, entorno desplegado y capacidades habilitadas
requieren revisión humana/backend. Package manifests y árboles son evidencia estática,
no prueba de runtime. No copies el mapa completo a AGENTS; seleccioná contexto por tarea.
