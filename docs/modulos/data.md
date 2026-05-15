# Data

`argentina.data` agrupa el acceso a **datasets públicos pesados**: EPH
(microdatos del INDEC) y Censo 2022 (parquets remotos vía DuckDB).

!!! warning "Extra requerido"
    Necesita `pandas`, `requests`, `pyarrow`, `duckdb`. Instalá con:

    ```bash
    pip install "argentina[data]"
    ```

    `import argentina` y `import argentina.data` no cargan estas
    dependencias — se importan recién al llamar las funciones.

## `arg.data.eph` — EPH trimestral del INDEC

Descarga los microdatos trimestrales oficiales de la **Encuesta Permanente
de Hogares (INDEC)** y los devuelve como `pandas.DataFrame`.

```python
import argentina as arg

# Personas (encuesta individual)
ind = arg.data.eph(anio=2024, periodo="trimestral", numero=1, tipo="individual")
# Hogares
hog = arg.data.eph(anio=2024, periodo="trimestral", numero=1, tipo="hogar")

print(f"{len(ind):,} personas, {len(ind.columns)} columnas")
# 46050 personas, 235 columnas
```

### Cache

La primera llamada baja el ZIP del INDEC (~3-5 MB), lo guarda en
`~/.cache/argentina/eph/T<N>_<año>/microdatos.zip`, lo extrae y lee el
`.txt`. Las siguientes llamadas son cache hits (sin red).

### Parámetros

- `anio`: año (≥ 2003).
- `periodo`: `"trimestral"` (alias: `"T"`, `"trim"`, `"trimestre"`).
  `"semestral"` queda como `NotImplementedError` (pre-2003).
- `numero`: 1-4.
- `tipo`: `"individual"` / `"personas"` o `"hogar"` / `"hogares"`.
- `cache_dir`: directorio alternativo.

### Columnas

Las columnas son las del INDEC tal cual:

| Variable | Significado |
|---|---|
| `CODUSU` | identificador de vivienda |
| `NRO_HOGAR`, `COMPONENTE` | identifican hogar y miembro |
| `ANO4`, `TRIMESTRE` | año y trimestre |
| `REGION` | 1=GBA, 40=NOA, 41=NEA, 42=Cuyo, 43=Pampeana, 44=Patagonia |
| `AGLOMERADO` | código del aglomerado urbano |
| `CH04` | sexo (1=varón, 2=mujer) |
| `CH06` | edad |
| `ESTADO` | ocupación (1=ocupado, 2=desocupado, 3=inactivo, 4=menor) |
| `P21` | ingreso de la ocupación principal |
| `PONDERA` | ponderador muestral |

Documentación completa de variables: ver el [diseño de registro de la EPH](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos)
del INDEC.

## `arg.data.censo` — Censo 2022 vía DuckDB + Parquet

Arquitectura para consultar parquets remotos sin descargar el dataset
entero: `arg.data.censo(...)` arma una query
`SELECT ... FROM read_parquet('https://...')` y DuckDB usa HTTP Range para
traer solo lo necesario.

```python
df = arg.data.censo(
    anio=2022,
    tabla="personas",
    provincia="Córdoba",      # vía arg.provincias.lookup
    departamento="14014",      # opcional
    limite=10000,
    sql_extra="edad >= 18",    # WHERE adicional
)
```

### Estado actual

El INDEC todavía **no publica** microdatos del Censo 2022 como parquets
oficiales accesibles vía HTTPS. `CENSO_PARQUETS_2022` viene vacío por
default:

```python
import argentina.data.censo as c
print(c.CENSO_PARQUETS_2022)
# {'personas': None, 'hogares': None, 'viviendas': None}
```

Para usar el módulo hoy:

```python
# 1) Configurar URL (mirror propio o cuando exista uno oficial)
c.CENSO_PARQUETS_2022["personas"] = "https://mi-mirror/personas.parquet"

# 2) o pasarla directamente
arg.data.censo(anio=2022, url="https://mi-mirror/personas.parquet", limite=100)
```

### Filtros automáticos

`provincia` y `departamento` aceptan **cualquier identificador** que
entiendan `arg.provincias.lookup` y `arg.departamentos.lookup` (nombre,
código INDEC, ISO, alias). Se traducen automáticamente al filtro SQL
correspondiente.

```python
arg.data.censo(anio=2022, tabla="personas", provincia="CABA")
# WHERE provincia_codigo = '02'

arg.data.censo(anio=2022, tabla="personas", provincia="PBA")
# WHERE provincia_codigo = '06'
```

### Alternativas mientras tanto

Para **datos agregados** del Censo 2022 ya hay APIs livianas en el paquete
base, sin necesidad de descargar nada:

- `arg.provincias.<X>.poblacion_2022` — población provincial.
- `arg.ciudades.top(n)` y `arg.ciudades.por_provincia(...)` — 33 ciudades
  principales.

Ver [Provincias](provincias.md) y [Ciudades](ciudades.md).
