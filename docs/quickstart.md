# Quickstart

5 minutos con `argentina`. Todos los ejemplos asumen:

```python
import argentina as arg
```

## Provincias y departamentos

```python
# Lookup flexible: nombre, código INDEC, ISO 3166-2, alias
arg.provincias.lookup("PBA")        # Buenos Aires
arg.provincias.lookup("Córdoba")    # Córdoba
arg.provincias.lookup("14")         # Córdoba (por código INDEC)
arg.provincias.lookup("AR-X")       # Córdoba (por ISO)

p = arg.provincias.CORDOBA
print(p.nombre, p.capital, p.region, p.poblacion_2022)
# Córdoba Córdoba Pampeana 3840905

# Iterable
for p in arg.provincias:
    print(p.nombre)

# Set completo de 529 departamentos del país
arg.departamentos.lookup("06427")          # La Matanza
arg.departamentos.por_provincia("PBA")     # 135 partidos
arg.departamentos.por_provincia("CABA")    # 15 comunas
```

## Identificadores

```python
# DNI
arg.personas.limpiar_dni("12.345.678")     # "12345678"
arg.personas.validar_dni("12345678")        # True
arg.personas.formatear_dni("12345678")      # "12.345.678"

# CUIT/CUIL con dígito verificador oficial
arg.personas.validar_cuit("20-12345678-6")  # True/False según dígito
arg.personas.calcular_digito_cuit("2012345678")
arg.personas.tipo_cuit("20-12345678-6")     # "persona_fisica"
arg.personas.extraer_dni_de_cuit("20-12345678-6")

# CBU
arg.bancos.validar_cbu("2850590940090418135201")
arg.bancos.formatear_cbu("28505909400904181352010")
```

## Códigos postales

```python
arg.postal.validar_cp4("1425")              # True (CP4 tradicional)
arg.postal.validar_cpa("C1425ABC")          # True (CPA argentino)
arg.postal.extraer_cp4("C1425ABC")          # "1425"
arg.postal.provincia_por_cpa("X5000AAA")    # "Córdoba"
arg.postal.validar_cpa_provincia("X5000AAA", "Córdoba")  # True
```

## Teléfonos

```python
arg.telefonos.limpiar("+54 9 11 1234-5678")           # "5491112345678"
arg.telefonos.normalizar_e164("011 4321-1234")        # "+541143211234"
arg.telefonos.es_celular("+54 9 351 1234567")         # True
arg.telefonos.provincia_por_caracteristica("+54 9 351 1234567")  # "Córdoba"
```

## Mapas en una línea

> Requiere `pip install "argentina[geo,maps]"`.

```python
m = arg.geo.mapa_de("Córdoba")
m                                     # se renderiza en Jupyter
m.save("cordoba.html")                # o guardar a HTML
```

Provincia con fondo Argenmap del IGN, polígono, marker en la capital y
créditos — todo en una línea. La toponimia es la oficial argentina
(Islas Malvinas incluidas).

## Series económicas

> Requiere `pip install "argentina[economia]"`.

```python
from argentina import economia

ipc = economia.ipc_nacional(start_date="2020-01-01")
print(ipc.tail())

# 493 series económicas oficiales (INDEC, BCRA, SSPM)
print(len(economia.SERIES))
economia.buscar("salario").head()
```

## EPH (microdatos INDEC)

> Requiere `pip install "argentina[data]"`.

```python
ind = arg.data.eph(anio=2024, periodo="trimestral", numero=1, tipo="individual")
print(f"{len(ind):,} personas, {len(ind.columns)} columnas")
# 46050 personas, 235 columnas (CODUSU, CH04, CH06, PONDERA, P21, ESTADO, ...)
```

La primera llamada baja el ZIP oficial del INDEC (~3-5 MB) y lo cachea en
`~/.cache/argentina/eph/`. Las siguientes son cache hits.

## Formato canónico para mostrar

```python
arg.formato.dni("12345678")                # '12.345.678'
arg.formato.cuit("20123456786")            # '20-12345678-6'
arg.formato.pesos(1_500_000)               # '$ 1.500.000'
arg.formato.pesos(1_500_000.5, decimales=2)  # '$ 1.500.000,50'
arg.formato.telefono("1140404040")         # '(011) 4040-4040'
arg.formato.fecha("2026-05-13", estilo="largo")  # '13 de mayo de 2026'
```

Un único punto de entrada (`arg.formato.*`) para todo lo que normalmente
escribís a mano en cada reporte.

## Ajustar montos por IPC (offline)

```python
from datetime import date

# Convertir 10.000 pesos de enero 2017 a enero 2024
arg.indices.ajustar_ipc(
    10_000,
    desde=date(2017, 1, 1),
    hasta=date(2024, 1, 1),
)
arg.indices.uva(date(2024, 1, 1))
arg.indices.disponibles()       # ('ipc_nacional', 'uva', 'cer', 'icl')
```

`indices` corre con stdlib (sin red, snapshot embebido). Si necesitás la
serie completa online, está `arg.economia` con el extra `[economia]`.

## Monotributo, IVA y Ganancias (tablas AFIP)

```python
# Categoría de monotributo según facturación anual
arg.afip.monotributo_categoria_por_facturacion(12_000_000, anio=2024)

# Alícuotas IVA del año
arg.afip.alicuotas_iva(anio=2026)
# {'general': 0.21, 'reducida': 0.105, 'especial': 0.27}

# Mínimo no imponible Ganancias
arg.afip.ganancias_minimo_no_imponible(anio=2024)
```

`arg.afip` solo expone tablas oficiales: no es un motor fiscal, no
calcula impuestos, no liquida. Para uso real, AFIP o un profesional.

## Para seguir

- **[Filosofía](filosofia.md)** — diseño y trade-offs.
- **[Extras opcionales](extras.md)** — todos los extras y qué traen.
- **[Módulos](modulos/provincias.md)** — referencia detallada.
