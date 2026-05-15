from __future__ import annotations

import re
import unicodedata


def quitar_tildes(texto: str | None) -> str | None:
    """Quita tildes y marcas diacríticas."""
    if texto is None:
        return None

    texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto


def normalizar_texto(texto: str | None) -> str | None:
    """Normaliza texto: minúsculas, sin tildes y espacios simples."""
    if texto is None:
        return None

    texto = quitar_tildes(texto)
    texto = texto.lower()
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def snake_case(texto: str | None) -> str | None:
    """Convierte texto a snake_case."""
    if texto is None:
        return None

    texto = normalizar_texto(texto)
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    texto = re.sub(r"_+", "_", texto)
    return texto.strip("_")


def limpiar_columnas(df):
    """Devuelve una copia del DataFrame con columnas en snake_case."""
    result = df.copy()
    result.columns = [snake_case(col) for col in result.columns]
    return result


def porcentaje_nulls(df):
    """Calcula porcentaje de valores nulos por columna."""
    total = len(df)

    if total == 0:
        return {
            col: 0.0
            for col in df.columns
        }

    return {
        col: float(df[col].isna().mean() * 100)
        for col in df.columns
    }


__all__ = [
    "quitar_tildes",
    "normalizar_texto",
    "snake_case",
    "limpiar_columnas",
    "porcentaje_nulls",
]
