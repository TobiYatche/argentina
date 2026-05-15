"""Provincias argentinas: metadata oficial y lookup flexible.

Las 24 provincias se exponen como constantes públicas (``CORDOBA``,
``BUENOS_AIRES``, ``CABA``, etc.) y vía ``lookup`` que acepta nombre,
código INDEC, ISO 3166-2 o alias comunes. Sin dependencias externas,
datos embebidos.
"""

from __future__ import annotations

import csv
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from functools import lru_cache
from importlib.resources import files


# Mapeo código INDEC → letra CPA (para Provincia.cpa_letra).
# Es la inversa del dict postal.CPA_PROVINCIAS, embebido acá para evitar
# imports circulares.
_LETRA_CPA_POR_INDEC = {
    "02": "C", "06": "B", "10": "K", "14": "X", "18": "W",
    "22": "H", "26": "U", "30": "E", "34": "P", "38": "Y",
    "42": "L", "46": "F", "50": "M", "54": "N", "58": "Q",
    "62": "R", "66": "A", "70": "J", "74": "D", "78": "Z",
    "82": "S", "86": "G", "90": "T", "94": "V",
}

# Característica telefónica de la capital provincial.
# Para algunas capitales chicas (Rawson, Santa Rosa, Viedma, Río Gallegos,
# Ushuaia) el código es de 4 dígitos.
_CODIGO_TELEFONO_POR_INDEC = {
    "02": "11",     # CABA
    "06": "221",    # La Plata
    "10": "383",    # San Fernando del Valle de Catamarca
    "14": "351",    # Córdoba
    "18": "379",    # Corrientes
    "22": "362",    # Resistencia
    "26": "280",    # Rawson
    "30": "343",    # Paraná
    "34": "370",    # Formosa
    "38": "388",    # San Salvador de Jujuy
    "42": "2954",   # Santa Rosa
    "46": "380",    # La Rioja
    "50": "261",    # Mendoza
    "54": "376",    # Posadas
    "58": "299",    # Neuquén
    "62": "2920",   # Viedma
    "66": "387",    # Salta
    "70": "264",    # San Juan
    "74": "266",    # San Luis
    "78": "2966",   # Río Gallegos
    "82": "342",    # Santa Fe
    "86": "385",    # Santiago del Estero
    "90": "381",    # San Miguel de Tucumán
    "94": "2901",   # Ushuaia
}


@dataclass(frozen=True)
class Provincia:
    nombre: str
    codigo_indec: str
    iso_id: str
    region: str
    capital: str
    capital_lat: float | None = None
    capital_lon: float | None = None
    poblacion_2022: int | None = None  # Censo Nacional 2022 (INDEC)
    superficie_km2: int | None = None  # Superficie continental (sin reclamos antárticos)

    @property
    def densidad_2022(self) -> float | None:
        """Densidad poblacional (hab/km²) según Censo 2022 y superficie continental."""
        if self.poblacion_2022 is None or not self.superficie_km2:
            return None
        return self.poblacion_2022 / self.superficie_km2

    @property
    def cpa_letra(self) -> str | None:
        """Letra inicial del CPA correspondiente a la provincia (X para Córdoba,
        C para CABA, B para Buenos Aires, etc.).
        """
        return _LETRA_CPA_POR_INDEC.get(self.codigo_indec)

    @property
    def codigo_telefono(self) -> str | None:
        """Característica telefónica de la **capital** provincial.

        Devuelve un string de 2-4 dígitos sin el ``0`` inicial. Para
        capitales chicas (Rawson, Santa Rosa, Viedma, Río Gallegos,
        Ushuaia) son 4 dígitos.
        """
        return _CODIGO_TELEFONO_POR_INDEC.get(self.codigo_indec)

    @property
    def aglomerados(self) -> tuple:
        """Aglomerados EPH de esta provincia (tuple de :class:`~argentina.aglomerados.Aglomerado`)."""
        from argentina.aglomerados import por_provincia as _por
        return _por(self.codigo_indec)

    @property
    def universidades(self) -> tuple:
        """Universidades nacionales con sede en esta provincia."""
        from argentina.universidades import por_provincia as _por
        return _por(self.codigo_indec)

    @property
    def aeropuertos(self) -> tuple:
        """Aeropuertos en esta provincia."""
        from argentina.aeropuertos import por_provincia as _por
        return _por(self.codigo_indec)

    @property
    def ciudades(self) -> tuple:
        """Ciudades del catálogo curado en esta provincia."""
        from argentina.ciudades import por_provincia as _por
        return _por(self.codigo_indec)

    @property
    def departamentos(self) -> tuple:
        """Departamentos/partidos/comunas oficiales del IGN en esta provincia."""
        from argentina.departamentos import por_provincia as _por
        return _por(self.codigo_indec)

    def como_dict(self) -> dict:
        """Devuelve la provincia como diccionario plano (apto para JSON / DataFrame).

        Excluye las properties calculadas; solo los campos del CSV embebido.
        """
        return asdict(self)

    def _repr_html_(self) -> str:
        coords = ""
        if self.capital_lat is not None and self.capital_lon is not None:
            coords = (
                f"<tr><td style='padding:2px 8px'>coords capital</td>"
                f"<td style='padding:2px 8px'>"
                f"<code>{self.capital_lat:.4f}, {self.capital_lon:.4f}</code>"
                f"</td></tr>"
            )
        poblacion = ""
        if self.poblacion_2022 is not None:
            poblacion = (
                f"<tr><td style='padding:2px 8px'>población (2022)</td>"
                f"<td style='padding:2px 8px'>"
                f"{self.poblacion_2022:,}".replace(",", ".") + "</td></tr>"
            )
        return (
            "<table style='border-collapse:collapse;font-size:90%'>"
            f"<tr><th colspan='2' style='text-align:left;padding:4px 8px;"
            f"background:#f0f0f0'>{self.nombre}</th></tr>"
            f"<tr><td style='padding:2px 8px'>código INDEC</td>"
            f"<td style='padding:2px 8px'><code>{self.codigo_indec}</code></td></tr>"
            f"<tr><td style='padding:2px 8px'>ISO 3166-2</td>"
            f"<td style='padding:2px 8px'><code>{self.iso_id}</code></td></tr>"
            f"<tr><td style='padding:2px 8px'>región</td>"
            f"<td style='padding:2px 8px'>{self.region}</td></tr>"
            f"<tr><td style='padding:2px 8px'>capital</td>"
            f"<td style='padding:2px 8px'>{self.capital}</td></tr>"
            f"{coords}"
            f"{poblacion}"
            "</table>"
        )


@lru_cache(maxsize=512)
def _normalizar(texto: str | None) -> str:
    """Normaliza texto para búsquedas flexibles."""
    if texto is None:
        return ""

    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _slug_constante(nombre: str) -> str:
    """Convierte nombre de provincia a nombre de constante."""
    texto = _normalizar(nombre)
    return texto.upper().replace(" ", "_")


def _cargar_provincias() -> tuple[Provincia, ...]:
    path = files("argentina").joinpath("data/provincias.csv")
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        provincias = []
        for row in reader:
            lat = row.get("capital_lat")
            lon = row.get("capital_lon")
            pob = row.get("poblacion_2022")
            sup = row.get("superficie_km2")
            provincias.append(
                Provincia(
                    nombre=row["nombre"],
                    codigo_indec=row["codigo_indec"].zfill(2),
                    iso_id=row["iso_id"],
                    region=row["region"],
                    capital=row["capital"],
                    capital_lat=float(lat) if lat else None,
                    capital_lon=float(lon) if lon else None,
                    poblacion_2022=int(pob) if pob else None,
                    superficie_km2=int(sup) if sup else None,
                )
            )
    return tuple(provincias)


PROVINCIAS = _cargar_provincias()


_PROVINCIAS_POR_CONSTANTE = {
    _slug_constante(p.nombre): p
    for p in PROVINCIAS
}


BUENOS_AIRES = _PROVINCIAS_POR_CONSTANTE["BUENOS_AIRES"]
CATAMARCA = _PROVINCIAS_POR_CONSTANTE["CATAMARCA"]
CORDOBA = _PROVINCIAS_POR_CONSTANTE["CORDOBA"]
CORRIENTES = _PROVINCIAS_POR_CONSTANTE["CORRIENTES"]
CHACO = _PROVINCIAS_POR_CONSTANTE["CHACO"]
CHUBUT = _PROVINCIAS_POR_CONSTANTE["CHUBUT"]
ENTRE_RIOS = _PROVINCIAS_POR_CONSTANTE["ENTRE_RIOS"]
FORMOSA = _PROVINCIAS_POR_CONSTANTE["FORMOSA"]
JUJUY = _PROVINCIAS_POR_CONSTANTE["JUJUY"]
LA_PAMPA = _PROVINCIAS_POR_CONSTANTE["LA_PAMPA"]
LA_RIOJA = _PROVINCIAS_POR_CONSTANTE["LA_RIOJA"]
MENDOZA = _PROVINCIAS_POR_CONSTANTE["MENDOZA"]
MISIONES = _PROVINCIAS_POR_CONSTANTE["MISIONES"]
NEUQUEN = _PROVINCIAS_POR_CONSTANTE["NEUQUEN"]
RIO_NEGRO = _PROVINCIAS_POR_CONSTANTE["RIO_NEGRO"]
SALTA = _PROVINCIAS_POR_CONSTANTE["SALTA"]
SAN_JUAN = _PROVINCIAS_POR_CONSTANTE["SAN_JUAN"]
SAN_LUIS = _PROVINCIAS_POR_CONSTANTE["SAN_LUIS"]
SANTA_CRUZ = _PROVINCIAS_POR_CONSTANTE["SANTA_CRUZ"]
SANTA_FE = _PROVINCIAS_POR_CONSTANTE["SANTA_FE"]
SANTIAGO_DEL_ESTERO = _PROVINCIAS_POR_CONSTANTE["SANTIAGO_DEL_ESTERO"]
TUCUMAN = _PROVINCIAS_POR_CONSTANTE["TUCUMAN"]
TIERRA_DEL_FUEGO = _PROVINCIAS_POR_CONSTANTE["TIERRA_DEL_FUEGO"]

CIUDAD_AUTONOMA_DE_BUENOS_AIRES = _PROVINCIAS_POR_CONSTANTE[
    "CIUDAD_AUTONOMA_DE_BUENOS_AIRES"
]
CABA = CIUDAD_AUTONOMA_DE_BUENOS_AIRES


_ALIASES = {
    "caba": CABA,
    "capital federal": CABA,
    "ciudad autonoma de buenos aires": CABA,
    "ciudad de buenos aires": CABA,
    "buenos aires ciudad": CABA,
    "bs as": BUENOS_AIRES,
    "buenos aires provincia": BUENOS_AIRES,
    "provincia de buenos aires": BUENOS_AIRES,
    "pba": BUENOS_AIRES,
    "tdf": TIERRA_DEL_FUEGO,
    "tierra del fuego antartida e islas del atlantico sur": TIERRA_DEL_FUEGO,
}

_ALIASES_NORMALIZADOS = {
    _normalizar(k): v
    for k, v in _ALIASES.items()
}


_LOOKUP: dict[str, Provincia] = {}

for provincia in PROVINCIAS:
    _LOOKUP[_normalizar(provincia.nombre)] = provincia
    _LOOKUP[_normalizar(provincia.codigo_indec)] = provincia
    _LOOKUP[_normalizar(provincia.iso_id)] = provincia
    _LOOKUP[_normalizar(_slug_constante(provincia.nombre))] = provincia

_LOOKUP.update(_ALIASES_NORMALIZADOS)


def lookup(valor: str | None, *, fuzzy: bool = False, cutoff: float = 0.75) -> Provincia | None:
    """Busca una provincia por nombre, código INDEC, ISO o alias.

    Parameters
    ----------
    valor : str | None
        Nombre, código INDEC, ISO 3166-2 o alias (case-insensitive, sin tildes).
    fuzzy : bool
        Si ``True`` y no hay match exacto, intenta un match aproximado
        con ``difflib`` (tolerancia a typos). Default ``False``.
    cutoff : float
        Similitud mínima para fuzzy (0-1). Default 0.75.

    Examples
    --------
    >>> arg.provincias.lookup("misisones")                # None
    >>> arg.provincias.lookup("misisones", fuzzy=True)    # Misiones
    >>> arg.provincias.lookup("buens aires", fuzzy=True)  # Buenos Aires
    """
    n = _normalizar(valor)
    if not n:
        return None
    if n in _LOOKUP:
        return _LOOKUP[n]
    if fuzzy:
        from difflib import get_close_matches
        match = get_close_matches(n, _LOOKUP.keys(), n=1, cutoff=cutoff)
        if match:
            return _LOOKUP[match[0]]
    return None


def listar() -> tuple[Provincia, ...]:
    """Devuelve todas las provincias argentinas."""
    return PROVINCIAS


def regiones() -> tuple[str, ...]:
    """Devuelve las regiones argentinas presentes en el catálogo, ordenadas.

    Hoy son seis: ``CABA``, ``Cuyo``, ``NEA``, ``NOA``, ``Pampeana``, ``Patagonia``.
    """
    return tuple(sorted({p.region for p in PROVINCIAS}))


def por_region(region: str | None) -> tuple[Provincia, ...]:
    """Devuelve las provincias de una región.

    Acepta nombre con o sin tildes, case-insensitive
    (``"patagonia"``, ``"PATAGONIA"``, ``"Patagonia"`` son equivalentes).
    """
    if region is None:
        return ()
    n = _normalizar(region)
    if not n:
        return ()
    return tuple(p for p in PROVINCIAS if _normalizar(p.region) == n)


def como_tabla() -> list[dict]:
    """Devuelve las 24 provincias como lista de dicts.

    Pensado para conversión directa: ``pandas.DataFrame(arg.provincias.como_tabla())``.
    """
    return [p.como_dict() for p in PROVINCIAS]


# Hacer el módulo iterable: `for p in argentina.provincias: ...`
import types as _types


class _ProvinciasModulo(_types.ModuleType):
    def __iter__(self):
        return iter(PROVINCIAS)

    def __len__(self):
        return len(PROVINCIAS)

    def __contains__(self, item):
        if isinstance(item, Provincia):
            return item in PROVINCIAS
        return lookup(item) is not None


sys.modules[__name__].__class__ = _ProvinciasModulo


def mapping(de: str, a: str) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items del catálogo.

    Útil para armar diccionarios de conversión rápidos. Ejemplo::

        arg.provincias.mapping("codigo_indec", "nombre")
        # → diccionario con la conversión

    Levanta ``AttributeError`` si alguno de los campos no existe.
    """
    from argentina._mapping import make_mapping
    return make_mapping(PROVINCIAS, de, a)


__all__ = [
    "Provincia",
    "PROVINCIAS",
    "CABA",
    "CIUDAD_AUTONOMA_DE_BUENOS_AIRES",
    "BUENOS_AIRES",
    "CATAMARCA",
    "CORDOBA",
    "CORRIENTES",
    "CHACO",
    "CHUBUT",
    "ENTRE_RIOS",
    "FORMOSA",
    "JUJUY",
    "LA_PAMPA",
    "LA_RIOJA",
    "MENDOZA",
    "MISIONES",
    "NEUQUEN",
    "RIO_NEGRO",
    "SALTA",
    "SAN_JUAN",
    "SAN_LUIS",
    "SANTA_CRUZ",
    "SANTA_FE",
    "SANTIAGO_DEL_ESTERO",
    "TUCUMAN",
    "TIERRA_DEL_FUEGO",
    "lookup",
    "listar",
    "regiones",
    "por_region",
    "como_tabla",
    "mapping",
]
