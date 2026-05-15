import math

import pytest

import argentina as arg


def test_distancia_misma_ciudad():
    d = arg.geo.distancia("Córdoba", "Córdoba")
    assert d == pytest.approx(0.0, abs=1e-6)


def test_distancia_caba_cordoba():
    # Distancia esperada: ~650 km (línea recta entre capitales)
    d = arg.geo.distancia("Buenos Aires", "Córdoba")
    assert 600 < d < 750


def test_distancia_caba_ushuaia():
    d = arg.geo.distancia("Buenos Aires", "Ushuaia")
    assert 2300 < d < 2500


def test_distancia_tuplas():
    # CABA → Córdoba con coordenadas explícitas
    d = arg.geo.distancia((-34.6037, -58.3816), (-31.4201, -64.1888))
    assert 600 < d < 750


def test_distancia_provincias():
    # Buenos Aires (La Plata) → Mendoza
    d = arg.geo.distancia(arg.provincias.BUENOS_AIRES, arg.provincias.MENDOZA)
    assert 950 < d < 1100


def test_distancia_simetrica():
    d_ab = arg.geo.distancia("Buenos Aires", "Mendoza")
    d_ba = arg.geo.distancia("Mendoza", "Buenos Aires")
    assert d_ab == pytest.approx(d_ba, abs=0.001)


def test_distancia_ciudad_y_provincia():
    # Combinar tipos
    d = arg.geo.distancia(arg.ciudades.lookup("Rosario"), arg.provincias.CORDOBA)
    assert d > 0


def test_distancia_invalido():
    with pytest.raises(ValueError):
        arg.geo.distancia("Atlantis", "Córdoba")
    with pytest.raises(ValueError):
        arg.geo.distancia(None, "Córdoba")
