# Bancos

`argentina.bancos` valida y normaliza identificadores bancarios argentinos:
principalmente **CBU** (Clave Bancaria Uniforme).

```python
import argentina as arg

arg.bancos.limpiar_cbu("2850590940090418135201")     # "2850590940090418135201"
arg.bancos.validar_cbu("2850590940090418135201")     # True/False según dígitos verificadores
arg.bancos.formatear_cbu("2850590940090418135201")   # "28505909-40090418135201" (canónico)
```

## ¿Qué es un CBU?

22 dígitos divididos en dos bloques:

```
XXXXXXXX-XXXXXXXXXXXXXX
└─ 8 ─┘└─ 14 ─┘
banco+sucursal       cuenta+dígitos verificadores
```

El primer bloque identifica banco y sucursal. El segundo identifica la
cuenta y trae **dos dígitos verificadores** (uno por bloque).

`validar_cbu` aplica el algoritmo oficial (multiplicadores y módulo 10).

## Limitación

- Validación **sintáctica**: que los dígitos verificadores sean consistentes.
- No consulta el sistema bancario: no podemos saber si la cuenta existe ni
  a quién pertenece.
- No valida **alias bancarios** (alias.banco) — eso requiere consultar el
  sistema interbancario.

## Otras utilidades

Ver [API reference](../api.md#argentinabancos) para la lista completa de
funciones expuestas por el módulo.
