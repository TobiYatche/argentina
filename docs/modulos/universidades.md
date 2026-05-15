# Universidades

`argentina.universidades` expone las **53 universidades nacionales argentinas**
(creadas por ley nacional) con sigla, nombre, provincia, sede y año de
fundación. Datos embebidos, sin red.

```python
import argentina as arg

arg.universidades.lookup("UBA")             # Universidad de Buenos Aires
arg.universidades.lookup("UNC")             # Universidad Nacional de Córdoba
arg.universidades.lookup("La Plata")        # UNLP (match parcial)
arg.universidades.lookup("Universidad Tecnológica Nacional")
```

`lookup` acepta sigla o nombre, es case-insensitive y tolera tildes.

## Filtros

```python
arg.universidades.por_provincia("Córdoba")    # (UNC, UNRC, UNVM)
arg.universidades.por_provincia("CABA")        # universidades de CABA
arg.universidades.por_anio(desde=2009)         # universidades nuevas
arg.universidades.por_anio(hasta=1900)         # las "históricas"
arg.universidades.listar()
```

## Atributos de `Universidad`

```python
u = arg.universidades.lookup("UBA")

u.sigla              # "UBA"
u.nombre             # "Universidad de Buenos Aires"
u.provincia_codigo   # "02"
u.provincia_nombre   # "Ciudad Autónoma de Buenos Aires"
u.sede               # "Ciudad Autónoma de Buenos Aires"
u.anio_fundacion     # 1821
u.tipo               # "nacional"
```

> Hoy `tipo` siempre vale `"nacional"` — el set no incluye universidades
> privadas ni provinciales. Está pensado para análisis del sistema
> universitario nacional.

## Atajos cruzados

`Provincia` tiene una property que evita importar este módulo:

```python
arg.provincias.CORDOBA.universidades
# (UNC, UNRC, UNVM)
```

## Fuzzy match

Para nombres mal tipeados:

```python
arg.matching.match_universidad("uba")                          # → UBA
arg.matching.match_universidad("universidad d buenos aires")   # → UBA
arg.matching.match_universidad("UNcordoba")                    # → UNC
```

## `mapping` y `como_tabla`

```python
arg.universidades.mapping("sigla", "nombre")
arg.universidades.como_tabla()
```

Stdlib pura, sin red.
