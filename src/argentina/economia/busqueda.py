"""Búsqueda local en el catálogo de series económicas."""

from __future__ import annotations

from typing import TYPE_CHECKING

from argentina.economia.catalogo import SERIES
from argentina.economia.series import _require_economia_dependencies

if TYPE_CHECKING:
    import pandas as pd

_COLUMNAS = ["alias", "id", "frecuencia", "tema", "descripcion"]


def buscar(palabra: str) -> "pd.DataFrame":
    """Busca aliases del catálogo cuya descripción, alias o dataset contengan ``palabra``.

    La búsqueda es case-insensitive y se hace sobre el catálogo local (sin red).
    Devuelve un DataFrame con columnas ``alias``, ``id``, ``frecuencia``, ``tema``
    y ``descripcion``. Si no hay coincidencias, devuelve un DataFrame vacío con
    esas mismas columnas.
    """
    _require_economia_dependencies()

    import pandas as pd

    aguja = palabra.lower()
    filas = []
    for alias, e in SERIES.items():
        haystack = f"{alias} {e['descripcion']} {e.get('dataset', '')}".lower()
        if aguja in haystack:
            filas.append({
                "alias": alias,
                "id": e["id"],
                "frecuencia": e.get("frecuencia", ""),
                "tema": e.get("tema", ""),
                "descripcion": e["descripcion"],
            })
    return pd.DataFrame(filas, columns=_COLUMNAS)
