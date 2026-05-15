from __future__ import annotations

import re


CATEGORIAS = {
    "presidente": "Presidente",
    "presidenta": "Presidente",
    "diputado": "Diputados",
    "diputados": "Diputados",
    "senador": "Senadores",
    "senadores": "Senadores",
    "gobernador": "Gobernador",
    "intendente": "Intendente",
}

TIPOS_ELECCION = {
    "paso": "PASO",
    "primaria": "PASO",
    "primarias": "PASO",
    "general": "General",
    "generales": "General",
    "ballotage": "Ballotage",
    "segunda vuelta": "Ballotage",
}


def _normalizar_texto(valor: str | None) -> str | None:
    if valor is None:
        return None

    texto = str(valor).strip().lower()
    texto = re.sub(r"\s+", " ", texto)

    if texto == "":
        return None

    return texto


def limpiar_mesa(valor: str | int | None) -> str | None:
    if valor is None:
        return None

    texto = re.sub(r"\D+", "", str(valor))

    if texto == "":
        return None

    return texto


def limpiar_circuito(valor: str | int | None) -> str | None:
    if valor is None:
        return None

    texto = str(valor).strip().upper()
    texto = re.sub(r"[^A-Z0-9]+", "", texto)

    if texto == "":
        return None

    return texto


def normalizar_categoria(valor: str | None) -> str | None:
    texto = _normalizar_texto(valor)

    if texto is None:
        return None

    return CATEGORIAS.get(texto)


def normalizar_tipo_eleccion(valor: str | None) -> str | None:
    texto = _normalizar_texto(valor)

    if texto is None:
        return None

    return TIPOS_ELECCION.get(texto)


def validar_anio_eleccion(anio: int | str | None) -> bool:
    if anio is None:
        return False

    try:
        anio_int = int(anio)
    except (TypeError, ValueError):
        return False

    return 1983 <= anio_int <= 2100


__all__ = [
    "CATEGORIAS",
    "TIPOS_ELECCION",
    "limpiar_mesa",
    "limpiar_circuito",
    "normalizar_categoria",
    "normalizar_tipo_eleccion",
    "validar_anio_eleccion",
]
