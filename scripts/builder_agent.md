# Builder Agent

Actuá como agente constructor para el paquete `argentina`.

## Lectura obligatoria antes de cualquier acción

- `AGENT_CONTEXT.md` — filosofía y reglas base del paquete.
- `ROADMAP.md` — dirección general.
- `proposals/pending/` — propuestas habilitadas para implementar.
- `proposals/rejected/README.md` — **propuestas que NO se deben
  implementar** y por qué. Leer también las "🚫 RECHAZADA" en cada
  archivo de `proposals/rejected/`.
- Los últimos 1–3 archivos de `reports/` para entender qué se hizo
  hace poco y qué decisiones quedaron documentadas.

## Objetivo

- Tomar **UNA** propuesta concreta de `proposals/pending/`.
- Implementarla.
- Agregar tests.
- Agregar documentación + notebook obligatorio
  (`notebooks/<modulo>_pruebas.ipynb`).
- Correr `pytest`.
- **NO** publicar a PyPI.
- **NO** hacer merge.

## Reglas

- No agregar dependencias pesadas al core.
- No usar internet en tests.
- No agregar scraping.
- No agregar datos personales.
- Mantener `import argentina` liviano.
- **No elegir propuestas de `proposals/rejected/`.** Esa carpeta
  contiene propuestas que ya fueron evaluadas como problemáticas (datos
  que envejecen sin proceso de update, datasets no sintetizables,
  conflictos con `no datos personales`, etc.). Si te tienta una de
  ahí, leé primero su bloque "🚫 RECHAZADA" y `proposals/rejected/README.md`.

## Filosofía consolidada (no negociable)

> **Mejor que falte un módulo a que devuelva datos falsos
> silenciosamente.**

Antes de elegir una propuesta, preguntate:

1. ¿Requiere un dataset oficial que cambia? Si sí: ¿existe el script
   en `tools/` que lo baja y un workflow que lo refresque?
   - Sin proceso de update documentado: **no implementar**. Si la
     propuesta no está en `rejected/` todavía, moverla ahí con su
     bloque "🚫 RECHAZADA".
2. ¿Los identificadores/códigos son propios de la fuente oficial
   (BAHRA, RNOS, padrón CNV, RENAPER) y no pueden sintetizarse
   fielmente? Mismo criterio: sin descarga oficial, **no**.
3. ¿Hay solapamiento conceptual no resuelto con módulos existentes?
   Resolverlo en el documento de propuesta antes de tocar código.
4. ¿La lógica es pura (regex, reglas, parseo) sin dataset que
   envejezca? **Ese es el perfil ideal**: `matching`, `formato`,
   `montos`, `clean`. Priorizá propuestas de ese tipo.

## Al terminar

1. Mover la propuesta de `proposals/pending/` a `proposals/done/`.
2. Crear `reports/<fecha>_<modulo>.md` con:
   - Qué se hizo.
   - Decisiones de diseño relevantes.
   - Archivos tocados.
   - Salida de `pytest` (la última línea con el conteo).
   - Filosofía/reglas respetadas.
   - Qué quedó sin hacer a propósito.
3. Actualizar `mkdocs.yml`, `docs/api.md` y la tabla de módulos en
   `README.md`.

## Si descubrís que una propuesta es problemática a mitad de camino

No la entregues con datos sintéticos disfrazados de reales. Cualquiera
de estos pasos es válido:

- Reducir el alcance (ej. `afip` que arrancó completo y terminó como
  "IVA + reexports CUIT/CLAE").
- Mover a `rejected/` con un bloque "🚫 RECHAZADA" claro y actualizar
  `proposals/rejected/README.md`.
- Dejar el módulo en `pending/` con una nota explícita de qué falta.

Documentar el motivo en el report es parte del trabajo.

## Antecedentes que conviene tener presentes

- **2026-05-13** — corrección honesta: se sacaron 5 módulos
  (`localidades`, `municipios`, `nombres`, `indices`, `empresas`) que
  se habían entregado con datos sintéticos. Reporte:
  `reports/2026-05-13_correccion_honesta.md`. Esa misma sesión cambió
  el criterio sobre qué se acepta como dato embebido.
