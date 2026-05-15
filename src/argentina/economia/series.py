"""Descarga de series económicas oficiales desde datos.gob.ar."""

from __future__ import annotations

from typing import TYPE_CHECKING

from argentina.economia.catalogo import SERIES

if TYPE_CHECKING:
    import pandas as pd

BASE_URL = "https://apis.datos.gob.ar/series/api/series"


def _require_economia_dependencies() -> None:
    """Verifica dependencias opcionales de economia."""
    try:
        import pandas  # noqa: F401
        import requests  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            'Para usar argentina.economia instalá: pip install "argentina[economia]"'
        ) from exc


def obtener_serie(
    serie_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 5000,
) -> "pd.DataFrame":
    """Descarga una serie de tiempo desde la API de datos.gob.ar.

    Devuelve un DataFrame con columnas ``fecha`` (datetime) y ``valor``.
    Si la API no devuelve datos, retorna un DataFrame vacío con esas columnas.
    """
    _require_economia_dependencies()

    import pandas as pd
    import requests

    params: dict[str, str | int] = {
        "ids": serie_id,
        "limit": limit,
        "format": "json",
    }
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    data = payload.get("data", [])
    if not data:
        return pd.DataFrame({"fecha": pd.Series(dtype="datetime64[ns]"), "valor": pd.Series(dtype="float64")})

    df = pd.DataFrame(data, columns=["fecha", "valor"])
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha").reset_index(drop=True)
    return df


def serie(
    nombre_o_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
    limit: int = 5000,
) -> "pd.DataFrame":
    """Descarga una serie usando un alias del catálogo o un ID directo."""
    if nombre_o_id in SERIES:
        serie_id = SERIES[nombre_o_id]["id"]
    else:
        serie_id = nombre_o_id
    return obtener_serie(serie_id, start_date=start_date, end_date=end_date, limit=limit)


def ipc_nacional(start_date: str | None = None, end_date: str | None = None) -> "pd.DataFrame":
    """Índice de precios al consumidor nacional (INDEC)."""
    return serie("ipc_nacional", start_date, end_date)


def ipc_nucleo(start_date: str | None = None, end_date: str | None = None) -> "pd.DataFrame":
    """IPC Núcleo Nacional. Base dic 2016 (INDEC)."""
    return serie("ipc_nucleo_nacional", start_date, end_date)


def emae(start_date: str | None = None, end_date: str | None = None) -> "pd.DataFrame":
    """Estimador mensual de actividad económica (INDEC)."""
    return serie("emae", start_date, end_date)


def tipo_cambio_minorista(start_date: str | None = None, end_date: str | None = None) -> "pd.DataFrame":
    """Tipo de cambio minorista vendedor (BCRA)."""
    return serie("tipo_cambio_minorista", start_date, end_date)
