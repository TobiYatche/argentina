import argentina


def test_limpiar_cue():
    assert argentina.educacion.limpiar_cue("0201234-00") == "020123400"


def test_validar_cue():
    assert argentina.educacion.validar_cue("020123400") is True


def test_validar_cue_invalido():
    assert argentina.educacion.validar_cue("123") is False


def test_limpiar_cueanexo():
    assert argentina.educacion.limpiar_cueanexo("0201234-01") == "020123401"


def test_validar_cueanexo():
    assert argentina.educacion.validar_cueanexo("020123401") is True


def test_extraer_jurisdiccion_cue():
    assert (
        argentina.educacion.extraer_jurisdiccion_cue(
            "020123400"
        )
        == "Ciudad Autónoma de Buenos Aires"
    )


def test_normalizar_sector():
    assert (
        argentina.educacion.normalizar_sector(
            "público"
        )
        == "Estatal"
    )

    assert (
        argentina.educacion.normalizar_sector(
            "privado"
        )
        == "Privado"
    )


def test_normalizar_ambito():
    assert (
        argentina.educacion.normalizar_ambito(
            "urbano"
        )
        == "Urbano"
    )


def test_normalizar_nivel():
    assert (
        argentina.educacion.normalizar_nivel(
            "secundario"
        )
        == "Secundaria"
    )
