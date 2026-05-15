# Notebooks

Recorridos interactivos del paquete. Dos formatos conviven acá:

## 1. Notebooks temáticos (`00_*` a `05_*`)

Recorridos cruzados — combinan varios módulos alrededor de un caso de
uso. Pensados como **onboarding**: para alguien que llega nuevo al
paquete y quiere ver de qué se trata en 5–15 minutos.

| Archivo | Cubre |
|---|---|
| [00_quickstart.ipynb](00_quickstart.ipynb) | recorrido en 5 min por las funciones más usadas |
| [01_limpieza_personas.ipynb](01_limpieza_personas.ipynb) | DNI, CUIT, nombres, estimación de año de nacimiento |
| [02_geo_basico.ipynb](02_geo_basico.ipynb) | provincias, ciudades, distancias, shapes, mapas |
| [03_direcciones_postal_telefonos.ipynb](03_direcciones_postal_telefonos.ipynb) | el trabajo sucio con bases administrativas |
| [04_bancos_afip.ipynb](04_bancos_afip.ipynb) | CBU, alias, Monotributo, IVA, Ganancias |
| [05_fechas_feriados.ipynb](05_fechas_feriados.ipynb) | fechas argentinas, feriados, ajustes por IPC |

Empezá por `00_quickstart.ipynb`. Los demás se pueden leer en cualquier
orden.

## 2. Notebooks de pruebas (`<modulo>_pruebas.ipynb`)

Recorridos exhaustivos — un módulo por notebook. Pensados como
**referencia interactiva**: cubren casos borde, comparan variantes,
muestran qué pasa con inputs raros. Útiles cuando ya sabés qué hace el
módulo y necesitás chequear un detalle.

Convención: cada vez que se agrega un módulo al paquete, también se
agrega su notebook de pruebas. Cubren todos los módulos públicos:
`bancos_pruebas`, `personas_pruebas`, `geo_*_pruebas`, etc.

## Convenciones comunes

- Todos importan así:

  ```python
  import argentina as arg
  ```

- Primera celda muestra la versión del paquete:

  ```python
  import argentina as arg
  print(f"argentina v{arg.__version__}")
  ```

- Las celdas de código son ejecutables tal cual. Las que requieren
  extras (`[geo]`, `[economia]`, etc.) lo aclaran arriba en una celda
  markdown.
- Las que necesitan red están comentadas para que el notebook se pueda
  recorrer sin conexión y sin gastar pedidos a APIs ajenas.

## ¿Cuál uso, temático o de pruebas?

- **¿Recién arrancás?** → `00_quickstart.ipynb` y los demás temáticos.
- **¿Ya conocés el paquete y querés exprimir un módulo?** →
  `<modulo>_pruebas.ipynb`.
- **¿Querés un snippet rápido para copiar?** → `examples/<modulo>_basico.py`.
- **¿Querés referencia formal?** → `docs/modulos/<modulo>.md`.
