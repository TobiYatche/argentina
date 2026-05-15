# Builder report — siete módulos nuevos en una sesión

**Fecha:** 2026-05-13
**Propuestas implementadas:** `02_afip`, `03_nombres`, `04_clae`,
`06_municipios`, `07_localidades`, `08_indices`, `09_empresas` (las 7
restantes en `proposals/pending/`).
**Estado:** todas implementadas, testeadas, documentadas. No publicado,
no mergeado.

## Resumen ejecutivo

Sesión con pedido explícito del usuario de "implementar todos los
paquetes". Las 7 propuestas pendientes (3 Alta + 4 Media) entregadas en
una sola sesión, manteniendo la consistencia del paquete:

| Propuesta | Módulo | Funciones | Tests | Notebook |
|---|---|---|---|---|
| 04_clae | `arg.clae` | 9 | 21 | ✓ |
| 02_afip | `arg.afip` | 15 | 22 | ✓ |
| 08_indices | `arg.indices` | 10 | 17 | ✓ |
| 09_empresas | `arg.empresas` | 12 | 22 | ✓ |
| 06_municipios | `arg.municipios` | 8 | 17 | ✓ |
| 07_localidades | `arg.localidades` | 8 | 16 | ✓ |
| 03_nombres | `arg.nombres` | 7 | 20 | ✓ |

**Pytest final:** `605 passed in 0.92s` (135 nuevos sobre los 470 que
había al inicio de la sesión).

## Decisión clave: snapshots ilustrativos honestos

Varias propuestas requerían datasets oficiales grandes (AFIP, CLAE,
INDEC BAHRA, RENAPER) que no se pueden bajar desde el agente sin
internet. Estrategia adoptada:

- **Embeber subsets representativos**, no exhaustivos.
- **Documentar honestamente** que el dataset es snapshot inicial.
- **Validar consistencia interna** en los tests, no valores específicos
  que no se puedan verificar.
- **Estructura lista para crecer**: misma API, basta ampliar el CSV.

Cada `docs/modulos/<modulo>.md` arranca con un bloque de aviso
explícito sobre el carácter ilustrativo del dataset.

## Cobertura por módulo

### `arg.clae` (04)

~120 códigos CLAE más usados, todos los sectores A-T cubiertos. Lookup
por código (con padding de ceros), filtros por sector/grupo, búsqueda
en descripción con normalización canónica.

### `arg.afip` (02)

Tablas Monotributo (1 año), IVA (3 años), Ganancias (1 año). API
completa. Año fuera de rango → `ValueError` con cobertura disponible.
Reexports de CUIT desde `personas` y de lookup/búsqueda desde `clae`,
todos delegando sin reimplementar.

### `arg.indices` (08)

IPC nacional INDEC, UVA, CER e ICL mensuales con valores plausibles
(2016-12 a 2025-12 para IPC/UVA/CER, 2020-01 a 2025-12 para ICL).
Funciones `ipc`, `uva`, `cer`, `icl`, `ajustar_ipc`, `factor_ipc`,
`ajustar` genérica, `cobertura`. Carga diferida con `lru_cache`.
Posicionado como complemento offline de `arg.economia` (online).

### `arg.empresas` (09)

60 entidades: 25 cotizantes BYMA, 15 estatales, 20 descentralizadas.
CUITs sintéticos pero **válidos** (pasan `personas.validar_cuit`).
Lookup por CUIT y por ticker. Scope respeta política `no datos
personales`: el doc abre con "qué NO incluye este módulo".

### `arg.municipios` (06)

~530 municipios: uno por departamento del catálogo + 15 comunas de
CABA. Lookup con desambiguación por provincia. Patrón heredado de
`departamentos`.

### `arg.localidades` (07)

~550 localidades: una cabecera por departamento + ciudades del catálogo
existente. Lookup con desambiguación por provincia o departamento.
Documenta la diferencia conceptual con `municipios`, `ciudades`,
`aglomerados` en una tabla comparativa.

### `arg.nombres` (03)

152 nombres comunes argentinos con género mayoritario y frecuencia
relativa. Aviso ético explícito en el doc sobre los límites del campo
"género". Función `genero_mayoritario` (no `genero`) que devuelve
`None` para ambiguos. Compatible con política `no datos personales`
(solo conteos agregados, sin DNI).

## Archivos tocados

### Nuevos módulos

- `src/argentina/clae.py`, `afip.py`, `indices.py`, `empresas.py`,
  `municipios.py`, `localidades.py`, `nombres.py`

### Nuevos datasets CSV

- `clae.csv`, `afip_monotributo.csv`, `afip_iva.csv`, `afip_ganancias.csv`
- `ipc_nacional.csv`, `uva.csv`, `cer.csv`, `icl.csv`
- `empresas_cotizantes.csv`, `empresas_estatales.csv`,
  `empresas_descentralizadas.csv`
- `municipios.csv`, `localidades.csv`, `nombres.csv`

### Nuevos tests

- `test_clae.py`, `test_afip.py`, `test_indices.py`, `test_empresas.py`,
  `test_municipios.py`, `test_localidades.py`, `test_nombres.py`

### Nuevos docs y notebooks

- 7 páginas en `docs/modulos/<modulo>.md`
- 7 notebooks `notebooks/<modulo>_pruebas.ipynb` (todos ejecutados)
- Entradas en `docs/api.md` y `mkdocs.yml`
- Filas en la tabla de módulos del `README.md`

### __init__ del paquete

Los 7 módulos expuestos en `src/argentina/__init__.py` con sus entradas
en `__all__`.

### Propuestas movidas

`proposals/pending/*` → `proposals/done/*` para las 7.

## Tests

```
$ python -m pytest -q
605 passed in 0.92s
```

Sin internet. Sin dependencias nuevas. `import argentina` sigue siendo
liviano (los CSVs grandes se cargan diferido con `lru_cache`).

## Filosofía respetada

- ✅ Core liviano: stdlib pura, sin nuevas deps.
- ✅ Sin scraping, sin internet.
- ✅ Sin datos personales (empresas: solo entidades públicas; nombres:
  solo conteos agregados).
- ✅ Consistencia interna: cada nuevo módulo reusa el patrón validado
  (`dataclass(frozen=True)` + CSV embebido + lookup + iterable +
  `como_tabla`).
- ✅ `import argentina as arg` respetado en todos los ejemplos.
- ✅ Notebooks obligatorios (memoria del proyecto), todos ejecutados.
- ✅ Errores explícitos en lugar de extrapolación silenciosa
  (`indices` y `afip` levantan `ValueError` para años fuera de rango).
- ✅ Datasets honestos: documentados como snapshots, no como verdad
  exhaustiva.

## No hecho (a propósito)

- No se publicó a PyPI.
- No se mergeó nada.
- No se actualizó `CHANGELOG.md` (queda para el próximo release; este
  reporte funciona como nota intermedia).
- Datasets oficiales completos: están como puerta abierta. La API
  está lista; solo hay que ampliar los CSVs.

## Próximos pasos sugeridos (fuera de scope)

- **Datos oficiales completos**: bajar desde fuentes oficiales (AAIP,
  INDEC, BCRA, CNV) y reemplazar los snapshots de muestra. Sería
  conveniente hacerlo como una tarea offline con acceso a internet
  controlado.
- **CHANGELOG y release**: este es un cambio mayor (7 módulos nuevos).
  Cuando se valide, bumpear a 0.4.0 y publicar.
- **Extra opcional `[afip-data-completo]` / `[clae-data-completo]`**:
  para los datasets grandes que no caben razonablemente en el core.

## Resumen en una línea

Siete módulos del ROADMAP entregados con API completa, tests sólidos,
documentación clara y datasets honestos. Ningún módulo agrega
dependencias ni rompe lo existente.
