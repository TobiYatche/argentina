import argentina as arg

print(arg.personas.limpiar_dni("12.345.678"))
print(arg.personas.validar_dni("12.345.678"))

print(arg.personas.limpiar_cuit("20-12345678-3"))
print(arg.personas.validar_cuit("20-12345678-3"))
print(arg.personas.extraer_dni_de_cuit("20-12345678-3"))

print(arg.personas.normalizar_nombre(" María   Laura "))
print(arg.personas.primer_nombre("María Laura"))
print(arg.personas.apellido_principal("Pérez Gómez"))

print(arg.personas.calcular_digito_cuit("2012345678"))
print(arg.personas.validar_cuit("20-12345678-6"))
print(arg.personas.validar_cuit("20-12345678-3"))
print(arg.personas.tipo_cuit("20-12345678-6"))
print(arg.personas.formatear_dni("12345678"))
print(arg.personas.formatear_cuit("20123456786"))

print(arg.personas.estimar_año_nacimiento("30.000.000"))
print(arg.personas.estimar_año_nacimiento(45_123_456))
print(arg.personas.estimar_dni(1990))
print(arg.personas.rango_dni_de_año(2000))
