"""Formateo de salida para datos argentinos.

Punto único de entrada para "¿cómo formateo X para mostrar?". Agrupa
funciones nuevas (teléfonos, pesos, código postal, fechas) y reexporta
las funciones ``formatear_*`` que ya viven en otros módulos
(``personas``, ``bancos``, ``patentes``).

Las implementaciones canónicas siguen en sus módulos. ``formato`` solo
agrega un alias descubrible — no duplica nada.

Convención: todas las funciones devuelven ``str`` o ``None`` si el input
no es formateable. No levantan excepciones para entradas inválidas
(consistente con ``limpiar_*`` y ``validar_*`` del resto del paquete).
"""

from __future__ import annotations

from datetime import date, datetime


# ---------------------------------------------------------------------------
# Nuevas: teléfono, pesos, código postal, fecha
# ---------------------------------------------------------------------------


_ESTILOS_TELEFONO = {"nacional", "e164", "internacional"}


def telefono(valor: str | int | None, *, estilo: str = "nacional") -> str | None:
    """Formatea un teléfono argentino.

    Estilos:

    - ``"nacional"`` (default): ``"(011) 4040-4040"`` para fijos AMBA,
      ``"(0351) 444-5555"`` para característica de 3 dígitos.
    - ``"e164"``: ``"+5491140404040"`` (celular) o ``"+541140404040"`` (fijo).
    - ``"internacional"``: ``"+54 9 11 4040-4040"`` o ``"+54 11 4040-4040"``.

    Devuelve ``None`` si el número no es válido (mismo criterio que
    ``arg.telefonos.validar``).
    """
    if estilo not in _ESTILOS_TELEFONO:
        raise ValueError(
            f"estilo inválido: {estilo!r}. Válidos: {sorted(_ESTILOS_TELEFONO)}"
        )

    from argentina import telefonos

    if not telefonos.validar(valor):
        return None

    nacional = telefonos._normalizar_nacional(valor)
    if nacional is None or len(nacional) != 10:
        return None

    es_cel = telefonos.es_celular(valor)

    if estilo == "e164":
        return telefonos.normalizar_e164(valor, celular=es_cel)

    # Partir en (caracteristica, resto) según AMBA o no.
    if nacional.startswith("11"):
        area = nacional[:2]
        resto = nacional[2:]  # 8 dígitos
    else:
        area = nacional[:3]
        resto = nacional[3:]  # 7 dígitos

    if estilo == "nacional":
        if len(resto) == 8:
            resto_fmt = f"{resto[:4]}-{resto[4:]}"
        else:  # 7
            resto_fmt = f"{resto[:3]}-{resto[3:]}"
        return f"(0{area}) {resto_fmt}"

    # internacional
    prefijo = "+54 9" if es_cel else "+54"
    if len(resto) == 8:
        resto_fmt = f"{resto[:4]}-{resto[4:]}"
    else:
        resto_fmt = f"{resto[:3]}-{resto[3:]}"
    return f"{prefijo} {area} {resto_fmt}"


def pesos(
    valor: float | int | str | None,
    *,
    decimales: int = 0,
    simbolo: str = "$ ",
) -> str | None:
    """Formatea un monto en pesos argentinos.

    Separador de miles: ``.`` — separador decimal: ``,`` (convención
    argentina). El símbolo va antes del número, separado por espacio por
    default.

    Parameters
    ----------
    valor : float | int | str | None
        Monto a formatear. Strings se intentan convertir con ``float``.
    decimales : int
        Cantidad de decimales a mostrar. Default ``0`` (montos enteros).
    simbolo : str
        Prefijo. Default ``"$ "``. Pasar ``""`` para omitirlo.

    Examples
    --------
    >>> import argentina as arg
    >>> arg.formato.pesos(1_500_000)
    '$ 1.500.000'
    >>> arg.formato.pesos(1_500_000.5, decimales=2)
    '$ 1.500.000,50'
    >>> arg.formato.pesos(-1000)
    '-$ 1.000'
    """
    if valor is None:
        return None
    if decimales < 0:
        raise ValueError(f"decimales debe ser >= 0, recibí {decimales}")

    try:
        monto = float(valor)
    except (TypeError, ValueError):
        return None

    negativo = monto < 0
    monto_abs = abs(monto)
    fmt = f"{monto_abs:,.{decimales}f}"
    # En Python `,` es miles y `.` decimal. Invertir al formato argentino.
    fmt = fmt.replace(",", "§").replace(".", ",").replace("§", ".")

    signo = "-" if negativo else ""
    return f"{signo}{simbolo}{fmt}"


def codigo_postal(valor: str | int | None) -> str | None:
    """Formatea un código postal argentino (CP4 o CPA).

    - CP4 (4 dígitos) → devuelto tal cual: ``"1414"``.
    - CPA (1 letra + 4 dígitos + 3 letras) → mayúsculas, sin separadores:
      ``"C1414BAA"``.

    Devuelve ``None`` si el input no es un código postal válido.
    """
    from argentina import postal

    limpio = postal.limpiar_codigo_postal(valor)
    if limpio is None:
        return None

    if postal.validar_cpa(limpio):
        return limpio  # ya viene en mayúsculas y sin separadores

    if postal.validar_cp4(limpio):
        return limpio  # 4 dígitos

    return None


_ESTILOS_FECHA = {"corto", "largo", "iso"}

_MESES_ES = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
)


def fecha(
    valor: str | date | datetime | None,
    *,
    estilo: str = "corto",
) -> str | None:
    """Formatea una fecha argentina.

    Estilos:

    - ``"corto"`` (default): ``"13/05/2026"``.
    - ``"largo"``: ``"13 de mayo de 2026"`` (meses en español).
    - ``"iso"``: ``"2026-05-13"``.

    Acepta cualquier formato que entienda ``arg.fechas.parsear_fecha``
    (``date``, ``datetime``, strings ``dd/mm/aaaa``, ISO, etc.). Devuelve
    ``None`` si no se puede parsear.
    """
    if estilo not in _ESTILOS_FECHA:
        raise ValueError(
            f"estilo inválido: {estilo!r}. Válidos: {sorted(_ESTILOS_FECHA)}"
        )

    from argentina import fechas

    f = fechas.parsear_fecha(valor)
    if f is None:
        return None

    if estilo == "corto":
        return f.strftime("%d/%m/%Y")
    if estilo == "iso":
        return f.isoformat()
    # largo
    mes = _MESES_ES[f.month - 1]
    return f"{f.day} de {mes} de {f.year}"


# ---------------------------------------------------------------------------
# Reexports: la implementación canónica vive en cada módulo de origen.
# Se exponen acá como funciones (no aliases module-level) para que tengan
# firma y docstring propios. El cuerpo delega sin reimplementar nada.
# ---------------------------------------------------------------------------


def dni(valor: str | int | None) -> str | None:
    """Formatea DNI con puntos: ``"12345678"`` → ``"12.345.678"``.

    Reexport de :func:`argentina.personas.formatear_dni`.
    """
    from argentina import personas
    return personas.formatear_dni(valor)


def cuit(valor: str | int | None) -> str | None:
    """Formatea CUIT/CUIL como ``XX-XXXXXXXX-X``.

    Reexport de :func:`argentina.personas.formatear_cuit`.
    """
    from argentina import personas
    return personas.formatear_cuit(valor)


def cbu(valor: str | int | None) -> str | None:
    """Formatea CBU como ``XXXXXXXX-XXXXXXXXXXXXXX``.

    Reexport de :func:`argentina.bancos.formatear_cbu`.
    """
    from argentina import bancos
    return bancos.formatear_cbu(valor)


def patente(valor: str | None) -> str | None:
    """Formatea patente con separadores canónicos.

    Reexport de :func:`argentina.patentes.formatear`.
    """
    from argentina import patentes
    return patentes.formatear(valor)


def parsear_pesos(valor):
    """Parsea un monto en pesos a ``float``: inverso de :func:`pesos`.

    Reexport de :func:`argentina.montos.parsear`.
    """
    from argentina import montos
    return montos.parsear(valor)


__all__ = [
    "telefono",
    "pesos",
    "codigo_postal",
    "fecha",
    "dni",
    "cuit",
    "cbu",
    "patente",
    "parsear_pesos",
]
