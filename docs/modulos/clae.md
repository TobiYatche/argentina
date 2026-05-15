# CLAE

`argentina.clae` expone el **Clasificador de Actividades Económicas**
oficial de AFIP — códigos de 6 dígitos jerárquicos que identifican la
actividad económica de cada contribuyente.

> **Subset CLAE-2018, no exhaustivo:** la base embebida es ~120 códigos
> representativos. El catálogo completo de AFIP tiene ~1000.
> Descripciones y jerarquía reflejan la nomenclatura pública pero pueden
> tener variaciones menores respecto al texto oficial. Para uso fiscal o
> de cumplimiento, **verificar siempre contra el Formulario 883 de AFIP**
> antes de reportar un código.

## Estructura jerárquica

- `codigo` — 6 dígitos.
- `sector` — letra A-T (nivel más alto).
- `grupo` — 4 dígitos (intermedio).
- `descripcion` — texto oficial.

## Lookup

```python
import argentina as arg

arg.clae.lookup("620100")
# Actividad(codigo='620100', descripcion='Servicios de consultores en
#           informática...', sector='J', sector_nombre='Información y
#           comunicaciones', grupo='6201')

arg.clae.lookup(620100)     # también acepta int
arg.clae.lookup("999999")   # None

arg.clae.es_valido("620100")   # True
arg.clae.es_valido("999999")   # False
```

## Filtros

```python
# Todas las actividades del sector J
arg.clae.por_sector("J")

# Todas las del grupo 6201
arg.clae.por_grupo("6201")

# Búsqueda por descripción (substring normalizado, sin tildes)
arg.clae.buscar("informática")
arg.clae.buscar("informatica")   # mismo resultado
```

## Sectores

```python
for s in arg.clae.sectores():
    print(s.letra, s.nombre)
# A Agricultura ganadería caza...
# B Explotación de minas y canteras
# C Industria manufacturera
# ...
```

## Listado completo

```python
arg.clae.listar()            # tuple[Actividad, ...]
arg.clae.como_tabla()        # list[dict]  apto para pandas
```

El módulo es iterable: `for a in arg.clae: ...`, `len(arg.clae)`,
`"620100" in arg.clae`.

## Cobertura

Los códigos embebidos cubren las principales actividades de:

- Agropecuario (sector A)
- Minería (B)
- Industria manufacturera (C)
- Energía (D), agua/residuos (E)
- Construcción (F)
- Comercio (G), transporte (H), gastronomía (I)
- TIC y software (J)
- Finanzas (K), inmobiliarias (L)
- Servicios profesionales (M), administrativos (N)
- Administración pública (O), enseñanza (P), salud (Q)
- Recreación (R), otros servicios (S, T)

Si el código que buscás no está, abrí issue con el código y la
descripción oficial — el subset crece on-demand.

## Filosofía

- Sin dependencias externas (CSV + stdlib).
- Sin internet.
- Datos embebidos versionados con el paquete.
- Coordinado con `arg.afip` cuando ese módulo está implementado
  (consultas fiscales-económicas viven juntas).
