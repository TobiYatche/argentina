from __future__ import annotations

BASE_URL = "https://apis.datos.gob.ar/georef/api"


def _require_requests() -> None:
    """Verifica que requests esté instalado."""
    try:
        import requests  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            'Para usar argentina.geo.direcciones instalá: '
            'pip install "argentina[georef]"'
        ) from exc


def _get_json(
    endpoint: str,
    params: dict | None = None,
    timeout: int = 30,
) -> dict:
    """Consulta Georef y devuelve JSON."""
    _require_requests()

    import requests

    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    response = requests.get(
        url,
        params=params,
        timeout=timeout,
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        return {}

    return data


def georreferenciar(
    direccion: str,
    provincia: str | None = None,
    departamento: str | None = None,
    localidad: str | None = None,
    max_resultados: int = 1,
    timeout: int = 30,
) -> dict | None:
    """
    Georreferencia una dirección usando Georef.

    Devuelve el primer resultado o None.
    """
    params = {
        "direccion": direccion,
        "max": max_resultados,
    }

    if provincia is not None:
        params["provincia"] = provincia

    if departamento is not None:
        params["departamento"] = departamento

    if localidad is not None:
        params["localidad"] = localidad

    data = _get_json(
        endpoint="direcciones",
        params=params,
        timeout=timeout,
    )

    resultados = data.get("direcciones", [])

    if not resultados:
        return None

    return resultados[0]


def normalizar_georef(
    direccion: str,
    provincia: str | None = None,
    departamento: str | None = None,
    localidad: str | None = None,
    max_resultados: int = 1,
    timeout: int = 30,
) -> dict | None:
    """
    Normaliza una dirección usando Georef.
    Alias semántico de georreferenciar.
    """
    return georreferenciar(
        direccion=direccion,
        provincia=provincia,
        departamento=departamento,
        localidad=localidad,
        max_resultados=max_resultados,
        timeout=timeout,
    )


def coordenadas(
    direccion: str,
    provincia: str | None = None,
    departamento: str | None = None,
    localidad: str | None = None,
    timeout: int = 30,
) -> tuple[float, float] | None:
    """
    Devuelve coordenadas (lat, lon) de una dirección.
    """
    resultado = georreferenciar(
        direccion=direccion,
        provincia=provincia,
        departamento=departamento,
        localidad=localidad,
        max_resultados=1,
        timeout=timeout,
    )

    if resultado is None:
        return None

    ubicacion = resultado.get("ubicacion")

    if not isinstance(ubicacion, dict):
        return None

    lat = ubicacion.get("lat")
    lon = ubicacion.get("lon")

    if lat is None or lon is None:
        return None

    return float(lat), float(lon)


__all__ = [
    "BASE_URL",
    "georreferenciar",
    "normalizar_georef",
    "coordenadas",
]
