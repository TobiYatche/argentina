# Educación

`argentina.educacion` agrupa utilidades específicas del sistema educativo
argentino: identificadores oficiales (CUE), normalización de categorías
(sector, ámbito, nivel).

## Ejemplos

```python
import argentina as arg

# CUE (Clave Única de Establecimiento)
arg.educacion.limpiar_cue("0201234-00")        # "020123400"
arg.educacion.validar_cue("020123400")          # True/False
arg.educacion.extraer_jurisdiccion_cue("020123400")    # código de jurisdicción

# Normalización de categorías
arg.educacion.normalizar_sector("público")     # forma canónica
arg.educacion.normalizar_ambito("urbano")
arg.educacion.normalizar_nivel("secundario")
```

## CUE: Clave Única de Establecimiento

Es el identificador oficial de los establecimientos educativos argentinos.
Está dividido en jurisdicción (provincia) + correlativo. `argentina.educacion`
valida el formato y permite extraer la jurisdicción.

## Normalización de categorías

Los datasets oficiales del Ministerio de Educación usan distintas formas
para los mismos conceptos (`"Público"`, `"público"`, `"estatal"`,
`"PUBLICO"`). Las funciones `normalizar_*` devuelven la forma canónica.

Ver [API reference](../api.md#argentinaeducacion) para la lista completa.
