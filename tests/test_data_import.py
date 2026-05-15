"""Verifica que ``import argentina`` no cargue dependencias de ``data``.

Corre en un subproceso fresh para que otros tests no contaminen sys.modules.
"""

import subprocess
import sys


def test_import_argentina_no_importa_data_deps():
    code = (
        "import sys, argentina;"
        "print("
        "'pandas' in sys.modules,"
        "'requests' in sys.modules,"
        "'duckdb' in sys.modules,"
        "'pyarrow' in sys.modules"
        ")"
    )
    out = subprocess.check_output([sys.executable, "-c", code]).decode().strip()
    assert out == "False False False False", f"esperado 'False False False False', vino {out!r}"
