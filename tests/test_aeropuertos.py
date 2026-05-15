import argentina as arg


def test_listar():
    assert len(arg.aeropuertos.listar()) >= 30


def test_lookup_iata():
    a = arg.aeropuertos.lookup("EZE")
    assert a is not None
    assert a.icao == "SAEZ"
    assert a.tipo == "internacional"


def test_lookup_iata_case_insensitive():
    a = arg.aeropuertos.lookup("aep")
    assert a is not None
    assert a.iata == "AEP"


def test_lookup_icao():
    a = arg.aeropuertos.lookup("SAWH")
    assert a is not None
    assert a.iata == "USH"
    assert "Ushuaia" in a.ciudad


def test_lookup_ciudad():
    a = arg.aeropuertos.lookup("Bariloche")
    assert a is not None
    assert a.iata == "BRC"


def test_lookup_nombre_parcial():
    a = arg.aeropuertos.lookup("Iguazú")
    assert a is not None
    assert a.iata == "IGR"


def test_lookup_inexistente():
    assert arg.aeropuertos.lookup("ZZZ") is None
    assert arg.aeropuertos.lookup(None) is None


def test_por_provincia():
    chubut = arg.aeropuertos.por_provincia("Chubut")
    iatas = [a.iata for a in chubut]
    assert "CRD" in iatas  # Comodoro Rivadavia
    assert "PMY" in iatas  # Puerto Madryn
    assert "REL" in iatas  # Trelew


def test_por_provincia_alias():
    caba = arg.aeropuertos.por_provincia("CABA")
    iatas = [a.iata for a in caba]
    assert "AEP" in iatas


def test_internacionales():
    inter = arg.aeropuertos.internacionales()
    iatas = {a.iata for a in inter}
    assert "EZE" in iatas
    assert "COR" in iatas
    assert "USH" in iatas
    # Todos deben ser internacionales
    for a in inter:
        assert a.tipo == "internacional"


def test_cabotaje():
    cab = arg.aeropuertos.cabotaje()
    iatas = {a.iata for a in cab}
    assert "AEP" in iatas  # Aeroparque es cabotaje
    for a in cab:
        assert a.tipo == "cabotaje"


def test_coordenadas_validas():
    eze = arg.aeropuertos.lookup("EZE")
    # Lat de Ezeiza ≈ -34.82, Lon ≈ -58.54
    assert -35 < eze.lat < -34
    assert -59 < eze.lon < -58


def test_iterable():
    iatas = [a.iata for a in arg.aeropuertos]
    assert "EZE" in iatas
