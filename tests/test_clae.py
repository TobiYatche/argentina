"""Tests del módulo ``argentina.clae``.

Sin internet, sin archivos externos.
"""

import argentina as arg


def test_lookup_codigo_conocido():
    a = arg.clae.lookup("620100")
    assert a is not None
    assert a.descripcion.startswith("Servicios de consultores en informática")
    assert a.sector == "J"
    assert a.grupo == "6201"


def test_lookup_acepta_int():
    a = arg.clae.lookup(620100)
    assert a is not None
    assert a.codigo == "620100"


def test_lookup_padding_codigo_corto():
    # 5 dígitos se padea con cero al frente.
    a = arg.clae.lookup("21000")  # → 021000 (silvicultura)
    assert a is not None
    assert a.codigo == "021000"


def test_lookup_codigo_inexistente():
    assert arg.clae.lookup("999999") is None
    assert arg.clae.lookup("000000") is None


def test_lookup_none_vacio():
    assert arg.clae.lookup(None) is None
    assert arg.clae.lookup("") is None
    assert arg.clae.lookup("xyz") is None


def test_es_valido():
    assert arg.clae.es_valido("620100") is True
    assert arg.clae.es_valido("999999") is False
    assert arg.clae.es_valido(None) is False


def test_listar_no_vacio():
    todas = arg.clae.listar()
    assert len(todas) >= 100  # subset representativo
    assert all(a.codigo for a in todas)
    assert all(len(a.codigo) == 6 for a in todas)


def test_por_sector_filtra():
    res = arg.clae.por_sector("J")
    assert all(a.sector == "J" for a in res)
    assert any(a.codigo == "620100" for a in res)


def test_por_sector_case_insensitive():
    assert arg.clae.por_sector("j") == arg.clae.por_sector("J")


def test_por_sector_inexistente():
    assert arg.clae.por_sector("Z") == ()
    assert arg.clae.por_sector(None) == ()
    assert arg.clae.por_sector("") == ()


def test_por_grupo_filtra():
    res = arg.clae.por_grupo("6201")
    assert all(a.grupo == "6201" for a in res)


def test_por_grupo_padding():
    assert arg.clae.por_grupo("6201") == arg.clae.por_grupo(6201)


def test_buscar_substring():
    res = arg.clae.buscar("informática")
    assert len(res) >= 1
    codigos = {a.codigo for a in res}
    assert "620100" in codigos


def test_buscar_normaliza_tildes():
    sin = arg.clae.buscar("informatica")
    con = arg.clae.buscar("informática")
    assert {a.codigo for a in sin} == {a.codigo for a in con}


def test_buscar_case_insensitive():
    assert {a.codigo for a in arg.clae.buscar("PETRÓLEO")} == {
        a.codigo for a in arg.clae.buscar("petróleo")
    }


def test_buscar_vacio():
    assert arg.clae.buscar("") == ()
    assert arg.clae.buscar(None) == ()


def test_sectores_lista_letras():
    sectores = arg.clae.sectores()
    letras = [s.letra for s in sectores]
    assert letras == sorted(letras)
    assert all(len(s.letra) == 1 for s in sectores)
    assert "J" in letras


def test_codigos_unicos():
    todas = arg.clae.listar()
    codigos = [a.codigo for a in todas]
    assert len(codigos) == len(set(codigos))


def test_modulo_iterable():
    n = 0
    for a in arg.clae:
        n += 1
        if n >= 3:
            break
    assert n == 3


def test_contains_modulo():
    assert "620100" in arg.clae
    assert "999999" not in arg.clae


def test_como_tabla():
    tabla = arg.clae.como_tabla()
    assert isinstance(tabla, list)
    assert all(isinstance(row, dict) for row in tabla)
    assert "codigo" in tabla[0]
    assert "descripcion" in tabla[0]
