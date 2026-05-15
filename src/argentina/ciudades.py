"""Ciudades argentinas principales con lookup flexible.

Set curado de las 30+ ciudades principales del país (todas las capitales
provinciales más los grandes aglomerados urbanos). Datos de población del
**Censo Nacional 2022 (INDEC)** — corresponden al municipio/partido/comuna,
no al aglomerado urbano completo.

``lookup`` acepta nombre, alias coloquiales (``"mardel"``, ``"tucuman"``...)
y es case-insensitive. Sin dependencias externas, datos embebidos.
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
class Ciudad:
    nombre: str
    provincia_codigo: str
    provincia_nombre: str
    poblacion_2022: int | None = None  # Censo Nacional 2022 (INDEC)
    lat: float | None = None
    lon: float | None = None

    @property
    def es_capital_provincial(self) -> bool:
        """``True`` si esta ciudad es la capital de su provincia."""
        from argentina.provincias import lookup as _l_prov
        p = _l_prov(self.provincia_codigo)
        if p is None:
            return False
        # Match por lookup: si arg.ciudades.lookup(p.capital) devuelve esta misma
        # ciudad, es la capital. Esto resuelve casos como CABA, donde la ciudad
        # se llama "Buenos Aires" pero la capital provincial es "Ciudad Autónoma
        # de Buenos Aires" (alias registrado en _ALIASES).
        cap_ciudad = lookup(p.capital)
        return cap_ciudad is not None and cap_ciudad.nombre == self.nombre

    def como_dict(self) -> dict:
        """Devuelve la ciudad como diccionario plano (apto para JSON / DataFrame)."""
        return asdict(self)

    def _repr_html_(self) -> str:
        pob = ""
        if self.poblacion_2022 is not None:
            pob_fmt = f"{self.poblacion_2022:,}".replace(",", ".")
            pob = (
                f"<tr><td style='padding:2px 8px'>población (2022)</td>"
                f"<td style='padding:2px 8px'>{pob_fmt}</td></tr>"
            )
        coords = ""
        if self.lat is not None and self.lon is not None:
            coords = (
                f"<tr><td style='padding:2px 8px'>coords</td>"
                f"<td style='padding:2px 8px'>"
                f"<code>{self.lat:.4f}, {self.lon:.4f}</code></td></tr>"
            )
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>provincia</td>"
            f"<td style='padding:2px 8px'>{self.provincia_nombre} "
            f"(<code>{self.provincia_codigo}</code>)</td></tr>"
            f"{pob}{coords}"
            "</table>"
        )


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


def _cargar_ciudades() -> tuple[Ciudad, ...]:
    path = files("argentina").joinpath("data/ciudades.csv")
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        ciudades = []
        for row in reader:
            pob = row.get("poblacion_2022")
            lat = row.get("lat")
            lon = row.get("lon")
            ciudades.append(
                Ciudad(
                    nombre=row["nombre"],
                    provincia_codigo=row["provincia_codigo"].zfill(2),
                    provincia_nombre=row["provincia_nombre"],
                    poblacion_2022=int(pob) if pob else None,
                    lat=float(lat) if lat else None,
                    lon=float(lon) if lon else None,
                )
            )
    return tuple(ciudades)


CIUDADES = _cargar_ciudades()


_ALIASES = {
    # Atajos coloquiales y abreviaciones habituales.
    "caba": "Buenos Aires",
    "capital federal": "Buenos Aires",
    "ciudad autonoma de buenos aires": "Buenos Aires",
    "ciudad de buenos aires": "Buenos Aires",
    "bsas": "Buenos Aires",
    "mardel": "Mar del Plata",
    "tucuman": "San Miguel de Tucumán",
    "jujuy": "San Salvador de Jujuy",
    "catamarca": "San Fernando del Valle de Catamarca",
    "comodoro": "Comodoro Rivadavia",
    "carlos paz": "Villa Carlos Paz",
}


_POR_NOMBRE = {_normalizar(c.nombre): c for c in CIUDADES}


def lookup(valor: str | None, *, fuzzy: bool = False, cutoff: float = 0.75) -> Ciudad | None:
    """Busca una ciudad por nombre o alias.

    Acepta nombres con o sin tildes, case-insensitive, y aliases comunes
    (``"CABA"``, ``"mardel"``, ``"Tucumán"`` para ``"San Miguel de Tucumán"``,
    ``"Catamarca"`` para la ciudad capital homónima, etc.).

    Si ``fuzzy=True`` y no hay match exacto, busca por similitud (typos):

    >>> arg.ciudades.lookup("rosrio", fuzzy=True)    # Rosario
    """
    if valor is None:
        return None
    n = _normalizar(valor)
    if not n:
        return None
    if n in _POR_NOMBRE:
        return _POR_NOMBRE[n]
    for alias, nombre_real in _ALIASES.items():
        if _normalizar(alias) == n:
            return _POR_NOMBRE.get(_normalizar(nombre_real))
    if fuzzy:
        from difflib import get_close_matches
        match = get_close_matches(n, _POR_NOMBRE.keys(), n=1, cutoff=cutoff)
        if match:
            return _POR_NOMBRE[match[0]]
    return None


def listar() -> tuple[Ciudad, ...]:
    """Devuelve todas las ciudades del set."""
    return CIUDADES


def por_provincia(provincia: str | None) -> tuple[Ciudad, ...]:
    """Devuelve ciudades de una provincia.

    Acepta cualquier identificador que entienda
    ``argentina.provincias.lookup`` (nombre, código INDEC, ISO o alias).
    """
    if provincia is None:
        return ()
    from argentina.provincias import lookup as _lookup_prov
    p = _lookup_prov(provincia)
    if p is None:
        return ()
    return tuple(c for c in CIUDADES if c.provincia_codigo == p.codigo_indec)


def top(n: int = 10) -> tuple[Ciudad, ...]:
    """Devuelve las ``n`` ciudades más pobladas (Censo 2022)."""
    con_pob = [c for c in CIUDADES if c.poblacion_2022 is not None]
    con_pob.sort(key=lambda c: c.poblacion_2022 or 0, reverse=True)
    return tuple(con_pob[:n])


def como_tabla() -> list[dict]:
    """Devuelve todas las ciudades como lista de dicts.

    Pensado para ``pandas.DataFrame(arg.ciudades.como_tabla())``.
    """
    return [c.como_dict() for c in CIUDADES]


# Módulo iterable: `for c in argentina.ciudades: ...`
import types as _types


class _CiudadesModulo(_types.ModuleType):
    def __iter__(self):
        return iter(CIUDADES)

    def __len__(self):
        return len(CIUDADES)

    def __contains__(self, item):
        if isinstance(item, Ciudad):
            return item in CIUDADES
        return lookup(item) is not None


sys.modules[__name__].__class__ = _CiudadesModulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.ciudades.mapping("nombre", "poblacion_2022")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(CIUDADES, de, a)


__all__ = [
    "Ciudad",
    "CIUDADES",
    "lookup",
    "listar",
    "por_provincia",
    "top",
    "como_tabla",
    "mapping",
]
