# Docs update — 2026-05-13 (v2)

Segunda pasada del agente `docs_agent` del mismo día. Entre v1 y v2 se
agregaron 8 módulos al paquete (`formato`, `clae`, `afip`, `indices`,
`empresas`, `municipios`, `localidades`, `nombres`) — todos con su propia
página en `docs/modulos/`, su notebook `<modulo>_pruebas.ipynb` y entradas
ya añadidas en `mkdocs.yml`, `docs/api.md` y `README.md`.

Versión del paquete al momento del reporte: **0.3.0**.

## Estado encontrado

- **Módulos nuevos en `src/argentina/`** (vs v1): `formato.py`, `clae.py`,
  `afip.py`, `indices.py`, `empresas.py`, `municipios.py`, `localidades.py`,
  `nombres.py`. Todos ya importados en `argentina/__init__.py` y exportados
  en `__all__`.
- **Páginas correspondientes en `docs/modulos/`**: ya existían (59-139
  líneas cada una), con buen tono, tablas de API, casos borde y filosofía.
  Sample-check sobre `formato.md`, `indices.md`, `afip.md`, `clae.md` y
  `empresas.md`: están al día con la API real. No requirieron reescritura.
- **Notebooks `<modulo>_pruebas.ipynb`**: ya existían para los 8 nuevos.
- **`mkdocs.yml` y `docs/api.md`**: ya listaban los 8 nuevos.
- **`README.md`**: ya mencionaba los 8 en la tabla de módulos principales.

Es decir: el grueso del trabajo de docs por módulo ya estaba hecho. La v2
se concentró en **integrar los módulos nuevos en el material transversal**.

## Cambios realizados en esta pasada

### `docs/quickstart.md`

Agregadas tres secciones nuevas, ubicadas antes del bloque "Para seguir":

- **Formato canónico para mostrar** — `arg.formato.{dni,cuit,pesos,telefono,fecha}`
  como punto único de entrada para presentación.
- **Ajustar montos por IPC (offline)** — ejemplo de `arg.indices.ajustar_ipc`
  y mención al complemento con `arg.economia` online.
- **Monotributo, IVA y Ganancias (tablas AFIP)** — uso típico de
  `arg.afip.monotributo_categoria_por_facturacion`, `alicuotas_iva`,
  `ganancias_minimo_no_imponible`. Aclaración explícita de que **no es
  un motor fiscal**.

### Notebooks temáticos regenerados

- `notebooks/00_quickstart.ipynb` — agregadas celdas de `formato` (sección 7),
  `indices.ajustar_ipc` (sección 9), `afip` (sección 10) y `clae`/`empresas`
  (sección 11). Pasó de 29 a 45 celdas.
- `notebooks/04_bancos_afip.ipynb` — incorporadas categorías de Monotributo,
  alícuotas de IVA y mínimos de Ganancias usando `arg.afip.*`. Sumado un
  bloque corto sobre `arg.empresas` (cotizantes, estatales) y `arg.clae`
  (lookup, búsqueda). Pasó de 23 a 41 celdas.
- `notebooks/05_fechas_feriados.ipynb` — agregada sección "Índices económicos
  offline" con `arg.indices.{disponibles, cobertura, ipc, uva, ajustar_ipc,
  factor_ipc, ajustar}`. Sumado `arg.formato.fecha` con sus tres estilos.
  Pasó de 23 a 41 celdas.

Los notebooks `01_limpieza_personas.ipynb`, `02_geo_basico.ipynb` y
`03_direcciones_postal_telefonos.ipynb` quedaron como estaban — los módulos
nuevos no afectan su scope.

### Lo que NO se tocó

- **`README.md`** — ya tiene la tabla con los 8 módulos nuevos. Mantengo.
- **`mkdocs.yml`** — ya tiene los 8 en `nav`. Mantengo.
- **`docs/api.md`** — ya tiene los 8 bloques mkdocstrings. Mantengo.
- **Páginas `docs/modulos/<nuevo>.md`** — están bien escritas, mantengo.
- **`<modulo>_pruebas.ipynb`** — son responsabilidad del builder (convención
  del proyecto: cada módulo nuevo trae su propio notebook de pruebas).
- **Lógica del paquete, APIs, `pyproject.toml`, `__init__.py`, CSVs** —
  fuera del scope del docs agent.

## Hallazgos / pendientes

1. **ROADMAP.md** está desactualizado: la sección "Próximas ideas" lista
   `municipios`, `localidades`, `nombres`, `matching`, `formato`, `clae`,
   `empresas` — todos ya construidos. Sugerencia: moverlos arriba (a
   "Core" u "Opcionales" según corresponda) o agregar una sección
   "Próximamente" con ideas realmente futuras. **No lo edité** porque el
   ROADMAP es decisión del builder/usuario, no del docs agent.
2. **`docs/index.md`** todavía cita las fuentes de datos sin mencionar
   IPC/UVA/CER/ICL embebidos en `arg.indices` ni las tablas AFIP en
   `arg.afip`. Considerar agregarlos cuando se actualicen los CSVs con
   datos oficiales (hoy `indices.md` y `afip.md` los marcan como snapshot
   ilustrativo / no exhaustivo).
3. **`CHANGELOG.md`** no se tocó. Idealmente la próxima release (0.4.0)
   tendría un bloque enumerando estos 8 módulos nuevos. Eso lo maneja el
   release agent / builder.
4. **`docs/extras.md`** quedó coherente: los módulos nuevos viven todos
   en el core (stdlib pura, sin extras). Si en el futuro alguno requiere
   `pandas`/`requests`, agregarlo a la tabla de extras.

## Convenciones aplicadas

- Tono según `scripts/docs_agent.md`: canchero, simple, profesional.
- Alias `import argentina as arg` en todos los ejemplos.
- Carga diferida y caches se explicitan donde corresponde.
- Cada módulo aclara: core vs extra, snapshot vs descarga, sintáctico vs
  motor real.

## Próxima pasada

Cuando entre alguno de los módulos pendientes del ROADMAP que aún no
están construidos (sección "Próximas ideas" depurada), el ciclo
estándar es:

1. Crear `docs/modulos/<nuevo>.md`.
2. Agregar bloque mkdocstrings en `docs/api.md`.
3. Agregar entrada en `mkdocs.yml` → `nav` → `Módulos`.
4. Agregar fila en la tabla del README.
5. Revisar si algún notebook temático (00..05) lo cubre y extenderlo.
6. Si el módulo aporta features quickstart-grade, mencionarlo en
   `docs/quickstart.md`.
