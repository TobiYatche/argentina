"""Constantes invariantes de la República Argentina.

Datos que no cambian (códigos, prefijos, capital, bbox geográfico, etc.) más
algunos agregados derivados del Censo 2022.
"""

from __future__ import annotations


# Identificadores oficiales
NOMBRE_OFICIAL = "República Argentina"
NOMBRE = "Argentina"
CODIGO_ISO = "AR"        # ISO 3166-1 alfa-2
CODIGO_ISO_3 = "ARG"     # ISO 3166-1 alfa-3
CODIGO_NUMERICO = "032"  # ISO 3166-1 numérico

# Comunicación / internet
TELEFONO_PREFIJO = "+54"
TLD = ".ar"
IDIOMA = "es-AR"

# Geografía
CAPITAL = "Ciudad Autónoma de Buenos Aires"
HUSO_HORARIO = "UTC-3"
# Bounding box continental aproximado (lon_min, lat_min, lon_max, lat_max)
BBOX = (-73.5, -55.0, -53.6, -21.8)
# Centro geográfico aproximado (provincia de La Pampa, oficialmente declarado)
CENTRO_GEOGRAFICO = (-35.83, -64.5)

# Superficie y población — derivados del Censo 2022 y catastro oficial
SUPERFICIE_CONTINENTAL_KM2 = 2_791_810   # suma de superficies provinciales del INDEC
SUPERFICIE_CON_RECLAMOS_KM2 = 3_761_274  # incluye Antártida Argentina y Atlántico Sur
POBLACION_2022 = 45_892_285              # Censo Nacional 2022 (INDEC)

# Moneda actual
MONEDA = "ARS"
MONEDA_NOMBRE = "Peso argentino"
MONEDA_SIMBOLO = "$"

# Estructura administrativa
CANTIDAD_PROVINCIAS = 24  # 23 provincias + CABA
CANTIDAD_DEPARTAMENTOS = 529


__all__ = [
    "NOMBRE_OFICIAL",
    "NOMBRE",
    "CODIGO_ISO",
    "CODIGO_ISO_3",
    "CODIGO_NUMERICO",
    "TELEFONO_PREFIJO",
    "TLD",
    "IDIOMA",
    "CAPITAL",
    "HUSO_HORARIO",
    "BBOX",
    "CENTRO_GEOGRAFICO",
    "SUPERFICIE_CONTINENTAL_KM2",
    "SUPERFICIE_CON_RECLAMOS_KM2",
    "POBLACION_2022",
    "MONEDA",
    "MONEDA_NOMBRE",
    "MONEDA_SIMBOLO",
    "CANTIDAD_PROVINCIAS",
    "CANTIDAD_DEPARTAMENTOS",
]
