import argentina as arg


def test_normalizar_sexo_femenino():
    assert arg.salud.normalizar_sexo("femenino") == "F"


def test_normalizar_sexo_varon():
    assert arg.salud.normalizar_sexo("varón") == "M"


def test_normalizar_sexo_x():
    assert arg.salud.normalizar_sexo("no binario") == "X"


def test_normalizar_sexo_none():
    assert arg.salud.normalizar_sexo(None) is None


def test_normalizar_tipo_documento_dni():
    assert arg.salud.normalizar_tipo_documento("dni") == "DNI"


def test_normalizar_tipo_documento_pasaporte():
    assert arg.salud.normalizar_tipo_documento("pasaporte") == "PASAPORTE"


def test_limpiar_matricula():
    assert arg.salud.limpiar_matricula("M.P. 12345") == "MP12345"


def test_grupo_etario_menor_1():
    assert arg.salud.grupo_etario(0.5) == "0"


def test_grupo_etario_3():
    assert arg.salud.grupo_etario(3) == "1-4"


def test_grupo_etario_70():
    assert arg.salud.grupo_etario(70) == "65+"


def test_grupo_etario_invalido():
    assert arg.salud.grupo_etario(-1) is None


def test_edad_en_anios():
    assert arg.salud.edad_en_anios(
        "2015-05-10",
        "2026-05-12",
    ) == 11


def test_edad_en_anios_antes_de_cumple():
    assert arg.salud.edad_en_anios(
        "2015-12-10",
        "2026-05-12",
    ) == 10


def test_edad_en_anios_fecha_invalida():
    assert arg.salud.edad_en_anios(
        "fecha mala",
        "2026-05-12",
    ) is None
