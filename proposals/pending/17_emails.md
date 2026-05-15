# Propuesta: emails

## Problema

En cualquier base de contactos argentina aparece el mismo problema con
emails: errores de tipeo, mayúsculas/minúsculas inconsistentes,
espacios sobrantes, dominios mal escritos, y la pregunta recurrente:

- `"  Juan.Perez@GMAIL.COM "` → cómo limpiarlo.
- `"juan@hotmial.com"` → ¿typo de hotmail?
- `"administracion@empresa.com.ar"` → ¿es un dominio argentino?
- `"contacto@argentina.gob.ar"` → ¿es un dominio público (gob)?
- `"contacto@uba.edu.ar"` → ¿es un dominio académico?

Hoy el paquete no tiene nada para emails. Es un gap obvio en
limpieza de datos generales.

Lo que hace distinto a Argentina vs un validador genérico de email:
- TLDs argentinos: `.com.ar`, `.com.ar`, `.gob.ar`, `.gov.ar`,
  `.edu.ar`, `.org.ar`, `.net.ar`, `.tur.ar`, `.int.ar`, `.mil.ar`,
  `.musica.ar` (segundo nivel argentino administrado por NIC.AR).
- Saber distinguir email "argentino" (TLD `.ar`) de "no argentino"
  importa para reporting de bases mixtas.

## Benchmark / paquete de referencia

- [`email-validator`](https://pypi.org/project/email-validator/) —
  validación estándar de emails, sintaxis + dominio. Inspiración del
  API.
- [`python-stdnum`](https://pypi.org/project/python-stdnum/) — patrón
  `validate()`/`compact()`/`format()` por código.
- [`DataPrep.clean_email`](https://docs.dataprep.ai/) — limpieza por
  lote con sugerencia de typos comunes.
- `argentina.clean.normalizar_texto` ya marca el patrón "limpieza
  transversal sin dataset". Este módulo lo replica para emails.

## Traducción a Argentina

Un módulo `argentina.emails` con:
- Validación sintáctica (regex RFC simplificado pero correcto).
- Limpieza canónica (lowercase domain, trim, sin tildes en local).
- Detección de TLD argentino y clasificación de tipo
  (`comercial`, `gobierno`, `educativo`, `organizacion`, `red`,
  `turismo`, `militar`, ...).
- Corrección de typos comunes de dominios (catálogo cerrado de los
  más frecuentes: `gmial → gmail`, `hotmial → hotmail`,
  `yhaoo → yahoo`, etc. — lista corta y estable).
- Extracción de partes (local, dominio, TLD).

## API propuesta

```python
import argentina as arg

# Limpieza canónica
arg.emails.limpiar("  Juan.Perez@GMAIL.COM ")
# 'juan.perez@gmail.com'

arg.emails.limpiar("invalido")
# None  (no parece email)

# Validación sintáctica
arg.emails.validar("juan@empresa.com.ar")  # True
arg.emails.validar("juan@empresa")          # False (sin TLD)
arg.emails.validar("@empresa.com")          # False
arg.emails.validar(None)                    # False

# Extracción de partes
arg.emails.parsear("juan@empresa.com.ar")
# Email(local='juan', dominio='empresa.com.ar', tld='com.ar')

arg.emails.dominio("juan@gmail.com")
# 'gmail.com'

arg.emails.tld("juan@empresa.com.ar")
# 'com.ar'

# Detección argentino
arg.emails.es_argentino("juan@empresa.com.ar")  # True
arg.emails.es_argentino("juan@gmail.com")        # False

# Tipo de dominio argentino
arg.emails.tipo("contacto@argentina.gob.ar")
# 'gobierno'

arg.emails.tipo("contacto@uba.edu.ar")
# 'educativo'

arg.emails.tipo("juan@empresa.com.ar")
# 'comercial'

arg.emails.tipo("juan@gmail.com")
# None  (no argentino)

# Corrección de typos comunes (catálogo cerrado)
arg.emails.sugerir_correccion("juan@hotmial.com")
# 'juan@hotmail.com'

arg.emails.sugerir_correccion("juan@gmail.com")
# None  (ya está bien)

# Constantes públicas (la lista de TLDs .ar es cerrada y estable)
arg.emails.TLDS_ARGENTINOS
# {'com.ar', 'gob.ar', 'gov.ar', 'edu.ar', 'org.ar', 'net.ar',
#  'tur.ar', 'int.ar', 'mil.ar', 'musica.ar', 'ar'}
```

Reglas:
- `limpiar` devuelve email canónico (`lower()` en dominio, trim,
  preserva case en local cuando es relevante — por default lowercase
  todo). Si no parece email, `None`.
- `validar` es sintáctico (regex), no chequea MX ni DNS. Para
  validación con DNS, escribir en doc "no es scope del módulo, usar
  `email-validator` aparte si hace falta".
- `Email` es dataclass frozen con `local`, `dominio`, `tld`.
- `tld` reconoce TLDs argentinos de segundo nivel (`com.ar` vs solo
  `ar`).
- `sugerir_correccion` usa catálogo cerrado de typos frecuentes (~30
  entradas). NO usa fuzzy genérico — eso es trabajo de `matching` si
  se quisiera generalizar.

## Archivos a modificar

- `src/argentina/emails.py` — módulo nuevo.
- `src/argentina/__init__.py` — agregar `from argentina import emails`.
- `tests/test_emails.py` — tests.
- `docs/modulos/emails.md` — documentación con tabla de TLDs `.ar` y
  catálogo de typos.
- `notebooks/emails_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. Stdlib pura (`re`).

## Core o extra

**Core.** Cero dataset que envejezca. Los TLDs de segundo nivel `.ar`
los administra NIC.AR y son **estables** (la última incorporación
fue `.musica.ar` hace varios años; cambios son raros y se agregan
con propuesta explícita, no con cron). El catálogo de typos
frecuentes es cerrado y conocido.

## Tests necesarios

- `limpiar` con espacios, mayúsculas, formas comunes → forma
  canónica.
- `limpiar` con basura → `None`.
- `validar` para emails válidos / inválidos / nulos.
- `parsear` devuelve `Email` con partes correctas para TLD simple
  (`.com`) y compuesto (`.com.ar`).
- `dominio`, `tld`, `local` consistentes con `parsear`.
- `es_argentino` para muestra representativa (cada TLD `.ar` da
  `True`; muestras `.com`/`.io`/`.es` dan `False`).
- `tipo` para cada categoría de TLD argentino.
- `tipo` para email no argentino → `None`.
- `sugerir_correccion`: typos del catálogo → versión corregida; sin
  typo → `None`.
- Email malformado a `sugerir_correccion` → `None` (no inventar).
- Constante `TLDS_ARGENTINOS` contiene todos los TLDs documentados.
- Sin internet, sin archivos externos, sin DNS lookup.

## Riesgos

- **TLDs nuevos.** NIC.AR podría sumar un TLD `.ar` nuevo. Mitigación:
  cambios históricamente raros (la lista se mueve ~1 vez por década);
  cuando pase, agregar al catálogo. NO es deuda que crece sola.
- **Validación sintáctica vs MX.** Un email puede ser sintácticamente
  válido y no existir. **Decisión:** validar es sintáctico por scope
  explícito. El doc lo deja claro y sugiere `email-validator` con DNS
  para quien lo necesite.
- **Catálogo de typos.** Mantenerlo corto y conservador. NO incluir
  typos genéricos (`gnail`, `gmaiI` con i mayúscula) que aplicarían a
  todos los dominios — solo los específicos de dominios populares
  argentinos/globales.
- **Privacidad.** Los emails son datos personales. **Decisión:** el
  módulo opera sobre strings, no almacena nada, no consulta nada
  online, no scrapea. Compatible con `AGENT_CONTEXT.md → no datos
  personales`. Mencionarlo en la doc.

## Prioridad

**Alta.** Hay un gap obvio (sin módulo de emails en el paquete) que
aparece en cualquier base de contactos. Implementación de baja
superficie con valor inmediato. Cero deuda — la lista de TLDs `.ar`
es estable, el catálogo de typos es cerrado.

## Contexto adicional

- Originada por feedback del usuario (2026-05-13): "limpieza de
  datos más general".
- Benchmark inspiracional: `email-validator`, `DataPrep.clean_email`,
  `python-stdnum` para el patrón `validar`/`limpiar`/`parsear`.
- Patrón consolidado: módulo transversal sin dataset, encaja con
  `clean`/`formato`/`matching`/`montos` (14)/`razones_sociales` (13).
- Convención `import argentina as arg` respetada.
