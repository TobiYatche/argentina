# Presidentes

`argentina.presidentes` cubre las **57 presidencias argentinas** desde la
Constitución de 1853 (Urquiza, 1854) hasta hoy: período, partido y tipo de
mandato (`constitucional`, `interino` o `de facto`). Segundos mandatos
aparecen como entradas separadas (Perón, CFK, Menem, Yrigoyen, Roca).

```python
import argentina as arg
from datetime import date

arg.presidentes.actual()                  # presidente vigente hoy
arg.presidentes.en(date(2003, 12, 1))     # Néstor Kirchner
arg.presidentes.en(date(1990, 1, 1))      # Menem (primer mandato)

arg.presidentes.lookup("Perón")           # primer mandato (1946)
arg.presidentes.lookup("CFK")             # alias
```

## Filtros

```python
arg.presidentes.por_partido("UCR")
arg.presidentes.por_tipo("de facto")      # 13 presidencias militares
arg.presidentes.por_tipo("constitucional")
arg.presidentes.listar()                  # las 57 entradas
```

## Atributos de `Presidente`

```python
p = arg.presidentes.lookup("Néstor Kirchner")

p.nombre              # "Néstor Carlos Kirchner"
p.desde               # date(2003, 5, 25)
p.hasta               # date(2007, 12, 10)
p.partido             # "PJ"
p.tipo                # "constitucional"
```

`@dataclass(frozen=True)`, comparable y hasheable.

## Para qué sirve

- Etiquetar series económicas o sociales por gobierno sin armar la tabla a
  mano cada vez.
- Cruzar con `argentina.economia` o `argentina.monedas` para análisis por
  período.
- Saber rápido qué presidente había en una fecha cualquiera.

```python
import argentina as arg
df["presidente"] = df["fecha"].map(
    lambda f: getattr(arg.presidentes.en(f), "nombre", None)
)
```

## Como tabla / mapping

```python
arg.presidentes.como_tabla()
# [{'nombre': '...', 'desde': ..., 'hasta': ..., 'partido': '...', 'tipo': '...'}, ...]

arg.presidentes.mapping("nombre", "partido")
```

Stdlib pura, sin red, sin pandas.
