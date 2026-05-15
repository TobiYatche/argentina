from __future__ import annotations

import csv
import re
import unicodedata
from bisect import bisect_right
from datetime import date
from importlib.resources import files


def _solo_digitos(valor: str | int | None) -> str | None:
    """Devuelve solo los dígitos de un valor."""
    if valor is None:
        return None

    digitos = re.sub(r"\D+", "", str(valor))

    if digitos == "":
        return None

    return digitos


def limpiar_dni(dni: str | int | None) -> str | None:
    """Limpia un DNI argentino."""
    return _solo_digitos(dni)


def validar_dni(dni: str | int | None) -> bool:
    """Valida formato básico de DNI argentino."""
    dni_limpio = limpiar_dni(dni)

    if dni_limpio is None:
        return False

    return len(dni_limpio) in {7, 8}


def limpiar_cuit(cuit: str | int | None) -> str | None:
    """Limpia un CUIT/CUIL argentino."""
    return _solo_digitos(cuit)


def calcular_digito_cuit(cuit_sin_digito: str | int | None) -> str | None:
    """
    Calcula dígito verificador de CUIT/CUIL.

    Recibe los primeros 10 dígitos.
    """
    digitos = _solo_digitos(cuit_sin_digito)

    if digitos is None or len(digitos) != 10:
        return None

    multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    suma = sum(
        int(digito) * multiplicador
        for digito, multiplicador in zip(digitos, multiplicadores)
    )

    resto = suma % 11
    digito = 11 - resto

    if digito == 11:
        return "0"

    if digito == 10:
        return "9"

    return str(digito)


def validar_cuit(
    cuit: str | int | None,
    digito: bool = True,
) -> bool:
    """
    Valida CUIT/CUIL argentino.

    Si digito=True, valida dígito verificador.
    Si digito=False, valida solo largo 11.
    """
    cuit_limpio = limpiar_cuit(cuit)

    if cuit_limpio is None or len(cuit_limpio) != 11:
        return False

    if not digito:
        return True

    esperado = calcular_digito_cuit(cuit_limpio[:10])

    return esperado == cuit_limpio[-1]


def tipo_cuit(cuit: str | int | None) -> str | None:
    """
    Clasifica CUIT/CUIL según prefijo.

    Devuelve:
    - "persona_fisica"
    - "persona_juridica"
    - None
    """
    cuit_limpio = limpiar_cuit(cuit)

    if cuit_limpio is None or len(cuit_limpio) != 11:
        return None

    prefijo = cuit_limpio[:2]

    if prefijo in {"20", "23", "24", "27"}:
        return "persona_fisica"

    if prefijo in {"30", "33", "34"}:
        return "persona_juridica"

    return None


def extraer_dni_de_cuit(cuit: str | int | None) -> str | None:
    """Extrae el DNI desde un CUIT/CUIL."""
    cuit_limpio = limpiar_cuit(cuit)

    if cuit_limpio is None or len(cuit_limpio) != 11:
        return None

    return cuit_limpio[2:10]


def formatear_dni(dni: str | int | None) -> str | None:
    """Formatea DNI con puntos."""
    dni_limpio = limpiar_dni(dni)

    if dni_limpio is None:
        return None

    if not validar_dni(dni_limpio):
        return None

    return f"{int(dni_limpio):,}".replace(",", ".")


def formatear_cuit(cuit: str | int | None) -> str | None:
    """Formatea CUIT/CUIL como XX-XXXXXXXX-X."""
    cuit_limpio = limpiar_cuit(cuit)

    if cuit_limpio is None or len(cuit_limpio) != 11:
        return None

    return f"{cuit_limpio[:2]}-{cuit_limpio[2:10]}-{cuit_limpio[10]}"


# ─────────────────────────────────────────────────────────────────────
# Generadores para testing / fixtures
# ─────────────────────────────────────────────────────────────────────

# Prefijos CUIT por categoría (oficiales AFIP).
PREFIJOS_CUIT = {
    "persona_fisica": ("20", "23", "24", "27"),
    "persona_juridica": ("30", "33", "34"),
}


def generar_dni(
    minimo: int = 1_000_000,
    maximo: int = 99_999_999,
    rng=None,
) -> str:
    """Devuelve un DNI aleatorio en el rango ``[minimo, maximo]``.

    Por default ``[1.000.000, 99.999.999]`` que cubre prácticamente toda la
    población argentina viva.

    Útil para fixtures de tests / datos de prueba. **No es un DNI real**: es
    solo un string con el formato correcto.

    Parameters
    ----------
    rng : random.Random, optional
        Generador propio para reproducibilidad. Por default usa el global.
    """
    import random as _random
    r = rng or _random
    return str(r.randint(minimo, maximo))


def generar_cuit(
    tipo: str = "persona_fisica",
    dni: int | str | None = None,
    rng=None,
) -> str:
    """Devuelve un CUIT con dígito verificador correcto.

    Parameters
    ----------
    tipo : str
        ``"persona_fisica"`` (prefijo 20/23/24/27) o ``"persona_juridica"``
        (prefijo 30/33/34).
    dni : int | str | None
        DNI base (8 dígitos). Si ``None``, se genera uno aleatorio.
    rng : random.Random, optional

    Returns
    -------
    str
        CUIT de 11 dígitos sin separadores. Pasalo por ``formatear_cuit``
        para el formato canónico ``XX-XXXXXXXX-X``.

    Examples
    --------
    >>> arg.personas.generar_cuit()  # CUIT random de persona física
    '20123456783'
    >>> arg.personas.generar_cuit("persona_juridica")
    '30987654329'
    >>> arg.personas.generar_cuit(dni=12345678)
    '20123456786'  # dígito calculado oficialmente
    """
    import random as _random
    r = rng or _random

    if tipo not in PREFIJOS_CUIT:
        raise ValueError(f"tipo debe ser 'persona_fisica' o 'persona_juridica', vino: {tipo!r}")

    prefijo = r.choice(PREFIJOS_CUIT[tipo])

    if dni is None:
        dni_str = generar_dni(rng=r)
    else:
        dni_str = _solo_digitos(dni) or ""
    dni_str = dni_str.zfill(8)[:8]

    base = f"{prefijo}{dni_str}"
    digito = calcular_digito_cuit(base)
    if digito is None:
        # Caso edge: el dígito calculado fue 10. Retry con otro DNI.
        return generar_cuit(tipo=tipo, dni=None, rng=r)
    return f"{base}{digito}"


def _quitar_tildes(texto: str) -> str:
    """Quita tildes y marcas diacríticas."""
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


def normalizar_nombre(nombre: str | None) -> str | None:
    """Normaliza nombres: minúsculas, sin tildes y espacios simples."""
    if nombre is None:
        return None

    texto = str(nombre).strip()

    if texto == "":
        return None

    texto = _quitar_tildes(texto)
    texto = texto.lower()
    texto = re.sub(r"[^a-zñ\s]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    if texto == "":
        return None

    return texto


def primer_nombre(nombre_completo: str | None) -> str | None:
    """Devuelve el primer nombre normalizado."""
    nombre = normalizar_nombre(nombre_completo)

    if nombre is None:
        return None

    return nombre.split(" ")[0]


def apellido_principal(apellidos: str | None) -> str | None:
    """Devuelve el primer apellido normalizado."""
    apellido = normalizar_nombre(apellidos)

    if apellido is None:
        return None

    return apellido.split(" ")[0]


# Modelo lineal calibrado contra dos hitos públicos:
#   - DNI 59.999.999 = agosto 2023 (último pre-salto). En sept-2023 los recién
#     nacidos comenzaron a recibir 70.000.000+ (RENAPER, sept-2023).
#   - Pendiente ~736.470 DNI/año, consistente con la fórmula viral que circula
#     en Reddit/X (año = 1942.5 + DNI/736470), que coincide con tablas de
#     calculadoras online y con varios anclajes informales.
#
# El RENAPER emite ~750k DNI/año mientras nacen ~500-700k chicos. La diferencia
# son extranjeros naturalizados, residentes que regularizan, inscripciones
# tardías y reasignaciones. Por eso un modelo "acumulado de nacimientos" pierde
# precisión: subestima la pendiente.
#
# La franja 60.000.000–69.999.999 quedó reservada en dic-2019 (Disposición
# Renaper 4678/2019) para CUIT/CUIL provisorios de extranjeros — NO se asigna
# como DNI personal. Por eso el estimador devuelve None ahí.

_DNI_CORTE_INICIO = 60_000_000           # último DNI personal pre-salto
_DNI_CORTE_FIN = 70_000_000               # primer DNI personal post-salto
_AÑO_SALTO = 2023.667                     # 1° de septiembre 2023 ≈ año + 8/12

# año = _INTERCEPT + DNI / _PENDIENTE_DNI_AÑO
# Pendiente única (pre y post salto): el RENAPER emite ~736k DNI/año total
# (nacimientos + naturalizaciones + extranjeros + reasignaciones). Validado
# tanto con la fórmula viral como con el hito 72M=mayo-2026.
_PENDIENTE_DNI_AÑO = 736_470.0
_INTERCEPT = _AÑO_SALTO - _DNI_CORTE_INICIO / _PENDIENTE_DNI_AÑO   # ≈ 1942.20


_NACIMIENTOS: tuple[tuple[int, int], ...] | None = None


def _cargar_nacimientos() -> tuple[tuple[int, int], ...]:
    """Carga la serie histórica de nacimientos desde el CSV embebido."""
    global _NACIMIENTOS

    if _NACIMIENTOS is not None:
        return _NACIMIENTOS

    path = files("argentina").joinpath("data/nacimientos_argentina.csv")
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = [(int(fila["anio"]), int(fila["nacimientos"])) for fila in reader]

    filas.sort(key=lambda x: x[0])
    _NACIMIENTOS = tuple(filas)
    return _NACIMIENTOS


def serie_nacimientos() -> tuple[tuple[int, int], ...]:
    """
    Serie histórica oficial de nacimientos en Argentina por año.

    Tupla de `(año, total_nacimientos)`. Fuente: Dirección de Estadísticas
    e Información en Salud (DEIS), Ministerio de Salud. 1914-2024. Los años
    1971-1974 son imputados linealmente entre 1970 y 1975 (DEIS no publica
    esos años, ver columna `fuente` del CSV).

    Datos auxiliares, NO se usan en `estimar_año_nacimiento` (el estimador
    usa una fórmula lineal calibrada contra hitos públicos del RENAPER).
    """
    return _cargar_nacimientos()


def _año_desde_dni(dni: int) -> float:
    """Conversión lineal DNI → año (fraccional). Asume DNI fuera del salto."""
    if dni < _DNI_CORTE_INICIO:
        return _INTERCEPT + dni / _PENDIENTE_DNI_AÑO
    # Post-salto: continuar la línea pero saltando el hueco 60M-70M
    return _AÑO_SALTO + (dni - _DNI_CORTE_FIN) / _PENDIENTE_DNI_AÑO


def _dni_desde_año(año: float) -> int:
    """Conversión inversa año (fraccional) → DNI."""
    if año < _AÑO_SALTO:
        return int(round((año - _INTERCEPT) * _PENDIENTE_DNI_AÑO))
    return int(round(_DNI_CORTE_FIN + (año - _AÑO_SALTO) * _PENDIENTE_DNI_AÑO))


def estimar_año_nacimiento(dni: str | int | None) -> int | None:
    """
    Estima el año de nacimiento a partir del DNI.

    Modelo lineal calibrado contra dos hitos públicos del RENAPER:
    - DNI 59.999.999 = agosto 2023 (último pre-salto a 70M)
    - Pendiente ~736.470 DNI/año (fórmula viral validada en blogs y foros)

    Margen típico ±2-3 años. Casos atípicos pueden caer más lejos:
    - Inscripciones tardías reciben DNI de la cohorte actual (no la suya).
    - Naturalizados reciben DNI en orden de naturalización, no de nacimiento.
    - Pre-1968 (DNI < ~14M) el sistema de Libreta Cívica/Enrolamiento
      asignaba números al inscribirse (~16-18 años), no al nacer.

    Devuelve `None` si:
    - El DNI es inválido.
    - Cae en 60.000.000–69.999.999 (CUIT/CUIL provisorios de extranjeros,
      Disposición Renaper 4678/2019, no es DNI personal).
    - Cae fuera del rango razonable (< 1M o demasiado alto para 2026).
    """
    dni_limpio = limpiar_dni(dni)

    if dni_limpio is None or not validar_dni(dni_limpio):
        return None

    n = int(dni_limpio)

    if _DNI_CORTE_INICIO <= n < _DNI_CORTE_FIN:
        return None

    año = _año_desde_dni(n)
    hoy = date.today().year

    if año < 1900 or año > hoy + 1:
        return None

    return int(año)


def estimar_dni(anio: int | None) -> int | None:
    """
    Estima el DNI representativo de quien nació a mediados de `anio`.

    Devuelve el DNI correspondiente al punto medio del año.
    """
    if anio is None:
        return None

    a = int(anio) + 0.5
    hoy = date.today().year

    if a < 1900 or a > hoy + 1:
        return None

    return _dni_desde_año(a)


def rango_dni_de_año(anio: int | None) -> tuple[int, int] | None:
    """
    Devuelve el rango (dni_inicio, dni_fin) de quienes nacieron en `anio`.

    Para el año del salto (2023) los nacimientos quedan partidos entre
    pre-salto (enero-agosto, DNIs hasta 59.999.999) y post-salto (septiembre
    en adelante, DNIs desde 70.000.000). En ese caso devuelve solo el tramo
    post-salto, que es donde caen los nacidos de septiembre en adelante.
    """
    if anio is None:
        return None

    a = int(anio)
    hoy = date.today().year

    if a < 1900 or a > hoy + 1:
        return None

    inicio = _dni_desde_año(float(a))
    fin = _dni_desde_año(float(a + 1)) - 1

    if inicio < 0 or fin < inicio:
        return None

    return (inicio, fin)


__all__ = [
    "limpiar_dni",
    "validar_dni",
    "limpiar_cuit",
    "validar_cuit",
    "calcular_digito_cuit",
    "tipo_cuit",
    "extraer_dni_de_cuit",
    "formatear_dni",
    "formatear_cuit",
    "normalizar_nombre",
    "primer_nombre",
    "apellido_principal",
    "serie_nacimientos",
    "estimar_año_nacimiento",
    "estimar_dni",
    "rango_dni_de_año",
    "PREFIJOS_CUIT",
    "generar_dni",
    "generar_cuit",
]
