# Propuesta: horarios

## Problema

En datasets de comercios, oficinas, atención al público, scraping de
guías comerciales y datos abiertos de municipios aparecen horarios
en formato texto, escritos por humanos:

- `"Lun a Vie de 9 a 18hs"`
- `"L-V 9-18"`
- `"lunes a viernes 9 a 13 y 16 a 20"`
- `"Mar, Mie, Vie 10-14"`
- `"24 hs"`
- `"horario corrido 8-20"`
- `"sábados 9:30 a 13:30"`
- `"cerrado"`, `"sin horario fijo"`

Hoy quien quiere normalizar esto y consultar "¿está abierto el martes
a las 15:00?" tiene que escribir el parser cada vez. Ningún módulo
del paquete cubre horarios.

## Benchmark / paquete de referencia

- [`opening_hours_py`](https://pypi.org/project/opening-hours/) (Rust
  port) y [`osm-opening-hours`](https://wiki.openstreetmap.org/wiki/Key:opening_hours) —
  OSM tiene un formato estándar para horarios de apertura. Modelo
  conceptual; el formato OSM es la salida canónica recomendada.
- [`DataPrep.clean`](https://docs.dataprep.ai/) — cleaning de texto
  estructurado.
- `argentina.fechas` (numérico) y la propuesta 16 `fechas_texto`
  (texto natural) cubren el lado fechas; este módulo cubre el lado
  **horarios**.

## Traducción a Argentina

Un módulo `argentina.horarios` que parsea horarios escritos en español
rioplatense y devuelve una estructura consultable. Sin dataset
externo — todo regex + tabla cerrada de días/meses (que ya está en
`fechas_texto` propuesta 16, reusar).

## API propuesta

```python
import argentina as arg

# Parsear horario
h = arg.horarios.parsear("Lun a Vie de 9 a 18hs")
# Horario(franjas=[
#     Franja(dia='lun', desde=time(9, 0), hasta=time(18, 0)),
#     Franja(dia='mar', desde=time(9, 0), hasta=time(18, 0)),
#     ...
#     Franja(dia='vie', desde=time(9, 0), hasta=time(18, 0)),
# ])

# Doble turno
arg.horarios.parsear("L a V 9 a 13 y 16 a 20")
# Horario con dos franjas por día.

# Días individuales
arg.horarios.parsear("Mar, Mie, Vie 10-14")
# Tres franjas, una por cada día listado.

# 24 horas
arg.horarios.parsear("24hs")
# Horario marcado como `siempre_abierto=True`.

# Cerrado / sin horario
arg.horarios.parsear("cerrado")
# Horario marcado como `siempre_cerrado=True`.

arg.horarios.parsear("sin horario fijo")
# None  (no estructurable)

# Consultar si está abierto en un momento
arg.horarios.esta_abierto(h, dia='martes', hora=time(15, 0))
# True

arg.horarios.esta_abierto(h, dia='sabado', hora=time(15, 0))
# False

# Formato canónico de salida (estilo OSM, simplificado)
arg.horarios.formato_osm(h)
# 'Mo-Fr 09:00-18:00'

# Texto humano normalizado
arg.horarios.formato_humano(h)
# 'Lunes a viernes de 9 a 18 hs'

# Días de la semana cubiertos
arg.horarios.dias_cubiertos(h)
# ('lun', 'mar', 'mie', 'jue', 'vie')
```

Reglas:
- `Horario` es dataclass frozen con `franjas: tuple[Franja, ...]`,
  `siempre_abierto: bool`, `siempre_cerrado: bool`.
- `Franja` es dataclass frozen con `dia: str` (clave canónica `lun`
  / `mar` / ...), `desde: time`, `hasta: time`.
- `parsear(None)` y `parsear("")` → `None`.
- Casos no parseables (texto libre tipo "sin horario fijo", "consultar
  por teléfono") → `None`, NO levantar.
- `esta_abierto` acepta `dia` como string (`'lunes'`, `'lun'`, `'L'`)
  o `date` (toma el día de la semana).
- Reusa el catálogo `DIAS_SEMANA` del módulo `fechas_texto` (propuesta
  16) si está disponible; si no, lo replica internamente.
- `formato_osm` devuelve string compatible con OSM
  `opening_hours`, simplificado (no soporta todas las features de OSM
  — solo lo que el parser produce).

## Archivos a modificar

- `src/argentina/horarios.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar `from argentina import horarios`.
- `tests/test_horarios.py` — tests.
- `docs/modulos/horarios.md` — documentación con tabla de formatos
  reconocidos.
- `notebooks/horarios_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura (`re`, `datetime.time`).

## Core o extra

**Core.** Cero dataset. Tabla cerrada de días en español.

## Tests necesarios

- `"Lun a Vie de 9 a 18hs"`, `"L-V 9-18"`, `"lunes a viernes 9 a 18"` →
  todos producen el mismo `Horario` (5 días, una franja).
- Doble turno: `"L a V 9 a 13 y 16 a 20"` → 5 días, dos franjas cada
  uno.
- Días individuales: `"Mar, Mie, Vie 10-14"` → 3 días, una franja.
- Horario con minutos: `"sábados 9:30 a 13:30"`.
- `"24hs"`, `"24 hs"`, `"24/7"` → `siempre_abierto=True`.
- `"cerrado"` → `siempre_cerrado=True`.
- Casos no parseables (`"sin horario fijo"`, `"consultar"`) → `None`.
- `esta_abierto` para variantes de input de `dia` (string corto/largo,
  `date`).
- `esta_abierto` en franja vs fuera de franja vs entre franjas
  (doble turno).
- `formato_osm` produce string OSM válido para casos canónicos.
- `formato_humano` ida y vuelta: `parsear(formato_humano(h))` debe
  recuperar `h` para los casos que el parser cubre.
- `dias_cubiertos` correcto.
- Sin internet, sin archivos externos.

## Riesgos

- **Variedad infinita de cómo se escriben horarios.** El módulo NO
  va a cubrir el 100% de los casos texto libre. Mitigación: catálogo
  cerrado de patrones documentados; lo que no matchea devuelve
  `None` honestamente, no inventa.
- **Ambigüedad de "16-20".** ¿Es 16hs a 20hs o 1620?
  Mitigación: regex requiere separador claro (`-`, `a`, `:`); cuando
  hay ambigüedad pura, asume formato hora si los números son razonables
  (`<= 24`).
- **AM/PM.** En Argentina se usa formato 24h prácticamente siempre.
  Mitigación: el parser **no soporta AM/PM** por default; documentarlo.
  Si aparece la necesidad real, agregar como opcional.
- **Husos / DST.** El módulo opera con `time` (no `datetime`); no
  considera zona horaria ni DST. Argentina no usa DST hoy, pero por
  las dudas dejarlo documentado.
- **Solapamiento con fechas_texto (16).** Compartirán el catálogo
  `DIAS_SEMANA`. Mitigación: si 16 se implementa antes, este módulo
  importa de allí; si no, este lo replica y luego se refactoriza.
  Es la única dependencia interna planificada y es deliberada.

## Prioridad

**Media.** Útil pero más nicho que `fechas_texto` (16) o `emails`
(17). Bien definido y aislado: implementación posible apenas estén
listos los módulos más prioritarios. Cero deuda de mantenimiento.

## Contexto adicional

- Originada por feedback del usuario (2026-05-13): "limpieza de
  datos más general".
- Inspiración: formato OSM `opening_hours` (estándar internacional
  para horarios) como salida canónica.
- Patrón consolidado: módulo transversal sin dataset, encaja con
  `clean`/`formato`/`matching`/`fechas_texto` (16).
- Convención `import argentina as arg` respetada.
- Implementar después de `fechas_texto` (16) para compartir
  catálogo de días.
