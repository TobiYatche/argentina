# Propuesta: afip

## Problema

`ROADMAP.md` lista `afip` dentro de **core**, pero el módulo no existe. Hoy lo
relacionado con AFIP está disperso:
- `argentina.personas` tiene `limpiar_cuit`, `validar_cuit`, `tipo_cuit`,
  `formatear_cuit`, `extraer_dni_de_cuit`, `generar_cuit` — todo CUIT, mezclado
  con DNI y nombres.
- No hay datos fiscales (categorías de Monotributo, alícuotas, mínimos, escalas).

Quien hace análisis de datos económicos/contables en Argentina necesita
constantemente: "¿qué categoría de Monotributo le corresponde a alguien que
factura X?", "¿cuál es el mínimo no imponible vigente?", "¿qué alícuota de IVA
aplica?". Hoy hay que buscar a mano en la web de AFIP cada vez.

Esto **no es scraping**: son tablas oficiales publicadas en PDF/HTML por AFIP,
que cambian pocas veces al año. Se embeben como CSV con `año_vigencia_desde` /
`año_vigencia_hasta` y se versionan con el paquete.

## Benchmark / paquete de referencia

- No hay paquete Python equivalente conocido. Lo más cercano: librerías
  contables internas de estudios, no publicadas.
- `argentina.feriados` ya marca la pauta de "datos oficiales versionados por año
  con vigencia". Misma filosofía acá.
- `argentina.economia` muestra cómo manejar series temporales, pero ese módulo
  es para descarga online (extra). El módulo `afip` propuesto es lo opuesto:
  tablas chicas embebidas, sin internet.

## Traducción a Argentina

Un módulo `argentina.afip` con:
- Categorías de Monotributo vigentes por año (A, B, C, ... + topes de
  facturación, alquileres, energía, superficie, valor unitario).
- Alícuotas de IVA (general 21%, reducida 10.5%, especial 27%, etc.) con
  vigencia.
- Mínimo no imponible de Ganancias por año.
- Conversión "facturación anual → categoría Monotributo".
- Funciones CUIT reexportadas desde `personas` para descubribilidad (no
  duplicar la implementación).

## API propuesta

```python
import argentina as arg

# Categorías Monotributo
arg.afip.monotributo_categorias(anio=2026)
# [Categoria(letra='A', tope=...), Categoria(letra='B', tope=...), ...]

arg.afip.monotributo_categoria_por_facturacion(15_000_000, anio=2026)
# Categoria(letra='C', ...)

# IVA
arg.afip.alicuotas_iva(anio=2026)
# {'general': 0.21, 'reducida': 0.105, 'especial': 0.27}

# Ganancias
arg.afip.ganancias_minimo_no_imponible(anio=2026)
# 3_600_000  (o lo que corresponda)

# CUIT: reexports de personas, sin reimplementar
arg.afip.validar_cuit("20-12345678-1")
arg.afip.limpiar_cuit("...")
arg.afip.formatear_cuit("...")
arg.afip.tipo_cuit("...")  # 'persona_fisica' | 'persona_juridica' | ...
```

Reglas:
- Dataclasses frozen para `Categoria`, `Alicuota`, etc. — mismo patrón que
  `Provincia`/`Departamento`.
- Todas las funciones aceptan `anio` con default = año actual (`datetime.date.today().year`).
- Si se pide un año fuera del rango de datos embebidos: `ValueError` con mensaje
  claro indicando el rango disponible. NO devolver silenciosamente datos
  desactualizados.

## Archivos a modificar

- `src/argentina/afip.py` — módulo nuevo.
- `src/argentina/data/afip_monotributo.csv` — categorías por año.
- `src/argentina/data/afip_iva.csv` — alícuotas por año.
- `src/argentina/data/afip_ganancias.csv` — mínimo no imponible por año.
- `src/argentina/__init__.py` — agregar `from argentina import afip`.
- `tests/test_afip.py` — tests.
- `docs/modulos/afip.md` — documentación.
- `notebooks/afip_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md` — entradas correspondientes.

NO modificar `personas.py`: las funciones CUIT siguen viviendo ahí, `afip` solo
las reexporta.

## Dependencias

Ninguna. CSV + stdlib. Misma filosofía que `provincias`/`feriados`.

## Core o extra

**Core.** Está listado en `ROADMAP.md → Core → afip`. Sin deps externas.

## Tests necesarios

- Cada año embebido devuelve la estructura correcta de categorías Monotributo.
- `monotributo_categoria_por_facturacion`: facturación por debajo del tope de
  A → categoría A; en el límite exacto → la categoría correspondiente;
  facturación que excede todas → `None` (o categoría "excede", a definir).
- Año fuera de rango → `ValueError`.
- Las reexports de CUIT funcionan igual que `personas.validar_cuit`, etc.
  (importar ambos y verificar identidad de comportamiento, no implementación).
- Sin internet, sin archivos externos.

## Riesgos

- **Datos que envejecen:** las tablas AFIP cambian (en general una vez al año,
  a veces dos por inflación). Mitigación: el CSV tiene `vigencia_desde` /
  `vigencia_hasta`, y los tests verifican que el año actual esté siempre
  cubierto. Es responsabilidad del mantenedor actualizar las tablas con cada
  resolución general — documentarlo en `docs/modulos/afip.md`.
- **Confusión de scope:** alguien podría esperar que `afip` calcule impuestos
  end-to-end o emita facturas. El módulo es **solo tablas oficiales + lookups**,
  no un motor fiscal. Documentarlo explícitamente en el primer párrafo de la
  doc.
- **Solapamiento con `personas`:** reexportar CUIT puede confundir sobre dónde
  vive la implementación. Mitigación: documentar en ambos módulos que la
  implementación canónica está en `personas` y `afip` reexporta por
  descubribilidad.

## Prioridad

**Alta.** Cierra un gap explícito del roadmap (está en *core* y nunca se
implementó). Encaja en la filosofía sin fricción. Tiene demanda real para
cualquier análisis económico-contable argentino.

## Contexto adicional

- Inconsistencia detectada en la auditoría: `afip` figura en `ROADMAP.md → Core`
  pero el módulo no existe en `src/argentina/`. Se reporta también en
  `reports/inconsistencies.md`. Esta propuesta es la forma concreta de
  resolverlo.
- Del historial: el patrón "CSV embebido + dataclass frozen + lookup" ya está
  validado por `provincias`/`departamentos`. Este módulo lo reusa.
- Del historial (`feedback_idioma_y_estilo`): nombres de funciones en español
  (`monotributo_categorias`, `alicuotas_iva`, etc.), sin features no pedidas
  (no caché, no async, no descarga online).
