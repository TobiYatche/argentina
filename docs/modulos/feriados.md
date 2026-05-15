# Feriados

`argentina.feriados` consulta el calendario oficial de feriados argentinos.

!!! warning "Extra requerido"
    Necesita `requests`. Instalá con:

    ```bash
    pip install "argentina[feriados]"
    ```

## API básica

```python
import argentina as arg

arg.feriados.obtener(2026)            # lista de feriados del año
arg.feriados.es_feriado("2026-05-25")  # True/False
arg.feriados.detalle("2026-05-25")     # dict con nombre, tipo, etc.
arg.feriados.proximo("2026-05-01")     # el próximo feriado a partir de la fecha
```

## Cache

`obtener(anio)` baja la lista una vez por año y la cachea con `lru_cache`
(32 años en memoria). Las funciones derivadas (`es_feriado`, `detalle`,
`proximo`) reutilizan ese cache, así que después de la primera llamada por
año no vuelven a pegar a la red.

## `proximo`

```python
arg.feriados.proximo()                  # desde hoy
arg.feriados.proximo("2026-12-26")       # cerca de fin de año
```

Si no encuentra feriados restantes en el año actual, salta automáticamente al
siguiente. Útil para responder "¿qué feriado viene?".

## Imports diferidos

El módulo se puede importar incluso sin `requests` instalado — `import
argentina` y `import argentina.feriados` no requieren la dependencia. Solo
se necesita al llamar funciones que consultan la API.

Sin el extra:

```
ImportError: Para usar argentina.feriados instalá el extra:
pip install "argentina[feriados]"
```
