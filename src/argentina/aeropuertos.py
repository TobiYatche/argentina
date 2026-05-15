"""Aeropuertos argentinos con códigos IATA / ICAO.

Set curado de los aeropuertos comerciales del país (~39), con código IATA
(3 letras), ICAO (4 letras), nombre, ciudad, provincia, lat/lon y tipo
(``"internacional"`` o ``"cabotaje"``). Datos embebidos, sin dependencias.
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from functools import lru_cache
from importlib.resources import files


@dataclass(frozen=True)
class Aeropuerto:
    iata: str
    icao: str
    nombre: str
    ciudad: str
    provincia_codigo: str
    provincia_nombre: str
    lat: float | None
    lon: float | None
    tipo: str  # "internacional" o "cabotaje"

    def _repr_html_(self) -> str:
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.iata} — {self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>ICAO</td>"
            f"<td style='padding:2px 8px'><code>{self.icao}</code></td></tr>"
            f"<tr><td style='padding:2px 8px'>ciudad</td>"
            f"<td style='padding:2px 8px'>{self.ciudad}, {self.provincia_nombre}</td></tr>"
            f"<tr><td style='padding:2px 8px'>tipo</td>"
            f"<td style='padding:2px 8px'>{self.tipo}</td></tr>"
            f"<tr><td style='padding:2px 8px'>coords</td>"
            f"<td style='padding:2px 8px'><code>{self.lat}, {self.lon}</code></td></tr>"
            "</table>"
        )

    def como_dict(self) -> dict:
        """Devuelve el aeropuerto como diccionario plano."""
        return asdict(self)


@lru_cache(maxsize=512)
def _normalizar(texto: str | None) -> str:
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _cargar() -> tuple[Aeropuerto, ...]:
    path = files("argentina").joinpath("data/aeropuertos.csv")
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        out.append(
            Aeropuerto(
                iata=r["iata"].upper(),
                icao=r["icao"].upper(),
                nombre=r["nombre"],
                ciudad=r["ciudad"],
                provincia_codigo=r["provincia_codigo"].zfill(2),
                provincia_nombre=r["provincia_nombre"],
                lat=float(r["lat"]) if r.get("lat") else None,
                lon=float(r["lon"]) if r.get("lon") else None,
                tipo=r["tipo"],
            )
        )
    return tuple(out)


AEROPUERTOS = _cargar()

_POR_IATA = {a.iata: a for a in AEROPUERTOS}
_POR_ICAO = {a.icao: a for a in AEROPUERTOS}
_POR_NOMBRE = {_normalizar(a.nombre): a for a in AEROPUERTOS}
_POR_CIUDAD = {_normalizar(a.ciudad): a for a in AEROPUERTOS}


def lookup(valor: str | None) -> Aeropuerto | None:
    """Busca un aeropuerto por código IATA, ICAO, nombre o ciudad.

    Acepta:
    - código **IATA** (3 letras, ej. ``"EZE"``, ``"AEP"``)
    - código **ICAO** (4 letras, ej. ``"SAEZ"``)
    - nombre del aeropuerto (case-insensitive, sin tildes)
    - ciudad donde está (devuelve el primer match)
    """
    if valor is None:
        return None
    s = str(valor).strip().upper()
    if not s:
        return None
    # IATA exacto (3)
    if len(s) == 3 and s in _POR_IATA:
        return _POR_IATA[s]
    # ICAO exacto (4)
    if len(s) == 4 and s in _POR_ICAO:
        return _POR_ICAO[s]
    # Por nombre / ciudad normalizado
    n = _normalizar(valor)
    if n in _POR_NOMBRE:
        return _POR_NOMBRE[n]
    if n in _POR_CIUDAD:
        return _POR_CIUDAD[n]
    # Match parcial: "iguazu" → IGR
    for nombre_norm, a in _POR_NOMBRE.items():
        if n in nombre_norm:
            return a
    for ciudad_norm, a in _POR_CIUDAD.items():
        if n in ciudad_norm:
            return a
    return None


def listar() -> tuple[Aeropuerto, ...]:
    """Devuelve todos los aeropuertos del set."""
    return AEROPUERTOS


def por_provincia(provincia: str | None) -> tuple[Aeropuerto, ...]:
    """Aeropuertos en una provincia.

    Acepta cualquier identificador que entienda ``arg.provincias.lookup``.
    """
    if provincia is None:
        return ()
    from argentina.provincias import lookup as _lookup_prov
    p = _lookup_prov(provincia)
    if p is None:
        return ()
    return tuple(a for a in AEROPUERTOS if a.provincia_codigo == p.codigo_indec)


def como_tabla() -> list[dict]:
    """Devuelve los aeropuertos como lista de dicts."""
    return [a.como_dict() for a in AEROPUERTOS]


def internacionales() -> tuple[Aeropuerto, ...]:
    """Solo aeropuertos internacionales."""
    return tuple(a for a in AEROPUERTOS if a.tipo == "internacional")


def cabotaje() -> tuple[Aeropuerto, ...]:
    """Solo aeropuertos de cabotaje."""
    return tuple(a for a in AEROPUERTOS if a.tipo == "cabotaje")


# Módulo iterable
import types as _types


class _AeropuertosModulo(_types.ModuleType):
    def __iter__(self):
        return iter(AEROPUERTOS)

    def __len__(self):
        return len(AEROPUERTOS)

    def __contains__(self, item):
        if isinstance(item, Aeropuerto):
            return item in AEROPUERTOS
        return lookup(item) is not None


sys.modules[__name__].__class__ = _AeropuertosModulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.aeropuertos.mapping("iata", "nombre")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(AEROPUERTOS, de, a)


__all__ = [
    "Aeropuerto",
    "AEROPUERTOS",
    "lookup",
    "listar",
    "por_provincia",
    "internacionales",
    "cabotaje",
    "como_tabla",
    "mapping",
]
