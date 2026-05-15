import argentina as arg

print("Aglomerados EPH:", len(arg.aglomerados))
print()
print("Por provincia: Buenos Aires")
for a in arg.aglomerados.por_provincia("Buenos Aires"):
    print(f"  {a.codigo:>3}  {a.nombre}")
print()
print("Lookup directo:")
print(" ", arg.aglomerados.lookup(32))
print(" ", arg.aglomerados.lookup("Mar del Plata"))
