"""Tests del módulo argentina.economia (sin conexión a internet)."""

from __future__ import annotations

import pandas as pd

from argentina.economia import buscar, obtener_serie, serie
from argentina.economia.catalogo import SERIES


class _FakeResponse:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._payload


def test_serie_resuelve_alias_a_id_correcto(monkeypatch):
    capturado = {}

    def fake_get(url, params=None, timeout=None):
        capturado["url"] = url
        capturado["params"] = params
        return _FakeResponse({"data": []})

    monkeypatch.setattr("requests.get", fake_get)

    serie("ipc_nacional")

    assert capturado["params"]["ids"] == SERIES["ipc_nacional"]["id"]


def test_obtener_serie_convierte_json_en_dataframe(monkeypatch):
    payload = {
        "data": [
            ["2020-01-01", 100.0],
            ["2020-02-01", 102.5],
            ["2020-03-01", 105.0],
        ]
    }

    def fake_get(url, params=None, timeout=None):
        return _FakeResponse(payload)

    monkeypatch.setattr("requests.get", fake_get)

    df = obtener_serie("cualquier_id")

    assert list(df.columns) == ["fecha", "valor"]
    assert len(df) == 3
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])
    assert df["fecha"].is_monotonic_increasing


def test_obtener_serie_respuesta_vacia_devuelve_dataframe_vacio(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        return _FakeResponse({"data": []})

    monkeypatch.setattr("requests.get", fake_get)

    df = obtener_serie("cualquier_id")

    assert list(df.columns) == ["fecha", "valor"]
    assert df.empty


def test_catalogo_tiene_entradas_y_campos_completos():
    assert len(SERIES) >= 480
    for alias, entry in SERIES.items():
        assert "id" in entry and entry["id"]
        assert "descripcion" in entry
        assert "fuente" in entry

    # Las series macro originales siguen presentes y con su ID conocido
    assert SERIES["ipc_nacional"]["id"] == "148.3_INIVELNAL_DICI_M_26"
    assert SERIES["emae"]["id"] == "143.3_NO_PR_2004_A_21"
    assert SERIES["tipo_cambio_minorista"]["id"] == "168.1_T_CAMBIOR_D_0_0_26"
    assert SERIES["ipc_nucleo_nacional"]["id"] == "148.3_INUCLEONAL_DICI_M_19"


def test_catalogo_ids_son_unicos():
    ids = [e["id"] for e in SERIES.values()]
    assert len(ids) == len(set(ids))


def test_buscar_devuelve_columnas_esperadas():
    resultado = buscar("emae")
    assert list(resultado.columns) == ["alias", "id", "frecuencia", "tema", "descripcion"]
    assert len(resultado) > 0


def test_buscar_es_case_insensitive():
    minusculas = buscar("ipc")
    mayusculas = buscar("IPC")
    mixto = buscar("Ipc")
    assert len(minusculas) == len(mayusculas) == len(mixto) > 0
    assert set(minusculas["alias"]) == set(mayusculas["alias"]) == set(mixto["alias"])


def test_buscar_sin_coincidencias_devuelve_df_vacio_con_columnas():
    resultado = buscar("xyzzy_palabra_que_no_existe")
    assert resultado.empty
    assert list(resultado.columns) == ["alias", "id", "frecuencia", "tema", "descripcion"]


def test_buscar_ids_corresponden_al_catalogo():
    resultado = buscar("emae")
    for _, fila in resultado.iterrows():
        assert SERIES[fila["alias"]]["id"] == fila["id"]


def test_buscar_matchea_en_descripcion_no_solo_en_alias():
    # "minorista" aparece en la descripción del tipo de cambio
    resultado = buscar("minorista")
    assert "tipo_cambio_minorista" in set(resultado["alias"])
