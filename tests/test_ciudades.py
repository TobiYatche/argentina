import argentina as arg


def test_lookup_caba():
    c = arg.ciudades.lookup("Buenos Aires")
    assert c is not None
    assert c.provincia_codigo == "02"
    assert c.poblacion_2022 == 3121707


def test_lookup_caba_alias():
    c = arg.ciudades.lookup("CABA")
    assert c is not None
    assert c.nombre == "Buenos Aires"


def test_lookup_sin_tilde():
    c = arg.ciudades.lookup("cordoba")
    assert c is not None
    assert c.nombre == "Córdoba"


def test_lookup_inexistente():
    assert arg.ciudades.lookup("Atlantis") is None
    assert arg.ciudades.lookup(None) is None
    assert arg.ciudades.lookup("") is None


def test_alias_mardel():
    c = arg.ciudades.lookup("mardel")
    assert c is not None
    assert c.nombre == "Mar del Plata"


def test_por_provincia():
    ciudades_ba = arg.ciudades.por_provincia("Buenos Aires")
    nombres = [c.nombre for c in ciudades_ba]
    assert "La Plata" in nombres
    assert "Mar del Plata" in nombres
    assert "Bahía Blanca" in nombres


def test_por_provincia_con_alias():
    ciudades_caba = arg.ciudades.por_provincia("CABA")
    assert len(ciudades_caba) == 1
    assert ciudades_caba[0].nombre == "Buenos Aires"


def test_top():
    top3 = arg.ciudades.top(3)
    assert len(top3) == 3
    # La más grande debe ser Buenos Aires
    assert top3[0].nombre == "Buenos Aires"
    # Y deben estar ordenadas por población descendente
    assert top3[0].poblacion_2022 > top3[1].poblacion_2022 > top3[2].poblacion_2022


def test_listar():
    todas = arg.ciudades.listar()
    assert len(todas) >= 30


def test_modulo_iterable():
    nombres = [c.nombre for c in arg.ciudades]
    assert "Buenos Aires" in nombres
    assert len(arg.ciudades) == len(arg.ciudades.listar())


def test_contains():
    assert "CABA" in arg.ciudades
    assert "Rosario" in arg.ciudades
    assert "Atlantis" not in arg.ciudades


def test_provincia_poblacion_2022():
    # Buenos Aires sigue siendo la provincia más poblada
    assert arg.provincias.BUENOS_AIRES.poblacion_2022 == 17569053
    assert arg.provincias.CORDOBA.poblacion_2022 == 3840905
