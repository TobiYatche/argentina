# argentina

Utilitários simples para trabalhar com dados administrativos e geográficos da Argentina.

Se você trabalha com bases argentinas, cedo ou tarde aparecem DNIs com pontos, províncias escritas de cinco formas diferentes, CBUs, CUITs, endereços inconsistentes ou códigos postais estranhos. Este pacote tenta resolver isso sem te fazer perder a manhã.

## Instalação

```bash
pip install argentina
```

Extras opcionais:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

Veja [Extras opcionais](../../extras.md) para a tabela completa (`maps`, `feriados`, `georef`, `elecciones`, etc.).

## Import recomendado

```python
import argentina as arg
```

A documentação e os exemplos usam `import argentina as arg` porque mantém os snippets curtos e consistentes. Se você copiar um trecho de qualquer parte do projeto, funciona tal qual.

Também é válido importar módulos específicos quando você só precisa de um:

```python
from argentina import provincias
import argentina.economia as economia
```

## Uso rápido

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## Núcleo leve

O pacote base tenta se manter leve. `import argentina` carrega em ~70 ms e **não** importa automaticamente:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

As funcionalidades mais pesadas se instalam como **extras opcionais** e suas dependências são importadas de forma diferida, somente quando você chama a função que precisa delas.

## Módulos principais

| Módulo | Descrição |
|---|---|
| `provincias` | lookup e metadata de províncias |
| `departamentos` | lookup e metadata de departamentos |
| `ciudades` | cidades do Censo 2022 |
| `personas` | DNI, CUIT/CUIL e nomes |
| `postal` | CP4 e CPA |
| `bancos` | CBU, CVU e alias |
| `afip` | tabelas oficiais AFIP (Monotributo, IVA, Ganhos) |
| `clae` | atividades econômicas AFIP |
| `fechas` | parsing de datas argentinas |
| `feriados` | feriados oficiais (opcional, via API) |
| `telefonos` | telefones argentinos |
| `direcciones` | parser básico de endereços |
| `formato` | formatação canônica de saída |
| `montos` | parsing de strings monetárias |
| `indices` | IPC, UVA, CER, ICL offline |
| `educacion` | CUE e categorias educacionais |
| `salud` | normalização básica de saúde |
| `identificar` | inspetor universal |
| `matching` | matching difuso |
| `geo` | ferramentas geográficas opcionais |
| `economia` | séries econômicas opcionais |
| `data` | datasets públicos opcionais (EPH, Censo) |

Mais detalhe em [docs/modulos/](../../modulos/).

## Filosofia

- **Núcleo leve** — `import argentina` não carrega pandas nem nada pesado.
- **Modular** — cada módulo resolve um domínio e pode ser usado separadamente.
- **Dados embutidos para o pequeno, download sob demanda para o grande** — províncias e departamentos vêm dentro; shapes do IGN e EPH baixam e cacheiam em `~/.cache/argentina/` na primeira vez.
- **Explícito sobre o que é aproximado** — matches difusos, validações sintáticas e dados parciais são documentados como tais.
- **Sem scraping nem dados pessoais** — apenas APIs públicas oficiais (INDEC, IGN, BCRA, Georef, datos.gob.ar).

> O objetivo não é reinventar pandas nem geopandas. O objetivo é resolver problemas argentinos frequentes com uma API simples e consistente.

Mais detalhe em [docs/filosofia.md](../../filosofia.md).

## Documentação

A documentação completa inclui exemplos por módulo, notebooks passo a passo, limitações, extras opcionais e API reference.

- **Web (mkdocs):** `https://TU_USUARIO.github.io/argentina/` *(placeholder — GitHub Pages ainda não publicado).*
- **Local:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  Abre `http://127.0.0.1:8000`.

Leitura sugerida conforme a necessidade:

| Se você quer… | Vá para |
|---|---|
| Resumo executivo | este `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| Referência completa por módulo | [`docs/`](../../) |
| Tutoriais interativos passo a passo | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| Snippets mínimos copy-paste | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| Catálogo de séries econômicas | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## Status

- **Versão:** 0.3.0 (Beta).
- **Python:** 3.9+.
- **Fontes:** INDEC (Censo 2022, EPH, séries econômicas), IGN (cartografia e Argenmap), BCRA, datos.gob.ar (Georef), argentinadatos.com (feriados).
- **Testes:** 550 testes automatizados (todos passando em 2026-05-13).
- **Pensado para:** pesquisa, análise de dados, consultoria, setor público e projetos privados que lidam com dados administrativos argentinos.

## Licença

MIT — ver [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE).
