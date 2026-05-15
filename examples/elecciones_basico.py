import argentina as arg

# Core (sin red, sin deps externas)
print(arg.elecciones.limpiar_mesa("Mesa 01234"))
print(arg.elecciones.limpiar_circuito(" 12-A "))

print(arg.elecciones.normalizar_categoria("Presidente"))
print(arg.elecciones.normalizar_categoria("diputado"))

print(arg.elecciones.normalizar_tipo_eleccion("PASO"))
print(arg.elecciones.normalizar_tipo_eleccion("segunda vuelta"))

print(arg.elecciones.validar_anio_eleccion(2023))
print(arg.elecciones.validar_anio_eleccion(1900))

# Wrapper opcional para APIs (instalar con `pip install "argentina[elecciones]"`)
print(arg.elecciones.api.disponible())
