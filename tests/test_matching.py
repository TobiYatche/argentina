"""Tests del módulo ``argentina.matching``.

Sin internet, sin archivos externos: los catálogos vienen del paquete.
"""

import argentina as arg


# ---------------------------------------------------------------------------
# API genérica: match() y candidatos()
# ---------------------------------------------------------------------------


def test_match_generica_exacto():
    res = arg.matching.match("Córdoba", ["Buenos Aires", "Córdoba", "Santa Fe"])
    assert res == ("Córdoba", 1.0)


def test_match_generica_typo():
    res = arg.matching.match("cordova", ["Buenos Aires", "Córdoba", "Santa Fe"])
    assert res is not None
    nombre, score = res
    assert nombre == "Córdoba"
    assert 0.7 <= score < 1.0


def test_match_generica_sin_tilde():
    res = arg.matching.match("cordoba", ["Buenos Aires", "Córdoba"])
    assert res is not None
    assert res[0] == "Córdoba"
    assert res[1] == 1.0  # diferente con tilde, igual normalizado


def test_match_generica_irrelevante():
    assert arg.matching.match("xyz", ["Buenos Aires", "Córdoba"]) is None


def test_match_generica_consulta_none():
    assert arg.matching.match(None, ["Buenos Aires"]) is None
    assert arg.matching.match("", ["Buenos Aires"]) is None


def test_match_generica_umbral_ajustable():
    # "abc" no llega al umbral default contra cualquiera de éstos.
    assert arg.matching.match("abc", ["Buenos Aires", "Córdoba"]) is None
    # Bajando muchísimo el umbral, devuelve el mejor que haya.
    res = arg.matching.match("abc", ["Buenos Aires", "Córdoba"], umbral=0.0)
    assert res is not None
    assert isinstance(res[1], float)


def test_candidatos_generica_ordenados_desc():
    res = arg.matching.candidatos(
        "cordova", ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza"], n=4
    )
    assert len(res) == 4
    scores = [s for _, s in res]
    assert scores == sorted(scores, reverse=True)
    assert res[0][0] == "Córdoba"


def test_candidatos_generica_n_limita_largo():
    res = arg.matching.candidatos(
        "cordova", ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza"], n=2
    )
    assert len(res) == 2


def test_candidatos_generica_filtra_por_umbral():
    res = arg.matching.candidatos(
        "cordova",
        ["Buenos Aires", "Córdoba", "Santa Fe"],
        umbral=0.8,
    )
    assert all(s >= 0.8 for _, s in res)
    assert any(nombre == "Córdoba" for nombre, _ in res)


# ---------------------------------------------------------------------------
# Provincias
# ---------------------------------------------------------------------------


def test_match_provincia_exacto_score_implicito_1():
    p = arg.matching.match_provincia("Córdoba")
    assert p is not None
    assert p.nombre == "Córdoba"


def test_match_provincia_typo_buennos_aires():
    p = arg.matching.match_provincia("buennos aires")
    assert p is not None
    assert p.nombre == "Buenos Aires"


def test_match_provincia_typo_cordova():
    p = arg.matching.match_provincia("cordova")
    assert p is not None
    assert p.nombre == "Córdoba"


def test_match_provincia_typo_mendosa():
    p = arg.matching.match_provincia("mendosa")
    assert p is not None
    assert p.nombre == "Mendoza"


def test_match_provincia_abreviatura_sgo_del_estero():
    # "sgo del estero" no es alias registrado en provincias.lookup, llega por fuzzy.
    assert arg.provincias.lookup("sgo del estero") is None
    p = arg.matching.match_provincia("sgo del estero")
    assert p is not None
    assert p.nombre == "Santiago del Estero"


def test_match_provincia_irrelevante_devuelve_none():
    assert arg.matching.match_provincia("xyz") is None
    assert arg.matching.match_provincia("asdf") is None


def test_match_provincia_none_y_vacio():
    assert arg.matching.match_provincia(None) is None
    assert arg.matching.match_provincia("") is None


def test_match_provincia_usa_lookup_para_alias():
    # PBA es alias en lookup → devuelve Buenos Aires directo sin fuzzy.
    p = arg.matching.match_provincia("PBA")
    assert p is not None
    assert p.nombre == "Buenos Aires"


def test_match_provincia_umbral_estricto_rechaza():
    # Con umbral alto, un typo flojo no llega.
    assert arg.matching.match_provincia("misisones", umbral=0.99) is None


def test_match_provincia_umbral_estricto_acepta_exacto():
    # Pero el exacto siempre pasa (va por lookup, sin fuzzy).
    assert arg.matching.match_provincia("Misiones", umbral=0.99) is not None


def test_candidatos_provincia_ordenados():
    res = arg.matching.candidatos_provincia("cordova", n=3)
    assert len(res) == 3
    scores = [s for _, s in res]
    assert scores == sorted(scores, reverse=True)
    assert res[0][0].nombre == "Córdoba"


def test_candidatos_provincia_n_limita_largo():
    res = arg.matching.candidatos_provincia("cordova", n=5)
    assert len(res) == 5


# ---------------------------------------------------------------------------
# Departamentos
# ---------------------------------------------------------------------------


def test_match_departamento_filtra_por_provincia():
    d = arg.matching.match_departamento(
        "gral san martin", provincia="Buenos Aires"
    )
    assert d is not None
    assert d.nombre == "General San Martín"
    assert d.provincia_codigo == "06"


def test_match_departamento_provincia_via_alias():
    d = arg.matching.match_departamento(
        "gral san martin", provincia="PBA"
    )
    assert d is not None
    assert d.provincia_codigo == "06"


def test_match_departamento_sin_provincia_intenta_lookup_exacto():
    # "Rosario" es alias en departamentos.lookup → match exacto sin fuzzy.
    d = arg.matching.match_departamento("rosario")
    assert d is not None
    assert d.nombre == "Rosario"


def test_match_departamento_provincia_inexistente():
    # Si la provincia no resuelve, devuelve None.
    assert (
        arg.matching.match_departamento("rosario", provincia="atlantis") is None
    )


def test_candidatos_departamento_filtra_por_provincia():
    res = arg.matching.candidatos_departamento(
        "san martin", provincia="Buenos Aires", n=5
    )
    assert len(res) <= 5
    # Todos los candidatos son de Buenos Aires.
    assert all(d.provincia_codigo == "06" for d, _ in res)


# ---------------------------------------------------------------------------
# Ciudades
# ---------------------------------------------------------------------------


def test_match_ciudad_exacto():
    c = arg.matching.match_ciudad("Rosario")
    assert c is not None
    assert c.nombre == "Rosario"


def test_match_ciudad_typo():
    c = arg.matching.match_ciudad("rosrio")
    assert c is not None
    assert c.nombre == "Rosario"


def test_match_ciudad_variante_mar_de_plata():
    c = arg.matching.match_ciudad("mar de plata")
    assert c is not None
    assert c.nombre == "Mar del Plata"


def test_match_ciudad_irrelevante():
    assert arg.matching.match_ciudad("xyz") is None


def test_candidatos_ciudad_ordenados():
    res = arg.matching.candidatos_ciudad("rosrio", n=3)
    assert len(res) == 3
    scores = [s for _, s in res]
    assert scores == sorted(scores, reverse=True)
    assert res[0][0].nombre == "Rosario"


# ---------------------------------------------------------------------------
# Universidades
# ---------------------------------------------------------------------------


def test_match_universidad_sigla_exacta():
    u = arg.matching.match_universidad("UBA")
    assert u is not None
    assert u.sigla == "UBA"


def test_match_universidad_typo_nombre():
    u = arg.matching.match_universidad("universidad d buenos aires")
    assert u is not None
    assert u.sigla == "UBA"


def test_match_universidad_irrelevante():
    assert arg.matching.match_universidad("xyz") is None


def test_candidatos_universidad_score_max_sigla_nombre():
    # "uba" matchea perfecto con la sigla → score 1.0 al tope.
    res = arg.matching.candidatos_universidad("uba", n=3)
    assert res[0][0].sigla == "UBA"
    assert res[0][1] == 1.0


# ---------------------------------------------------------------------------
# Aglomerados
# ---------------------------------------------------------------------------


def test_match_aglomerado_exacto_via_lookup():
    # "Gran Córdoba" se resuelve por lookup parcial existente.
    a = arg.matching.match_aglomerado("Gran Córdoba")
    assert a is not None
    assert "Córdoba" in a.nombre


def test_match_aglomerado_typo():
    a = arg.matching.match_aglomerado("Gran Cordova")
    assert a is not None
    assert "Córdoba" in a.nombre


def test_match_aglomerado_irrelevante():
    assert arg.matching.match_aglomerado("xyz") is None


# ---------------------------------------------------------------------------
# Comportamiento transversal
# ---------------------------------------------------------------------------


def test_modulo_expuesto_en_paquete():
    assert hasattr(arg, "matching")
    assert callable(arg.matching.match_provincia)


def test_umbral_default_publico():
    assert isinstance(arg.matching.UMBRAL_DEFAULT, float)
    assert 0.0 < arg.matching.UMBRAL_DEFAULT <= 1.0


def test_devuelve_mismos_objetos_que_lookup():
    # match_*() y lookup() exacto deben devolver el mismo Provincia.
    a = arg.matching.match_provincia("Córdoba")
    b = arg.provincias.lookup("Córdoba")
    assert a is b
