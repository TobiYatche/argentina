"""Distancia geográfica entre puntos / ciudades / provincias.

Implementa la fórmula de **haversine** (esfera de radio medio terrestre)
sin dependencias externas — solo `math` de stdlib. Resultado en km.

Acepta:

- Tuplas ``(lat, lon)`` directas.
- Strings que ``argentina.ciudades.lookup`` reconoce (nombre o alias).
- Strings que ``argentina.provincias.lookup`` reconoce (en cuyo caso se usan
  las coordenadas de la **capital** de la provincia).
- Objetos ``Ciudad`` o ``Provincia`` directamente.

Ejemplos::

    arg.geo.distancia("Buenos Aires", "Córdoba")           # ~696 km
    arg.geo.distancia("CABA", "Ushuaia")                    # ~3035 km
    arg.geo.distancia((-34.6, -58.4), (-31.4, -64.2))       # tuplas
    arg.geo.distancia(arg.provincias.CORDOBA, arg.ciudades.lookup("Rosario"))
"""

from __future__ import annotations

import math
from typing import Any

RADIO_TIERRA_KM = 6371.0088  # radio medio (WGS84)


def _coords(punto: Any) -> tuple[float, float]:
    """Resuelve cualquier representación a una tupla ``(lat, lon)``."""
    if punto is None:
        raise ValueError("no se puede calcular distancia con None")

    # Tupla / lista (lat, lon)
    if isinstance(punto, (tuple, list)) and len(punto) == 2:
        lat, lon = punto
        return float(lat), float(lon)

    # Provincia
    from argentina.provincias import Provincia as _Provincia
    if isinstance(punto, _Provincia):
        if punto.capital_lat is None or punto.capital_lon is None:
            raise ValueError(
                f"{punto.nombre}: sin coordenadas de capital en el catálogo"
            )
        return punto.capital_lat, punto.capital_lon

    # Ciudad
    from argentina.ciudades import Ciudad as _Ciudad
    if isinstance(punto, _Ciudad):
        if punto.lat is None or punto.lon is None:
            raise ValueError(f"{punto.nombre}: sin coordenadas")
        return punto.lat, punto.lon

    # String → buscamos primero en ciudades, después en provincias
    if isinstance(punto, str):
        from argentina.ciudades import lookup as _lookup_ciudad
        from argentina.provincias import lookup as _lookup_prov

        c = _lookup_ciudad(punto)
        if c is not None and c.lat is not None:
            return c.lat, c.lon
        p = _lookup_prov(punto)
        if p is not None and p.capital_lat is not None:
            return p.capital_lat, p.capital_lon
        raise ValueError(f"no se reconoce como ciudad ni provincia: {punto!r}")

    raise TypeError(f"tipo no soportado para coordenadas: {type(punto).__name__}")


def distancia(a: Any, b: Any) -> float:
    """Distancia haversine entre dos puntos, en kilómetros.

    Cada argumento puede ser:

    - ``(lat, lon)`` — tupla o lista
    - ``str`` — nombre o alias de ciudad/provincia del paquete
    - ``Ciudad`` / ``Provincia``
    """
    lat1, lon1 = _coords(a)
    lat2, lon2 = _coords(b)

    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    h = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
    return 2 * RADIO_TIERRA_KM * math.asin(math.sqrt(h))


__all__ = ["distancia", "RADIO_TIERRA_KM"]
