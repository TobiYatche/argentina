import pytest

from argentina.geo import basemaps


def test_argenmap_tiles():
    assert "ign" in basemaps.ARGENMAP_TILES.lower()


def test_argenmap_attribution():
    assert "Instituto Geográfico Nacional" in (
        basemaps.ARGENMAP_ATTRIBUTION
    )


def test_require_folium_message():
    try:
        import folium  # noqa: F401
    except ImportError:
        with pytest.raises(ImportError):
            basemaps.add_argenmap(None)
