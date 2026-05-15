import argentina as arg

print(arg.educacion.limpiar_cue("0201234-00"))
print(arg.educacion.validar_cue("020123400"))

print(arg.educacion.limpiar_cueanexo("0201234-01"))
print(arg.educacion.validar_cueanexo("020123401"))

print(
    arg.educacion.extraer_jurisdiccion_cue(
        "020123400"
    )
)

print(arg.educacion.normalizar_sector("público"))
print(arg.educacion.normalizar_ambito("urbano"))
print(arg.educacion.normalizar_nivel("secundario"))
