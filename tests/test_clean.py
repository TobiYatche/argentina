import argentina


def test_quitar_tildes():
    assert argentina.clean.quitar_tildes("Córdoba") == "Cordoba"


def test_normalizar_texto():
    assert argentina.clean.normalizar_texto("  Código   de Provincia ") == "codigo de provincia"


def test_snake_case():
    assert argentina.clean.snake_case("Código de Provincia") == "codigo_de_provincia"


def test_snake_case_con_signos():
    assert argentina.clean.snake_case("Edad (años)") == "edad_anos"


def test_snake_case_none():
    assert argentina.clean.snake_case(None) is None


def test_limpiar_columnas():
    try:
        import pandas as pd
    except ImportError:
        return

    df = pd.DataFrame({
        "Código de Provincia": [6],
        "Edad (años)": [30],
    })

    result = argentina.clean.limpiar_columnas(df)

    assert list(result.columns) == [
        "codigo_de_provincia",
        "edad_anos",
    ]


def test_porcentaje_nulls():
    try:
        import pandas as pd
    except ImportError:
        return

    df = pd.DataFrame({
        "a": [1, None],
        "b": [None, None],
    })

    result = argentina.clean.porcentaje_nulls(df)

    assert result["a"] == 50.0
    assert result["b"] == 100.0
