"""Wrapper de compatibilidad. Reexporta desde ``argentina.geo.shapes``."""

from __future__ import annotations

from argentina.geo.shapes import (
    departamentos,
    provincias,
)

__all__ = [
    "provincias",
    "departamentos",
]
