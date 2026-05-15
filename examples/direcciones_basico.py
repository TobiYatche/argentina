import argentina as arg

direccion = "Av. Santa Fe 3253 Piso 2 Depto B"

print(arg.direcciones.normalizar(direccion))
print(arg.direcciones.extraer_calle(direccion))
print(arg.direcciones.extraer_altura(direccion))
print(arg.direcciones.extraer_piso(direccion))
print(arg.direcciones.extraer_departamento(direccion))
print(arg.direcciones.tiene_altura(direccion))
print(arg.direcciones.parsear(direccion))
