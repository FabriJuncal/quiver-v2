# Technical plan — v1

1. Reconciliar rc.1/tag/estado y abrir requirement rc.2 sin alterar el tag existente.
2. Actualizar metadata pública, notas, changelog, guías, tests y checks a rc.2.
3. Ejecutar T2: suite completa, check-release, diff/secret scan dirigido y dry-runs.
4. Crear commit de candidata; verificar checkout limpio de ese commit.
5. Generar ZIP con `git archive`, SHA-256 y ARTIFACTS.json fuera del árbol exportado.
6. Extraer ZIP en temporal, ejecutar suite/check-release y comprobar exclusiones/permisos.
7. Self review N2 del diff y artefactos; persistir evidencia y detenerse ante aprobación
   final de push/tag/GitHub Release. CI macOS/Linux queda pendiente hasta push autorizado.

Rollback: borrar solo artefactos locales ignorados o revertir el commit rc.2. No tocar
configuración habitual ni instalaciones existentes. Publicación es un boundary separado.
