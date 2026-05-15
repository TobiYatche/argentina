from __future__ import annotations

import re


# Códigos BCRA (los 3 primeros dígitos del CBU identifican la entidad).
# Lista ampliada de los principales bancos argentinos vigentes.
# Fuente: tabla pública del BCRA. Hay fusiones recientes (HSBC → Galicia, etc.);
# se prefiere el nombre histórico más reconocido para retro-compatibilidad.
BANCOS = {
    "005": "HSBC Bank Argentina",
    "007": "Banco de Galicia y Buenos Aires",
    "011": "Banco de la Nación Argentina",
    "014": "Banco de la Provincia de Buenos Aires",
    "015": "ICBC",
    "016": "Citibank N.A.",
    "017": "BBVA Argentina",
    "020": "Banco de la Provincia de Buenos Aires",
    "027": "Banco Supervielle",
    "029": "Banco de la Ciudad de Buenos Aires",
    "034": "Banco Patagonia",
    "044": "Banco Hipotecario",
    "045": "Banco de San Juan",
    "046": "Banco do Brasil",
    "060": "Banco del Tucumán",
    "065": "Banco Industrial (Bind)",
    "072": "Banco Santander Argentina",
    "083": "Banco del Chubut",
    "085": "Banco Macro",
    "086": "Banco Itaú Argentina",
    "093": "Banco de la Provincia de Córdoba (Bancor)",
    "094": "Banco de la Provincia de Tierra del Fuego",
    "095": "Banco BICE",
    "097": "Banco de Corrientes",
    "098": "Banco de la Provincia del Neuquén (BPN)",
    "143": "Brubank",
    "147": "Banco Interfinanzas",
    "150": "HSBC Bank Argentina",
    "165": "JP Morgan Chase",
    "191": "Banco Credicoop Cooperativo",
    "247": "Banco Roela",
    "259": "Banco Itaú Argentina",
    "262": "Banco Mariva",
    "266": "BNP Paribas",
    "268": "Provincia Microempresas",
    "269": "Banco de la República Oriental del Uruguay",
    "277": "Banco de San Juan",
    "281": "Banco Meridian",
    "285": "Banco Macro",
    "295": "American Express Bank",
    "299": "Banco Coinag",
    "305": "Banco Columbia",
    "309": "Nuevo Banco de La Rioja",
    "310": "Banco del Sol / Mercado Pago",
    "311": "Nuevo Banco del Chaco",
    "315": "Banco Más Ventas",
    "319": "Banco CMF",
    "321": "Banco de Santiago del Estero",
    "322": "Banco Industrial",
    "330": "Nuevo Banco de Santa Fe",
    "331": "Banco Cetelem Argentina",
    "332": "Banco de Servicios y Transacciones",
    "336": "Bradesco Argentina",
    "338": "Banco de Servicios Financieros (BSF)",
    "384": "Wilobank",
    "386": "Nuevo Banco de Entre Ríos",
    "389": "Banco Columbia",
    "426": "Banco Comafi",
    "431": "Brubank",
}

# Alias semántico (mismo dict).
BANCOS_BCRA = BANCOS


def _solo_digitos(
    valor: str | int | None,
) -> str | None:
    """Devuelve solo dígitos."""
    if valor is None:
        return None

    digitos = re.sub(r"\D+", "", str(valor))

    if digitos == "":
        return None

    return digitos


def limpiar_cbu(
    valor: str | int | None,
) -> str | None:
    """Limpia un CBU/CVU dejando solo dígitos."""
    digitos = _solo_digitos(valor)

    if digitos is None:
        return None

    return digitos


def _validar_bloque_cbu(
    numeros: str,
    dv: str,
    pesos: list[int],
) -> bool:
    """Valida bloque de CBU."""
    suma = sum(
        int(n) * p
        for n, p in zip(numeros, pesos)
    )

    resto = suma % 10
    calculado = (10 - resto) % 10

    return calculado == int(dv)


def validar_cbu(
    valor: str | int | None,
) -> bool:
    """
    Valida CBU argentino con dígitos verificadores reales.
    """
    cbu = limpiar_cbu(valor)

    if cbu is None or len(cbu) != 22:
        return False

    bloque1 = cbu[:7]
    dv1 = cbu[7]

    bloque2 = cbu[8:21]
    dv2 = cbu[21]

    pesos1 = [7, 1, 3, 9, 7, 1, 3]
    pesos2 = [3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3]

    return (
        _validar_bloque_cbu(
            bloque1,
            dv1,
            pesos1,
        )
        and
        _validar_bloque_cbu(
            bloque2,
            dv2,
            pesos2,
        )
    )


def formatear_cbu(
    valor: str | int | None,
) -> str | None:
    """Formatea CBU como XXXXXXXX-XXXXXXXXXXXXXX."""
    cbu = limpiar_cbu(valor)

    if cbu is None or len(cbu) != 22:
        return None

    return f"{cbu[:8]}-{cbu[8:]}"


def codigo_banco_cbu(
    valor: str | int | None,
) -> str | None:
    """Extrae código bancario del CBU."""
    cbu = limpiar_cbu(valor)

    if cbu is None or len(cbu) < 3:
        return None

    return cbu[:3]


def banco_por_cbu(
    valor: str | int | None,
) -> str | None:
    """Obtiene el nombre del banco a partir del CBU."""
    codigo = codigo_banco_cbu(valor)

    if codigo is None:
        return None

    return BANCOS.get(codigo)


# Alias semántico más corto, recomendado en código nuevo.
banco_de_cbu = banco_por_cbu


def banco_por_codigo(
    codigo: str | int | None,
) -> str | None:
    """Obtiene el nombre del banco a partir del código BCRA (3 dígitos)."""
    if codigo is None:
        return None
    s = re.sub(r"\D+", "", str(codigo))
    if not s:
        return None
    # Pad a 3 dígitos por las dudas (ej. "11" → "011").
    s = s.zfill(3)[:3]
    return BANCOS.get(s)


def limpiar_alias(
    valor: str | None,
) -> str | None:
    """Normaliza alias bancario."""
    if valor is None:
        return None

    texto = str(valor).strip().upper()

    if texto == "":
        return None

    texto = re.sub(r"\s+", "", texto)

    return texto


def validar_alias(
    valor: str | None,
) -> bool:
    """
    Valida alias bancario argentino.

    Reglas básicas:
    - 6 a 20 caracteres
    - letras
    - números
    - punto
    - guion
    """
    alias = limpiar_alias(valor)

    if alias is None:
        return False

    if not (6 <= len(alias) <= 20):
        return False

    return bool(
        re.fullmatch(
            r"[A-Z0-9.-]+",
            alias,
        )
    )


def generar_cbu(
    codigo_banco: str | None = None,
    rng=None,
) -> str:
    """Genera un CBU con dígitos verificadores válidos.

    Útil para fixtures de tests. **No es un CBU real**: los DVs son correctos
    pero la cuenta no existe en ningún banco.

    Parameters
    ----------
    codigo_banco : str | None
        Código BCRA de 3 dígitos. Si ``None``, se elige uno aleatorio del
        catálogo ``BANCOS``.
    rng : random.Random, optional
        Generador propio para reproducibilidad.

    Examples
    --------
    >>> arg.bancos.generar_cbu()
    '0850590940090418135201'
    >>> arg.bancos.generar_cbu(codigo_banco="011")  # forzar Banco Nación
    '0110000940090418135201'
    """
    import random as _random
    r = rng or _random

    if codigo_banco is None:
        codigo_banco = r.choice(list(BANCOS.keys()))
    codigo_banco = re.sub(r"\D+", "", str(codigo_banco)).zfill(3)[:3]

    # Bloque 1: banco(3) + sucursal(4) + DV1(1) = 8
    sucursal = r.randint(0, 9999)
    bloque1_sin_dv = f"{codigo_banco}{sucursal:04d}"
    pesos1 = [7, 1, 3, 9, 7, 1, 3]
    suma1 = sum(int(d) * p for d, p in zip(bloque1_sin_dv, pesos1))
    dv1 = (10 - (suma1 % 10)) % 10
    bloque1 = f"{bloque1_sin_dv}{dv1}"

    # Bloque 2: cuenta(13) + DV2(1) = 14
    cuenta = r.randint(0, 9_999_999_999_999)
    bloque2_sin_dv = f"{cuenta:013d}"
    pesos2 = [3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3]
    suma2 = sum(int(d) * p for d, p in zip(bloque2_sin_dv, pesos2))
    dv2 = (10 - (suma2 % 10)) % 10

    return f"{bloque1}{bloque2_sin_dv}{dv2}"


def validar_cvu(
    valor: str | int | None,
) -> bool:
    """
    Validación básica de CVU.

    Por ahora:
    - largo 22
    - solo dígitos

    Expandible más adelante.
    """
    cvu = limpiar_cbu(valor)

    if cvu is None:
        return False

    return len(cvu) == 22


__all__ = [
    "BANCOS",
    "BANCOS_BCRA",
    "limpiar_cbu",
    "validar_cbu",
    "formatear_cbu",
    "codigo_banco_cbu",
    "banco_por_cbu",
    "banco_de_cbu",
    "banco_por_codigo",
    "limpiar_alias",
    "validar_alias",
    "validar_cvu",
    "generar_cbu",
]
