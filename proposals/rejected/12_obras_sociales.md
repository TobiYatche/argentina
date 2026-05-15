# Propuesta: obras_sociales

## Problema

`argentina.salud` cubre normalizaciones básicas (sexo, tipo
documento, matrícula) y grupos etarios. `argentina.bancos` usa el
padrón BCRA como catálogo oficial de entidades financieras.

Falta el **catálogo oficial de obras sociales argentinas**: el RNOS
(Registro Nacional de Obras Sociales) publicado por la
Superintendencia de Servicios de Salud. Es un padrón cerrado de ~280
obras sociales sindicales, de personal de dirección, y monotributistas,
con:
- Código RNOS (4 dígitos).
- Razón social oficial.
- CUIT.
- Tipo (sindical / dirección / monotributo / convencionada / etc.).
- Estado (activa / suspendida / cancelada).

Hoy no hay forma en el paquete de:
- Validar que "OSDE" sea una obra social registrada.
- Mapear código RNOS → razón social (en padrones AFIP/SIPA viene el
  código numérico).
- Filtrar las obras sociales activas hoy.
- Saber el CUIT de una obra social.

## Benchmark / paquete de referencia

- `argentina.bancos` marca el patrón exacto: padrón oficial cerrado
  + dataclass frozen + lookup + filtros + reuso de
  `personas.limpiar_cuit`. `obras_sociales` lo replica con el padrón
  RNOS.
- `argentina.universidades` también sigue el mismo patrón con CUIT y
  denominación oficial.
- No hay paquete Python equivalente conocido. Estudios y obras
  sociales mantienen el padrón en Excel internos.

## Traducción a Argentina

Un módulo `argentina.obras_sociales` con:
- Padrón RNOS embebido como CSV.
- Dataclass `ObraSocial` frozen con `codigo_rnos`, `denominacion`,
  `cuit`, `tipo`, `estado`.
- Lookup por código RNOS o por CUIT.
- Filtros por tipo, estado, y búsqueda por denominación.
- Reexport opcional desde `salud` para descubribilidad
  (`arg.salud.obra_social_lookup`).

## API propuesta

```python
import argentina as arg

# Lookup por código RNOS
arg.obras_sociales.lookup("1-2700-1")
# ObraSocial(codigo_rnos='1-2700-1', denominacion='OSDE',
#            cuit='30546741253', tipo='direccion', estado='activa')

# Lookup por CUIT
arg.obras_sociales.por_cuit("30-54674125-3")
# ObraSocial(...)

# Listados
arg.obras_sociales.listar()  # tuple[ObraSocial, ...]
arg.obras_sociales.activas()  # solo estado='activa'

arg.obras_sociales.por_tipo("sindical")
arg.obras_sociales.por_tipo("direccion")

# Búsqueda en denominación
arg.obras_sociales.buscar("osde")
# [ObraSocial(...)]

arg.obras_sociales.buscar("personal civil")
# [ObraSocial(...), ObraSocial(...)]

# Validación
arg.obras_sociales.es_obra_social("30-54674125-3")  # True (por CUIT)
arg.obras_sociales.es_obra_social("1-2700-1")       # True (por código)

# Metadata
arg.obras_sociales.tipos()   # ('sindical', 'direccion', 'monotributo',
                             #  'convencionada', 'estatal')
arg.obras_sociales.estados() # ('activa', 'suspendida', 'cancelada')
```

Reglas:
- `ObraSocial` es dataclass frozen, mismo patrón que el resto del
  paquete.
- `lookup` acepta el código RNOS con o sin guiones, normaliza
  internamente (mismo patrón que `personas.limpiar_cuit`).
- `por_cuit` reusa `personas.limpiar_cuit` para normalizar el input.
- `buscar` usa normalización lowercase + NFKD sin tildes.
- Cada `ObraSocial.cuit` pasa `personas.validar_cuit` — validar en el
  test, no en runtime.

## Archivos a modificar

- `src/argentina/obras_sociales.py` — módulo nuevo.
- `src/argentina/data/obras_sociales.csv` — padrón RNOS embebido.
- `src/argentina/__init__.py` — agregar
  `from argentina import obras_sociales`.
- `src/argentina/salud.py` — reexports opcionales con import diferido:
  `arg.salud.obra_social_lookup`, `arg.salud.obras_sociales_activas`.
  NO duplicar lógica.
- `tests/test_obras_sociales.py` — tests.
- `docs/modulos/obras_sociales.md` — documentación, con sección clara
  sobre el carácter snapshot del dataset y cadencia de actualización.
- `notebooks/obras_sociales_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. CSV + stdlib. Reuso de `personas.limpiar_cuit` y
`personas.validar_cuit` (ya en core).

## Core o extra

**Core.** Padrón oficial cerrado, embebido, sin scraping ni internet.
~280 filas, CSV muy chico.

## Tests necesarios

- `lookup("1-2700-1")` devuelve OSDE.
- `lookup` con código sin guiones / con espacios / case mixto funciona.
- `lookup` de código inexistente → `None`.
- `por_cuit` con CUIT registrado devuelve la obra social.
- `por_cuit` con CUIT sin guiones / con espacios funciona (reuso de
  `personas.limpiar_cuit`).
- `por_cuit` con CUIT no registrado → `None`.
- `activas()` filtra correctamente; `cantidad ≥ 200` (con tolerancia
  documentada).
- `por_tipo("sindical")` devuelve solo sindicales.
- `buscar("osde")` y `buscar("OSDE")` y `buscar("Osde")` devuelven lo
  mismo.
- `buscar("personal civil")` puede devolver más de un resultado
  (varias OS de personal civil).
- `es_obra_social` separa correctamente código vs CUIT vs
  inexistentes.
- Consistencia: cada `ObraSocial.cuit` pasa
  `personas.validar_cuit(cuit)`.
- Códigos RNOS no se repiten dentro del CSV.
- `tipos()` y `estados()` devuelven exactamente los valores del CSV.
- Reexports desde `salud` devuelven exactamente lo mismo que llamando
  directo.
- Sin internet, sin archivos externos.

## Riesgos

- **Datos snapshot.** El RNOS se actualiza (altas, bajas,
  suspensiones). Mitigación: doc con cadencia de actualización
  trimestral; `version_snapshot` documentado; tests no validan valores
  específicos que cambien sino estructura y consistencia interna
  (mismo enfoque que adoptó el builder en el reporte
  2026-05-13_paquete_completo).
- **Tamaño manejable.** ~280 filas: <100 KB. Sin riesgo.
- **Solapamiento con `salud`.** `salud` ya cubre normalización; `obras_sociales`
  agrega catálogo. Ambos viven en paralelo. Los reexports desde
  `salud` son por descubribilidad, no por reimplementación.
- **Privacidad.** Ninguno de los datos del RNOS es personal: son
  razones sociales, CUITs y códigos de entidades públicas registradas.
  Misma política que `bancos`/`universidades`/`empresas`.

## Prioridad

**Media.** Útil para análisis de datos sanitarios, padrones AFIP/SIPA
con código RNOS, y cualquier flujo que reciba "código de obra social"
como input. No es operación diaria como `dias_habiles` o `vencimientos`,
pero cierra el cuadrante de "datos del sistema de salud" que `salud`
abrió.

## Contexto adicional

- Originada en la auditoría: `salud` existe pero no tiene catálogo de
  entidades; `bancos` muestra que el paquete maneja bien padrones
  oficiales cerrados.
- Sigue el patrón consolidado por `bancos`/`universidades`/`empresas`:
  - padrón oficial cerrado embebido,
  - dataclass frozen,
  - lookup por código o por CUIT,
  - filtros por tipo/estado,
  - reuso de `personas.limpiar_cuit`/`validar_cuit`.
- Convención `import argentina as arg` respetada.
- Sugerencia al cerrar: agregar `obras_sociales` a `ROADMAP.md → Core`
  como parte del cluster de catálogos oficiales.
