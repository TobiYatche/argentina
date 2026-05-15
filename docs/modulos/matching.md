# Matching

`argentina.matching` ofrece **matching difuso** (fuzzy) sobre los catálogos
del paquete. Cuando `lookup()` exacto falla — typos, abreviaturas no
aliasadas, variantes — `matching` encuentra el ítem más parecido.

Stdlib pura (`difflib.SequenceMatcher`), sin dependencias externas, sin
internet. Reusa los catálogos ya embebidos (provincias, departamentos,
ciudades, universidades, aglomerados).

## Cuándo usar `matching` vs `lookup`

- **`lookup()`** es exacto sobre el nombre normalizado (lowercase + sin
  tildes + alfanumérico) más una lista curada de alias. Si la entrada está
  limpia, es lo mejor: rápido y predecible.
- **`matching`** entra cuando los datos llegan sucios: Excel cargados a
  mano, formularios, scrapes de terceros. Acepta typos y abreviaturas no
  aliasadas.

Convención: cada `match_*()` intenta primero `lookup()` exacto, y solo si
falla calcula similitud.

## Provincias

```python
import argentina as arg

arg.matching.match_provincia("buennos aires")    # → Buenos Aires
arg.matching.match_provincia("cordova")          # → Córdoba
arg.matching.match_provincia("sgo del estero")   # → Santiago del Estero
arg.matching.match_provincia("mendosa")          # → Mendoza
arg.matching.match_provincia("xyz")              # → None
```

Devuelve el mismo objeto `Provincia` que devolvería `arg.provincias.lookup()`.

### Inspeccionar candidatos con score

```python
arg.matching.candidatos_provincia("cordova", n=3)
# [(Provincia(nombre='Córdoba', ...), 0.86),
#  (Provincia(nombre='Formosa', ...), 0.57),
#  (Provincia(nombre='Mendoza', ...), 0.43)]
```

## Departamentos

Los nombres de departamento se repiten entre provincias ("Capital" aparece
en muchas). Filtrar por provincia es fuertemente recomendado:

```python
arg.matching.match_departamento("gral san martin", provincia="Buenos Aires")
# Departamento(nombre='General San Martín', provincia_codigo='06', ...)

arg.matching.match_departamento("gral san martin", provincia="PBA")  # alias
# idem
```

`provincia` acepta cualquier identificador que entienda
`argentina.provincias.lookup()` (nombre, código INDEC, ISO, alias).

Sin `provincia`, el universo es los ~530 departamentos del país y se
prioriza `departamentos.lookup()` exacto antes del fuzzy.

## Ciudades

```python
arg.matching.match_ciudad("mar de plata")    # → Mar del Plata
arg.matching.match_ciudad("rosrio")          # → Rosario
```

## Universidades

```python
arg.matching.match_universidad("uba")                          # → UBA
arg.matching.match_universidad("universidad d buenos aires")   # → UBA
```

El score se calcula contra **sigla y nombre completo**, tomando el mejor de
los dos.

## Aglomerados (EPH)

```python
arg.matching.match_aglomerado("Gran Cordova")    # → Gran Córdoba
```

## Función genérica

Si tenés una lista de strings arbitraria:

```python
arg.matching.match("cordova", ["Buenos Aires", "Córdoba", "Santa Fe"])
# ('Córdoba', 0.857)

arg.matching.candidatos(
    "cordova",
    ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza"],
    n=3,
)
# [('Córdoba', 0.857), ('Mendoza', 0.43), ('Buenos Aires', 0.32)]
```

`match()` compara con normalización canónica (sin tildes, lowercase,
alfanumérico) pero devuelve el **string original** del candidato, no el
normalizado.

## Umbral

Todas las funciones `match_*` aceptan `umbral` (default `0.7`, expuesto
como `arg.matching.UMBRAL_DEFAULT`).

- Subirlo (ej. `0.85`) reduce falsos positivos.
- Bajarlo (ej. `0.5`) acepta matches más laxos.

El default es razonable, no óptimo: ajustar según el dataset.

```python
# Estricto: rechaza typos flojos.
arg.matching.match_provincia("misisones", umbral=0.99)   # None

# Pero el match exacto siempre pasa (no usa fuzzy).
arg.matching.match_provincia("Misiones", umbral=0.99)    # Misiones
```

`candidatos_*` por default usa `umbral=0.0` para que el usuario vea toda la
distribución de scores.

## Casos borde

```python
arg.matching.match_provincia(None)    # None
arg.matching.match_provincia("")       # None
arg.matching.match_provincia("xyz")    # None (sin match por encima del umbral)
```

## Performance

`difflib.SequenceMatcher` es `O(n*m)` por par. Para los volúmenes del
paquete (24 provincias, ~530 departamentos, ~30 ciudades) es instantáneo
en una consulta puntual. Para loops grandes (cientos de miles de
consultas) puede sentirse; en ese caso considerar agrupar consultas o
deduplicar antes de matchear. Hoy no hay extra opcional con backend más
rápido; se agregará si aparece la necesidad.

## Filosofía

- Sin dependencias externas.
- Sin internet.
- Reusa la misma normalización canónica que el resto del paquete.
- Cada función específica decide "qué tipo de cosa es lo buscado" — el
  módulo no inventa heurísticas para adivinar.
