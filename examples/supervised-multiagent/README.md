# Factory multiagente supervisada — ejemplo offline

**SINTÉTICO. No hubo ayudante, permiso real, llamada a modelo ni ahorro medido.**
Este ejemplo demuestra formato y validadores v2. No activa configuración ni habilita
dispatch. La distribución sigue 2.2.2; función local experimental, no publicada.

Desde la raíz de Factory, con Python >=3.11 (sustituir python3.14 si corresponde):

```bash
python3.14 -I -B scripts/lib/check_execution.py --project examples/supervised-multiagent/project
python3.14 -B -m unittest discover -s tests -p 'test_supervised_delegation.py'
python3.14 -B -m unittest discover -s tests -p 'test_workspace_audit.py'
```

Esperado: STATIC PASS para un registro sintético; advertencias de controles desconocidos
y NO APTO PARA PILOTO. No es contradictorio: datos coherentes no prueban permisos vivos.
Los tests construyen temporales, simulan Codex y no usan tu configuración habitual.

## Ver un inventario real, sin escribir

```bash
python3.14 -I -B scripts/lib/audit_workspace.py snapshot --root examples/supervised-multiagent/project/src --scope-id preview
```

Salida JSON: paths, tipo, permisos, tamaño y hash; nunca contenido de archivos.
La raíz debe ser explícita, revisada y limitada. No apuntar a HOME/proyecto completo
para sustituir una selección de contexto. La utilidad no copia, filtra secretos ni
escribe manifests; el coordinador los persiste fuera de la raíz inventariada.
Usar rutas canónicas sin componentes symlink; en macOS, por ejemplo, /private/tmp
en lugar del alias /tmp. La comprobación no garantiza inmunidad a carreras hostiles.

Comparar los dos manifests sintéticos incluidos:

```bash
python3.14 -I -B scripts/lib/audit_workspace.py compare --before examples/supervised-multiagent/project/docs/requirements/demo/slices/S01/attempt-1-copy-before.json --after examples/supervised-multiagent/project/docs/requirements/demo/slices/S01/attempt-1-copy-after.json
```

Esperado: result clean, changes vacío, exit 0. Exit 2 significa diferencias finales;
exit 1, lectura/formato inválido o comparación incompleta. No convertir ninguno en
rollback automático ni aceptar una entrega con incidente. La comparación no revisa
filesystem actual, solo manifests: snapshot es una operación separada.

## Recorridos guiados — M19/M20

1. **Limpio:** coordinador registra manifests y fin observado; compara, revisa entrega,
   verifica criterios y base, ejecuta tests proporcionales. Acepta solo con evidencia.
   Si hay próxima slice autorizada, la activa y trabaja en ella en el mismo turno.
   El registro sintético accepted aquí NO cierra por sí solo la slice de ejemplo.
2. **Cambio en copia:** preservar informe, rechazar entrega, confirmar detención;
   failed con incident_refs. Copia no reutilizable; no borrar ni restaurar original.
3. **Cambio humano en original:** detener integración, preservar ambas versiones,
   reconciliar con usuario. No asumir autoría del hijo ni eliminar trabajo humano.
4. **Fin desconocido:** informar último evento observado, no porcentaje de avance;
   mantener cupo ocupado y no reintentar/reasignar/continuar sobre archivos compartidos.
5. **Control obligatorio desconocido antes de lanzar:** no despachar. Si inline seguro
   es suficiente, continuar inline con acción concreta; si no, limitación y paso exacto
   para resolver el control. Modelo/costo unknown si no se observan.

Estos recorridos son revisión de UX, no prueba de obediencia real. M10 en tests
demuestra que editar/restaurar entre snapshots puede dejar comparación clean.

## Contratos y contexto

Fuente canónica: [Guided Delegation](../../docs/guides/GUIDED_DELEGATION.md).
Estructura de run v1/v2: [RUN.schema.json](../../templates/slice/RUN.schema.json).
V2 agrega supervision: policy, aprobación del riesgo, revisión del contexto,
controles con evidencia, manifests/informes por intento y incident_refs.
El checker recalcula comparación y verifica refs; no autentica autoría ni prueba que
los manifests provengan de un runtime aislado. Evidencia coherentemente falsificada
no se detecta por hashes. Evitar acceso del hijo a baselines/evidencia requiere control real.

Los campos simulados approved/accepted viven solo en project/. No copiarlos al
estado real como aprobación humana. Se conservan unknown los controles efectivos.
Generador determinista: tests/delegation_fixture.py, audited_fixture_files; el test
comprueba igualdad byte a byte con este ejemplo. El ejemplo v1 permanece intacto.
