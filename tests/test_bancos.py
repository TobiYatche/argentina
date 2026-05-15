import argentina as arg


def test_limpiar_cbu():
    assert (
        arg.bancos.limpiar_cbu(
            "0170 0001 4000 0001 2345 67"
        )
        == "0170000140000001234567"
    )


def test_validar_cbu_valido():
    assert (
        arg.bancos.validar_cbu(
            "2850590940090418135201"
        )
        is True
    )


def test_validar_cbu_invalido():
    assert (
        arg.bancos.validar_cbu(
            "2850590940090418135202"
        )
        is False
    )


def test_formatear_cbu():
    assert (
        arg.bancos.formatear_cbu(
            "2850590940090418135201"
        )
        == "28505909-40090418135201"
    )


def test_codigo_banco_cbu():
    assert (
        arg.bancos.codigo_banco_cbu(
            "0170099120000067797370"
        )
        == "017"
    )


def test_banco_por_cbu():
    assert (
        arg.bancos.banco_por_cbu(
            "0170099120000067797370"
        )
        == "BBVA Argentina"
    )


def test_limpiar_alias():
    assert (
        arg.bancos.limpiar_alias(
            " Mi.Alias.CBU "
        )
        == "MI.ALIAS.CBU"
    )


def test_validar_alias():
    assert (
        arg.bancos.validar_alias(
            "MI.ALIAS.CBU"
        )
        is True
    )


def test_validar_alias_invalido():
    assert (
        arg.bancos.validar_alias(
            "A"
        )
        is False
    )


def test_validar_cvu():
    assert (
        arg.bancos.validar_cvu(
            "0000003100000000000001"
        )
        is True
    )
