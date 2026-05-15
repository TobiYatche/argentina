"""Clasificador de Actividades Económicas (CLAE).

Códigos de 6 dígitos jerárquicos que AFIP usa para identificar la actividad
económica de cada contribuyente. Incluye:

- ``codigo`` (6 dígitos) — clave única.
- ``descripcion`` — texto oficial.
- ``sector`` — letra A-T.
- ``sector_nombre`` — nombre del sector.
- ``grupo`` — 4 dígitos (jerarquía intermedia).

> **Subset CLAE-2018:** la base embebida es un subconjunto representativo
> (~120 códigos) del catálogo CLAE-2018 (el catálogo completo de AFIP
> tiene ~1000 códigos). Las descripciones y la estructura jerárquica
> reflejan la nomenclatura pública pero pueden tener variaciones menores
> respecto al texto oficial. Para uso fiscal o de cumplimiento,
> **verificar siempre contra el Formulario 883 de AFIP** antes de
> reportar un código.

Sin internet, sin dependencias externas.
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
class Actividad:
    codigo: str
    descripcion: str
    sector: str
    sector_nombre: str
    grupo: str

    def como_dict(self) -> dict:
        return asdict(self)

    def _repr_html_(self) -> str:
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>CLAE {self.codigo}</th></tr>"
            f"<tr><td style='padding:2px 8px'>descripción</td>"
            f"<td style='padding:2px 8px'>{self.descripcion}</td></tr>"
            f"<tr><td style='padding:2px 8px'>sector</td>"
            f"<td style='padding:2px 8px'><code>{self.sector}</code> — "
            f"{self.sector_nombre}</td></tr>"
            f"<tr><td style='padding:2px 8px'>grupo</td>"
            f"<td style='padding:2px 8px'><code>{self.grupo}</code></td></tr>"
            "</table>"
        )


@dataclass(frozen=True)
class Sector:
    letra: str
    nombre: str


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


def _normalizar_codigo(valor: str | int | None) -> str | None:
    if valor is None:
        return None
    s = re.sub(r"\D+", "", str(valor))
    if not s:
        return None
    if len(s) > 6:
        return None
    return s.zfill(6)


def _cargar() -> tuple[Actividad, ...]:
    path = files("argentina").joinpath("data/clae.csv")
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return tuple(
        Actividad(
            codigo=r["codigo"],
            descripcion=r["descripcion"],
            sector=r["sector"],
            sector_nombre=r["sector_nombre"],
            grupo=r["grupo"],
        )
        for r in rows
    )


ACTIVIDADES = _cargar()
_POR_CODIGO = {a.codigo: a for a in ACTIVIDADES}


def lookup(valor: str | int | None) -> Actividad | None:
    """Busca una actividad por código de 6 dígitos.

    Acepta ``str`` o ``int``. Códigos cortos (5 dígitos por omitir el cero
    inicial) se padean a 6.
    """
    codigo = _normalizar_codigo(valor)
    if codigo is None:
        return None
    return _POR_CODIGO.get(codigo)


def es_valido(valor: str | int | None) -> bool:
    """``True`` si el código está en el catálogo embebido."""
    return lookup(valor) is not None


def listar() -> tuple[Actividad, ...]:
    """Devuelve todas las actividades del catálogo."""
    return ACTIVIDADES


def por_sector(letra: str | None) -> tuple[Actividad, ...]:
    """Devuelve actividades de un sector (letra A-T)."""
    if letra is None:
        return ()
    n = str(letra).strip().upper()
    if not n:
        return ()
    return tuple(a for a in ACTIVIDADES if a.sector == n)


def por_grupo(grupo: str | int | None) -> tuple[Actividad, ...]:
    """Devuelve actividades de un grupo (4 dígitos)."""
    if grupo is None:
        return ()
    g = re.sub(r"\D+", "", str(grupo))
    if not g:
        return ()
    g = g.zfill(4)
    return tuple(a for a in ACTIVIDADES if a.grupo == g)


def buscar(texto: str | None) -> tuple[Actividad, ...]:
    """Busca por substring en la descripción (normalizado sin tildes)."""
    n = _normalizar(texto)
    if not n:
        return ()
    return tuple(a for a in ACTIVIDADES if n in _normalizar(a.descripcion))


def sectores() -> tuple[Sector, ...]:
    """Devuelve los sectores presentes en el catálogo, ordenados por letra."""
    vistos: dict[str, str] = {}
    for a in ACTIVIDADES:
        vistos.setdefault(a.sector, a.sector_nombre)
    return tuple(
        Sector(letra=letra, nombre=vistos[letra]) for letra in sorted(vistos)
    )


def como_tabla() -> list[dict]:
    """Devuelve las actividades como lista de dicts."""
    return [a.como_dict() for a in ACTIVIDADES]


import types as _types


class _ClaeModulo(_types.ModuleType):
    def __iter__(self):
        return iter(ACTIVIDADES)

    def __len__(self):
        return len(ACTIVIDADES)

    def __contains__(self, item):
        if isinstance(item, Actividad):
            return item in ACTIVIDADES
        return lookup(item) is not None


sys.modules[__name__].__class__ = _ClaeModulo


__all__ = [
    "Actividad",
    "Sector",
    "ACTIVIDADES",
    "lookup",
    "es_valido",
    "listar",
    "por_sector",
    "por_grupo",
    "buscar",
    "sectores",
    "como_tabla",
]
