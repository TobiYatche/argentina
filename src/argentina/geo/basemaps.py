from __future__ import annotations


# Fondo Argenmap IGN Argentina.
# Importante:
# Usar tiles argentinos ayuda a mantener
# la toponimia argentina para Islas Malvinas.

ARGENMAP_TILES = (
    "https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/"
    "capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png"
)

ARGENMAP_ATTRIBUTION = (
    "Instituto Geográfico Nacional de la República Argentina"
)


def _require_folium() -> None:
    """Verifica que folium esté instalado."""
    try:
        import folium  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            'Para usar argentina.geo.basemaps instalá: '
            'pip install "argentina[maps]"'
        ) from exc


def add_argenmap(
    m,
    name: str = "Argenmap IGN",
    show: bool = True,
):
    """
    Agrega fondo base Argenmap IGN a un mapa Folium.
    """
    _require_folium()

    import folium

    folium.TileLayer(
        tiles=ARGENMAP_TILES,
        attr=ARGENMAP_ATTRIBUTION,
        name=name,
        overlay=False,
        control=True,
        show=show,
    ).add_to(m)

    return m


def add_creditos_argentina(m):
    """
    Agrega créditos cartográficos argentinos.
    """
    _require_folium()

    import folium

    html = (
        '<div '
        'style="'
        'position: fixed; '
        'bottom: 10px; '
        'left: 10px; '
        'z-index: 9999; '
        'background-color: white; '
        'padding: 6px; '
        'border: 1px solid #999; '
        'font-size: 11px;'
        '">'
        'Cartografía: IGN Argentina / Argenmap. '
        'Toponimia argentina: Islas Malvinas.'
        '</div>'
    )

    m.get_root().html.add_child(
        folium.Element(html)
    )

    return m


def add_layer_control(m):
    """
    Agrega control de capas Folium.
    """
    _require_folium()

    import folium

    folium.LayerControl().add_to(m)

    return m


__all__ = [
    "ARGENMAP_TILES",
    "ARGENMAP_ATTRIBUTION",
    "add_argenmap",
    "add_creditos_argentina",
    "add_layer_control",
]
