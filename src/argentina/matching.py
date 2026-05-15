"""Matching difuso (fuzzy) sobre los catálogos del paquete.

Complemento de ``lookup()``: cuando la búsqueda exacta falla, ``matching``
intenta encontrar el ítem más parecido por similitud de strings.

Resuelve casos típicos donde llegan datos sucios:

- typos: ``"buennos aires"`` → :class:`~argentina.provincias.Provincia` Buenos Aires
- abreviaturas no aliasadas: ``"sgo del estero"`` → Santiago del Estero
- variantes: ``"cordova"`` → Córdoba

Stdlib pura (``difflib.SequenceMatcher``). Sin dependencias externas.
Sin internet, sin archivos externos: reusa los catálogos embebidos del
paquete.

Cada función específica (``match_provincia``, ``match_departamento``, …):

1. Intenta primero el ``lookup()`` exacto del módulo correspondiente. Si
   matchea, devuelve el objeto con score implícito ``1.0``.
2. Si no, calcula similitud contra los nombres normalizados (mismo
   ``_normalizar`` que usan los módulos: lowercase + NFKD sin tildes +
   alfanumérico).
3. Si el mejor score llega al ``umbral``, devuelve el ítem; si no, ``None``.

El umbral default es ``0.7``. Es ajustable y no se promete óptimo: subirlo
para ser estrictos, bajarlo para tolerar más ruido.

Para inspeccionar los candidatos con score, usar ``candidatos_*`` (top-N).

Para matchear contra una lista arbitraria de strings, usar la función
genérica :func:`match`.
"""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from functools import lru_cache
from typing import Iterable, Sequence


UMBRAL_DEFAULT = 0.7


@lru_cache(maxsize=2048)
def _normalizar(texto: str | None) -> str:
    """Normalización canónica: lowercase + NFKD sin tildes + alfanumérico.

    Misma normalización que usan los módulos ``provincias``, ``departamentos``,
    ``ciudades``, etc. Reusarla mantiene los matches consistentes con
    ``lookup()``.
    """
    if texto is None:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _score(a: str, b: str) -> float:
    """Score de similitud entre dos strings ya normalizados, en [0.0, 1.0]."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


# ---------------------------------------------------------------------------
# API genérica
# ---------------------------------------------------------------------------


def match(
    consulta: str | None,
    candidatos: Iterable[str],
    *,
    umbral: float = UMBRAL_DEFAULT,
) -> tuple[str, float] | None:
    """Encuentra el candidato más parecido a ``consulta``.

    Compara con normalización canónica (lowercase + sin tildes +
    alfanumérico) pero devuelve el candidato **original**, no el normalizado.

    Parameters
    ----------
    consulta : str | None
        Texto a matchear.
    candidatos : Iterable[str]
        Lista/tupla/generador de strings entre los que elegir.
    umbral : float
        Score mínimo en [0, 1] para considerar match válido. Default ``0.7``.

    Returns
    -------
    tuple[str, float] | None
        ``(candidato_original, score)`` o ``None`` si ningún candidato
        llega al umbral.

    Examples
    --------
    >>> import argentina as arg
    >>> arg.matching.match("cordova", ["Buenos Aires", "Córdoba", "Santa Fe"])
    ('Córdoba', 1.0)
    >>> arg.matching.match("xyz", ["Buenos Aires", "Córdoba"])
    """
    aguja = _normalizar(consulta)
    if not aguja:
        return None

    mejor: tuple[str, float] | None = None
    for c in candidatos:
        s = _score(aguja, _normalizar(c))
        if mejor is None or s > mejor[1]:
            mejor = (c, s)

    if mejor is None or mejor[1] < umbral:
        return None
    return mejor


def candidatos(
    consulta: str | None,
    opciones: Iterable[str],
    *,
    n: int = 3,
    umbral: float = 0.0,
) -> list[tuple[str, float]]:
    """Top-``n`` candidatos ordenados por score descendente.

    No filtra por umbral por default (``umbral=0.0``) para que sea fácil
    inspeccionar resultados; subirlo si solo interesan los buenos.
    """
    aguja = _normalizar(consulta)
    if not aguja:
        return []

    puntuados = [(c, _score(aguja, _normalizar(c))) for c in opciones]
    puntuados = [p for p in puntuados if p[1] >= umbral]
    puntuados.sort(key=lambda p: p[1], reverse=True)
    return puntuados[:n]


# ---------------------------------------------------------------------------
# Helpers de catálogo
# ---------------------------------------------------------------------------


def _mejor_por_score(
    consulta: str,
    items: Sequence,
    *,
    clave,
    umbral: float,
):
    """Devuelve ``(item, score)`` con mejor score sobre ``items`` o ``None``.

    ``clave(item)`` devuelve el string a comparar contra ``consulta``
    (ya normalizada).
    """
    aguja = _normalizar(consulta)
    if not aguja or not items:
        return None

    mejor_item = None
    mejor_score = 0.0
    for item in items:
        s = _score(aguja, _normalizar(clave(item)))
        if s > mejor_score:
            mejor_score = s
            mejor_item = item

    if mejor_item is None or mejor_score < umbral:
        return None
    return mejor_item, mejor_score


def _topn_por_score(
    consulta: str,
    items: Sequence,
    *,
    clave,
    n: int,
    umbral: float,
) -> list[tuple[object, float]]:
    aguja = _normalizar(consulta)
    if not aguja or not items:
        return []
    puntuados = [(it, _score(aguja, _normalizar(clave(it)))) for it in items]
    puntuados = [p for p in puntuados if p[1] >= umbral]
    puntuados.sort(key=lambda p: p[1], reverse=True)
    return puntuados[:n]


# ---------------------------------------------------------------------------
# Provincias
# ---------------------------------------------------------------------------


def match_provincia(valor: str | None, *, umbral: float = UMBRAL_DEFAULT):
    """Matchea ``valor`` contra el catálogo de provincias.

    Intenta primero ``argentina.provincias.lookup(valor)`` (exacto, alias,
    código INDEC, ISO). Si falla, intenta similitud contra los nombres
    oficiales.

    Returns
    -------
    Provincia | None
    """
    if valor is None:
        return None
    from argentina import provincias

    exacto = provincias.lookup(valor)
    if exacto is not None:
        return exacto
    res = _mejor_por_score(
        valor, provincias.PROVINCIAS, clave=lambda p: p.nombre, umbral=umbral
    )
    return res[0] if res else None


def candidatos_provincia(
    valor: str | None,
    *,
    n: int = 3,
    umbral: float = 0.0,
) -> list[tuple[object, float]]:
    """Top-``n`` provincias por score, ordenadas desc."""
    from argentina import provincias

    return _topn_por_score(
        valor, provincias.PROVINCIAS, clave=lambda p: p.nombre, n=n, umbral=umbral
    )


# ---------------------------------------------------------------------------
# Departamentos
# ---------------------------------------------------------------------------


def match_departamento(
    valor: str | None,
    *,
    provincia: str | None = None,
    umbral: float = UMBRAL_DEFAULT,
):
    """Matchea ``valor`` contra el catálogo de departamentos.

    Si se pasa ``provincia`` (cualquier identificador que entienda
    ``argentina.provincias.lookup``), el universo de búsqueda se restringe
    a los departamentos de esa provincia, lo que reduce muchísimo el
    riesgo de ambigüedad (nombres como "Capital" se repiten en varias
    provincias).

    Returns
    -------
    Departamento | None
    """
    if valor is None:
        return None
    from argentina import departamentos

    if provincia is None:
        universo = departamentos.DEPARTAMENTOS
    else:
        universo = departamentos.por_provincia(provincia)
        if not universo:
            return None

    # Solo intentar lookup() exacto cuando no hay filtro de provincia,
    # ya que lookup() del módulo no filtra por provincia.
    if provincia is None:
        exacto = departamentos.lookup(valor)
        if exacto is not None:
            return exacto

    res = _mejor_por_score(
        valor, universo, clave=lambda d: d.nombre, umbral=umbral
    )
    return res[0] if res else None


def candidatos_departamento(
    valor: str | None,
    *,
    provincia: str | None = None,
    n: int = 3,
    umbral: float = 0.0,
) -> list[tuple[object, float]]:
    """Top-``n`` departamentos por score, ordenados desc.

    Acepta ``provincia`` para acotar el universo (recomendado).
    """
    from argentina import departamentos

    if provincia is None:
        universo = departamentos.DEPARTAMENTOS
    else:
        universo = departamentos.por_provincia(provincia)
    return _topn_por_score(
        valor, universo, clave=lambda d: d.nombre, n=n, umbral=umbral
    )


# ---------------------------------------------------------------------------
# Ciudades
# ---------------------------------------------------------------------------


def match_ciudad(valor: str | None, *, umbral: float = UMBRAL_DEFAULT):
    """Matchea ``valor`` contra el catálogo de ciudades.

    Returns
    -------
    Ciudad | None
    """
    if valor is None:
        return None
    from argentina import ciudades

    exacto = ciudades.lookup(valor)
    if exacto is not None:
        return exacto
    res = _mejor_por_score(
        valor, ciudades.CIUDADES, clave=lambda c: c.nombre, umbral=umbral
    )
    return res[0] if res else None


def candidatos_ciudad(
    valor: str | None,
    *,
    n: int = 3,
    umbral: float = 0.0,
) -> list[tuple[object, float]]:
    """Top-``n`` ciudades por score, ordenadas desc."""
    from argentina import ciudades

    return _topn_por_score(
        valor, ciudades.CIUDADES, clave=lambda c: c.nombre, n=n, umbral=umbral
    )


# ---------------------------------------------------------------------------
# Universidades
# ---------------------------------------------------------------------------


def match_universidad(valor: str | None, *, umbral: float = UMBRAL_DEFAULT):
    """Matchea ``valor`` contra el catálogo de universidades nacionales.

    El ``lookup()`` exacto ya cubre sigla y nombre; aquí se agrega
    tolerancia a typos.

    Returns
    -------
    Universidad | None
    """
    if valor is None:
        return None
    from argentina import universidades

    exacto = universidades.lookup(valor)
    if exacto is not None:
        return exacto

    aguja = _normalizar(valor)
    if not aguja:
        return None
    # Comparar contra sigla y nombre; quedarnos con el mejor.
    mejor_item = None
    mejor_score = 0.0
    for u in universidades.UNIVERSIDADES:
        s_sigla = _score(aguja, _normalizar(u.sigla))
        s_nombre = _score(aguja, _normalizar(u.nombre))
        s = max(s_sigla, s_nombre)
        if s > mejor_score:
            mejor_score = s
            mejor_item = u
    if mejor_item is None or mejor_score < umbral:
        return None
    return mejor_item


def candidatos_universidad(
    valor: str | None,
    *,
    n: int = 3,
    umbral: float = 0.0,
) -> list[tuple[object, float]]:
    """Top-``n`` universidades por score (mejor de sigla y nombre)."""
    from argentina import universidades

    aguja = _normalizar(valor)
    if not aguja:
        return []
    puntuados = []
    for u in universidades.UNIVERSIDADES:
        s = max(
            _score(aguja, _normalizar(u.sigla)),
            _score(aguja, _normalizar(u.nombre)),
        )
        if s >= umbral:
            puntuados.append((u, s))
    puntuados.sort(key=lambda p: p[1], reverse=True)
    return puntuados[:n]


# ---------------------------------------------------------------------------
# Aglomerados
# ---------------------------------------------------------------------------


def match_aglomerado(valor: str | None, *, umbral: float = UMBRAL_DEFAULT):
    """Matchea ``valor`` contra el catálogo de aglomerados EPH.

    Returns
    -------
    Aglomerado | None
    """
    if valor is None:
        return None
    from argentina import aglomerados

    exacto = aglomerados.lookup(valor)
    if exacto is not None:
        return exacto
    res = _mejor_por_score(
        valor, aglomerados.AGLOMERADOS, clave=lambda a: a.nombre, umbral=umbral
    )
    return res[0] if res else None


def candidatos_aglomerado(
    valor: str | None,
    *,
    n: int = 3,
    umbral: float = 0.0,
) -> list[tuple[object, float]]:
    """Top-``n`` aglomerados por score, ordenados desc."""
    from argentina import aglomerados

    return _topn_por_score(
        valor, aglomerados.AGLOMERADOS, clave=lambda a: a.nombre, n=n, umbral=umbral
    )


__all__ = [
    "UMBRAL_DEFAULT",
    "match",
    "candidatos",
    "match_provincia",
    "candidatos_provincia",
    "match_departamento",
    "candidatos_departamento",
    "match_ciudad",
    "candidatos_ciudad",
    "match_universidad",
    "candidatos_universidad",
    "match_aglomerado",
    "candidatos_aglomerado",
]
