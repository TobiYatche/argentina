# Fechas

`argentina.fechas` ofrece utilidades para fechas argentinas: parseo de
formatos comunes (`dd/mm/aaaa`), nombres de meses en español, días hábiles,
etc.

## Casos de uso típicos

- Parsear cadenas en formato argentino (`12/05/2024`) sin confusiones con
  el formato estadounidense (`MM/DD/YYYY`).
- Calcular fechas relativas a feriados o fines de semana (combinando con
  [`argentina.feriados`](feriados.md)).
- Formatear fechas con nombres de mes en español.

## Ejemplo básico

```python
import argentina as arg

# (Ejemplos genéricos: ver API reference para la lista exacta de funciones.)
arg.fechas.parsear("12/05/2024")
arg.fechas.formatear_es(date(2024, 5, 12))
```

Ver [API reference](../api.md#argentinafechas) para la lista completa de
funciones expuestas.

## Combinación con feriados

```python
from datetime import date
import argentina as arg

# Si el módulo expone hábil/no_hábil:
es_habil = arg.fechas.es_dia_habil(date(2024, 5, 25))   # False (feriado patrio)
```

Para el calendario completo de feriados oficiales, ver
[`argentina.feriados`](feriados.md) (requiere extra `[feriados]`).
