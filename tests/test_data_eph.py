import pytest

from argentina.data.eph import (
    EPH_URL_TRIMESTRAL,
    _normalizar_periodo,
    _normalizar_tipo,
    _validar_eph_args,
    eph,
)


def test_normalizar_periodo():
    assert _normalizar_periodo("T") == "trimestral"
    assert _normalizar_periodo("sem") == "semestral"


def test_normalizar_tipo():
    assert _normalizar_tipo("individual") == "individual"
    assert _normalizar_tipo("personas") == "individual"
    assert _normalizar_tipo("HOGAR") == "hogar"


def test_normalizar_tipo_invalido():
    with pytest.raises(ValueError):
        _normalizar_tipo("desconocido")


def test_validar_eph_args():
    assert _validar_eph_args(2026, "semestral", 1) == (
        2026,
        "semestral",
        1,
    )


def test_validar_eph_args_invalido():
    with pytest.raises(ValueError):
        _validar_eph_args(2026, "semestral", 3)


def test_eph_semestral_no_implementado():
    """EPH semestral (pre-2003) sigue como NotImplementedError."""
    with pytest.raises(NotImplementedError):
        eph(2003, "semestral", 1)


def test_eph_url_pattern():
    """La URL se construye correctamente para EPH trimestral."""
    url = EPH_URL_TRIMESTRAL.format(numero=1, anio=2024)
    assert "indec.gob.ar" in url
    assert "EPH_usu_1_Trim_2024_txt.zip" in url


def test_eph_trimestral_descarga_y_lee(monkeypatch, tmp_path):
    """eph() trimestral: simulamos descarga + lectura sin red."""
    import importlib
    import zipfile

    # Armar un ZIP fake con un microdato de individual
    fake_zip = tmp_path / "src.zip"
    fake_csv_content = "CODUSU;ANO4;TRIMESTRE;EDAD\n100;2024;1;30\n100;2024;1;5\n"
    with zipfile.ZipFile(fake_zip, "w") as zf:
        zf.writestr("usu_individual_T124.txt", fake_csv_content)

    # Monkeypatch del download para que copie el zip fake al destino.
    # Importamos el módulo crudo porque `argentina.data.eph` (atributo) es la
    # función después del `from argentina.data.eph import eph` en data/__init__.
    def fake_download(url, path, timeout=300):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(fake_zip.read_bytes())
        return path

    modulo = importlib.import_module("argentina.data.eph")
    monkeypatch.setattr(modulo, "_download_file", fake_download)

    df = eph(anio=2024, periodo="trimestral", numero=1, tipo="individual", cache_dir=tmp_path)
    assert list(df.columns) == ["CODUSU", "ANO4", "TRIMESTRE", "EDAD"]
    assert len(df) == 2
    assert df["EDAD"].tolist() == [30, 5]
