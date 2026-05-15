"""Limpia outputs grandes de notebooks (.ipynb) en `notebooks/`.

Útil antes de commitear: si un notebook ejecutado pesa más de un umbral
(default 1 MB), se borran sus outputs y se baja `execution_count` a `null`.
Notebooks por debajo del umbral se dejan intactos para conservar los
gráficos chicos como referencia.

Uso:

    python tools/limpiar_outputs_grandes.py
    python tools/limpiar_outputs_grandes.py --max-kb 500
    python tools/limpiar_outputs_grandes.py --check     # solo lista, no escribe
    python tools/limpiar_outputs_grandes.py notebooks/uno.ipynb otro.ipynb
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_MAX_KB = 1024


def _peso_kb(path: Path) -> float:
    return path.stat().st_size / 1024


def _limpiar_notebook(path: Path) -> tuple[float, float]:
    nb = json.loads(path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    antes = _peso_kb(path)
    path.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    despues = _peso_kb(path)
    return antes, despues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Notebooks o directorios. Default: notebooks/",
    )
    ap.add_argument(
        "--max-kb",
        type=float,
        default=DEFAULT_MAX_KB,
        help=f"Umbral en KB. Notebooks más grandes se limpian. Default: {DEFAULT_MAX_KB}",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Solo lista qué notebooks superan el umbral, no los modifica.",
    )
    args = ap.parse_args()

    if not args.paths:
        args.paths = [Path("notebooks")]

    notebooks: list[Path] = []
    for p in args.paths:
        if p.is_dir():
            notebooks.extend(sorted(p.glob("*.ipynb")))
        elif p.suffix == ".ipynb":
            notebooks.append(p)

    if not notebooks:
        print("No se encontraron notebooks.", file=sys.stderr)
        return 1

    grandes = [nb for nb in notebooks if _peso_kb(nb) > args.max_kb]

    if not grandes:
        print(f"OK — ningún notebook supera {args.max_kb:.0f} KB.")
        return 0

    if args.check:
        print(f"Notebooks que superan {args.max_kb:.0f} KB:")
        for nb in grandes:
            print(f"  {nb}  ({_peso_kb(nb):.0f} KB)")
        return 1

    for nb in grandes:
        antes, despues = _limpiar_notebook(nb)
        print(f"  {nb}  {antes:.0f} → {despues:.0f} KB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
