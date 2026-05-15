# Propuesta: auditar

## Problema

El paquete ya tiene **muchos** `limpiar_*` y `validar_*` (DNI, CUIT,
CBU, CUE, alias, código postal, patente, matricula, teléfono, monto,
fecha, dirección...). Pero todos son funciones **por valor**: el
usuario que recibe una columna de 50.000 DNIs tiene que escribir el
loop, contar válidos/inválidos, decidir qué hacer con los errores,
generar un reporte de calidad.

`argentina.identificar.identificar(valor)` resuelve "qué tipo es
este valor", pero también opera valor-a-valor.

Falta el **módulo de auditoría por lote**: pasarle una lista/Serie
de strings y un tipo (`'dni'`, `'cuit'`, `'cbu'`, ...) y obtener:

- Conteos: total, válidos, inválidos, nulos.
- Distribución de errores (top razones de invalidez).
- Sugerencia de corrección cuando aplica (ej. DNI con espacios sobrantes
  → versión limpia).
- Estadísticas de "calidad" en porcentajes.

Esto es lo que cualquiera escribe a mano la primera vez que toca un
dataset con identificadores. Un módulo que lo resuelva ahorra el
boilerplate y unifica el reporte.

## Benchmark / paquete de referencia

- [`DataPrep.clean`](https://docs.dataprep.ai/) — cada cleaner devuelve
  estadísticas del lote (% limpios, % erróneos, ejemplos). Modelo
  exacto.
- [`pandas-profiling` / `ydata-profiling`](https://github.com/ydataai/ydata-profiling) —
  audita un DataFrame entero. Inspiración conceptual; este módulo es
  mucho más acotado (un solo tipo por vez).
- `argentina.identificar` (existente) — resuelve la pieza "qué es
  este valor". Este módulo construye el agregado por lote arriba.

## Traducción a Argentina

Un módulo `argentina.auditar` que orquesta los `limpiar_*`/`validar_*`
existentes y devuelve un reporte por lote. Sin nuevos validadores —
solo agregado y reporting sobre los que ya hay.

## API propuesta

```python
import argentina as arg

dnis = ["12345678", "1234567", " 12 345 678 ", "abc", "", None, "33445566"]

# Auditar una lista contra un tipo
reporte = arg.auditar.auditar(dnis, tipo="dni")
# Reporte(
#     tipo='dni',
#     total=7,
#     validos=2,
#     invalidos=3,
#     nulos=2,
#     recuperables=1,            # se pueden limpiar y quedan válidos
#     porcentaje_validos=28.57,
#     errores_top=[('formato', 2), ('largo', 1)],
#     ejemplos_invalidos=['abc', '1234567'],
# )

# Aplicar limpieza por lote y devolver tanto los valores limpios como
# el reporte
limpios, reporte = arg.auditar.limpiar_lote(dnis, tipo="dni")
# limpios = ['12345678', None, '12345678', None, None, None, '33445566']

# Tipos soportados (todos los limpiar_*/validar_* del paquete)
arg.auditar.tipos_soportados()
# ('dni', 'cuit', 'cbu', 'alias', 'cue', 'codigo_postal', 'patente',
#  'matricula', 'telefono', 'monto', 'fecha', 'cuitanexo', ...)

# Detección automática (sin pasarle el tipo)
reporte = arg.auditar.auditar_auto(["20-12345678-1", "12345678"])
# Reporte(tipo_inferido='mixto',
#         por_tipo={'cuit': Reporte(...), 'dni': Reporte(...)})

# Auditar un DataFrame entero columna por columna (extra opcional con
# pandas, si está instalado)
arg.auditar.auditar_df(df, columnas={'documento': 'dni', 'cuit': 'cuit'})
# {'documento': Reporte(...), 'cuit': Reporte(...)}
```

Reglas:
- `Reporte` es dataclass frozen, con todos los campos enumerados.
- "Recuperables" = valores que NO pasan `validar_*` sobre el original
  pero SÍ pasan `validar_*(limpiar_*(original))`. Útil para identificar
  cuántos se rescatan con sólo limpiar formato.
- `errores_top` clasifica fallos con etiquetas estables: `'formato'`
  (caracteres inválidos), `'largo'` (cantidad de dígitos), `'checksum'`
  (dígito verificador inválido), `'fuera_rango'` (valor numérico fuera
  del rango admisible), `'desconocido'`.
- `ejemplos_invalidos`: máximo 5, primeros encontrados, para inspección
  manual.
- `auditar_auto` usa `identificar` valor a valor, agrupa por tipo y
  devuelve un reporte por tipo.
- `auditar_df`: import diferido de pandas; sin pandas, `ImportError`
  con mensaje claro.

## Archivos a modificar

- `src/argentina/auditar.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar `from argentina import auditar`.
- `tests/test_auditar.py` — tests.
- `docs/modulos/auditar.md` — documentación con tabla de tipos
  soportados y etiquetas de error.
- `notebooks/auditar_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna en core. Pandas como **extra opcional** SOLO para
`auditar_df`; si no está instalado, esa función levanta `ImportError`
claro pero el resto del módulo funciona sin problemas.

## Core o extra

**Core** (las funciones principales). `auditar_df` queda como función
con dependencia opcional.

## Tests necesarios

- `auditar(lista, tipo='dni')`: total, válidos, inválidos, nulos
  cuadran con la entrada.
- `recuperables` cuenta correctamente DNIs con espacios/puntos que se
  rescatan al limpiar.
- `errores_top` clasifica los errores con etiquetas correctas
  (formato vs largo vs checksum).
- `ejemplos_invalidos` no excede 5.
- `limpiar_lote` mantiene orden y longitud de la entrada.
- `tipos_soportados()` enumera correctamente todos los tipos del
  paquete (test que verifica completitud contra lo importado).
- `auditar_auto` con lista mixta DNIs+CUITs separa correctamente por
  tipo.
- `auditar_df` con pandas instalado: tests parametrizados que se
  saltan si pandas no está (`pytest.importorskip`).
- `auditar_df` sin pandas: `ImportError` claro.
- Lista vacía → `Reporte(total=0, ...)` sin dividir por cero.
- Reporte serializable a dict (`.as_dict()`) para integrar con JSON.
- Sin internet, sin archivos externos.

## Riesgos

- **Acoplamiento con otros módulos.** `auditar` orquesta `personas`,
  `bancos`, `educacion`, `postal`, `telefonos`, `patentes`, `salud`,
  `montos`, `fechas`. Si un módulo cambia su firma, `auditar`
  rompe. Mitigación: tabla de mapeo `tipo → (limpiar, validar)` en
  un solo lugar; tests que validan que el mapeo se mantiene.
- **Etiquetas de error.** Catálogo cerrado de etiquetas
  (`formato`/`largo`/`checksum`/...) puede no encajar limpio para
  todos los tipos. Mitigación: cada validador puede aportar etiqueta
  específica vía wrapper interno; las "no clasificadas" caen en
  `'desconocido'`.
- **Crecimiento de tipos.** Cuando se agregue un nuevo `limpiar_*`/
  `validar_*` al paquete (próximas propuestas), hay que sumarlo al
  registro de `tipos_soportados`. Mitigación: convención de
  registración explícita + test que falla si un módulo expone
  `limpiar_X`/`validar_X` que no está en el mapeo.
- **Volumen.** Para listas muy grandes (>1M), el reporte completo
  puede ser pesado. Mitigación: `auditar(..., max_ejemplos=...)`
  y `auditar(..., truncar_errores=True)` documentados. No agregar
  iteradores ni async — out of scope.

## Prioridad

**Alta.** Es el módulo "meta" que aprovecha toda la inversión previa
del paquete. Convierte el paquete en una herramienta de **auditoría
de calidad de datos argentinos** end-to-end, no sólo de validación
puntual. Cero deuda de mantenimiento (solo orquesta lo que ya existe).

## Contexto adicional

- Originada por feedback del usuario (2026-05-13): "limpieza de datos
  más general". Este módulo es exactamente eso a nivel agregado.
- Inspiración: `DataPrep.clean` (estadísticas por columna),
  `ydata-profiling` (auditoría general).
- Sinergia con `montos` (propuesta 14) y `razones_sociales`
  (propuesta 13): apenas existan, se agregan al `tipos_soportados`
  y `auditar` los cubre gratis.
- Patrón "módulo transversal que reusa otros sin reimplementar":
  igual a `formato`, `matching`, `identificar`.
- Convención `import argentina as arg` respetada.
