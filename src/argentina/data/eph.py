"""Microdatos de la EPH (Encuesta Permanente de Hogares, INDEC).

Descarga el ZIP oficial de microdatos por trimestre desde el FTP del INDEC,
lo cachea bajo ``~/.cache/argentina/eph/`` y lo lee como ``pandas.DataFrame``.

Por ahora soporta únicamente **EPH trimestral** (desde 2003). La EPH puntual
(semestral pre-2003) no está implementada.

Fuente:
    https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos
"""

from __future__ import annotations

import zipfile
from pathlib import Path


# URL oficial INDEC: ZIP de microdatos trimestrales en formato txt (sep=';').
EPH_URL_TRIMESTRAL = (
    "https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/"
    "EPH_usu_{numero}_Trim_{anio}_txt.zip"
)

DEFAULT_CACHE_DIR = Path.home() / ".cache" / "argentina"


def _require_data_dependencies() -> None:
    """Verifica dependencias opcionales de data."""
    try:
        import pandas  # noqa: F401
        import requests  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            'Para usar argentina.data instalá: pip install "argentina[data]"'
        ) from exc


def _normalizar_periodo(
    periodo: str,
) -> str:
    """Normaliza período EPH."""
    p = str(periodo).strip().lower()

    aliases = {
        "t": "trimestral",
        "trim": "trimestral",
        "trimestre": "trimestral",
        "trimestral": "trimestral",
        "s": "semestral",
        "sem": "semestral",
        "semestre": "semestral",
        "semestral": "semestral",
    }

    if p not in aliases:
        raise ValueError(
            "periodo debe ser 'trimestral' o 'semestral'."
        )

    return aliases[p]


def _validar_eph_args(
    anio: int,
    periodo: str,
    numero: int,
) -> tuple[int, str, int]:
    """Valida argumentos EPH."""
    anio = int(anio)
    numero = int(numero)
    periodo = _normalizar_periodo(periodo)

    if anio < 2003:
        raise ValueError("EPH continua disponible desde 2003.")

    if periodo == "trimestral" and numero not in {1, 2, 3, 4}:
        raise ValueError("Para EPH trimestral, numero debe ser 1, 2, 3 o 4.")

    if periodo == "semestral" and numero not in {1, 2}:
        raise ValueError("Para EPH semestral, numero debe ser 1 o 2.")

    return anio, periodo, numero


def _normalizar_tipo(tipo: str) -> str:
    """Normaliza ``tipo`` ('individual' o 'hogar')."""
    t = str(tipo).strip().lower()
    aliases = {
        "individual": "individual",
        "individuo": "individual",
        "individuos": "individual",
        "personas": "individual",
        "persona": "individual",
        "hogar": "hogar",
        "hogares": "hogar",
    }
    if t not in aliases:
        raise ValueError("tipo debe ser 'individual' o 'hogar'.")
    return aliases[t]


def _download_file(url: str, path: Path, timeout: int = 300) -> Path:
    """Descarga un archivo si no existe."""
    import requests

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path

    # Streaming para no cargar todo en memoria.
    tmp = path.with_suffix(path.suffix + ".part")
    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                if chunk:
                    f.write(chunk)
    tmp.rename(path)
    return path


def _extract_zip(zip_path: Path, out_dir: Path) -> Path:
    """Extrae un ZIP si hace falta."""
    out_dir.mkdir(parents=True, exist_ok=True)
    if any(out_dir.iterdir()):
        return out_dir
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(out_dir)
    return out_dir


def _find_microdato(directory: Path, tipo: str) -> Path:
    """Busca el archivo de microdatos según ``tipo``.

    El INDEC nombra los archivos como ``usu_individual_T<N><AA>.txt`` o
    ``usu_hogar_T<N><AA>.txt``. También aparecen variantes con extensión
    ``.csv`` o mayúsculas.
    """
    patterns = [
        f"usu_{tipo}_*.txt",
        f"usu_{tipo}_*.csv",
        f"USU_{tipo.upper()}_*.txt",
    ]
    for pattern in patterns:
        files = list(directory.rglob(pattern))
        if files:
            return files[0]
    raise FileNotFoundError(
        f"No se encontró microdato tipo {tipo!r} en {directory}. "
        f"Archivos disponibles: {[p.name for p in directory.rglob('*') if p.is_file()][:10]}"
    )


def eph(
    anio: int,
    periodo: str = "trimestral",
    numero: int = 1,
    tipo: str = "individual",
    cache_dir: str | Path | None = None,
):
    """Devuelve los microdatos EPH de un trimestre como ``pandas.DataFrame``.

    Parameters
    ----------
    anio : int
        Año (≥ 2003).
    periodo : str
        Por ahora solo ``"trimestral"`` (alias: ``"T"``, ``"trim"``, etc.).
        ``"semestral"`` está validado pero no implementado.
    numero : int
        Trimestre 1-4.
    tipo : str
        ``"individual"`` (personas) o ``"hogar"``.
    cache_dir : str | Path | None
        Directorio de cache. Default: ``~/.cache/argentina``.

    Returns
    -------
    pandas.DataFrame
        Microdatos crudos del INDEC (columnas tal cual vienen en el txt,
        separador ``;``, encoding latin-1).
    """
    # Validar primero para que errores de uso sean claros aún sin extra.
    anio, periodo, numero = _validar_eph_args(
        anio=anio, periodo=periodo, numero=numero,
    )
    tipo = _normalizar_tipo(tipo)

    if periodo != "trimestral":
        raise NotImplementedError(
            "Por ahora solo está implementada la EPH trimestral (continua). "
            "La EPH semestral pre-2003 no se descarga automáticamente."
        )

    _require_data_dependencies()
    import pandas as pd

    cache_base = Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR
    cache = cache_base / "eph" / f"T{numero}_{anio}"

    url = EPH_URL_TRIMESTRAL.format(numero=numero, anio=anio)
    zip_path = cache / "microdatos.zip"
    extract_dir = cache / "extracted"

    _download_file(url, zip_path)
    _extract_zip(zip_path, extract_dir)

    microdato = _find_microdato(extract_dir, tipo)
    return pd.read_csv(
        microdato,
        sep=";",
        encoding="latin-1",
        low_memory=False,
    )


__all__ = [
    "EPH_URL_TRIMESTRAL",
    "DEFAULT_CACHE_DIR",
    "eph",
]
