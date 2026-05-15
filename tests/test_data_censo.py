import importlib

import pytest

from argentina.data.censo import CENSO_PARQUETS_2022, censo


def test_censo_anio_invalido():
    # ValueError debe dispararse antes que el chequeo de deps.
    with pytest.raises(ValueError):
        censo(anio=2010)


def test_censo_sin_url_ni_tabla():
    """Sin URL y sin tabla → ValueError pidiendo uno u otro."""
    with pytest.raises(ValueError, match="tabla"):
        censo(anio=2022)


def test_censo_tabla_sin_url_configurada():
    """Si la tabla existe pero no tiene URL, error claro pidiendo URL."""
    # Por default CENSO_PARQUETS_2022 está vacío.
    with pytest.raises(ValueError, match="URL"):
        censo(anio=2022, tabla="personas")


def test_censo_provincia_invalida(monkeypatch):
    """Una provincia que no existe → ValueError claro."""
    # Configurar una URL fake para que llegue al filtro
    monkeypatch.setitem(CENSO_PARQUETS_2022, "personas", "https://example.com/x.parquet")
    with pytest.raises(ValueError, match="rovincia"):
        censo(anio=2022, tabla="personas", provincia="Atlantis")


def test_censo_construye_query(monkeypatch):
    """Con URL y filtros, llega a DuckDB con la query correcta."""
    capturado = {}

    class FakeConn:
        def execute(self, sql):
            capturado["sql"] = sql
            return self

        def fetchdf(self):
            import pandas as pd
            return pd.DataFrame({"x": [1]})

        def close(self):
            pass

    class FakeDuckDB:
        @staticmethod
        def connect():
            return FakeConn()

    monkeypatch.setitem(
        CENSO_PARQUETS_2022,
        "personas",
        "https://example.com/personas.parquet",
    )

    # Importar duckdb es lo que hace _require_censo_dependencies. Lo neutralizamos
    # y mockeamos el módulo duckdb visto por la función.
    modulo = importlib.import_module("argentina.data.censo")
    monkeypatch.setattr(modulo, "_require_censo_dependencies", lambda: None)

    import sys
    sys.modules["duckdb"] = FakeDuckDB

    try:
        df = censo(
            anio=2022,
            tabla="personas",
            provincia="Córdoba",
            limite=100,
        )
    finally:
        sys.modules.pop("duckdb", None)

    sql = capturado["sql"]
    assert "read_parquet('https://example.com/personas.parquet')" in sql
    assert "provincia_codigo = '14'" in sql  # Córdoba
    assert "LIMIT 100" in sql
    assert len(df) == 1
