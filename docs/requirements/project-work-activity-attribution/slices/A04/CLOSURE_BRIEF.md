# Closure Brief — A04

- **Estado:** bloqueada tras diagnóstico de throughput, 2026-09-25; no es un cierre completo del requirement.
- **Alcance ejecutado:** T14 inició contra `http://127.0.0.1:8009`, checkpoint
  `jaredpalmer/kev-4b`, exclusivamente con casos sintéticos congelados. No se
  ejecutó A05 ni se cambió código, umbrales, dataset, configuración global,
  router o launcher.
- **Evidencia:** `/v1/models` confirmó checkpoint, MPS/MLX `bfloat16` y, tras
  los intentos, cuatro batches/solicitudes completadas con caché. El cliente
  `kev_classify` agotó su límite fijo de 5 s en dos intentos sin recibir señales
  ni `usage`. La corrección autorizada elevó su timeout a 180 s y las 11
  regresiones afectadas pasaron. El diagnóstico recibió un caso en 176445.453
  ms y mostró que Metal procesa una solicitud a la vez.
- **Resultado:** 300 casos se estiman en 14.7 h; T14 no puede calcular
  precisión, cobertura, abstención, matriz de confusión, p50/p95 ni consumo
  propio; son unknown. Kev permanece sin habilitar y A05 sigue fuera de alcance.
- **Única siguiente acción:** decidir si autoriza un candidato Kev local
  operativo, con endpoint y checkpoint explícitos, para repetir A04.
