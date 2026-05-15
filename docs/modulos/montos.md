# Montos

`argentina.montos` parsea strings con montos monetarios y los convierte
a número. Es el **inverso** de [`argentina.formato.pesos`](formato.md).

Stdlib pura (`re` + `decimal`). Sin dataset, sin internet, sin
dependencia de mantenimiento — la lógica de parsing no envejece.

## Casos resueltos

```python
import argentina as arg

arg.montos.parsear("$ 1.500.000,50")    # 1500000.5  (formato argentino canónico)
arg.montos.parsear("$1.500.000")        # 1500000.0
arg.montos.parsear("1500000.50")        # 1500000.5  (formato "inglés")
arg.montos.parsear("ARS 1.500.000")     # 1500000.0
arg.montos.parsear("1,5M")              # 1500000.0  (sufijo corto)
arg.montos.parsear("1.5 millones")      # 1500000.0  (escala en texto)
arg.montos.parsear("500 mil")           # 500000.0
arg.montos.parsear("-1.500,50")         # -1500.5
arg.montos.parsear("no es un monto")    # None
```

Devuelve `None` para entradas inválidas (consistente con los
`limpiar_*` del paquete: nunca levanta para datos sucios).

## Reglas de detección de formato

| Entrada | Formato | Resultado |
|---|---|---|
| `"1.500,50"` | argentino | `1500.50` |
| `"1500.5"`   | inglés    | `1500.5`  |
| `"1,500.50"` | inglés (con miles) | `1500.5` |
| `"1.500.000"` | argentino (varios puntos) | `1500000` |
| `"1.500"` | **ambiguo** | heurística: `1500` (asume argentino) |

### Heurística

- **Tiene `,` y `.`** → el separador decimal es el **último** de los dos.
- **Solo `,`** → argentino: `,` es decimal.
- **Solo `.`** y 1–2 cifras después → inglés: `.` es decimal.
- **Solo `.`** y 3 cifras después → ambiguo (`"1.500"`). Default:
  argentino (miles). Cambialo con `asumir=...`.
- **Varios `.`** (`"1.500.000"`) → argentino seguro (miles).
- **Sin separadores** (`"1500000"`) → entero.

### Forzar interpretación

```python
arg.montos.parsear("1.500")                       # 1500.0 (heurística)
arg.montos.parsear("1.500", asumir="ingles")      # 1.5
arg.montos.parsear("1.500", asumir="argentino")   # 1500.0 (explícito)
```

### Modo estricto

Si preferís que falle a que adivine mal:

```python
arg.montos.parsear_estricto("1.500")              # None  (ambiguo)
arg.montos.parsear_estricto("1.500,50")           # 1500.5
arg.montos.parsear_estricto("1500.5")             # 1500.5
```

## Sufijos multiplicadores

Tabla cerrada (sin argot):

| Sufijo | Multiplicador |
|---|---|
| `K`, `mil`, `miles` | × 1.000 |
| `M`, `MM`, `mill`, `millón`, `millones` | × 1.000.000 |

```python
arg.montos.parsear("500K")          # 500000.0
arg.montos.parsear("2.5MM")         # 2500000.0
arg.montos.parsear("1.5 millones")  # 1500000.0
```

**No** se interpreta argot (`"1 palo"`, `"500 lucas"`). El módulo es
para datos, no texto natural.

## Precisión decimal

Para evitar errores de coma flotante en cálculos críticos:

```python
from decimal import Decimal

arg.montos.parsear_decimal("1.234,56")  # Decimal('1234.56')
arg.montos.parsear_decimal("0,1") + arg.montos.parsear_decimal("0,2")
# Decimal('0.3')   (no 0.30000000000000004)
```

## Detección de moneda

Solo cuando viene marcada **inequívocamente**:

```python
arg.montos.moneda_detectada("u$s 1.500")  # 'USD'
arg.montos.moneda_detectada("USD 100")     # 'USD'
arg.montos.moneda_detectada("100 dolares") # 'USD'
arg.montos.moneda_detectada("ARS 100")     # 'ARS'
arg.montos.moneda_detectada("100 pesos")   # 'ARS'

arg.montos.moneda_detectada("$ 1.500")     # None  ($ solo es ambiguo)
```

El módulo **no infiere moneda por contexto**: si la entrada es solo `$`,
devuelve `None`. Que sea ARS o USD lo decide el código que llama, no este
módulo.

## Parseo completo

Combina valor + moneda + formato:

```python
arg.montos.parsear_completo("u$s 1.500,50")
# Monto(valor=1500.5, moneda='USD', formato_detectado='argentino')

arg.montos.parsear_completo("ARS 1500.50")
# Monto(valor=1500.5, moneda='ARS', formato_detectado='ingles')
```

## Detección de formato (sin convertir)

Útil para auditar una columna antes de decidir cómo parsearla:

```python
arg.montos.formato_detectado("1.500.000,50")  # 'argentino'
arg.montos.formato_detectado("1,500,000.50")  # 'ingles'
arg.montos.formato_detectado("1500000")       # 'entero'
arg.montos.formato_detectado("1.500")         # 'ambiguo'
```

## Reexport en `formato`

Para descubribilidad bidireccional (formateo ↔ parseo):

```python
arg.formato.pesos(1500.5, decimales=2)        # '$ 1.500,50'
arg.formato.parsear_pesos("$ 1.500,50")       # 1500.5
```

`arg.formato.parsear_pesos` delega a `arg.montos.parsear` sin
reimplementar.

## Filosofía

- **Sin dataset** — solo lógica. Cero deuda de mantenimiento.
- **Sin internet, sin dependencias.**
- **Inmune a la inflación**: el módulo no valida rangos plausibles,
  solo parsea. No tiene nada que envejezca.
- **No infiere lo que no está**: moneda solo cuando viene marcada;
  formato ambiguo se reporta como tal en lugar de adivinar mal en
  silencio.
- Complemento natural de [`formato.pesos`](formato.md): pareja
  parseo ↔ formateo cerrada.
