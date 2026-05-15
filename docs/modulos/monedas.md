# Monedas

`argentina.monedas` cubre la historia de la moneda argentina: m$n, Peso Ley
18.188, Peso Argentino, Austral y Peso (ARS, actual). Permite saber qué
moneda regía en una fecha y hacer conversiones **nominales** entre épocas
(siguiendo los cambios oficiales y los ceros que se quitaron en cada reforma).

```python
import argentina as arg
from datetime import date

arg.monedas.actual()                # Moneda(codigo_iso='ARS', ...)
arg.monedas.en(date(1986, 6, 1))    # Austral
arg.monedas.en(date(1975, 1, 1))    # Peso Ley 18.188

arg.monedas.lookup("austral")
arg.monedas.lookup("ARS")
arg.monedas.lookup("$a")
```

## Conversión nominal

```python
arg.monedas.convertir(10_000, "₳")          # → 1.0 peso actual
arg.monedas.convertir(1_000_000, "m$n")     # → 1e-7 pesos actuales
arg.monedas.convertir(100, "ARS", "ARP")    # ARS → Peso Argentino histórico
```

> **Importante:** `convertir` es **nominal**, no ajusta por inflación.
> Para deflactar/inflar usando el IPC oficial está `argentina.economia`.

## Atributos de `Moneda`

```python
m = arg.monedas.lookup("ARS")

m.codigo_iso         # "ARS"
m.simbolo            # "$"
m.nombre             # "Peso"
m.desde              # date(1992, 1, 1)
m.hasta              # None (vigente)
m.factor_a_actual    # 1.0
```

## Listar y exportar

```python
arg.monedas.listar()
arg.monedas.como_tabla()       # lista de dicts, lista para DataFrame
arg.monedas.mapping("codigo_iso", "simbolo")
# {"ARM": "m$n", "ARL": "$Ley", "ARP": "$a", "ARA": "₳", "ARS": "$"}
```

Stdlib pura, sin red, sin pandas.
