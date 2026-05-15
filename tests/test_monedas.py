from datetime import date

import pytest

import argentina as arg


def test_actual():
    actual = arg.monedas.actual()
    assert actual.codigo_iso == "ARS"
    assert actual.simbolo == "$"
    assert actual.vigente is True


def test_en_fecha():
    m = arg.monedas.en(date(1986, 6, 1))
    assert m.nombre == "Austral"


def test_en_fecha_1980():
    m = arg.monedas.en(date(1980, 1, 1))
    assert m.nombre == "Peso Ley 18.188"


def test_en_fecha_actual():
    m = arg.monedas.en(date.today())
    assert m.codigo_iso == "ARS"


def test_lookup_iso():
    assert arg.monedas.lookup("ARS").nombre == "Peso"
    assert arg.monedas.lookup("ara") is not None  # case-insensitive (Austral)


def test_lookup_simbolo():
    assert arg.monedas.lookup("m$n").nombre == "Peso Moneda Nacional"
    assert arg.monedas.lookup("₳").nombre == "Austral"


def test_convertir_idempotente():
    assert arg.monedas.convertir(1000, "ARS", "ARS") == 1000.0


def test_convertir_austral_a_pesos():
    # 10.000 australes = 1 peso
    assert arg.monedas.convertir(10_000, "₳") == pytest.approx(1.0)


def test_convertir_mn_a_pesos():
    # Factor acumulado m$n → ARS = 1 / 10^13
    # 1 m$n = 10^-13 pesos
    r = arg.monedas.convertir(1, "m$n")
    assert r == pytest.approx(1e-13)


def test_convertir_pesos_a_australes():
    # 1 peso = 10.000 australes (vuelta atrás)
    assert arg.monedas.convertir(1, "ARS", "Austral") == pytest.approx(10_000)


def test_convertir_invalida():
    assert arg.monedas.convertir(100, "USD") is None


def test_listar_orden():
    monedas = arg.monedas.listar()
    for a, b in zip(monedas, monedas[1:]):
        assert a.inicio < b.inicio


def test_factores_completos():
    # Todas las monedas excepto la última tienen factor_a_siguiente
    for m in arg.monedas.MONEDAS[:-1]:
        assert m.factor_a_siguiente is not None
    assert arg.monedas.actual().factor_a_siguiente is None
