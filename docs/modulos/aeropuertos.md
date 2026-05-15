# Aeropuertos

`argentina.aeropuertos` expone los **39 aeropuertos comerciales** argentinos
con códigos **IATA** (3 letras) e **ICAO** (4 letras), coordenadas, ciudad,
provincia y tipo (internacional o cabotaje). Datos embebidos, sin red.

## Lookup flexible

```python
import argentina as arg

arg.aeropuertos.lookup("EZE")            # IATA → Ministro Pistarini
arg.aeropuertos.lookup("SAEZ")           # ICAO → idem
arg.aeropuertos.lookup("Bariloche")      # por ciudad → BRC
arg.aeropuertos.lookup("Iguazú")         # match parcial → IGR
```

Acepta IATA, ICAO, nombre del aeropuerto o de la ciudad. Es case-insensitive
y tolera tildes.

## Filtros frecuentes

```python
arg.aeropuertos.por_provincia("Chubut")
arg.aeropuertos.internacionales()
arg.aeropuertos.cabotaje()
arg.aeropuertos.listar()                 # los 39
```

`por_provincia` acepta cualquier identificador de
`argentina.provincias.lookup` (nombre, código INDEC, ISO, alias).

## Atributos de `Aeropuerto`

```python
a = arg.aeropuertos.lookup("EZE")

a.iata               # "EZE"
a.icao               # "SAEZ"
a.nombre             # "Ministro Pistarini"
a.ciudad             # "Ezeiza"
a.provincia_codigo   # "06"
a.provincia_nombre   # "Buenos Aires"
a.lat                # -34.8222
a.lon                # -58.5358
a.tipo               # "internacional"
```

Es un `@dataclass(frozen=True)`, comparable, hasheable y serializable.

## Combinación con `geo.distancia`

```python
eze = arg.aeropuertos.lookup("EZE")
ush = arg.aeropuertos.lookup("USH")
arg.geo.distancia((eze.lat, eze.lon), (ush.lat, ush.lon))   # ~2310 km
```

## `mapping` para joins rápidos

```python
arg.aeropuertos.mapping("iata", "nombre")
# {"EZE": "Ministro Pistarini", "AEP": "Jorge Newbery", ...}

arg.aeropuertos.mapping("iata", "provincia_nombre")
```

## Casos borde

```python
arg.aeropuertos.lookup(None)         # None
arg.aeropuertos.lookup("ZZZ")        # None
```

Stdlib pura, sin red.
