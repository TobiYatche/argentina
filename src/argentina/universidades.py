"""Universidades nacionales argentinas.

Set curado de las 53 universidades nacionales argentinas creadas por ley
nacional, con sigla, nombre completo, provincia, sede y año de fundación.
Datos embebidos, sin dependencias externas.

Notas:
- Se incluyen universidades **nacionales** (no privadas ni provinciales).
- El año de fundación es el de la primera creación; en algunos casos
  (UNC = 1613, UBA = 1821) corresponde a antecedentes coloniales o
  pre-nacionales.
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
class Universidad:
    sigla: str
    nombre: str
    provincia_codigo: str
    provincia_nombre: str
    sede: str
    anio_fundacion: int
    tipo: str  # por ahora siempre "nacional"

    def _repr_html_(self) -> str:
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.sigla} — {self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>provincia</td>"
            f"<td style='padding:2px 8px'>{self.provincia_nombre}</td></tr>"
            f"<tr><td style='padding:2px 8px'>sede principal</td>"
            f"<td style='padding:2px 8px'>{self.sede}</td></tr>"
            f"<tr><td style='padding:2px 8px'>fundada en</td>"
            f"<td style='padding:2px 8px'>{self.anio_fundacion}</td></tr>"
            "</table>"
        )

    def como_dict(self) -> dict:
        """Devuelve la universidad como diccionario plano."""
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


def _cargar() -> tuple[Universidad, ...]:
    path = files("argentina").joinpath("data/universidades.csv")
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return tuple(
        Universidad(
            sigla=r["sigla"],
            nombre=r["nombre"],
            provincia_codigo=r["provincia_codigo"].zfill(2),
            provincia_nombre=r["provincia_nombre"],
            sede=r["sede"],
            anio_fundacion=int(r["anio_fundacion"]),
            tipo=r["tipo"],
        )
        for r in rows
    )


UNIVERSIDADES = _cargar()

_POR_SIGLA = {_normalizar(u.sigla): u for u in UNIVERSIDADES}
_POR_NOMBRE = {_normalizar(u.nombre): u for u in UNIVERSIDADES}


def lookup(valor: str | None) -> Universidad | None:
    """Busca una universidad por sigla o nombre.

    Acepta:
    - sigla (``"UBA"``, ``"unc"``, ``"UNLP"``)
    - nombre completo (case-insensitive, sin tildes)
    - nombre parcial común (``"Universidad de Buenos Aires"``)
    """
    if valor is None:
        return None
    n = _normalizar(valor)
    if not n:
        return None
    if n in _POR_SIGLA:
        return _POR_SIGLA[n]
    if n in _POR_NOMBRE:
        return _POR_NOMBRE[n]
    # Match parcial: "buenos aires" → UBA
    for nombre_norm, u in _POR_NOMBRE.items():
        if n in nombre_norm:
            return u
    return None


def listar() -> tuple[Universidad, ...]:
    """Devuelve todas las universidades nacionales del set."""
    return UNIVERSIDADES


def por_provincia(provincia: str | None) -> tuple[Universidad, ...]:
    """Universidades de una provincia.

    Acepta cualquier identificador que entienda ``arg.provincias.lookup``.
    """
    if provincia is None:
        return ()
    from argentina.provincias import lookup as _lookup_prov
    p = _lookup_prov(provincia)
    if p is None:
        return ()
    return tuple(u for u in UNIVERSIDADES if u.provincia_codigo == p.codigo_indec)


def como_tabla() -> list[dict]:
    """Devuelve las universidades como lista de dicts."""
    return [u.como_dict() for u in UNIVERSIDADES]


def por_anio(desde: int | None = None, hasta: int | None = None) -> tuple[Universidad, ...]:
    """Filtra por año de fundación (rango inclusivo)."""
    def en_rango(u: Universidad) -> bool:
        if desde is not None and u.anio_fundacion < desde:
            return False
        if hasta is not None and u.anio_fundacion > hasta:
            return False
        return True
    return tuple(u for u in UNIVERSIDADES if en_rango(u))


# Módulo iterable
import types as _types


class _UniversidadesModulo(_types.ModuleType):
    def __iter__(self):
        return iter(UNIVERSIDADES)

    def __len__(self):
        return len(UNIVERSIDADES)

    def __contains__(self, item):
        if isinstance(item, Universidad):
            return item in UNIVERSIDADES
        return lookup(item) is not None


sys.modules[__name__].__class__ = _UniversidadesModulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.universidades.mapping("sigla", "nombre")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(UNIVERSIDADES, de, a)


__all__ = [
    "Universidad",
    "UNIVERSIDADES",
    "lookup",
    "listar",
    "por_provincia",
    "por_anio",
    "como_tabla",
    "mapping",
]
