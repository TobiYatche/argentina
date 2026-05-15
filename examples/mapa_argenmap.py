import argentina as arg
import folium

m = folium.Map(
    location=[-34.6037, -58.3816],
    zoom_start=4,
    tiles=None,
)

arg.geo.basemaps.add_argenmap(m)

arg.geo.basemaps.add_creditos_argentina(m)

arg.geo.basemaps.add_layer_control(m)

m.save("mapa_argentina.html")

print(
    "Mapa guardado en mapa_argentina.html"
)
