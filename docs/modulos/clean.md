# Clean

`argentina.clean` agrupa funciones de **limpieza de texto** que usa todo el
paquete por dentro y que es útil exponer por separado.

```python
import argentina as arg

arg.clean.quitar_tildes("Córdoba")              # "Cordoba"
arg.clean.normalizar_texto("  Código   de Provincia ")  # "codigo de provincia"
arg.clean.snake_case("Código de Provincia")     # "codigo_de_provincia"
```

## Cuándo usar este módulo

- Cuando limpiás columnas de DataFrames (nombres, descripciones, claves).
- Cuando construís índices de lookup propios.
- Cuando comparás strings que pueden venir con tildes, espacios y mayúsculas
  arbitrarias.

## Algoritmo de normalización

`normalizar_texto` aplica, en orden:

1. `str(x).strip().lower()`
2. NFKD + descarte de caracteres combinantes (quita tildes)
3. Reemplazo de cualquier secuencia no alfanumérica por un espacio
4. Colapsa espacios múltiples

Es el mismo algoritmo que usa internamente `arg.provincias.lookup`,
`arg.departamentos.lookup`, `arg.ciudades.lookup`, etc. Útil cuando armás
tus propios diccionarios `texto_libre → entidad`.

## API

Las funciones disponibles son: `quitar_tildes`, `normalizar_texto`,
`snake_case` y otras utilidades de limpieza.

Ver [API reference](../api.md#argentinaclean) para la lista completa.

## Ejemplo: limpiar una columna

```python
import pandas as pd
df = pd.DataFrame({"provincia": ["Córdoba", " córdoba ", "CÓRDOBA"]})
df["norm"] = df["provincia"].map(arg.clean.normalizar_texto)
# todas las filas → "cordoba"
```
