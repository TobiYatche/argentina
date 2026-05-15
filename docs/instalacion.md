# Instalación

## Requisitos

- Python **3.9 o superior**
- `pip` reciente (cualquiera ≥ 22 anda bien)

## Instalación básica

```bash
pip install argentina
```

Esto instala el **núcleo liviano**: provincias, departamentos, ciudades,
DNI/CUIT, códigos postales, teléfonos, fechas, bancos, parser de
direcciones, etc. Sin `pandas`, `requests` ni nada pesado.

## Import recomendado

```python
import argentina as arg
```

El alias `arg` es la **convención canónica** del paquete. Está usado así
en toda la documentación, los notebooks (`notebooks/`), los ejemplos
(`examples/`) y los docstrings. Si copiás un snippet de cualquier lado,
va a funcionar tal cual con este import.

Verificá la instalación:

```python
import argentina as arg

print(arg.__version__)               # versión instalada
print(arg.provincias.CORDOBA)         # smoke test del core
```

Si el `print` muestra un objeto `Provincia(...)` con nombre, código
INDEC, capital y población, está todo en orden.

## Instalación con extras

Cada módulo que necesita dependencias externas las pide solo cuando lo
usás. Para que estén disponibles, instalá el extra correspondiente:

| Quiero usar... | Comando |
|---|---|
| Series económicas (IPC, EMAE, BCRA) | `pip install "argentina[economia]"` |
| Geometrías del IGN (provincias/departamentos como `GeoDataFrame`) | `pip install "argentina[geo]"` |
| Mapas Folium con Argenmap | `pip install "argentina[maps]"` |
| Geocoding con Georef | `pip install "argentina[georef]"` |
| Feriados oficiales | `pip install "argentina[feriados]"` |
| Datos electorales | `pip install "argentina[elecciones]"` |
| EPH (microdatos INDEC) y Censo 2022 | `pip install "argentina[data]"` |

Podés combinar varios:

```bash
pip install "argentina[economia,geo,maps,data]"
```

## Instalación para desarrollo

Si vas a contribuir o correr los tests:

```bash
git clone https://github.com/tobiasyatche/argentina.git
cd argentina
pip install -e ".[dev]"

pytest                          # correr la suite
mkdocs serve                    # ver esta documentación localmente
```

El extra `[dev]` incluye `pytest`, `ruff`, `build`, `twine`, `mkdocs`,
`mkdocs-material` y `mkdocstrings`.

## Servir la documentación localmente

```bash
mkdocs serve
```

Abre [http://127.0.0.1:8000](http://127.0.0.1:8000) en el navegador.
Los cambios en `docs/` se recargan automáticamente.

Para generar la versión estática:

```bash
mkdocs build           # → site/
```
