# País

`argentina.pais` agrupa **constantes invariantes** de la República Argentina:
códigos, capital, moneda, BBOX, etc. Cosas que casi nunca cambian y que es
útil tener centralizadas en vez de hardcodearlas en cada script.

```python
import argentina as arg

arg.pais.NOMBRE_OFICIAL         # "República Argentina"
arg.pais.NOMBRE                 # "Argentina"
arg.pais.CODIGO_ISO             # "AR" (ISO 3166-1 alfa-2)
arg.pais.CODIGO_ISO_3           # "ARG" (ISO 3166-1 alfa-3)
arg.pais.CODIGO_NUMERICO        # "032" (ISO 3166-1 numérico)

arg.pais.TELEFONO_PREFIJO       # "+54"
arg.pais.TLD                    # ".ar"
arg.pais.IDIOMA                 # "es-AR"

arg.pais.CAPITAL                # "Ciudad Autónoma de Buenos Aires"
arg.pais.HUSO_HORARIO           # "UTC-3"

arg.pais.MONEDA                 # "ARS"
arg.pais.MONEDA_NOMBRE          # "Peso argentino"
arg.pais.MONEDA_SIMBOLO         # "$"

arg.pais.BBOX                   # (lon_min, lat_min, lon_max, lat_max)
arg.pais.CENTRO_GEOGRAFICO      # (lat, lon)

arg.pais.POBLACION_2022             # 45_892_285 (Censo INDEC 2022)
arg.pais.SUPERFICIE_CONTINENTAL_KM2 # 2_791_810
arg.pais.CANTIDAD_PROVINCIAS        # 24
arg.pais.CANTIDAD_DEPARTAMENTOS     # 529
```

## Para qué sirve

Para no tener que recordar el código ISO, el prefijo telefónico o el BBOX
cada vez que arrancás un proyecto. También sirve cuando armás visualizaciones
y necesitás centrar un mapa o ajustar un viewport:

```python
import folium

m = folium.Map(location=arg.pais.CENTRO_GEOGRAFICO, zoom_start=4)
arg.geo.basemaps.add_argenmap(m)
```

## Por qué importa el dato de Malvinas

`SUPERFICIE_CONTINENTAL_KM2` y `POBLACION_2022` son cifras **continentales**:
no incluyen reclamos antárticos. El paquete es explícito sobre qué dato está
mirando, sin entrar en discusiones políticas. Para basemaps con toponimia
oficial argentina ver [Geo](geo.md).

Stdlib pura, sin red.
