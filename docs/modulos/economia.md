# Economía

`argentina.economia` da acceso a **493 series económicas oficiales** de
Argentina (INDEC, BCRA y SSPM), descargables desde la API de Series de
Tiempo de datos.gob.ar.

!!! warning "Extra requerido"
    Necesita `pandas` y `requests`. Instalá con:

    ```bash
    pip install "argentina[economia]"
    ```

    No se carga al hacer `import argentina` para mantener el paquete base
    liviano. Se importa explícitamente:

    ```python
    from argentina import economia
    # o
    import argentina.economia as economia
    ```

## Series macro

Wrappers directos para las más usadas:

```python
from argentina import economia

economia.ipc_nacional(start_date="2020-01-01")            # IPC general nacional
economia.ipc_nucleo(start_date="2020-01-01")              # IPC núcleo
economia.emae(start_date="2020-01-01")                    # Estimador Mensual de Actividad
economia.tipo_cambio_minorista(start_date="2024-01-01")    # BCRA minorista vendedor
```

Cada llamada devuelve un `pandas.DataFrame` con columnas `fecha` (datetime)
y `valor` (float).

## Cualquier serie del catálogo

```python
economia.serie("emae_desestacionalizada", start_date="2020-01-01")
economia.serie("ipc_nacional", start_date="2020-01-01", end_date="2024-12-31")
```

`serie(alias)` acepta cualquier clave del diccionario `economia.SERIES`.
493 series cubriendo:

- IPC base dic 2016: núcleo, regulados, estacionales, bienes, servicios,
  12 capítulos × 7 regiones.
- EMAE, IPI, ISAC, oferta y demanda globales.
- Salarios, empleo, hidrocarburos.
- Tipo de cambio (minorista), entre otros.

## Por ID directo

```python
economia.obtener_serie("148.3_INIVELNAL_DICI_M_26")
```

Útil si tenés un ID de la API que no está en el catálogo local.

## Explorar el catálogo

```python
economia.SERIES                       # dict con las 493 entradas
len(economia.SERIES)                  # 493
list(economia.SERIES.keys())[:10]     # primeros aliases
economia.SERIES["ipc_nacional"]       # metadata
```

Cada entrada del catálogo trae `id`, `descripcion`, `fuente` (INDEC/BCRA/SSPM),
`frecuencia` (mensual/trimestral/anual/etc.), `tema` y `dataset`.

## Búsqueda local

```python
economia.buscar("salario").head()
economia.buscar("petroleo")
economia.buscar("ipc")
```

`buscar(palabra)` filtra el catálogo localmente (sin red) por una palabra
que aparezca en el alias, descripción o dataset. Devuelve un `DataFrame`
con `alias`, `id`, `frecuencia`, `tema`, `descripcion`.

## Limitaciones

- **Sin caché de respuestas:** cada llamada va a la API. Si vas a hacer
  muchas llamadas con los mismos parámetros, guardá los DataFrames en disco
  (parquet/feather).
- **Sin descarga masiva:** una serie por llamada. Para bajar muchas en
  paralelo conviene paralelizar manualmente.
- **Dependencia de datos.gob.ar:** si la API está caída, las funciones
  fallan. El catálogo local (`SERIES`) sí funciona offline.
