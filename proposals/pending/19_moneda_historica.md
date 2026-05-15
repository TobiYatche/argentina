# Propuesta: moneda_historica

## Problema

Cualquier análisis económico argentino que vaya más allá de los
últimos 30 años choca contra la cadena de cambios de moneda:

1. **Peso moneda nacional** (m$n) — hasta 1969.
2. **Peso ley 18.188** ($) — 1970–1983: `1 $ ley = 100 m$n`.
3. **Peso argentino** ($a) — 1983–1985: `1 $a = 10.000 $ ley`.
4. **Austral** (₳) — 1985–1991: `1 ₳ = 1.000 $a`.
5. **Peso convertible / peso actual** ($) — 1992–hoy:
   `1 $ = 10.000 ₳`.

La conversión total: **1 peso actual = 10.000.000.000.000 (10
trillones) de pesos moneda nacional**.

Hoy, cualquier dataset histórico — sueldos de los 60s, presupuestos
provinciales del 80, contratos del austral — viene en la moneda de
su época. Convertirlos a una unidad común requiere:

- Saber la cadena exacta de equivalencias.
- Saber qué moneda regía cada año.
- Aplicar los factores oficiales (todos por ley, no negociables).

Es un problema **resuelto por ley argentina** — los multiplicadores
están en boletín oficial, son constantes y no envejecen. Pero
ningún paquete Python lo resuelve en una función.

Foros internacionales (Wikipedia "Argentine peso/austral/historical
exchange rates", FRED St. Louis, Worlddata) muestran que es un
dolor recurrente para analistas extranjeros que tocan datos
argentinos históricos.

## Benchmark / paquete de referencia

- [Wikipedia "Argentine peso"](https://en.wikipedia.org/wiki/Argentine_peso) y
  [Wikipedia "Argentine austral"](https://en.wikipedia.org/wiki/Argentine_austral) —
  documentan los factores oficiales.
- [`forex-python`](https://pypi.org/project/forex-python/) — convierte
  entre monedas vigentes, NO maneja monedas históricas
  reemplazadas.
- `argentina.monedas` (ya existe en el paquete) — cubre el catálogo
  de monedas vigentes. Esta propuesta lo **extiende con la
  dimensión histórica**.

## Traducción a Argentina

Un módulo `argentina.moneda_historica` con:
- Catálogo de las 5 monedas argentinas históricas con `vigencia_desde`,
  `vigencia_hasta`, `factor_a_siguiente`.
- Función para identificar qué moneda regía en una fecha dada.
- Función para convertir un monto + moneda + fecha → monto en pesos
  actuales (cadena de multiplicaciones).
- Función para convertir entre cualquier par (mn ↔ austral ↔ actual).

**No incluye inflación.** Eso es trabajo separado de un módulo
`indices` (propuesta 08, hoy en standby por requerir series oficiales
BCRA). Este módulo es **solo cambios de denominación legales** —
multiplicadores por ley, no inflación.

## API propuesta

```python
import argentina as arg
from datetime import date

# Qué moneda regía en una fecha
arg.moneda_historica.moneda_vigente(date(1980, 6, 1))
# 'peso_ley'

arg.moneda_historica.moneda_vigente(date(1988, 1, 1))
# 'austral'

arg.moneda_historica.moneda_vigente(date(2026, 5, 13))
# 'peso'

# Conversión a peso actual (solo cambios de denominación legales,
# NO ajuste por inflación)
arg.moneda_historica.a_peso_actual(1_000_000, moneda='peso_mn')
# 1e-7  (un millón de pesos moneda nacional ≈ 0,0000001 peso actual)

arg.moneda_historica.a_peso_actual(100_000, moneda='austral')
# 10  (100k australes = 10 pesos actuales)

# Conversión genérica entre cualquier par
arg.moneda_historica.convertir(
    100_000, desde='austral', hacia='peso_argentino'
)
# 100_000_000  (100k australes = 100M pesos argentinos)

# Inferir moneda desde fecha + convertir en un paso
arg.moneda_historica.a_peso_actual_por_fecha(
    1_000_000, fecha=date(1965, 1, 1)
)
# 1e-7  (en 1965 regía peso_mn, conversión automática)

# Listar monedas con metadata
arg.moneda_historica.listar()
# (MonedaHistorica(
#     codigo='peso_mn', nombre='Peso moneda nacional', simbolo='m$n',
#     vigencia_desde=date(1881, 1, 1), vigencia_hasta=date(1969, 12, 31),
#     factor_a_siguiente=Decimal('0.01'),  # 100 m$n = 1 $ley
#  ), ...)

# Formatear monto histórico con su símbolo
arg.moneda_historica.formato(1_500, moneda='austral')
# '₳ 1.500'  (usa formato.pesos por debajo + símbolo correspondiente)
```

Reglas:
- Internamente usar `decimal.Decimal` para preservar precisión en la
  cadena de multiplicaciones (los factores son potencias de 10
  enormes; floats pierden precisión).
- API expone `float` por simplicidad, con función explícita
  `convertir_decimal(...)` para quien necesite `Decimal`.
- `moneda` acepta `'peso_mn' | 'peso_ley' | 'peso_argentino' |
  'austral' | 'peso'` (o `'peso_actual'` como alias).
- Fechas fuera de rango (`< 1881` o `> hoy`): `ValueError` con
  mensaje claro.
- En la frontera exacta de un cambio (ej. 31/12/1969 vs 1/1/1970):
  documentar y testear la decisión.

## Archivos a modificar

- `src/argentina/moneda_historica.py` — módulo nuevo. Catálogo como
  tupla literal en código (cerrado, estable, no necesita CSV).
- `src/argentina/__init__.py` — agregar
  `from argentina import moneda_historica`.
- `src/argentina/monedas.py` — agregar reexport opcional
  `arg.monedas.historica` con import diferido, para descubribilidad.
- `tests/test_moneda_historica.py` — tests.
- `docs/modulos/moneda_historica.md` — documentación con tabla
  histórica completa de factores y fechas.
- `notebooks/moneda_historica_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura (`datetime`, `decimal`).

## Core o extra

**Core.** Cero dataset que envejezca. Los factores son leyes de
denominación (Ley 18.188/1969, Decreto 1.025/1983, Ley 23.928/1991),
constantes hasta que el Congreso vote otra reforma — evento histórico
puntual, no actualización periódica.

## Tests necesarios

- `moneda_vigente` para fechas-tipo en cada período (1960 → peso_mn,
  1975 → peso_ley, 1984 → peso_argentino, 1988 → austral, 2026 →
  peso).
- `moneda_vigente` en fronteras exactas: 31/12/1969, 1/1/1970, etc.
- `a_peso_actual(10**13, moneda='peso_mn')` ≈ `1.0`
  (10 trillones m/n = 1 peso actual).
- `a_peso_actual(10_000, moneda='austral')` = `1.0`.
- `convertir` bidireccional: `convertir(convertir(x, a→b), b→a) ≈ x`
  con tolerancia.
- Misma moneda en ambos lados de `convertir` → identidad.
- `convertir_decimal` mantiene precisión exacta (test con
  `Decimal('1.000000000000001')`).
- Fechas fuera de rango → `ValueError`.
- `listar()` devuelve exactamente 5 monedas.
- `formato(...)` usa el símbolo correcto por moneda.
- Sin internet, sin archivos externos.

## Riesgos

- **Confusión con inflación.** Usuarios pueden esperar que "convertir
  un sueldo de 1980 a pesos actuales" considere inflación. NO es eso.
  Mitigación: docstrings y doc del módulo arrancan explicando:
  "este módulo aplica los multiplicadores legales de denominación;
  para ajuste por inflación / poder adquisitivo, hace falta serie IPC
  histórica empalmada — fuera de scope". Sería la propuesta 08
  (indices) cuando haya fuentes oficiales reales.
- **Precisión float.** `1 / 10**13` está cerca del límite de
  precisión de double. Mitigación: usar `Decimal` internamente y
  ofrecer `convertir_decimal` para quien necesite precisión exacta.
- **Casos borde de fechas.** La transición entre monedas es por
  decreto con fecha exacta. Documentar y testear. Si el usuario pasa
  una fecha del día anterior a un cambio, la conversión es la
  vieja; del día del cambio, la nueva.
- **Nombres de monedas.** "Peso ley", "Peso argentino", "Peso
  convertible" pueden confundirse en docstring y arg-parse.
  Mitigación: catálogo cerrado de keys (`'peso_mn'`/`'peso_ley'`/
  `'peso_argentino'`/`'austral'`/`'peso'`) documentado en una sola
  tabla.

## Prioridad

**Alta.** Gap claro y dolor real documentado (Wikipedia, FRED,
foros). Implementación de baja superficie (5 monedas + cadena de
multiplicaciones). Cero deuda de mantenimiento — los multiplicadores
son ley, no cambian salvo evento histórico puntual.

## Contexto adicional

- Originada por la búsqueda en foros (2026-05-13) de problemas
  reales documentados para analistas extranjeros con datos
  argentinos históricos.
- Encaja con `monedas` (catálogo de vigentes) como su contraparte
  histórica.
- NO sustituye a `indices` (propuesta 08, en standby) — esa
  resolvería ajuste por inflación con series IPC; esta resuelve
  cambios de denominación legales.
- Convención `import argentina as arg` respetada.
- Patrón consolidado: lógica + dataclass + tabla cerrada
  hardcodeada, sin CSV externo. Mismo modelo que
  `razones_sociales` (13).
