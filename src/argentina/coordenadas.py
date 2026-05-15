"""Acceso unificado a coordenadas (lat, lon) de cualquier entidad del paquete.

``arg.coordenadas(valor)`` recibe lo que sea (nombre de ciudad, código IATA
de aeropuerto, nombre/ISO de provincia, una tupla ya armada, un objeto
``Ciudad``/``Provincia``/``Aeropuerto``) y devuelve siempre la misma
tupla ``(lat, lon)`` — o ``None`` si no se reconoce.

Ejemplos::

    arg.coordenadas("Córdoba")          # (-31.42, -64.19)  [ciudad]
    arg.coordenadas("PBA")              # (-34.92, -57.95)  [provincia → capital]
    arg.coordenadas("EZE")              # (-34.82, -58.54)  [aeropuerto]
    arg.coordenadas((-34.6, -58.4))     # (-34.6, -58.4)    [passthrough]
    arg.coordenadas(arg.provincias.CORDOBA)  # idem ciudad ↑
"""

from __future__ import annotations

from typing import Any


def coordenadas(valor: Any) -> tuple[float, float] | None:
    """Devuelve ``(lat, lon)`` de cualquier ciudad/provincia/aeropuerto del paquete.

    Prioridad de resolución cuando hay ambigüedad (ej. ``"Córdoba"`` es ciudad
    Y provincia): primero ciudad, después provincia, después aeropuerto.
    Para provincias usa las coordenadas de la **capital**.

    Returns
    -------
    tuple[float, float] | None
    """
    if valor is None:
        return None

    # Tupla / lista ya armada (passthrough con conversión a float)
    if isinstance(valor, (tuple, list)) and len(valor) == 2:
        try:
            return float(valor[0]), float(valor[1])
        except (TypeError, ValueError):
            return None

    # Objetos del paquete
    from argentina.provincias import Provincia as _Provincia
    if isinstance(valor, _Provincia):
        if valor.capital_lat is None or valor.capital_lon is None:
            return None
        return valor.capital_lat, valor.capital_lon

    from argentina.ciudades import Ciudad as _Ciudad
    if isinstance(valor, _Ciudad):
        if valor.lat is None or valor.lon is None:
            return None
        return valor.lat, valor.lon

    from argentina.aeropuertos import Aeropuerto as _Aeropuerto
    if isinstance(valor, _Aeropuerto):
        if valor.lat is None or valor.lon is None:
            return None
        return valor.lat, valor.lon

    # String: probamos ciudad → provincia → aeropuerto
    if isinstance(valor, str):
        from argentina.ciudades import lookup as _l_ciudad
        c = _l_ciudad(valor)
        if c is not None and c.lat is not None:
            return c.lat, c.lon

        from argentina.provincias import lookup as _l_prov
        p = _l_prov(valor)
        if p is not None and p.capital_lat is not None:
            return p.capital_lat, p.capital_lon

        from argentina.aeropuertos import lookup as _l_aero
        a = _l_aero(valor)
        if a is not None and a.lat is not None:
            return a.lat, a.lon

    return None


__all__ = ["coordenadas"]
