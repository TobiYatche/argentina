# argentina

Simple utilities for working with Argentinian administrative and geographic data.

If you work with Argentinian databases, sooner or later you'll bump into DNIs with dots, provinces spelled five different ways, CBUs, CUITs, inconsistent addresses, or strange postal codes. This package aims to solve that without ruining your morning.

## Installation

```bash
pip install argentina
```

Optional extras:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

See [Optional extras](../../extras.md) for the full table (`maps`, `feriados`, `georef`, `elecciones`, etc.).

## Recommended import

```python
import argentina as arg
```

The documentation and examples use `import argentina as arg` because it keeps snippets short and consistent. If you copy a snippet from anywhere in the project, it just works.

Importing specific modules also works when you only need one:

```python
from argentina import provincias
import argentina.economia as economia
```

## Quick use

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## Lightweight core

The base package tries to stay lightweight. `import argentina` starts in ~70 ms and does **not** automatically import:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

Heavier features are installed as **optional extras** and their dependencies are imported lazily, only when you call the function that needs them.

## Main modules

| Module | Description |
|---|---|
| `provincias` | lookup and metadata of provinces |
| `departamentos` | lookup and metadata of departments |
| `ciudades` | cities from the 2022 Census |
| `personas` | DNI, CUIT/CUIL, and names |
| `postal` | CP4 and CPA postal codes |
| `bancos` | CBU, CVU, and alias |
| `afip` | official AFIP tables (Monotributo, VAT, Income tax) |
| `clae` | AFIP economic activities |
| `fechas` | Argentinian date parsing |
| `feriados` | official holidays (optional, via API) |
| `telefonos` | Argentinian phone numbers |
| `direcciones` | basic address parser |
| `formato` | canonical output formatting |
| `montos` | monetary string parsing |
| `indices` | IPC, UVA, CER, ICL (offline) |
| `educacion` | CUE and educational categories |
| `salud` | basic health normalization |
| `identificar` | universal inspector |
| `matching` | fuzzy matching |
| `geo` | optional geographic tools |
| `economia` | optional economic series |
| `data` | optional public datasets (EPH, Census) |

Full reference at [docs/modulos/](../../modulos/).

## Philosophy

- **Lightweight core** — `import argentina` does not load pandas or anything heavy.
- **Modular** — each module solves one domain and can be used separately.
- **Embedded data for the small stuff, on-demand downloads for the big** — provinces and departments are included; IGN shapes and EPH are downloaded and cached in `~/.cache/argentina/` on first use.
- **Explicit about what is approximate** — fuzzy matches, syntactic validations, and partial data are documented as such.
- **No scraping, no personal data** — only official public APIs (INDEC, IGN, BCRA, Georef, datos.gob.ar).

> The goal is not to reinvent pandas or geopandas. The goal is to solve frequent Argentinian problems with a simple, consistent API.

More detail at [docs/filosofia.md](../../filosofia.md).

## Documentation

The full documentation includes per-module examples, step-by-step notebooks, limitations, optional extras, and an API reference.

- **Web (mkdocs):** `https://TU_USUARIO.github.io/argentina/` *(placeholder — GitHub Pages not published yet).*
- **Local:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  Then open `http://127.0.0.1:8000`.

Suggested reading by need:

| If you want… | Go to |
|---|---|
| Executive summary | this `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| Full per-module reference | [`docs/`](../../) |
| Step-by-step interactive walkthroughs | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| Minimal copy-paste snippets | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| Catalog of economic series | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## Status

- **Version:** 0.3.0 (Beta).
- **Python:** 3.9+.
- **Sources:** INDEC (Censo 2022, EPH, economic series), IGN (cartography and Argenmap), BCRA, datos.gob.ar (Georef), argentinadatos.com (holidays).
- **Tests:** 550 automated tests (all passing as of 2026-05-13).
- **Intended for:** research, data analysis, consulting, public sector, and private projects working with Argentinian administrative data.

## License

MIT — see [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE).
