"""Tests del sprint 0.3.0: mapping, extraer_de_texto, generadores, fuzzy lookup."""

import random

import argentina as arg


# === 1. mapping(a, b) ===

def test_mapping_provincias():
    m = arg.provincias.mapping("codigo_indec", "nombre")
    assert m["14"] == "Córdoba"
    assert m["02"] == "Ciudad Autónoma de Buenos Aires"
    assert len(m) == 24


def test_mapping_provincias_iso_nombre():
    m = arg.provincias.mapping("iso_id", "nombre")
    assert m["AR-X"] == "Córdoba"


def test_mapping_ciudades_poblacion():
    m = arg.ciudades.mapping("nombre", "poblacion_2022")
    assert m["Buenos Aires"] == 3_121_707


def test_mapping_aeropuertos_iata_icao():
    m = arg.aeropuertos.mapping("iata", "icao")
    assert m["EZE"] == "SAEZ"


def test_mapping_monedas():
    m = arg.monedas.mapping("codigo_iso", "simbolo")
    assert m["ARS"] == "$"
    assert m["ARM"] == "m$n"


def test_mapping_universidades():
    m = arg.universidades.mapping("sigla", "anio_fundacion")
    assert m["UBA"] == 1821
    assert m["UNC"] == 1613


def test_mapping_atributo_invalido():
    import pytest
    with pytest.raises(AttributeError):
        arg.provincias.mapping("codigo_indec", "no_existe")


# === 2. arg.telefonos.extraer_de_texto ===

def test_extraer_basico():
    matches = arg.telefonos.extraer_de_texto("Llamame al 11 1234-5678")
    assert len(matches) == 1
    assert "1234-5678" in matches[0]


def test_extraer_multiples():
    texto = "Tel 1: 11 1234-5678. Tel 2: 0351 765-4321"
    matches = arg.telefonos.extraer_de_texto(texto)
    assert len(matches) == 2


def test_extraer_dedupe():
    texto = "Igual: 11 1234-5678 y 11 1234-5678 otra vez"
    matches = arg.telefonos.extraer_de_texto(texto)
    assert len(matches) == 1


def test_extraer_normalizar_e164():
    texto = "Tel: +54 9 11 1234-5678"
    matches = arg.telefonos.extraer_de_texto(texto, normalizar=True)
    assert "+5491112345678" in matches


def test_extraer_sin_telefonos():
    assert arg.telefonos.extraer_de_texto("hola que tal") == ()
    assert arg.telefonos.extraer_de_texto("") == ()
    assert arg.telefonos.extraer_de_texto(None) == ()


def test_extraer_ignora_numeros_cortos():
    # Códigos postales y números chicos no deberían matchear
    texto = "El CP es 1425 y la calle 123"
    matches = arg.telefonos.extraer_de_texto(texto)
    assert matches == ()


# === 3. Generadores ===

def test_generar_dni():
    dni = arg.personas.generar_dni()
    assert arg.personas.validar_dni(dni)
    assert 1_000_000 <= int(dni) <= 99_999_999


def test_generar_dni_rango():
    r = random.Random(0)
    for _ in range(20):
        dni = arg.personas.generar_dni(20_000_000, 40_000_000, rng=r)
        assert 20_000_000 <= int(dni) <= 40_000_000


def test_generar_cuit_fisica():
    r = random.Random(1)
    for _ in range(10):
        cuit = arg.personas.generar_cuit(rng=r)
        assert arg.personas.validar_cuit(cuit)
        assert arg.personas.tipo_cuit(cuit) == "persona_fisica"


def test_generar_cuit_juridica():
    r = random.Random(2)
    for _ in range(10):
        cuit = arg.personas.generar_cuit("persona_juridica", rng=r)
        assert arg.personas.validar_cuit(cuit)
        assert arg.personas.tipo_cuit(cuit) == "persona_juridica"


def test_generar_cuit_con_dni_explicito():
    cuit = arg.personas.generar_cuit(dni=12345678, rng=random.Random(0))
    assert arg.personas.extraer_dni_de_cuit(cuit) == "12345678"
    assert arg.personas.validar_cuit(cuit)


def test_generar_cbu_valido():
    r = random.Random(3)
    for _ in range(10):
        cbu = arg.bancos.generar_cbu(rng=r)
        assert arg.bancos.validar_cbu(cbu)
        assert len(cbu) == 22


def test_generar_cbu_banco_especifico():
    cbu = arg.bancos.generar_cbu(codigo_banco="011", rng=random.Random(0))
    assert cbu.startswith("011")
    assert arg.bancos.validar_cbu(cbu)
    assert arg.bancos.banco_de_cbu(cbu) == "Banco de la Nación Argentina"


def test_generar_cuit_tipo_invalido():
    import pytest
    with pytest.raises(ValueError):
        arg.personas.generar_cuit("persona_inexistente")


# === 4. Fuzzy lookup ===

def test_fuzzy_provincia_typo():
    # Sin fuzzy: None
    assert arg.provincias.lookup("misisones") is None
    # Con fuzzy: Misiones
    p = arg.provincias.lookup("misisones", fuzzy=True)
    assert p is not None
    assert p.nombre == "Misiones"


def test_fuzzy_provincia_buens_aires():
    p = arg.provincias.lookup("buens aires", fuzzy=True)
    assert p is not None
    assert p.nombre == "Buenos Aires"


def test_fuzzy_ciudad():
    c = arg.ciudades.lookup("rosrio", fuzzy=True)
    assert c is not None
    assert c.nombre == "Rosario"


def test_fuzzy_no_rompe_matches_exactos():
    # Con fuzzy=True el match exacto sigue funcionando
    p = arg.provincias.lookup("Córdoba", fuzzy=True)
    assert p.nombre == "Córdoba"


def test_fuzzy_cutoff_alto():
    # Cutoff exigente: typos grandes no matchean
    p = arg.provincias.lookup("xyz", fuzzy=True, cutoff=0.95)
    assert p is None


def test_fuzzy_off_default():
    # Por default fuzzy es False (no rompe perf)
    assert arg.provincias.lookup("misisones") is None
