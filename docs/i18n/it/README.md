# argentina

Utilità semplici per lavorare con dati amministrativi e geografici dell'Argentina.

Se lavori con basi dati argentine, prima o poi compaiono DNI con i punti, province scritte in cinque modi diversi, CBU, CUIT, indirizzi incoerenti o codici postali strani. Questo pacchetto cerca di risolvere queste cose senza farti perdere la mattinata.

## Installazione

```bash
pip install argentina
```

Extra opzionali:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

Vedi [Extra opzionali](../../extras.md) per la tabella completa (`maps`, `feriados`, `georef`, `elecciones`, ecc.).

## Import consigliato

```python
import argentina as arg
```

La documentazione e gli esempi usano `import argentina as arg` perché mantiene gli snippet brevi e coerenti. Se copi uno snippet da qualunque parte del progetto, funziona così com'è.

È valido anche importare moduli specifici quando ne serve solo uno:

```python
from argentina import provincias
import argentina.economia as economia
```

## Uso rapido

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## Nucleo leggero

Il pacchetto base cerca di rimanere leggero. `import argentina` parte in ~70 ms e **non** importa automaticamente:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

Le funzionalità più pesanti si installano come **extra opzionali** e le loro dipendenze vengono importate in modo differito, solo quando chiami la funzione che le richiede.

## Moduli principali

| Modulo | Descrizione |
|---|---|
| `provincias` | lookup e metadata delle province |
| `departamentos` | lookup e metadata dei dipartimenti |
| `ciudades` | città dal Censo 2022 |
| `personas` | DNI, CUIT/CUIL e nomi |
| `postal` | CP4 e CPA |
| `bancos` | CBU, CVU e alias |
| `afip` | tabelle ufficiali AFIP (Monotributo, IVA, Imposte) |
| `clae` | attività economiche AFIP |
| `fechas` | parsing di date argentine |
| `feriados` | festività ufficiali (opzionale, via API) |
| `telefonos` | telefoni argentini |
| `direcciones` | parser di indirizzi base |
| `formato` | formattazione canonica di output |
| `montos` | parsing di stringhe monetarie |
| `indices` | IPC, UVA, CER, ICL offline |
| `educacion` | CUE e categorie educative |
| `salud` | normalizzazione base di salute |
| `identificar` | ispettore universale |
| `matching` | matching fuzzy |
| `geo` | strumenti geografici opzionali |
| `economia` | serie economiche opzionali |
| `data` | dataset pubblici opzionali (EPH, Censo) |

Maggiori dettagli in [docs/modulos/](../../modulos/).

## Filosofia

- **Nucleo leggero** — `import argentina` non carica pandas né nulla di pesante.
- **Modulare** — ogni modulo risolve un dominio e può essere usato separatamente.
- **Dati embeddati per il piccolo, download on-demand per il grande** — province e dipartimenti sono dentro; shape IGN ed EPH si scaricano e vengono memorizzati in cache in `~/.cache/argentina/` la prima volta.
- **Esplicito su ciò che è approssimato** — match fuzzy, validazioni sintattiche e dati parziali sono documentati come tali.
- **Niente scraping, niente dati personali** — solo API pubbliche ufficiali (INDEC, IGN, BCRA, Georef, datos.gob.ar).

> L'obiettivo non è reinventare pandas né geopandas. L'obiettivo è risolvere problemi argentini frequenti con un'API semplice e coerente.

Maggiori dettagli in [docs/filosofia.md](../../filosofia.md).

## Documentazione

La documentazione completa include esempi per modulo, notebook passo passo, limitazioni, extra opzionali e riferimento API.

- **Web (mkdocs):** `https://TU_USUARIO.github.io/argentina/` *(placeholder — GitHub Pages non ancora pubblicato).*
- **Locale:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  Apri `http://127.0.0.1:8000`.

Lettura suggerita in base al bisogno:

| Se vuoi… | Vai a |
|---|---|
| Riepilogo esecutivo | questo `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| Riferimento completo per modulo | [`docs/`](../../) |
| Tutorial interattivi passo passo | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| Snippet minimi copy-paste | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| Catalogo delle serie economiche | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## Stato

- **Versione:** 0.3.0 (Beta).
- **Python:** 3.9+.
- **Fonti:** INDEC (Censo 2022, EPH, serie economiche), IGN (cartografia e Argenmap), BCRA, datos.gob.ar (Georef), argentinadatos.com (festività).
- **Test:** 550 test automatizzati (tutti passano al 2026-05-13).
- **Pensato per:** ricerca, analisi di dati, consulenza, settore pubblico e progetti privati che toccano dati amministrativi argentini.

## Licenza

MIT — vedi [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE).
