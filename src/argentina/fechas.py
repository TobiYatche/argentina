from __future__ import annotations

from datetime import date, datetime


FORMATOS_FECHA = (
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d/%m/%y",
    "%d-%m-%y",
)


def parsear_fecha(valor: str | date | datetime | None) -> date | None:
    """Parsea fechas frecuentes en datos argentinos."""
    if valor is None:
        return None

    if isinstance(valor, datetime):
        return valor.date()

    if isinstance(valor, date):
        return valor

    texto = str(valor).strip()

    if texto == "":
        return None

    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(texto[:10], formato).date()
        except ValueError:
            continue

    return None


def es_fecha_valida(valor: str | date | datetime | None) -> bool:
    """Indica si una fecha puede parsearse."""
    return parsear_fecha(valor) is not None


def fecha_iso(valor: str | date | datetime | None) -> str | None:
    """Devuelve fecha en formato ISO YYYY-MM-DD."""
    fecha = parsear_fecha(valor)

    if fecha is None:
        return None

    return fecha.isoformat()


def edad_en_anios(
    fecha_nacimiento: str | date | datetime | None,
    fecha_referencia: str | date | datetime | None = None,
) -> int | None:
    """Calcula edad en años completos."""
    nacimiento = parsear_fecha(fecha_nacimiento)

    if fecha_referencia is None:
        referencia = date.today()
    else:
        referencia = parsear_fecha(fecha_referencia)

    if nacimiento is None or referencia is None:
        return None

    if nacimiento > referencia:
        return None

    edad = referencia.year - nacimiento.year

    if (referencia.month, referencia.day) < (
        nacimiento.month,
        nacimiento.day,
    ):
        edad -= 1

    return edad


def cohorte_nacimiento(
    fecha_nacimiento: str | date | datetime | None,
) -> int | None:
    """Devuelve año de nacimiento."""
    fecha = parsear_fecha(fecha_nacimiento)

    if fecha is None:
        return None

    return fecha.year


def anio_lectivo(
    fecha: str | date | datetime | None,
    mes_inicio: int = 3,
) -> int | None:
    """
    Devuelve año lectivo argentino.

    Por default, el año lectivo inicia en marzo.
    Enero y febrero se asignan al año lectivo anterior.
    """
    fecha_parseada = parsear_fecha(fecha)

    if fecha_parseada is None:
        return None

    if fecha_parseada.month < mes_inicio:
        return fecha_parseada.year - 1

    return fecha_parseada.year


def mes_anio(
    fecha: str | date | datetime | None,
) -> str | None:
    """Devuelve período mensual en formato YYYY-MM."""
    fecha_parseada = parsear_fecha(fecha)

    if fecha_parseada is None:
        return None

    return f"{fecha_parseada.year:04d}-{fecha_parseada.month:02d}"


__all__ = [
    "FORMATOS_FECHA",
    "parsear_fecha",
    "es_fecha_valida",
    "fecha_iso",
    "edad_en_anios",
    "cohorte_nacimiento",
    "anio_lectivo",
    "mes_anio",
]
