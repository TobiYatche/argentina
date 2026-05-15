import argentina


def test_limpiar_codigo_postal_cpa():
    assert argentina.postal.limpiar_codigo_postal(" c1425 abc ") == "C1425ABC"


def test_limpiar_codigo_postal_cp4():
    assert argentina.postal.limpiar_codigo_postal(" 1425 ") == "1425"


def test_validar_cp4():
    assert argentina.postal.validar_cp4("1425") is True


def test_validar_cp4_invalido():
    assert argentina.postal.validar_cp4("C1425ABC") is False


def test_validar_cpa():
    assert argentina.postal.validar_cpa("C1425ABC") is True


def test_validar_cpa_con_espacio():
    assert argentina.postal.validar_cpa("C1425 ABC") is True


def test_validar_cpa_invalido():
    assert argentina.postal.validar_cpa("1425") is False


def test_tipo_codigo_postal():
    assert argentina.postal.tipo_codigo_postal("1425") == "cp4"
    assert argentina.postal.tipo_codigo_postal("C1425ABC") == "cpa"
    assert argentina.postal.tipo_codigo_postal("abc") is None


def test_extraer_cp4():
    assert argentina.postal.extraer_cp4("C1425ABC") == "1425"
    assert argentina.postal.extraer_cp4("1425") == "1425"


def test_letra_provincia():
    assert argentina.postal.letra_provincia("C1425ABC") == "C"


def test_provincia_por_cpa():
    assert argentina.postal.provincia_por_cpa("C1425ABC") == "Ciudad Autónoma de Buenos Aires"
    assert argentina.postal.provincia_por_cpa("X5000AAA") == "Córdoba"


def test_validar_cpa_provincia():
    assert argentina.postal.validar_cpa_provincia("X5000AAA", "Córdoba") is True
    assert argentina.postal.validar_cpa_provincia("X5000AAA", "Buenos Aires") is False
