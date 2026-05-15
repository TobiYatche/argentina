# Direcciones

`argentina.direcciones` hace **parseo local** de direcciones argentinas
(sin red, sin geocoding). Separa calle, altura, piso, departamento, etc., a
partir de texto libre.

Para georreferenciación real (obtener lat/lon de una dirección), ver
[Geo](geo.md) → `argentina.geo.direcciones`.

## Casos de uso

```python
import argentina as arg

arg.direcciones.parsear("Av. Santa Fe 3253, 4to A, CABA")
arg.direcciones.limpiar(" Av.  Santa Fe   3253 ")
```

Ver [API reference](../api.md#argentinadirecciones) para la lista completa
de funciones.

## ¿Cuándo usar parser local vs georef?

| Necesidad | Módulo | Requiere |
|---|---|---|
| Separar calle / altura / piso / depto | `argentina.direcciones` | nada |
| Normalizar texto antes de mandar a otro sistema | `argentina.direcciones` | nada |
| Coordenadas (lat/lon) reales | `argentina.geo.direcciones` | extra `[georef]` (red) |
| Validar contra catastro | (no implementado en el paquete) | — |
