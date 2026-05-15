"""Helper de alto nivel: armar un mapa Folium prearmado en una línea.

Compone ``argentina.geo.shapes`` + ``argentina.geo.basemaps`` +
``argentina.provincias`` para el caso común: "quiero ver la provincia X en un
mapa".

Requiere ``folium`` y ``geopandas`` (extras ``[maps]`` y ``[geo]``).
"""

from __future__ import annotations

from argentina import provincias as _provs


def _require_dependencies() -> None:
    try:
        import folium  # noqa: F401
        import geopandas  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            'Para usar argentina.geo.mapa instalá: '
            'pip install "argentina[maps,geo]"'
        ) from exc


def mapa_de(
    nombre_o_codigo: str,
    *,
    zoom: int | None = None,
    incluir_capital: bool = True,
    color: str = "#FFD580",
):
    """Devuelve un mapa Folium centrado en una provincia argentina.

    Acepta cualquier cosa que ``argentina.provincias.lookup`` reconozca:
    nombre, código INDEC, ISO, alias (``"PBA"``, ``"CABA"``, ``"TDF"``…).

    El mapa trae:
    - Argenmap IGN como fondo (toponimia argentina, Islas Malvinas).
    - Polígono de la provincia con borde negro y relleno suave.
    - Marker en la capital con popup (si ``incluir_capital=True`` y hay coords).
    - Créditos y control de capas.

    Parameters
    ----------
    nombre_o_codigo : str
        Identificador de provincia (cualquier formato que entienda ``lookup``).
    zoom : int, optional
        Nivel de zoom inicial. Si ``None`` lo elige según el tamaño visual de
        la provincia (CABA = 11, Patagonia grande = 5, resto = 7).
    incluir_capital : bool
        Si ``True``, agrega un marker en la capital con popup.
    color : str
        Color de relleno del polígono.
    """
    _require_dependencies()

    import folium
    from argentina.geo import basemaps, shapes

    p = _provs.lookup(nombre_o_codigo)
    if p is None:
        raise ValueError(
            f"No se encontró la provincia: {nombre_o_codigo!r}. "
            f"Probá con un nombre, código INDEC, ISO o alias conocido."
        )

    gdf = shapes.provincias()
    fila = gdf[gdf["in1"] == p.codigo_indec]
    if fila.empty:
        raise ValueError(
            f"El IGN no devolvió un polígono para {p.nombre} "
            f"(código {p.codigo_indec})."
        )

    geom = fila.iloc[0].geometry
    centroide = geom.representative_point()

    if zoom is None:
        if p.codigo_indec == "02":          # CABA
            zoom = 11
        elif p.codigo_indec in {"78", "94"}:  # Santa Cruz, TDF (grandes/lejanas)
            zoom = 5
        else:
            zoom = 7

    m = folium.Map(
        location=[centroide.y, centroide.x],
        zoom_start=zoom,
        tiles=None,
    )
    basemaps.add_argenmap(m)

    folium.GeoJson(
        fila[["nam", "in1", "geometry"]],
        name=p.nombre,
        style_function=lambda f: {
            "fillColor": color,
            "color": "black",
            "weight": 1.2,
            "fillOpacity": 0.4,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["nam", "in1"],
            aliases=["Provincia:", "Código INDEC:"],
        ),
    ).add_to(m)

    if incluir_capital and p.capital_lat is not None and p.capital_lon is not None:
        popup_html = (
            f"<b>{p.capital}</b><br>"
            f"Capital de {p.nombre}<br>"
            f"Región: {p.region}<br>"
            f"<code>ISO {p.iso_id} · INDEC {p.codigo_indec}</code>"
        )
        folium.Marker(
            location=[p.capital_lat, p.capital_lon],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=p.capital,
            icon=folium.Icon(color="red", icon="star"),
        ).add_to(m)

    basemaps.add_creditos_argentina(m)
    basemaps.add_layer_control(m)
    return m


__all__ = ["mapa_de"]
