# AI Model Routing

En v2.2.2 se distingue REQUESTED PROFILE de EFFECTIVE SESSION CONFIG (unknown por defecto).
No asumir coincidencia ni introspectar modelo. [Session Preflight](SESSION_PREFLIGHT.md) solo
interrumpe por necesidad material; [asf](ASF_LAUNCHER.md) ofrece overrides deterministas de inicio.
Aplicar Finalization Gate del contrato: toda aparición de `ACCIÓN DEL USUARIO: ninguna` en
estos ejemplos es una actualización seguida de ejecución, nunca cierre con trabajo pendiente.

AI Software Factory gestiona modelos de forma **guiada**, no automática.

## Aplicación obligatoria y límites

Aplicar [routing-v1 del catálogo](../../config/MODEL_CATALOG.md#selección-proporcional-y-registro-de-routing)
antes de planificar/implementar: verificabilidad, ruta rápida, diagnóstico y decisión
breve o referencia vigente en STATE/brief. El review comprueba su correspondencia con
el trabajo. No basta declarar «usé el router»; tampoco hace falta narrarlo en cada turno.
Install, init y el snippet de adopt distribuyen la instrucción; proyectos existentes
deben integrar el snippet compatible. Un snippet sin integrar no es una instrucción activa.

Esto refuerza cumplimiento de procedimiento, no lo garantiza técnicamente. Markdown,
un registro o un test de instalación no prueban que el modelo lo obedeció. Un control
duro exigiría un runtime que medie cada ejecución, valide una decisión y compruebe la
configuración aceptada; aun así eso no prueba razonamiento interno ni corrección.
Ese controlador queda fuera del router guiado. El launcher solo fija intención de inicio.

En Codex, comprobar que AGENTS.md sea la instrucción efectivamente descubierta: un
AGENTS.override.md, instrucciones más cercanas o truncamiento pueden cambiar lo cargado.
Las instrucciones se descubren al iniciar una ejecución/sesión; después de instalar
cambios, iniciar una sesión nueva para comprobar su carga. Consultar el doctor de Factory
y la [documentación oficial de descubrimiento](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance).

Las verificaciones offline prueban propagación/consistencia, no ahorro o calidad medidos.
No ejecutar benchmarks ni cambiar configuración personal para certificar esta política.

La Factory:

1. clasifica la capacidad requerida;
2. recomienda modelo + reasoning;
3. decide si cambiar compensa la interrupción;
4. guía al usuario paso a paso cuando el cambio es material;
5. nunca deja al usuario preguntándose cómo continuar.

---

# Perfiles

## ECONOMICAL

**GPT-5.6 Luna (`gpt-5.6-luna`) / Low**

Para trabajo claro, mecánico y de alto volumen.

## BALANCED

**GPT-5.6 Terra (`gpt-5.6-terra`) / Medium**

Default recomendado para desarrollo cotidiano.

## ADVANCED

**GPT-5.6 Sol (`gpt-5.6-sol`) / High**

Para alto riesgo, ambigüedad o razonamiento complejo.

## Exceptional Override

**GPT-6 Astra (`gpt-6-astra`) / High o XHigh**

Solo para problemas extraordinariamente difíciles.

---

# Experiencia normal

El usuario abre:

```bash
codex
```

o, si instaló perfiles:

```bash
codex --profile asf-balanced
```

La mayoría del tiempo Factory no habla de modelos.

Ejemplo:

```text
Perfil requerido:
BALANCED — GPT-5.6 Terra (gpt-5.6-terra) / Medium

Esta etapa no depende materialmente de verificar la configuración efectiva.

ACCIÓN DEL USUARIO: ninguna

Continúo con Project Discovery.
```

---

# AI Model Gate

Se muestra únicamente cuando el cambio de configuración tiene **beneficio material**.

Formato obligatorio:

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI MODEL GATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Próxima tarea:
[descripción]

Perfil requerido:
ADVANCED

Modelo preferido:
GPT-5.6 Sol

ID:
gpt-5.6-sol

Reasoning:
High

Fallback si no aparece:
GPT-5.6 Terra
gpt-5.6-terra
High o XHigh

Motivo:
[riesgo/razón concreta]

QUÉ TENÉS QUE HACER

1. Si no sabés qué modelo está activo, ejecutá:
   /status

2. Si ya estás en GPT-5.6 Sol con High o una configuración superior:
   no cambies nada.

3. Si necesitás cambiar:
   /model

4. Seleccioná:
   GPT-5.6 Sol
   High

5. Volvé y escribí:
   continuar

ACCIÓN DEL USUARIO: requerida
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

El agente se detiene aquí.

No ejecutar la slice crítica hasta la confirmación.

Omitir este gate cuando la configuración suficiente ya esté confirmada para la fase en la sesión actual. Una slice nueva no reinicia la confirmación. Seguir la política canónica de `config/MODEL_CATALOG.md`.

---

# Confirmación

Después de:

```text
continuar
```

no afirmar que el modelo cambió por introspección.

Interpretar la respuesta como confirmación del usuario de que completó el gate.

Mostrar como actualización, seguida de ejecución real:

```text
AI MODEL GATE confirmado.

Perfil requerido:
ADVANCED — GPT-5.6 Sol (gpt-5.6-sol) / High

ACCIÓN DEL USUARIO: ninguna

Continúo con la slice.
```

Este ejemplo supone que no hay otro boundary pendiente y que la ejecución está autorizada. Si falta aprobación de criterios/plan, autorización o evidencia de review, presentar exactamente ese paso: confirmar el modelo no lo satisface.

---

# Modelo activo desconocido

La Factory **no debe inventar** qué modelo está usando la sesión.

Si saberlo no es necesario:

- no preguntar;
- continuar.

Si el próximo trabajo requiere un gate:

- guiar al usuario con `/status`;
- indicar exactamente qué seleccionar con `/model`.

---

# Switch Benefit

Antes de interrumpir:

- LOW → no gate;
- MEDIUM → continuar y reevaluar en phase boundary;
- HIGH → gate solo si falta confirmar configuración suficiente para la fase/sesión.

Esto evita cambiar de modelo por micro-optimizaciones.

---

# Reasoning antes de modelo

Cuando el problema sea profundidad y no capacidad:

```text
GPT-5.6 Terra / Medium
→ GPT-5.6 Terra / High
```

puede ser preferible a:

```text
GPT-5.6 Terra
→ GPT-5.6 Sol
```

En cambio, ante seguridad, autorización, datos o arquitectura crítica, preferir:

**GPT-5.6 Sol (`gpt-5.6-sol`) / High**

---

# Downgrade

No interrumpir por un cierre corto.

Sí sugerir downgrade cuando comienza una fase grande y mecánica, el beneficio es HIGH y no exige volver a subir inmediatamente:

```text
AI MODEL OPTIMIZATION

Parte compleja finalizada.

Trabajo restante:
20 transformaciones repetitivas.

Perfil recomendado:
ECONOMICAL

Modelo:
GPT-5.6 Luna
gpt-5.6-luna

Reasoning:
Low

QUÉ HACER:
/model
→ GPT-5.6 Luna
→ Low
→ continuar

Fallback si Luna no aparece:
GPT-5.6 Terra (gpt-5.6-terra) / Low, si satisface las restricciones de costo.

ACCIÓN DEL USUARIO: requerida
```

---

# Review

## N0

Self verification.

## N1

Self review.

`/review` opcional si aporta valor.

## N2

`/review` recomendado para cambios no triviales o compartidos.

## N3

Review dedicado requerido cuando sea técnicamente posible. Si no lo es, aplicar la excepción con alternativa aprobada de workflow 08 antes del cierre.

Guided instruction:

```text
REVIEW GATE

Qué hacer:

1. ejecutá:
   /review

2. elegí la opción y rama/commit exactos que el agente determinó
   inspeccionando Git según workflow/08_IMPLEMENTATION_REVIEW.md.

3. cuando finalice, escribí:
   continuar con review

ACCIÓN DEL USUARIO: requerida
```

Si existe `review_model = "gpt-5.6-sol"`, Codex puede utilizar GPT-5.6 Sol para el review sin cambiar el modelo principal.

No prueba reasoning High. Verificarlo si el runtime lo permite; de lo contrario registrarlo NO VERIFICADO. La política de evidencia, excepción técnica y límite de una ronda de corrección está en workflow 08. N3 requiere una alternativa aprobada si el review dedicado es técnicamente imposible.

---

# Persistencia

## PROJECT_PROFILE

Persistir AI Policy.

## Requirement STATE

Persistir AI Strategy.

## EXECUTION_BRIEF

Persistir recomendación resuelta:

- perfil;
- modelo preferido;
- ID;
- reasoning;
- fallback;
- switch benefit;
- model gate required;
- fecha/catálogo.

No persistir el modelo activo real de la sesión.

---

# Regla de Guided Mode

Toda recomendación de modelo debe terminar en una acción inequívoca:

- `ACCIÓN DEL USUARIO: ninguna` + continuar;
- o pasos numerados + comando exacto + texto exacto a escribir después.

Nunca terminar con:

```text
Sería mejor usar un modelo más potente.
```

Eso no es Guided Mode.
