"""Datos del Censo Nacional 2022 (INDEC) vía DuckDB + Parquet remoto.

Diseño: en lugar de descargar archivos enteros (los microdatos del Censo pesan
varios GB), usamos DuckDB para consultar parquets remotos vía HTTPS y traer
solo las filas/columnas que pedimos:

    SELECT * FROM read_parquet('https://.../personas.parquet')
    WHERE provincia_codigo = '14' AND ...

URLs por tabla:
    Configurar en :data:`CENSO_PARQUETS_2022`. Por defecto vacío — el INDEC
    todavía no publica microdatos del Censo 2022 como parquets oficiales.
    Cuando exista (o si tenés un mirror propio), agregá las URLs ahí o pasalas
    al parámetro ``url=`` de :func:`censo` directamente.

Ejemplo con URL propia::

    import argentina.data.censo as c
    c.CENSO_PARQUETS_2022['personas'] = 'https://mi-mirror/personas.parquet'

    df = arg.data.censo(anio=2022, tabla='personas', provincia='Córdoba')
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


# URLs por tabla. Por ahora vacías (placeholder explícito): el usuario tiene
# que configurarlas o pasar ``url=`` a la función.
CENSO_PARQUETS_2022: dict[str, str | None] = {
    "personas": None,
    "hogares": None,
    "viviendas": None,
}


def _require_censo_dependencies() -> None:
    """Verifica dependencias opcionales para Censo."""
    try:
        import duckdb  # noqa: F401
        import pandas  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            'Para usar argentina.data.censo instalá: pip install "argentina[data]"'
        ) from exc


def _resolver_codigo_provincia(provincia: str | None) -> str | None:
    """Resuelve cualquier identificador de provincia a su código INDEC (2 dígitos)."""
    if provincia is None:
        return None
    # Usamos el catálogo de provincias para aceptar nombres/aliases/ISO.
    from argentina.provincias import lookup as _lookup_prov
    p = _lookup_prov(provincia)
    if p is None:
        # Si vino "14" directo, devolverlo padded.
        s = str(provincia).strip()
        if s.isdigit() and len(s) <= 2:
            return s.zfill(2)
        raise ValueError(f"Provincia no reconocida: {provincia!r}")
    return p.codigo_indec


def _resolver_codigo_departamento(departamento: str | None) -> str | None:
    """Resuelve un departamento a su código INDEC (5 dígitos)."""
    if departamento is None:
        return None
    from argentina.departamentos import lookup as _lookup_depto
    d = _lookup_depto(departamento)
    if d is None:
        s = str(departamento).strip()
        if s.isdigit() and len(s) <= 5:
            return s.zfill(5)
        raise ValueError(f"Departamento no reconocido: {departamento!r}")
    return d.codigo_departamento


def censo(
    anio: int = 2022,
    tabla: str | None = None,
    provincia: str | None = None,
    departamento: str | None = None,
    limite: int | None = None,
    url: str | None = None,
    sql_extra: str | None = None,
) -> "pd.DataFrame":
    """Consulta datos del Censo 2022 vía DuckDB + Parquet remoto.

    Parameters
    ----------
    anio : int
        Por ahora solo ``2022``.
    tabla : str
        ``"personas"``, ``"hogares"`` o ``"viviendas"``. Usado para resolver
        la URL desde :data:`CENSO_PARQUETS_2022` cuando ``url`` no se pasa.
    provincia : str | None
        Filtro por provincia. Acepta cualquier identificador que entienda
        ``argentina.provincias.lookup`` (nombre, código INDEC, ISO, alias).
        Asume que el parquet tiene una columna ``provincia_codigo`` o similar
        — se filtra como ``WHERE provincia_codigo = '<código>'``.
    departamento : str | None
        Filtro por departamento (5 dígitos INDEC). ``WHERE departamento_codigo = ...``.
    limite : int | None
        ``LIMIT N``. Útil para previsualizar sin descargar todo.
    url : str | None
        URL al parquet remoto. Si se pasa, ignora ``tabla``.
    sql_extra : str | None
        SQL adicional para incluir después del ``WHERE`` (sin la palabra
        ``WHERE``). Ej: ``"edad >= 18 AND sexo = 'F'"``.

    Returns
    -------
    pandas.DataFrame
        Resultado de la query.

    Raises
    ------
    ValueError
        Año no 2022, o falta URL (no pasaste ``url=`` y la tabla no está
        configurada en ``CENSO_PARQUETS_2022``).
    """
    # Validar primero para que errores de uso sean claros aún sin extra.
    if int(anio) != 2022:
        raise ValueError("Por ahora solo se prepara soporte para Censo 2022.")

    # Resolver URL
    if url is None:
        if tabla is None:
            raise ValueError(
                "Pasá 'tabla' (personas/hogares/viviendas) o 'url=' explícita."
            )
        url = CENSO_PARQUETS_2022.get(tabla)
        if not url:
            raise ValueError(
                f"No hay URL configurada para tabla '{tabla}'. "
                "Configurá CENSO_PARQUETS_2022 o pasá 'url=' a la función. "
                "El INDEC aún no publica microdatos parquet del Censo 2022."
            )

    cod_prov = _resolver_codigo_provincia(provincia)
    cod_depto = _resolver_codigo_departamento(departamento)

    _require_censo_dependencies()
    import duckdb

    # Construir SQL parametrizado. Usamos quote para los códigos (siempre dígitos).
    where = []
    if cod_prov is not None:
        where.append(f"provincia_codigo = '{cod_prov}'")
    if cod_depto is not None:
        where.append(f"departamento_codigo = '{cod_depto}'")
    if sql_extra:
        where.append(f"({sql_extra})")

    sql = f"SELECT * FROM read_parquet('{url}')"
    if where:
        sql += " WHERE " + " AND ".join(where)
    if limite is not None:
        sql += f" LIMIT {int(limite)}"

    con = duckdb.connect()
    try:
        return con.execute(sql).fetchdf()
    finally:
        con.close()


__all__ = [
    "CENSO_PARQUETS_2022",
    "censo",
]
