"""Departamentos argentinos: set completo con lookup flexible.

Incluye los 529 departamentos/partidos/comunas del país según los códigos
INDEC oficiales servidos por el IGN. ``codigo_departamento`` son los 5 dígitos
estándar (2 provincia + 3 departamento). ``lookup`` acepta código, nombre
único o alias coloquial. Sin dependencias externas, datos embebidos.
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass
from functools import lru_cache
from importlib.resources import files


@dataclass(frozen=True)
class Departamento:
    codigo_departamento: str
    nombre: str
    provincia_codigo: str
    provincia_nombre: str

    def _repr_html_(self) -> str:
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>código depto</td>"
            f"<td style='padding:2px 8px'><code>{self.codigo_departamento}</code></td></tr>"
            f"<tr><td style='padding:2px 8px'>provincia</td>"
            f"<td style='padding:2px 8px'>{self.provincia_nombre} "
            f"(<code>{self.provincia_codigo}</code>)</td></tr>"
            "</table>"
        )

    def como_dict(self) -> dict:
        """Devuelve el departamento como diccionario plano."""
        return asdict(self)


@lru_cache(maxsize=2048)
def _normalizar(texto: str | None) -> str:
    """Normaliza texto para búsquedas flexibles."""
    if texto is None:
        return ""

    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _cargar_departamentos() -> tuple[Departamento, ...]:
    path = files("argentina").joinpath("data/departamentos.csv")
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        departamentos = []
        for row in reader:
            departamentos.append(
                Departamento(
                    codigo_departamento=row["codigo_departamento"],
                    nombre=row["nombre"],
                    provincia_codigo=row["provincia_codigo"],
                    provincia_nombre=row["provincia_nombre"],
                )
            )
    return tuple(departamentos)


DEPARTAMENTOS = _cargar_departamentos()


_POR_CODIGO = {d.codigo_departamento: d for d in DEPARTAMENTOS}


_ALIASES = {
    # Códigos oficiales INDEC vía IGN (5 dígitos: provincia + departamento).
    "la matanza": _POR_CODIGO["06427"],
    "la plata": _POR_CODIGO["06441"],
    "rosario": _POR_CODIGO["82084"],
    "general pueyrredon": _POR_CODIGO["06357"],
    "mar del plata": _POR_CODIGO["06357"],  # nombre coloquial de Gral Pueyrredón
    "rio cuarto": _POR_CODIGO["14098"],
}


_LOOKUP: dict[str, Departamento] = {}

_contador_nombres = Counter(_normalizar(d.nombre) for d in DEPARTAMENTOS)

for _d in DEPARTAMENTOS:
    _LOOKUP[_normalizar(_d.codigo_departamento)] = _d
    _nombre_norm = _normalizar(_d.nombre)
    if _contador_nombres[_nombre_norm] == 1:
        _LOOKUP[_nombre_norm] = _d

for _alias, _d in _ALIASES.items():
    _LOOKUP[_normalizar(_alias)] = _d


def lookup(valor: str | None) -> Departamento | None:
    """Busca un departamento por código o nombre único.

    Nombres duplicados entre provincias (como "Capital") no resuelven a un
    único departamento y devuelven ``None``. Para esos casos hay que usar
    el código de departamento o un alias específico.
    """
    return _LOOKUP.get(_normalizar(valor))


def listar() -> tuple[Departamento, ...]:
    """Devuelve todos los departamentos disponibles."""
    return DEPARTAMENTOS


def como_tabla() -> list[dict]:
    """Devuelve los 529 departamentos como lista de dicts."""
    return [d.como_dict() for d in DEPARTAMENTOS]


def por_provincia(provincia: str | None) -> tuple[Departamento, ...]:
    """Devuelve los departamentos de una provincia.

    Acepta cualquier identificador que entienda ``argentina.provincias.lookup``:
    nombre (con o sin tildes), código INDEC, ISO 3166-2 o alias comunes
    (``"PBA"``, ``"CABA"``, ``"TDF"``, etc.).

    Si no se encuentra la provincia, devuelve una tupla vacía.
    """
    if provincia is None:
        return ()

    # Resolver alias usando el catálogo de provincias.
    from argentina.provincias import lookup as _lookup_prov
    p = _lookup_prov(provincia)
    if p is not None:
        codigo = p.codigo_indec
        return tuple(d for d in DEPARTAMENTOS if d.provincia_codigo == codigo)

    # Fallback: matchear directo contra código o nombre (caso código INDEC
    # de una provincia que no esté en el catálogo).
    aguja = _normalizar(provincia)
    if not aguja:
        return ()
    return tuple(
        d for d in DEPARTAMENTOS
        if _normalizar(d.provincia_codigo) == aguja
        or _normalizar(d.provincia_nombre) == aguja
    )


# Hacer el módulo iterable: `for d in argentina.departamentos: ...`
import types as _types


class _DepartamentosModulo(_types.ModuleType):
    def __iter__(self):
        return iter(DEPARTAMENTOS)

    def __len__(self):
        return len(DEPARTAMENTOS)

    def __contains__(self, item):
        if isinstance(item, Departamento):
            return item in DEPARTAMENTOS
        return lookup(item) is not None


sys.modules[__name__].__class__ = _DepartamentosModulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.departamentos.mapping("codigo_departamento", "nombre")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(DEPARTAMENTOS, de, a)


__all__ = [
    "Departamento",
    "DEPARTAMENTOS",
    "lookup",
    "listar",
    "por_provincia",
    "como_tabla",
    "mapping",
]
