# Propuesta: dias_habiles

## Problema

El paquete tiene `argentina.fechas` (parseo, edad, cohortes, año
lectivo) y `argentina.feriados` (consulta de feriados nacionales).
Falta la **operación combinada** que se necesita en cualquier flujo
con plazos legales/fiscales/bancarios argentinos:

- "¿Cuántos días hábiles hay entre 1-mar-2026 y 15-abr-2026?"
- "¿Cuál es la fecha que está 10 días hábiles después del 1-mar-2026?"
- "¿1-mar-2026 es día hábil?"
- "¿Cuál es el próximo día hábil después de un feriado?"

Hoy esto exige al usuario armar un loop manual que combine
`feriados.es_feriado()` + `weekday()` — todos los usuarios reescriben
el mismo código.

Además, en Argentina conviven al menos tres definiciones de "día
hábil":
- **Administrativo** (AFIP, Justicia): excluye sábados, domingos,
  feriados nacionales.
- **Bancario** (BCRA, días con bancos abiertos): incluye además
  asuetos bancarios específicos (24-dic, 31-dic en algunos años).
- **Comercial**: similar al administrativo, pero algunos casos
  excluyen sábados parciales (mañana hábil) según jurisdicción.

Sin un módulo que abstraiga estas reglas, cada script reinventa una
versión incompleta.

## Benchmark / paquete de referencia

- `workalendar` (Python) — calendario laboral multi-país, soporta
  Argentina parcialmente. Modelo de "calendario con feriados + días no
  hábiles" exactamente lo que se necesita.
- `pandas.tseries.offsets.BDay` — pero es global y no maneja feriados
  argentinos específicos. Además arrastra pandas, contrario a la
  filosofía core.
- `argentina.feriados` ya marca la mitad del trabajo (lista de
  feriados); este módulo construye la otra mitad (operaciones de
  conteo y desplazamiento).
- `numpy.busday_*` — funciona, pero arrastra numpy y exige construir
  manualmente la lista de feriados.

## Traducción a Argentina

Un módulo `argentina.dias_habiles` con tres modos (`"administrativo"`,
`"bancario"`, `"comercial"`) y operaciones sobre cada uno:

## API propuesta

```python
import argentina as arg
from datetime import date

# Es día hábil
arg.dias_habiles.es_habil(date(2026, 3, 23))                       # True
arg.dias_habiles.es_habil(date(2026, 3, 24))                       # False (Día Memoria)
arg.dias_habiles.es_habil(date(2026, 12, 24), modo="bancario")     # False (asueto)
arg.dias_habiles.es_habil(date(2026, 12, 24), modo="administrativo") # True

# Próximo día hábil (incluye la fecha dada si ya es hábil)
arg.dias_habiles.proximo(date(2026, 3, 24))
# date(2026, 3, 25)

arg.dias_habiles.proximo(date(2026, 3, 24), incluir_actual=False)
# date(2026, 3, 25)

# Día hábil anterior
arg.dias_habiles.anterior(date(2026, 3, 24))
# date(2026, 3, 23)

# Sumar/restar días hábiles
arg.dias_habiles.sumar(date(2026, 3, 1), 10)
# date(2026, 3, 13)  (10 días hábiles después)

arg.dias_habiles.sumar(date(2026, 3, 1), -5)
# date(2026, 2, 20)  (5 días hábiles antes)

# Contar días hábiles entre dos fechas (excluyente del extremo
# superior, mismo criterio que numpy.busday_count)
arg.dias_habiles.contar(desde=date(2026, 3, 1), hasta=date(2026, 4, 1))
# 21

# Listar días hábiles en un rango
arg.dias_habiles.listar(desde=date(2026, 3, 1), hasta=date(2026, 3, 31))
# (date(2026, 3, 2), date(2026, 3, 3), ...)

# Modos disponibles
arg.dias_habiles.modos()
# ('administrativo', 'bancario', 'comercial')
```

Reglas:
- `modo="administrativo"` es el default.
- Todas las funciones aceptan `datetime.date`, `datetime.datetime` o
  string ISO; usan `fechas.parsear_fecha` para normalizar.
- `incluir_actual` en `proximo`/`anterior` default `True`.
- `contar(desde, hasta)`: cuenta hábiles en `[desde, hasta)` —
  documentar explícitamente (es la convención de numpy/pandas, evita
  el error off-by-one típico).
- Los asuetos bancarios extra (24-dic, 31-dic, etc.) se embeben por
  año en un CSV chico. Año fuera de rango → fallback al cálculo solo
  con feriados nacionales + warning explícito documentado.

## Archivos a modificar

- `src/argentina/dias_habiles.py` — módulo nuevo.
- `src/argentina/data/asuetos_bancarios.csv` — asuetos bancarios extra
  por año (≈ 5-10 filas por año, BCRA).
- `src/argentina/__init__.py` — agregar
  `from argentina import dias_habiles`.
- `tests/test_dias_habiles.py` — tests.
- `docs/modulos/dias_habiles.md` — documentación con tabla "modo →
  qué excluye".
- `notebooks/dias_habiles_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

- Stdlib pura para las operaciones (`datetime`, `calendar`).
- `argentina.feriados` para la lista de feriados nacionales. `feriados`
  tiene `requests` como opcional, pero la consulta puede ser puramente
  offline si se usa la lista embebida (consultar cómo está implementado
  hoy `feriados`). Si `feriados` exige internet para `es_feriado`:
  ofrecer un fallback con lista embebida propia o exigir el extra.
- NO depender de pandas / numpy / workalendar.

## Core o extra

**Core.** Las operaciones son stdlib pura; el único dato externo son
los asuetos bancarios embebidos.

## Tests necesarios

- `es_habil` con días claramente hábiles → `True`; con sábado/domingo
  → `False`; con feriado nacional → `False`.
- `es_habil(modo="bancario")` con asueto bancario embebido → `False`.
- `es_habil(modo="administrativo")` con asueto bancario → `True` (no
  aplica administrativamente).
- `proximo` desde un viernes feriado → lunes siguiente (o martes si
  el lunes también es feriado).
- `anterior` simétrico.
- `proximo(fecha_habil, incluir_actual=True)` → la misma fecha.
- `sumar(fecha, 0)` → la misma fecha (si ya es hábil) o próximo hábil
  (documentar criterio explícito).
- `sumar(fecha, n)` y `sumar(resultado, -n)` son reversibles cuando
  empiezan en hábil.
- `contar` excluye el extremo superior (`contar(d, d)` = `0`).
- `contar(date(2026, 3, 1), date(2026, 4, 1))` consistente con
  `len(listar(...))` ajustado por el criterio de extremo.
- Modo inválido → `ValueError`.
- Reuso de `fechas.parsear_fecha`: aceptar string ISO devuelve mismo
  resultado que `date` directo.
- Sin internet, sin archivos externos.

## Riesgos

- **Asuetos bancarios desactualizados.** El BCRA publica asuetos
  bancarios cada año (a veces sobre la marcha por situaciones
  puntuales). Mitigación: snapshot inicial con asuetos conocidos +
  doc de cadencia. Año futuro sin asuetos cargados → operar solo con
  feriados nacionales + warning documentado, NO error.
- **Acoplamiento con `feriados`.** Si `feriados.es_feriado` requiere
  internet en su forma actual, este módulo lo hereda. Mitigación:
  resolverlo en la implementación — preferir una lista offline de
  feriados (calculada algorítmicamente para móviles + tabla embebida
  para no recurrentes) y dejar la API de `feriados` con internet como
  enriquecimiento opcional. Decisión específica del builder.
- **Múltiples definiciones.** El parámetro `modo` puede crecer
  (judicial, escolar, etc.). Mitigación: empezar con los 3 modos
  comprometidos y cerrar la API a esos 3. Modos nuevos = decisión
  explícita futura.
- **Confusión sobre el extremo del rango.** `contar(d, d)` = 0 puede
  sorprender. Mitigación: doc explícita arriba del módulo y en cada
  función relevante.

## Prioridad

**Alta.** Operación frecuentísima en flujos con plazos argentinos
(vencimientos, pagos, notificaciones, recursos administrativos). Hoy
no cubierta. Encaja perfecto con `vencimientos` (propuesta 10) — los
dos tienen sinergia: `vencimientos.vencimiento(..., ajustar_feriado=True)`
puede usar internamente `dias_habiles.proximo`.

## Contexto adicional

- Originada en la auditoría: `fechas` y `feriados` existen por
  separado y nunca se combinaron en operaciones útiles.
- Sigue el patrón establecido: stdlib first, datos chicos embebidos,
  imports rápidos.
- Convención `import argentina as arg` respetada.
- Sinergia explícita con la propuesta 10 (`vencimientos`):
  conviene implementar `dias_habiles` antes y usarlo desde
  `vencimientos.ajustar_feriado`.
- Sugerencia al cerrar: agregar `dias_habiles` a `ROADMAP.md → Core`.
