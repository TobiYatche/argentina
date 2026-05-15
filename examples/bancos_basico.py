import argentina as arg

cbu = "0170 0001 4000 0001 2345 67"

print(arg.bancos.limpiar_cbu(cbu))

print(
    arg.bancos.validar_cbu(
        "2850590940090418135201"
    )
)

print(
    arg.bancos.formatear_cbu(
        "2850590940090418135201"
    )
)

print(
    arg.bancos.codigo_banco_cbu(
        "0170099120000067797370"
    )
)

print(
    arg.bancos.banco_por_cbu(
        "0170099120000067797370"
    )
)

print(
    arg.bancos.limpiar_alias(
        " Mi.Alias.CBU "
    )
)

print(
    arg.bancos.validar_alias(
        "MI.ALIAS.CBU"
    )
)

print(
    arg.bancos.validar_cvu(
        "0000003100000000000001"
    )
)
