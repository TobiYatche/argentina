# Propuesta: localidades

> ## 🚫 RECHAZADA — no reimplementar sin fuente oficial
>
> **Motivo:** BAHRA (Base de Asentamientos Humanos de la República
> Argentina) del INDEC tiene ~4000 entidades con códigos oficiales
> propios. Los códigos NO pueden inventarse ni derivarse de
> `departamentos` / `ciudades` — son códigos BAHRA específicos del
> INDEC. Embeber un subset sintético es directamente falso (los
> códigos resultantes no corresponden a la realidad).
>
> Hubo un intento previo (2026-05-13) con códigos generados; cuando el
> usuario preguntó "¿está actualizada BAHRA?" tuve que reconocer que
> ni siquiera era BAHRA. Se sacó. Ver
> `reports/2026-05-13_correccion_honesta.md`.
>
> **Para reactivar:** bajar BAHRA oficial del INDEC, definir cadencia
> de update post-censo, y solo después mover a `pending/`.
>
> **Decisión conceptual previa:** resolver solapamiento con
> `ciudades`, `municipios` y `aglomerados` antes de implementar.

## Problema

El paquete ya tiene:
- `argentina.ciudades` — catálogo de ciudades (centros poblados con
  cierto peso).
- `argentina.aglomerados` — aglomerados urbanos (unidades estadísticas
  del INDEC: 31 grandes aglomerados de la EPH).
- `argentina.municipios` (propuesto en 06) — gobiernos locales (~2300).

Falta la **localidad** como unidad censal del INDEC: ~4000 entidades con
nombre y código oficial, que no necesariamente coinciden con "ciudades"
ni con "municipios". Una localidad es la unidad geográfica más granular
del INDEC con código propio (BAHRA / Base de Asentamientos Humanos de la
República Argentina), independiente de si hay gobierno local ahí.

Hoy no se puede:
- Mapear un punto de censo / EPH a su localidad oficial.
- Listar todas las localidades de un departamento (más granular que
  ciudades).
- Hacer cruces con datos del INDEC que vienen identificados por código
  BAHRA.

## Benchmark / paquete de referencia

- INDEC publica BAHRA (Base de Asentamientos Humanos de la República
  Argentina), con código, nombre, tipo, provincia, departamento. Es la
  fuente oficial.
- `argentina.departamentos` marca el patrón "CSV embebido + dataclass +
  lookup + `por_provincia(...)`". `localidades` lo extiende sumando
  `por_departamento(...)`.
- El paquete `us` no tiene un análogo a esta granularidad — Argentina
  pide más detalle territorial que el que `us` cubre, por eso se justifica
  un módulo propio y no se puede copiar el modelo.

## Traducción a Argentina

Un módulo `argentina.localidades` con:
- Tabla BAHRA embebida como CSV (~4000 filas).
- Dataclass `Localidad` frozen con `codigo`, `nombre`, `tipo` (ciudad /
  pueblo / paraje / etc.), `provincia_codigo`, `departamento_codigo`.
- `lookup` por código exacto o nombre **único en su departamento**.
- `por_provincia(...)`, `por_departamento(...)`, `listar()`.
- Función `cercanas(...)` postergada — sería trabajo de `geo`, no acá.

## API propuesta

```python
import argentina as arg

# Lookup por código BAHRA
arg.localidades.lookup("06028010000")
# Localidad(codigo='06028010000', nombre='San Isidro', tipo='ciudad',
#           provincia_codigo='06', departamento_codigo='06028', ...)

# Lookup por nombre + departamento (porque "San José" se repite mucho)
arg.localidades.lookup("San Isidro", departamento="06028")
# Localidad(...)

arg.localidades.lookup("San José")
# None  (ambiguo a nivel país)

# Filtros
arg.localidades.por_provincia("BA")
# (Localidad(...), ...)

arg.localidades.por_departamento("06028")
# (Localidad(...), ...)

arg.localidades.por_tipo("paraje")
# (Localidad(...), ...)

arg.localidades.listar()  # tuple[Localidad, ...]

arg.localidades.tipos()  # tuple[str, ...]  ('ciudad', 'pueblo', 'paraje', ...)
```

Reglas:
- `Localidad` es dataclass frozen, mismo patrón que `Provincia` /
  `Departamento` / `Municipio`.
- `lookup` por nombre exige unicidad: si hay duplicados a nivel país,
  devolver `None` (igual que `departamentos.lookup` con "Capital").
- `provincia=` y `departamento=` aceptan código o nombre/alias —
  reutilizando los lookups existentes.
- Normalización: lowercase + NFKD sin tildes + alfanumérico.

## Archivos a modificar

- `src/argentina/localidades.py` — módulo nuevo.
- `src/argentina/data/localidades.csv` — tabla BAHRA embebida.
- `src/argentina/__init__.py` — agregar `from argentina import localidades`.
- `tests/test_localidades.py` — tests.
- `docs/modulos/localidades.md` — documentación con sección clara sobre
  la diferencia entre ciudad / aglomerado / municipio / localidad.
- `notebooks/localidades_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. CSV + stdlib.

## Core o extra

**Core.** Datos oficiales embebidos, sin scraping ni internet. Está en
`ROADMAP.md → Próximas ideas → localidades`.

## Tests necesarios

- `lookup` por código devuelve la localidad correcta.
- `lookup` por nombre único en su departamento devuelve la localidad.
- `lookup` por nombre ambiguo a nivel país → `None`.
- `lookup` por nombre ambiguo con `departamento=` correcto devuelve el
  esperado.
- `por_provincia("BA")` devuelve subconjunto correcto.
- `por_departamento("06028")` devuelve subconjunto correcto.
- `por_tipo("paraje")` filtra correctamente.
- `listar()` devuelve cantidad esperada (≈ 4000, con tolerancia
  documentada).
- Consistencia cruzada: cada `Localidad.provincia_codigo` existe en
  `provincias.listar()`; cada `departamento_codigo` existe en
  `departamentos.listar()` cuando ese departamento esté en el subconjunto
  embebido.
- Normalización: `lookup("san isidro", departamento="06028")` =
  `lookup("San Isidro", departamento="06028")`.
- Sin internet, sin archivos externos.

## Riesgos

- **Solapamiento conceptual con `ciudades` y `municipios`.** Es el
  riesgo principal. Mitigación: la doc de `localidades` debe arrancar
  con una tabla comparativa explícita:
  - localidad = unidad censal INDEC (BAHRA), más granular, ~4000.
  - ciudad = subset notable (centros poblados con peso), ya existente.
  - municipio = entidad de gobierno local (~2300), propuesta en 06.
  - aglomerado = unidad estadística de EPH (31), ya existente.
  Resolver esa decisión **antes** de implementar `localidades` y
  `municipios` en simultáneo.
- **Tamaño del CSV.** ~4000 filas con nombre/código/tipo: estimado
  <500 KB. Aceptable.
- **Desactualización.** BAHRA se actualiza tras cada censo. Mitigación:
  campo `version_bahra` en doc; cadencia de update documentada en
  `docs/modulos/localidades.md`.
- **`departamentos` actual no es exhaustivo.** La memoria del proyecto
  registra que `departamentos` es "subconjunto representativo, no
  exhaustivo". Si `localidades` referencia códigos de departamento que
  no están en `departamentos.csv`, los tests de consistencia cruzada
  fallan. Mitigación: definir si `departamentos` se completa a su
  totalidad como prerequisito, o si la consistencia cruzada se valida
  sólo donde haya match.

## Prioridad

**Alta.** Cierra un ítem explícito de `ROADMAP → Próximas ideas` y es
el complemento natural de `municipios` (propuesta 06): los dos
necesitan implementarse en orden coordinado y con la decisión
conceptual ya tomada. Si se implementa antes `municipios`, este sale
solo poco después.

## Contexto adicional

- Originado en `ROADMAP.md → Próximas ideas → localidades` y mencionado
  en `reports/inconsistencies.md` como ítem sin propuesta concreta.
- Extiende el patrón `provincias` → `departamentos` (→ `municipios`) →
  `localidades`, manteniendo la jerarquía clara.
- Convención `import argentina as arg` respetada.
- Coordinar antes de implementar con la propuesta 06 (`municipios`) para
  decidir solapamiento conceptual.
