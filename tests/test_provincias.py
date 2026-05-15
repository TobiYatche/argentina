import argentina


def test_lookup_cordoba():
    p = argentina.provincias.lookup("Córdoba")
    assert p is not None
    assert p.nombre == "Córdoba"
    assert p.codigo_indec == "14"
    assert p.iso_id == "AR-X"


def test_lookup_cordoba_sin_tilde():
    p = argentina.provincias.lookup("cordoba")
    assert p is not None
    assert p.nombre == "Córdoba"


def test_lookup_codigo_indec():
    p = argentina.provincias.lookup("14")
    assert p is not None
    assert p.nombre == "Córdoba"


def test_lookup_iso():
    p = argentina.provincias.lookup("AR-X")
    assert p is not None
    assert p.nombre == "Córdoba"


def test_lookup_pba():
    p = argentina.provincias.lookup("PBA")
    assert p is not None
    assert p.nombre == "Buenos Aires"


def test_lookup_caba():
    p = argentina.provincias.lookup("CABA")
    assert p is not None
    assert p.nombre == "Ciudad Autónoma de Buenos Aires"


def test_constante_buenos_aires():
    assert argentina.provincias.BUENOS_AIRES.codigo_indec == "06"


def test_constante_cordoba():
    assert argentina.provincias.CORDOBA.iso_id == "AR-X"


def test_caba_alias_mismo_objeto():
    assert argentina.provincias.CABA is argentina.provincias.CIUDAD_AUTONOMA_DE_BUENOS_AIRES


def test_listar():
    provincias = argentina.provincias.listar()
    assert len(provincias) == 24
    assert argentina.provincias.BUENOS_AIRES in provincias
