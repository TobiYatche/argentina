"""Geometrías oficiales de Argentina descargadas on-demand.

Este módulo es opcional: para usarlo hay que instalar las dependencias
geoespaciales con ``pip install "argentina[geo]"`` (geopandas, requests,
pyogrio).

Fuente: Instituto Geográfico Nacional (IGN), capas SIG servidas vía WFS.
https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/CapasSIG

Filosofía: NO se incluyen shapefiles en el paquete. Las geometrías se bajan
desde el WFS del IGN (o de una URL pasada como argumento) y se cachean en
disco bajo ``~/.cache/argentina``.
"""

from __future__ import annotations

from pathlib import Path
import zipfile


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "argentina"

_IGN_WFS = (
    "https://wms.ign.gob.ar/geoserver/ign/ows"
    "?service=WFS&version=1.0.0&request=GetFeature"
    "&typeName=ign%3A{capa}&outputFormat=SHAPE-ZIP"
)

SHAPE_URLS = {
    "provincias": _IGN_WFS.format(capa="provincia"),
    "departamentos": _IGN_WFS.format(capa="departamento"),
}


def _require_geo_dependencies() -> None:
    """Verifica que estén instaladas las dependencias geoespaciales."""
    try:
        import geopandas  # noqa: F401
        import requests  # noqa: F401
    except ImportError as exc:
        raise ImportError(
            "Para usar argentina.shapes instalá el extra geoespacial: "
            'pip install "argentina[geo]"'
        ) from exc


def _download_file(url: str, path: Path, overwrite: bool = False) -> Path:
    """Descarga un archivo si no existe."""
    _require_geo_dependencies()

    import requests

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and not overwrite:
        return path

    response = requests.get(url, timeout=300)
    response.raise_for_status()

    path.write_bytes(response.content)

    return path


def _extract_zip(zip_path: Path, out_dir: Path, overwrite: bool = False) -> Path:
    """Extrae un ZIP si hace falta."""
    out_dir.mkdir(parents=True, exist_ok=True)

    if any(out_dir.iterdir()) and not overwrite:
        return out_dir

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(out_dir)

    return out_dir


def _find_vector_file(directory: Path) -> Path:
    """Busca un archivo vectorial dentro de una carpeta.

    Prefiere ``.gpkg``, después ``.geojson``, después ``.shp``.
    """
    extensions = [".gpkg", ".geojson", ".shp"]

    for ext in extensions:
        files = list(directory.rglob(f"*{ext}"))
        if files:
            return files[0]

    raise FileNotFoundError(
        f"No se encontró archivo vectorial en {directory}"
    )


def _load_shape(
    name: str,
    url: str | None = None,
    cache_dir: str | Path | None = None,
    overwrite: bool = False,
):
    """Descarga, cachea y lee una geometría."""
    if url is None:
        url = SHAPE_URLS[name]

    if not url or "PLACEHOLDER" in url:
        raise ValueError(
            f"No hay URL configurada para '{name}'. "
            "Pasá una URL explícita usando el argumento url=."
        )

    _require_geo_dependencies()

    import geopandas as gpd

    if cache_dir is None:
        cache_dir = DEFAULT_CACHE_DIR

    cache_dir = Path(cache_dir)

    layer_dir = cache_dir / "shapes" / name
    zip_path = layer_dir / f"{name}.zip"
    extract_dir = layer_dir / "extracted"

    _download_file(url, zip_path, overwrite=overwrite)
    _extract_zip(zip_path, extract_dir, overwrite=overwrite)

    vector_path = _find_vector_file(extract_dir)

    return gpd.read_file(vector_path)


def provincias(
    url: str | None = None,
    cache_dir: str | Path | None = None,
    overwrite: bool = False,
):
    """Devuelve geometrías de provincias argentinas como GeoDataFrame."""
    return _load_shape(
        name="provincias",
        url=url,
        cache_dir=cache_dir,
        overwrite=overwrite,
    )


def departamentos(
    url: str | None = None,
    cache_dir: str | Path | None = None,
    overwrite: bool = False,
):
    """Devuelve geometrías de departamentos argentinos como GeoDataFrame."""
    return _load_shape(
        name="departamentos",
        url=url,
        cache_dir=cache_dir,
        overwrite=overwrite,
    )


__all__ = [
    "provincias",
    "departamentos",
]
