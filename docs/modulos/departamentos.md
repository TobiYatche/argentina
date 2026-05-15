# Departamentos

`argentina.departamentos` expone los **529 departamentos/partidos/comunas**
oficiales del país, según los códigos INDEC servidos por el IGN.

## Lookup

```python
import argentina as arg

arg.departamentos.lookup("06427")        # La Matanza (Buenos Aires)
arg.departamentos.lookup("14014")        # Capital (Córdoba)
arg.departamentos.lookup("Rosario")      # único en el país → Santa Fe
arg.departamentos.lookup("La Matanza")   # alias
arg.departamentos.lookup("Mar del Plata") # alias coloquial → General Pueyrredón
```

`codigo_departamento` son los 5 dígitos del INDEC: 2 de provincia + 3 de
departamento. `lookup` acepta:

- el código exacto (string de 5 dígitos);
- un nombre **único** en el set (case-insensitive, sin tildes);
- aliases comunes (`la matanza`, `la plata`, `rosario`, `mar del plata`,
  `general pueyrredon`, `rio cuarto`).

## Nombres duplicados

"Capital" se repite en muchas provincias (Córdoba, Misiones, Salta, etc.).
Para evitar resoluciones ambiguas, `lookup` devuelve `None` para nombres
ambiguos:

```python
arg.departamentos.lookup("Capital")     # None — usar código
arg.departamentos.lookup("14014")        # Capital de Córdoba ✓
arg.departamentos.lookup("La Capital")  # único: Santa Fe ✓
```

## Atributos de `Departamento`

```python
d = arg.departamentos.lookup("06427")

d.codigo_departamento     # "06427"
d.nombre                   # "La Matanza"
d.provincia_codigo         # "06"
d.provincia_nombre         # "Buenos Aires"
```

## Filtrar por provincia

```python
arg.departamentos.por_provincia("Buenos Aires")    # 135 partidos
arg.departamentos.por_provincia("PBA")              # idem, alias
arg.departamentos.por_provincia("CABA")             # 15 comunas
arg.departamentos.por_provincia("14")               # 26 deptos de Córdoba
arg.departamentos.por_provincia("AR-X")             # idem por ISO
```

`por_provincia` acepta cualquier identificador que entienda `arg.provincias.lookup`.

## Iterable

```python
for d in arg.departamentos:
    print(d.codigo_departamento, d.nombre)

len(arg.departamentos)               # 529
"La Matanza" in arg.departamentos    # True
```

## Origen de los datos

Los códigos y nombres provienen del shapefile oficial del **IGN** (Instituto
Geográfico Nacional), capa `ign:departamento`. Coinciden con los códigos
INDEC publicados oficialmente.

Para obtener los **polígonos** (geometrías reales) de los departamentos, ver
[Geo](geo.md).

## Casos borde

```python
arg.departamentos.lookup(None)                 # None
arg.departamentos.lookup("Atlantis")           # None
arg.departamentos.por_provincia("Mendoza")     # tupla con los deptos de Mendoza
arg.departamentos.por_provincia(None)          # ()
```
