import argentina as arg


class MockResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return [
            {
                "fecha": "2026-05-25",
                "nombre": "Día de la Revolución de Mayo",
                "tipo": "inamovible",
            }
        ]


def test_obtener(monkeypatch):
    import argentina.feriados as feriados

    feriados.obtener.cache_clear()

    def mock_get(url, timeout):
        return MockResponse()

    import requests

    monkeypatch.setattr(requests, "get", mock_get)

    data = arg.feriados.obtener(2026)

    assert isinstance(data, list)
    assert data[0]["fecha"] == "2026-05-25"


def test_es_feriado(monkeypatch):
    import argentina.feriados as feriados

    feriados.obtener.cache_clear()

    def mock_get(url, timeout):
        return MockResponse()

    import requests

    monkeypatch.setattr(requests, "get", mock_get)

    assert arg.feriados.es_feriado("2026-05-25") is True
    assert arg.feriados.es_feriado("2026-05-26") is False


def test_detalle(monkeypatch):
    import argentina.feriados as feriados

    feriados.obtener.cache_clear()

    def mock_get(url, timeout):
        return MockResponse()

    import requests

    monkeypatch.setattr(requests, "get", mock_get)

    detalle = arg.feriados.detalle("2026-05-25")

    assert detalle is not None
    assert detalle["tipo"] == "inamovible"


def test_proximo(monkeypatch):
    import argentina.feriados as feriados

    feriados.obtener.cache_clear()

    def mock_get(url, timeout):
        return MockResponse()

    import requests

    monkeypatch.setattr(requests, "get", mock_get)

    prox = arg.feriados.proximo("2026-05-01")

    assert prox is not None
    assert prox["fecha"] == "2026-05-25"
