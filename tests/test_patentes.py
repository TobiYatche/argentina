import argentina as arg


def test_limpiar():
    assert arg.patentes.limpiar(" abc 123 ") == "ABC123"
    assert arg.patentes.limpiar("AB-123-CD") == "AB123CD"
    assert arg.patentes.limpiar(None) is None
    assert arg.patentes.limpiar("  ") is None


def test_vieja():
    assert arg.patentes.tipo("ABC 123") == "vieja"
    assert arg.patentes.validar("ABC123") is True
    assert arg.patentes.formatear("abc123") == "ABC 123"


def test_mercosur():
    assert arg.patentes.tipo("AB 123 CD") == "mercosur"
    assert arg.patentes.es_mercosur("AB123CD") is True
    assert arg.patentes.formatear("ab123cd") == "AB 123 CD"


def test_moto_vieja():
    assert arg.patentes.tipo("123 ABC") == "moto_vieja"
    assert arg.patentes.es_moto("123ABC") is True
    assert arg.patentes.formatear("123abc") == "123 ABC"


def test_moto_mercosur():
    assert arg.patentes.tipo("A999BBB") == "moto_mercosur"
    assert arg.patentes.es_moto("A999BBB") is True
    assert arg.patentes.es_mercosur("A999BBB") is True
    assert arg.patentes.formatear("a999bbb") == "A 999 BBB"


def test_invalidos():
    for v in ["pepe", "", None, "1234", "AAAA1234", "12 34"]:
        assert arg.patentes.tipo(v) is None
        assert arg.patentes.validar(v) is False
        assert arg.patentes.formatear(v) is None
