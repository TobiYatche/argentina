import argentina as arg


def test_bancos_bcra_alias():
    assert arg.bancos.BANCOS_BCRA is arg.bancos.BANCOS


def test_codigos_principales():
    # Bancos grandes deben estar
    assert "011" in arg.bancos.BANCOS  # Nación
    assert "285" in arg.bancos.BANCOS  # Macro
    assert "072" in arg.bancos.BANCOS  # Santander
    assert "007" in arg.bancos.BANCOS  # Galicia
    assert "017" in arg.bancos.BANCOS  # BBVA


def test_banco_por_codigo():
    assert arg.bancos.banco_por_codigo("011") == "Banco de la Nación Argentina"
    assert arg.bancos.banco_por_codigo("285") == "Banco Macro"
    assert arg.bancos.banco_por_codigo(11) == "Banco de la Nación Argentina"  # numérico, padded
    assert arg.bancos.banco_por_codigo("999") is None
    assert arg.bancos.banco_por_codigo(None) is None


def test_banco_de_cbu_alias():
    # banco_de_cbu es el mismo que banco_por_cbu
    assert arg.bancos.banco_de_cbu is arg.bancos.banco_por_cbu


def test_banco_de_cbu_real():
    # Macro: CBU empieza con 285
    cbu = "2850590940090418135201"
    assert arg.bancos.banco_de_cbu(cbu) == "Banco Macro"
