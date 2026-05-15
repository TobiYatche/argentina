# argentina

Einfache Werkzeuge für die Arbeit mit administrativen und geografischen Daten Argentiniens.

Wenn du mit argentinischen Datenbanken arbeitest, tauchen früher oder später DNIs mit Punkten, auf fünf verschiedene Arten geschriebene Provinzen, CBUs, CUITs, inkonsistente Adressen oder seltsame Postleitzahlen auf. Dieses Paket versucht, dir genau diese Dinge abzunehmen, ohne dir den Vormittag zu ruinieren.

## Installation

```bash
pip install argentina
```

Optionale Extras:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

Siehe [Optionale Extras](../../extras.md) für die vollständige Tabelle (`maps`, `feriados`, `georef`, `elecciones`, usw.).

## Empfohlener Import

```python
import argentina as arg
```

Die Dokumentation und die Beispiele verwenden `import argentina as arg`, weil das Snippets kurz und konsistent hält. Wenn du ein Snippet von irgendwo im Projekt kopierst, funktioniert es genau so.

Es ist auch gültig, einzelne Module zu importieren, wenn du nur eines brauchst:

```python
from argentina import provincias
import argentina.economia as economia
```

## Schnelle Verwendung

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## Schlanker Kern

Das Basispaket versucht, schlank zu bleiben. `import argentina` startet in ~70 ms und importiert **nicht** automatisch:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

Schwerere Funktionalitäten werden als **optionale Extras** installiert, und ihre Abhängigkeiten werden verzögert importiert — nur wenn du die Funktion aufrufst, die sie braucht.

## Hauptmodule

| Modul | Beschreibung |
|---|---|
| `provincias` | Lookup und Metadaten der Provinzen |
| `departamentos` | Lookup und Metadaten der Bezirke |
| `ciudades` | Städte aus dem Censo 2022 |
| `personas` | DNI, CUIT/CUIL und Namen |
| `postal` | CP4 und CPA Postleitzahlen |
| `bancos` | CBU, CVU und Alias |
| `afip` | offizielle AFIP-Tabellen (Monotributo, MwSt., Einkommensteuer) |
| `clae` | AFIP-Wirtschaftstätigkeiten |
| `fechas` | Parsing argentinischer Daten |
| `feriados` | offizielle Feiertage (optional, via API) |
| `telefonos` | argentinische Telefonnummern |
| `direcciones` | einfacher Adressparser |
| `formato` | kanonische Ausgabeformatierung |
| `montos` | Parsing monetärer Strings |
| `indices` | IPC, UVA, CER, ICL (offline) |
| `educacion` | CUE und Bildungskategorien |
| `salud` | grundlegende Gesundheitsnormalisierung |
| `identificar` | Universal-Inspektor |
| `matching` | Fuzzy-Matching |
| `geo` | optionale geografische Werkzeuge |
| `economia` | optionale Wirtschaftsreihen |
| `data` | optionale öffentliche Datensätze (EPH, Census) |

Mehr Details in [docs/modulos/](../../modulos/).

## Philosophie

- **Schlanker Kern** — `import argentina` lädt weder pandas noch sonst Schweres.
- **Modular** — jedes Modul löst eine Domäne und ist separat nutzbar.
- **Eingebettete Daten für Kleines, On-Demand-Downloads für Großes** — Provinzen und Bezirke sind enthalten; IGN-Shapes und EPH werden beim ersten Aufruf heruntergeladen und in `~/.cache/argentina/` zwischengespeichert.
- **Explizit darüber, was approximativ ist** — Fuzzy-Matches, syntaktische Validierungen und Teildaten werden als solche dokumentiert.
- **Kein Scraping, keine persönlichen Daten** — nur offizielle öffentliche APIs (INDEC, IGN, BCRA, Georef, datos.gob.ar).

> Ziel ist es nicht, pandas oder geopandas neu zu erfinden. Ziel ist es, häufige argentinische Probleme mit einer einfachen, konsistenten API zu lösen.

Mehr Details in [docs/filosofia.md](../../filosofia.md).

## Dokumentation

Die vollständige Dokumentation enthält Beispiele pro Modul, Schritt-für-Schritt-Notebooks, Einschränkungen, optionale Extras und eine API-Referenz.

- **Web (mkdocs):** `https://TU_USUARIO.github.io/argentina/` *(Platzhalter — GitHub Pages noch nicht veröffentlicht).*
- **Lokal:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  Öffne `http://127.0.0.1:8000`.

Empfohlene Lektüre je nach Bedarf:

| Wenn du willst… | Geh zu |
|---|---|
| Executive Summary | diese `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| Vollständige Modulreferenz | [`docs/`](../../) |
| Interaktive Schritt-für-Schritt-Tutorials | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| Minimale Copy-Paste-Snippets | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| Katalog der Wirtschaftsreihen | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## Status

- **Version:** 0.3.0 (Beta).
- **Python:** 3.9+.
- **Quellen:** INDEC (Censo 2022, EPH, Wirtschaftsreihen), IGN (Kartografie und Argenmap), BCRA, datos.gob.ar (Georef), argentinadatos.com (Feiertage).
- **Tests:** 550 automatisierte Tests (alle bestehen am 2026-05-13).
- **Gedacht für:** Forschung, Datenanalyse, Beratung, öffentlicher Sektor und private Projekte, die argentinische Verwaltungsdaten verarbeiten.

## Lizenz

MIT — siehe [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE).
