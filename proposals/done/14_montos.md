# Propuesta: montos

## Problema

En Argentina aparecen montos escritos de mil maneras y nadie tiene
forma rápida de convertirlos a un número limpio:

- `"$ 1.500.000,50"` (formato argentino estándar)
- `"$1.500.000"`
- `"1500000.50"` (formato exportado por sistemas en inglés)
- `"ARS 1.500.000"`
- `"AR$ 1.500.000"`
- `"1,5M"`, `"1.5 millones"`, `"$1,5 millones"`
- `"1.500.000 pesos"`
- `"u$s 1.500"` (en dólares, marcado)
- `"-1.500,50"` (negativo)

`argentina.formato.pesos` ya cubre el camino inverso (número → string).
Falta el camino crítico para data cleaning: **string → número**, con
detección de variantes y moneda.

`argentina.clean` cubre normalización de texto pero no parsing
numérico.

## Benchmark / paquete de referencia

- [`DataPrep.clean_currency`](https://docs.dataprep.ai/) — limpia
  columnas de moneda con detección de formato.
- [`python-stdnum`](https://pypi.org/project/python-stdnum/) — modelo
  `parse() / validate() / compact() / format()` por código.
- [`Babel`](https://babel.pocoo.org/) — parser localizado de números
  por país. Inspiración conceptual, pero arrastra una dependencia
  pesada y es overkill para Argentina específica.
- `argentina.formato.pesos` ya existe en el paquete: este módulo es
  su **inverso** y su **complemento de detección**.

## Traducción a Argentina

Un módulo `argentina.montos` 100% lógica (regex + reglas) que:

- Parsea strings con variantes argentinas y devuelve un float / Decimal.
- Detecta la moneda (`ARS`, `USD`) cuando viene marcada.
- Maneja sufijos cortos (`M` = millón, `K` = mil) con criterio
  documentado.
- Acepta números tal cual (`1500000`) o ya-parseados (`1500000.5`).

## API propuesta

```python
import argentina as arg

# Parseo directo: string → float
arg.montos.parsear("$ 1.500.000,50")
# 1500000.5

arg.montos.parsear("1.500.000")
# 1500000.0

arg.montos.parsear("1500000.50")  # formato "inglés", también acepta
# 1500000.5

arg.montos.parsear("1,5M")
# 1500000.0

arg.montos.parsear("1.5 millones")
# 1500000.0

arg.montos.parsear("-1.500,50")
# -1500.5

arg.montos.parsear("no es un monto")
# None  (no levanta; consistencia con limpiar_*)

# Parseo extendido con detección de moneda
arg.montos.parsear_completo("u$s 1.500,50")
# Monto(valor=1500.5, moneda='USD', formato_detectado='argentino')

arg.montos.parsear_completo("ARS 1500.50")
# Monto(valor=1500.5, moneda='ARS', formato_detectado='ingles')

# Detección de formato (sin convertir)
arg.montos.formato_detectado("1.500.000,50")  # 'argentino'
arg.montos.formato_detectado("1,500,000.50")  # 'ingles'
arg.montos.formato_detectado("1500000")       # 'ambiguo'

# Detección de moneda en el string
arg.montos.moneda_detectada("u$s 1.500")  # 'USD'
arg.montos.moneda_detectada("$ 1.500")    # None  (ambiguo o ARS por
                                          # contexto — documentar)
```

Reglas:
- `parsear(None)` → `None`; `parsear("")` → `None`. Consistencia con
  los `limpiar_*` del paquete.
- `parsear` devuelve `float`. Para precisión decimal: `parsear_decimal`
  devuelve `Decimal`.
- Estrategia de detección formato:
  - Si tiene `,` Y `.`: el separador decimal es el último de los dos.
  - Si tiene solo `,`: decimal argentino (`"1.500,5"` no se ve nunca
    sin punto miles, así que `,` lone = decimal).
  - Si tiene solo `.` y 1-2 cifras tras él: probablemente decimal
    inglés (`"1500.50"`).
  - Si tiene solo `.` y 3 cifras tras él: probablemente miles
    argentino (`"1.500"`).
  - Si es ambiguo (`"1.500"`): documentar la heurística usada y dar
    `parsear(..., asumir='argentino' | 'ingles')` para forzar.
- Sufijos `K`/`M`/`MM`/`B`: definir tabla cerrada en doc.
- "millones"/"mil" en texto: detectar regex `\d+([,.]\d+)?\s*(M|mill|millones)`.
- NO inferir moneda por contexto. Solo cuando viene explícita
  (`u$s`, `USD`, `dólares`).

## Archivos a modificar

- `src/argentina/montos.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar `from argentina import montos`.
- `src/argentina/formato.py` — agregar reexport opcional:
  `arg.formato.parsear_pesos = montos.parsear` (con import diferido)
  para descubribilidad bidireccional (formato.pesos ↔ formato.parsear_pesos).
- `tests/test_montos.py` — tests.
- `docs/modulos/montos.md` — documentación, **con tabla de reglas de
  detección de formato explícita** porque el espacio es ambiguo.
- `notebooks/montos_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura (`re`, `decimal`).

## Core o extra

**Core.** Cero dataset. Lógica pura sobre strings.

## Tests necesarios

- `parsear` con todas las variantes listadas en "Problema" devuelve
  el número correcto.
- `parsear(None)`, `parsear("")`, `parsear("no es un monto")` → `None`.
- `parsear` negativo, decimal cero, monto cero, monto con muchos
  decimales (precisión documentada).
- `parsear_decimal` devuelve `Decimal` con precisión configurable.
- `parsear_completo` detecta moneda cuando viene marcada, devuelve
  `None` en `moneda` cuando no.
- Heurística de formato: casos felices, casos ambiguos con
  `asumir=...` resuelven correctamente.
- Sufijos `K`/`M`/`MM` y "mil"/"millones" funcionan.
- `formato_detectado` sobre la lista canónica de ejemplos da el
  esperado.
- Round-trip con `formato.pesos`: para una muestra,
  `parsear(formato.pesos(x)) == x` (con tolerancia float).
- Sin internet, sin archivos externos.

## Riesgos

- **Ambigüedad estructural.** `"1.500"` puede ser `1.5` o `1500`. La
  heurística por defecto puede equivocarse. Mitigación: documentar
  reglas explícitamente; permitir `asumir='argentino' | 'ingles'`;
  agregar `parsear_estricto` que devuelve `None` ante ambigüedad en
  vez de heurística.
- **Sufijos coloquiales.** `"1 palo"` (= 1 millón), `"500 lucas"`
  (= 500.000). Tentación de soportar argot. **Decisión:** NO.
  El módulo es para datos, no para texto natural. Documentarlo
  explícitamente.
- **Moneda implícita.** Un sistema podría exportar `"$ 1.500"` para
  USD. Mitigación: el módulo solo reporta moneda cuando viene
  marcada inequívocamente; nunca infiere por contexto.
- **Inflación.** Los rangos plausibles de pesos cambian. Mitigación:
  el módulo NO valida rangos plausibles — solo parsea. Eso lo hace
  inmune a inflación (criterio nuevo del proyecto: nada que envejezca).

## Prioridad

**Alta.** Operación frecuentísima en data cleaning de datos
económicos/contables argentinos. Hoy no hay alternativa en el paquete.
Cero deuda de mantenimiento — la lógica de parsing no envejece.

## Contexto adicional

- Originada por feedback del usuario (2026-05-13): preferir limpieza
  de datos general sobre módulos que requieran actualización
  periódica.
- Encaja con `formato.pesos` (ya implementado) como su inverso.
- Patrón consolidado: `clean`/`formato`/`matching`/`patentes` son
  todos módulos transversales sin dataset, esta propuesta sigue ese
  modelo.
- Convención `import argentina as arg` respetada.
