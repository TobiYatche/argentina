# argentina

**🌐 Languages / Idiomas:**
[Español](README.md) ·
[English](docs/i18n/en/README.md) ·
[Português](docs/i18n/pt/README.md) ·
[Français](docs/i18n/fr/README.md) ·
[Italiano](docs/i18n/it/README.md) ·
[Deutsch](docs/i18n/de/README.md) ·
[中文](docs/i18n/zh/README.md) ·
[日本語](docs/i18n/ja/README.md) ·
[한국어](docs/i18n/ko/README.md) ·
[Русский](docs/i18n/ru/README.md) ·
[العربية](docs/i18n/ar/README.md)

---

Utilidades simples para trabajar con datos administrativos y geográficos de Argentina.

Si trabajás con bases argentinas, tarde o temprano aparecen DNIs con puntos,
provincias escritas de cinco maneras distintas, CBUs, CUITs, direcciones
inconsistentes o códigos postales raros. Este paquete intenta resolver esas
cosas sin hacerte perder la mañana.

## Instalación

```bash
pip install argentina
```

Extras opcionales:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

Ver [Extras opcionales](docs/extras.md) para la tabla completa
(`maps`, `feriados`, `georef`, `elecciones`, etc.).

## Import recomendado

```python
import argentina as arg
```

La documentación y los ejemplos usan `import argentina as arg` porque
mantiene los ejemplos cortos y consistentes. Si copiás un snippet de
cualquier lado del proyecto, funciona tal cual.

También es válido importar módulos específicos cuando solo necesitás uno:

```python
from argentina import provincias
import argentina.economia as economia
```

## Uso rápido

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## Core liviano

El paquete base intenta mantenerse liviano. `import argentina` arranca en
~70 ms y **no** importa automáticamente:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

Las funcionalidades más pesadas se instalan como **extras opcionales** y
sus dependencias se importan de forma diferida, solo cuando llamás a la
función que las necesita.

## Módulos principales

| Módulo | Descripción |
|---|---|
| `provincias` | lookup y metadata de provincias |
| `departamentos` | lookup y metadata de departamentos |
| `ciudades` | ciudades del Censo 2022 |
| `personas` | DNI, CUIT/CUIL y nombres |
| `postal` | CP4 y CPA |
| `bancos` | CBU, CVU y alias |
| `afip` | tablas oficiales AFIP (Monotributo, IVA, Ganancias) |
| `clae` | actividades económicas AFIP |
| `fechas` | parseo de fechas argentinas |
| `feriados` | feriados oficiales (opcional, vía API) |
| `telefonos` | teléfonos argentinos |
| `direcciones` | parser básico de direcciones |
| `formato` | formateo canónico de salida |
| `montos` | parseo de strings monetarios |
| `indices` | IPC, UVA, CER, ICL offline |
| `educacion` | CUE y categorías educativas |
| `salud` | normalización básica de salud |
| `identificar` | inspector universal |
| `matching` | matching difuso |
| `geo` | herramientas geográficas opcionales |
| `economia` | series económicas opcionales |
| `data` | datasets públicos opcionales (EPH, Censo) |

Más detalle en [docs/modulos/](docs/modulos/).

## Filosofía

- **Core liviano** — `import argentina` no carga pandas ni nada pesado.
- **Modular** — cada módulo resuelve un dominio y se puede usar por
  separado.
- **Datos embebidos para lo chico, descarga on-demand para lo grande** —
  provincias y departamentos vienen adentro; shapes IGN y EPH se bajan y
  cachean en `~/.cache/argentina/` la primera vez.
- **Explícito sobre lo aproximado** — los matches difusos, las
  validaciones sintácticas y los datos parciales se documentan como
  tales.
- **Sin scraping ni datos personales** — solo APIs públicas oficiales
  (INDEC, IGN, BCRA, Georef, datos.gob.ar).

> El objetivo no es reinventar pandas ni geopandas. El objetivo es
> resolver problemas argentinos frecuentes con una API simple y
> consistente.

Más detalle en [docs/filosofia.md](docs/filosofia.md).

## Documentación

La documentación completa incluye ejemplos por módulo, notebooks paso a
paso, limitaciones, extras opcionales y API reference.

- **Web (mkdocs):** `https://TU_USUARIO.github.io/argentina/`
  *(placeholder — GitHub Pages todavía no publicado).*
- **Local:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  Abre `http://127.0.0.1:8000`.

Lectura sugerida según necesidad:

| Si querés… | Andá a |
|---|---|
| Resumen ejecutivo | este `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| Referencia completa por módulo | [`docs/`](docs/) |
| Recorridos interactivos paso a paso | [`notebooks/`](notebooks/README.md) |
| Snippets mínimos copy-paste | [`examples/`](examples/README.md) |
| Catálogo de series económicas | [`SERIES_DISPONIBLES.md`](SERIES_DISPONIBLES.md) |

## Estado

- **Versión:** 0.3.0 (Beta).
- **Python:** 3.9+.
- **Fuentes:** INDEC (Censo 2022, EPH, series económicas), IGN
  (cartografía y Argenmap), BCRA, datos.gob.ar (Georef),
  argentinadatos.com (feriados).
- **Tests:** 550 tests automatizados (pasan todos al 2026-05-13).
- **Pensado para:** investigación, análisis de datos, consultoría,
  sector público y proyectos privados que tocan datos administrativos
  argentinos.

## Licencia

MIT — ver [LICENSE](LICENSE).
