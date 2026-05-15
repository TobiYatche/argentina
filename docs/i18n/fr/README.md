# argentina

Utilitaires simples pour travailler avec les données administratives et géographiques de l'Argentine.

Si vous travaillez avec des bases argentines, tôt ou tard apparaissent des DNI avec des points, des provinces écrites de cinq façons différentes, des CBU, des CUIT, des adresses incohérentes ou des codes postaux étranges. Ce package essaie de résoudre ces choses sans vous faire perdre la matinée.

## Installation

```bash
pip install argentina
```

Extras optionnels :

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

Voir [Extras optionnels](../../extras.md) pour le tableau complet (`maps`, `feriados`, `georef`, `elecciones`, etc.).

## Import recommandé

```python
import argentina as arg
```

La documentation et les exemples utilisent `import argentina as arg` parce que cela garde les snippets courts et cohérents. Si vous copiez un snippet depuis n'importe où dans le projet, il fonctionne tel quel.

Il est également valide d'importer des modules spécifiques quand vous n'en avez besoin que d'un :

```python
from argentina import provincias
import argentina.economia as economia
```

## Utilisation rapide

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## Noyau léger

Le package de base essaie de rester léger. `import argentina` démarre en ~70 ms et **n'**importe **pas** automatiquement :

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

Les fonctionnalités plus lourdes s'installent comme **extras optionnels** et leurs dépendances sont importées de manière différée, uniquement lorsque vous appelez la fonction qui en a besoin.

## Modules principaux

| Module | Description |
|---|---|
| `provincias` | lookup et métadonnées des provinces |
| `departamentos` | lookup et métadonnées des départements |
| `ciudades` | villes du Recensement 2022 |
| `personas` | DNI, CUIT/CUIL et noms |
| `postal` | CP4 et CPA |
| `bancos` | CBU, CVU et alias |
| `afip` | tableaux officiels AFIP (Monotributo, TVA, Impôts) |
| `clae` | activités économiques AFIP |
| `fechas` | parsing de dates argentines |
| `feriados` | jours fériés officiels (optionnel, via API) |
| `telefonos` | numéros de téléphone argentins |
| `direcciones` | parser d'adresses basique |
| `formato` | formatage canonique de sortie |
| `montos` | parsing de chaînes monétaires |
| `indices` | IPC, UVA, CER, ICL hors-ligne |
| `educacion` | CUE et catégories éducatives |
| `salud` | normalisation basique de santé |
| `identificar` | inspecteur universel |
| `matching` | matching flou |
| `geo` | outils géographiques optionnels |
| `economia` | séries économiques optionnelles |
| `data` | datasets publics optionnels (EPH, Recensement) |

Plus de détails dans [docs/modulos/](../../modulos/).

## Philosophie

- **Noyau léger** — `import argentina` ne charge pas pandas ni rien de lourd.
- **Modulaire** — chaque module résout un domaine et peut être utilisé séparément.
- **Données embarquées pour le petit, téléchargement à la demande pour le grand** — provinces et départements sont à l'intérieur ; shapes IGN et EPH se téléchargent et se cachent dans `~/.cache/argentina/` la première fois.
- **Explicite sur ce qui est approximatif** — les matches flous, les validations syntaxiques et les données partielles sont documentés comme tels.
- **Pas de scraping, pas de données personnelles** — uniquement des APIs publiques officielles (INDEC, IGN, BCRA, Georef, datos.gob.ar).

> L'objectif n'est pas de réinventer pandas ni geopandas. L'objectif est de résoudre des problèmes argentins fréquents avec une API simple et cohérente.

Plus de détails dans [docs/filosofia.md](../../filosofia.md).

## Documentation

La documentation complète inclut des exemples par module, des notebooks pas à pas, des limitations, des extras optionnels et une référence d'API.

- **Web (mkdocs) :** `https://TU_USUARIO.github.io/argentina/` *(placeholder — GitHub Pages pas encore publié).*
- **Local :**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  Ouvre `http://127.0.0.1:8000`.

Lecture suggérée selon le besoin :

| Si vous voulez… | Allez à |
|---|---|
| Résumé exécutif | ce `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| Référence complète par module | [`docs/`](../../) |
| Tutoriels interactifs pas à pas | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| Snippets minimaux copy-paste | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| Catalogue des séries économiques | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## Statut

- **Version :** 0.3.0 (Beta).
- **Python :** 3.9+.
- **Sources :** INDEC (Censo 2022, EPH, séries économiques), IGN (cartographie et Argenmap), BCRA, datos.gob.ar (Georef), argentinadatos.com (jours fériés).
- **Tests :** 550 tests automatisés (tous passent au 2026-05-13).
- **Conçu pour :** recherche, analyse de données, conseil, secteur public et projets privés qui touchent à des données administratives argentines.

## Licence

MIT — voir [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE).
