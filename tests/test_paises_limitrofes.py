import argentina as arg


def test_listar():
    assert len(arg.paises_limitrofes) == 5


def test_lookup_iso():
    p = arg.paises_limitrofes.lookup("CL")
    assert p is not None
    assert p.nombre == "Chile"


def test_lookup_iso3():
    p = arg.paises_limitrofes.lookup("BRA")
    assert p is not None
    assert p.nombre == "Brasil"


def test_lookup_nombre():
    p = arg.paises_limitrofes.lookup("Uruguay")
    assert p is not None
    assert p.codigo_iso == "UY"


def test_lookup_case_insensitive():
    assert arg.paises_limitrofes.lookup("chile") == arg.paises_limitrofes.lookup("CL")


def test_por_provincia():
    # Mendoza solo limita con Chile
    pais = arg.paises_limitrofes.por_provincia("Mendoza")
    assert len(pais) == 1
    assert pais[0].nombre == "Chile"


def test_por_provincia_jujuy():
    # Jujuy limita con Chile y Bolivia
    pais = arg.paises_limitrofes.por_provincia("Jujuy")
    nombres = {p.nombre for p in pais}
    assert nombres == {"Chile", "Bolivia"}


def test_por_provincia_alias():
    # PBA limita solo con Uruguay (Río de la Plata)
    pais = arg.paises_limitrofes.por_provincia("PBA")
    assert len(pais) == 1
    assert pais[0].nombre == "Uruguay"


def test_chile_es_la_frontera_mas_larga():
    chile = arg.paises_limitrofes.lookup("CL")
    longitudes = sorted([p.frontera_km for p in arg.paises_limitrofes], reverse=True)
    assert chile.frontera_km == longitudes[0]


def test_iterable():
    nombres = [p.nombre for p in arg.paises_limitrofes]
    assert set(nombres) == {"Brasil", "Bolivia", "Chile", "Paraguay", "Uruguay"}
