# Identificar

`argentina.identificar(valor)` es un **inspector universal**: recibe cualquier
string y deduce qué tipo de cosa argentina es. Devuelve un `dict` con `tipo` y
la metadata derivada, o `None` si nada matchea.

```python
import argentina as arg

arg.identificar("20-12345678-6")
# {'tipo': 'cuit', 'tipo_persona': 'persona_fisica', 'dni': '12345678', ...}

arg.identificar("C1425ABC")
# {'tipo': 'cpa', 'cp4': '1425', 'provincia': 'Ciudad Autónoma de Buenos Aires'}

arg.identificar("+54 9 351 1234567")
# {'tipo': 'telefono', 'celular': True, 'provincia': 'Córdoba', ...}

arg.identificar("AB 123 CD")
# {'tipo': 'patente', 'subtipo': 'mercosur', ...}

arg.identificar("Rosario")
# {'tipo': 'ciudad', 'provincia': 'Santa Fe', 'poblacion_2022': 1028658, ...}
```

## Tipos reconocidos

Hoy reconoce: `cuit`, `cbu`, `cpa`, `cp4`, `telefono`, `patente`, `dni`,
`departamento`, `ciudad`, `provincia`.

El orden de prueba va de más específico (formatos con dígito verificador) a
más genérico (lookup de catálogos). Si dos coinciden, gana el más restrictivo.

## Para qué sirve

Para procesar columnas mezcladas donde no sabés qué hay en cada fila —
formularios, scrapes, dumps de Excel. En vez de probar `validar_*` uno por
uno, hacés:

```python
import pandas as pd

df = pd.DataFrame({"valor": [
    "20-12345678-6",
    "C1425ABC",
    "Rosario",
    "AB 123 CD",
]})
df["info"] = df["valor"].map(arg.identificar)
df["tipo"] = df["info"].map(lambda d: d.get("tipo") if d else None)
```

## Filosofía

- Compone los módulos existentes, no inventa heurísticas propias.
- Sin red, sin pandas, sin dependencias.
- Si dudás de la inferencia, usá directamente
  `arg.personas.validar_cuit`/`arg.bancos.validar_cbu`/etc.
