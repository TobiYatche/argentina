import argentina as arg


def test_normalizar():
    assert (
        arg.direcciones.normalizar(
            " Av. Santa Fe 3253  Piso 2 Depto B "
        )
        == "av santa fe 3253 piso 2 depto b"
    )


def test_extraer_altura():
    assert arg.direcciones.extraer_altura("Av. Santa Fe 3253") == "3253"


def test_extraer_calle():
    assert arg.direcciones.extraer_calle("Av. Santa Fe 3253") == "av santa fe"


def test_extraer_piso():
    assert (
        arg.direcciones.extraer_piso(
            "Av. Santa Fe 3253 Piso 2 Depto B"
        )
        == "2"
    )


def test_extraer_departamento():
    assert (
        arg.direcciones.extraer_departamento(
            "Av. Santa Fe 3253 Piso 2 Depto B"
        )
        == "B"
    )


def test_tiene_altura():
    assert arg.direcciones.tiene_altura("Av. Santa Fe 3253") is True
    assert arg.direcciones.tiene_altura("Av. Santa Fe") is False


def test_parsear():
    parsed = arg.direcciones.parsear(
        "Av. Santa Fe 3253 Piso 2 Depto B"
    )

    assert parsed["calle"] == "av santa fe"
    assert parsed["altura"] == "3253"
    assert parsed["piso"] == "2"
    assert parsed["departamento"] == "B"
    assert parsed["tiene_altura"] is True
