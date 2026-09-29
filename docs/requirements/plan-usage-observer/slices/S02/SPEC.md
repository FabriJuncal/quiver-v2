# Slice Spec — S02

- **Slice ID:** S02
- **Status:** completed

## Goal

Agregar al observador offline un lifecycle explícito, límites temporales observables,
revisiones preservadas del reporte y costos explicables calculados únicamente con
tarifas sintéticas, sin convertir faltantes en cero.

## Scope

- Eventos explícitos de inicio, pausa, reanudación, cierre técnico, aceptación,
  fallo, retry y cancelación, con timestamp provisto y referencia de aceptación.
- Tiempo transcurrido y pausado derivado solo de límites válidos; actividad, espera
  y tiempo-agente permanecen unknown.
- Snapshots tarifarios sintéticos, inmutables y versionados; aritmética Decimal por
  respuesta sin sumar reasoning como categoría adicional ni presentar subtotal como
  gasto facturado.
- Reporte v2 con lifecycle, tiempos, costo, revisión y outcomes; reporte v1 accesible
  explícitamente y revisiones anteriores preservadas.
- Guía, wireframe, esquema y fixtures artificiales de T2.

Fuera de alcance: S03, sesiones reales, precios comerciales, cobro/factura,
proveedores online, dependencias, launcher, router, configuración global y publicación.

## Criteria covered

- AC-04, AC-05, AC-06, AC-07, AC-08 y AC-10.

## Dependencies

- S01 cerrada y aprobada con notas, sin findings obligatorios abiertos.
- Plan v1 y perfil T2 reforzado aprobados.
- Autorización explícita del usuario del 2026-09-24 limitada a S02.

## Validation

- T04–T07, T11 y T12 con archivos temporales, relojes controlados y tarifas
  exclusivamente sintéticas.
- Regresiones S01 focalizadas solo donde cambia el contrato compartido de reporte,
  persistencia o conteo.
- Sintaxis Python/JSON, enlaces relativos y `git diff --check`.

## AI Profile Recommendation

- **Profile:** ADVANCED — heredado de `../../STATE.md` para integridad, concurrencia
  y aritmética.
- **Reasoning:** High recomendado; configuración efectiva de esta sesión NO VERIFICADA.
- **Reason:** contexto y oráculos suficientes; sin evidencia de capacidad insuficiente,
  por lo que no se abre Model Gate para esta ejecución ya autorizada.
