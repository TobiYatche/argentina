"""Aglomerados urbanos de la Encuesta Permanente de Hogares (INDEC).

La EPH muestrea los aglomerados urbanos del país (32 códigos en el catálogo
vigente — incluye CABA y Partidos del GBA por separado, que algunas
publicaciones suman como "Gran Buenos Aires"). Cada microdato trae la
columna ``AGLOMERADO`` con el código numérico — este módulo lo decodifica.

Útil para enriquecer un DataFrame de EPH con el nombre y la provincia del
aglomerado, o para filtrar por aglomerados de una región.
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
class Aglomerado:
    codigo: int
    nombre: str
    provincia_codigo: str
    provincia_nombre: str

    def como_dict(self) -> dict:
        """Devuelve el aglomerado como diccionario plano."""
        return asdict(self)

    def _repr_html_(self) -> str:
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>código EPH</td>"
            f"<td style='padding:2px 8px'><code>{self.codigo}</code></td></tr>"
            f"<tr><td style='padding:2px 8px'>provincia</td>"
            f"<td style='padding:2px 8px'>{self.provincia_nombre} "
            f"(<code>{self.provincia_codigo}</code>)</td></tr>"
            "</table>"
        )


@lru_cache(maxsize=256)
def _normalizar(texto: str | None) -> str:
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _cargar() -> tuple[Aglomerado, ...]:
    path = files("argentina").joinpath("data/aglomerados.csv")
    with path.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return tuple(
        Aglomerado(
            codigo=int(r["codigo"]),
            nombre=r["nombre"],
            provincia_codigo=r["provincia_codigo"].zfill(2),
            provincia_nombre=r["provincia_nombre"],
        )
        for r in rows
    )


AGLOMERADOS = _cargar()

_POR_CODIGO = {a.codigo: a for a in AGLOMERADOS}
_POR_NOMBRE = {_normalizar(a.nombre): a for a in AGLOMERADOS}


def lookup(valor) -> Aglomerado | None:
    """Busca un aglomerado por código numérico o nombre."""
    if valor is None:
        return None
    # Numérico
    try:
        return _POR_CODIGO.get(int(valor))
    except (TypeError, ValueError):
        pass
    # Por nombre normalizado
    n = _normalizar(valor)
    if not n:
        return None
    if n in _POR_NOMBRE:
        return _POR_NOMBRE[n]
    # Match parcial (ej. "córdoba" → "Gran Córdoba")
    for nombre_norm, agl in _POR_NOMBRE.items():
        if n in nombre_norm:
            return agl
    return None


def listar() -> tuple[Aglomerado, ...]:
    """Devuelve los 31 aglomerados de la EPH."""
    return AGLOMERADOS


def como_tabla() -> list[dict]:
    """Devuelve los aglomerados como lista de dicts."""
    return [a.como_dict() for a in AGLOMERADOS]


def por_provincia(provincia) -> tuple[Aglomerado, ...]:
    """Aglomerados de una provincia.

    Acepta cualquier identificador que entienda ``arg.provincias.lookup``.
    """
    if provincia is None:
        return ()
    from argentina.provincias import lookup as _lookup_prov
    p = _lookup_prov(provincia)
    if p is None:
        return ()
    return tuple(a for a in AGLOMERADOS if a.provincia_codigo == p.codigo_indec)


# Módulo iterable
import types as _types


class _AglomeradosModulo(_types.ModuleType):
    def __iter__(self):
        return iter(AGLOMERADOS)

    def __len__(self):
        return len(AGLOMERADOS)

    def __contains__(self, item):
        if isinstance(item, Aglomerado):
            return item in AGLOMERADOS
        return lookup(item) is not None


sys.modules[__name__].__class__ = _AglomeradosModulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.aglomerados.mapping("codigo", "nombre")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(AGLOMERADOS, de, a)


__all__ = [
    "Aglomerado",
    "AGLOMERADOS",
    "lookup",
    "listar",
    "por_provincia",
    "como_tabla",
    "mapping",
]
