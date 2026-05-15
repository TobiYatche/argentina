from __future__ import annotations

import re
import unicodedata


def _quitar_tildes(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def normalizar(direccion: str | None) -> str | None:
    """Normaliza una dirección argentina básica."""
    if direccion is None:
        return None

    texto = str(direccion).strip().lower()

    if texto == "":
        return None

    texto = _quitar_tildes(texto)
    texto = re.sub(r"[.,;]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    reemplazos = {
        "avenida": "av",
        "avda": "av",
        "av.": "av",
        "calle": "",
        "pje": "pasaje",
        "pje.": "pasaje",
        "dto": "depto",
        "dpto": "depto",
        "departamento": "depto",
        "piso.": "piso",
    }

    palabras = [
        reemplazos.get(palabra, palabra)
        for palabra in texto.split()
    ]

    texto = " ".join(
        palabra for palabra in palabras if palabra
    )
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto or None


def extraer_altura(direccion: str | None) -> str | None:
    """Extrae la primera altura numérica probable."""
    texto = normalizar(direccion)

    if texto is None:
        return None

    match = re.search(r"\b(\d{1,5})\b", texto)

    if match is None:
        return None

    return match.group(1)


def tiene_altura(direccion: str | None) -> bool:
    """Indica si una dirección tiene altura numérica."""
    return extraer_altura(direccion) is not None


def extraer_calle(direccion: str | None) -> str | None:
    """Extrae calle antes de la altura."""
    texto = normalizar(direccion)

    if texto is None:
        return None

    altura = extraer_altura(texto)

    if altura is None:
        return texto

    calle = texto.split(altura, 1)[0].strip()

    return calle or None


def extraer_piso(direccion: str | None) -> str | None:
    """Extrae piso si aparece explícitamente."""
    texto = normalizar(direccion)

    if texto is None:
        return None

    match = re.search(
        r"\b(?:piso|p)\s*([0-9]{1,2}|pb)\b",
        texto,
    )

    if match is None:
        return None

    return match.group(1).upper()


def extraer_departamento(direccion: str | None) -> str | None:
    """Extrae departamento/unidad si aparece explícitamente."""
    texto = normalizar(direccion)

    if texto is None:
        return None

    match = re.search(
        r"\b(?:depto|departamento|unidad|uf)\s*([a-z0-9]{1,4})\b",
        texto,
    )

    if match is None:
        return None

    return match.group(1).upper()


def parsear(direccion: str | None) -> dict:
    """Parsea una dirección argentina básica."""
    return {
        "direccion_normalizada": normalizar(direccion),
        "calle": extraer_calle(direccion),
        "altura": extraer_altura(direccion),
        "piso": extraer_piso(direccion),
        "departamento": extraer_departamento(direccion),
        "tiene_altura": tiene_altura(direccion),
    }


__all__ = [
    "normalizar",
    "extraer_altura",
    "extraer_calle",
    "extraer_piso",
    "extraer_departamento",
    "tiene_altura",
    "parsear",
]
