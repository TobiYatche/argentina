import argentina as arg
from datetime import date


def test_parsear_fecha_argentina():
    assert arg.fechas.parsear_fecha("31/12/2024") == date(2024, 12, 31)


def test_parsear_fecha_guion():
    assert arg.fechas.parsear_fecha("31-12-2024") == date(2024, 12, 31)


def test_parsear_fecha_iso():
    assert arg.fechas.parsear_fecha("2024-12-31") == date(2024, 12, 31)


def test_parsear_fecha_invalida():
    assert arg.fechas.parsear_fecha("31/31/2024") is None


def test_es_fecha_valida():
    assert arg.fechas.es_fecha_valida("31/12/2024") is True
    assert arg.fechas.es_fecha_valida("mala") is False


def test_fecha_iso():
    assert arg.fechas.fecha_iso("31/12/2024") == "2024-12-31"


def test_edad_en_anios():
    assert arg.fechas.edad_en_anios("10/05/2015", "12/05/2026") == 11


def test_edad_en_anios_antes_de_cumple():
    assert arg.fechas.edad_en_anios("10/12/2015", "12/05/2026") == 10


def test_edad_fecha_futura():
    assert arg.fechas.edad_en_anios("12/05/2030", "12/05/2026") is None


def test_cohorte_nacimiento():
    assert arg.fechas.cohorte_nacimiento("10/05/2015") == 2015


def test_anio_lectivo_marzo():
    assert arg.fechas.anio_lectivo("15/03/2024") == 2024


def test_anio_lectivo_febrero():
    assert arg.fechas.anio_lectivo("15/02/2024") == 2023


def test_mes_anio():
    assert arg.fechas.mes_anio("31/12/2024") == "2024-12"
