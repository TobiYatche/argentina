from __future__ import annotations

from datetime import date
from functools import lru_cache

API_URL = "https://api.argentinadatos.com/v1/feriados/{anio}"


def _require_requests() -> None:
    """Verifica que requests esté instalado."""
    try:
        import requests  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            'Para usar argentina.feriados instalá: pip install "argentina[feriados]"'
        ) from exc


def _parse_fecha(valor: str | date | None) -> date | None:
    """Parsea fecha ISO."""
    if valor is None:
        return None

    if isinstance(valor, date):
        return valor

    try:
        return date.fromisoformat(str(valor)[:10])
    except ValueError:
        return None


@lru_cache(maxsize=32)
def obtener(anio: int | str) -> list[dict]:
    """Obtiene feriados argentinos de un año."""
    _require_requests()

    import requests

    anio_int = int(anio)

    response = requests.get(
        API_URL.format(anio=anio_int),
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        return []

    return data


def es_feriado(
    fecha: str | date,
) -> bool:
    """Indica si una fecha es feriado nacional."""
    fecha_parseada = _parse_fecha(fecha)

    if fecha_parseada is None:
        return False

    feriados = obtener(fecha_parseada.year)

    fechas = {
        item.get("fecha")
        for item in feriados
    }

    return fecha_parseada.isoformat() in fechas


def detalle(
    fecha: str | date,
) -> dict | None:
    """Devuelve detalle del feriado si existe."""
    fecha_parseada = _parse_fecha(fecha)

    if fecha_parseada is None:
        return None

    for item in obtener(fecha_parseada.year):
        if item.get("fecha") == fecha_parseada.isoformat():
            return item

    return None


def proximo(
    desde: str | date | None = None,
) -> dict | None:
    """Devuelve el próximo feriado desde una fecha."""
    if desde is None:
        desde_fecha = date.today()
    else:
        desde_fecha = _parse_fecha(desde)

    if desde_fecha is None:
        return None

    candidatos = []

    for anio in [desde_fecha.year, desde_fecha.year + 1]:
        for item in obtener(anio):
            fecha_item = _parse_fecha(item.get("fecha"))

            if fecha_item is not None and fecha_item >= desde_fecha:
                candidatos.append(
                    (fecha_item, item)
                )

    if not candidatos:
        return None

    candidatos.sort(
        key=lambda x: x[0]
    )

    return candidatos[0][1]


__all__ = [
    "API_URL",
    "obtener",
    "es_feriado",
    "detalle",
    "proximo",
]
