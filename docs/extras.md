# Extras opcionales

El paquete base es liviano: `pip install argentina` no instala
dependencias. Cada módulo que necesita librerías externas las pide vía
un **extra** opcional.

## Tabla completa

| Extra | Comando | Trae | Habilita |
|---|---|---|---|
| `economia` | `pip install "argentina[economia]"` | `pandas`, `requests` | Series económicas (IPC, EMAE, BCRA, SSPM) |
| `geo` | `pip install "argentina[geo]"` | `geopandas`, `requests`, `pyogrio` | Geometrías del IGN como `GeoDataFrame` |
| `maps` | `pip install "argentina[maps]"` | `folium` | Mapas interactivos con Argenmap |
| `georef` | `pip install "argentina[georef]"` | `requests` | Geocoding con Georef (datos.gob.ar) |
| `feriados` | `pip install "argentina[feriados]"` | `requests` | Calendario de feriados oficiales |
| `elecciones` | `pip install "argentina[elecciones]"` | `pandas`, `requests` | Datos electorales argentinos |
| `data` | `pip install "argentina[data]"` | `pandas`, `requests`, `pyarrow`, `duckdb` | EPH (INDEC) y Censo 2022 |
| `dev` | `pip install "argentina[dev]"` | `pytest`, `ruff`, `build`, `twine`, `mkdocs`, `mkdocs-material`, `mkdocstrings` | Desarrollo, tests y docs |

## Cómo se combinan

Podés instalar varios extras de una:

```bash
pip install "argentina[economia,geo,maps]"
pip install "argentina[data,geo,maps]"
pip install "argentina[geo,maps,georef,feriados]"
```

## Qué pasa si falta un extra

Si llamás una función que requiere un extra que no instalaste, vas a ver un
`ImportError` con el comando exacto:

```python
>>> import argentina as arg
>>> arg.geo.shapes.provincias()
Traceback (most recent call last):
  ...
ImportError: Para usar argentina.geo.shapes instalá el extra geoespacial:
pip install "argentina[geo]"
```

## Por qué se hizo así

- **Tiempo de import del paquete base.** `import argentina` carga en
  ~70 ms y usa ~4 MB. Si todo fuera dependencia base, sería ~1 segundo y
  ~36 MB (porque `pandas` solo ya pesa eso).
- **Instalaciones más chicas.** El núcleo cabe en ~80 KB. Algunos
  entornos restringidos (Lambda, embebidos, etc.) no pueden instalar
  `geopandas` o `duckdb`.
- **Claridad sobre qué hace cada cosa.** El extra dice exactamente qué
  habilita: si pediste `[geo]` ya sabés que vas a poder usar shapefiles.

Ver [Filosofía](filosofia.md) para más detalle.
