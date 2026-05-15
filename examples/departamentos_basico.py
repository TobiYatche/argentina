import argentina as arg

print(arg.departamentos.lookup("06441"))

print(arg.departamentos.lookup("Rosario"))

print(arg.departamentos.lookup("Capital"))

print()

for d in arg.departamentos.por_provincia("Buenos Aires"):
    print(d)

print()

for d in arg.departamentos.listar():
    print(
        d.codigo_departamento,
        d.nombre,
        d.provincia_nombre,
    )
