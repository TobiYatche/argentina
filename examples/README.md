# Ejemplos

Scripts mínimos, reproducibles y autocontenidos. **Un módulo por archivo.**

Cada `*_basico.py` es el ejemplo más chico posible para arrancar con un
módulo: lo que copiarías y pegarías en una shell para ver si funciona.

## Convenciones

- Todos importan así:

  ```python
  import argentina as arg
  ```

  Es la convención canónica del paquete. Si abrís un notebook, un script
  o la documentación, vas a ver siempre `arg.` adelante.

- Cada script corre con `python examples/<nombre>.py` sin argumentos.
- Sin dependencias extras a menos que el módulo las requiera (en ese
  caso el script lo aclara arriba con un comentario tipo
  `# requiere: pip install "argentina[geo]"`).
- Los outputs van a stdout con `print(...)`. Sin frameworks, sin CLIs.

## ¿Cómo se elige `examples/` vs `notebooks/`?

| | `examples/*.py` | `notebooks/*.ipynb` |
|---|---|---|
| Formato | script de Python | Jupyter notebook |
| Tono | mínimo reproducible | recorrido didáctico |
| Audiencia | "dame el snippet" | "explicámelo paso a paso" |
| Tests | sirven como smoke test | no se ejecutan en CI |
| Cuándo usar uno | querés ver la API rápido | querés entender el porqué |

Los dos tienen el mismo scope (módulo por módulo), pero distinto público.

## Mapa

```
examples/
├── provincias_basico.py
├── personas_basico.py
├── postal_basico.py
├── ...                          # un script por módulo
└── README.md                    # este archivo
```

## ¿Y los temáticos?

Los recorridos cruzados (quickstart, limpieza de personas, geo,
direcciones+postal+teléfonos, bancos+AFIP, fechas+feriados+índices)
viven como notebooks numerados `00..05` en `notebooks/`. No se replican
acá para no duplicar mantenimiento.
