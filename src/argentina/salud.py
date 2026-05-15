from __future__ import annotations

from datetime import date, datetime
import re
import unicodedata


def _quitar_tildes(texto: str) -> str:
    """Quita tildes y marcas diacríticas."""
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def _normalizar_texto(valor: str | None) -> str | None:
    """Normaliza texto básico."""
    if valor is None:
        return None

    texto = str(valor).strip().lower()

    if texto == "":
        return None

    texto = _quitar_tildes(texto)
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    if texto == "":
        return None

    return texto


def normalizar_sexo(valor: str | None) -> str | None:
    """Normaliza sexo a 'M', 'F' o 'X'."""
    texto = _normalizar_texto(valor)

    if texto is None:
        return None

    mapa = {
        "m": "M",
        "masculino": "M",
        "varon": "M",
        "hombre": "M",
        "f": "F",
        "femenino": "F",
        "mujer": "F",
        "x": "X",
        "otro": "X",
        "otra": "X",
        "no binario": "X",
        "nobinario": "X",
    }

    return mapa.get(texto)


def normalizar_tipo_documento(valor: str | None) -> str | None:
    """Normaliza tipo de documento frecuente en salud."""
    texto = _normalizar_texto(valor)

    if texto is None:
        return None

    mapa = {
        "dni": "DNI",
        "documento nacional de identidad": "DNI",
        "du": "DNI",
        "lc": "LC",
        "libreta civica": "LC",
        "le": "LE",
        "libreta enrolamiento": "LE",
        "pasaporte": "PASAPORTE",
        "pas": "PASAPORTE",
        "ci": "CI",
        "cedula": "CI",
        "cedula identidad": "CI",
    }

    return mapa.get(texto)


def limpiar_matricula(valor: str | int | None) -> str | None:
    """Limpia una matrícula profesional dejando letras y números."""
    if valor is None:
        return None

    texto = str(valor).strip().upper()
    texto = re.sub(r"[^A-Z0-9]+", "", texto)

    if texto == "":
        return None

    return texto


def grupo_etario(edad: int | float | None) -> str | None:
    """Clasifica edad en grupos etarios simples."""
    if edad is None:
        return None

    try:
        edad_num = float(edad)
    except (TypeError, ValueError):
        return None

    if edad_num < 0:
        return None

    if edad_num < 1:
        return "0"
    if edad_num <= 4:
        return "1-4"
    if edad_num <= 9:
        return "5-9"
    if edad_num <= 14:
        return "10-14"
    if edad_num <= 19:
        return "15-19"
    if edad_num <= 24:
        return "20-24"
    if edad_num <= 34:
        return "25-34"
    if edad_num <= 44:
        return "35-44"
    if edad_num <= 54:
        return "45-54"
    if edad_num <= 64:
        return "55-64"

    return "65+"


def _to_date(valor: str | date | datetime | None) -> date | None:
    """Convierte string ISO o date/datetime a date."""
    if valor is None:
        return None

    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    if isinstance(valor, str):
        texto = valor.strip()

        if texto == "":
            return None

        try:
            return date.fromisoformat(texto[:10])
        except ValueError:
            return None

    return None


def edad_en_anios(
    fecha_nacimiento: str | date | datetime | None,
    fecha_referencia: str | date | datetime | None = None,
) -> int | None:
    """Calcula edad en años completos."""
    nacimiento = _to_date(fecha_nacimiento)

    if fecha_referencia is None:
        referencia = date.today()
    else:
        referencia = _to_date(fecha_referencia)

    if nacimiento is None or referencia is None:
        return None

    if nacimiento > referencia:
        return None

    edad = referencia.year - nacimiento.year

    if (referencia.month, referencia.day) < (
        nacimiento.month,
        nacimiento.day,
    ):
        edad -= 1

    return edad


__all__ = [
    "normalizar_sexo",
    "normalizar_tipo_documento",
    "limpiar_matricula",
    "grupo_etario",
    "edad_en_anios",
]
