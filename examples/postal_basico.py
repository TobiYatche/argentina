import argentina as arg

print(arg.postal.limpiar_codigo_postal(" c1425 abc "))
print(arg.postal.validar_cp4("1425"))
print(arg.postal.validar_cpa("C1425ABC"))
print(arg.postal.tipo_codigo_postal("C1425ABC"))
print(arg.postal.extraer_cp4("C1425ABC"))
print(arg.postal.letra_provincia("C1425ABC"))
print(arg.postal.provincia_por_cpa("C1425ABC"))
print(arg.postal.validar_cpa_provincia("X5000AAA", "Córdoba"))
