# Propuesta: vencimientos

## Problema

`argentina.afip` ya cubre tablas fiscales (Monotributo, IVA, Ganancias).
`argentina.fechas` cubre parsing y operaciones básicas con fechas.
`argentina.feriados` cubre feriados nacionales.

Falta lo que probablemente sea **la operación más frecuente de cualquier
contador/área impositiva en Argentina**: saber **cuándo vence cada
impuesto/aporte** para un CUIT dado.

AFIP publica anualmente la Resolución General con el cronograma de
vencimientos por:
- Impuesto/aporte (IVA, Ganancias, Bienes Personales, F.931 SUSS,
  Monotributo, etc.).
- Terminación del CUIT (0-1, 2-3, 4-5, 6-7, 8-9).
- Período fiscal mensual.

Hoy no hay forma en el paquete de:
- "¿Cuándo vence el IVA de marzo 2026 para un CUIT terminado en 4?"
- "¿Cuándo vence el F.931 de mayo para todos los CUITs?"
- Listar todos los vencimientos de un mes determinado.

## Benchmark / paquete de referencia

- No hay paquete Python equivalente conocido. Cada estudio contable
  mantiene su propio Excel con el cronograma AFIP.
- `argentina.feriados` marca el patrón de "calendario oficial por año
  con consulta puntual". `vencimientos` lo extiende a un calendario más
  rico (con dimensión "tipo de obligación" y "terminación CUIT").
- `argentina.afip` (ya implementado) marca el patrón de "tablas
  fiscales oficiales versionadas por año". Misma filosofía: snapshot
  por año, vigencia explícita.

## Traducción a Argentina

Un módulo `argentina.vencimientos` con:
- Cronograma AFIP de vencimientos embebido por año (RG anual).
- Funciones para consultar fecha de vencimiento por (impuesto, período,
  terminación CUIT).
- Integración opcional con `feriados`: si el vencimiento cae feriado,
  AFIP lo corre al siguiente día hábil — la función puede aplicar ese
  ajuste o devolver la fecha "cruda" según parámetro.
- Reexport del namespace desde `afip` para descubribilidad
  (`arg.afip.vencimiento_iva(...)`).

## API propuesta

```python
import argentina as arg
from datetime import date

# Vencimiento puntual
arg.vencimientos.vencimiento(
    impuesto="iva",
    periodo=date(2026, 3, 1),
    cuit="20-12345678-1",
)
# date(2026, 4, 22)

# Misma función aceptando terminación directamente
arg.vencimientos.vencimiento(
    impuesto="iva",
    periodo=date(2026, 3, 1),
    terminacion=8,
)
# date(2026, 4, 22)

# Listar todos los vencimientos del mes
arg.vencimientos.del_mes(date(2026, 4, 1))
# [Vencimiento(impuesto='iva', periodo=date(2026, 3, 1), terminacion=0,
#              fecha=date(2026, 4, 18)), ...]

# Listar impuestos cubiertos
arg.vencimientos.impuestos()
# ('iva', 'ganancias_pf', 'ganancias_pj', 'monotributo', 'f931_suss',
#  'bienes_personales')

# Próximo vencimiento para un CUIT (útil para alertas)
arg.vencimientos.proximo(
    cuit="20-12345678-1",
    impuesto="iva",
    desde=date(2026, 5, 1),
)
# Vencimiento(...)

# Listar años cubiertos
arg.vencimientos.anios_cubiertos()
# (2024, 2025, 2026)

# Aplicar corrimiento por feriado
arg.vencimientos.vencimiento(
    impuesto="iva",
    periodo=date(2026, 3, 1),
    terminacion=8,
    ajustar_feriado=True,  # default False
)
# date(2026, 4, 23)  si el 22 era feriado
```

Reglas:
- `Vencimiento` es dataclass frozen, mismo patrón que el resto del
  paquete.
- `cuit` y `terminacion` son mutuamente excluyentes; pasar ambos →
  `ValueError`. `cuit` reutiliza `personas.limpiar_cuit` antes de
  extraer la terminación.
- Año fuera del rango embebido → `ValueError` con mensaje que indique
  los años cubiertos (mismo patrón que `afip`/`indices`).
- `ajustar_feriado=True` consulta `feriados.es_feriado` con import
  diferido. Sin ese flag, devuelve la fecha cruda del cronograma RG.

## Archivos a modificar

- `src/argentina/vencimientos.py` — módulo nuevo.
- `src/argentina/data/vencimientos.csv` — cronograma por (anio,
  impuesto, periodo_mes, terminacion, fecha).
- `src/argentina/__init__.py` — agregar `from argentina import vencimientos`.
- `src/argentina/afip.py` — agregar reexports
  (`arg.afip.vencimiento`, `arg.afip.vencimientos_del_mes`) que llaman
  al módulo `vencimientos` con import diferido. NO duplicar lógica.
- `tests/test_vencimientos.py` — tests.
- `docs/modulos/vencimientos.md` — documentación, con sección clara
  sobre la cobertura de años del snapshot.
- `notebooks/vencimientos_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. CSV + stdlib. Para `ajustar_feriado=True`: import diferido de
`argentina.feriados`, que tiene `requests` como opcional — documentar
que sin ese extra el ajuste por feriado no funciona y queda explícito
con error claro.

## Core o extra

**Core.** Datos oficiales embebidos, sin scraping, sin internet.

## Tests necesarios

- `vencimiento(impuesto, periodo, terminacion)` devuelve la fecha
  correcta según el snapshot embebido.
- `vencimiento` aceptando `cuit` da el mismo resultado que pasando
  `terminacion`.
- Pasar `cuit` + `terminacion` simultáneamente → `ValueError`.
- CUIT con guiones/espacios funciona (reuso de `personas.limpiar_cuit`).
- Año fuera de rango → `ValueError` con cobertura listada.
- `del_mes(date(2026, 4, 1))` devuelve solo vencimientos de abril 2026.
- `impuestos()` devuelve la tupla esperada.
- `proximo(cuit, impuesto, desde)` ordena por fecha y devuelve el más
  cercano ≥ `desde`.
- `ajustar_feriado=True` modifica la fecha cuando corresponde, sin
  modificarla cuando no.
- Reexports desde `afip` devuelven exactamente lo mismo que llamando
  directo.
- Sin internet (sin `ajustar_feriado=True`), sin archivos externos.

## Riesgos

- **Datos que envejecen.** AFIP publica nueva RG cada año (típicamente
  diciembre del año anterior). El CSV embebido queda atrás. Mitigación:
  doc con cadencia anual de actualización; warning si el año en curso
  no está cubierto. NO extrapolar.
- **Cobertura inicial.** El builder no puede bajar la RG completa desde
  AFIP. Mitigación: snapshot ilustrativo embebido con al menos un año
  reciente; doc explícita sobre el carácter ilustrativo (mismo patrón
  que adoptó el builder para `afip`/`clae`/`localidades` según el
  reporte 2026-05-13_paquete_completo).
- **Solapamiento con `afip`.** `afip` tiene tablas (Monotributo, IVA,
  Ganancias) por año; `vencimientos` tiene fechas por
  (impuesto, período, terminación). Conviven sin solaparse. Los
  reexports desde `afip` son por descubribilidad, no por
  reimplementación.
- **Feriados como dependencia funcional.** `feriados` usa `requests`
  como opcional. Si `ajustar_feriado=True` se llama sin el extra:
  error claro. NO mockear, NO mentir.

## Prioridad

**Alta.** Operación constante en el ecosistema contable/fiscal
argentino, hoy no cubierta. Cierra una pieza natural del cuadrante
fiscal donde `afip` ya entregó tablas. Implementación mecánica: datos
+ lookup por clave compuesta + ajuste opcional por feriado.

## Contexto adicional

- Originada en la auditoría del repo + necesidad práctica. NO figura
  en `ROADMAP.md`, pero encaja en core (datos oficiales embebidos sin
  deps).
- Sigue el patrón validado por `afip`/`feriados`/`indices`:
  - dataset oficial versionado por año,
  - dataclass frozen,
  - `ValueError` con cobertura ante años fuera de rango,
  - reexport desde el módulo "hermano" (afip) por descubribilidad.
- Sugerencia adicional al cerrar: agregar `vencimientos` a
  `ROADMAP.md → Core`.
- Convención `import argentina as arg` respetada.
