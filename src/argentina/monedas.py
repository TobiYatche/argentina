"""Historia monetaria argentina.

Las monedas oficiales que tuvo Argentina, sus períodos, símbolo, código ISO
y la **equivalencia con la siguiente** (factor de conversión nominal al
cambiar de moneda). Útil para convertir cifras históricas entre monedas.

Datos embebidos, sin dependencias externas.

Factor acumulado de m$n (Peso Moneda Nacional) hasta el peso actual:

- 100        m$n           = 1 Peso Ley 18.188 ($Ley)
- 10 000     $Ley          = 1 Peso Argentino ($a)
- 1 000      $a            = 1 Austral (₳)
- 10 000     ₳             = 1 Peso Convertible ($)

Total acumulado: **1 peso actual = 10^13 m$n**.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True)
class Moneda:
    nombre: str
    simbolo: str
    codigo_iso: str           # "" si no tenía código ISO formal
    inicio: date
    fin: date | None          # None si es la moneda actual
    # Factor para convertir UNA unidad de esta moneda a la moneda SIGUIENTE.
    # Por ejemplo: m$n → $Ley es 1/100 (100 m$n = 1 $Ley).
    # Para la moneda actual es None.
    factor_a_siguiente: float | None
    notas: str

    @property
    def vigente(self) -> bool:
        """``True`` si es la moneda de curso legal actual."""
        return self.fin is None

    def vigente_en(self, fecha) -> bool:
        """``True`` si esta moneda estaba vigente en la fecha dada."""
        f = fecha if isinstance(fecha, date) else date.fromisoformat(str(fecha))
        if f < self.inicio:
            return False
        return self.fin is None or f < self.fin

    def como_dict(self) -> dict:
        d = asdict(self)
        d["inicio"] = self.inicio.isoformat()
        d["fin"] = self.fin.isoformat() if self.fin else None
        return d


# Orden cronológico. El factor_a_siguiente acumula al cambiar de moneda.
MONEDAS = (
    Moneda(
        nombre="Peso Moneda Nacional",
        simbolo="m$n",
        codigo_iso="ARM",
        inicio=date(1881, 11, 5),
        fin=date(1970, 1, 1),
        factor_a_siguiente=1 / 100,       # 100 m$n = 1 $Ley
        notas="Implantado por la Ley 1130. Equivalencia 1 peso oro = 1 m$n.",
    ),
    Moneda(
        nombre="Peso Ley 18.188",
        simbolo="$Ley",
        codigo_iso="ARL",
        inicio=date(1970, 1, 1),
        fin=date(1983, 6, 1),
        factor_a_siguiente=1 / 10_000,    # 10000 $Ley = 1 $a
        notas="Quita 2 ceros respecto al m$n.",
    ),
    Moneda(
        nombre="Peso Argentino",
        simbolo="$a",
        codigo_iso="ARP",
        inicio=date(1983, 6, 1),
        fin=date(1985, 6, 14),
        factor_a_siguiente=1 / 1_000,     # 1000 $a = 1 ₳
        notas="Quita 4 ceros respecto al $Ley.",
    ),
    Moneda(
        nombre="Austral",
        simbolo="₳",
        codigo_iso="ARA",
        inicio=date(1985, 6, 14),
        fin=date(1992, 1, 1),
        factor_a_siguiente=1 / 10_000,    # 10000 ₳ = 1 $
        notas="Plan Austral. Quita 3 ceros respecto al $a.",
    ),
    Moneda(
        nombre="Peso",
        simbolo="$",
        codigo_iso="ARS",
        inicio=date(1992, 1, 1),
        fin=None,
        factor_a_siguiente=None,           # moneda actual
        notas="Convertibilidad 1992-2002. Tras la salida de la convertibilidad mantuvo nombre y código.",
    ),
)


def actual() -> Moneda:
    """Moneda de curso legal actual."""
    return MONEDAS[-1]


def en(fecha) -> Moneda | None:
    """Moneda vigente en la fecha dada."""
    f = fecha if isinstance(fecha, date) else date.fromisoformat(str(fecha))
    for m in MONEDAS:
        if m.vigente_en(f):
            return m
    return None


def listar() -> tuple[Moneda, ...]:
    """Devuelve todas las monedas en orden cronológico."""
    return MONEDAS


def lookup(valor: str | None) -> Moneda | None:
    """Busca por código ISO, símbolo o nombre."""
    if valor is None:
        return None
    s = str(valor).strip()
    if not s:
        return None
    s_upper = s.upper()
    for m in MONEDAS:
        if m.codigo_iso.upper() == s_upper:
            return m
    for m in MONEDAS:
        if m.simbolo == s:
            return m
    s_lower = s.lower()
    for m in MONEDAS:
        if m.nombre.lower() == s_lower:
            return m
    for m in MONEDAS:
        if s_lower in m.nombre.lower():
            return m
    return None


def convertir(
    monto: float,
    desde: str | Moneda,
    hasta: str | Moneda | None = None,
) -> float | None:
    """Convierte un monto entre monedas argentinas (nominal, sin inflación).

    Por defecto convierte a la moneda actual. Por ejemplo, 1.000.000 m$n
    equivalen a 0.000001 pesos actuales (factor acumulado 1 / 10^13).

    Esto es **conversión nominal de cambios de moneda**, NO ajuste por
    inflación. Para eso usar la serie del IPC en ``argentina.economia``.

    Parameters
    ----------
    monto : float
    desde : str | Moneda
        Código ISO, símbolo o nombre. Ej. ``"m$n"``, ``"ARS"``, ``"Austral"``.
    hasta : str | Moneda | None
        Idem; si es None, se convierte a la moneda actual.

    Returns
    -------
    float | None
        Monto convertido, o ``None`` si no se reconocen las monedas.
    """
    m_desde = lookup(desde) if not isinstance(desde, Moneda) else desde
    m_hasta = actual() if hasta is None else (
        lookup(hasta) if not isinstance(hasta, Moneda) else hasta
    )
    if m_desde is None or m_hasta is None:
        return None

    idx_d = MONEDAS.index(m_desde)
    idx_h = MONEDAS.index(m_hasta)
    if idx_d == idx_h:
        return float(monto)

    factor = 1.0
    if idx_d < idx_h:
        # Convertir hacia adelante (multiplicar factores hacia siguiente)
        for m in MONEDAS[idx_d:idx_h]:
            if m.factor_a_siguiente is None:
                return None
            factor *= m.factor_a_siguiente
        return float(monto) * factor
    else:
        # Convertir hacia atrás (dividir)
        for m in MONEDAS[idx_h:idx_d]:
            if m.factor_a_siguiente is None:
                return None
            factor *= m.factor_a_siguiente
        return float(monto) / factor


def como_tabla() -> list[dict]:
    """Lista de dicts apta para ``pandas.DataFrame``."""
    return [m.como_dict() for m in MONEDAS]


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.monedas.mapping("codigo_iso", "nombre")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(MONEDAS, de, a)


__all__ = [
    "Moneda",
    "MONEDAS",
    "actual",
    "en",
    "listar",
    "lookup",
    "convertir",
    "como_tabla",
    "mapping",
]
