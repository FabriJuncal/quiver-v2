# S03 — cierre offline

Utilidad audit_workspace.py: snapshot/compare por stdout, sin copias ni restauración.
Detecta diferencias finales y rechaza enlaces/archivos especiales/lectura incompleta;
tipos, hashes, permisos y alcance contrastados. Ejemplo v2 generado con datos sintéticos.

Validación filesystem: 13 tests OK (0.239 s). Comandos README snapshot y compare
ejecutados: exit 0, inventario real de src de ejemplo y comparación sintética clean.
M10 prueba límite de cambios transitorios; M11 conserva cambio humano; M21 muestra
que inventario no es scanner de secretos. Modelo/aislamiento/red no verificados.

Sin cambios sobre configuración ni agentes. Continúa S04 con regresión y self review.
