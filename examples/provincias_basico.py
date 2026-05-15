import argentina as arg

print(arg.provincias.BUENOS_AIRES)
print(arg.provincias.CORDOBA)
print(arg.provincias.CABA)

p = arg.provincias.lookup("PBA")
print(p.nombre)
print(p.codigo_indec)
print(p.iso_id)
print(p.region)
print(p.capital)

print(arg.provincias.lookup("CABA"))
print(arg.provincias.lookup("14"))
print(arg.provincias.lookup("AR-X"))

for provincia in arg.provincias.listar():
    print(provincia.nombre, provincia.codigo_indec, provincia.iso_id)
