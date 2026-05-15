"""Patentes de vehículos argentinos.

Soporta los tres formatos vigentes (sin red, sin pandas):

- **Vieja** (1995-2016): ``AAA 999`` — 3 letras + 3 dígitos. Ej: ``"ABC 123"``.
- **Mercosur** (desde 2016 en autos): ``AA 999 BB`` — 2 letras + 3 dígitos + 2 letras.
- **Moto** (vieja, hasta 2016): ``999 AAA`` — 3 dígitos + 3 letras.
- **Moto Mercosur**: misma estructura ``A999BBB`` (1 letra + 3 dígitos + 3 letras).
"""

from __future__ import annotations

import re

# Patrones canónicos (después de limpiar: solo [A-Z0-9]).
_RE_VIEJA      = re.compile(r"^[A-Z]{3}\d{3}$")          # AAA999
_RE_MERCOSUR   = re.compile(r"^[A-Z]{2}\d{3}[A-Z]{2}$")  # AA999BB
_RE_MOTO_VIEJA = re.compile(r"^\d{3}[A-Z]{3}$")          # 999AAA
_RE_MOTO_MERC  = re.compile(r"^[A-Z]\d{3}[A-Z]{3}$")     # A999BBB


def limpiar(valor: str | None) -> str | None:
    """Devuelve solo letras y dígitos, en mayúsculas."""
    if valor is None:
        return None
    s = re.sub(r"[^A-Za-z0-9]+", "", str(valor)).upper()
    return s if s else None


def tipo(valor: str | None) -> str | None:
    """Devuelve ``"vieja"``, ``"mercosur"``, ``"moto_vieja"``, ``"moto_mercosur"`` o ``None``."""
    s = limpiar(valor)
    if s is None:
        return None
    if _RE_VIEJA.match(s):
        return "vieja"
    if _RE_MERCOSUR.match(s):
        return "mercosur"
    if _RE_MOTO_VIEJA.match(s):
        return "moto_vieja"
    if _RE_MOTO_MERC.match(s):
        return "moto_mercosur"
    return None


def validar(valor: str | None) -> bool:
    """``True`` si tiene formato de patente argentina válido."""
    return tipo(valor) is not None


def es_mercosur(valor: str | None) -> bool:
    """``True`` para formato Mercosur (auto o moto)."""
    t = tipo(valor)
    return t in {"mercosur", "moto_mercosur"}


def es_moto(valor: str | None) -> bool:
    """``True`` para patente de moto (cualquier formato)."""
    t = tipo(valor)
    return t in {"moto_vieja", "moto_mercosur"}


def formatear(valor: str | None) -> str | None:
    """Devuelve la patente con separadores canónicos.

    - vieja        → ``"AAA 999"``
    - mercosur     → ``"AA 999 BB"``
    - moto vieja   → ``"999 AAA"``
    - moto mercosur→ ``"A 999 BBB"``

    Si la patente es inválida, devuelve ``None``.
    """
    s = limpiar(valor)
    t = tipo(s)
    if t is None:
        return None
    if t == "vieja":
        return f"{s[:3]} {s[3:]}"
    if t == "mercosur":
        return f"{s[:2]} {s[2:5]} {s[5:]}"
    if t == "moto_vieja":
        return f"{s[:3]} {s[3:]}"
    if t == "moto_mercosur":
        return f"{s[:1]} {s[1:4]} {s[4:]}"
    return None


__all__ = [
    "limpiar",
    "validar",
    "tipo",
    "es_mercosur",
    "es_moto",
    "formatear",
]
