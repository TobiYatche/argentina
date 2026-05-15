# Formato

`argentina.formato` es el **punto único de entrada para formatear**
datos argentinos para mostrar. Agrupa funciones nuevas (teléfono, pesos,
código postal, fecha) y re-exporta las `formatear_*` que ya viven en
otros módulos.

Convenciones:

- Todas las funciones devuelven `str` o `None` si el input no es
  formateable. Nunca levantan excepciones para datos inválidos
  (consistente con `limpiar_*` y `validar_*`).
- Stdlib pura. Sin dependencias externas. Sin internet.
- La localización argentina (separadores `.` y `,`, meses en español)
  está hardcodeada — el paquete entero asume Argentina.

## ¿Qué función uso?

| Necesito formatear… | Función |
|---|---|
| Teléfono | `arg.formato.telefono` |
| Monto en pesos | `arg.formato.pesos` |
| Código postal (CP4 o CPA) | `arg.formato.codigo_postal` |
| Fecha | `arg.formato.fecha` |
| DNI | `arg.formato.dni` (reexport de `personas`) |
| CUIT/CUIL | `arg.formato.cuit` (reexport de `personas`) |
| CBU | `arg.formato.cbu` (reexport de `bancos`) |
| Patente | `arg.formato.patente` (reexport de `patentes`) |

## Teléfono

```python
import argentina as arg

arg.formato.telefono("1140404040")
# '(011) 4040-4040'

arg.formato.telefono("1140404040", estilo="e164")
# '+541140404040'

arg.formato.telefono("+5491140404040", estilo="internacional")
# '+54 9 11 4040-4040'
```

Estilos válidos: `"nacional"` (default), `"e164"`, `"internacional"`.

Acepta cualquier formato que entienda `arg.telefonos.validar`. Para
números celulares, los estilos `e164` e `internacional` agregan el `9` de
movilidad.

## Pesos

```python
arg.formato.pesos(1_500_000)
# '$ 1.500.000'

arg.formato.pesos(1_500_000.5, decimales=2)
# '$ 1.500.000,50'

arg.formato.pesos(-1000)
# '-$ 1.000'

arg.formato.pesos(100, simbolo="ARS ")
# 'ARS 100'

arg.formato.pesos(100, simbolo="")
# '100'
```

- Separador de miles: `.` (punto).
- Separador decimal: `,` (coma).
- Para montos negativos el signo va **antes** del símbolo.
- `decimales=0` (default) no muestra coma.

## Código postal

```python
arg.formato.codigo_postal("1414")          # '1414'  (CP4)
arg.formato.codigo_postal("C1414BAA")      # 'C1414BAA'  (CPA)
arg.formato.codigo_postal("c1414baa")      # 'C1414BAA'  (normaliza)
arg.formato.codigo_postal("  C1414-BAA ")  # 'C1414BAA'  (limpia)
arg.formato.codigo_postal("xyz")           # None
```

Internamente usa `arg.postal.limpiar_codigo_postal` y valida con
`validar_cpa` / `validar_cp4`.

## Fecha

```python
from datetime import date

arg.formato.fecha(date(2026, 5, 13))
# '13/05/2026'

arg.formato.fecha("13/05/2026", estilo="largo")
# '13 de mayo de 2026'

arg.formato.fecha("2026-05-13", estilo="iso")
# '2026-05-13'
```

Estilos válidos: `"corto"` (default), `"largo"`, `"iso"`.

Acepta cualquier input que entienda `arg.fechas.parsear_fecha` (`date`,
`datetime`, strings `dd/mm/aaaa`, ISO, etc.).

Los nombres de mes en español están hardcodeados (sin `locale`).

## Reexports

```python
arg.formato.dni("12345678")              # '12.345.678'
arg.formato.cuit("20123456786")          # '20-12345678-6'
arg.formato.cbu("2850590940090418135201")  # '28505909-40090418135201'
arg.formato.patente("AB123CD")           # 'AB 123 CD'
```

Cada reexport llama a la implementación original — no la copia. Si la
función original cambia, el reexport refleja el cambio inmediatamente.

La implementación canónica sigue viviendo en `personas`, `bancos` y
`patentes`. `formato` agrega un nombre estándar y un punto de entrada
descubrible.

## Casos borde

Todas las funciones devuelven `None` para inputs inválidos:

```python
arg.formato.telefono(None)          # None
arg.formato.telefono("123")         # None  (no llega a 10 dígitos válidos)
arg.formato.pesos("xx")             # None
arg.formato.codigo_postal("999")    # None  (no es CP4 ni CPA)
arg.formato.fecha("asdf")           # None
```

`telefono` y `fecha` levantan `ValueError` solo si se pasa un `estilo`
no reconocido (error de programador, no de input).
