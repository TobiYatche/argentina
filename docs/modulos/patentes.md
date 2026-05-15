# Patentes

`argentina.patentes` limpia, valida y formatea **patentes de vehículos
argentinos** en sus formatos vigentes:

- **Vieja**: `AAA 999` (autos previo a 2016).
- **Mercosur**: `AA 999 BB` (autos 2016+).
- **Moto vieja**: `999 AAA`.
- **Moto Mercosur**: `A 999 BBB`.

```python
import argentina as arg

arg.patentes.validar("ABC 123")        # True (vieja)
arg.patentes.validar("AB 123 CD")      # True (Mercosur)
arg.patentes.validar("123 ABC")        # True (moto vieja)
arg.patentes.validar("A999BBB")        # True (moto Mercosur)
arg.patentes.validar("XX 99 ZZ")       # False
```

## Limpieza y formato

```python
arg.patentes.limpiar("ab 123 cd")      # "AB123CD" — saca espacios y mayúscula
arg.patentes.formatear("ab123cd")      # "AB 123 CD" — formato canónico
```

## Clasificación

```python
arg.patentes.tipo("AB 123 CD")         # "mercosur"
arg.patentes.tipo("ABC 123")           # "vieja"
arg.patentes.tipo("123 ABC")           # "moto_vieja"
arg.patentes.tipo("A999BBB")           # "moto_mercosur"

arg.patentes.es_mercosur("AB123CD")    # True
arg.patentes.es_moto("123 ABC")        # True
```

## Casos borde

```python
arg.patentes.validar(None)             # False
arg.patentes.validar("")               # False
arg.patentes.tipo("no es patente")     # None
```

Solo regex de stdlib — sin red, sin consultas al RNPA, sin pandas. Valida la
**forma** de la patente, no que el vehículo exista.
