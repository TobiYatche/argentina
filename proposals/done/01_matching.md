# Propuesta: matching

## Problema

Los módulos `provincias`, `departamentos`, `ciudades`, `aglomerados` y `universidades`
ya tienen `lookup(...)` con normalización (lowercase + NFKD sin tildes). Pero `lookup`
es **exacto sobre el nombre normalizado**: si el usuario escribe "Bs As", "Sgo. del
Estero", "Cap. Fed.", "Tdf", "Buennos Aires" (typo), o cualquier abreviatura no
registrada como alias, `lookup` devuelve `None`.

En análisis de datos reales (planillas Excel cargadas a mano, formularios, scrapeos
de terceros) los nombres llegan sucios. Hoy el usuario tiene que limpiar manualmente
o agregar aliases uno por uno a los CSV embebidos. No hay un mecanismo público para
"matchear lo más cercano" con un score de confianza.

## Benchmark / paquete de referencia

- `rapidfuzz` / `thefuzz` (Python) — fuzzy string matching con score.
- `difflib.get_close_matches` (stdlib) — alternativa cero-deps, suficiente para
  catálogos chicos (24 provincias, ~530 departamentos, etc.).
- `us` (Python) — su `states.lookup()` también es exacto; no resuelve typos. No
  copiar, pero sirve de contraste: queremos algo más permisivo.
- `recordlinkage` / `dedupe` — overkill para este caso, son para registros con
  múltiples campos.

## Traducción a Argentina

Un módulo `argentina.matching` que ofrezca matching fuzzy sobre los catálogos ya
existentes del paquete, manteniendo la filosofía core liviano (stdlib primero).
Pensado para cuando `lookup()` exacto falla.

Casos típicos a resolver:
- "buennos aires" → `provincias.BA` (typo)
- "sgo del estero" → `provincias.SGO` (abreviatura no aliasada)
- "cordova" → `provincias.CB` (variante)
- "Gral. San Martín" vs "General San Martín" en departamentos

## API propuesta

```python
import argentina as arg

# Match contra un catálogo del paquete, devuelve el objeto o None
arg.matching.match_provincia("buennos aires")
# Provincia(codigo='06', nombre='Buenos Aires', ...)

# Match con score explícito (0.0 - 1.0)
arg.matching.match_provincia("xyz", umbral=0.6)
# None  (no llega al umbral)

# Top-N candidatos con score
arg.matching.candidatos_provincia("cordova", n=3)
# [(Provincia(...), 0.91), (Provincia(...), 0.55), ...]

# Equivalentes para los otros catálogos
arg.matching.match_departamento("gral san martin", provincia="BA")
arg.matching.match_ciudad("mar de plata")
arg.matching.match_universidad("uba")

# Función genérica para usar contra cualquier lista
arg.matching.match("cordova", candidatos=["Buenos Aires", "Córdoba", "Santa Fe"])
# ("Córdoba", 0.83)
```

Reglas:
- Antes del fuzzy, intentar `lookup()` exacto del módulo correspondiente. Si hay
  match exacto, devolverlo con score `1.0` sin pasar por fuzzy.
- Normalizar (lowercase + NFKD sin tildes + alfanumérico) ambos lados antes de
  comparar — misma normalización que ya usan los módulos existentes.
- Devolver el **mismo objeto** que devolvería `lookup()` del módulo correspondiente
  (Provincia, Departamento, Ciudad, etc.), no un dict.

## Archivos a modificar

- `src/argentina/matching.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar `from argentina import matching`.
- `tests/test_matching.py` — tests del módulo.
- `docs/modulos/matching.md` — documentación.
- `notebooks/matching_pruebas.ipynb` — notebook obligatorio (memoria del proyecto).
- `mkdocs.yml` — agregar entrada en la nav.
- `README.md` — mencionar el módulo en la lista.

## Dependencias

Ninguna. `difflib.SequenceMatcher` de stdlib es suficiente para los volúmenes del
paquete (catálogos de cientos a miles de items). Si en el futuro hace falta más
performance, agregar `rapidfuzz` como **extra opcional** (`argentina[matching-fast]`),
pero NO en core.

## Core o extra

**Core.** Sin dependencias externas, stdlib pura, encaja en la filosofía.

## Tests necesarios

- Matches exactos devuelven score `1.0` y el objeto correcto.
- Typos comunes ("buennos aires", "cordova", "mendosa") matchean al destino con
  score > 0.8.
- Abreviaturas no aliasadas ("sgo del estero", "tdf") matchean.
- Strings irrelevantes ("xyz", "asdf") devuelven `None` con umbral default.
- `umbral` configurable: bajarlo permite matches más laxos, subirlo los rechaza.
- `candidatos_*` devuelve lista ordenada por score descendente, longitud ≤ n.
- `match_departamento(..., provincia=...)` filtra antes de matchear.
- Sin internet, sin archivos externos: los catálogos vienen de los módulos existentes.

## Riesgos

- **Falsos positivos:** "san juan" podría matchear a la provincia o a varios
  departamentos. Mitigación: el módulo no decide "qué tipo de cosa es", el usuario
  elige `match_provincia` / `match_departamento` / etc. La función `match()`
  genérica acepta la lista de candidatos explícitamente.
- **Umbrales mágicos:** elegir un umbral default es arbitrario. Empezar con `0.7`
  y documentar que es ajustable. No prometer que el default es óptimo.
- **Performance:** `difflib` es O(n*m) por par. Para ~530 departamentos × N
  consultas puede sentirse en loops grandes. Documentar el límite y dejar la puerta
  abierta al extra opcional con `rapidfuzz` si aparece la necesidad real.

## Prioridad

**Alta.** Resuelve un problema concreto que aparece apenas se usan los `lookup`
contra datos reales. Es un complemento natural a módulos ya implementados (no
empieza nada nuevo desde cero), encaja en core sin sumar deps, y está listado
explícitamente en `ROADMAP.md → Próximas ideas → matching`.

## Contexto adicional

- Del historial del proyecto: la normalización canónica (lowercase + NFKD sin
  tildes + alfanumérico) ya está consolidada en `provincias` y `departamentos`.
  Este módulo la reusa, no inventa una nueva.
- Convención de imports del usuario: `import argentina as arg` → todos los
  ejemplos arriba siguen ese patrón.
- Propuesta originada desde `ROADMAP.md` (sección "Próximas ideas") + auditoría
  del repo actual; no requirió decisión nueva del usuario.
