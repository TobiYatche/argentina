# Propuesta: indices

> ## 🚫 RECHAZADA — datos que envejecen cada mes
>
> **Motivo:** IPC nacional INDEC, UVA, CER e ICL son series **mensuales**
> que se publican el mes siguiente. Embeberlas en core implica que cada
> mes el CSV queda 30 días atrás respecto a la fuente oficial. La propia
> propuesta admite "datos que envejecen, cadencia mensual de
> actualización, tests que verifican que el último mes cubierto no es
> más viejo que (mes actual - 3 meses)".
>
> Hubo un intento previo (2026-05-13) con series simuladas mediante
> tasas mensuales aproximadas; se sacó porque los valores no eran los
> oficiales y la diferencia con la realidad era arbitraria. Ver
> `reports/2026-05-13_correccion_honesta.md`.
>
> **Para reactivar:** dos caminos válidos, no implementar sin uno de
> los dos:
>
> 1. **Mantenerlo en `arg.economia` (online, ya existe)** y agregar
>    helpers `ajustar_ipc(...)` sobre la descarga online, en el extra
>    `[economia]`.
> 2. **Si va a ser offline**: agregar `tools/bajar_indices.py` con
>    cadencia mensual automatizada (GitHub Action / pre-release) que
>    refresque los CSVs antes de publicar a PyPI. Sin ese proceso, no
>    embeber.

## Problema

En Argentina, **ajustar montos por inflación es una operación diaria**
para cualquier análisis económico: salarios reales, precios históricos,
contratos indexados, comparaciones interanuales. Hoy el paquete tiene
`argentina.economia` que **descarga** las series oficiales (IPC nacional,
UVA, CER, etc.) desde datos.gob.ar usando pandas/requests.

Pero:
- `economia` necesita **internet** y dependencias pesadas (pandas,
  requests). Para cualquier script que sólo quiera "convertir $10k de
  2010 a pesos de hoy", arrastrar pandas y hacer una llamada HTTP es
  sobreingeniería.
- `economia` da la serie cruda, **no la operación**. Ajustar a mano
  exige tomar el índice de la fecha origen, el de la fecha destino,
  multiplicar — todos los usuarios reescriben lo mismo.

Falta un módulo **offline** con los índices oficiales embebidos por mes
(IPC nacional, UVA, CER, ICL) y funciones que hagan la operación de
ajuste directamente, sin internet ni pandas.

## Benchmark / paquete de referencia

- `inflate` (R) — ajusta valores monetarios por inflación. Ese patrón
  exactamente: dataset embebido + funciones de conversión.
- `argentina.feriados` muestra el patrón "datos oficiales versionados
  por año/mes embebidos, sin internet, sin pandas". Misma filosofía
  acá.
- `argentina.economia` queda como **complemento online**: para series
  largas, datos crudos, análisis con pandas. `indices` queda como
  **operación offline**: para conversiones rápidas en cualquier script.

## Traducción a Argentina

Un módulo `argentina.indices` con:
- IPC Nacional mensual (INDEC, base 2016=100) embebido como CSV.
- UVA y CER diarios — solo último valor de cada mes embebido (sino el
  CSV crece a decenas de miles de filas). Para granularidad diaria, el
  usuario usa `economia`.
- ICL (Índice de Contratos de Locación, BCRA) mensual.
- Funciones que hacen la operación de ajuste directamente, devolviendo
  el monto convertido.

## API propuesta

```python
import argentina as arg
from datetime import date

# Ajustar un monto por IPC entre dos fechas
arg.indices.ajustar_ipc(10_000, desde=date(2010, 1, 1), hasta=date(2026, 5, 1))
# 2_345_678.90  (float, en pesos del mes destino)

# Obtener el valor de un índice en un mes
arg.indices.ipc(date(2026, 4, 1))
# 1234.56

arg.indices.uva(date(2026, 5, 1))
# 1567.89

# Factor de ajuste entre dos fechas (para reusar)
arg.indices.factor_ipc(desde=date(2010, 1, 1), hasta=date(2026, 5, 1))
# 234.56

# Listar índices disponibles
arg.indices.disponibles()
# ('ipc_nacional', 'uva', 'cer', 'icl')

# Versión genérica con nombre de índice
arg.indices.ajustar("ipc_nacional", 10_000, desde=..., hasta=...)
arg.indices.ajustar("uva", 10_000, desde=..., hasta=...)

# Rango cubierto por cada índice
arg.indices.cobertura("ipc_nacional")
# (date(2016, 12, 1), date(2026, 4, 1))
```

Reglas:
- Todas las funciones aceptan `datetime.date` o `datetime.datetime`;
  internamente truncan al primer día del mes para IPC/ICL (datos
  mensuales). UVA y CER documentan que solo está el último valor del
  mes embebido.
- Si la fecha pedida está fuera del rango cubierto: `ValueError` con
  mensaje claro indicando el rango disponible (mismo patrón que `afip`
  en propuesta 02). NO extrapolar silenciosamente.
- IPC nacional INDEC arranca en diciembre 2016 (cambio metodológico).
  Para fechas previas hay que usar IPC-CABA o IPC San Luis empalmados.
  **Decisión:** este módulo embebe SOLO IPC nacional INDEC desde
  diciembre 2016. Empalmes con series previas quedan fuera de scope —
  el usuario que necesite series largas usa `economia`.

## Archivos a modificar

- `src/argentina/indices.py` — módulo nuevo.
- `src/argentina/data/ipc_nacional.csv` — IPC mensual INDEC (~120 filas
  desde 2016).
- `src/argentina/data/uva.csv` — UVA fin de mes (~120 filas).
- `src/argentina/data/cer.csv` — CER fin de mes (~120 filas).
- `src/argentina/data/icl.csv` — ICL mensual (~80 filas desde 2020).
- `src/argentina/__init__.py` — agregar `from argentina import indices`.
- `tests/test_indices.py` — tests.
- `docs/modulos/indices.md` — documentación con tabla de cobertura y
  guía "cuándo usar `indices` (offline) vs `economia` (online)".
- `notebooks/indices_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. CSV + stdlib. Esto es **clave**: hoy `economia` arrastra
pandas/requests; `indices` resuelve el 80% de los casos sin ninguna de
las dos.

## Core o extra

**Core.** Sin dependencias externas, sin internet.

## Tests necesarios

- `ipc(date(2020, 1, 1))` devuelve el valor INDEC oficial conocido.
- `ajustar_ipc(100, desde, hasta)` con `desde == hasta` devuelve `100`
  (factor 1).
- `ajustar_ipc(100, desde=X, hasta=Y) * ajustar_ipc(1, desde=Y, hasta=X)`
  ≈ `100` (reversibilidad, con tolerancia de redondeo).
- Fecha fuera de rango → `ValueError`.
- `disponibles()` devuelve la tupla esperada.
- `ajustar("ipc_nacional", ...)` y `ajustar_ipc(...)` dan el mismo
  resultado.
- `cobertura(indice)` devuelve los extremos correctos.
- Spot-check con un puñado de pares (mes, valor) verificados contra
  publicación INDEC/BCRA — no probar la serie entera.
- Tiempo de import del paquete no regresa (extender
  `test_import_light.py`): este módulo NO debe cargar todos los CSV en
  import-time; carga diferida con `@lru_cache` o similar.
- Sin internet, sin archivos externos.

## Riesgos

- **Datos que envejecen.** Cada mes INDEC publica un nuevo dato. El
  CSV embebido queda atrás. Mitigación: documentar cadencia mensual de
  actualización; tests que verifican que el último mes cubierto no es
  más viejo que (mes actual - 3 meses) (con tolerancia configurable),
  y que el test no se ejecute en modo strict por default — solo
  warning, para no bloquear CI.
- **Empalmes de series.** IPC nacional INDEC arranca en 2016. Antes
  hay que empalmar con IPC-CABA / IPC San Luis. **Esta propuesta NO
  empalma** — empalmes son metodológicamente delicados y agregan
  superficie. Si se necesita serie larga, usar `economia` o un módulo
  futuro `indices_empalmados` (decisión separada).
- **Solapamiento con `economia`.** Riesgo de confusión "¿uso indices
  o economia?". Mitigación: doc explícita en ambos módulos con la
  guía: corto+offline+rápido → `indices`; largo+online+análisis con
  pandas → `economia`.
- **Precisión.** Operar con floats puede acumular error en series
  largas. Mitigación: usar `decimal.Decimal` internamente para las
  multiplicaciones y devolver float al final, o documentar la
  precisión esperada (4-6 decimales significativos).

## Prioridad

**Alta.** Es una operación constante en cualquier análisis económico
argentino; hoy no tiene una forma simple en el paquete. Implementación
mecánica (datos + multiplicaciones), bajo riesgo técnico, alto valor
inmediato. Resuelve el caso de uso "convertir un monto de fecha A a
fecha B" sin arrastrar `economia` + pandas + internet.

## Contexto adicional

- Originada en la auditoría del repo, no figura textualmente en
  `ROADMAP.md` pero encaja en la sección "Opcionales → economia" como
  contraparte offline. Sugerencia: agregar `indices` a `ROADMAP.md →
  Core` como parte del cierre del ciclo.
- Del historial: la memoria del proyecto registra que `economia` se
  decidió pesado a propósito (pandas/requests OK ahí). Esta propuesta
  **no toca** esa decisión, solo agrega un módulo paralelo y liviano.
- Del historial: el patrón "datos oficiales embebidos por fecha con
  vigencia" ya está validado por `feriados`.
- Convención `import argentina as arg` respetada.
