import argentina as arg


def test_codigos():
    assert arg.pais.CODIGO_ISO == "AR"
    assert arg.pais.CODIGO_ISO_3 == "ARG"
    assert arg.pais.CODIGO_NUMERICO == "032"


def test_comunicacion():
    assert arg.pais.TELEFONO_PREFIJO == "+54"
    assert arg.pais.TLD == ".ar"


def test_moneda_actual():
    assert arg.pais.MONEDA == "ARS"


def test_estructura():
    assert arg.pais.CANTIDAD_PROVINCIAS == 24
    assert arg.pais.CANTIDAD_PROVINCIAS == len(arg.provincias)
    assert arg.pais.CANTIDAD_DEPARTAMENTOS == 529
    assert arg.pais.CANTIDAD_DEPARTAMENTOS == len(arg.departamentos)


def test_bbox():
    lon_min, lat_min, lon_max, lat_max = arg.pais.BBOX
    assert lon_min < lon_max
    assert lat_min < lat_max
    # Argentina está en hemisferio sur y al oeste
    assert lon_max < 0
    assert lat_max < 0
