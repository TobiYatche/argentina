"""Países limítrofes de la Argentina.

5 países que comparten frontera con Argentina, con código ISO, nombre,
longitud aproximada de la frontera (km) y las provincias argentinas que
hacen frontera con cada uno.

Datos embebidos, sin dependencias externas.
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from functools import lru_cache
from importlib.resources import files


# Provincias argentinas que hacen frontera con cada país (por código ISO).
# Hardcodeado porque no cambia y es chico.
_PROVINCIAS_FRONTERIZAS = {
    "BR": ("Misiones", "Corrientes"),
    "BO": ("Jujuy", "Salta", "Formosa"),
    "CL": (
        "Jujuy", "Salta", "Catamarca", "La Rioja", "San Juan",
        "Mendoza", "Neuquén", "Río Negro", "Chubut", "Santa Cruz",
        "Tierra del Fuego",
    ),
    "PY": ("Formosa", "Chaco", "Misiones", "Corrientes"),
    "UY": ("Entre Ríos", "Corrientes", "Buenos Aires"),
}


@dataclass(frozen=True)
class PaisLimitrofe:
    codigo_iso: str        # ISO 3166-1 alfa-2 (BR, CL, ...)
    codigo_iso_3: str      # ISO 3166-1 alfa-3 (BRA, CHL, ...)
    nombre: str
    nombre_corto: str
    frontera_km: int       # longitud aproximada de la frontera
    provincias_argentinas: tuple

    def como_dict(self) -> dict:
        return asdict(self)

    def _repr_html_(self) -> str:
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>ISO</td>"
            f"<td style='padding:2px 8px'><code>{self.codigo_iso}</code> / "
            f"<code>{self.codigo_iso_3}</code></td></tr>"
            f"<tr><td style='padding:2px 8px'>frontera</td>"
            f"<td style='padding:2px 8px'>{self.frontera_km:,} km</td></tr>"
            f"<tr><td style='padding:2px 8px'>provincias argentinas</td>"
            f"<td style='padding:2px 8px'>{', '.join(self.provincias_argentinas)}</td></tr>"
            "</table>"
        )


@lru_cache(maxsize=128)
def _normalizar(texto: str | None) -> str:
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def _cargar() -> tuple[PaisLimitrofe, ...]:
    path = files("argentina").joinpath("data/paises_limitrofes.csv")
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return tuple(
        PaisLimitrofe(
            codigo_iso=r["codigo_iso"],
            codigo_iso_3=r["codigo_iso_3"],
            nombre=r["nombre"],
            nombre_corto=r["nombre_corto"],
            frontera_km=int(r["frontera_km"]),
            provincias_argentinas=_PROVINCIAS_FRONTERIZAS[r["codigo_iso"]],
        )
        for r in rows
    )


PAISES_LIMITROFES = _cargar()

_POR_ISO = {p.codigo_iso: p for p in PAISES_LIMITROFES}
_POR_ISO3 = {p.codigo_iso_3: p for p in PAISES_LIMITROFES}
_POR_NOMBRE = {_normalizar(p.nombre): p for p in PAISES_LIMITROFES}


def lookup(valor: str | None) -> PaisLimitrofe | None:
    """Busca un país limítrofe por código ISO (alfa-2 o alfa-3) o nombre."""
    if valor is None:
        return None
    s = str(valor).strip().upper()
    if not s:
        return None
    if len(s) == 2 and s in _POR_ISO:
        return _POR_ISO[s]
    if len(s) == 3 and s in _POR_ISO3:
        return _POR_ISO3[s]
    n = _normalizar(valor)
    return _POR_NOMBRE.get(n)


def listar() -> tuple[PaisLimitrofe, ...]:
    """Devuelve los 5 países limítrofes."""
    return PAISES_LIMITROFES


def por_provincia(provincia: str | None) -> tuple[PaisLimitrofe, ...]:
    """Países limítrofes con los que limita una provincia argentina.

    Acepta cualquier identificador que entienda ``arg.provincias.lookup``.
    """
    if provincia is None:
        return ()
    from argentina.provincias import lookup as _l
    p = _l(provincia)
    if p is None:
        return ()
    return tuple(
        pais for pais in PAISES_LIMITROFES
        if p.nombre in pais.provincias_argentinas
    )


def como_tabla() -> list[dict]:
    """Lista de dicts apta para ``pandas.DataFrame``."""
    return [p.como_dict() for p in PAISES_LIMITROFES]


# Módulo iterable
import types as _types


class _Modulo(_types.ModuleType):
    def __iter__(self):
        return iter(PAISES_LIMITROFES)

    def __len__(self):
        return len(PAISES_LIMITROFES)

    def __contains__(self, item):
        if isinstance(item, PaisLimitrofe):
            return item in PAISES_LIMITROFES
        return lookup(item) is not None


sys.modules[__name__].__class__ = _Modulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.paises_limitrofes.mapping("codigo_iso", "nombre")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(PAISES_LIMITROFES, de, a)


__all__ = [
    "PaisLimitrofe",
    "PAISES_LIMITROFES",
    "lookup",
    "listar",
    "por_provincia",
    "como_tabla",
    "mapping",
]
