# Ciudades

`argentina.ciudades` es un set curado de las **33 ciudades principales** del
país: todas las capitales provinciales + los grandes aglomerados (Rosario,
Mar del Plata, Bahía Blanca, Comodoro Rivadavia, Concordia, Tandil, etc.).
Datos del Censo Nacional 2022 (INDEC).

## Lookup

```python
import argentina as arg

arg.ciudades.lookup("Rosario")
arg.ciudades.lookup("CABA")             # alias
arg.ciudades.lookup("mardel")           # alias para Mar del Plata
arg.ciudades.lookup("tucuman")          # alias para San Miguel de Tucumán
arg.ciudades.lookup("jujuy")            # alias para San Salvador de Jujuy
arg.ciudades.lookup("comodoro")         # alias para Comodoro Rivadavia
```

Case-insensitive, sin tildes, con aliases coloquiales.

## Atributos de `Ciudad`

```python
c = arg.ciudades.lookup("Rosario")

c.nombre              # "Rosario"
c.provincia_codigo    # "82"
c.provincia_nombre    # "Santa Fe"
c.poblacion_2022      # 1028658
c.lat                 # -32.9442
c.lon                 # -60.6505
```

## Top N por población

```python
top5 = arg.ciudades.top(5)
for c in top5:
    print(f"{c.nombre:25s}  {c.poblacion_2022:,}".replace(",", "."))

# Buenos Aires             3.121.707
# Córdoba                  1.565.112
# Rosario                  1.028.658
# La Plata                   772.618
# San Miguel de Tucumán      695.807
```

## Filtrar por provincia

```python
arg.ciudades.por_provincia("Buenos Aires")
# La Plata, Mar del Plata, Bahía Blanca, Vicente López, Tandil

arg.ciudades.por_provincia("CABA")
# Solo Buenos Aires
```

Acepta cualquier identificador que entienda `arg.provincias.lookup`.

## Iterable

```python
for c in arg.ciudades:
    print(c.nombre, c.poblacion_2022)

len(arg.ciudades)              # 33
"CABA" in arg.ciudades         # True
"Atlantis" in arg.ciudades     # False
```

## Nota sobre las poblaciones

La población corresponde al **municipio/partido/comuna**, no al aglomerado
urbano completo. Por eso:

- "Mendoza" aparece con ~115 k habitantes (la ciudad), aunque el Gran Mendoza
  tiene más de 1 millón distribuidos en varios departamentos.
- "San Juan" aparece con ~471 k (incluye el Gran San Juan).
- "Córdoba" y "Rosario" aparecen con su población municipal "real" porque
  el municipio coincide con el centro urbano.

Para análisis a nivel aglomerado, combinar con `arg.geo.shapes.departamentos()`
y unir varios partidos vecinos.

**Fuente:** Censo Nacional de Población, Hogares y Viviendas 2022 (INDEC).
