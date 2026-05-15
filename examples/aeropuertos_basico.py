import argentina as arg

# Lookup directo
print(arg.aeropuertos.lookup("EZE"))
print(arg.aeropuertos.lookup("Bariloche"))
print()

# Por provincia
print("Aeropuertos en Chubut:")
for a in arg.aeropuertos.por_provincia("Chubut"):
    print(f"  {a.iata}/{a.icao}  {a.nombre}  ({a.tipo})")

print()

# Solo internacionales
print(f"Aeropuertos internacionales: {len(arg.aeropuertos.internacionales())}")
for a in arg.aeropuertos.internacionales():
    print(f"  {a.iata}  {a.ciudad}")

print()

# Distancia entre aeropuertos (con geo.distancia y las coordenadas embebidas)
eze = arg.aeropuertos.lookup("EZE")
ush = arg.aeropuertos.lookup("USH")
d = arg.geo.distancia((eze.lat, eze.lon), (ush.lat, ush.lon))
print(f"EZE → USH: {d:.0f} km")
