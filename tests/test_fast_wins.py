"""Fast wins de v0.2.0: properties cruzadas, helpers de export, arg.coordenadas."""

import argentina as arg


# === 1. Provincia.cpa_letra / codigo_telefono / aglomerados ===

def test_provincia_cpa_letra():
    assert arg.provincias.CORDOBA.cpa_letra == "X"
    assert arg.provincias.CABA.cpa_letra == "C"
    assert arg.provincias.BUENOS_AIRES.cpa_letra == "B"
    assert arg.provincias.TIERRA_DEL_FUEGO.cpa_letra == "V"


def test_provincia_codigo_telefono():
    assert arg.provincias.CABA.codigo_telefono == "11"
    assert arg.provincias.CORDOBA.codigo_telefono == "351"
    assert arg.provincias.MENDOZA.codigo_telefono == "261"
    # Capital chica: 4 dígitos
    assert arg.provincias.TIERRA_DEL_FUEGO.codigo_telefono == "2901"


def test_provincia_aglomerados():
    aglo = arg.provincias.CORDOBA.aglomerados
    nombres = {a.nombre for a in aglo}
    assert "Gran Córdoba" in nombres
    assert "Río Cuarto" in nombres


def test_provincia_aglomerados_buenos_aires():
    aglo = arg.provincias.BUENOS_AIRES.aglomerados
    # PBA tiene varios aglomerados EPH
    nombres = {a.nombre for a in aglo}
    assert "Gran La Plata" in nombres
    assert "Partidos del GBA" in nombres


# === 2. Ciudad.es_capital_provincial ===

def test_ciudad_es_capital_cordoba():
    c = arg.ciudades.lookup("Córdoba")
    assert c.es_capital_provincial is True


def test_ciudad_es_capital_la_plata():
    c = arg.ciudades.lookup("La Plata")
    assert c.es_capital_provincial is True


def test_ciudad_no_es_capital_rosario():
    c = arg.ciudades.lookup("Rosario")
    assert c.es_capital_provincial is False  # Capital de Santa Fe es Santa Fe


def test_ciudad_es_capital_buenos_aires():
    # "Buenos Aires" (CABA): la capital de la provincia "Ciudad Autónoma..."
    # se resuelve vía alias al mismo objeto.
    c = arg.ciudades.lookup("Buenos Aires")
    assert c.es_capital_provincial is True


# === 3. arg.coordenadas(valor) ===

def test_coordenadas_ciudad():
    c = arg.coordenadas("Córdoba")
    assert c is not None
    assert -32 < c[0] < -31
    assert -65 < c[1] < -64


def test_coordenadas_provincia():
    # Provincia → coords de la capital
    c = arg.coordenadas("PBA")
    assert c is not None
    # La Plata ≈ (-34.92, -57.95)
    assert -35 < c[0] < -34
    assert -58 < c[1] < -57


def test_coordenadas_aeropuerto():
    c = arg.coordenadas("EZE")
    assert c is not None
    # Ezeiza ≈ (-34.82, -58.54)
    assert -35 < c[0] < -34
    assert -59 < c[1] < -58


def test_coordenadas_tupla_passthrough():
    c = arg.coordenadas((-34.6, -58.4))
    assert c == (-34.6, -58.4)


def test_coordenadas_objeto():
    c = arg.coordenadas(arg.provincias.CORDOBA)
    assert c == (-31.4201, -64.1888)


def test_coordenadas_inexistente():
    assert arg.coordenadas("Atlantis") is None
    assert arg.coordenadas(None) is None
    assert arg.coordenadas("") is None


# === 4. provincias.por_region + regiones ===

def test_regiones():
    regs = arg.provincias.regiones()
    assert "Patagonia" in regs
    assert "NOA" in regs
    assert "CABA" in regs
    # Hay exactamente 6 regiones
    assert len(regs) == 6


def test_por_region_patagonia():
    pat = arg.provincias.por_region("Patagonia")
    nombres = {p.nombre for p in pat}
    assert nombres == {"Chubut", "Neuquén", "Río Negro", "Santa Cruz", "Tierra del Fuego"}


def test_por_region_case_insensitive():
    a = arg.provincias.por_region("PATAGONIA")
    b = arg.provincias.por_region("patagonia")
    c = arg.provincias.por_region("Patagonia")
    assert a == b == c


def test_por_region_inexistente():
    assert arg.provincias.por_region("Atlántida") == ()
    assert arg.provincias.por_region(None) == ()


# === 5. como_dict / como_tabla ===

def test_provincia_como_dict():
    d = arg.provincias.CORDOBA.como_dict()
    assert d["nombre"] == "Córdoba"
    assert d["codigo_indec"] == "14"
    assert d["poblacion_2022"] == 3840905


def test_provincias_como_tabla():
    t = arg.provincias.como_tabla()
    assert len(t) == 24
    assert all(isinstance(r, dict) for r in t)
    # Columnas esperadas
    assert "nombre" in t[0]
    assert "codigo_indec" in t[0]
    assert "poblacion_2022" in t[0]


def test_ciudades_como_tabla():
    t = arg.ciudades.como_tabla()
    assert len(t) >= 33
    assert "nombre" in t[0]
    assert "lat" in t[0]


def test_departamentos_como_tabla():
    t = arg.departamentos.como_tabla()
    assert len(t) >= 500
    assert "codigo_departamento" in t[0]


def test_aglomerados_como_tabla():
    t = arg.aglomerados.como_tabla()
    assert len(t) >= 31
    assert "codigo" in t[0]


def test_universidades_como_tabla():
    t = arg.universidades.como_tabla()
    assert len(t) >= 50
    assert "sigla" in t[0]


def test_aeropuertos_como_tabla():
    t = arg.aeropuertos.como_tabla()
    assert len(t) >= 30
    assert "iata" in t[0]
