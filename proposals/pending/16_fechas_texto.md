# Propuesta: fechas_texto

## Problema

`argentina.fechas` cubre el camino numérico: `parsear_fecha("13/05/2026")`,
`es_fecha_valida`, `fecha_iso`, `edad_en_anios`, `cohorte_nacimiento`,
`anio_lectivo`, `mes_anio`. Resuelto.

Lo que falta es el camino que aparece en cualquier dato exportado de
sistemas argentinos o pegado de Excel/PDF/contratos:

- `"13 de mayo de 2026"` (fecha extendida en español)
- `"mayo de 2024"` / `"mayo 2024"` (mes-año sin día)
- `"marzo/2024"`, `"mar-24"`, `"mar/24"`
- `"primer trimestre de 2024"`, `"Q1 2024"`, `"1T 2024"`, `"I trim. 2024"`
- `"primer semestre 2024"`, `"S1 2024"`, `"1S 2024"`
- `"ayer"`, `"hoy"`, `"mañana"`, `"anteayer"`
- `"lunes pasado"`, `"viernes que viene"`
- `"fin del mes pasado"`, `"principio del año"`
- `"2024"` solo (año pelado)

Hoy hay que escribir el regex/diccionario a mano para cada caso.
Ningún módulo del paquete cubre lenguaje natural argentino.

## Benchmark / paquete de referencia

- [`dateparser`](https://github.com/scrapinghub/dateparser) — parser
  de fechas en lenguaje natural multi-idioma. Modelo conceptual. Pero
  arrastra dependencias y soporta 200 idiomas: overkill y peso
  innecesario para el caso argentino.
- [`DataPrep.clean_date`](https://docs.dataprep.ai/) — limpieza de
  columnas de fechas con detección de formato.
- [`maya`](https://github.com/timofurrer/maya) — parsing de fechas
  inteligente. Inspiración conceptual.
- `argentina.fechas` ya existe en el paquete. Esta propuesta lo
  **extiende** con un módulo paralelo orientado a texto.

## Traducción a Argentina

Un módulo `argentina.fechas_texto` enfocado **sólo en español
rioplatense**, con regex + reglas hardcodeadas (sin dataset). Devuelve
`date` para fechas puntuales y `tuple[date, date]` para
períodos/rangos.

## API propuesta

```python
import argentina as arg
from datetime import date

# Fechas puntuales en lenguaje natural
arg.fechas_texto.parsear("13 de mayo de 2026")
# date(2026, 5, 13)

arg.fechas_texto.parsear("13 de may de 2026")
# date(2026, 5, 13)

arg.fechas_texto.parsear("mayo de 2024")
# date(2024, 5, 1)  # primer día del mes — documentar

arg.fechas_texto.parsear("mar-24")
# date(2024, 3, 1)

# Relativas (requieren `hoy=`; sin hoy, usan date.today())
arg.fechas_texto.parsear("ayer", hoy=date(2026, 5, 13))
# date(2026, 5, 12)

arg.fechas_texto.parsear("anteayer", hoy=date(2026, 5, 13))
# date(2026, 5, 11)

arg.fechas_texto.parsear("lunes pasado", hoy=date(2026, 5, 13))
# date(2026, 5, 11)

# Períodos: devuelven (inicio, fin) inclusivos
arg.fechas_texto.parsear_periodo("primer trimestre de 2024")
# (date(2024, 1, 1), date(2024, 3, 31))

arg.fechas_texto.parsear_periodo("Q1 2024")
# (date(2024, 1, 1), date(2024, 3, 31))

arg.fechas_texto.parsear_periodo("1S 2024")
# (date(2024, 1, 1), date(2024, 6, 30))

arg.fechas_texto.parsear_periodo("mayo 2024")
# (date(2024, 5, 1), date(2024, 5, 31))

arg.fechas_texto.parsear_periodo("2024")
# (date(2024, 1, 1), date(2024, 12, 31))

# Detección sin parsear
arg.fechas_texto.es_periodo("Q1 2024")  # True
arg.fechas_texto.es_periodo("13/05/2026")  # False (es fecha puntual)
arg.fechas_texto.es_relativa("ayer")  # True

# Catálogo de meses/días reconocidos (constante pública, no envejece)
arg.fechas_texto.MESES
# {'enero': 1, 'ene': 1, 'feb': 2, 'febrero': 2, ...}

arg.fechas_texto.DIAS_SEMANA
# {'lunes': 0, 'lun': 0, 'l': 0, ...}
```

Reglas:
- Devuelve `None` ante input no reconocido (consistencia con
  `limpiar_*`). No levanta.
- `parsear` siempre devuelve `date | None`. Para período, usar
  `parsear_periodo` explícitamente.
- Para mes-año sin día (`"mayo de 2024"`): `parsear` devuelve el
  primer día del mes; `parsear_periodo` devuelve el rango completo del
  mes.
- Las funciones relativas (`"ayer"`, `"lunes pasado"`) requieren `hoy=`
  opcional; sin él, usan `date.today()`. Esto deja el módulo testable
  sin congelar tiempo.
- NO infiere zona horaria. Trabaja con `date`, no `datetime`. Quien
  necesite zona, usa `fechas` + `datetime`.
- Reusa internamente `argentina.fechas.parsear_fecha` para los
  formatos numéricos (no reimplementa).

## Archivos a modificar

- `src/argentina/fechas_texto.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar `from argentina import fechas_texto`.
- `src/argentina/fechas.py` — agregar reexports opcionales con import
  diferido: `arg.fechas.parsear_texto = fechas_texto.parsear` para
  descubribilidad.
- `tests/test_fechas_texto.py` — tests.
- `docs/modulos/fechas_texto.md` — documentación con tabla de formatos
  reconocidos y limitaciones explícitas.
- `notebooks/fechas_texto_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura (`re`, `datetime`).

## Core o extra

**Core.** Cero dataset. Solo regex + tablas hardcodeadas de
meses/días en español rioplatense (cerradas, no envejecen).

## Tests necesarios

- Fechas extendidas (`"13 de mayo de 2026"`, `"13 de may de 2026"`,
  con/sin tildes, mayúsculas/minúsculas).
- Mes-año sin día → primer día del mes en `parsear`; rango completo
  en `parsear_periodo`.
- Trimestres en todas las variantes (`"Q1 2024"`, `"1T 2024"`,
  `"primer trimestre de 2024"`, `"I trim. 2024"`) → mismo rango.
- Semestres (`"S1 2024"`, `"1S 2024"`, `"primer semestre"`).
- Año solo (`"2024"`) → rango completo del año.
- Relativas con `hoy=` fijo: `"ayer"`, `"anteayer"`, `"mañana"`,
  `"hoy"`.
- Día de la semana relativo (`"lunes pasado"`, `"viernes que viene"`):
  test con `hoy=` fijo para que sea determinista.
- Input nulo, vacío, basura → `None`.
- `MESES` y `DIAS_SEMANA` tienen todas las claves esperadas con
  abreviaturas comunes.
- Sin internet, sin archivos externos.

## Riesgos

- **Ambigüedad lengua.** `"3 mar"` ¿es 3 de marzo o "3 días marzo"?
  Mitigación: regex anclado al patrón completo; lo que no matchea
  exactamente devuelve `None`. NO inventar.
- **"Mes" vs "trimestre" confuso.** `"mayo 2024"` es mes;
  `"Q2 2024"` es trimestre. `parsear` y `parsear_periodo` son
  funciones distintas — el usuario elige semántica.
- **Tildes inconsistentes.** `"miércoles"` vs `"miercoles"`. Mitigación:
  normalizar entrada con `clean.quitar_tildes` antes del match.
- **Crecimiento de superficie.** Tentación de agregar `"hace 3 meses"`,
  `"último cuatrimestre"`, etc. **Decisión:** el módulo cubre lo que
  está en el catálogo cerrado documentado. Nuevas formas se agregan
  con propuesta explícita, no en silencio.

## Prioridad

**Alta.** Cubre un caso de uso frecuentísimo (parsear fechas pegadas
de PDFs, contratos, planillas) que hoy obliga a regex artesanal. Cero
deuda de mantenimiento — la lista de meses/días/períodos en español
no envejece.

## Contexto adicional

- Originada por feedback del usuario (2026-05-13): preferir limpieza
  de datos general sobre módulos que requieran actualización.
- Complementa `argentina.fechas` (numérico) con texto natural.
- Patrón consolidado: módulo transversal sin dataset, igual a
  `clean`/`formato`/`matching`/`razones_sociales` (13)/`montos` (14).
- Convención `import argentina as arg` respetada.
- Benchmark de inspiración: `dateparser` (modelo) y
  `DataPrep.clean_date` (mismo problema).
