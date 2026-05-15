# Propuesta: clae

## Problema

CLAE (Clasificador de Actividades Económicas) es el código oficial que AFIP
usa para identificar la actividad económica de cada contribuyente. Es un
código de 6 dígitos jerárquico (sector → subsector → división → grupo → clase
→ actividad).

Hoy en el paquete `argentina`:
- No hay forma de validar si "620100" es un código CLAE válido.
- No hay forma de obtener la descripción ("Servicios de consultores en
  informática y suministros de programas de informática").
- No hay forma de listar actividades por sector ("todas las actividades de
  Construcción").
- No hay forma de navegar la jerarquía ("dame todas las actividades del
  grupo 6201").

Esto aparece constantemente en análisis fiscales, padrones de empresas, datos
de empleo (SIPA), AFIP. Hoy hay que cargar a mano el CSV oficial cada vez.

## Benchmark / paquete de referencia

- No hay paquete Python equivalente conocido. Tablas de NAICS (USA) existen
  como datasets pero no como librería.
- `argentina.departamentos` muestra el patrón "CSV embebido + dataclass +
  lookup por código o por nombre + filtros jerárquicos (`por_provincia`)" —
  exactamente lo que necesita `clae`.
- `argentina.universidades` también marca el patrón de "catálogo oficial
  pesado embebido con licencia compatible".

## Traducción a Argentina

Un módulo `argentina.clae` con:
- Tabla oficial de actividades CLAE (~1000 códigos) embebida como CSV.
- Lookup por código exacto.
- Filtros por sector / subsector / división.
- Búsqueda en descripción (substring + normalización tildes).
- Reexport desde `afip` cuando ese módulo se implemente (propuesta 02).

## API propuesta

```python
import argentina as arg

# Lookup por código de 6 dígitos
arg.clae.lookup("620100")
# Actividad(codigo='620100', descripcion='Servicios de consultores en
#           informática...', sector='J', sector_nombre='Información y
#           comunicaciones', ...)

# Validación
arg.clae.es_valido("620100")  # True
arg.clae.es_valido("999999")  # False

# Listado
arg.clae.listar()  # tuple[Actividad, ...]
arg.clae.por_sector("J")  # actividades del sector Información y comunicaciones
arg.clae.por_grupo("6201")  # actividades del grupo 6201

# Búsqueda por descripción
arg.clae.buscar("consultoría informática")
# [Actividad(...), Actividad(...), ...]

# Sectores (nivel más alto)
arg.clae.sectores()  # [Sector(letra='A', nombre='Agricultura...'), ...]
```

Reglas:
- `Actividad` y `Sector` son dataclasses frozen.
- `lookup` acepta el código como `str` o `int`; normaliza a `str` de 6 dígitos
  con padding (`62100` → `"062100"` si tiene sentido, o `ValueError` si no).
- `buscar` usa la misma normalización del paquete (lowercase + NFKD sin
  tildes) en ambos lados del match.

## Archivos a modificar

- `src/argentina/clae.py` — módulo nuevo.
- `src/argentina/data/clae.csv` — tabla oficial AFIP (código, descripción,
  sector, sector_nombre, grupo).
- `src/argentina/__init__.py` — agregar `from argentina import clae`.
- `tests/test_clae.py` — tests.
- `docs/modulos/clae.md` — documentación.
- `notebooks/clae_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

Si la propuesta 02 (`afip`) ya está implementada al momento de hacer este
módulo: agregar reexports `arg.afip.clae_lookup`, `arg.afip.clae_buscar` con
import diferido para no acoplar afip ↔ clae.

## Dependencias

Ninguna. CSV + stdlib.

## Core o extra

**Core.** Datos oficiales embebidos, sin scraping ni internet. Listado en
`ROADMAP.md → Próximas ideas → clae`.

## Tests necesarios

- `lookup("620100")` devuelve la actividad correcta.
- `lookup` con padding de ceros funciona consistentemente.
- `lookup` de código inexistente devuelve `None`.
- `es_valido` separa códigos del catálogo oficial de los inventados.
- `por_sector("J")` devuelve solo actividades del sector J.
- `por_grupo("6201")` devuelve subconjunto correcto.
- `buscar("informática")` y `buscar("Informatica")` devuelven el mismo
  resultado (normalización).
- `sectores()` devuelve exactamente los sectores oficiales (A-S según CLAE).
- Sin internet, sin archivos externos.

## Riesgos

- **Tamaño del CSV.** ~1000 filas con descripciones largas: estimado <500 KB.
  Aceptable.
- **Versión del clasificador.** Existen CLAE 2010 y CLAE 2018 (actualizado).
  Mitigación: embeber la versión vigente y dejar un campo `version` en el
  dataclass. Documentar la versión usada.
- **Solapamiento con `afip`.** Sin coordinación, `afip.clae_*` y `clae.*`
  podrían divergir. Mitigación: `afip` solo reexporta, no reimplementa.
  Misma decisión que tomamos en 02 con CUIT (la implementación canónica vive
  en `personas`, `afip` reexporta).

## Prioridad

**Alta.** Encaja directamente con `afip` (propuesta 02): los dos pertenecen
al universo fiscal-económico y se usan juntos en la práctica. Implementación
mecánica (datos + lookup), bajo riesgo, alto valor para usuarios de datos
oficiales argentinos.

## Contexto adicional

- Originado en `ROADMAP.md → Próximas ideas → clae` y mencionado en
  `reports/inconsistencies.md` como uno de los ítems sin propuesta concreta.
- Sigue el patrón validado por `departamentos`/`universidades`:
  catálogo oficial + dataclass + lookup + filtros + búsqueda por texto.
- Convención `import argentina as arg` respetada.
