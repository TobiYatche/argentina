# Geo

`argentina.geo` es el subpaquete con herramientas **geográficas**. Está
dividido en varios submódulos según la fuente y el tipo de operación.

!!! info "Extras"
    - `argentina.geo.shapes` → necesita `[geo]` (geopandas, pyogrio).
    - `argentina.geo.basemaps` → necesita `[maps]` (folium).
    - `argentina.geo.direcciones` → necesita `[georef]` (requests).
    - `argentina.geo.mapa` → necesita `[geo,maps]` (combina shapes + basemaps).
    - `argentina.geo.postal` → placeholders, no requiere extras.

## `geo.shapes` — geometrías oficiales del IGN

Descarga polígonos de provincias y departamentos desde el **WFS oficial del
IGN**, los cachea en `~/.cache/argentina/shapes/` y devuelve `GeoDataFrame`.

```python
import argentina as arg

# Primera llamada: baja el ZIP del IGN (~45 MB provincias, ~57 MB deptos).
# Siguientes: cache hit instantáneo.
gdf = arg.geo.shapes.provincias()        # 24 polígonos
gdf = arg.geo.shapes.departamentos()     # 529 polígonos
```

Columnas del IGN: `gid`, `entidad`/`objeto`, `fna` (nombre completo), `gna`,
`nam` (nombre corto), `in1` (código INDEC), `fdc`, `sag`, `geometry`.
CRS: **EPSG:4326** (WGS 84).

Pasar `url=` permite usar mirrors propios. `overwrite=True` fuerza redescarga.

## `geo.basemaps` — fondos cartográficos argentinos

Provee tiles del **Argenmap del IGN** para usar con Folium, manteniendo la
toponimia argentina (Islas Malvinas, sector antártico).

```python
import folium
import argentina as arg

m = folium.Map(location=[-38, -64], zoom_start=4, tiles=None)
arg.geo.basemaps.add_argenmap(m)
arg.geo.basemaps.add_creditos_argentina(m)
arg.geo.basemaps.add_layer_control(m)
m.save("mapa.html")
```

## `geo.direcciones` — geocoding con Georef

```python
arg.geo.direcciones.georreferenciar(
    direccion="Av. Santa Fe 3253",
    provincia="CABA",
)
arg.geo.direcciones.coordenadas(
    direccion="Av. Santa Fe 3253",
    provincia="CABA",
)
# (-34.588..., -58.410...)
```

Llama a la **API Georef** de datos.gob.ar. Filtros opcionales por
`provincia` y `localidad` reducen falsos positivos en calles comunes (hay
muchas "Av. San Martín 100" en el país).

## `geo.mapa.mapa_de` — atajo de un paso

```python
m = arg.geo.mapa_de("Córdoba")
m                                       # se renderiza en Jupyter
m.save("cordoba.html")
```

Devuelve un Folium completo con Argenmap + polígono de la provincia +
marker en la capital + créditos + control de capas. Acepta cualquier
identificador que entienda `arg.provincias.lookup`.

Argumentos opcionales: `zoom`, `incluir_capital`, `color`.

## `geo.postal` — placeholders

Funciones planeadas para georreferenciación postal real (mapear CP a
polígono, validar contra municipio). Por ahora son placeholders explícitos
que tiran `NotImplementedError`:

- `georreferenciar_codigo_postal`
- `codigo_postal_por_direccion`
- `validar_codigo_postal_municipio`

Para validación sintáctica de códigos postales, ver [Postal](postal.md).

## Cache

Las descargas grandes (IGN) se cachean en `~/.cache/argentina/shapes/`:

```
~/.cache/argentina/
└── shapes/
    ├── provincias/
    │   ├── provincias.zip       (45 MB)
    │   └── extracted/...
    └── departamentos/
        ├── departamentos.zip    (57 MB)
        └── extracted/...
```

Se puede cambiar con `cache_dir=` o eliminar el directorio para forzar
descarga limpia.
