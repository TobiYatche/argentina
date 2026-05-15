"""Tests del wrapper opcional `argentina.elecciones.api`.

Importar el módulo no debe pegar a la red ni requerir el extra `[elecciones]`.
"""

import argentina as arg


def test_modulo_importa_sin_pegar_a_red():
    # Sólo verificar que está accesible.
    assert arg.elecciones.api is not None


def test_disponible_devuelve_dict():
    estado = arg.elecciones.api.disponible()

    assert isinstance(estado, dict)
    assert set(estado.keys()) == {"requests", "pandas"}
    assert all(isinstance(v, bool) for v in estado.values())


def test_obtener_json_existe():
    # No la llamamos para no pegar a la red — sólo confirmar que es callable.
    assert callable(arg.elecciones.api.obtener_json)
