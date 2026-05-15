from __future__ import annotations

import re


# Mapeo de característica telefónica → provincia.
# Cobertura: las características principales del país. No es exhaustivo —
# faltan muchas características de 4 dígitos (localidades chicas). Para esos
# casos, ``provincia_por_caracteristica`` devuelve None.
CARACTERISTICAS_PROVINCIA = {
    "11":  "Buenos Aires",  # AMBA / CABA (compartido)
    "220": "Buenos Aires",
    "221": "Buenos Aires",
    "223": "Buenos Aires",
    "224": "Buenos Aires",
    "225": "Buenos Aires",
    "226": "Buenos Aires",
    "227": "Buenos Aires",
    "228": "Buenos Aires",
    "229": "Buenos Aires",
    "230": "Buenos Aires",
    "236": "Buenos Aires",
    "237": "Buenos Aires",
    "249": "Buenos Aires",
    "260": "Mendoza",
    "261": "Mendoza",
    "262": "Mendoza",
    "263": "Mendoza",
    "264": "San Juan",
    "266": "San Luis",
    "280": "Chubut",
    "291": "Buenos Aires",
    "294": "Río Negro",
    "297": "Chubut",
    "298": "Río Negro",
    "299": "Neuquén",
    "336": "Buenos Aires",
    "341": "Santa Fe",
    "342": "Santa Fe",
    "343": "Entre Ríos",
    "345": "Entre Ríos",
    "346": "Santa Fe",
    "348": "Buenos Aires",
    "351": "Córdoba",
    "353": "Córdoba",
    "354": "Córdoba",
    "356": "Córdoba",
    "358": "Córdoba",
    "362": "Chaco",
    "364": "Chaco",
    "370": "Formosa",
    "376": "Misiones",
    "379": "Corrientes",
    "380": "La Rioja",
    "381": "Tucumán",
    "383": "Catamarca",
    "385": "Santiago del Estero",
    "387": "Salta",
    "388": "Jujuy",
}


def limpiar(valor: str | int | None) -> str | None:
    """Devuelve solo dígitos de un teléfono."""
    if valor is None:
        return None

    digitos = re.sub(r"\D+", "", str(valor))

    if digitos == "":
        return None

    return digitos


def _sin_prefijo_argentina(numero: str | None) -> str | None:
    """Quita prefijo internacional argentino si está presente."""
    numero = limpiar(numero)

    if numero is None:
        return None

    if numero.startswith("0054"):
        numero = numero[4:]
    elif numero.startswith("54"):
        numero = numero[2:]

    return numero


def _normalizar_nacional(numero: str | int | None) -> str | None:
    """
    Normaliza a formato nacional sin prefijo país.

    Maneja:
    - +54 9 11 xxxx xxxx
    - 54 9 11 xxxx xxxx
    - 011 15 xxxx xxxx
    - 11 15 xxxx xxxx
    - 11 xxxx xxxx
    """
    numero_limpio = _sin_prefijo_argentina(numero)

    if numero_limpio is None:
        return None

    # Quitar 0 inicial de llamadas nacionales.
    if numero_limpio.startswith("0"):
        numero_limpio = numero_limpio[1:]

    # Quitar 9 móvil luego del código país.
    if numero_limpio.startswith("9"):
        numero_limpio = numero_limpio[1:]

    # Quitar 15 móvil local después de característica.
    # Casos frecuentes:
    # 11 15 1234 5678 -> 11 1234 5678
    # 351 15 123 4567 -> 351 123 4567
    for area_len in range(2, 5):
        area = numero_limpio[:area_len]
        resto = numero_limpio[area_len:]

        if resto.startswith("15") and len(resto) > 2:
            return area + resto[2:]

    return numero_limpio


def validar(numero: str | int | None) -> bool:
    """Valida largo básico de teléfono argentino."""
    nacional = _normalizar_nacional(numero)

    if nacional is None:
        return False

    return len(nacional) == 10


def extraer_caracteristica(numero: str | int | None) -> str | None:
    """
    Extrae característica aproximada.

    Devuelve 2 dígitos para AMBA si empieza con 11.
    Para otros casos usa una heurística simple de 3 dígitos.
    """
    nacional = _normalizar_nacional(numero)

    if nacional is None or len(nacional) < 10:
        return None

    if nacional.startswith("11"):
        return "11"

    return nacional[:3]


def es_celular(numero: str | int | None) -> bool:
    """
    Detecta celular argentino por patrones frecuentes.

    Reconoce:
    - +54 9 ...
    - 54 9 ...
    - 011 15 ...
    - 11 15 ...
    """
    limpio = limpiar(numero)

    if limpio is None:
        return False

    if limpio.startswith("549"):
        return validar(limpio)

    nacional = _sin_prefijo_argentina(limpio)

    if nacional is None:
        return False

    if nacional.startswith("0"):
        nacional = nacional[1:]

    if nacional.startswith("9"):
        return validar(nacional)

    for area_len in range(2, 5):
        resto = nacional[area_len:]

        if resto.startswith("15"):
            return validar(nacional)

    return False


def normalizar_e164(numero: str | int | None, celular: bool | None = None) -> str | None:
    """
    Normaliza teléfono argentino a formato E.164 básico.

    Si celular=True, agrega +549.
    Si celular=False, agrega +54.
    Si celular=None, intenta detectar celular.
    """
    nacional = _normalizar_nacional(numero)

    if nacional is None or len(nacional) != 10:
        return None

    if celular is None:
        celular = es_celular(numero)

    if celular:
        return "+549" + nacional

    return "+54" + nacional


def provincia_por_caracteristica(numero: str | int | None) -> str | None:
    """Devuelve la provincia probable según la característica del teléfono.

    Usa la tabla embebida ``CARACTERISTICAS_PROVINCIA``. No es exhaustivo:
    cubre las áreas principales del país. Si la característica no está mapeada,
    devuelve ``None``.
    """
    caracteristica = extraer_caracteristica(numero)
    if caracteristica is None:
        return None
    return CARACTERISTICAS_PROVINCIA.get(caracteristica)


def extraer_de_texto(texto: str | None, *, normalizar: bool = False) -> tuple[str, ...]:
    """Extrae teléfonos argentinos válidos de un texto libre.

    Busca candidatos numéricos con un patrón laxo y los filtra contra
    :func:`validar` (que aplica las reglas argentinas). Devuelve una tupla
    con los matches originales tal cual aparecen en el texto, o (si
    ``normalizar=True``) en formato E.164.

    Inspirado en ``phonenumbers.PhoneNumberMatcher`` pero específico para
    Argentina. Sin dependencias.

    Examples
    --------
    >>> arg.telefonos.extraer_de_texto("Llamame al 11 1234-5678 o al 0351 7654321")
    ('11 1234-5678', '0351 7654321')

    >>> arg.telefonos.extraer_de_texto("Tel: +54 9 11 1234-5678", normalizar=True)
    ('+5491112345678',)
    """
    if not texto:
        return ()
    s = str(texto)
    # Candidatos: secuencias largas de dígitos con separadores
    # opcionales (+, espacios, guiones, puntos, paréntesis).
    candidatos_re = re.compile(
        r"(?<![\w\d])(?:\+?\d)(?:[\d\s.\-()]{8,25})\d(?![\w\d])"
    )
    resultados = []
    vistos: set[str] = set()
    for m in candidatos_re.finditer(s):
        bruto = m.group(0)
        # Eliminar paréntesis sueltos en bordes para que no sumen al tamaño
        candidato = bruto.strip(" \t\n(),.;")
        if validar(candidato):
            valor = normalizar_e164(candidato) if normalizar else candidato
            if valor and valor not in vistos:
                vistos.add(valor)
                resultados.append(valor)
    return tuple(resultados)


__all__ = [
    "CARACTERISTICAS_PROVINCIA",
    "limpiar",
    "validar",
    "extraer_caracteristica",
    "es_celular",
    "normalizar_e164",
    "provincia_por_caracteristica",
    "extraer_de_texto",
]
