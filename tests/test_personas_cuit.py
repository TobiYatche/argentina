import argentina as arg


def test_calcular_digito_cuit():
    assert arg.personas.calcular_digito_cuit("2012345678") == "6"


def test_validar_cuit_con_digito_valido():
    assert arg.personas.validar_cuit("20-12345678-6") is True


def test_validar_cuit_con_digito_invalido():
    assert arg.personas.validar_cuit("20-12345678-3") is False


def test_validar_cuit_solo_largo():
    assert arg.personas.validar_cuit(
        "20-12345678-3",
        digito=False,
    ) is True


def test_tipo_cuit_persona_fisica():
    assert (
        arg.personas.tipo_cuit("20-12345678-6")
        == "persona_fisica"
    )


def test_tipo_cuit_persona_juridica():
    assert (
        arg.personas.tipo_cuit("30-12345678-1")
        == "persona_juridica"
    )


def test_formatear_dni():
    assert arg.personas.formatear_dni("12345678") == "12.345.678"


def test_formatear_dni_invalido():
    assert arg.personas.formatear_dni("123") is None


def test_formatear_cuit():
    assert (
        arg.personas.formatear_cuit("20123456786")
        == "20-12345678-6"
    )
