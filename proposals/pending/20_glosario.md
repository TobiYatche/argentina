# Propuesta: glosario

## Problema

El paquete `argentina` está pensado en español rioplatense, pero los
datos argentinos están **plagados de acrónimos** que ni los argentinos
recuerdan todos:

- Fiscales: AFIP, ARBA, AGIP, ARCA, ATM Salta, DGR, DGI, ARSE
- Estadísticos: INDEC, EPH, EAHU, IPC, IPI, ICA, EMAE, EMI
- Documentos: DNI, CUIT, CUIL, CDI, CIE, LC, LE
- Provinciales/jurisdiccionales: CABA, AMBA, GBA, PBA, IGN
- Bancarios: BCRA, CBU, CVU, ALC, MEP, CCL, MULC, MEPI
- Salud/educación: ANMAT, RENAPER, ANSES, SUSS, CONICET, INTA, INTI
- Geográficos: BAHRA, INDEC-Departamentos, IGN

Búsquedas en foros internacionales confirman que extranjeros que
trabajan con datos argentinos pierden tiempo googleando cada sigla.
La documentación oficial (datos.gob.ar, INDEC, AFIP) está
**exclusivamente en español**, sin glosario público para uso
programático.

Hoy el paquete tiene módulos por dominio (`afip`, `bancos`,
`personas`, `economia`, `geo`) pero no un **punto único de consulta
de acrónimos** que diga "qué significa esta sigla y a qué dominio
pertenece".

## Benchmark / paquete de referencia

- [`acronymsapi`](https://github.com/abrahamcalf/acronymsapi),
  [`acronym-lookup`](https://www.npmjs.com/package/acronym-lookup) —
  paquetes JS/Python para acrónimos genéricos. Inspiración
  conceptual.
- [Wikipedia listas de acrónimos argentinos](https://es.wikipedia.org/wiki/Anexo:Acr%C3%B3nimos_de_Argentina) —
  fuente referencial.
- `argentina.identificar` ya existe en el paquete: hace "qué tipo
  es este valor". Este módulo hace "qué significa esta sigla".

## Traducción a Argentina

Un módulo `argentina.glosario` con catálogo cerrado y curado de
~80–120 acrónimos del Estado argentino y del campo de datos
económicos/sociales/geográficos. Cada entrada con:

- Sigla.
- Nombre completo en español.
- Traducción al inglés (para uso internacional / cross-reference).
- Dominio (`fiscal | estadistico | bancario | documento | salud |
  educacion | geografico | judicial | ...`).
- Descripción corta.
- Link a la página oficial / Wikipedia (opcional).

**Catálogo cerrado y estable.** Las siglas de organismos del Estado
cambian muy rara vez (cuando un organismo se renombra o disuelve);
cuando pasa, se agrega entrada con `vigente_hasta`. No es un dataset
que envejece — es histórico-acumulativo.

## API propuesta

```python
import argentina as arg

# Lookup directo
arg.glosario.lookup("AFIP")
# Sigla(
#     sigla='AFIP',
#     nombre='Administración Federal de Ingresos Públicos',
#     nombre_en='Federal Administration of Public Revenue',
#     dominio='fiscal',
#     descripcion='Organismo fiscal nacional...',
#     vigente=True,
#     reemplazado_por=None,
# )

# Caso insensitive
arg.glosario.lookup("afip") == arg.glosario.lookup("AFIP")  # True

# Sigla histórica con sucesora
arg.glosario.lookup("DGI")
# Sigla(sigla='DGI', vigente_hasta=date(1997, ...),
#       reemplazado_por='AFIP', ...)

# Buscar por dominio
arg.glosario.por_dominio("fiscal")
# (Sigla('AFIP', ...), Sigla('ARBA', ...), Sigla('AGIP', ...), ...)

# Buscar por nombre/descripción (substring normalizado)
arg.glosario.buscar("ingresos públicos")
# [Sigla('AFIP', ...)]

# Listar
arg.glosario.listar()  # tuple[Sigla, ...]
arg.glosario.dominios()
# ('fiscal', 'estadistico', 'bancario', 'documento', 'salud',
#  'educacion', 'geografico', 'judicial', ...)

# Detección en texto libre
arg.glosario.extraer_siglas("Según el INDEC y AFIP, el CUIT...")
# [Sigla('INDEC', ...), Sigla('AFIP', ...), Sigla('CUIT', ...)]
```

Reglas:
- `Sigla` es dataclass frozen.
- `lookup` normaliza entrada (uppercase, sin puntos: `"A.F.I.P."` →
  `"AFIP"`).
- `vigente=False` para siglas históricas (DGI, ANSeS antes de ANSES,
  etc.); `reemplazado_por` apunta a la actual.
- `buscar` y `extraer_siglas` reusan `clean.normalizar_texto`.
- `extraer_siglas` solo matchea siglas conocidas; NO infiere ni
  inventa nuevas siglas — evita falsos positivos en mayúsculas
  irrelevantes.

## Archivos a modificar

- `src/argentina/glosario.py` — módulo nuevo. Catálogo como tupla
  literal en código (cerrado, ~100 entradas).
- `src/argentina/__init__.py` — agregar
  `from argentina import glosario`.
- `tests/test_glosario.py` — tests.
- `docs/modulos/glosario.md` — documentación con tabla completa de
  siglas por dominio.
- `notebooks/glosario_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura.

## Core o extra

**Core.** Catálogo cerrado, histórico-acumulativo. Cero
mantenimiento periódico — solo agregar entradas cuando un organismo
nuevo nace o uno viejo se renombra (eventos puntuales, no
recurrentes).

## Tests necesarios

- `lookup("AFIP")`, `lookup("afip")`, `lookup("A.F.I.P.")` → misma
  entrada.
- `lookup` para sigla inexistente → `None`.
- Cada `Sigla.dominio` está en `dominios()`.
- `por_dominio("fiscal")` devuelve al menos las siglas-tipo (AFIP,
  ARBA, AGIP).
- `buscar("ingresos públicos")` y `buscar("ingresos publicos")`
  devuelven la misma lista.
- `extraer_siglas("...AFIP, INDEC, CUIT...")` extrae las tres
  correctas; "ESTO ES SOLO MAYÚSCULAS" no extrae nada inventado.
- Las siglas históricas (DGI, ANSeS) tienen `vigente_hasta` y
  `reemplazado_por` apuntando a una sigla que **sí está en el
  catálogo**.
- `dominios()` devuelve la lista cerrada esperada.
- Sin internet, sin archivos externos.

## Riesgos

- **Curaduría inicial.** Decidir qué siglas entran y cuáles no
  requiere criterio. Mitigación: scope explícito en doc — siglas de
  organismos del Estado nacional/provincial + identificadores
  fiscales + términos estadísticos de uso frecuente. Excluye:
  acrónimos de partidos políticos, empresas privadas, ONGs.
- **Traducción al inglés.** No siempre hay traducción oficial.
  Mitigación: cuando no hay traducción establecida, usar
  descripción funcional (`'AFIP' → 'Federal Tax Authority of
  Argentina'`) y marcarlo como `nombre_en_funcional=True`. Documentar
  el criterio.
- **Solapamiento con otros módulos.** `CUIT` aparece en `personas`,
  `AFIP` aparece en `afip`. Mitigación: el glosario es **vista
  paralela** — el `lookup` devuelve metadata; las funciones
  operativas siguen en sus módulos. Documentar.
- **Crecimiento del catálogo.** Riesgo de inflar con siglas
  ultra-nicho. Mitigación: cap pragmático ~120 entradas; nuevas
  entradas requieren justificación documentada (al menos un caso de
  uso real).

## Prioridad

**Media.** Útil pero más nicho que `moneda_historica` (19) o
`fechas_texto` (16). Resuelve una barrera idiomática real pero no
está en el camino crítico de limpieza de datos. Buen módulo "puente"
para usuarios extranjeros y para apps con audiencia internacional.

## Contexto adicional

- Originada por la búsqueda en foros (2026-05-13): la documentación
  oficial argentina (INDEC, datos.gob.ar, AFIP) está
  exclusivamente en español, lo cual genera fricción documentada
  para analistas extranjeros.
- Patrón consolidado: catálogo cerrado + dataclass + lookup, igual a
  `monedas`/`presidentes`/`paises_limitrofes`. Mismo modelo, distinto
  dominio.
- Convención `import argentina as arg` respetada.
