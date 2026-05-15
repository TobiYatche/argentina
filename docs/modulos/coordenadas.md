# Coordenadas

`argentina.coordenadas(valor)` resuelve coordenadas `(lat, lon)` a partir de
cualquier identificador que entienda el paquete: nombre de ciudad, provincia,
aeropuerto, objetos del paquete, o tuplas que ya vengan armadas.

```python
import argentina as arg

arg.coordenadas("Córdoba")               # (-31.4201, -64.1888)
arg.coordenadas("Buenos Aires")          # capital de la provincia
arg.coordenadas("CABA")                  # alias
arg.coordenadas("EZE")                   # aeropuerto
arg.coordenadas(arg.provincias.MENDOZA)  # objeto Provincia
arg.coordenadas((-34.6, -58.4))          # tuple directa
```

Cuando no encuentra match devuelve `None`.

## Para qué sirve

Es el atajo que usa internamente `argentina.geo.distancia(a, b)`. Si tenés
nombres sucios y querés un par `(lat, lon)` sin abrir cinco módulos:

```python
a = arg.coordenadas("rosario")
b = arg.coordenadas("eze")
```

## Orden de resolución

`coordenadas` prueba en este orden:

1. ¿Es ya una tupla `(lat, lon)` válida?
2. ¿Es un objeto `Ciudad`/`Provincia`/`Aeropuerto`?
3. ¿Matchea con `arg.ciudades.lookup`?
4. ¿Matchea con `arg.aeropuertos.lookup`?
5. ¿Matchea con `arg.provincias.lookup` (devuelve coordenadas de la capital)?

Stdlib pura, sin red.
