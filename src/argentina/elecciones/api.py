"""Wrappers opcionales para APIs electorales argentinas.

Los imports de `requests` y `pandas` son **diferidos** dentro de cada función
para que importar `argentina.elecciones` no requiera tener instalado el extra
`[elecciones]`. Si llamás a una función que necesita una dep no instalada, se
levanta un `ImportError` con el comando de instalación.
"""

from __future__ import annotations

from importlib import util as _importlib_util


_INSTALL_HINT = 'pip install "argentina[elecciones]"'


def _tiene(modulo: str) -> bool:
    return _importlib_util.find_spec(modulo) is not None


def _require_requests():
    if not _tiene("requests"):
        raise ImportError(
            f"requests no está instalado. Instalá el extra: {_INSTALL_HINT}"
        )
    import requests
    return requests


def _require_pandas():
    if not _tiene("pandas"):
        raise ImportError(
            f"pandas no está instalado. Instalá el extra: {_INSTALL_HINT}"
        )
    import pandas
    return pandas


def disponible() -> dict:
    """Reporta qué dependencias del extra [elecciones] están instaladas."""
    return {
        "requests": _tiene("requests"),
        "pandas": _tiene("pandas"),
    }


def obtener_json(
    url: str,
    params: dict | None = None,
    timeout: int = 30,
):
    """GET genérico que devuelve JSON. Requiere `requests`.

    Pensado como bloque de construcción para wrappers concretos sobre
    endpoints electorales (resultados.gob.ar, escrutinios provinciales, etc.).
    """
    requests = _require_requests()
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


__all__ = [
    "disponible",
    "obtener_json",
]
