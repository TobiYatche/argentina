import argentina as arg


def test_identificar_cuit():
    r = arg.identificar("20-12345678-6")
    assert r is not None
    assert r["tipo"] == "cuit"
    assert r["tipo_persona"] == "persona_fisica"
    assert r["dni"] == "12345678"


def test_identificar_cuit_invalido_dv():
    # El dígito 3 no es el correcto para 2012345678, pero igual lo detecta como CUIT
    r = arg.identificar("20-12345678-3")
    assert r["tipo"] == "cuit"
    assert r["valido_dv"] is False


def test_identificar_cbu():
    # CBU válido (Macro 285)
    r = arg.identificar("2850590940090418135201")
    assert r["tipo"] == "cbu"
    assert r["banco"] == "Banco Macro"
    assert r["codigo_banco"] == "285"


def test_identificar_cpa():
    r = arg.identificar("C1425ABC")
    assert r["tipo"] == "cpa"
    assert r["cp4"] == "1425"
    assert "Buenos Aires" in r["provincia"]


def test_identificar_cp4():
    r = arg.identificar("1425")
    assert r["tipo"] == "cp4"
    assert r["valor"] == "1425"


def test_identificar_telefono():
    r = arg.identificar("+54 9 351 1234567")
    assert r["tipo"] == "telefono"
    assert r["celular"] is True
    assert r["caracteristica"] == "351"
    assert r["provincia"] == "Córdoba"


def test_identificar_patente_mercosur():
    r = arg.identificar("AB 123 CD")
    assert r["tipo"] == "patente"
    assert r["subtipo"] == "mercosur"
    assert r["es_mercosur"] is True


def test_identificar_patente_vieja():
    r = arg.identificar("ABC 123")
    assert r["tipo"] == "patente"
    assert r["subtipo"] == "vieja"


def test_identificar_departamento():
    r = arg.identificar("06427")  # La Matanza
    assert r["tipo"] == "departamento"
    assert r["nombre"] == "La Matanza"


def test_identificar_provincia():
    r = arg.identificar("Córdoba")
    # "Córdoba" matchea ciudad antes que provincia (Córdoba es ciudad capital)
    assert r["tipo"] in {"ciudad", "provincia"}


def test_identificar_provincia_por_iso():
    r = arg.identificar("AR-X")
    assert r["tipo"] == "provincia"
    assert r["nombre"] == "Córdoba"


def test_identificar_provincia_alias():
    r = arg.identificar("PBA")
    assert r["tipo"] == "provincia"
    assert r["nombre"] == "Buenos Aires"


def test_identificar_ciudad():
    r = arg.identificar("Rosario")
    assert r["tipo"] == "ciudad"
    assert r["provincia"] == "Santa Fe"


def test_identificar_inexistente():
    assert arg.identificar("xyz inexistente 123") is None
    assert arg.identificar("") is None
    assert arg.identificar(None) is None


def test_identificar_dni():
    r = arg.identificar("12.345.678")
    assert r["tipo"] == "dni"
    assert r["valor"] == "12345678"
    assert r["formato"] == "12.345.678"
