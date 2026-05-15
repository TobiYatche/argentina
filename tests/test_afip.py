"""Tests del módulo ``argentina.afip``.

Sin internet, sin archivos externos.
"""

import argentina as arg


# ---------------------------------------------------------------------------
# IVA
# ---------------------------------------------------------------------------


def test_iva_alicuotas_estructura():
    iva = arg.afip.alicuotas_iva()
    assert set(iva.keys()) == {"general", "reducida", "especial"}


def test_iva_alicuotas_valores():
    iva = arg.afip.alicuotas_iva()
    assert iva["general"] == 0.21
    assert iva["reducida"] == 0.105
    assert iva["especial"] == 0.27


def test_iva_constante_publica():
    assert arg.afip.ALICUOTAS_IVA["general"] == 0.21


def test_iva_devuelve_copia():
    # Mutar el resultado no afecta a la constante.
    iva = arg.afip.alicuotas_iva()
    iva["general"] = 0.99
    assert arg.afip.alicuotas_iva()["general"] == 0.21


# ---------------------------------------------------------------------------
# Reexports CUIT
# ---------------------------------------------------------------------------


def test_validar_cuit_reexport():
    for v in ["20-12345678-6", "20123456786", "xxx", None]:
        assert arg.afip.validar_cuit(v) == arg.personas.validar_cuit(v)


def test_limpiar_cuit_reexport():
    for v in ["20-12345678-6", "20 12345678 6", "xxx", None]:
        assert arg.afip.limpiar_cuit(v) == arg.personas.limpiar_cuit(v)


def test_formatear_cuit_reexport():
    for v in ["20123456786", "20-12345678-6", "abc", None]:
        assert arg.afip.formatear_cuit(v) == arg.personas.formatear_cuit(v)


def test_tipo_cuit_reexport():
    for v in ["20123456786", "30708080086", "xxx", None]:
        assert arg.afip.tipo_cuit(v) == arg.personas.tipo_cuit(v)


# ---------------------------------------------------------------------------
# Reexports CLAE
# ---------------------------------------------------------------------------


def test_clae_lookup_reexport():
    assert arg.afip.clae_lookup("620100") == arg.clae.lookup("620100")


def test_clae_buscar_reexport():
    assert arg.afip.clae_buscar("informática") == arg.clae.buscar("informática")


# ---------------------------------------------------------------------------
# Comportamiento transversal
# ---------------------------------------------------------------------------


def test_modulo_expuesto_en_paquete():
    assert hasattr(arg, "afip")
