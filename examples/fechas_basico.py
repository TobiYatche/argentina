import argentina as arg

print(arg.fechas.parsear_fecha("31/12/2024"))
print(arg.fechas.fecha_iso("31/12/2024"))
print(arg.fechas.es_fecha_valida("31/12/2024"))

print(
    arg.fechas.edad_en_anios(
        "10/05/2015",
        "12/05/2026",
    )
)

print(arg.fechas.anio_lectivo("15/02/2024"))
print(arg.fechas.cohorte_nacimiento("10/05/2015"))
print(arg.fechas.mes_anio("31/12/2024"))
