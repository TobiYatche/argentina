from argentina.economia.series import (
    obtener_serie,
    serie,
    ipc_nacional,
    ipc_nucleo,
    emae,
    tipo_cambio_minorista,
)
from argentina.economia.busqueda import buscar

from argentina.economia.catalogo import SERIES

__all__ = [
    "SERIES",
    "obtener_serie",
    "serie",
    "buscar",
    "ipc_nacional",
    "ipc_nucleo",
    "emae",
    "tipo_cambio_minorista",
]
