# Teléfonos

`argentina.telefonos` limpia, valida y normaliza teléfonos argentinos. Maneja
los formatos más frecuentes (`+54`, `54`, `0`, `9`, `15`, paréntesis,
guiones, espacios).

## Operaciones básicas

```python
import argentina as arg

arg.telefonos.limpiar("+54 9 11 1234-5678")        # "5491112345678"
arg.telefonos.validar("+54 9 11 1234-5678")         # True
arg.telefonos.validar("011 4321-1234")               # True
arg.telefonos.validar("123")                          # False
```

## Detectar celular vs fijo

`es_celular` reconoce los marcadores clásicos `9` (internacional) y `15`
(local):

```python
arg.telefonos.es_celular("+54 9 11 1234-5678")    # True
arg.telefonos.es_celular("011 15 1234-5678")       # True
arg.telefonos.es_celular("011 4321-1234")          # False (fijo)
```

## Extraer característica

```python
arg.telefonos.extraer_caracteristica("+54 9 11 1234-5678")    # "11"
arg.telefonos.extraer_caracteristica("+54 9 351 1234567")     # "351"
```

Devuelve `"11"` para AMBA y los 3 dígitos iniciales para el resto del país
(heurística simple).

## Provincia por característica

```python
arg.telefonos.provincia_por_caracteristica("+54 9 351 1234567")    # "Córdoba"
arg.telefonos.provincia_por_caracteristica("011 4321-1234")        # "Buenos Aires"
arg.telefonos.provincia_por_caracteristica("0299 4123456")         # "Neuquén"
```

El mapeo está en `arg.telefonos.CARACTERISTICAS_PROVINCIA`:

```python
arg.telefonos.CARACTERISTICAS_PROVINCIA["11"]     # "Buenos Aires"
arg.telefonos.CARACTERISTICAS_PROVINCIA["351"]    # "Córdoba"
```

Cubre las áreas principales del país (~45 entradas). No es exhaustivo:
faltan muchas características de 4 dígitos correspondientes a localidades
chicas. Para esos casos `provincia_por_caracteristica` devuelve `None`.

## Normalizar a E.164

```python
arg.telefonos.normalizar_e164("+54 9 11 1234-5678")    # "+5491112345678"
arg.telefonos.normalizar_e164("011 4321-1234")          # "+541143211234"

# Forzar tipo cuando sabés que el dato es celular o fijo
arg.telefonos.normalizar_e164("11 1234-5678", celular=True)    # "+5491112345678"
arg.telefonos.normalizar_e164("11 4321-1234", celular=False)   # "+541143211234"
```

Útil para WhatsApp Business, servicios de SMS, etc., que típicamente
requieren formato canónico.

## Limitaciones

- **Sintáctico:** no consulta operadores ni valida que la línea exista.
- **Heurístico:** discrimina celular/fijo por patrones (`9`, `15`). Si una
  empresa usa numeración celular en un teléfono fijo (raro pero posible),
  el paquete lo clasifica como celular.
- La tabla de **característica → provincia** es aproximada y tiene
  excepciones por localidad.
