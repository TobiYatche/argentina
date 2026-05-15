import argentina as arg

print(arg.salud.normalizar_sexo("femenino"))
print(arg.salud.normalizar_sexo("varón"))

print(arg.salud.normalizar_tipo_documento("dni"))
print(arg.salud.limpiar_matricula("M.P. 12345"))

print(arg.salud.grupo_etario(3))
print(arg.salud.edad_en_anios("2015-05-10", "2026-05-12"))
