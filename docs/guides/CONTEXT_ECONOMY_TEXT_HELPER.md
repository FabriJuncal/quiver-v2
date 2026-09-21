# Ahorro de contexto y ayudante textual opcional — CE-v1

Estado: implementación offline. No instala un SDK, no lee credenciales, no llama a
modelos y no habilita agentes. Inline sigue siendo el modo predeterminado.

## Qué aporta

`scripts/lib/context_economy.py` ofrece piezas pequeñas y componibles para U01
(revisión de Specs/Slices) y U02 (sugerencias de pruebas):

1. selecciona únicamente archivos textuales explícitos y obligatorios;
2. rechaza escapes, symlinks, hardlinks, rutas privadas, secretos sintéticos,
   cambios durante la lectura y presupuestos excedidos;
3. genera un fingerprint que incluye objetivo, criterios, contexto, dependencias,
   instrucciones, política y configuración solicitada;
4. reutiliza solo una entrega aceptada, íntegra y todavía equivalente;
5. construye un request textual estructurado sin tools ni background;
6. mantiene el dispatcher deshabilitado salvo que todos los gates estén aprobados.

Dependencias e instrucciones deben declararse completas y la configuración resuelta
debe ser conocida antes de crear una identidad reutilizable. No resume ni recorta
silenciosamente: la lectura se detiene al superar el presupuesto, sin cargar primero
el archivo completo. La estimación `utf8-bytes/4-ceiling` sirve
solo para presupuestar contexto; no afirma tokens facturados.

## Flujo seguro

```text
inline/local (default)
  → seleccionar y revisar contexto
  → buscar evidencia aceptada equivalente
  → si alcanza: continuar inline o reutilizar con validación del coordinador
  → si no alcanza y el ayudante sigue deshabilitado: continuar inline
  → solo con activación separada: persistir RUN v3 preparado
  → crear su dispatch guard duradero y efectuar un único despacho
```

RUN v3 usa `api_runtime.response_id`; nunca reutiliza `thread_id`. Tiene un solo intento.
`api_runtime.dispatch_guard_ref` liga el RUN preparado a un guard local exclusivo. El
claim `unknown` se persiste antes de invocar el transporte; una segunda invocación,
reinicio, timeout o caída no puede volver a consumirlo. Una respuesta `submitted`
todavía debe ser validada por el coordinador; no ejecuta comandos ni cierra una Slice.

El límite final vuelve a validar paths canónicos, duplicados, bytes, hashes, contenido
sensible sintético, digest y presupuesto del contexto serializado. El booleano de
revisión no reemplaza estas comprobaciones.

## Walkthroughs offline

- Contexto local: seleccionar Spec, Slice, criterios e instrucciones; validar los
  hashes antes de aceptar el resultado.
- Reutilización: si fingerprint y artefactos coinciden, mostrar procedencia y revisar
  aplicabilidad. Reutilizar no equivale a DONE.
- Ayudante deshabilitado: el transporte recibe cero llamadas y el trabajo local seguro
  continúa.
- Respuesta rechazada: conservar el error observado, no aplicar la salida y continuar
  inline cuando sea seguro.
- Resultado incierto: registrar `unknown`, no reintentar y pedir reconciliación antes
  de otro despacho.

Cada mensaje guiado debe informar hecho observado, pendiente, riesgo y próxima acción.
`ACCIÓN DEL USUARIO: ninguna` significa continuar, no cerrar el turno.

## Medición honesta

`normalize_usage` mantiene separados input, output, cache y reasoning; cache/reasoning
son subconjuntos y no se suman dos veces. `normalize_observations` separa tokens,
duración, memoria y costo. Ausente es `null`, no cero.

Una medición de memoria válida debe guardar bytes de peak RSS, herramienta/SO y lista
de procesos incluidos. No sumar picos individuales como simultáneos. Un costo requiere
una base estructurada con tipo (estimación/factura), modelo, fecha y fuente; rechaza
NaN/infinito y debe distinguir estimación de factura.
La prueba con transporte falso demuestra el contrato y una llamada evitada; no prueba
ahorro real de API, RAM de un cliente real ni ahorro total de desarrollo.

## Comprobar sin red

```bash
python3 -I -B tests/test_context_economy.py
python3 -B -m unittest discover -s tests -v
bash scripts/check-release.sh
```

Activar un cliente real, elegir modelo/SDK, usar datos, credenciales o presupuesto y
publicar son decisiones posteriores independientes.
