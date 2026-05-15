from __future__ import annotations

import re


# Letras CPA por jurisdicción postal argentina.
# El CPA completo tiene formato: letra + 4 dígitos + 3 letras.
# Ejemplo: C1425ABC.
CPA_PROVINCIAS = {
    "A": "Salta",
    "B": "Buenos Aires",
    "C": "Ciudad Autónoma de Buenos Aires",
    "D": "San Luis",
    "E": "Entre Ríos",
    "F": "La Rioja",
    "G": "Santiago del Estero",
    "H": "Chaco",
    "J": "San Juan",
    "K": "Catamarca",
    "L": "La Pampa",
    "M": "Mendoza",
    "N": "Misiones",
    "P": "Formosa",
    "Q": "Neuquén",
    "R": "Río Negro",
    "S": "Santa Fe",
    "T": "Tucumán",
    "U": "Chubut",
    "V": "Tierra del Fuego",
    "W": "Corrientes",
    "X": "Córdoba",
    "Y": "Jujuy",
    "Z": "Santa Cruz",
}


CPA_REGEX = re.compile(r"^[A-Z]\d{4}[A-Z]{3}$")
CP4_REGEX = re.compile(r"^\d{4}$")


def limpiar_codigo_postal(codigo: str | int | None) -> str | None:
    """Limpia un código postal argentino."""
    if codigo is None:
        return None

    texto = str(codigo).strip().upper()
    texto = re.sub(r"[^A-Z0-9]+", "", texto)

    if texto == "":
        return None

    return texto


def validar_cp4(codigo: str | int | None) -> bool:
    """Valida código postal tradicional de 4 dígitos."""
    codigo_limpio = limpiar_codigo_postal(codigo)

    if codigo_limpio is None:
        return False

    return bool(CP4_REGEX.match(codigo_limpio))


def validar_cpa(codigo: str | int | None) -> bool:
    """Valida Código Postal Argentino CPA."""
    codigo_limpio = limpiar_codigo_postal(codigo)

    if codigo_limpio is None:
        return False

    if not CPA_REGEX.match(codigo_limpio):
        return False

    return codigo_limpio[0] in CPA_PROVINCIAS


def es_cp4(codigo: str | int | None) -> bool:
    """Indica si el código postal es CP tradicional de 4 dígitos."""
    return validar_cp4(codigo)


def es_cpa(codigo: str | int | None) -> bool:
    """Indica si el código postal es CPA de 8 caracteres."""
    return validar_cpa(codigo)


def tipo_codigo_postal(codigo: str | int | None) -> str | None:
    """Devuelve 'cp4', 'cpa' o None."""
    if validar_cp4(codigo):
        return "cp4"

    if validar_cpa(codigo):
        return "cpa"

    return None


def extraer_cp4(codigo: str | int | None) -> str | None:
    """Extrae los 4 dígitos del CPA o devuelve el CP4."""
    codigo_limpio = limpiar_codigo_postal(codigo)

    if codigo_limpio is None:
        return None

    if validar_cp4(codigo_limpio):
        return codigo_limpio

    if validar_cpa(codigo_limpio):
        return codigo_limpio[1:5]

    return None


def letra_provincia(codigo: str | int | None) -> str | None:
    """Devuelve la letra de provincia del CPA."""
    codigo_limpio = limpiar_codigo_postal(codigo)

    if not validar_cpa(codigo_limpio):
        return None

    return codigo_limpio[0]


def provincia_por_cpa(codigo: str | int | None) -> str | None:
    """Devuelve provincia según letra inicial del CPA."""
    letra = letra_provincia(codigo)

    if letra is None:
        return None

    return CPA_PROVINCIAS.get(letra)


def validar_cpa_provincia(
    codigo: str | int | None,
    provincia: str | None,
) -> bool:
    """Valida si el CPA corresponde a la provincia esperada."""
    provincia_cpa = provincia_por_cpa(codigo)

    if provincia_cpa is None or provincia is None:
        return False

    try:
        from argentina.provincias import lookup
    except ImportError:
        return provincia_cpa.lower() == str(provincia).lower()

    prov_input = lookup(provincia)
    prov_cpa = lookup(provincia_cpa)

    if prov_input is None or prov_cpa is None:
        return False

    return prov_input == prov_cpa


__all__ = [
    "CPA_PROVINCIAS",
    "limpiar_codigo_postal",
    "validar_cp4",
    "validar_cpa",
    "es_cp4",
    "es_cpa",
    "tipo_codigo_postal",
    "extraer_cp4",
    "letra_provincia",
    "provincia_por_cpa",
    "validar_cpa_provincia",
]
