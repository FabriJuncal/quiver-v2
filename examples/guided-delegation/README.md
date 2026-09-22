# Guided delegation — ejemplo offline

Este proyecto es una fixture sintética, no un permiso para lanzar workers.
Sus eventos, IDs, autorización y evidencias son inventados y están etiquetados como
SYNTHETIC. No copiar su autorización a un proyecto real.

Desde la raíz de Factory, con Python 3.11 o posterior:

```bash
python3 -I -B scripts/lib/check_execution.py --project examples/guided-delegation/project
```

Resultado esperado: un registro, STATIC PASS y modelo efectivo desconocido.
No se ejecutan agentes, comandos de la entrega ni tests del proyecto de ejemplo;
no se escriben archivos. `accepted` representa aceptación sintética de una entrega,
no cierre automático del slice: SPEC permanece active deliberadamente.

El generador de fixtures de tests y el ejemplo distribuido se comparan byte a byte.
Los hashes vinculan el brief, contexto, instrucciones y evidencia; editar un archivo
referenciado exige reconciliar el registro, no ignorar la inconsistencia.

Ver [contrato operativo](../../docs/guides/GUIDED_DELEGATION.md) y
[recorridos de revisión documental](WALKTHROUGHS.md). No hay dispatcher ni comandos
`/delegate`, `/retry` o `/cancel` implementados por Factory.
