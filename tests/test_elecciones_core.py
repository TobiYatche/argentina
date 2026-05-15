import argentina as arg


def test_limpiar_mesa():
    assert arg.elecciones.limpiar_mesa("Mesa 01234") == "01234"


def test_limpiar_mesa_none():
    assert arg.elecciones.limpiar_mesa(None) is None


def test_limpiar_mesa_sin_digitos():
    assert arg.elecciones.limpiar_mesa("abc") is None


def test_limpiar_circuito():
    assert arg.elecciones.limpiar_circuito(" 12-A ") == "12A"


def test_limpiar_circuito_none():
    assert arg.elecciones.limpiar_circuito(None) is None


def test_normalizar_categoria_presidente():
    assert arg.elecciones.normalizar_categoria("Presidente") == "Presidente"


def test_normalizar_categoria_diputados():
    assert arg.elecciones.normalizar_categoria("diputado") == "Diputados"
    assert arg.elecciones.normalizar_categoria("diputados") == "Diputados"


def test_normalizar_categoria_desconocida():
    assert arg.elecciones.normalizar_categoria("concejal") is None


def test_normalizar_tipo_eleccion_paso():
    assert arg.elecciones.normalizar_tipo_eleccion("PASO") == "PASO"
    assert arg.elecciones.normalizar_tipo_eleccion("primarias") == "PASO"


def test_normalizar_tipo_eleccion_general():
    assert arg.elecciones.normalizar_tipo_eleccion("general") == "General"


def test_normalizar_tipo_eleccion_ballotage():
    assert arg.elecciones.normalizar_tipo_eleccion("segunda vuelta") == "Ballotage"


def test_validar_anio_eleccion_valido():
    assert arg.elecciones.validar_anio_eleccion(2023) is True
    assert arg.elecciones.validar_anio_eleccion("1983") is True


def test_validar_anio_eleccion_fuera_de_rango():
    assert arg.elecciones.validar_anio_eleccion(1982) is False
    assert arg.elecciones.validar_anio_eleccion(2101) is False


def test_validar_anio_eleccion_invalido():
    assert arg.elecciones.validar_anio_eleccion(None) is False
    assert arg.elecciones.validar_anio_eleccion("dos mil") is False
