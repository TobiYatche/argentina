# Propuesta: provincias_internacional

## Problema

Búsquedas en foros y guías internacionales (Wikipedia, Umbrex,
PostGrid, Smarty) repiten errores y carencias al referenciar
provincias argentinas:

1. **Conteo errado:** "Argentina tiene 23 provincias" (Umbrex, varios
   blogs) — son **24** con CABA. Error frecuente en doc
   internacional.
2. **Nombres en inglés inconsistentes:**
   `"Buenos Aires Province"`, `"Province of Buenos Aires"`,
   `"Provincia de Buenos Aires"` aparecen en datasets de FRED, World
   Bank, OECD.
3. **CABA vs "Capital Federal":** datasets pre-1996 (reforma
   constitucional) usan "Capital Federal" / "Federal Capital"; los
   actuales usan "CABA" / "Autonomous City of Buenos Aires".
   Confusión adicional con "Buenos Aires" (a secas, refiere a CABA
   o a la provincia según contexto).
4. **Códigos múltiples:** la misma provincia tiene código INDEC
   (`'06'`), letra ISO 3166-2 (`'AR-B'`), letra de patente (`'C'`
   para Capital, `'B'` para Buenos Aires), letra CPA (la primera
   del CPA), código BCRA, etc. Hoy el paquete los cubre disperso
   entre módulos.

`argentina.provincias.lookup` acepta nombres en español + algunos
aliases (PBA, CABA, BA, TDF). Pero **no acepta nombres en inglés**
ni hace el mapeo entre todos los sistemas de codificación. Para un
analista que junta datos de FRED + INDEC + Wikipedia, conciliar las
referencias es trabajo manual.

## Benchmark / paquete de referencia

- [`us.states`](https://pypi.org/project/us/) — modelo claro: cada
  estado expone múltiples identificadores (FIPS, abreviatura, nombre
  largo, capital, etc.) y `lookup` los acepta todos. Misma idea
  acá, ampliada a inglés.
- [`pycountry`](https://pypi.org/project/pycountry/) — `subdivisions`
  con códigos ISO 3166-2. Inspiración para incluir aliases ISO.
- `argentina.provincias` (ya existente) — esta propuesta lo
  **extiende sin reescribir**: nuevo módulo `provincias_internacional`
  agrega capa de aliases y mapeo de códigos cruzados, importando y
  reusando `provincias` por debajo.

## Traducción a Argentina

Un módulo `argentina.provincias_internacional` que:

- Reusa el catálogo de `provincias` (no duplica).
- Agrega aliases en inglés y formas históricas para `lookup`
  permisivo.
- Expone identificadores cruzados: INDEC, ISO 3166-2, letra patente,
  letra CPA, abreviatura comercial.
- Devuelve el mismo objeto `Provincia` que `provincias.lookup`
  (compatibilidad total).

## API propuesta

```python
import argentina as arg

# Lookup permisivo (acepta inglés, formas históricas, códigos)
arg.provincias_internacional.lookup("Buenos Aires Province")
# Provincia(codigo='06', nombre='Buenos Aires', ...)

arg.provincias_internacional.lookup("Province of Buenos Aires")
# Provincia(codigo='06', ...)

arg.provincias_internacional.lookup("Federal Capital")  # forma histórica
# Provincia(codigo='02', nombre='Ciudad Autónoma de Buenos Aires', ...)

arg.provincias_internacional.lookup("Autonomous City of Buenos Aires")
# Provincia(codigo='02', ...)

arg.provincias_internacional.lookup("AR-B")  # ISO 3166-2
# Provincia(codigo='06', ...)

arg.provincias_internacional.lookup("AR-C")  # ISO 3166-2 para CABA
# Provincia(codigo='02', ...)

# Nombre en inglés
arg.provincias_internacional.nombre_en(prov)
# 'Buenos Aires Province'

arg.provincias_internacional.nombre_en("CABA")
# 'Autonomous City of Buenos Aires'

# Tabla de identificadores cruzados para una provincia
arg.provincias_internacional.codigos("BA")
# Codigos(
#     indec='06',
#     iso_3166_2='AR-B',
#     letra_patente='B',
#     letra_cpa='B',
#     abreviatura='BA',
# )

# Listar provincias con sus nombres en inglés
arg.provincias_internacional.listar_en()
# ((Provincia(...), 'Buenos Aires Province'),
#  (Provincia(...), 'Autonomous City of Buenos Aires'),
#  ...)

# Constantes públicas para cross-reference
arg.provincias_internacional.NOMBRES_EN
# {'06': 'Buenos Aires Province', '02': 'Autonomous City of Buenos Aires', ...}

arg.provincias_internacional.NOMBRES_HISTORICOS
# {'02': ('Capital Federal', 'Federal Capital', 'Distrito Federal'), ...}
```

Reglas:
- Devuelve el **mismo dataclass `Provincia`** que `provincias.lookup`.
  No introduce una clase paralela — compatibilidad bidireccional.
- `lookup` cae primero a `provincias.lookup` (alias en español); si
  falla, prueba aliases en inglés / históricos / códigos cruzados.
  Si nada matchea: `None`.
- `nombre_en` admite `Provincia | str` como entrada.
- `Codigos` es dataclass frozen con los identificadores cruzados.
- Catálogos de aliases (inglés + históricos + códigos) viven en este
  módulo, no se ensucia el catálogo "limpio" de `provincias`.

## Archivos a modificar

- `src/argentina/provincias_internacional.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar
  `from argentina import provincias_internacional`.
- `src/argentina/provincias.py` — agregar reexport opcional con
  import diferido: `arg.provincias.lookup_intl = ...`. Mínimo, sin
  romper API actual.
- `tests/test_provincias_internacional.py` — tests.
- `docs/modulos/provincias_internacional.md` — documentación con
  tabla maestra de 24 provincias × identificadores cruzados ×
  nombres en inglés.
- `notebooks/provincias_internacional_pruebas.ipynb` — notebook
  obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura.

## Core o extra

**Core.** Cero dataset que envejezca. La lista de 24 provincias
argentinas es **constitucional** (Constitución de 1853 + reforma de
1994 para CABA); los nombres en inglés son convenciones de uso
internacional estables (FRED, OECD, World Bank); los códigos ISO
3166-2 los administra ISO con cambios extremadamente raros.

## Tests necesarios

- `lookup` para cada una de las 24 provincias con:
  - Nombre español canónico (regresión sobre `provincias.lookup`).
  - Nombre en inglés (`"Buenos Aires Province"`, etc.).
  - Forma histórica donde aplique (`"Federal Capital"` → CABA).
  - Código ISO 3166-2 (`AR-B`, `AR-C`, ...).
- `lookup` insensible a case y espacios.
- `lookup` para entrada irrelevante → `None`.
- `nombre_en(prov)` para cada provincia devuelve la forma canónica
  en inglés.
- `codigos(prov)` devuelve los 5 identificadores esperados, todos
  no-`None`.
- Test de regresión: cada `Provincia` que devuelve
  `provincias_internacional.lookup` es **el mismo objeto** (identidad,
  no solo equivalencia) que devuelve `provincias.lookup` para el
  mismo destino canonical. Garantiza no duplicación.
- `NOMBRES_EN` tiene 24 entradas, una por provincia.
- `listar_en()` devuelve 24 tuplas.
- Sin internet, sin archivos externos.

## Riesgos

- **Subjetividad de nombres en inglés.** "Buenos Aires Province" vs
  "Province of Buenos Aires" — ambos correctos. Mitigación: elegir
  uno como canónico (el más usado en datasets internacionales
  consultados: FRED, World Bank, OECD); el otro queda como alias
  reconocido pero no devuelto por `nombre_en`. Documentar el
  criterio.
- **"Buenos Aires" ambiguo.** A secas puede referir a CABA o a la
  provincia. Mitigación: `lookup("Buenos Aires")` devuelve la
  **provincia** (consistente con `provincias.lookup` actual); para
  CABA hay que usar `"CABA"`, `"Federal Capital"`, `"Autonomous City
  of Buenos Aires"`, etc. Documentar explícitamente.
- **Códigos cruzados que se mueven.** Aunque raro, ISO podría
  renombrar un código (ej. cambio de `AR-DF` a `AR-C` para CABA en
  1996). Mitigación: el módulo embebe los códigos vigentes; si
  cambian en el futuro, agregar el viejo como alias (no perder
  retrocompatibilidad).
- **Solapamiento con `provincias` actual.** Riesgo de divergencia
  futura entre los dos módulos. Mitigación: el módulo nuevo reusa
  `provincias` por debajo y solo agrega aliases; los tests de
  identidad evitan que se separen.

## Prioridad

**Media-alta.** Resuelve un gap concreto y medido (foros
internacionales tropiezan con conteos errados, nombres
inconsistentes y códigos múltiples). Implementación de baja
superficie: el catálogo de aliases ya está en cabeza, queda
sistematizarlo. Cero deuda de mantenimiento — la lista de
provincias es constitucional.

## Contexto adicional

- Originada por la búsqueda en foros (2026-05-13): error documentado
  "Argentina tiene 23 provincias" en guías internacionales, falta
  de mapeo entre códigos múltiples para analistas que cruzan
  FRED/OECD/INDEC.
- Patrón consolidado: módulo que **extiende sin reescribir**, igual
  a `formato` (que reexporta `formatear_*` de otros módulos). Misma
  filosofía acá.
- Convención `import argentina as arg` respetada.
- Sinergia con `glosario` (20): los acrónimos provinciales (PBA,
  CABA, GBA, AMBA) calzan en el glosario como entradas, mientras
  acá viven los nombres expandidos y traducciones.
