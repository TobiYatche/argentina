from datetime import date

import argentina as arg


def test_listar():
    assert len(arg.presidentes) >= 50


def test_en_fecha():
    # Kirchner 2003-2007
    p = arg.presidentes.en(date(2005, 1, 1))
    assert p.nombre == "Néstor Kirchner"


def test_en_fecha_string():
    p = arg.presidentes.en("2010-06-01")
    assert p.nombre == "Cristina Fernández de Kirchner"


def test_en_fecha_alfonsin():
    p = arg.presidentes.en(date(1986, 1, 1))
    assert p.nombre == "Raúl Alfonsín"
    assert p.tipo == "constitucional"


def test_lookup_simple():
    p = arg.presidentes.lookup("Perón")
    assert p is not None
    assert "Perón" in p.nombre


def test_lookup_sin_tilde():
    p = arg.presidentes.lookup("peron")
    assert p is not None


def test_por_partido():
    ucr = arg.presidentes.por_partido("UCR")
    nombres = {p.nombre for p in ucr}
    assert "Raúl Alfonsín" in nombres
    assert "Hipólito Yrigoyen" in nombres


def test_por_tipo_de_facto():
    de_facto = arg.presidentes.por_tipo("de facto")
    nombres = {p.nombre for p in de_facto}
    assert "Jorge Rafael Videla" in nombres
    assert "Juan Carlos Onganía" in nombres


def test_dias_mandato():
    # Alfonsín renunció 5 meses antes; ~2042 días en lugar de 6 años (~2191)
    p = arg.presidentes.lookup("Alfonsín")
    assert 2000 < p.dias < 2100


def test_vigente_en():
    p = arg.presidentes.lookup("Néstor Kirchner")
    assert p.vigente_en(date(2005, 6, 1)) is True
    assert p.vigente_en(date(2010, 1, 1)) is False


def test_orden_cronologico():
    # La lista debe estar ordenada por fecha de inicio
    for a, b in zip(arg.presidentes, arg.presidentes.listar()[1:]):
        assert a.inicio <= b.inicio


def test_como_tabla():
    t = arg.presidentes.como_tabla()
    assert len(t) >= 50
    assert isinstance(t[0]["inicio"], str)  # ISO format
