# Docs update — 2026-05-13 (v3, i18n)

Tercera pasada del agente `docs_agent`. Foco: **internacionalización del
README** a 10 idiomas además del español original.

Versión del paquete al momento del reporte: **0.3.0**.

## Pedido del usuario

> "quiero que sumes mas idiomas en la documentacion. ingles portugues francés
> por lo menos traducilo a 10 idiomas"

## Decisiones tomadas

### Scope acotado

Traduje **el README** (no toda la documentación) a 10 idiomas. Razón:

- El README es el primer (y a menudo único) contacto de un usuario nuevo
  con el paquete. Cubre el 80% de lo que necesita saber: para qué sirve,
  cómo instalarlo, ejemplo rápido, qué hay adentro, filosofía.
- Mantener `docs/modulos/`, `quickstart.md`, etc. sincronizados en 10
  idiomas sería un costo enorme con poco retorno: los nombres de funciones
  y los ejemplos de código son los mismos en cualquier idioma, y los
  módulos cambian seguido.
- La estrategia es **README como puerta multilingüe, docs detallados en
  español**. Si se necesita expandir, el patrón ya está creado.

### Selección de idiomas

Elegí cobertura amplia: 5 europeas latinas/germánicas + 4 asiáticas + 1
semítica. Total 10 (sin contar el original):

1. **en** — English (lingua franca técnica)
2. **pt** — Português (público regional inmediato; Brasil)
3. **fr** — Français (presencia académica e institucional)
4. **it** — Italiano (afinidad cultural/migratoria con Argentina)
5. **de** — Deutsch (sector tech europeo)
6. **zh** — 中文 simplificado
7. **ja** — 日本語
8. **ko** — 한국어
9. **ru** — Русский
10. **ar** — العربية (con `<div dir="rtl">` para render correcto)

### Estructura

```
docs/i18n/
├── index.md           ← landing multilingüe (sección "Idiomas" del mkdocs nav)
├── en/README.md
├── pt/README.md
├── fr/README.md
├── it/README.md
├── de/README.md
├── zh/README.md
├── ja/README.md
├── ko/README.md
├── ru/README.md
└── ar/README.md
```

Cada `<lang>/README.md` es una traducción del README español:
instalación, ejemplo rápido, tabla de módulos principales + extras,
filosofía, documentación, estado, licencia. Los bloques de código se
mantienen tal cual (`arg.provincias.lookup` se entiende en cualquier
idioma).

## Cambios concretos

### Archivos nuevos

- `docs/i18n/index.md` — landing con tabla de idiomas, banderas y links
  a cada traducción. Explica el alcance (README only) y cómo se
  mantienen sincronizados.
- `docs/i18n/en/README.md` (inglés)
- `docs/i18n/pt/README.md` (portugués)
- `docs/i18n/fr/README.md` (francés)
- `docs/i18n/it/README.md` (italiano)
- `docs/i18n/de/README.md` (alemán)
- `docs/i18n/zh/README.md` (chino simplificado)
- `docs/i18n/ja/README.md` (japonés)
- `docs/i18n/ko/README.md` (coreano)
- `docs/i18n/ru/README.md` (ruso)
- `docs/i18n/ar/README.md` (árabe, con dirección RTL)

### Archivos actualizados

- **`README.md`** — agregado al inicio un bloque de 11 banderas + links a
  los 10 idiomas + el original. Es la primera cosa que ve un visitante
  del repo en GitHub.
- **`docs/index.md`** — agregada una nota arriba con link a
  `i18n/index.md` para usuarios que llegan vía mkdocs.
- **`mkdocs.yml`** — `nav` ahora incluye una sección `Idiomas` después de
  `API reference`, con cada traducción accesible desde el sidebar.

## Lo que NO se tradujo

- `docs/quickstart.md`, `docs/instalacion.md`, `docs/filosofia.md`,
  `docs/extras.md`, `docs/api.md`.
- Las páginas `docs/modulos/<modulo>.md` (29 archivos).
- Los notebooks `notebooks/*.ipynb`.
- El `CHANGELOG.md`.

Cada traducción menciona dónde vive la documentación original en
español, así el lector que necesita más detalle sabe a dónde ir.

## Convenciones aplicadas

- **Fuente de verdad: el README español.** Las 10 traducciones se basan
  en él. Si cambia el español, hay que re-traducir las demás (próxima
  pasada del docs agent).
- **Bloques de código sin traducir.** Los identificadores
  (`arg.provincias.lookup`, `PBA`, `Córdoba`, etc.) se mantienen en
  español: forman parte de la API.
- **Tono adaptado, pero coherente.** En cada idioma intenté mantener el
  registro "directo, claro, sin marketing" del original argentino,
  ajustado a las convenciones de cada idioma (no se traduce
  literalmente "canchero" — se busca su equivalente funcional).
- **Árabe con RTL.** El archivo árabe envuelve el contenido en
  `<div dir="rtl">` para que GitHub y mkdocs lo rendericen correcto.
- **Banderas como atajo visual** sólo en el bloque del README y en el
  índice `i18n/index.md`. En el resto de la doc no se usan emojis
  (siguiendo `scripts/docs_agent.md`).

## Hallazgos / pendientes

1. **El nav de `mkdocs.yml` ya no incluye** `modulos/indices.md`,
   `modulos/empresas.md`, `modulos/municipios.md`, `modulos/localidades.md`,
   `modulos/nombres.md`. Las páginas siguen existiendo en `docs/modulos/`
   y siguen referenciadas desde `docs/api.md`. Si se quiere ocultar
   esas páginas del sidebar pero mantenerlas accesibles por URL/búsqueda,
   ya está hecho. Si fue un descuido del linter, recordá reintroducirlas
   en la próxima pasada.
2. **Mantenimiento.** Cuando se actualice el README español, el docs agent
   tiene que re-traducir los 10. Sugerencia: agregar un check en CI que
   compare el hash del README español con un hash de referencia
   versionado en cada `i18n/<lang>/`. Out of scope para el docs agent
   (toca CI).
3. **Cobertura de idiomas.** Faltan idiomas regionales con afinidad
   directa (guaraní, quechua, mapuche). Decisión consciente de no
   incluirlos: el peso de mantener traducciones de calidad en idiomas
   minoritarios sin hablantes mantenedores activos es alto. Si aparecen
   colaboradores nativos, agregarlos.
4. **`docs/i18n/index.md` y los `<lang>/README.md` NO están en el README
   español como secciones internas** — solo como banderas al inicio.
   Razón: el README español ya es corto (145 líneas) y compacto; agregar
   un bloque grande de idiomas lo ensucia.

## Próxima pasada

Cuando el README español cambie:

1. Revisar el diff.
2. Aplicar los mismos cambios a cada `docs/i18n/<lang>/README.md`.
3. Si entra una sección nueva (ej. una herramienta nueva), traducirla en
   los 10 idiomas.
4. Si cambia solo un ejemplo de código, los bloques de código se copian
   tal cual (no se traducen).
