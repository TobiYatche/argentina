# argentina

> Disponible también en [10 idiomas](i18n/index.md) (English, Português,
> Français, Italiano, Deutsch, 中文, 日本語, 한국어, Русский, العربية).

`argentina` es un paquete Python con utilidades simples para trabajar con datos
administrativos, geográficos y públicos de Argentina.

El objetivo es resolver tareas repetitivas que aparecen en proyectos de datos
argentinos:

- normalización de provincias y departamentos
- limpieza de DNI, CUIT/CUIL y nombres
- validación de códigos postales argentinos
- limpieza de teléfonos y direcciones
- identificadores bancarios como CBU
- códigos frecuentes de AFIP
- fechas argentinas
- herramientas geográficas opcionales
- módulos pesados opcionales para economía y datasets públicos

## Ejemplo rápido

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu("2850590940090418135201")
arg.telefonos.normalizar_e164("+54 9 351 1234567")
```

## Núcleo liviano, extras opcionales

`pip install argentina` no descarga `pandas`, `requests`, `geopandas` ni
ninguna otra dependencia pesada. `import argentina` tarda **~70 ms** y usa
**~4 MB** de memoria. Los módulos que necesitan deps externas las importan
solo cuando los usás, y se instalan con extras:

```bash
pip install argentina                    # núcleo liviano
pip install "argentina[economia]"        # + pandas, requests
pip install "argentina[geo,maps]"        # + geopandas, folium, etc.
pip install "argentina[data]"            # + duckdb, pyarrow para EPH/Censo
```

Ver [Extras opcionales](extras.md) para la lista completa.

## ¿Por dónde empiezo?

- **[Instalación](instalacion.md)** — qué instalar según lo que vas a hacer.
- **[Quickstart](quickstart.md)** — ejemplos prácticos en 5 minutos.
- **[Filosofía](filosofia.md)** — por qué el paquete está armado así.
- **[Módulos](modulos/provincias.md)** — referencia por dominio.

## Dónde vive qué

El proyecto separa cuatro capas de documentación, cada una con su rol:

| Capa | Para qué | Dónde |
|---|---|---|
| **README / PyPI** | resumen ejecutivo, instalación, ejemplo rápido | [README](https://github.com/tobiasyatche/argentina#readme) |
| **Docs (esta web)** | referencia completa, filosofía, limitaciones | esta sección |
| **Notebooks** | recorridos interactivos paso a paso | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| **Examples** | scripts mínimos copy-paste por módulo | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |

Si recién llegás, abrí el README. Si querés entender un módulo,
[Módulos](modulos/provincias.md). Si querés un recorrido guiado,
notebooks. Si querés un snippet, examples.

> Cuando esté publicado, la versión web de estos docs vivirá en
> `https://TU_USUARIO.github.io/argentina/` (GitHub Pages). Mientras
> tanto, `mkdocs serve` desde el repo funciona igual.

## Import recomendado

```python
import argentina as arg
```

Convención canónica usada en toda la documentación, los notebooks, los
ejemplos y los docstrings. Vas a ver siempre `arg.` adelante.

## Estado del proyecto

- **Versión actual:** `0.3.0`.
- **Fuentes de datos:** INDEC (Censo 2022, EPH, series económicas), IGN
  (cartografía), BCRA, datos.gob.ar (Georef), argentinadatos.com (feriados).
- **Licencia:** MIT.
- **Python:** 3.9+.
- **Changelog:** ver [CHANGELOG.md](https://github.com/tobiasyatche/argentina/blob/main/CHANGELOG.md).
