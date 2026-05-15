import argentina as arg

# Lookup directo
print(arg.universidades.lookup("UBA"))
print(arg.universidades.lookup("unlp"))
print()

# Universidades por provincia
print("Universidades en Córdoba:")
for u in arg.universidades.por_provincia("Córdoba"):
    print(f"  {u.sigla:8s}  {u.nombre}  ({u.anio_fundacion})")

print()

# Universidades creadas a partir de 2000
print("Universidades nacionales creadas desde 2009:")
for u in arg.universidades.por_anio(desde=2009):
    print(f"  {u.anio_fundacion}  {u.sigla:10s}  {u.sede}")
