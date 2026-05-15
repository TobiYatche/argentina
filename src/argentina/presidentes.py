"""Presidentes argentinos desde la Constitución de 1853.

Incluye presidentes constitucionales, interinos y de facto. Cada entrada
trae nombre, período (inicio, fin), partido y tipo de mandato.

Datos embebidos, sin dependencias externas.

Notas:
- Antes de 1854 (cargo de "Presidente" de la Confederación) hubo gobernantes
  como las Juntas, el Triunvirato y los Directores Supremos — no se incluyen.
- Los segundos mandatos aparecen como entradas separadas (Roca, Yrigoyen,
  Perón, Menem, CFK).
- "Tipo" puede ser: ``"constitucional"``, ``"interino"`` o ``"de facto"``.
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
from functools import lru_cache
from importlib.resources import files


@dataclass(frozen=True)
class Presidente:
    nombre: str
    inicio: date
    fin: date
    partido: str
    tipo: str  # constitucional / interino / de facto

    @property
    def dias(self) -> int:
        """Duración del mandato en días."""
        return (self.fin - self.inicio).days

    def vigente_en(self, fecha) -> bool:
        """``True`` si esta presidencia estaba vigente en la fecha dada."""
        f = _fecha(fecha)
        return self.inicio <= f < self.fin

    def como_dict(self) -> dict:
        d = asdict(self)
        d["inicio"] = self.inicio.isoformat()
        d["fin"] = self.fin.isoformat()
        return d

    def _repr_html_(self) -> str:
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>período</td>"
            f"<td style='padding:2px 8px'>{self.inicio} → {self.fin}</td></tr>"
            f"<tr><td style='padding:2px 8px'>partido</td>"
            f"<td style='padding:2px 8px'>{self.partido}</td></tr>"
            f"<tr><td style='padding:2px 8px'>tipo</td>"
            f"<td style='padding:2px 8px'>{self.tipo}</td></tr>"
            "</table>"
        )


def _fecha(valor) -> date:
    """Acepta `date`, `datetime` o ISO string."""
    if isinstance(valor, date) and not isinstance(valor, type(date(2000, 1, 1).today())):
        return valor
    if hasattr(valor, "date"):  # datetime
        return valor.date()
    if isinstance(valor, str):
        return date.fromisoformat(valor)
    if isinstance(valor, date):
        return valor
    raise TypeError(f"no se entiende como fecha: {valor!r}")


@lru_cache(maxsize=512)
def _normalizar(texto: str | None) -> str:
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def _cargar() -> tuple[Presidente, ...]:
    path = files("argentina").joinpath("data/presidentes.csv")
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return tuple(
        Presidente(
            nombre=r["nombre"],
            inicio=date.fromisoformat(r["inicio"]),
            fin=date.fromisoformat(r["fin"]),
            partido=r["partido"],
            tipo=r["tipo"],
        )
        for r in rows
    )


PRESIDENTES = _cargar()


def listar() -> tuple[Presidente, ...]:
    """Devuelve todos los presidentes en orden cronológico."""
    return PRESIDENTES


def en(fecha) -> Presidente | None:
    """Devuelve el presidente vigente en una fecha dada."""
    f = _fecha(fecha)
    for p in PRESIDENTES:
        if p.inicio <= f < p.fin:
            return p
    return None


def actual() -> Presidente | None:
    """Devuelve el presidente vigente hoy."""
    return en(date.today())


def por_partido(partido: str | None) -> tuple[Presidente, ...]:
    """Filtra por partido. Case-insensitive, sin tildes."""
    if partido is None:
        return ()
    n = _normalizar(partido)
    if not n:
        return ()
    return tuple(p for p in PRESIDENTES if _normalizar(p.partido) == n)


def por_tipo(tipo: str | None) -> tuple[Presidente, ...]:
    """Filtra por tipo (``"constitucional"`` / ``"interino"`` / ``"de facto"``)."""
    if tipo is None:
        return ()
    n = _normalizar(tipo)
    if not n:
        return ()
    return tuple(p for p in PRESIDENTES if _normalizar(p.tipo) == n)


def lookup(nombre: str | None) -> Presidente | None:
    """Busca un presidente por nombre (case-insensitive, sin tildes, match parcial).

    Si hay más de un mandato (Perón, CFK, Menem, etc.), devuelve el primero.
    """
    if nombre is None:
        return None
    n = _normalizar(nombre)
    if not n:
        return None
    for p in PRESIDENTES:
        if _normalizar(p.nombre) == n:
            return p
    for p in PRESIDENTES:
        if n in _normalizar(p.nombre):
            return p
    return None


def como_tabla() -> list[dict]:
    """Lista de dicts apta para ``pandas.DataFrame``."""
    return [p.como_dict() for p in PRESIDENTES]


# Módulo iterable
import types as _types


class _Modulo(_types.ModuleType):
    def __iter__(self):
        return iter(PRESIDENTES)

    def __len__(self):
        return len(PRESIDENTES)

    def __contains__(self, item):
        if isinstance(item, Presidente):
            return item in PRESIDENTES
        return lookup(item) is not None


sys.modules[__name__].__class__ = _Modulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.presidentes.mapping("nombre", "partido")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(PRESIDENTES, de, a)


__all__ = [
    "Presidente",
    "PRESIDENTES",
    "listar",
    "en",
    "actual",
    "por_partido",
    "por_tipo",
    "lookup",
    "como_tabla",
    "mapping",
]
