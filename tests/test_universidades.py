import argentina as arg


def test_listar():
    assert len(arg.universidades.listar()) >= 50


def test_lookup_sigla():
    u = arg.universidades.lookup("UBA")
    assert u is not None
    assert u.nombre == "Universidad de Buenos Aires"
    assert u.provincia_codigo == "02"


def test_lookup_sigla_case_insensitive():
    u = arg.universidades.lookup("unc")
    assert u is not None
    assert u.sigla == "UNC"


def test_lookup_nombre_completo():
    u = arg.universidades.lookup("Universidad Nacional de Córdoba")
    assert u is not None
    assert u.sigla == "UNC"


def test_lookup_nombre_parcial():
    u = arg.universidades.lookup("La Plata")
    assert u is not None
    assert u.sigla == "UNLP"


def test_lookup_inexistente():
    assert arg.universidades.lookup("UNX") is None
    assert arg.universidades.lookup(None) is None
    assert arg.universidades.lookup("") is None


def test_por_provincia():
    cordoba = arg.universidades.por_provincia("Córdoba")
    siglas = [u.sigla for u in cordoba]
    assert "UNC" in siglas
    assert "UNRC" in siglas
    assert "UNVM" in siglas


def test_por_provincia_alias():
    caba = arg.universidades.por_provincia("CABA")
    siglas = [u.sigla for u in caba]
    assert "UBA" in siglas
    assert "UTN" in siglas


def test_por_anio_rango():
    nuevas = arg.universidades.por_anio(desde=2009)
    for u in nuevas:
        assert u.anio_fundacion >= 2009
    # Hay varias en/después de 2009
    assert len(nuevas) >= 6


def test_por_anio_solo_hasta():
    antiguas = arg.universidades.por_anio(hasta=1900)
    siglas = {u.sigla for u in antiguas}
    assert "UBA" in siglas       # 1821
    assert "UNC" in siglas       # 1613
    assert "UNLP" not in siglas  # 1905


def test_iterable():
    siglas = [u.sigla for u in arg.universidades]
    assert "UBA" in siglas
    assert len(arg.universidades) == len(arg.universidades.listar())


def test_contains():
    assert "UBA" in arg.universidades
    assert "UNX" not in arg.universidades
