import argentina as arg


def test_superficie():
    assert arg.provincias.CORDOBA.superficie_km2 == 165321
    assert arg.provincias.BUENOS_AIRES.superficie_km2 == 307571
    assert arg.provincias.CABA.superficie_km2 == 203


def test_densidad_caba():
    # CABA: ~3.1M habitantes / 203 km² → ~15.000 hab/km²
    d = arg.provincias.CABA.densidad_2022
    assert 14000 < d < 17000


def test_densidad_santa_cruz():
    # Santa Cruz: muy baja
    d = arg.provincias.SANTA_CRUZ.densidad_2022
    assert 0.5 < d < 2.5


def test_densidad_ranking():
    top = sorted(arg.provincias, key=lambda p: p.densidad_2022 or 0, reverse=True)
    # CABA siempre primera por mucho
    assert top[0].nombre == "Ciudad Autónoma de Buenos Aires"
    # Santa Cruz última o muy baja
    assert top[-1].nombre == "Santa Cruz"


def test_todas_tienen_superficie():
    for p in arg.provincias:
        assert p.superficie_km2 is not None
        assert p.superficie_km2 > 0
