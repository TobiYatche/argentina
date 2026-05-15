import argentina as arg

print(f"Buenos Aires → Córdoba:   {arg.geo.distancia('Buenos Aires', 'Córdoba'):>7.1f} km")
print(f"Buenos Aires → Mendoza:   {arg.geo.distancia('Buenos Aires', 'Mendoza'):>7.1f} km")
print(f"Buenos Aires → Ushuaia:   {arg.geo.distancia('Buenos Aires', 'Ushuaia'):>7.1f} km")
print(f"Ushuaia → La Quiaca:      {arg.geo.distancia('Ushuaia', arg.ciudades.lookup('San Salvador de Jujuy')):>7.1f} km")
print(f"Rosario ↔ Córdoba:        {arg.geo.distancia('Rosario', 'Córdoba'):>7.1f} km")
