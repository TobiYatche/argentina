"""Tests del módulo ``argentina.formato``.

Sin internet, sin archivos externos.
"""

from datetime import date, datetime

import pytest

import argentina as arg


# ---------------------------------------------------------------------------
# Teléfono
# ---------------------------------------------------------------------------


def test_telefono_nacional_amba_fijo():
    assert arg.formato.telefono("1140404040") == "(011) 4040-4040"


def test_telefono_nacional_acepta_inputs_sucios():
    assert arg.formato.telefono("011 4040-4040") == "(011) 4040-4040"
    assert arg.formato.telefono("(011) 4040-4040") == "(011) 4040-4040"


def test_telefono_nacional_caracteristica_3_digitos():
    assert arg.formato.telefono("3514445555") == "(0351) 444-5555"


def test_telefono_e164_fijo():
    assert arg.formato.telefono("1140404040", estilo="e164") == "+541140404040"


def test_telefono_e164_celular():
    assert (
        arg.formato.telefono("+5491140404040", estilo="e164")
        == "+5491140404040"
    )


def test_telefono_internacional_fijo():
    assert (
        arg.formato.telefono("1140404040", estilo="internacional")
        == "+54 11 4040-4040"
    )


def test_telefono_internacional_celular():
    assert (
        arg.formato.telefono("+5491140404040", estilo="internacional")
        == "+54 9 11 4040-4040"
    )


def test_telefono_invalido_devuelve_none():
    assert arg.formato.telefono("xyz") is None
    assert arg.formato.telefono(None) is None
    assert arg.formato.telefono("") is None
    assert arg.formato.telefono("123") is None


def test_telefono_estilo_invalido_levanta():
    with pytest.raises(ValueError):
        arg.formato.telefono("1140404040", estilo="culichi")


# ---------------------------------------------------------------------------
# Pesos
# ---------------------------------------------------------------------------


def test_pesos_basico():
    assert arg.formato.pesos(1_500_000) == "$ 1.500.000"


def test_pesos_con_decimales():
    assert arg.formato.pesos(1_500_000.5, decimales=2) == "$ 1.500.000,50"


def test_pesos_decimales_cero_no_muestra_coma():
    assert arg.formato.pesos(1500) == "$ 1.500"
    assert "," not in arg.formato.pesos(1500)


def test_pesos_separador_miles_es_punto():
    res = arg.formato.pesos(1_234_567)
    assert res == "$ 1.234.567"


def test_pesos_cero():
    assert arg.formato.pesos(0) == "$ 0"


def test_pesos_negativo_signo_antes_del_simbolo():
    assert arg.formato.pesos(-1000) == "-$ 1.000"


def test_pesos_string_numerico():
    assert arg.formato.pesos("1500") == "$ 1.500"


def test_pesos_string_invalido():
    assert arg.formato.pesos("xx") is None
    assert arg.formato.pesos("") is None


def test_pesos_none():
    assert arg.formato.pesos(None) is None


def test_pesos_simbolo_personalizado():
    assert arg.formato.pesos(100, simbolo="ARS ") == "ARS 100"
    assert arg.formato.pesos(100, simbolo="") == "100"


def test_pesos_decimales_negativos_levanta():
    with pytest.raises(ValueError):
        arg.formato.pesos(100, decimales=-1)


# ---------------------------------------------------------------------------
# Código postal
# ---------------------------------------------------------------------------


def test_codigo_postal_cp4():
    assert arg.formato.codigo_postal("1414") == "1414"


def test_codigo_postal_cpa_canonico():
    assert arg.formato.codigo_postal("C1414BAA") == "C1414BAA"


def test_codigo_postal_cpa_normaliza_minusculas():
    assert arg.formato.codigo_postal("c1414baa") == "C1414BAA"


def test_codigo_postal_cpa_quita_separadores():
    assert arg.formato.codigo_postal("  C1414-BAA ") == "C1414BAA"


def test_codigo_postal_invalido():
    assert arg.formato.codigo_postal("xyz") is None
    assert arg.formato.codigo_postal("999") is None
    assert arg.formato.codigo_postal(None) is None
    assert arg.formato.codigo_postal("") is None


# ---------------------------------------------------------------------------
# Fecha
# ---------------------------------------------------------------------------


def test_fecha_corto_default():
    assert arg.formato.fecha(date(2026, 5, 13)) == "13/05/2026"


def test_fecha_corto_explicito():
    assert arg.formato.fecha(date(2026, 5, 13), estilo="corto") == "13/05/2026"


def test_fecha_largo():
    assert (
        arg.formato.fecha(date(2026, 5, 13), estilo="largo")
        == "13 de mayo de 2026"
    )


def test_fecha_largo_meses_en_espanol():
    meses_esperados = [
        (1, "enero"), (2, "febrero"), (3, "marzo"), (4, "abril"),
        (5, "mayo"), (6, "junio"), (7, "julio"), (8, "agosto"),
        (9, "septiembre"), (10, "octubre"), (11, "noviembre"), (12, "diciembre"),
    ]
    for m, nombre in meses_esperados:
        s = arg.formato.fecha(date(2026, m, 15), estilo="largo")
        assert nombre in s, f"falta {nombre} en {s!r}"


def test_fecha_iso():
    assert arg.formato.fecha(date(2026, 5, 13), estilo="iso") == "2026-05-13"


def test_fecha_acepta_string():
    assert arg.formato.fecha("13/05/2026") == "13/05/2026"
    assert arg.formato.fecha("2026-05-13") == "13/05/2026"


def test_fecha_acepta_datetime():
    assert arg.formato.fecha(datetime(2026, 5, 13, 9, 30)) == "13/05/2026"


def test_fecha_invalida():
    assert arg.formato.fecha("asdf") is None
    assert arg.formato.fecha(None) is None
    assert arg.formato.fecha("") is None


def test_fecha_estilo_invalido_levanta():
    with pytest.raises(ValueError):
        arg.formato.fecha(date(2026, 5, 13), estilo="brasileño")


# ---------------------------------------------------------------------------
# Reexports: devuelven exactamente lo mismo que la función original
# ---------------------------------------------------------------------------


def test_dni_reexport_coincide_con_personas():
    for v in ["12345678", "12.345.678", "1234567", None, "xxx"]:
        assert arg.formato.dni(v) == arg.personas.formatear_dni(v)


def test_cuit_reexport_coincide_con_personas():
    for v in ["20123456786", "20-12345678-6", "abc", None]:
        assert arg.formato.cuit(v) == arg.personas.formatear_cuit(v)


def test_cbu_reexport_coincide_con_bancos():
    for v in ["2850590940090418135201", "xxx", None]:
        assert arg.formato.cbu(v) == arg.bancos.formatear_cbu(v)


def test_patente_reexport_coincide_con_patentes():
    for v in ["AB123CD", "AAA111", "abc", None]:
        assert arg.formato.patente(v) == arg.patentes.formatear(v)


# ---------------------------------------------------------------------------
# Comportamiento transversal
# ---------------------------------------------------------------------------


def test_modulo_expuesto_en_paquete():
    assert hasattr(arg, "formato")
    assert callable(arg.formato.telefono)
    assert callable(arg.formato.pesos)
    assert callable(arg.formato.fecha)
    assert callable(arg.formato.codigo_postal)


def test_reexports_no_reimplementan():
    # Los reexports delegan, así no hay riesgo de desincronización.
    # Verifico que están definidos como funciones que llaman al original.
    import inspect

    fuente = inspect.getsource(arg.formato.dni)
    assert "personas.formatear_dni" in fuente
