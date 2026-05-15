import argentina as arg

# Lookup directo
print(arg.ciudades.lookup("Rosario"))
print(arg.ciudades.lookup("CABA"))
print(arg.ciudades.lookup("mardel"))

print()

# Top 5 ciudades más pobladas según Censo 2022
print("Top 5 ciudades:")
for c in arg.ciudades.top(5):
    print(f"  {c.nombre:30s}  {c.poblacion_2022:>10,}".replace(",", "."))

print()

# Ciudades incluidas en una provincia
print("Ciudades de Buenos Aires en el set:")
for c in arg.ciudades.por_provincia("Buenos Aires"):
    print(f"  {c.nombre}")

print()

# Cruce con argentina.provincias
p = arg.provincias.CORDOBA
print(f"Provincia de {p.nombre}:")
print(f"  capital: {p.capital}  ({p.capital_lat}, {p.capital_lon})")
print(f"  población provincia (Censo 2022): {p.poblacion_2022:,}".replace(",", "."))
