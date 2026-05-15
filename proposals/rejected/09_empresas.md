# Propuesta: empresas

> ## 🚫 RECHAZADA — sin fuente oficial estable + CUITs no verificables
>
> **Motivo:** el universo "cotizantes BYMA + estatales + descentralizadas"
> cambia (altas/bajas trimestrales en CNV/BYMA; reestructuraciones del
> sector público). El bloqueante mayor: **la asociación CUIT ↔ empresa
> no se puede sintetizar**. Sin un padrón oficial bajado, embeber
> CUITs sintéticos (aunque cumplan el dígito verificador) es directamente
> falso — el CUIT pertenece a OTRA entidad.
>
> Hubo un intento previo (2026-05-13) con CUITs generados y
> denominaciones reales (YPFD → YPF S.A. con CUIT inventado). Se sacó
> porque la asociación es falsa, no solo aproximada. Ver
> `reports/2026-05-13_correccion_honesta.md`.
>
> **Para reactivar:** bajar padrón oficial de CNV (cotizantes) + lista
> JGM (estatales nacionales) + nomenclador AFIP (descentralizadas).
> Validar licencia de cada fuente. Definir cadencia de update
> trimestral. Solo después mover a `pending/`.
>
> **Política recordatoria:** `AGENT_CONTEXT.md` dice "no datos
> personales". Scope del módulo, si se reactiva, debe limitarse a
> entidades cuyos datos son inequívocamente públicos por obligación
> regulatoria. NO ampliar a padrón AFIP completo ni a monotributistas.

## Problema

`ROADMAP.md → Próximas ideas` lista `empresas`. Pero "empresas" es un
término amplio y peligroso: implementado mal, choca de frente con la
política del proyecto registrada en `AGENT_CONTEXT.md`:
**"no datos personales"**. Un padrón completo de razones sociales
incluye monotributistas (personas físicas con CUIT), pymes con
dirección/teléfono, etc. — eso son datos personales.

Esta propuesta acota deliberadamente el scope a **entidades públicas y
cotizantes**, donde los datos son inequívocamente públicos por
obligación regulatoria:

- Empresas que cotizan en BYMA / CNV (~100 emisores activos).
- Empresas públicas / estatales nacionales (lista YPF, ARSAT, AySA,
  Aerolíneas, etc. — ~50 entidades).
- Organismos descentralizados con CUIT propio (INTA, CONICET, INDEC,
  ANMAT — ~150 entidades).

NO incluye:
- Padrón AFIP completo de contribuyentes.
- Datos de monotributistas.
- Empresas privadas no cotizantes.
- Datos de contacto, direcciones, teléfonos.

Hoy no hay forma en el paquete de:
- Validar que un CUIT pertenece a una entidad cotizante o pública.
- Saber el ticker BYMA de una empresa.
- Listar empresas estatales nacionales con su CUIT.

## Benchmark / paquete de referencia

- `yfinance` (Python) — toma tickers, pero el universo es global, no
  argentino. No tiene el filtro "qué cotiza en BYMA".
- `argentina.universidades` muestra el patrón "registro oficial de
  entidades públicas con CUIT, embebido como CSV". `empresas` lo replica
  para BYMA + estatales + descentralizadas.
- `argentina.bancos` también marca el patrón: usa el padrón BCRA
  embebido. Mismo enfoque para `empresas`: solo padrones oficiales
  cerrados, no scraping.

## Traducción a Argentina

Un módulo `argentina.empresas` con tres catálogos cerrados:
- **Cotizantes** (CNV/BYMA): ticker, denominación, CUIT, sector.
- **Estatales**: denominación, CUIT, ámbito (nacional / provincial),
  jurisdicción.
- **Descentralizadas**: denominación, CUIT, dependencia (ministerio que
  la rige).

Sin padrón completo de empresas privadas. Sin direcciones. Sin
teléfonos. Sin scraping. Sin internet.

## API propuesta

```python
import argentina as arg

# Lookup por CUIT en cualquiera de los tres catálogos
arg.empresas.lookup("30-50000567-7")
# Empresa(cuit='30500005677', denominacion='YPF S.A.',
#         tipo='cotizante', ticker='YPFD', ...)

# Lookup por ticker BYMA
arg.empresas.por_ticker("YPFD")
# Empresa(..., tipo='cotizante')

# Listados por tipo
arg.empresas.cotizantes()
# (Empresa(...), Empresa(...), ...)

arg.empresas.estatales(ambito="nacional")
# (Empresa(...), ...)

arg.empresas.descentralizadas()
# (Empresa(...), ...)

# Búsqueda por denominación (substring normalizado)
arg.empresas.buscar("ypf")
# [Empresa(...)]

# Validación
arg.empresas.es_publica("30-50000567-7")  # True
arg.empresas.es_cotizante("30-50000567-7")  # True

arg.empresas.listar()  # tuple[Empresa, ...]  (todo el universo cubierto)
arg.empresas.tipos()   # ('cotizante', 'estatal', 'descentralizada')
```

Reglas:
- `Empresa` es dataclass frozen, con `tipo` como discriminador.
- El CUIT se normaliza al formato canónico de 11 dígitos antes de
  comparar (reusar `personas.limpiar_cuit`).
- `buscar` usa normalización lowercase + NFKD sin tildes.
- Si una entidad aparece en más de un catálogo (ej. cotizante también
  estatal): se decide por reglas explícitas documentadas
  (`cotizante` gana sobre `estatal`, etc.). NO devolver listas
  ambiguas.

## Archivos a modificar

- `src/argentina/empresas.py` — módulo nuevo.
- `src/argentina/data/empresas_cotizantes.csv` — padrón CNV/BYMA.
- `src/argentina/data/empresas_estatales.csv` — empresas estatales
  nacionales (fuente: Decreto / Jefatura de Gabinete).
- `src/argentina/data/empresas_descentralizadas.csv` — organismos
  descentralizados.
- `src/argentina/__init__.py` — agregar `from argentina import empresas`.
- `tests/test_empresas.py` — tests.
- `docs/modulos/empresas.md` — documentación que arranca con sección
  de scope: qué incluye y, explícitamente, qué NO incluye (con la
  política `no datos personales` citada literal).
- `notebooks/empresas_pruebas.ipynb` — notebook obligatorio.
- `mkdocs.yml`, `README.md`.

## Dependencias

Ninguna. CSV + stdlib.

## Core o extra

**Core.** Datos oficiales embebidos, sin scraping ni internet. Scope
acotado para mantener tamaño chico (~300 entidades en total).

## Tests necesarios

- `lookup` por CUIT en cualquiera de los tres catálogos devuelve la
  entidad correcta.
- `lookup` por CUIT con/sin guiones / con espacios funciona (reuso de
  `personas.limpiar_cuit`).
- `por_ticker("YPFD")` devuelve la cotizante correspondiente.
- `por_ticker(...)` con ticker inexistente → `None`.
- `cotizantes()`, `estatales()`, `descentralizadas()` devuelven solo el
  catálogo correspondiente.
- `buscar("ypf")` y `buscar("YPF")` devuelven lo mismo.
- `es_publica` / `es_cotizante` separan correctamente.
- Cada CUIT del catálogo pasa `personas.validar_cuit` (consistencia
  cruzada — la propia base no tiene CUITs malformados).
- Los tickers no se repiten dentro de `empresas_cotizantes.csv`.
- Sin internet, sin archivos externos.

## Riesgos

- **Privacidad.** Es el riesgo central. Mitigación ya integrada al
  scope: solo entidades cuyos datos son inequívocamente públicos por
  obligación regulatoria (cotizantes CNV, estatales, descentralizadas).
  Antes de incluir cualquier dataset nuevo en el módulo, releer la
  política y validar. Si surge la tentación de "agregar también el
  padrón de monotributistas porque está en datos.gob.ar", **no
  hacerlo** sin decisión explícita del usuario.
- **Desactualización del padrón cotizantes.** Empresas entran y salen
  de BYMA. Mitigación: doc con cadencia trimestral de actualización;
  campo `fecha_alta` opcional.
- **Conflicto con `bancos`.** Las entidades financieras están en
  `bancos`. Algunas también son cotizantes (Galicia, Macro, Supervielle,
  BBVA). Mitigación: `empresas.lookup(cuit_banco)` devuelve la entrada
  como `tipo='cotizante'`; `bancos.lookup(cuit_banco)` devuelve la
  entrada como entidad bancaria. Ambas conviven, son vistas distintas
  sobre la misma entidad. Documentar.
- **Scope creep.** Riesgo de que alguien quiera "agregar todas las
  pymes argentinas". Mitigación: el documento `docs/modulos/empresas.md`
  abre con la lista explícita de lo que NO incluye este módulo, y por
  qué.

## Prioridad

**Media.** Útil para análisis de empresas listadas, sector público y
organismos. Pero más nicho que `clae` o `formato` (que tocan flujos
diarios de cualquier usuario del paquete). Implementar después de
resolver `afip` (propuesta 02), `clae` (04) y `formato` (05), que
están más en el camino crítico.

## Contexto adicional

- Originado en `ROADMAP.md → Próximas ideas → empresas` y mencionado
  en `reports/inconsistencies.md` como ítem sin propuesta concreta.
- Política explícita citada de `AGENT_CONTEXT.md`: "no datos
  personales". Este módulo se diseña para respetar esa política, no
  para circunscribirla.
- Convención `import argentina as arg` respetada.
- Antes de implementar, validar que cada uno de los tres datasets
  tiene fuente oficial estable y licencia compatible. Si alguno no la
  tiene, recortar el scope (ej. solo cotizantes).
