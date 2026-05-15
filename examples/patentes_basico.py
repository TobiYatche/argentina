import argentina as arg

for p in ["abc 123", "AB 123 CD", "123 ABC", "A999BBB", "pepe"]:
    print(f"{p!r:15}  tipo={arg.patentes.tipo(p)!r:18}  formato={arg.patentes.formatear(p)!r}")
