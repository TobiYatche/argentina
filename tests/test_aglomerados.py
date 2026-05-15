import argentina as arg


def test_listar():
    assert len(arg.aglomerados.listar()) >= 31


def test_lookup_codigo():
    a = arg.aglomerados.lookup(32)
    assert a is not None
    assert "Buenos Aires" in a.nombre


def test_lookup_codigo_string():
    a = arg.aglomerados.lookup("13")
    assert a is not None
    assert "Córdoba" in a.nombre


def test_lookup_nombre():
    a = arg.aglomerados.lookup("Mar del Plata")
    assert a is not None
    assert a.codigo == 34


def test_lookup_parcial():
    # "córdoba" → debería matchear "Gran Córdoba"
    a = arg.aglomerados.lookup("córdoba")
    assert a is not None
    assert "Córdoba" in a.nombre


def test_lookup_inexistente():
    assert arg.aglomerados.lookup(999) is None
    assert arg.aglomerados.lookup("Atlantis") is None
    assert arg.aglomerados.lookup(None) is None


def test_por_provincia():
    ba = arg.aglomerados.por_provincia("Buenos Aires")
    nombres = [a.nombre for a in ba]
    assert "Gran La Plata" in nombres
    assert "Mar del Plata" in nombres
    assert "Partidos del GBA" in nombres


def test_por_provincia_alias():
    caba = arg.aglomerados.por_provincia("CABA")
    assert len(caba) >= 1
    assert "Ciudad de Buenos Aires" in [a.nombre for a in caba]


def test_iterable():
    nombres = [a.nombre for a in arg.aglomerados]
    assert "Gran Mendoza" in nombres
    assert "Posadas" in nombres


def test_modulo_contains():
    assert 32 in arg.aglomerados
    assert 9999 not in arg.aglomerados
