import argentina as arg

for v in [
    "20-12345678-6",
    "2850590940090418135201",
    "C1425ABC",
    "1425",
    "+54 9 351 1234567",
    "AB 123 CD",
    "06427",
    "AR-X",
    "PBA",
    "Rosario",
    "Córdoba",
]:
    r = arg.identificar(v)
    print(f"{v!r:30}  →  {r}")
