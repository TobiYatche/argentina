# Changelog

Todas las versiones notables de `argentina` se registran en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y el proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [0.3.0] — 2026-05-12

Sprint inspirado en paquetes referencia del ecosistema (`us`, `pycountry`,
`phonenumbers`, `pycpfcnpj`).

### Features nuevas

- **`<modulo>.mapping(de, a)`** — devuelve diccionario
  `{item.<de>: item.<a>}`. Disponible en `provincias`, `departamentos`,
  `ciudades`, `universidades`, `aeropuertos`, `aglomerados`,
  `paises_limitrofes`, `presidentes`, `monedas`. Inspirado en
  `us.states.mapping(...)`.
- **`argentina.telefonos.extraer_de_texto(texto, normalizar=False)`** —
  extrae teléfonos argentinos válidos de texto libre. Inspirado en
  `phonenumbers.PhoneNumberMatcher` pero específico para Argentina.
- **`argentina.personas.generar_dni()`**, **`generar_cuit(tipo=...)`** —
  generan identificadores válidos (con dígito verificador correcto) para
  fixtures de tests. Aceptan `rng=random.Random(seed)` para reproducibilidad.
  Inspirado en `pycpfcnpj.gen.*`.
- **`argentina.bancos.generar_cbu(codigo_banco=None)`** — genera CBU con
  ambos dígitos verificadores válidos.
- **Fuzzy lookup**: `arg.provincias.lookup(valor, fuzzy=True)` y
  `arg.ciudades.lookup(valor, fuzzy=True)` toleran typos
  (`"misisones"` → Misiones, `"buens aires"` → Buenos Aires). Usa
  `difflib` de stdlib. Default `fuzzy=False` (sin cambios de comportamiento
  para los existentes).

### Sin breaking changes

Todas las APIs anteriores siguen funcionando igual. `lookup(valor)` no cambia
de comportamiento por default; solo cuando se pasa `fuzzy=True` activa la
búsqueda aproximada.

## [0.2.0] — 2026-05-12

### Módulos nuevos

- **`argentina.patentes`** — limpia, valida y formatea patentes argentinas
  en sus 4 formatos: vieja (`AAA 999`), Mercosur (`AA 999 BB`), moto vieja
  (`999 AAA`), moto Mercosur (`A 999 BBB`). Solo regex, sin dependencias.
- **`argentina.aglomerados`** — los aglomerados urbanos de la EPH (INDEC)
  decodificados: dado el código `AGLOMERADO` de un microdato, devuelve
  nombre y provincia. `lookup`, `listar`, `por_provincia`, módulo iterable.
- **`argentina.universidades`** — set curado de 53 universidades nacionales
  argentinas con sigla, nombre, provincia, sede y año de fundación. Funciones
  `lookup`, `por_provincia`, `por_anio`.
- **`argentina.aeropuertos`** — 39 aeropuertos comerciales del país con
  IATA, ICAO, nombre, ciudad, provincia, lat/lon y tipo
  (internacional/cabotaje). Funciones `lookup`, `por_provincia`,
  `internacionales`, `cabotaje`. Combinable con `arg.geo.distancia` para
  distancias aéreas.

### Features nuevas

- **`argentina.identificar(valor)`** — inspector universal: recibe cualquier
  string y devuelve un dict con `tipo` (cuit/cbu/cpa/cp4/telefono/patente/
  dni/departamento/ciudad/provincia) más toda la metadata derivada. Compone
  los módulos existentes sin red.
- **`argentina.geo.distancia(a, b)`** — distancia haversine en km entre dos
  puntos. Acepta tuplas `(lat, lon)`, strings (nombre de ciudad o provincia),
  objetos `Ciudad` o `Provincia`. Sin dependencias (solo `math` de stdlib).
- **`Provincia.superficie_km2`** + **`Provincia.densidad_2022`** —
  superficie continental (sin reclamos antárticos) y densidad poblacional
  derivada del Censo 2022.
- **`argentina.bancos.BANCOS_BCRA`** — tabla expandida a ~55 bancos
  argentinos con su código BCRA. Nuevas funciones `banco_de_cbu(cbu)` (alias
  de `banco_por_cbu`) y `banco_por_codigo(codigo)`.

### Más módulos y atajos

- **`argentina.pais`** — constantes nacionales invariantes: `CODIGO_ISO`,
  `CODIGO_ISO_3`, `TELEFONO_PREFIJO`, `TLD`, `CAPITAL`, `MONEDA`, `BBOX`,
  `SUPERFICIE_CONTINENTAL_KM2`, `POBLACION_2022`, etc.
- **`argentina.paises_limitrofes`** — 5 países limítrofes (Brasil, Bolivia,
  Chile, Paraguay, Uruguay) con código ISO, longitud de frontera (km) y las
  provincias argentinas que limitan con cada uno. `lookup`, `por_provincia`.
- **`argentina.presidentes`** — 57 presidentes argentinos desde 1853 con
  período, partido y tipo (constitucional / interino / de facto). Funciones
  `en(fecha)`, `actual()`, `lookup`, `por_partido`, `por_tipo`.
- **`argentina.monedas`** — 5 monedas oficiales de Argentina (m$n, $Ley, $a,
  Austral, Peso) con su período de vigencia y factor de conversión nominal.
  Función `convertir(monto, desde, hasta)` para hacer cambios históricos.
- **`Provincia.universidades`** / **`.aeropuertos`** / **`.ciudades`** /
  **`.departamentos`** — properties cross-module: atajan
  ``arg.universidades.por_provincia(p)`` a ``p.universidades``, etc.

### Cross-module helpers y conveniencias (fast wins)

- **`Provincia.cpa_letra`** — letra inicial del CPA correspondiente
  (X para Córdoba, C para CABA, B para Buenos Aires, etc.).
- **`Provincia.codigo_telefono`** — característica telefónica de la capital.
- **`Provincia.aglomerados`** — aglomerados EPH de la provincia (tuple de
  `Aglomerado`).
- **`Ciudad.es_capital_provincial`** — bool: ``True`` si la ciudad es la
  capital de su provincia. Maneja correctamente el caso CABA vía alias.
- **`arg.coordenadas(valor)`** — acceso unificado: devuelve
  ``(lat, lon)`` de cualquier ciudad, provincia (vía capital), aeropuerto,
  tupla ya armada u objeto del paquete.
- **`arg.provincias.por_region("Patagonia")`** y
  **`arg.provincias.regiones()`** — filtrar/enumerar regiones.
- **`<Dataclass>.como_dict()`** en `Provincia`, `Ciudad`, `Departamento`,
  `Aglomerado`, `Universidad`, `Aeropuerto`.
- **`<modulo>.como_tabla()`** — lista de dicts apta para
  `pandas.DataFrame(...)` sin importar pandas.

### Sin breaking changes

Todas las APIs anteriores siguen funcionando igual.

## [0.1.1] — 2026-05-12

### Cambios menores

- Reescritos los docstrings de `provincias`, `departamentos` y `ciudades`
  para describir el patrón propio (constantes públicas + `lookup` flexible
  + dataclass frozen) en lugar de comparar con otros paquetes.
- Misma corrección en `README.md` y en la documentación
  (`docs/filosofia.md`, `docs/modulos/provincias.md`).
- Sin cambios de API ni de comportamiento.

## [0.1.0] — 2026-05-12

Primera versión publicada en PyPI. **Yanked**: ver 0.1.1 para reemplazo.

### Módulos del paquete base (sin dependencias externas)

- `argentina.provincias` — 24 provincias con metadata oficial (código INDEC,
  ISO 3166-2, región, capital + lat/lon, población Censo 2022). Constantes
  públicas, `lookup` flexible, aliases (`PBA`, `CABA`, `TDF`, `bs as`), módulo
  iterable.
- `argentina.departamentos` — 529 departamentos/partidos/comunas oficiales
  (códigos INDEC reales vía IGN), `lookup` por código o nombre único,
  `por_provincia(...)`, aliases coloquiales (`La Matanza`, `Mar del Plata`...).
- `argentina.ciudades` — 33 ciudades principales con población (Censo 2022),
  lat/lon, `top(n)`, `por_provincia(...)`, aliases (`mardel`, `tucuman`...).
- `argentina.postal` — validación CP4 y CPA, extracción, provincia por letra
  CPA, validación cruzada con `arg.provincias`.
- `argentina.telefonos` — limpiar/validar/normalizar a E.164, distinguir
  celular vs fijo, característica, mapeo característica → provincia.
- `argentina.personas` — DNI/CUIT/CUIL con dígito verificador oficial,
  normalización de nombres.
- `argentina.direcciones` — parsing local de direcciones (sin red).
- `argentina.bancos` — CBU, alias bancarios.
- `argentina.clean` — normalización de texto (sin tildes, snake_case, etc.).
- `argentina.educacion`, `argentina.salud`, `argentina.fechas` — utilidades
  específicas por dominio.

### Subpaquetes

- `argentina.geo`:
  - `geo.shapes` — geometrías oficiales (provincias y departamentos) desde el
    WFS del IGN, cache local en `~/.cache/argentina/shapes/`.
  - `geo.basemaps` — fondos cartográficos argentinos (Argenmap del IGN) para
    Folium, con créditos y toponimia argentina para Islas Malvinas.
  - `geo.direcciones` — georreferenciación contra la API Georef (datos.gob.ar).
  - `geo.postal` — placeholders para georreferenciación postal.
  - `geo.mapa.mapa_de(...)` — helper de un solo paso para armar un mapa con
    Argenmap + polígono + capital de cualquier provincia.

- `argentina.elecciones` — utilidades para datos electorales argentinos.

- `argentina.data` (extra `[data]`):
  - `data.eph` — descarga de microdatos EPH trimestrales del INDEC, cache
    local, lectura como `pandas.DataFrame`.
  - `data.censo` — arquitectura DuckDB + Parquet remoto para Censo 2022
    (URLs configurables).

- `argentina.feriados` (extra `[feriados]`) — listado y consulta de feriados
  oficiales argentinos.

- `argentina.economia` (extra `[economia]`) — 493 series económicas oficiales
  (INDEC, BCRA, SSPM) vía datos.gob.ar.

- `argentina.shapes` — wrapper de compatibilidad de `argentina.geo.shapes`.

### Extras opcionales

- `[economia]` → `pandas`, `requests`
- `[geo]` → `geopandas`, `requests`, `pyogrio`
- `[maps]` → `folium`
- `[georef]` → `requests`
- `[feriados]` → `requests`
- `[elecciones]` → `pandas`, `requests`
- `[data]` → `pandas`, `requests`, `pyarrow`, `duckdb`
- `[dev]` → `pytest` + deps para correr la suite completa

### Características

- **Paquete base sin dependencias.** `import argentina` carga en ~68 ms con
  ~3.7 MB de memoria, sin `pandas`/`requests`/`duckdb`/`pyarrow`.
- **Imports diferidos** en todos los módulos que requieren deps externas.
- **216 tests** cubriendo todos los módulos.
- **Notebooks de uso real** (`notebooks/*_pruebas.ipynb`) para cada módulo.
- **Datos del Censo Nacional 2022 (INDEC)** integrados como población
  provincial y de ciudades principales.

[0.1.0]: https://github.com/tobiasyatche/argentina/releases/tag/v0.1.0
