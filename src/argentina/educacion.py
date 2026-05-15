from __future__ import annotations

import re


JURISDICCIONES = {
    "02": "Ciudad Autónoma de Buenos Aires",
    "06": "Buenos Aires",
    "10": "Catamarca",
    "14": "Córdoba",
    "18": "Corrientes",
    "22": "Chaco",
    "26": "Chubut",
    "30": "Entre Ríos",
    "34": "Formosa",
    "38": "Jujuy",
    "42": "La Pampa",
    "46": "La Rioja",
    "50": "Mendoza",
    "54": "Misiones",
    "58": "Neuquén",
    "62": "Río Negro",
    "66": "Salta",
    "70": "San Juan",
    "74": "San Luis",
    "78": "Santa Cruz",
    "82": "Santa Fe",
    "86": "Santiago del Estero",
    "90": "Tucumán",
    "94": "Tierra del Fuego",
}


SECTORES = {
    "estatal": "Estatal",
    "publico": "Estatal",
    "público": "Estatal",
    "privado": "Privado",
    "privada": "Privado",
}


AMBITOS = {
    "urbano": "Urbano",
    "rural": "Rural",
}


NIVELES = {
    "inicial": "Inicial",
    "jardin": "Inicial",
    "jardín": "Inicial",
    "primaria": "Primaria",
    "primario": "Primaria",
    "secundaria": "Secundaria",
    "secundario": "Secundaria",
    "superior": "Superior",
}


def _solo_digitos(valor: str | int | None) -> str | None:
    """Devuelve solo dígitos."""
    if valor is None:
        return None

    digitos = re.sub(r"\D+", "", str(valor))

    if digitos == "":
        return None

    return digitos


def limpiar_cue(cue: str | int | None) -> str | None:
    """Limpia un CUE argentino."""
    cue_limpio = _solo_digitos(cue)

    if cue_limpio is None:
        return None

    return cue_limpio.zfill(9)


def validar_cue(cue: str | int | None) -> bool:
    """Valida formato básico de CUE."""
    crudos = _solo_digitos(cue)

    if crudos is None:
        return False

    return len(crudos) == 9


def limpiar_cueanexo(cueanexo: str | int | None) -> str | None:
    """Limpia un CUEANEXO argentino."""
    cueanexo_limpio = _solo_digitos(cueanexo)

    if cueanexo_limpio is None:
        return None

    return cueanexo_limpio.zfill(9)


def validar_cueanexo(cueanexo: str | int | None) -> bool:
    """Valida formato básico de CUEANEXO."""
    crudos = _solo_digitos(cueanexo)

    if crudos is None:
        return False

    return len(crudos) == 9


def extraer_jurisdiccion_cue(
    cue: str | int | None,
) -> str | None:
    """Extrae jurisdicción desde un CUE."""
    cue_limpio = limpiar_cue(cue)

    if cue_limpio is None:
        return None

    codigo = cue_limpio[:2]

    return JURISDICCIONES.get(codigo)


def normalizar_sector(
    valor: str | None,
) -> str | None:
    """Normaliza sector educativo."""
    if valor is None:
        return None

    texto = str(valor).strip().lower()

    return SECTORES.get(texto)


def normalizar_ambito(
    valor: str | None,
) -> str | None:
    """Normaliza ámbito educativo."""
    if valor is None:
        return None

    texto = str(valor).strip().lower()

    return AMBITOS.get(texto)


def normalizar_nivel(
    valor: str | None,
) -> str | None:
    """Normaliza nivel educativo."""
    if valor is None:
        return None

    texto = str(valor).strip().lower()

    return NIVELES.get(texto)


__all__ = [
    "JURISDICCIONES",
    "limpiar_cue",
    "validar_cue",
    "limpiar_cueanexo",
    "validar_cueanexo",
    "extraer_jurisdiccion_cue",
    "normalizar_sector",
    "normalizar_ambito",
    "normalizar_nivel",
]
