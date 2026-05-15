from argentina.geo import direcciones


class MockResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "direcciones": [
                {
                    "nomenclatura": "AV SANTA FE 3253",
                    "ubicacion": {
                        "lat": -34.588,
                        "lon": -58.41,
                    },
                    "provincia": {
                        "nombre": "Ciudad Autónoma de Buenos Aires",
                        "id": "02",
                    },
                }
            ]
        }


def test_georreferenciar(monkeypatch):
    def mock_get(url, params, timeout):
        return MockResponse()

    import requests

    monkeypatch.setattr(requests, "get", mock_get)

    resultado = direcciones.georreferenciar(
        direccion="Av. Santa Fe 3253",
        provincia="CABA",
    )

    assert resultado is not None
    assert resultado["nomenclatura"] == "AV SANTA FE 3253"


def test_coordenadas(monkeypatch):
    def mock_get(url, params, timeout):
        return MockResponse()

    import requests

    monkeypatch.setattr(requests, "get", mock_get)

    coords = direcciones.coordenadas(
        direccion="Av. Santa Fe 3253",
        provincia="CABA",
    )

    assert coords == (-34.588, -58.41)


def test_georreferenciar_sin_resultados(monkeypatch):
    class EmptyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "direcciones": []
            }

    def mock_get(url, params, timeout):
        return EmptyResponse()

    import requests

    monkeypatch.setattr(requests, "get", mock_get)

    resultado = direcciones.georreferenciar(
        direccion="direccion inexistente"
    )

    assert resultado is None
