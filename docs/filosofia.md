# Filosofía

> El objetivo no es reinventar pandas ni geopandas. El objetivo es resolver
> problemas argentinos frecuentes con una API simple y consistente.

`argentina` toma cuatro decisiones de diseño que explican casi todo lo demás.

## 1. Núcleo liviano

`pip install argentina` no instala dependencias. Cero. El paquete base usa
únicamente la librería estándar de Python.

```python
import argentina        # ~70 ms, ~4 MB de memoria, sin pandas ni nada
```

¿Por qué importa? Porque si solo querés validar un DNI o lookup una
provincia, no tiene sentido cargar `pandas`. Los módulos que requieren
deps externas las importan **dentro de las funciones**, no al inicio del
archivo.

```python
# argentina/geo/shapes.py (simplificado)
def provincias():
    import geopandas as gpd        # ← acá, no arriba
    import requests
    ...
```

Esto permite que:

- el paquete sea instalable en entornos restringidos sin compilación;
- el tiempo de import sea trivial incluso en CI;
- los usuarios elijan exactamente qué traer.

## 2. Extras opcionales por dominio

En vez de un solo `requirements.txt` gigante, hay extras nombrados:

```bash
pip install "argentina[economia]"   # pandas + requests
pip install "argentina[geo]"         # geopandas + pyogrio
pip install "argentina[maps]"        # folium
pip install "argentina[data]"        # pandas + duckdb + pyarrow
```

Si llamás una función que necesita un extra sin haberlo instalado, ves un
`ImportError` con el comando exacto:

```
ImportError: Para usar argentina.geo.shapes instalá el extra geoespacial:
pip install "argentina[geo]"
```

Ver [Extras opcionales](extras.md) para la lista completa.

## 3. API simple y predecible

Para las entidades del paquete (provincias, departamentos, ciudades) el patrón
es siempre el mismo: **constantes públicas + `lookup` flexible + dataclass
frozen**.

```python
arg.provincias.CORDOBA
arg.provincias.lookup("PBA")     # case-insensitive, sin tildes, alias
arg.provincias.lookup("AR-X")    # ISO 3166-2
arg.provincias.lookup("14")      # código INDEC
```

Los `Provincia`/`Departamento`/`Ciudad` son `@dataclass(frozen=True)`. No
hay clases con estado, ni ORM, ni magia. Si querés `pandas`, exportá vos:

```python
import pandas as pd
df = pd.DataFrame([p.__dict__ for p in arg.provincias])
```

## 4. Datos embebidos para lo chico, descarga on-demand para lo grande

Lo que pesa poco y casi nunca cambia se incluye en el paquete:

| Dataset | Tamaño | Origen |
|---|---|---|
| 24 provincias | ~1 KB | INDEC |
| 529 departamentos | ~16 KB | IGN |
| 33 ciudades principales | ~1 KB | INDEC Censo 2022 |

Lo que es grande o se actualiza periódicamente vive en cache local:

| Dataset | Tamaño | Origen | Cache |
|---|---|---|---|
| Shapes de provincias (IGN) | ~45 MB | WFS IGN | `~/.cache/argentina/shapes/` |
| Shapes de departamentos (IGN) | ~57 MB | WFS IGN | `~/.cache/argentina/shapes/` |
| Microdatos EPH (por trimestre) | ~3-5 MB | INDEC FTP | `~/.cache/argentina/eph/` |

Las descargas son **explícitas y solo cuando se llama la función**.
Importar `argentina` nunca toca la red.

## Limitaciones conocidas

- **Sin AFIP en vivo.** No consultamos APIs de AFIP ni padrones. Validamos
  CUIT/CUIL sintácticamente (dígito verificador con multiplicadores
  oficiales).
- **Sin scraping.** Todo el paquete se conecta a APIs públicas oficiales
  (INDEC, IGN, BCRA, Georef, datos.gob.ar).
- **Sin Google Maps.** Los basemaps son del IGN (Argenmap). Cuando se
  hace zoom out con un proveedor extranjero, las Islas Malvinas pueden
  aparecer rotuladas en inglés — el paquete no puede reescribir los
  tiles raster del proveedor.
- **Censo 2022:** los datos agregados están embebidos (`Provincia.poblacion_2022`,
  `Ciudad.poblacion_2022`). Los microdatos del Censo todavía no tienen una
  URL oficial pública como Parquet: la arquitectura está lista
  (`arg.data.censo` usa DuckDB + `read_parquet`) pero hay que configurar
  la URL.
