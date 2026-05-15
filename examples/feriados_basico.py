import argentina as arg

feriados = arg.feriados.obtener(2026)

print(feriados[:3])
print(arg.feriados.es_feriado("2026-05-25"))
print(arg.feriados.detalle("2026-05-25"))
print(arg.feriados.proximo("2026-05-01"))
