import argentina


def test_limpiar_dni():
    assert argentina.personas.limpiar_dni("12.345.678") == "12345678"


def test_limpiar_dni_con_espacios():
    assert argentina.personas.limpiar_dni(" 12 345 678 ") == "12345678"


def test_limpiar_dni_none():
    assert argentina.personas.limpiar_dni(None) is None


def test_validar_dni_valido_8_digitos():
    assert argentina.personas.validar_dni("12.345.678") is True


def test_validar_dni_valido_7_digitos():
    assert argentina.personas.validar_dni("1.234.567") is True


def test_validar_dni_invalido():
    assert argentina.personas.validar_dni("123") is False


def test_limpiar_cuit():
    assert argentina.personas.limpiar_cuit("20-12345678-3") == "20123456783"


def test_validar_cuit():
    # CUIT con dígito verificador correcto
    assert argentina.personas.validar_cuit("20-12345678-6") is True


def test_validar_cuit_invalido():
    assert argentina.personas.validar_cuit("20-123") is False


def test_validar_cuit_solo_largo_back_compat():
    # Comportamiento previo (solo largo) sigue accesible con digito=False
    assert argentina.personas.validar_cuit(
        "20-12345678-3", digito=False
    ) is True


def test_extraer_dni_de_cuit():
    assert argentina.personas.extraer_dni_de_cuit("20-12345678-3") == "12345678"


def test_extraer_dni_de_cuit_invalido():
    assert argentina.personas.extraer_dni_de_cuit("20-123") is None


def test_normalizar_nombre():
    assert argentina.personas.normalizar_nombre(" María   Laura ") == "maria laura"


def test_primer_nombre():
    assert argentina.personas.primer_nombre("María Laura") == "maria"


def test_apellido_principal():
    assert argentina.personas.apellido_principal("Pérez Gómez") == "perez"


def test_serie_nacimientos_no_vacia():
    serie = argentina.personas.serie_nacimientos()
    assert len(serie) > 100
    assert all(isinstance(a, int) and isinstance(n, int) for a, n in serie)


def test_serie_nacimientos_cubre_periodo_esperado():
    serie = argentina.personas.serie_nacimientos()
    años = [a for a, _ in serie]
    assert min(años) == 1914
    assert max(años) >= 2024


def test_serie_nacimientos_valores_razonables():
    serie = dict(argentina.personas.serie_nacimientos())
    # En 2000 hubo ~700k nacimientos según DEIS
    assert 650_000 < serie[2000] < 750_000
    # En 1980 ~700k
    assert 650_000 < serie[1980] < 750_000


def test_estimar_año_nacimiento_dni_moderno():
    # DNI 50M ≈ nacido alrededor de 2010 según modelo lineal calibrado
    año = argentina.personas.estimar_año_nacimiento(50_000_000)
    assert año is not None
    assert 2008 <= año <= 2012


def test_estimar_año_nacimiento_consistente_con_formula_viral():
    # La fórmula viral en Reddit/X dice: año = 1942.5 + DNI/736470
    # Nuestro modelo está calibrado contra el mismo hito y debe coincidir ±1 año
    for dni in [10_000_000, 20_000_000, 30_000_000, 40_000_000, 50_000_000]:
        esperado = int(1942.5 + dni / 736_470)
        obtenido = argentina.personas.estimar_año_nacimiento(dni)
        assert abs(obtenido - esperado) <= 1


def test_estimar_año_nacimiento_acepta_string_y_int():
    assert argentina.personas.estimar_año_nacimiento("30.000.000") == \
        argentina.personas.estimar_año_nacimiento(30_000_000)


def test_estimar_año_nacimiento_dni_invalido():
    assert argentina.personas.estimar_año_nacimiento("abc") is None
    assert argentina.personas.estimar_año_nacimiento(None) is None
    assert argentina.personas.estimar_año_nacimiento("123") is None


def test_estimar_año_nacimiento_franja_cuit_extranjero():
    # 60.000.000–69.999.999 reservada para CUIT/CUIL provisorios de extranjeros
    # (Disposición Renaper 4678/2019). No es DNI personal.
    assert argentina.personas.estimar_año_nacimiento(60_000_000) is None
    assert argentina.personas.estimar_año_nacimiento(65_000_000) is None
    assert argentina.personas.estimar_año_nacimiento(69_999_999) is None


def test_estimar_año_nacimiento_post_salto():
    # En septiembre 2023 saltaron a 70M; los recién nacidos tienen 70M+
    año = argentina.personas.estimar_año_nacimiento(70_500_000)
    assert año is not None
    assert año >= 2023


def test_estimar_año_nacimiento_fuera_de_rango():
    # Muy por encima del último DNI emitido
    assert argentina.personas.estimar_año_nacimiento(99_999_999) is None


def test_estimar_dni_año_moderno():
    # 1990 → DNI alrededor de 35M según modelo lineal
    dni = argentina.personas.estimar_dni(1990)
    assert dni is not None
    assert 34_000_000 < dni < 37_000_000


def test_estimar_dni_año_reciente_post_salto():
    # Año posterior al salto → DNI debe estar en 70M+
    dni = argentina.personas.estimar_dni(2024)
    assert dni is not None
    assert dni >= 70_000_000


def test_estimar_dni_fuera_de_rango():
    assert argentina.personas.estimar_dni(1800) is None
    assert argentina.personas.estimar_dni(2100) is None
    assert argentina.personas.estimar_dni(None) is None


def test_rango_dni_de_año():
    rango = argentina.personas.rango_dni_de_año(2000)
    assert rango is not None
    inicio, fin = rango
    assert inicio < fin
    # El ancho refleja la pendiente del modelo (~736k DNI/año)
    assert 700_000 < (fin - inicio + 1) < 800_000


def test_rango_dni_de_año_consistente_con_estimar():
    # DNI tomado del rango de un año debe estimar ese mismo año
    año_objetivo = 1995
    rango = argentina.personas.rango_dni_de_año(año_objetivo)
    assert rango is not None
    inicio, fin = rango
    medio = (inicio + fin) // 2
    assert argentina.personas.estimar_año_nacimiento(medio) == año_objetivo


def test_rango_dni_de_año_fuera():
    assert argentina.personas.rango_dni_de_año(1800) is None
    assert argentina.personas.rango_dni_de_año(None) is None


def test_roundtrip_dni_año_moderno():
    dni_original = 38_500_000
    año = argentina.personas.estimar_año_nacimiento(dni_original)
    dni_estimado = argentina.personas.estimar_dni(año)
    assert abs(dni_estimado - dni_original) < 750_000  # ~1 año de DNIs


def test_calibracion_contra_hito_publico():
    # El último DNI 59.999.999 se entregó alrededor de agosto 2023
    año = argentina.personas.estimar_año_nacimiento(59_999_999)
    assert año == 2023


def test_calibracion_dni_70M_es_2023():
    # 70.000.000 fue el primer DNI post-salto, asignado septiembre 2023
    año = argentina.personas.estimar_año_nacimiento(70_000_001)
    assert año == 2023


def test_calibracion_dni_72M_es_2026():
    # Sanity check temporal: si la pendiente es ~736k/año, el DNI 72M
    # corresponde a ~2 años después del salto (sept 2023) = ~2026.
    # En mayo 2026 el RENAPER debería estar entregando ~72M.
    año = argentina.personas.estimar_año_nacimiento(72_000_000)
    assert año == 2026
