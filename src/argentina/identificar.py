"""Inspector universal: dado un string cualquiera, deduce qué identificador
argentino es y lo enriquece con metadata.

Compone los módulos `provincias`, `departamentos`, `personas`, `postal`,
`telefonos`, `bancos`, `patentes` — sin red ni dependencias externas.

Ejemplo::

    arg.identificar("20-12345678-3")
    # {'tipo': 'cuit', 'valor': '20123456783', 'valido_dv': False,
    #  'tipo_persona': 'persona_fisica', 'dni': '12345678', 'formato': '20-12345678-3'}

    arg.identificar("C1425ABC")
    # {'tipo': 'cpa', 'valor': 'C1425ABC', 'cp4': '1425',
    #  'provincia': 'Ciudad Autónoma de Buenos Aires'}

    arg.identificar("+54 9 351 1234567")
    # {'tipo': 'telefono', 'celular': True, 'e164': '+5493511234567',
    #  'caracteristica': '351', 'provincia': 'Córdoba'}
"""

from __future__ import annotations

from typing import Any

# Importamos sub-módulos a nivel del archivo: todos son livianos.
from argentina import bancos as _bancos
from argentina import ciudades as _ciudades
from argentina import departamentos as _departamentos
from argentina import patentes as _patentes
from argentina import personas as _personas
from argentina import postal as _postal
from argentina import provincias as _provincias
from argentina import telefonos as _telefonos


def identificar(valor: Any) -> dict | None:
    """Detecta el tipo de identificador y devuelve un dict con metadata.

    Si no se reconoce, devuelve ``None``. Si un mismo string podría
    encajar en varias categorías (raro), se prioriza la más específica.

    Tipos detectables:

    - ``"cuit"`` (con o sin dígito verificador válido)
    - ``"dni"``
    - ``"cbu"``
    - ``"cpa"`` / ``"cp4"``
    - ``"telefono"``
    - ``"patente"``
    - ``"provincia"`` (nombre, código INDEC, ISO, alias)
    - ``"departamento"`` (código INDEC)
    - ``"ciudad"`` (nombre o alias)
    """
    if valor is None:
        return None

    s = str(valor).strip()
    if not s:
        return None

    # === Identificadores con formato estricto (orden importa) ===

    # CUIT/CUIL: 11 dígitos con guiones opcionales
    limpio_cuit = _personas.limpiar_cuit(s) if hasattr(_personas, "limpiar_cuit") else None
    if limpio_cuit and len(limpio_cuit) == 11 and limpio_cuit.isdigit():
        valido_dv = _personas.validar_cuit(s)
        return {
            "tipo": "cuit",
            "valor": limpio_cuit,
            "valido_dv": valido_dv,
            "tipo_persona": _personas.tipo_cuit(s),
            "dni": _personas.extraer_dni_de_cuit(s),
            "formato": _personas.formatear_cuit(limpio_cuit),
        }

    # CBU: 22 dígitos
    limpio_cbu = _bancos.limpiar_cbu(s)
    if limpio_cbu and len(limpio_cbu) == 22:
        return {
            "tipo": "cbu",
            "valor": limpio_cbu,
            "valido_dv": _bancos.validar_cbu(s),
            "banco": _bancos.banco_de_cbu(s),
            "codigo_banco": _bancos.codigo_banco_cbu(s),
            "formato": _bancos.formatear_cbu(s),
        }

    # CPA: letra + 4 dígitos + 3 letras
    if _postal.validar_cpa(s):
        return {
            "tipo": "cpa",
            "valor": _postal.limpiar_codigo_postal(s),
            "cp4": _postal.extraer_cp4(s),
            "provincia": _postal.provincia_por_cpa(s),
            "letra_provincia": _postal.letra_provincia(s),
        }

    # CP4: 4 dígitos exactos
    if _postal.validar_cp4(s):
        return {
            "tipo": "cp4",
            "valor": _postal.limpiar_codigo_postal(s),
        }

    # Patente: vieja, mercosur o moto
    tipo_pat = _patentes.tipo(s)
    if tipo_pat is not None:
        return {
            "tipo": "patente",
            "valor": _patentes.limpiar(s),
            "subtipo": tipo_pat,
            "es_mercosur": _patentes.es_mercosur(s),
            "es_moto": _patentes.es_moto(s),
            "formato": _patentes.formatear(s),
        }

    # Teléfono: valida a 10 dígitos nacionales
    if _telefonos.validar(s):
        return {
            "tipo": "telefono",
            "valor": _telefonos.limpiar(s),
            "celular": _telefonos.es_celular(s),
            "e164": _telefonos.normalizar_e164(s),
            "caracteristica": _telefonos.extraer_caracteristica(s),
            "provincia": _telefonos.provincia_por_caracteristica(s),
        }

    # DNI: 7 u 8 dígitos
    if _personas.validar_dni(s):
        limpio_dni = _personas.limpiar_dni(s)
        return {
            "tipo": "dni",
            "valor": limpio_dni,
            "formato": _personas.formatear_dni(limpio_dni),
        }

    # === Identificadores territoriales (lookup) ===
    # Orden: ciudad → departamento → provincia.
    # "Rosario" matchea ciudad antes que el departamento homónimo (más útil
    # en el caso común — caja de texto libre).

    # Ciudad (nombre o alias)
    c = _ciudades.lookup(s)
    if c is not None:
        return {
            "tipo": "ciudad",
            "nombre": c.nombre,
            "provincia": c.provincia_nombre,
            "poblacion_2022": c.poblacion_2022,
            "lat": c.lat,
            "lon": c.lon,
        }

    # Departamento (código de 5 dígitos o nombre único)
    d = _departamentos.lookup(s)
    if d is not None:
        return {
            "tipo": "departamento",
            "codigo": d.codigo_departamento,
            "nombre": d.nombre,
            "provincia": d.provincia_nombre,
            "provincia_codigo": d.provincia_codigo,
        }

    # Provincia (nombre, INDEC, ISO, alias)
    p = _provincias.lookup(s)
    if p is not None:
        return {
            "tipo": "provincia",
            "nombre": p.nombre,
            "codigo_indec": p.codigo_indec,
            "iso_id": p.iso_id,
            "region": p.region,
            "capital": p.capital,
            "poblacion_2022": p.poblacion_2022,
        }

    return None


__all__ = ["identificar"]
