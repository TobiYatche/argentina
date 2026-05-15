# Propuesta: razones_sociales

## Problema

En cualquier planilla con empresas argentinas aparece el mismo problema:
la misma empresa escrita de cinco formas distintas.

- `"Acme S.A."`, `"Acme SA"`, `"ACME Sociedad Anónima"`, `"acme s.a"`,
  `"Acme S.A. (en formación)"`.
- `"Distribuidora del Sur SRL"`, `"DISTRIBUIDORA DEL SUR S.R.L."`,
  `"Distribuidora del Sur S R L"`.

Esto rompe cualquier `groupby` / `join` / deduplicación. Hoy el paquete
tiene:

- `argentina.clean.normalizar_texto` — quita tildes, lower, espacios.
  No conoce sufijos societarios.
- `argentina.empresas.buscar` — usa normalización del paquete pero
  para un padrón cerrado de cotizantes/estatales.

Falta el módulo que limpie y categorice **cualquier** razón social
argentina por tipo societario, sin depender de un padrón.

## Benchmark / paquete de referencia

- [`cleanco`](https://pypi.org/project/cleanco/) — limpia sufijos
  societarios (Inc., LLC, GmbH, S.A.) y devuelve el tipo. Modelo
  exactamente lo que se necesita, sin dataset.
- [`brutils`](https://github.com/brazilian-utils/python) (Brasil) —
  utilidades para CNPJ/CPF/razões sociais. Mismo enfoque: lógica
  pura, sin padrón.
- [`python-stdnum`](https://pypi.org/project/python-stdnum/) —
  `validate()`, `compact()`, `format()` por número/código. Pauta el
  patrón estándar internacional para este tipo de módulos.
- `argentina.clean` y `argentina.formato` ya marcan el patrón de
  módulos transversales sin dataset.

## Traducción a Argentina

Un módulo `argentina.razones_sociales` con catálogo embebido de
**tipos societarios argentinos** (no de empresas — la lista de tipos
es cerrada y estable, no envejece):

- S.A. — Sociedad Anónima
- S.R.L. — Sociedad de Responsabilidad Limitada
- S.A.S. — Sociedad por Acciones Simplificada
- S.A.U. — Sociedad Anónima Unipersonal
- S.C.A. — Sociedad en Comandita por Acciones
- S.C.S. — Sociedad en Comandita Simple
- S.C. — Sociedad Colectiva
- S.E. — Sociedad del Estado
- S.D.H. — Sociedad de Hecho
- Ltda. — Sociedad Limitada (uso menor)
- Coop. — Cooperativa
- Mut. — Mutual
- Aso. Civ. — Asociación Civil
- Fund. — Fundación

Más variantes ortográficas comunes para cada uno (sin puntos, con
espacios, en mayúsculas/minúsculas, "Sociedad Anónima" expandido,
etc.). Esa lista cambia rara vez — décadas — y cuando cambia se
agrega una entrada, no se reemplaza el dataset.

## API propuesta

```python
import argentina as arg

# Detectar tipo societario
arg.razones_sociales.tipo("Acme S.A.")
# 'S.A.'

arg.razones_sociales.tipo("Distribuidora del Sur S R L")
# 'S.R.L.'

arg.razones_sociales.tipo("Cooperativa de Trabajo La Juanita")
# 'Coop.'

arg.razones_sociales.tipo("Acme")  # sin sufijo reconocible
# None

# Quitar sufijo societario (devuelve el "nombre limpio")
arg.razones_sociales.quitar_sufijo("Acme S.A.")
# 'Acme'

arg.razones_sociales.quitar_sufijo("DISTRIBUIDORA DEL SUR S.R.L.")
# 'DISTRIBUIDORA DEL SUR'

# Normalizar a forma canónica
arg.razones_sociales.normalizar("acme s a")
# 'Acme S.A.'

arg.razones_sociales.normalizar("Distribuidora del Sur sociedad anónima")
# 'Distribuidora del Sur S.A.'

# Comparar dos razones (útil para deduplicar)
arg.razones_sociales.son_equivalentes("Acme S.A.", "ACME Sociedad Anónima")
# True

# Listar tipos disponibles
arg.razones_sociales.tipos()
# (TipoSocietario(sigla='S.A.', nombre='Sociedad Anónima', ...), ...)
```

Reglas:
- `TipoSocietario` es dataclass frozen con `sigla` canónica (`'S.A.'`),
  `nombre_completo` (`'Sociedad Anónima'`), `variantes` (tupla de
  formas reconocidas).
- `tipo`, `quitar_sufijo`, `normalizar` aceptan `str | None`; con
  `None` devuelven `None` (consistencia con `limpiar_*` /
  `formatear_*` del paquete).
- `son_equivalentes` compara después de `quitar_sufijo` +
  normalización del paquete (`clean.normalizar_texto`).
- La comparación es **conservadora**: solo dice `True` cuando coincide
  base + tipo. NO usa fuzzy matching (eso ya lo cubre `matching`).

## Archivos a modificar

- `src/argentina/razones_sociales.py` — módulo nuevo. Catálogo de
  tipos como tupla literal en el código (cerrado, estable, no necesita
  CSV externo).
- `src/argentina/__init__.py` — agregar
  `from argentina import razones_sociales`.
- `src/argentina/clean.py` — agregar reexports opcionales
  (`arg.clean.quitar_sufijo_societario`) con import diferido.
- `tests/test_razones_sociales.py` — tests.
- `docs/modulos/razones_sociales.md` — documentación.
- `notebooks/razones_sociales_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura (`re`). Reuso de `clean.normalizar_texto` para la
comparación.

## Core o extra

**Core.** Cero dataset que envejezca: la lista de tipos societarios
argentinos es cerrada y estable. El "dataset" son ~15 entradas
hardcodeadas en el código, no un CSV con vigencia.

## Tests necesarios

- `tipo("Acme S.A.")` = `'S.A.'`; con variantes de espaciado, puntos,
  mayúsculas/minúsculas → mismo resultado.
- `tipo("Acme")` (sin sufijo) → `None`.
- `tipo(None)` → `None`.
- `tipo("Sociedad Anónima Acme")` → `'S.A.'` (forma expandida).
- `quitar_sufijo("Acme S.A.")` = `"Acme"`; preserva mayúsculas
  originales del nombre.
- `quitar_sufijo("DISTRIBUIDORA DEL SUR S.R.L.")` =
  `"DISTRIBUIDORA DEL SUR"`.
- `normalizar(...)` canoniza a una única forma estándar.
- `son_equivalentes(a, b)` true para pares variantes/sinónimos, false
  para empresas distintas.
- Cada tipo societario tiene al menos 3 variantes ortográficas
  reconocidas en sus tests.
- Sin internet, sin archivos externos.

## Riesgos

- **Sufijos ambiguos.** `"Ltda."` se usa raramente en Argentina pero
  aparece. Mitigación: incluirlo en la lista pero documentar que su
  uso es menor.
- **Razón social que coincide con un sufijo.** Ej: una empresa que se
  llama literalmente `"S.A. Hermanos"`. Mitigación: el matching de
  sufijo se hace solo al final de la cadena (regex anclado), no en
  medio. Documentar y testear este caso.
- **Sufijos compuestos.** `"S.A. (en formación)"`, `"S.R.L. en
  liquidación"`. Mitigación: pre-procesar quitando paréntesis y
  cláusulas conocidas antes de matchear el sufijo.
- **Nuevos tipos societarios.** La Ley de Sociedades cambia rara vez
  (S.A.S. se sumó en 2017, antes de eso S.A.U. en 2014). Cuando
  cambie: agregar una entrada al código fuente, no actualizar un
  dataset. Es la diferencia clave con `obras_sociales` o
  `vencimientos`.

## Prioridad

**Alta.** Resuelve un problema diario de limpieza de datos
empresariales argentinos, sin dataset que envejezca. Encaja en la
filosofía core estricto. Habilita deduplicación de empresas en
cualquier dataset.

## Contexto adicional

- Originado por feedback del usuario (2026-05-13): preferir limpieza
  de datos general sobre módulos que requieran actualización
  periódica. Esta propuesta sigue exactamente ese criterio.
- Benchmark inspiracional: `cleanco` (Python, mismo concepto para
  USA/Europa), `brutils` (Brasil).
- Patrón consolidado del paquete: lógica + regex + dataclass frozen
  sin CSV externo, igual a `clean`/`formato`/`matching`/`patentes`.
- Convención `import argentina as arg` respetada.
