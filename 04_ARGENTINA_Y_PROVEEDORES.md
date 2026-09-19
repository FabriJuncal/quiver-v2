# Argentina y selección de proveedores

La ubicación del desarrollador importa principalmente para pagos, fiscalidad, disponibilidad de proveedores y latencia. No debería forzar el framework de la aplicación.

## Billing

No codificar el producto alrededor de un único proveedor.

Representar internamente conceptos simples:

```text
customer
subscription
plan
status
entitlements
```

Luego integrar un proveedor según necesidad:

- Argentina → evaluar Mercado Pago.
- Global sin estructura societaria compatible con Stripe → evaluar Merchant of Record.
- Empresa en país compatible → Stripe puede ser opción.
- Proyecto existente → mantener proveedor actual salvo problema real.

## Infraestructura

Elegir región según:

1. usuarios;
2. base de datos;
3. backend;
4. restricciones regulatorias.

No elegir región solo por dónde trabaja el desarrollador.

## Regla

> No crear una estructura societaria extranjera únicamente para satisfacer una herramienta antes de validar el producto.
