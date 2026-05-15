# Países limítrofes

`argentina.paises_limitrofes` expone los **5 países que limitan con Argentina**
(Brasil, Bolivia, Chile, Paraguay, Uruguay) con ISO, longitud de frontera (km)
y las provincias argentinas que tocan con cada uno.

```python
import argentina as arg

arg.paises_limitrofes.lookup("Chile")          # CL
arg.paises_limitrofes.lookup("BRA")            # Brasil (por ISO-3)
arg.paises_limitrofes.lookup("uruguay")        # case-insensitive

arg.paises_limitrofes.por_provincia("Mendoza")  # → (Chile,)
arg.paises_limitrofes.por_provincia("Jujuy")    # → (Chile, Bolivia)
arg.paises_limitrofes.listar()
```

## Atributos

```python
br = arg.paises_limitrofes.lookup("Brasil")

br.codigo_iso              # "BR"
br.codigo_iso_3            # "BRA"
br.nombre                  # "Brasil"
br.frontera_km             # km de frontera con Argentina
br.provincias_argentinas   # tuple de Provincia que limitan
```

## Casos de uso

- Filtrar bases con migraciones, fronteras, comercio exterior.
- Saber rápido qué provincia argentina tiene frontera con qué país.
- Joins simples por ISO.

```python
arg.paises_limitrofes.mapping("codigo_iso", "nombre")
# {"BO": "Bolivia", "BR": "Brasil", "CL": "Chile", ...}
```

Stdlib pura, sin red, sin pandas.
