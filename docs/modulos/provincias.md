# Provincias

`argentina.provincias` expone las **24 provincias** argentinas con metadata
oficial, lookup flexible y constantes públicas. Datos embebidos, sin red.

## Lookup flexible

```python
import argentina as arg

arg.provincias.lookup("Córdoba")    # con tilde
arg.provincias.lookup("cordoba")    # sin tilde
arg.provincias.lookup("PBA")        # alias
arg.provincias.lookup("CABA")       # alias
arg.provincias.lookup("14")         # código INDEC
arg.provincias.lookup("AR-X")       # ISO 3166-2
arg.provincias.lookup("TDF")        # alias Tierra del Fuego
```

`lookup` es case-insensitive y normaliza tildes y caracteres no alfanuméricos.
Devuelve un objeto `Provincia` o `None` si no se encuentra.

## Constantes públicas

Cada provincia está expuesta como atributo del módulo:

```python
arg.provincias.BUENOS_AIRES
arg.provincias.CORDOBA
arg.provincias.CABA                                  # alias de CIUDAD_AUTONOMA_DE_BUENOS_AIRES
arg.provincias.CIUDAD_AUTONOMA_DE_BUENOS_AIRES
arg.provincias.TIERRA_DEL_FUEGO
```

## Atributos de `Provincia`

```python
p = arg.provincias.CORDOBA

p.nombre              # "Córdoba"
p.codigo_indec        # "14"
p.iso_id              # "AR-X"
p.region              # "Pampeana"
p.capital             # "Córdoba"
p.capital_lat         # -31.4201
p.capital_lon         # -64.1888
p.poblacion_2022      # 3840905 (Censo INDEC 2022)
```

Es un `@dataclass(frozen=True)`, así que cualquier provincia se puede comparar,
usar como clave de dict, hashear, etc.

## Iterable

El módulo soporta iteración directa:

```python
for p in arg.provincias:
    print(p.nombre, p.poblacion_2022)

len(arg.provincias)              # 24
"PBA" in arg.provincias           # True
"Atlantis" in arg.provincias      # False
```

## Listado completo

```python
arg.provincias.listar()           # tuple[Provincia, ...]
arg.provincias.PROVINCIAS         # equivalente, expuesto directo
```

## Aliases reconocidos por `lookup`

Más allá del nombre, código INDEC e ISO:

| Alias | Resuelve a |
|---|---|
| `PBA`, `bs as`, `provincia de buenos aires` | Buenos Aires |
| `CABA`, `Capital Federal`, `Ciudad de Buenos Aires` | Ciudad Autónoma de Buenos Aires |
| `TDF`, `Tierra del Fuego, Antártida e Islas del Atlántico Sur` | Tierra del Fuego |

## Casos borde

```python
arg.provincias.lookup(None)       # None
arg.provincias.lookup("")          # None
arg.provincias.lookup("Patagonia") # None (es región, no provincia)
arg.provincias.lookup("99")        # None (código inexistente)
```

## Ejemplo: ranking por población

```python
top5 = sorted(arg.provincias, key=lambda p: p.poblacion_2022, reverse=True)[:5]
for p in top5:
    print(f"{p.nombre:35s}  {p.poblacion_2022:,}".replace(",", "."))

# Buenos Aires                          17.569.053
# Córdoba                                3.840.905
# Santa Fe                               3.556.522
# Ciudad Autónoma de Buenos Aires        3.121.707
# Mendoza                                 2.014.533
```

**Fuente de datos:** Censo Nacional de Población, Hogares y Viviendas 2022 (INDEC).
