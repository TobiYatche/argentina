"""Parseo de montos monetarios escritos en formato argentino (y variantes).

Inverso natural de :func:`argentina.formato.pesos`. Acepta strings con
distintas convenciones de separadores y devuelve un número limpio.

Ejemplos:

- ``"$ 1.500.000,50"`` → ``1500000.5`` (formato argentino canónico)
- ``"1500000.50"``      → ``1500000.5`` (formato "inglés", también acepta)
- ``"1,5M"``            → ``1500000.0`` (sufijo corto)
- ``"1.5 millones"``    → ``1500000.0`` (escala en texto)
- ``"u$s 1.500,50"``    → con :func:`parsear_completo` detecta moneda USD

Convenciones del paquete:

- ``parsear(None)`` y ``parsear("")`` → ``None`` (no levanta).
- ``parsear("no es un monto")`` → ``None``.
- Para precisión decimal: :func:`parsear_decimal` devuelve ``Decimal``.
- No infiere moneda por contexto: solo cuando viene marcada inequívocamente.
- No interpreta argot (``"1 palo"``, ``"500 lucas"``). Es para datos,
  no texto natural.

Stdlib pura (``re``, ``decimal``).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Literal


# ---------------------------------------------------------------------------
# Constantes y patrones
# ---------------------------------------------------------------------------


Formato = Literal["argentino", "ingles", "ambiguo", "entero"]
Asumir = Literal["argentino", "ingles"]


# Marcadores de moneda y sus interpretaciones.
# IMPORTANTE: solo se reporta moneda cuando viene marcada inequívocamente.
# El símbolo "$" solo NO infiere moneda — en Argentina puede ser ARS o USD
# según contexto.
_MARCADORES_MONEDA: tuple[tuple[str, str], ...] = (
    # USD primero porque "u$s" tiene "$" adentro.
    ("usd", "USD"),
    ("u$s", "USD"),
    ("us$", "USD"),
    ("dolares", "USD"),
    ("dolar", "USD"),
    ("ars", "ARS"),
    ("ar$", "ARS"),
    ("pesos", "ARS"),
    ("peso", "ARS"),
)


# Sufijos multiplicadores (cerrados — no argot).
_MULTIPLICADORES_SUFIJO: dict[str, float] = {
    "k": 1_000.0,
    "m": 1_000_000.0,
    "mm": 1_000_000.0,
    "mil": 1_000.0,
    "miles": 1_000.0,
    "millon": 1_000_000.0,
    "millón": 1_000_000.0,
    "millones": 1_000_000.0,
    "mill": 1_000_000.0,
}


_RE_LIMPIAR_SIMBOLOS = re.compile(r"[$\s\xa0]+")


@dataclass(frozen=True)
class Monto:
    """Resultado de :func:`parsear_completo`."""
    valor: float
    moneda: str | None  # 'ARS', 'USD' o None si no estaba marcada
    formato_detectado: Formato


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------


def _quitar_marcadores_moneda(texto: str) -> tuple[str, str | None]:
    """Devuelve ``(texto_sin_marcadores, moneda_detectada_o_None)``."""
    bajo = texto.lower()
    moneda: str | None = None
    for marca, codigo in _MARCADORES_MONEDA:
        if marca in bajo:
            moneda = codigo
            # Reemplazar la primera aparición (case-insensitive).
            i = bajo.find(marca)
            texto = texto[:i] + " " + texto[i + len(marca):]
            bajo = texto.lower()
            break
    return texto, moneda


def _detectar_sufijo_multiplicador(texto: str) -> tuple[str, float]:
    """Detecta sufijo K/M/mil/millones al final del texto.

    Devuelve ``(texto_sin_sufijo, multiplicador)``. Si no hay sufijo,
    multiplicador es ``1.0``. El sufijo puede pegarse al número sin
    espacio (``"1,5M"``) o tener espacio (``"1,5 millones"``).
    """
    # Alternativas largas primero. Lookbehind permite dígito o espacio
    # antes del sufijo, pero exige que algo no-alfa lo preceda para no
    # romper palabras (ej. evita matchear la "m" final de "elemento").
    m = re.search(
        r"(?i)(?<=[\d\s])(millones|millón|millon|miles|mill|mil|mm|m|k)\.?\s*$",
        texto,
    )
    if not m:
        return texto, 1.0
    sufijo = m.group(1).lower().rstrip(".")
    mult = _MULTIPLICADORES_SUFIJO.get(sufijo, 1.0)
    if mult == 1.0:
        return texto, 1.0
    return texto[: m.start()].strip(), mult


def detectar_formato(texto: str) -> Formato:
    """Detecta el formato numérico de un string (sin convertir).

    Reglas:

    - Si tiene ``,`` Y ``.``: el separador decimal es el último de los dos.
    - Si tiene solo ``,``: argentino (decimal ``,``).
    - Si tiene solo ``.`` y exactamente 1-2 cifras después: inglés
      (decimal ``.``).
    - Si tiene solo ``.`` y exactamente 3 cifras después: argentino
      (miles ``.``).
    - Caso ambiguo (``"1.500"`` o ``"1500"``): devuelve ``"ambiguo"``
      cuando hay ``.``, ``"entero"`` cuando no hay separadores.
    """
    digitos_y_seps = re.sub(r"[^0-9,.\-]+", "", texto)
    if not digitos_y_seps:
        return "ambiguo"

    tiene_coma = "," in digitos_y_seps
    tiene_punto = "." in digitos_y_seps

    if tiene_coma and tiene_punto:
        ultimo_coma = digitos_y_seps.rfind(",")
        ultimo_punto = digitos_y_seps.rfind(".")
        return "argentino" if ultimo_coma > ultimo_punto else "ingles"

    if tiene_coma:
        return "argentino"

    if tiene_punto:
        # Solo punto: distinguir miles argentino (1.500) de decimal inglés (1.5)
        partes = digitos_y_seps.split(".")
        # Si hay varios puntos → miles argentino seguro.
        if len(partes) > 2:
            return "argentino"
        ultima = partes[-1]
        if len(ultima) == 3:
            return "ambiguo"
        # 1-2 cifras tras el punto → inglés decimal probable.
        return "ingles"

    return "entero"


def _aplicar_formato(numero: str, formato: Formato) -> str:
    """Normaliza ``numero`` (solo dígitos, coma, punto, signo) a notación
    canónica Python (``.`` como decimal, sin separador de miles).
    """
    if formato == "argentino":
        # Punto = miles → quitar; coma = decimal → reemplazar por punto.
        return numero.replace(".", "").replace(",", ".")
    if formato == "ingles":
        # Coma = miles → quitar; punto = decimal → mantener.
        return numero.replace(",", "")
    if formato == "entero":
        # Sin separadores, solo dígitos y signo.
        return numero
    # ambiguo: aplicar regla argentina por default (más común en datos AR).
    # Si tiene punto, asumir que es separador de miles.
    return numero.replace(".", "").replace(",", ".")


def _parsear_a_decimal(
    valor: str | int | float | None,
    *,
    asumir: Asumir | None = None,
) -> Decimal | None:
    """Núcleo de parsing. Devuelve ``Decimal`` o ``None``."""
    if valor is None:
        return None

    # Números ya parseados.
    if isinstance(valor, (int, float)):
        try:
            return Decimal(str(valor))
        except (InvalidOperation, ValueError):
            return None

    texto = str(valor).strip()
    if not texto:
        return None

    # Quitar marcadores de moneda y símbolos de pesos.
    texto, _moneda = _quitar_marcadores_moneda(texto)
    texto = _RE_LIMPIAR_SIMBOLOS.sub("", texto).strip()
    if not texto:
        return None

    # Detectar sufijo multiplicador antes de tocar el número.
    texto_sin_sufijo, mult = _detectar_sufijo_multiplicador(texto)
    cuerpo = texto_sin_sufijo.strip()

    # Validar: tras quitar moneda/sufijo, debe quedar solo número y separadores.
    if not re.fullmatch(r"-?\d[\d.,]*", cuerpo):
        return None

    formato = detectar_formato(cuerpo)
    if formato == "ambiguo" and asumir is not None:
        formato = asumir

    canonico = _aplicar_formato(cuerpo, formato)
    try:
        d = Decimal(canonico)
    except (InvalidOperation, ValueError):
        return None

    if mult != 1.0:
        d = d * Decimal(str(mult))
    return d


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------


def parsear(
    valor: str | int | float | None,
    *,
    asumir: Asumir | None = None,
) -> float | None:
    """Parsea un monto a ``float``. Devuelve ``None`` si no es parseable.

    Parameters
    ----------
    valor : str | int | float | None
        Texto o número.
    asumir : ``'argentino'`` | ``'ingles'`` | ``None``
        Cuando el formato es ambiguo (ej. ``"1.500"`` puede ser ``1.5``
        o ``1500``), forzar la interpretación. Default: heurística
        argentina (``"1.500"`` → ``1500``).

    Examples
    --------
    >>> parsear("$ 1.500.000,50")
    1500000.5
    >>> parsear("1500000.50")
    1500000.5
    >>> parsear("1,5M")
    1500000.0
    >>> parsear(None)
    """
    d = _parsear_a_decimal(valor, asumir=asumir)
    return float(d) if d is not None else None


def parsear_decimal(
    valor: str | int | float | None,
    *,
    asumir: Asumir | None = None,
) -> Decimal | None:
    """Como :func:`parsear` pero devuelve ``Decimal`` (precisión exacta)."""
    return _parsear_a_decimal(valor, asumir=asumir)


def parsear_estricto(
    valor: str | int | float | None,
) -> float | None:
    """Como :func:`parsear` pero devuelve ``None`` ante formato ambiguo.

    Útil cuando la cadena puede ser ``"1.500"`` y NO se quiere que la
    heurística decida — preferís que falle a que adivine mal.
    """
    if isinstance(valor, str):
        texto = valor.strip()
        # Replicar la limpieza para detectar formato sobre el cuerpo numérico.
        texto, _ = _quitar_marcadores_moneda(texto)
        texto = _RE_LIMPIAR_SIMBOLOS.sub("", texto).strip()
        texto, _ = _detectar_sufijo_multiplicador(texto)
        if texto and re.fullmatch(r"-?\d[\d.,]*", texto):
            if detectar_formato(texto) == "ambiguo":
                return None
    return parsear(valor)


def parsear_completo(
    valor: str | int | float | None,
    *,
    asumir: Asumir | None = None,
) -> Monto | None:
    """Parsea un monto detectando además moneda y formato.

    >>> parsear_completo("u$s 1.500,50")
    Monto(valor=1500.5, moneda='USD', formato_detectado='argentino')
    >>> parsear_completo("ARS 1500.50")
    Monto(valor=1500.5, moneda='ARS', formato_detectado='ingles')
    """
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        return Monto(valor=float(valor), moneda=None, formato_detectado="entero")

    texto = str(valor).strip()
    if not texto:
        return None

    texto_sin_moneda, moneda = _quitar_marcadores_moneda(texto)
    cuerpo = _RE_LIMPIAR_SIMBOLOS.sub("", texto_sin_moneda).strip()
    cuerpo_sin_sufijo, _mult = _detectar_sufijo_multiplicador(cuerpo)
    cuerpo_sin_sufijo = cuerpo_sin_sufijo.strip()
    if not cuerpo_sin_sufijo:
        return None

    formato = detectar_formato(cuerpo_sin_sufijo)
    if formato == "ambiguo" and asumir is not None:
        formato = asumir

    d = _parsear_a_decimal(valor, asumir=asumir)
    if d is None:
        return None

    return Monto(valor=float(d), moneda=moneda, formato_detectado=formato)


def formato_detectado(valor: str | None) -> Formato | None:
    """Detecta el formato sin convertir. ``None`` si la entrada está vacía."""
    if valor is None:
        return None
    texto = str(valor).strip()
    if not texto:
        return None
    texto, _ = _quitar_marcadores_moneda(texto)
    texto = _RE_LIMPIAR_SIMBOLOS.sub("", texto).strip()
    texto, _ = _detectar_sufijo_multiplicador(texto)
    if not texto:
        return None
    return detectar_formato(texto)


def moneda_detectada(valor: str | None) -> str | None:
    """Devuelve ``'ARS'``, ``'USD'`` o ``None``.

    Solo reporta moneda cuando viene marcada inequívocamente
    (``u$s``, ``USD``, ``dólares``, ``ARS``, ``pesos``). El símbolo
    ``$`` solo es ambiguo en Argentina, por eso NO basta.
    """
    if valor is None:
        return None
    _, moneda = _quitar_marcadores_moneda(str(valor))
    return moneda


__all__ = [
    "Monto",
    "parsear",
    "parsear_decimal",
    "parsear_estricto",
    "parsear_completo",
    "detectar_formato",
    "formato_detectado",
    "moneda_detectada",
]
