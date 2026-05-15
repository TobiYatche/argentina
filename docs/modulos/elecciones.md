# Elecciones

`argentina.elecciones` ofrece utilidades para datos electorales argentinos:
normalización de tipos de elección, categorías, validación de años,
identificadores (mesa, circuito, sección).

!!! warning "Extra requerido para la parte que pega a red"
    El módulo `argentina.elecciones.api` necesita `requests` y `pandas`.
    Instalá con:

    ```bash
    pip install "argentina[elecciones]"
    ```

    La parte sintáctica (`limpiar_mesa`, `normalizar_categoria`,
    `validar_anio_eleccion`) no requiere ningún extra.

## Ejemplos

```python
import argentina as arg

# Limpieza y validación local (sin red)
arg.elecciones.limpiar_mesa("Mesa 01234")
arg.elecciones.limpiar_circuito("...")
arg.elecciones.normalizar_categoria("presidente")
arg.elecciones.normalizar_tipo_eleccion("PASO")
arg.elecciones.validar_anio_eleccion(2023)

# Parte que pega a red (requiere extra)
arg.elecciones.api.disponible()
```

Ver [API reference](../api.md#argentinaelecciones) para la lista completa.

## Cobertura

- **Sintáctica:** normalización de strings comunes (PASO, generales,
  ballotage; categorías presidenciales/legislativas; identificadores de
  mesa/circuito).
- **Consultas:** el submódulo `api` está preparado para integrarse con
  fuentes oficiales (DINE, datos.gob.ar) cuando publican datasets
  consistentes.
