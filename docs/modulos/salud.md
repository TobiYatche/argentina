# Salud

`argentina.salud` agrupa utilidades específicas del sistema de salud
argentino: códigos sanitarios, normalización de categorías, etc.

```python
import argentina as arg

# (Ejemplos genéricos: ver API reference para la lista exacta de funciones.)
arg.salud.normalizar_obra_social("OSDE")
arg.salud.limpiar_codigo_efector("...")
```

Ver [API reference](../api.md#argentinasalud) para la lista completa de
funciones expuestas.

## Limitaciones

- Sin consultas a APIs externas (Superintendencia, PAMI, etc.).
- Normalización **sintáctica** de strings y validación de formato.
- Para padrones reales (afiliaciones, prestadores activos) hay que
  consultar las fuentes oficiales por separado.
