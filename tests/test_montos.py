"""Tests del módulo ``argentina.montos``.

Sin internet, sin archivos externos.
"""

from decimal import Decimal

import pytest

import argentina as arg


# ---------------------------------------------------------------------------
# parsear: formato argentino
# ---------------------------------------------------------------------------


def test_parsear_argentino_canonico():
    assert arg.montos.parsear("$ 1.500.000,50") == 1_500_000.5


def test_parsear_argentino_sin_espacios():
    assert arg.montos.parsear("$1.500.000") == 1_500_000.0


def test_parsear_argentino_decimal_coma():
    assert arg.montos.parsear("1.234,56") == 1234.56


def test_parsear_argentino_solo_coma_decimal():
    assert arg.montos.parsear("0,50") == 0.5


def test_parsear_argentino_solo_punto_miles():
    assert arg.montos.parsear("1.500.000") == 1_500_000.0


def test_parsear_argentino_pesos_palabra():
    assert arg.montos.parsear("1.500.000 pesos") == 1_500_000.0


def test_parsear_ars_prefijo():
    assert arg.montos.parsear("ARS 1.500.000") == 1_500_000.0
    assert arg.montos.parsear("AR$ 1.500.000") == 1_500_000.0


# ---------------------------------------------------------------------------
# parsear: formato inglés
# ---------------------------------------------------------------------------


def test_parsear_ingles_punto_decimal():
    assert arg.montos.parsear("1500000.50") == 1_500_000.5


def test_parsear_ingles_con_miles_coma():
    assert arg.montos.parsear("1,500,000.50") == 1_500_000.5


# ---------------------------------------------------------------------------
# parsear: negativos, cero, números
# ---------------------------------------------------------------------------


def test_parsear_negativo():
    assert arg.montos.parsear("-1.500,50") == -1500.5


def test_parsear_cero():
    assert arg.montos.parsear("0") == 0.0
    assert arg.montos.parsear("0,00") == 0.0


def test_parsear_int_pasa_directo():
    assert arg.montos.parsear(1500000) == 1_500_000.0


def test_parsear_float_pasa_directo():
    assert arg.montos.parsear(1500000.5) == 1_500_000.5


# ---------------------------------------------------------------------------
# parsear: sufijos multiplicadores
# ---------------------------------------------------------------------------


def test_parsear_sufijo_M():
    assert arg.montos.parsear("1,5M") == 1_500_000.0
    assert arg.montos.parsear("1.5M") == 1_500_000.0
    assert arg.montos.parsear("2M") == 2_000_000.0


def test_parsear_sufijo_K():
    assert arg.montos.parsear("500K") == 500_000.0
    assert arg.montos.parsear("2K") == 2_000.0


def test_parsear_sufijo_MM():
    assert arg.montos.parsear("2.5MM") == 2_500_000.0


def test_parsear_palabra_millones():
    assert arg.montos.parsear("1.5 millones") == 1_500_000.0
    assert arg.montos.parsear("1 millón") == 1_000_000.0


def test_parsear_palabra_mil():
    assert arg.montos.parsear("500 mil") == 500_000.0


# ---------------------------------------------------------------------------
# parsear: casos inválidos
# ---------------------------------------------------------------------------


def test_parsear_none():
    assert arg.montos.parsear(None) is None


def test_parsear_vacio():
    assert arg.montos.parsear("") is None
    assert arg.montos.parsear("   ") is None


def test_parsear_texto_no_es_monto():
    assert arg.montos.parsear("no es un monto") is None
    assert arg.montos.parsear("abc") is None


def test_parsear_solo_simbolos():
    assert arg.montos.parsear("$") is None
    assert arg.montos.parsear("$$$") is None


# ---------------------------------------------------------------------------
# parsear_decimal
# ---------------------------------------------------------------------------


def test_parsear_decimal_devuelve_decimal():
    res = arg.montos.parsear_decimal("1.234,56")
    assert isinstance(res, Decimal)
    assert res == Decimal("1234.56")


def test_parsear_decimal_precision_exacta():
    # Decimal evita el error típico de float (0.1 + 0.2 != 0.3)
    res = arg.montos.parsear_decimal("0,1") + arg.montos.parsear_decimal("0,2")
    assert res == Decimal("0.3")


def test_parsear_decimal_none():
    assert arg.montos.parsear_decimal(None) is None
    assert arg.montos.parsear_decimal("xx") is None


# ---------------------------------------------------------------------------
# parsear_estricto: rechaza ambigüedad
# ---------------------------------------------------------------------------


def test_parsear_estricto_rechaza_ambiguo():
    # "1.500" es ambiguo (¿miles AR o decimal ENG?)
    assert arg.montos.parsear_estricto("1.500") is None


def test_parsear_estricto_acepta_inequivoco():
    assert arg.montos.parsear_estricto("1.500,50") == 1500.5
    assert arg.montos.parsear_estricto("1500.5") == 1500.5
    assert arg.montos.parsear_estricto("1500") == 1500.0


# ---------------------------------------------------------------------------
# asumir explícito sobre ambiguos
# ---------------------------------------------------------------------------


def test_parsear_ambiguo_heuristica_default_argentina():
    # Sin asumir, "1.500" se interpreta como argentino (miles): 1500
    assert arg.montos.parsear("1.500") == 1500.0


def test_parsear_ambiguo_asumir_ingles():
    assert arg.montos.parsear("1.500", asumir="ingles") == 1.5


def test_parsear_ambiguo_asumir_argentino_explicito():
    assert arg.montos.parsear("1.500", asumir="argentino") == 1500.0


# ---------------------------------------------------------------------------
# parsear_completo: detecta moneda y formato
# ---------------------------------------------------------------------------


def test_parsear_completo_usd():
    m = arg.montos.parsear_completo("u$s 1.500,50")
    assert m.valor == 1500.5
    assert m.moneda == "USD"
    assert m.formato_detectado == "argentino"


def test_parsear_completo_ars():
    m = arg.montos.parsear_completo("ARS 1500.50")
    assert m.valor == 1500.5
    assert m.moneda == "ARS"
    assert m.formato_detectado == "ingles"


def test_parsear_completo_sin_moneda_marcada():
    m = arg.montos.parsear_completo("$ 1.500.000,50")
    # $ solo no infiere moneda (ambiguo en Argentina).
    assert m.moneda is None
    assert m.valor == 1_500_000.5


def test_parsear_completo_numero_directo():
    m = arg.montos.parsear_completo(1500)
    assert m.valor == 1500.0
    assert m.moneda is None


def test_parsear_completo_invalido():
    assert arg.montos.parsear_completo(None) is None
    assert arg.montos.parsear_completo("") is None
    assert arg.montos.parsear_completo("xyz") is None


# ---------------------------------------------------------------------------
# formato_detectado
# ---------------------------------------------------------------------------


def test_formato_detectado_argentino():
    assert arg.montos.formato_detectado("1.500.000,50") == "argentino"


def test_formato_detectado_ingles():
    assert arg.montos.formato_detectado("1,500,000.50") == "ingles"
    assert arg.montos.formato_detectado("1500.5") == "ingles"


def test_formato_detectado_entero():
    assert arg.montos.formato_detectado("1500000") == "entero"


def test_formato_detectado_ambiguo():
    assert arg.montos.formato_detectado("1.500") == "ambiguo"


def test_formato_detectado_vacio_none():
    assert arg.montos.formato_detectado(None) is None
    assert arg.montos.formato_detectado("") is None


# ---------------------------------------------------------------------------
# moneda_detectada
# ---------------------------------------------------------------------------


def test_moneda_detectada_usd():
    assert arg.montos.moneda_detectada("u$s 1.500") == "USD"
    assert arg.montos.moneda_detectada("USD 100") == "USD"
    assert arg.montos.moneda_detectada("US$ 100") == "USD"
    assert arg.montos.moneda_detectada("100 dolares") == "USD"


def test_moneda_detectada_ars():
    assert arg.montos.moneda_detectada("ARS 100") == "ARS"
    assert arg.montos.moneda_detectada("100 pesos") == "ARS"
    assert arg.montos.moneda_detectada("AR$ 100") == "ARS"


def test_moneda_detectada_dolar_solo_no_infiere():
    # "$" solo NO basta — es ambiguo en Argentina.
    assert arg.montos.moneda_detectada("$ 1.500") is None
    assert arg.montos.moneda_detectada("$1500") is None


def test_moneda_detectada_none_vacio():
    assert arg.montos.moneda_detectada(None) is None
    assert arg.montos.moneda_detectada("") is None


# ---------------------------------------------------------------------------
# Round-trip con formato.pesos (inverso)
# ---------------------------------------------------------------------------


def test_round_trip_con_formato_pesos():
    for n in [1500000.0, 0.0, -1000.0, 1234.5, 999999.99]:
        formateado = arg.formato.pesos(n, decimales=2)
        parseado = arg.montos.parsear(formateado)
        assert parseado == n, f"round-trip falló para {n}: {formateado} → {parseado}"


def test_round_trip_decimales_cero():
    for n in [1500, -1000, 0]:
        formateado = arg.formato.pesos(n, decimales=0)
        parseado = arg.montos.parsear(formateado)
        assert parseado == float(n)


# ---------------------------------------------------------------------------
# Reexport en formato
# ---------------------------------------------------------------------------


def test_formato_parsear_pesos_reexport():
    assert arg.formato.parsear_pesos("$ 1.500,50") == 1500.5
    assert arg.formato.parsear_pesos("$ 1.500,50") == arg.montos.parsear("$ 1.500,50")


# ---------------------------------------------------------------------------
# Comportamiento transversal
# ---------------------------------------------------------------------------


def test_modulo_expuesto_en_paquete():
    assert hasattr(arg, "montos")
    assert callable(arg.montos.parsear)
