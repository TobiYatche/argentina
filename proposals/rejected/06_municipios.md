# Propuesta: municipios

> ## 🚫 RECHAZADA — no reimplementar sin fuente oficial
>
> **Motivo:** el "Listado de gobiernos locales" del INDEC tiene ~2300
> entidades, se actualiza (creaciones, fusiones, anexos) y no puede
> derivarse de los `departamentos` existentes (Buenos Aires tiene 1
> partido por depto, pero Santa Fe / Córdoba tienen varios municipios
> dentro de un mismo depto). Embeber un subset sintético es engañoso.
>
> Hubo un intento previo (2026-05-13) generando "1 municipio por
> departamento + 15 comunas CABA"; se sacó porque no es el listado
> oficial. Ver `reports/2026-05-13_correccion_honesta.md`.
>
> **Para reactivar:** bajar el CSV oficial INDEC, definir cadencia
> mínima de update anual, y solo después mover a `pending/`.
>
> **Decisión conceptual previa:** resolver el solapamiento con
> `ciudades` y `localidades` antes de implementar.

## Problema

El paquete tiene `provincias` (24 entidades) y `departamentos` (subconjunto
representativo). Falta el nivel intermedio/inferior que en Argentina es
políticamente relevante: los **gobiernos locales** (municipios y comunas).

Un departamento puede contener varios municipios; un municipio tiene su
propio intendente, presupuesto, normativa, código INDEC. El total ronda los
~2300 gobiernos locales (INDEC, "Listado de gobiernos locales").

Sin este módulo no se pueden hacer:
- Cruces de datos a nivel municipal (presupuestos provinciales asignados a
  municipios, datos electorales municipales, padrón sanitario).
- Lookup "¿qué municipio corresponde a esta dirección?" cuando se tiene
  provincia/departamento.
- Listados por provincia para análisis subnacional fino.

## Benchmark / paquete de referencia

- INDEC publica el "Listado de gobiernos locales" actualizado, con código
  INDEC, nombre, tipo (municipio / comuna / comisión de fomento), provincia,
  departamento. Es la fuente oficial.
- `argentina.departamentos` ya marca el patrón "CSV embebido + dataclass +
  lookup + `por_provincia(...)`" — `municipios` agrega un nivel más:
  `por_departamento(...)`.
- El paquete `us` tiene `us.states` pero no llega al nivel de
  counties/municipios; acá Argentina pide más granularidad que la que `us`
  cubre, por eso este módulo es necesario y no copiable directamente.

## Traducción a Argentina

Un módulo `argentina.municipios` con:
- Tabla oficial INDEC de gobiernos locales embebida como CSV.
- Dataclass `Municipio` frozen con `codigo`, `nombre`, `tipo`,
  `provincia_codigo`, `departamento_codigo`, posiblemente `categoria` (1ª /
  2ª / 3ª, donde aplique).
- `lookup` por código exacto o nombre **único en su provincia**.
- `por_provincia(...)`, `por_departamento(...)`, `listar()`.

## API propuesta

```python
import argentina as arg

# Lookup por código INDEC
arg.municipios.lookup("060854")
# Municipio(codigo='060854', nombre='Tigre', tipo='municipio',
#           provincia_codigo='06', departamento_codigo='060854', ...)

# Lookup por nombre + provincia (porque "San Martín" se repite)
arg.municipios.lookup("Tigre", provincia="BA")
# Municipio(...)

arg.municipios.lookup("San Martín")
# None  (ambiguo entre provincias)

# Filtros
arg.municipios.por_provincia("BA")
# (Municipio(...), Municipio(...), ...)

arg.municipios.por_departamento("060805")
# (Municipio(...), ...)

# Listar todo
arg.municipios.listar()  # tuple[Municipio, ...]

# Tipos disponibles (municipio, comuna, comisión de fomento, ...)
arg.municipios.tipos()  # ('municipio', 'comuna', 'comision_fomento')
```

Reglas:
- `Municipio` es dataclass frozen, mismo patrón que `Provincia` /
  `Departamento`.
- `lookup` por nombre exige unicidad: si hay duplicados a nivel país,
  devolver `None` (igual que `departamentos.lookup` con nombres duplicados
  como "Capital"). Pasar `provincia=...` para desambiguar.
- Normalización: lowercase + NFKD sin tildes + alfanumérico para el lookup
  por nombre.
- `provincia=` acepta código (`"06"`), letra ISO (`"BA"`), nombre o alias —
  mismo input que acepta `provincias.lookup`.

## Archivos a modificar

- `src/argentina/municipios.py` — módulo nuevo.
- `src/argentina/data/municipios.csv` — tabla INDEC embebida.
- `src/argentina/__init__.py` — agregar `from argentina import municipios`.
- `tests/test_municipios.py` — tests.
- `docs/modulos/municipios.md` — documentación.
- `notebooks/municipios_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. CSV + stdlib.

## Core o extra

**Core.** Datos oficiales embebidos, sin scraping ni internet. Listado en
`ROADMAP.md → Próximas ideas → municipios`.

## Tests necesarios

- `lookup` por código devuelve el municipio correcto.
- `lookup` por nombre único en su provincia devuelve el municipio.
- `lookup` por nombre ambiguo a nivel país sin `provincia=` → `None`.
- `lookup` por nombre ambiguo con `provincia=` correcta devuelve el
  esperado.
- `por_provincia("BA")` devuelve solo los de Buenos Aires; tamaño esperado
  conocido (≥ 130).
- `por_departamento("060854")` devuelve un subconjunto correcto.
- `listar()` devuelve cantidad esperada (≈ 2300, con tolerancia documentada
  en el test).
- Normalización: `lookup("tigre")` = `lookup("Tigre")` = `lookup("TIGRE")`.
- Cada `Municipio.provincia_codigo` existe en `provincias.listar()`
  (consistencia cruzada).
- Sin internet, sin archivos externos.

## Riesgos

- **Tamaño del CSV.** ~2300 filas: estimado <300 KB. Aceptable.
- **Desactualización.** Los gobiernos locales cambian (creaciones,
  fusiones). El INDEC actualiza la lista periódicamente. Mitigación: campo
  `version_indec` en la doc; ciclo de actualización del CSV explícito en
  `docs/modulos/municipios.md` (≥ 1 vez por año).
- **Heterogeneidad por provincia.** No todas las provincias tienen la misma
  estructura: Santa Fe tiene "comunas", Buenos Aires no. Mitigación: el
  campo `tipo` lo expresa explícitamente.
- **Solapamiento con `ciudades`.** El paquete ya tiene `ciudades` (con
  ~varios miles de localidades). Riesgo: confusión entre "ciudad",
  "localidad", "municipio". Mitigación: documentación clara en `municipios.md`
  explicando la diferencia (ciudad/localidad = unidad censal/geográfica;
  municipio = entidad de gobierno local). Esto se cruza con la idea
  pendiente `localidades` del ROADMAP — coordinar en una iteración
  posterior.
- **Volumen para tests.** No incluir el CSV completo en asserts; sólo
  spot-checks de filas conocidas y conteos por provincia.

## Prioridad

**Media.** Útil y bien definido, pero más nicho que `clae` o `formato`
(que tocan flujos diarios). Requiere validar el dataset oficial INDEC y
decidir el solapamiento con `ciudades` antes de implementar.

## Contexto adicional

- Originado en `ROADMAP.md → Próximas ideas → municipios` y mencionado en
  `reports/inconsistencies.md` como uno de los ítems sin propuesta concreta.
- Extiende el patrón consolidado de `provincias` → `departamentos`,
  sumando un nivel administrativo más.
- Convención `import argentina as arg` respetada.
- Antes de implementar, conviene definir junto con `localidades` (también
  pendiente en el roadmap) cómo se relacionan los conceptos
  ciudad/localidad/municipio — esa decisión es **previa** al código.
