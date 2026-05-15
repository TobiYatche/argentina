import pytest

import argentina.geo.shapes as shapes


def test_shape_urls_configured():
    """Las URLs ya no son placeholder — apuntan al WFS del IGN."""
    for name in ("provincias", "departamentos"):
        url = shapes.SHAPE_URLS[name]
        assert url.startswith("https://"), f"{name}: URL no es HTTPS"
        assert "PLACEHOLDER" not in url, f"{name}: URL sigue siendo placeholder"
        assert "ign.gob.ar" in url, f"{name}: URL no es del IGN"


def test_placeholder_url_raises_value_error():
    """Si alguien pasa una URL placeholder/vacía explícita, seguimos rechazándola."""
    with pytest.raises(ValueError):
        shapes.provincias(url="PLACEHOLDER_FOO")
    with pytest.raises(ValueError):
        shapes.provincias(url="")


def test_find_vector_file_prefers_gpkg(tmp_path):
    shp = tmp_path / "test.shp"
    gpkg = tmp_path / "test.gpkg"

    shp.write_text("")
    gpkg.write_text("")

    result = shapes._find_vector_file(tmp_path)

    assert result == gpkg


def test_extract_zip(tmp_path):
    zip_path = tmp_path / "test.zip"
    out_dir = tmp_path / "out"

    source_file = tmp_path / "archivo.txt"
    source_file.write_text("hola")

    import zipfile

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(source_file, arcname="archivo.txt")

    shapes._extract_zip(zip_path, out_dir)

    assert (out_dir / "archivo.txt").exists()
