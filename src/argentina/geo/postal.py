from __future__ import annotations


def georreferenciar_codigo_postal(*args, **kwargs):
    """Placeholder para georreferenciar zonas por código postal."""
    raise NotImplementedError(
        "argentina.geo.postal.georreferenciar_codigo_postal todavía no está implementado. "
        "La validación sintáctica vive en argentina.postal."
    )


def codigo_postal_por_direccion(*args, **kwargs):
    """Placeholder para obtener código postal desde dirección."""
    raise NotImplementedError(
        "argentina.geo.postal.codigo_postal_por_direccion todavía no está implementado. "
        "Para direcciones se recomienda usar una fuente oficial o Georef para coordenadas."
    )


def validar_codigo_postal_municipio(*args, **kwargs):
    """Placeholder para validar código postal contra municipio."""
    raise NotImplementedError(
        "argentina.geo.postal.validar_codigo_postal_municipio todavía no está implementado. "
        "Requiere una base territorial postal confiable."
    )


__all__ = [
    "georreferenciar_codigo_postal",
    "codigo_postal_por_direccion",
    "validar_codigo_postal_municipio",
]
