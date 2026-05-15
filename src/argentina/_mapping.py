"""Helper interno: ``mapping(items, de, a)``.

Genera un diccionario ``{getattr(item, de): getattr(item, a)}`` para cualquier
secuencia de dataclasses. Usado por los métodos ``mapping()`` de los módulos
de lookup (provincias, departamentos, ciudades, etc).
"""

from __future__ import annotations

from typing import Any, Callable, Iterable


def make_mapping(
    items: Iterable[Any],
    de: str,
    a: str,
    *,
    fallback: Callable[[Any, str], Any] | None = None,
) -> dict:
    """Devuelve ``{item.<de>: item.<a>}`` para todos los items.

    Si ``de`` o ``a`` no son atributos directos del item, ``fallback`` se
    invoca con ``(item, name)`` y debe devolver el valor a usar. Si no hay
    fallback, se levanta ``AttributeError``.
    """
    def _get(item: Any, name: str) -> Any:
        try:
            return getattr(item, name)
        except AttributeError:
            if fallback is not None:
                return fallback(item, name)
            raise

    return {_get(item, de): _get(item, a) for item in items}


__all__ = ["make_mapping"]
