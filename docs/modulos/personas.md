# Personas

`argentina.personas` agrupa limpieza, validación y normalización de
identificadores y nombres argentinos. Todo sintáctico — no consulta AFIP
ni padrones.

## DNI

```python
import argentina as arg

arg.personas.limpiar_dni("12.345.678")     # "12345678"
arg.personas.limpiar_dni(" 12 345 678 ")    # "12345678"

arg.personas.validar_dni("12345678")        # True
arg.personas.validar_dni("123")             # False

arg.personas.formatear_dni("12345678")      # "12.345.678"
```

## CUIT / CUIL

`validar_cuit` aplica el **algoritmo oficial** de dígito verificador
(multiplicadores `5 4 3 2 7 6 5 4 3 2`, módulo 11, con los wrap-around
`10 → 9` y `11 → 0`):

```python
arg.personas.limpiar_cuit("20-12345678-6")   # "20123456786"
arg.personas.validar_cuit("20-12345678-6")    # True/False según dígito
arg.personas.validar_cuit("20-12345678-3", digito=False)  # True (sólo largo)

arg.personas.calcular_digito_cuit("2012345678")   # devuelve el dígito correcto

arg.personas.formatear_cuit("20123456786")    # "20-12345678-6"
```

### Tipo de CUIT por prefijo

```python
arg.personas.tipo_cuit("20-12345678-6")    # "persona_fisica"
arg.personas.tipo_cuit("30-12345678-9")    # "persona_juridica"
```

| Prefijo | Tipo |
|---|---|
| 20, 23, 24, 27 | `persona_fisica` |
| 30, 33, 34 | `persona_juridica` |

### Extraer DNI desde CUIT

```python
arg.personas.extraer_dni_de_cuit("20-12345678-6")    # "12345678"
```

## Nombres

```python
arg.personas.normalizar_nombre(" María   Laura ")    # "María Laura"
arg.personas.primer_nombre("María Laura")             # "María"
arg.personas.apellido_principal("Pérez Gómez")        # "Pérez"
```

## Importante

- Todo es **sintáctico**: no consulta AFIP, no usa pandas ni APIs externas.
- Para validar identidad real hay que consultar AFIP / RENAPER por otros
  medios.
- `validar_cuit("...", digito=False)` chequea solo que tenga 11 dígitos.
  Útil cuando el dataset trae CUITs con dígitos verificadores que no son los
  oficiales (formularios viejos, errores conocidos).
