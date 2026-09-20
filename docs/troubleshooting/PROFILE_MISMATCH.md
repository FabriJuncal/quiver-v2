# BALANCED aparece como High

BALANCED solicita GPT-5.6 Terra (`gpt-5.6-terra`) / Medium. Que `/status` muestre High es una
configuración diferente. La causa posible es un override del proyecto, CLI o modo de sesión;
no asumir cuál sin evidencia. Perfil solicitado y configuración efectiva son conceptos separados.

Para iniciar con overrides explícitos: `asf balanced`. Para corregir sesión actual:

1. Ejecutá `/status`.
2. Ejecutá `/model`, seleccioná GPT-5.6 Terra (`gpt-5.6-terra`) y Medium si están disponibles.
3. Escribí `continuar`; si la configuración sigue diferente, pegá el resultado de `/status`.

No publicar config completa (puede contener datos privados). Doctor detecta claves conflictivas
sin imprimir valores sensibles: `"$ASF_ROOT/scripts/doctor.sh" --project .`.
No editar `config.toml` automáticamente. Los perfiles existentes se preservan aun si fueron
personalizados. `asf balanced --dry-run` permite revisar el comando sin sesión.
La verificación interactiva solo bloquea cuando la tarea dependa materialmente de esa capacidad;
una diferencia por sí sola no debe detener trabajo normal.
