import argentina


def test_lookup_codigo():
    # 06427 = La Matanza (Buenos Aires). Código INDEC oficial vía IGN.
    d = argentina.departamentos.lookup("06427")

    assert d is not None
    assert d.nombre == "La Matanza"
    assert d.provincia_nombre == "Buenos Aires"


def test_lookup_nombre_unico():
    d = argentina.departamentos.lookup("Rosario")

    assert d is not None
    assert d.codigo_departamento == "82084"


def test_lookup_nombre_duplicado():
    # "Capital" se repite en muchas provincias → ambiguo
    d = argentina.departamentos.lookup("Capital")

    assert d is None


def test_por_provincia_nombre():
    departamentos = argentina.departamentos.por_provincia(
        "Buenos Aires"
    )

    nombres = [d.nombre for d in departamentos]

    assert "La Matanza" in nombres
    assert "Avellaneda" in nombres


def test_por_provincia_codigo():
    departamentos = argentina.departamentos.por_provincia("14")

    nombres = [d.nombre for d in departamentos]

    assert "Capital" in nombres
    assert "Río Cuarto" in nombres


def test_listar():
    departamentos = argentina.departamentos.listar()

    # Set completo de departamentos del país (IGN)
    assert len(departamentos) >= 500
