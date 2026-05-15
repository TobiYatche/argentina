import argentina as arg

resultado = arg.geo.direcciones.georreferenciar(
    direccion="Av. Santa Fe 3253",
    provincia="CABA",
)

print(resultado)

coords = arg.geo.direcciones.coordenadas(
    direccion="Av. Santa Fe 3253",
    provincia="CABA",
)

print(coords)
