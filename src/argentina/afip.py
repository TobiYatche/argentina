"""AFIP: alícuotas de IVA + reexports de CUIT y CLAE.

Provee acceso offline a los datos AFIP estables y a las funciones de
CUIT/CLAE ya implementadas en el paquete.

**Alcance acotado a propósito:** las tablas de Monotributo y mínimo no
imponible de Ganancias cambian por resolución general (a veces varias
veces al año por inflación) y embeberlas sin un proceso explícito de
actualización corre el riesgo de devolver datos desactualizados
silenciosamente. Por eso este módulo NO incluye esas tablas. Para
valores vigentes, consultar AFIP directamente. Cuando se decida
incorporar Monotributo/Ganancias con un proceso de actualización claro,
se agrega.

Las alícuotas de IVA (general 21 %, reducida 10,5 %, especial 27 %)
están en la Ley 23.349 y modificatorias; son estables hace décadas.
Esas sí se embeben.

Las funciones CUIT (``validar_cuit``, ``limpiar_cuit``,
``formatear_cuit``, ``tipo_cuit``) se reexportan desde
:mod:`argentina.personas` para descubribilidad. La implementación
canónica vive ahí.

Este módulo **no es un motor fiscal** — solo lookups. No calcula
impuestos, no emite facturas, no liquida.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# IVA (alícuotas estables Ley 23.349 + mod.)
# ---------------------------------------------------------------------------


ALICUOTAS_IVA = {
    "general": 0.21,
    "reducida": 0.105,
    "especial": 0.27,
}


def alicuotas_iva() -> dict[str, float]:
    """Devuelve las alícuotas de IVA vigentes.

    Claves: ``'general'``, ``'reducida'``, ``'especial'``.
    Valores estables de la Ley 23.349 y modificatorias.
    """
    return dict(ALICUOTAS_IVA)


# ---------------------------------------------------------------------------
# CUIT: reexports de personas (NO reimplementar)
# ---------------------------------------------------------------------------


def validar_cuit(cuit, *args, **kwargs) -> bool:
    """Valida un CUIT/CUIL. Reexport de :func:`argentina.personas.validar_cuit`."""
    from argentina import personas
    return personas.validar_cuit(cuit, *args, **kwargs)


def limpiar_cuit(cuit):
    """Normaliza un CUIT a 11 dígitos. Reexport de :func:`argentina.personas.limpiar_cuit`."""
    from argentina import personas
    return personas.limpiar_cuit(cuit)


def formatear_cuit(cuit):
    """Formatea un CUIT como ``XX-XXXXXXXX-X``. Reexport de :func:`argentina.personas.formatear_cuit`."""
    from argentina import personas
    return personas.formatear_cuit(cuit)


def tipo_cuit(cuit):
    """Categoría del CUIT (persona física / jurídica). Reexport de :func:`argentina.personas.tipo_cuit`."""
    from argentina import personas
    return personas.tipo_cuit(cuit)


# ---------------------------------------------------------------------------
# CLAE: reexport diferido
# ---------------------------------------------------------------------------


def clae_lookup(codigo):
    """Busca una actividad CLAE. Reexport de :func:`argentina.clae.lookup`."""
    from argentina import clae as _clae
    return _clae.lookup(codigo)


def clae_buscar(texto):
    """Busca actividades CLAE por descripción. Reexport de :func:`argentina.clae.buscar`."""
    from argentina import clae as _clae
    return _clae.buscar(texto)


__all__ = [
    "ALICUOTAS_IVA",
    "alicuotas_iva",
    "validar_cuit",
    "limpiar_cuit",
    "formatear_cuit",
    "tipo_cuit",
    "clae_lookup",
    "clae_buscar",
]
