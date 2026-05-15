"""Verifica que ``import argentina`` no cargue pandas/requests.

Corre en un subproceso fresh para que otros tests no contaminen sys.modules.
"""

import subprocess
import sys


def test_import_argentina_no_importa_pandas_requests():
    code = (
        "import sys, argentina;"
        "print('pandas' in sys.modules, 'requests' in sys.modules)"
    )
    out = subprocess.check_output([sys.executable, "-c", code]).decode().strip()
    assert out == "False False", f"esperado 'False False', vino '{out}'"
