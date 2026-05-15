# Aglomerados

`argentina.aglomerados` decodifica los **aglomerados urbanos de la EPH**
(INDEC). La variable `AGLOMERADO` de los microdatos es un código numérico —
este módulo lo convierte en nombre y provincia.

```python
import argentina as arg

arg.aglomerados.lookup(32)                  # Ciudad de Buenos Aires
arg.aglomerados.lookup("Mar del Plata")     # código 34
arg.aglomerados.por_provincia("Buenos Aires")
# (Gran La Plata, Bahía Blanca - Cerri, Partidos del GBA, Mar del Plata)
```

Útil cuando trabajás con los microdatos que devuelve `argentina.data.eph(...)`:
en vez de cargar la tabla de aglomerados aparte, hacés el join directo.

## Atributos de `Aglomerado`

```python
a = arg.aglomerados.lookup(32)

a.codigo              # 32
a.nombre              # "Ciudad de Buenos Aires"
a.provincia_codigo    # "02"
a.provincia_nombre    # "Ciudad Autónoma de Buenos Aires"
```

## Cruce con `provincias`

Cada `Provincia` tiene atajos:

```python
arg.provincias.CORDOBA.aglomerados
# (Gran Córdoba, Río Cuarto)
```

## `mapping` para joins

```python
arg.aglomerados.mapping("codigo", "nombre")
# {32: "Ciudad de Buenos Aires", 33: "Partidos del GBA", ...}
```

Ideal para mergear contra una columna `AGLOMERADO` en un `DataFrame`.

## Casos borde

```python
arg.aglomerados.lookup(None)        # None
arg.aglomerados.lookup(999)         # None
```

Stdlib pura, sin red.
