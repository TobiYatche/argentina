# Propuesta: nombres

> ## 🚫 RECHAZADA — no reimplementar sin fuente oficial
>
> **Motivo:** la base de nombres argentinos viene de AAIP / RENAPER y
> cambia con cada año de nuevos nacimientos. Sin un proceso explícito
> de descarga oficial (script en `tools/`, cadencia anual mínima), el
> CSV embebido queda viejo o, peor, se llena con frecuencias inventadas
> que no reflejan la realidad demográfica.
>
> Hubo un intento previo (2026-05-13) con dataset sintético; se sacó
> tras observación del usuario sobre datos no verificables. Ver
> `reports/2026-05-13_correccion_honesta.md`.
>
> **Para reactivar:** primero implementar `tools/bajar_nombres.py` que
> consuma datos.gob.ar (AAIP) y valide licencia. Recién después
> volver a `pending/`.

## Problema

`argentina.personas` ya tiene utilidades para nombres (`normalizar_nombre`,
`primer_nombre`, `apellido_principal`) pero opera **sintácticamente** sobre el
string. No conoce el universo de nombres reales argentinos.

Casos que hoy no se pueden resolver con el paquete:
- "¿`Catalina` es nombre o apellido?" — el orden importa en formularios
  argentinos y a veces no es claro.
- "¿Cuán popular es `Joaquín` para nacidos en 2010?" — análisis demográfico,
  estimación de cohortes.
- "¿Es un nombre típicamente masculino o femenino?" — útil para imputar género
  cuando no está reportado (con todas las cautelas del caso).
- "¿`Tobías` y `Tobias` son el mismo nombre?" — para deduplicar registros.

Esto complementa lo que ya hace `personas` con DNI (`estimar_año_nacimiento`,
`rango_dni_de_año`) y se basa en datos públicos: la AAIP publica los nombres
inscriptos en RENAPER por año.

## Benchmark / paquete de referencia

- `gender-guesser` (Python) — clasifica nombres por género usando una base
  estática. Modelo válido, pero su dataset es internacional y no captura nombres
  argentinos (Lautaro, Catriel, Morena, Mateo con frecuencias locales).
- `names-dataset` — base global de nombres con frecuencia. Mismo problema:
  granularidad país, no por año argentino.
- `argentina.presidentes` y `argentina.universidades` ya muestran el patrón de
  "CSV embebido + dataclass frozen + lookup + listar()" — este módulo lo sigue.

## Traducción a Argentina

Un módulo `argentina.nombres` con:
- Base de nombres inscriptos en Argentina (fuente: AAIP/RENAPER, datasets
  publicados en `datos.gob.ar`).
- Para cada nombre: cantidad de inscripciones por año (o rango agregado),
  género reportado mayoritario, primer y último año de aparición notable.
- Funciones de consulta sin internet, sin scraping.

## API propuesta

```python
import argentina as arg

# Lookup directo
n = arg.nombres.lookup("Joaquín")
# Nombre(nombre='Joaquín', genero_mayoritario='M', frecuencia_total=...,
#        primer_anio=1900, ultimo_anio=2024)

# Insensible a tildes / case (reutiliza la normalización del paquete)
arg.nombres.lookup("joaquin") is arg.nombres.lookup("Joaquín")  # True

# Existencia
arg.nombres.es_nombre("Catalina")  # True
arg.nombres.es_nombre("Schwarzenegger")  # False (probablemente apellido)

# Popularidad por año
arg.nombres.frecuencia("Mateo", anio=2010)  # int
arg.nombres.top_nombres(anio=2010, n=10)
# [Nombre(...), Nombre(...), ...]

# Género mayoritario (con warning explícito en la doc sobre los límites de esto)
arg.nombres.genero_mayoritario("Catalina")  # 'F'
arg.nombres.genero_mayoritario("René")      # None  (ambiguo)

arg.nombres.listar()  # tuple[Nombre, ...]
```

Reglas:
- `Nombre` es dataclass frozen, igual patrón que `Provincia`/`Departamento`.
- Normalización: lowercase + NFKD sin tildes para el lookup; el `.nombre` del
  dataclass guarda la forma canónica con tildes.
- `genero_mayoritario` devuelve `'M'`, `'F'` o `None` cuando la diferencia
  entre conteos es menor a un umbral configurable (default 60/40).
- La doc deja explícito que esto **describe la base reportada**, no prescribe
  el género de ninguna persona individual.

## Archivos a modificar

- `src/argentina/nombres.py` — módulo nuevo.
- `src/argentina/data/nombres.csv` — base agregada (nombre, género_mayoritario,
  frecuencia_total, primer_anio, ultimo_anio). Posiblemente un segundo CSV
  `nombres_por_anio.csv` si se quiere granularidad anual completa.
- `src/argentina/__init__.py` — agregar `from argentina import nombres`.
- `tests/test_nombres.py` — tests.
- `docs/modulos/nombres.md` — documentación, con sección clara sobre límites
  éticos del campo "género".
- `notebooks/nombres_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna en core. CSV embebido + stdlib.

**Decisión a tomar en build:** el CSV completo de nombres argentinos puede ser
grande (decenas de MB si se incluye granularidad anual de todos los nombres).
Opciones:
1. CSV agregado solamente (~1-2 MB, miles de nombres). Default recomendado.
2. CSV anual completo como **extra opcional** (`argentina[nombres-anual]`)
   distribuido aparte o descargado on-demand a `~/.cache/argentina/` con
   import diferido (mismo patrón que `geo.shapes`).

Empezar con (1) y dejar (2) como evolución si aparece la necesidad.

## Core o extra

**Core** para el dataset agregado. Si se agrega granularidad anual completa más
adelante, hacerla **extra opcional**.

## Tests necesarios

- `lookup` con tildes / sin tildes / case mixto devuelve el mismo objeto.
- `es_nombre` para nombres conocidos → `True`; para palabras random → `False`.
- `genero_mayoritario` para nombres claros (Catalina, Joaquín) devuelve el
  esperado; para nombres ambiguos (René, Camilo) devuelve `None`.
- `frecuencia` con año fuera del rango embebido → `ValueError` o `0` (decidir
  en la implementación, ser consistente con `afip`).
- `top_nombres(anio, n)` devuelve `n` items ordenados por frecuencia
  descendente.
- Import del paquete sigue siendo liviano: medir tiempo de import en CI no
  regresa (ya hay `test_import_light.py` en el repo, extender ahí).
- Sin internet, sin archivos externos.

## Riesgos

- **Tamaño del CSV.** El dataset oficial de AAIP es grande. Mitigación: empezar
  con el agregado (sin granularidad anual completa), filtrar a nombres con
  frecuencia mínima razonable, comprimir el CSV si hace falta.
- **Sensibilidad del campo "género".** Imputar género desde nombre es un campo
  con problemas éticos conocidos (personas trans/no-binarias, nombres
  ambiguos). Mitigación: la doc deja claro qué *describe* el dato y qué *no*;
  la función se llama `genero_mayoritario` (no `genero`); devuelve `None` para
  ambiguos.
- **Privacidad.** La fuente AAIP publica conteos agregados, no nombres
  individuales asociados a personas. La memoria del proyecto es explícita:
  "no datos personales". Confirmar que el CSV embebido es solo conteo agregado
  por (nombre, año, género), sin DNI ni cualquier identificador. Si no se
  consigue una fuente que cumpla, descartar el módulo.

## Prioridad

**Media.** Está en `ROADMAP.md → Próximas ideas → nombres`. Útil para análisis
demográficos, pero más nicho que `matching` o `afip`. Implementar después de
los dos anteriores, y solo si se valida una fuente de datos limpia y con
licencia compatible.

## Contexto adicional

- Del historial: el módulo `personas` ya tiene la base sintáctica de manejo
  de nombres (`normalizar_nombre`, `primer_nombre`, `apellido_principal`),
  y `serie_nacimientos` muestra el patrón "datos demográficos agregados sin
  internet". `nombres` extiende ese hilo.
- Convención `import argentina as arg` respetada en todos los ejemplos.
- Propuesta originada desde `ROADMAP.md → Próximas ideas` + observación de
  que `personas` se queda corto cuando hace falta semántica sobre nombres.
