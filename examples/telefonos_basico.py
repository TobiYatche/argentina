import argentina as arg

print(arg.telefonos.limpiar("+54 9 11 1234-5678"))
print(arg.telefonos.validar("+54 9 11 1234-5678"))

print(arg.telefonos.extraer_caracteristica("+54 9 351 1234567"))

print(arg.telefonos.es_celular("+54 9 11 1234-5678"))
print(arg.telefonos.es_celular("011 15 1234-5678"))

print(arg.telefonos.normalizar_e164("+54 9 11 1234-5678"))
print(arg.telefonos.normalizar_e164("011 4321-1234"))
