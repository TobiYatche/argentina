# Postal

`argentina.postal` valida y parsea códigos postales argentinos en sus dos
formatos vigentes.

## Formatos soportados

- **CP4** — código postal tradicional de 4 dígitos (ej. `"1425"`).
- **CPA** — Código Postal Argentino de 8 caracteres: letra de provincia +
  4 dígitos + 3 letras (ej. `"C1425ABC"`).

## Limpiar y validar

```python
import argentina as arg

arg.postal.limpiar_codigo_postal(" c1425 abc ")    # "C1425ABC"
arg.postal.validar_cp4("1425")                       # True
arg.postal.validar_cpa("C1425ABC")                   # True

# tipo_codigo_postal discrimina:
arg.postal.tipo_codigo_postal("1425")         # "cp4"
arg.postal.tipo_codigo_postal("C1425ABC")     # "cpa"
arg.postal.tipo_codigo_postal("abc")          # None
```

## Extraer CP4 a partir del CPA

```python
arg.postal.extraer_cp4("C1425ABC")    # "1425"
arg.postal.extraer_cp4("1425")        # "1425"
```

Útil cuando tu sistema downstream solo entiende códigos de 4 dígitos pero los
datos vienen con CPAs completos.

## Provincia por CPA

La letra inicial del CPA identifica la jurisdicción postal:

```python
arg.postal.letra_provincia("C1425ABC")     # "C"
arg.postal.provincia_por_cpa("C1425ABC")    # "Ciudad Autónoma de Buenos Aires"
arg.postal.provincia_por_cpa("X5000AAA")    # "Córdoba"
```

### Tabla `CPA_PROVINCIAS`

```python
arg.postal.CPA_PROVINCIAS["X"]    # "Córdoba"

# 24 letras (una por provincia):
# A=Salta, B=Buenos Aires, C=CABA, D=San Luis, E=Entre Ríos,
# F=La Rioja, G=Sgo del Estero, H=Chaco, J=San Juan, K=Catamarca,
# L=La Pampa, M=Mendoza, N=Misiones, P=Formosa, Q=Neuquén,
# R=Río Negro, S=Santa Fe, T=Tucumán, U=Chubut, V=Tierra del Fuego,
# W=Corrientes, X=Córdoba, Y=Jujuy, Z=Santa Cruz
```

## Validación cruzada con `arg.provincias`

```python
arg.postal.validar_cpa_provincia("X5000AAA", "Córdoba")           # True
arg.postal.validar_cpa_provincia("X5000AAA", "Buenos Aires")      # False (mal)
arg.postal.validar_cpa_provincia("B1900AAA", "PBA")                # True (alias)
arg.postal.validar_cpa_provincia("S2000AAA", "santa fe")           # True (case-insensitive)
```

Cualquier identificador que entienda `arg.provincias.lookup` es válido como
segundo argumento.

## Limitación

Todo es **sintáctico**: el paquete no valida que el código existe
físicamente, ni que pertenece a una calle real. Para georreferenciación
postal real (mapear CP a polígono, validar contra un municipio existente),
ver los placeholders en `arg.geo.postal`.
