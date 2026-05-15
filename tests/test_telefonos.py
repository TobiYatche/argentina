import argentina as arg


def test_limpiar():
    assert arg.telefonos.limpiar("+54 9 11 1234-5678") == "5491112345678"


def test_validar_celular_amba():
    assert arg.telefonos.validar("+54 9 11 1234-5678") is True


def test_validar_fijo_amba():
    assert arg.telefonos.validar("011 4321-1234") is True


def test_validar_invalido():
    assert arg.telefonos.validar("123") is False


def test_extraer_caracteristica_amba():
    assert arg.telefonos.extraer_caracteristica("+54 9 11 1234-5678") == "11"


def test_extraer_caracteristica_cordoba():
    assert arg.telefonos.extraer_caracteristica("+54 9 351 1234567") == "351"


def test_es_celular_con_9():
    assert arg.telefonos.es_celular("+54 9 11 1234-5678") is True


def test_es_celular_con_15():
    assert arg.telefonos.es_celular("011 15 1234-5678") is True


def test_normalizar_e164_celular():
    assert arg.telefonos.normalizar_e164("+54 9 11 1234-5678") == "+5491112345678"


def test_normalizar_e164_fijo():
    assert arg.telefonos.normalizar_e164("011 4321-1234") == "+541143211234"


def test_normalizar_e164_forzar_celular():
    assert arg.telefonos.normalizar_e164("11 1234-5678", celular=True) == "+5491112345678"
