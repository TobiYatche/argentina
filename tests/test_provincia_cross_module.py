"""Properties cross-module en Provincia: universidades / aeropuertos / ciudades / departamentos."""

import argentina as arg


def test_universidades():
    cordoba = arg.provincias.CORDOBA.universidades
    siglas = {u.sigla for u in cordoba}
    assert "UNC" in siglas
    assert "UNRC" in siglas
    assert "UNVM" in siglas


def test_universidades_caba():
    caba = arg.provincias.CABA.universidades
    siglas = {u.sigla for u in caba}
    assert "UBA" in siglas
    assert "UTN" in siglas


def test_aeropuertos():
    chubut = arg.provincias.CHUBUT.aeropuertos
    iatas = {a.iata for a in chubut}
    assert "CRD" in iatas
    assert "PMY" in iatas


def test_ciudades():
    cordoba = arg.provincias.CORDOBA.ciudades
    nombres = {c.nombre for c in cordoba}
    assert "Córdoba" in nombres
    assert "Río Cuarto" in nombres


def test_departamentos():
    ba = arg.provincias.BUENOS_AIRES.departamentos
    assert len(ba) == 135  # partidos de Buenos Aires


def test_departamentos_caba():
    caba = arg.provincias.CABA.departamentos
    assert len(caba) == 15  # comunas


def test_consistencia_cantidades():
    # Sumar las cantidades por todas las provincias = total
    total_univ = sum(len(p.universidades) for p in arg.provincias)
    assert total_univ == len(arg.universidades)

    total_aero = sum(len(p.aeropuertos) for p in arg.provincias)
    assert total_aero == len(arg.aeropuertos)

    total_dep = sum(len(p.departamentos) for p in arg.provincias)
    assert total_dep == len(arg.departamentos)
