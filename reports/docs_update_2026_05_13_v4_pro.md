# Docs update — 2026-05-13 (v4, profesionalización)

Cuarta pasada del agente `docs_agent`. Foco: **mejorar la experiencia de
onboarding** y separar claramente PyPI / docs / notebooks / examples
como capas con roles distintos.

Versión del paquete al momento del reporte: **0.3.0**.

## Pedido del usuario

> "Quiero mejorar y profesionalizar la documentación pública del paquete
> `argentina`. Objetivo: usar PyPI como resumen ejecutivo, usar MkDocs como
> documentación completa, agregar notebooks de ejemplos, mejorar onboarding,
> explicar claramente instalación e imports recomendados, dejar una
> experiencia tipo paquete serio/open source mantenible."

**Nota: el mensaje del usuario quedó truncado** en la sección
"3. INSTALACIÓN ARRIBA DE TODO" — terminaba con un bloque
```bash
pip install argentina
```
sin más detalles. Avancé con la directiva clara (PyPI / docs / notebooks /
examples + import recomendado + onboarding) y dejé esto anotado. Si en la
próxima pasada el usuario completa la sección 3, ajusto.

## Decisiones tomadas

### 1. Onboarding "Empezá acá" arriba de todo

El README hoy empieza con:

1. Título.
2. Bloque de banderas multilingüe (heredado de v3).
3. Descripción + frase-gancho (corta).
4. Bloque "Empezá acá" — instalación + import recomendado + 3 líneas que
   prueban que funcionó.

Eso es lo que ve un usuario nuevo cuando llega al README de PyPI o de
GitHub. Si lee solo esas 20 líneas, ya entiende qué es el paquete, cómo
se instala y cómo se importa.

### 2. Capas separadas con roles explícitos

Agregué una sección **"Dónde vive qué"** en:

- `README.md` — tabla "Si querés X, andá a Y".
- `docs/index.md` — misma tabla pero apuntando a URLs absolutas de
  GitHub para que se renderice bien en mkdocs build/serve.

Las cuatro capas:

| Capa | Rol | Dónde |
|---|---|---|
| PyPI / README | resumen ejecutivo | `README.md` |
| docs/ (mkdocs) | referencia completa | `docs/` |
| notebooks/ | recorridos interactivos | `notebooks/` |
| examples/ | snippets mínimos copy-paste | `examples/` |

La idea: nadie tiene que adivinar dónde buscar.

### 3. Import recomendado destacado

`import argentina as arg` está ahora:

- **Mencionado explícitamente** como "convención canónica" en el README
  (no enterrado en un ejemplo cualquiera).
- **En su propia sección** en `docs/instalacion.md`, explicando que es
  la convención usada en docs, notebooks, examples y docstrings.
- **En su propia sección** en `docs/index.md`.
- **Documentado** en los nuevos `examples/README.md` y `notebooks/README.md`
  como convención obligatoria.

Por qué importa: si copiás un snippet de cualquier capa del proyecto,
funciona tal cual sin que tengas que adivinar cómo se llamó al módulo.

### 4. READMEs para `examples/` y `notebooks/`

Antes no existían. Ahora:

- **`examples/README.md`** — explica que son scripts mínimos
  reproducibles, un módulo por archivo, todos importan con `arg`.
  Incluye tabla `examples/` vs `notebooks/` para que el usuario sepa
  cuál usar.
- **`notebooks/README.md`** — explica los dos formatos que conviven:
  temáticos (`00..05`) para onboarding y `<modulo>_pruebas.ipynb` para
  referencia interactiva. Incluye tabla con todos los notebooks
  temáticos enlazados.

## Cambios concretos

### Archivos nuevos

- `examples/README.md` (62 líneas) — convención, mapa, decisión
  examples vs notebooks.
- `notebooks/README.md` (76 líneas) — convención, listado temáticos,
  diferencia con `_pruebas.ipynb`, decisión.

### Archivos actualizados

- **`README.md`** — reescrita la frase-gancho ("Si trabajás con bases
  argentinas, tarde o temprano aparecen DNIs con puntos…") usando el
  ejemplo de tono correcto del `scripts/docs_agent.md`. Agregado el
  bloque "Empezá acá" con el import canónico destacado. Agregada
  sección "Dónde vive qué".
- **`docs/instalacion.md`** — agregada sección "Import recomendado"
  destacando `import argentina as arg` como convención canónica.
  Refuerzo del smoke test al final del bloque de verificación.
- **`docs/index.md`** — agregada sección "Dónde vive qué" con URLs
  absolutas a GitHub, más sección "Import recomendado".

### Lo que NO se tocó

- Las traducciones `docs/i18n/<lang>/README.md` (v3) — están alineadas
  con el README anterior. Si querés que reflejen el "Empezá acá" nuevo,
  hay que regenerarlas. **Pendiente para próxima pasada** (lo dejo
  anotado).
- `mkdocs.yml`, `docs/api.md` — fueron tocados por el linter; respeto
  el estado actual.
- Las páginas `docs/modulos/*.md`, incluida la nueva `montos.md` (ya
  bien armada por el builder).
- Los notebooks temáticos `00..05` y los `<modulo>_pruebas.ipynb` —
  ya están al día.

## Notas sobre el módulo nuevo `arg.montos`

- Detectado en `src/argentina/montos.py` (`Monto`, `parsear`,
  `parsear_decimal`, `parsear_estricto`, `parsear_completo`,
  `formato_detectado`, `moneda_detectada`).
- Ya está en el README (tabla "Núcleo liviano"), `docs/api.md` (bloque
  mkdocstrings), `mkdocs.yml` (`nav` → Módulos) y
  `docs/modulos/montos.md`.
- **Es el inverso de `arg.formato.pesos`** — eso lo aclara la propia
  página de montos. Buena pareja conceptual: `formato` para mostrar,
  `montos` para parsear.

## Hallazgos / pendientes

1. **Traducciones desactualizadas.** Los 10 archivos `docs/i18n/<lang>/README.md`
   se generaron en v3 a partir del README anterior, que ahora cambió
   (nueva frase-gancho, sección "Empezá acá", sección "Dónde vive qué"
   y mención al módulo `montos`). En la próxima pasada de docs agent
   conviene regenerar las 10 traducciones para mantenerlas alineadas.
2. **PyPI tagline.** El `pyproject.toml` tiene una `description` que
   apunta a las features ("provincias, departamentos, ciudades,
   geografía (IGN)…"). Hoy el README abre con una frase distinta más
   orientada al pain point. Convendría alinear la `description` con la
   nueva frase-gancho del README — pero **es edición de pyproject**,
   no de docs, así que queda fuera de scope del docs agent. Lo dejo
   apuntado.
3. **Mensaje del usuario truncado.** La sección "3. INSTALACIÓN ARRIBA
   DE TODO" terminaba con un bloque `pip install argentina` sin más.
   Avancé con lo razonable (instalación + import + onboarding) pero
   puede haber detalle perdido. Si el usuario completa la sección 3,
   reviso y ajusto.
4. **`docs/i18n/index.md`** menciona "el README español es la fuente de
   verdad" — sigue siendo cierto, pero ahora el README cambió, así que
   el versionado conceptual se corrió. Es justo el punto que
   marqué en el hallazgo 1.

## Próxima pasada

- Re-traducir los 10 `docs/i18n/<lang>/README.md` al README español
  actualizado.
- Si el usuario completa la sección 3 del mensaje original, integrar.
- Cuando aparezca un módulo nuevo: ya está formalizado el ciclo
  (página `docs/modulos/`, bloque en `api.md`, entrada en `mkdocs.yml`,
  fila en README, ejemplo `*_basico.py`, notebook `*_pruebas.ipynb`,
  mención en notebook temático si corresponde).
- Sugerencia: agregar un script `scripts/check_docs_sync.py` que
  chequee paridad módulo ↔ docs/notebooks/examples y avise cuando
  falte algo. Fuera de scope del docs agent puro (es tooling), pero
  facilitaría las próximas pasadas.
