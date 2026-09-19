# Ejemplo — Proyecto existente

```yaml
project:
  name: Legacy Mobile Platform
  mode: existing
  type: mobile-platform

frontend:
  framework: ionic-angular

backend:
  framework: php

database:
  provider: sql-server
```

CAPABILITY_MAP:

| Capacidad | Solución | Acción |
|---|---|---|
| Frontend | Ionic/Angular | KEEP |
| API | PHP | KEEP |
| DB | SQL Server | KEEP |
| Auth | existente | KEEP |
| Testing | parcial | IMPROVE |
| Legacy migration | necesaria | ADD skill |
| Billing | no aplica | IGNORE |

No migrar a Next.js/Supabase por defecto.
