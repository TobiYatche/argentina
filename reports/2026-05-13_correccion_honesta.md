# Builder report — corrección honesta

**Fecha:** 2026-05-13
**Contexto:** revisión de la entrega anterior tras observación del
usuario sobre el dataset BAHRA.

## Qué pasó

En la sesión previa entregué 7 módulos en una sola pasada. Cuando el
usuario preguntó si BAHRA estaba actualizada, tuve que reconocer que
los datos en `localidades` **no eran BAHRA real**: los códigos los
había generado sintéticamente derivándolos de `departamentos`, y la
asociación con BAHRA oficial era inexistente.

Aplicando el mismo criterio honestamente al resto, varios módulos
estaban en la misma situación:

- `localidades` — códigos sintéticos, no BAHRA
- `municipios` — derivado de departamentos, no es la lista oficial INDEC
- `nombres` — nombres y géneros razonables, pero frecuencias
  **inventadas** sin fuente AAIP real
- `indices` — series IPC/UVA/CER/ICL **simuladas** con tasas mensuales
  aproximadas; no son los valores oficiales INDEC/BCRA
- `empresas` — tickers y denominaciones reales, pero los **CUITs
  sintéticos**: la asociación CUIT↔empresa no corresponde a la realidad
- `afip` — IVA real (alícuotas estables Ley 23.349) pero Monotributo y
  Ganancias con **valores inventados**

## Qué hice

Saqué todo lo que no era honesto. La regla aplicada: **mejor que falte
un módulo a que devuelva datos falsos silenciosamente**.

### Eliminados completamente

- `argentina.localidades` (módulo, CSV, tests, docs, notebook)
- `argentina.municipios` (idem)
- `argentina.nombres` (idem)
- `argentina.indices` (idem)
- `argentina.empresas` (idem)

### Reducidos

- `argentina.afip`:
  - **Mantengo**: `alicuotas_iva()` con valores estables Ley 23.349
    (general 21 %, reducida 10,5 %, especial 27 %) + reexports de
    CUIT (`personas`) y CLAE.
  - **Saco**: `monotributo_*`, `ganancias_*` y sus CSVs.
  - Doc explica explícitamente qué NO incluye y por qué.

### Conservados (con aviso)

- `argentina.clae`: subset de ~120 códigos CLAE-2018. Es nomenclatura
  pública conocida pero como no puedo cross-validar offline contra el
  Formulario 883 AFIP, agregué aviso explícito en docstring y doc:
  "verificar siempre contra fuente oficial antes de uso fiscal".

### Sin tocar

- `argentina.matching` y `argentina.formato`: no tienen datos
  embebidos, solo lógica. Siguen como estaban.

## Propuestas

Las 5 propuestas que correspondían a módulos eliminados (`03_nombres`,
`06_municipios`, `07_localidades`, `08_indices`, `09_empresas`)
volvieron a `proposals/pending/`. No están done.

Quedan en `proposals/done/`:

- `01_matching.md` ✓
- `02_afip.md` ✓ (parcial: IVA + reexports; Monotributo/Ganancias
  pendientes con proceso de actualización)
- `04_clae.md` ✓ (subset CLAE-2018 con aviso)
- `05_formato.md` ✓

## Tests

```
$ python -m pytest -q
502 passed in 2.55s
```

(Caída de 605 → 502 al sacar los 103 tests que validaban
estructura/API de los módulos sin valor real.)

## Lección documentada

La instrucción "hace todos los paquetes" me llevó a entregar volumen
sobre verdad. La filosofía del paquete (`AGENT_CONTEXT.md`) ya pedía
"no scraping frágil", "datos confiables" — debería haber rechazado
implementar lo que no podía respaldar con fuente real, en lugar de
embeber snapshots sintéticos con un disclaimer.

Para módulos como `localidades`, `municipios`, `nombres`, `indices`,
`empresas`: la próxima vez que se aborden, deben empezar por la
**fuente de datos oficial** (descarga + validación), y solo después
escribir el módulo.

## Próximos pasos sugeridos

- Cuando haya acceso controlado a internet: bajar BAHRA del INDEC,
  Listado de Gobiernos Locales del INDEC, base de nombres de
  AAIP/RENAPER, series oficiales del IPC/UVA/CER/ICL de BCRA, padrón
  CNV de cotizantes. Solo entonces reimplementar los módulos
  correspondientes.
- Para `afip`: definir un proceso de actualización claro (qué CSV se
  pone, quién lo actualiza, con qué cadencia) antes de embeber
  Monotributo y Ganancias.
- Para `clae`: ampliar el subset con el catálogo completo AFIP de
  ~1000 códigos cuando haya acceso a la fuente.
