import pytest

from argentina.geo import postal


def test_georreferenciar_codigo_postal_not_implemented():
    with pytest.raises(NotImplementedError):
        postal.georreferenciar_codigo_postal("C1425ABC")


def test_codigo_postal_por_direccion_not_implemented():
    with pytest.raises(NotImplementedError):
        postal.codigo_postal_por_direccion("Av. Santa Fe 3253, CABA")


def test_validar_codigo_postal_municipio_not_implemented():
    with pytest.raises(NotImplementedError):
        postal.validar_codigo_postal_municipio("C1425ABC", "CABA")
