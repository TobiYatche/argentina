# Propuesta: formato

## Problema

El paquete hoy tiene funciones `formatear_*` dispersas:

- `argentina.personas.formatear_dni`, `formatear_cuit`
- `argentina.bancos.formatear_cbu`
- `argentina.patentes.formatear`

Lo que falta para casos diarios:
- `formatear_telefono` — `1140404040` → `(11) 4040-4040`, o E.164
  (`+5491140404040`), o internacional con espacios.
- `formatear_pesos` — `1500000` → `$ 1.500.000` (separador miles `.`,
  decimales `,` como manda Argentina).
- `formatear_codigo_postal` — CP4 vs CPA con formato consistente.
- `formatear_fecha` — fechas con formato local (`dd/mm/aaaa`), nombres de
  meses en español.

Además, el patrón actual tiene una inconsistencia: `patentes.formatear` se
llama solo `formatear` (sin sufijo), mientras `personas.formatear_dni` /
`personas.formatear_cuit` sí tienen sufijo. La convención no está unificada.

## Benchmark / paquete de referencia

- `babel` (Python) — formateo localizado de números, fechas, monedas.
  Resuelve mucho, pero suma una dependencia pesada y es overkill para
  Argentina específicamente.
- `argentina.clean` ya marca el patrón de "módulo transversal con utilidades
  comunes". Este módulo es el equivalente para formateo de salida.
- `us.states.lookup()` y `us.states.STATES_AND_TERRITORIES` muestran cómo
  un paquete-país agrupa utilidades por dominio. Aplicar la misma lógica acá.

## Traducción a Argentina

Un módulo `argentina.formato` que:
1. Agrega funciones de formateo nuevas (teléfono, pesos, código postal,
   fecha).
2. Re-exporta las funciones `formatear_*` existentes de otros módulos para
   descubribilidad.
3. No reimplementa nada de lo que ya existe — solo importa y reexporta.

El módulo es el **punto único de entrada** para "¿cómo formateo X para
mostrar?", sin reemplazar las funciones donde ya viven.

## API propuesta

```python
import argentina as arg

# Nuevas
arg.formato.telefono("1140404040")
# '(011) 4040-4040'

arg.formato.telefono("1140404040", estilo="e164")
# '+5491140404040'

arg.formato.telefono("1140404040", estilo="internacional")
# '+54 9 11 4040-4040'

arg.formato.pesos(1_500_000)
# '$ 1.500.000'

arg.formato.pesos(1_500_000.50, decimales=2)
# '$ 1.500.000,50'

arg.formato.codigo_postal("C1414BAA")
# 'C1414BAA'  (CPA en mayúsculas, sin espacios)

arg.formato.codigo_postal("1414")
# '1414'  (CP4)

arg.formato.fecha(date(2026, 5, 13))
# '13/05/2026'

arg.formato.fecha(date(2026, 5, 13), estilo="largo")
# '13 de mayo de 2026'

# Reexports desde otros módulos (la implementación NO vive acá)
arg.formato.dni("12345678")       # → personas.formatear_dni
arg.formato.cuit("20123456781")   # → personas.formatear_cuit
arg.formato.cbu("...")            # → bancos.formatear_cbu
arg.formato.patente("ab123cd")    # → patentes.formatear
```

Reglas:
- Todas las funciones devuelven `str` o `None` (si el input no es
  formateable, no hacer `raise`, devolver `None` — consistencia con los
  `limpiar_*` existentes).
- `estilo` cuando aplica es un keyword con default sensato; valores válidos
  enumerados en la docstring.
- Los reexports son **funciones, no aliases module-level**: definir
  `def dni(valor): return personas.formatear_dni(valor)` para que la firma
  y la documentación sean explícitas. Import diferido si hace falta.

## Archivos a modificar

- `src/argentina/formato.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar `from argentina import formato`.
- `tests/test_formato.py` — tests para las funciones nuevas + tests de que
  los reexports devuelvan lo mismo que la función original.
- `docs/modulos/formato.md` — documentación con tabla "¿necesitás formatear
  X? → usá esta función".
- `notebooks/formato_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

NO modificar `personas.py`, `bancos.py`, `patentes.py`. Las implementaciones
canónicas siguen ahí; `formato` solo agrega un punto de entrada.

## Dependencias

Ninguna. Stdlib pura. La localización de Argentina (separadores `.` y `,`,
nombres de meses en español) se hardcodea en español — el paquete entero
asume Argentina, no necesita `locale` ni `babel`.

## Core o extra

**Core.** Sin dependencias externas, complementario a los módulos existentes.

## Tests necesarios

- `telefono` con varios estilos devuelve el formato correcto.
- `telefono` con número inválido → `None`.
- `pesos`: separador miles `.`, coma decimal, símbolo `$ ` con espacio.
- `pesos` con `0` decimales no muestra coma.
- `codigo_postal`: distingue CP4 y CPA, CPA en mayúsculas.
- `fecha` en estilo corto vs largo.
- `fecha` con nombres de meses en español (enero..diciembre, sin tildes en
  los outputs si el `locale` no está disponible).
- Para cada reexport: `formato.dni(x) == personas.formatear_dni(x)` para una
  muestra de inputs.
- Sin internet, sin archivos externos.

## Riesgos

- **Solapamiento con módulos existentes.** Si alguien edita
  `personas.formatear_dni` sin actualizar el reexport, ambos quedarían
  desincronizados. Mitigación: el reexport llama a la función original (no
  la copia), así no hay desincronización posible.
- **Convención de nombres dispar.** Hoy hay `patentes.formatear` (sin
  sufijo) y `personas.formatear_dni` (con sufijo). Esta propuesta no
  resuelve eso (no toca código existente), pero el módulo `formato` ofrece
  un nombre estándar (`arg.formato.patente`, `arg.formato.dni`). En una
  futura iteración mayor podría considerarse alinear las APIs originales —
  decisión separada.
- **Sobre-ingeniería.** El módulo es relativamente fino. Riesgo: que se
  vuelva un "cajón de sastre". Mitigación: alcance acotado a *formateo de
  salida*, no parsing ni validación (esas viven en los `limpiar_*` /
  `validar_*` de cada módulo).

## Prioridad

**Alta.** Transversal: toca todos los módulos donde ya hay datos validables.
Costo bajo, valor inmediato: hoy un usuario tiene que aprender 4 módulos
distintos para encontrar todas las funciones de formateo. Después de esta
propuesta, todas son descubribles desde un único punto.

## Contexto adicional

- Originado en `ROADMAP.md → Próximas ideas → formato` + observación de la
  auditoría: el repo ya tiene `formatear_*` dispersos sin un agrupador.
- Sin scraping, sin internet, sin deps — encaja en la filosofía del
  `AGENT_CONTEXT.md`.
- Sigue las convenciones API ya establecidas (`limpiar_*`, `validar_*`,
  `normalizar_*`, `formatear_*`, `lookup`, `listar`).
- Convención `import argentina as arg` respetada en todos los ejemplos.
