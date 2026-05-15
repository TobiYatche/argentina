# Docs update — 2026-05-13 (v6, sync i18n)

Sexta pasada del agente `docs_agent`. Foco único: **sincronizar las 10
traducciones del README** con la versión española actualizada en v5.

Versión del paquete al momento del reporte: **0.3.0**.

## Pedido del usuario

> "esto esta para todos los idiomas?"

La respuesta corta era **no** — y estaba marcado como pendiente desde v5
en el reporte anterior. Esta pasada lo arregla.

## Qué cambió respecto a v5 (lo que las traducciones tenían que reflejar)

El README español pasó a tener este orden y secciones, que ahora también
aparecen en los 10 archivos `docs/i18n/<lang>/README.md`:

1. Título + tagline + frase-gancho ("Si trabajás con bases argentinas…").
2. **Instalación** — `pip install argentina` + 3 extras destacados.
3. **Import recomendado** — sección dedicada con `import argentina as arg`
   + mención de los imports alternativos.
4. **Uso rápido** — bloque mínimo con `provincias.lookup`,
   `personas.limpiar_dni`, `postal.validar_cpa`, `bancos.validar_cbu`.
5. **Core liviano** — lista explícita de los 6 paquetes que NO se
   importan automáticamente.
6. **Módulos principales** — tabla simplificada (sin contar entradas)
   con 22 módulos y sus descripciones traducidas a cada idioma.
7. **Filosofía** — 5 bullets + el blockquote "El objetivo no es
   reinventar pandas ni geopandas…".
8. **Documentación** — placeholder de GitHub Pages, comandos
   `mkdocs serve`, tabla "Si querés X, andá a Y".
9. **Estado** — versión 0.3.0 (Beta), Python 3.9+, **550 tests** (no
   más "~250"), fuentes, propósito.
10. **Licencia** — MIT con link a GitHub (no path relativo, así no
    rompe `mkdocs build --strict`).

## Cómo se regeneraron

Para evitar drift entre las 10 traducciones, escribí un script que
construye los 10 archivos desde un template único:

- **Bloques de código compartidos** (instalación, import, uso rápido,
  `mkdocs serve`) se reutilizan literales en todos los idiomas. La API
  de Python es la misma en cualquier idioma.
- **Texto narrativo** se traduce por idioma (`tagline`, `hook`,
  bullets de filosofía, descripciones de módulos, etc.).
- **Tablas** se traducen los encabezados y la primera columna; la
  segunda columna con código se mantiene literal.
- **Árabe** envuelto en `<div dir="rtl">` para que GitHub y mkdocs
  rendericen RTL correctamente.

El script vive en `/tmp/build_i18n_readmes.py` durante esta pasada. Si
se decide versionarlo, conviene moverlo a `scripts/build_i18n.py` para
poder regenerar en futuras pasadas — pero **eso queda fuera de scope**
de esta corrida (es tooling, no docs).

## Archivos actualizados

Los 10 archivos quedaron en 139 líneas (143 el árabe por el wrapper RTL):

```
docs/i18n/en/README.md   139 líneas  → inglés
docs/i18n/pt/README.md   139 líneas  → portugués
docs/i18n/fr/README.md   139 líneas  → francés
docs/i18n/it/README.md   139 líneas  → italiano
docs/i18n/de/README.md   139 líneas  → alemán
docs/i18n/zh/README.md   139 líneas  → chino simplificado
docs/i18n/ja/README.md   139 líneas  → japonés
docs/i18n/ko/README.md   139 líneas  → coreano
docs/i18n/ru/README.md   139 líneas  → ruso
docs/i18n/ar/README.md   143 líneas  → árabe (con RTL)
```

## Validación

`mkdocs build --strict`:

- **Pasa** sin warnings ni errors.
- Como las 10 traducciones ahora linkean al `LICENSE` por URL absoluta
  de GitHub en vez de path relativo (`../../../LICENSE`), también
  desaparecieron los 9 INFO que aparecían en la pasada v5. Build
  100% silencioso ahora.

## Pendientes

1. **Workflow GH Pages** — Cuando se decida publicar la doc, falta el
   `.github/workflows/docs.yml` con `mkdocs gh-deploy`. Fuera de scope
   del docs agent (CI/CD).
2. **`TU_USUARIO`** — Reemplazar el placeholder por el handle real al
   publicar.
3. **Script de regeneración i18n** — Mover `/tmp/build_i18n_readmes.py`
   a `scripts/` y agregarlo al `Makefile` o equivalente, para que la
   próxima sincronización sea un comando. Fuera de scope (tooling).
4. **Calidad de traducciones a ja/ko/zh/ru/ar** — Funcionales y con
   terminología técnica correcta, pero un hablante nativo va a
   encontrar matices de tono mejorables. Issue tracker es el camino.
5. **`pyproject.toml > description`** — Sigue apuntando a features; la
   nueva frase-gancho del README es más narrativa. Alinear manual,
   fuera de scope.

## Cuando vuelva a cambiar el README español

Pasos:

1. Editar el README español.
2. Actualizar el diccionario `LANGS[lang]` correspondiente en el
   script de regeneración.
3. Correr el script.
4. `mkdocs build --strict` para validar.
5. Si entra un módulo nuevo, agregar fila en cada `LANGS[lang]["mod_desc"]`
   y en `MODULOS_ORDEN`.
