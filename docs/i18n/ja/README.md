# argentina

アルゼンチンの行政・地理データを扱うためのシンプルな Python ユーティリティ。

アルゼンチンのデータベースを扱っていると、いずれドット付きの DNI、5 通りに書かれた州名、CBU、CUIT、表記揺れのある住所、奇妙な郵便番号に遭遇します。このパッケージは、そんな繰り返し作業で午前中を潰さないようにすることを目的としています。

## インストール

```bash
pip install argentina
```

オプションの extras:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

完全な一覧は [オプションの extras](../../extras.md) を参照 (`maps`、`feriados`、`georef`、`elecciones` など)。

## 推奨インポート

```python
import argentina as arg
```

ドキュメントとサンプルでは `import argentina as arg` を使っています。スニペットを短く一貫させるためです。プロジェクトのどこからコピーしてもそのまま動きます。

ひとつのモジュールだけ必要なときは個別インポートも有効です:

```python
from argentina import provincias
import argentina.economia as economia
```

## クイック利用

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## 軽量コア

ベースパッケージは軽量を維持しようとしています。`import argentina` は約 70 ms で立ち上がり、以下を**自動的にはインポートしません**:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

より重い機能は**オプションの extras** としてインストールされ、依存ライブラリはそれを必要とする関数を呼ぶときに初めて遅延読み込みされます。

## 主要モジュール

| モジュール | 説明 |
|---|---|
| `provincias` | 州のルックアップとメタデータ |
| `departamentos` | 郡のルックアップとメタデータ |
| `ciudades` | 2022 年センサスの都市 |
| `personas` | DNI、CUIT/CUIL、氏名 |
| `postal` | CP4 と CPA の郵便番号 |
| `bancos` | CBU、CVU、エイリアス |
| `afip` | AFIP 公式表 (Monotributo、IVA、所得税) |
| `clae` | AFIP 経済活動コード |
| `fechas` | アルゼンチン日付パース |
| `feriados` | 公式祝日 (オプション、API 経由) |
| `telefonos` | アルゼンチンの電話 |
| `direcciones` | 基本住所パーサー |
| `formato` | 正準的な出力整形 |
| `montos` | 金額文字列のパース |
| `indices` | IPC、UVA、CER、ICL (オフライン) |
| `educacion` | CUE と教育カテゴリ |
| `salud` | 基本的な保健正規化 |
| `identificar` | ユニバーサルインスペクター |
| `matching` | ファジーマッチング |
| `geo` | オプションの地理ツール |
| `economia` | オプションの経済時系列 |
| `data` | オプションの公開データセット (EPH、センサス) |

詳細は [docs/modulos/](../../modulos/) を参照してください。

## 設計思想

- **軽量コア** ── `import argentina` で pandas のような重いものを読み込みません。
- **モジュール式** ── 各モジュールは 1 領域を解決し、単独で使えます。
- **小さなものは埋め込み、大きなものはオンデマンドダウンロード** ── 州と郡はパッケージ内蔵。IGN シェイプと EPH は初回呼び出し時にダウンロードされ、`~/.cache/argentina/` にキャッシュされます。
- **近似値は明示** ── ファジーマッチ、構文検証、部分的なデータはそのことを明記しています。
- **スクレイピングなし、個人情報なし** ── 利用するのは公式公開 API のみ (INDEC、IGN、BCRA、Georef、datos.gob.ar)。

> 目的は pandas や geopandas を再発明することではありません。アルゼンチン固有のよくある問題を、シンプルで一貫した API で解決することが目的です。

詳細は [docs/filosofia.md](../../filosofia.md) を参照してください。

## ドキュメント

完全なドキュメントには、モジュールごとのサンプル、ステップバイステップのノートブック、制限事項、オプション extras、API リファレンスが含まれます。

- **Web (mkdocs):** `https://TU_USUARIO.github.io/argentina/` *(プレースホルダー ── GitHub Pages はまだ公開していません)。*
- **ローカル:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  `http://127.0.0.1:8000` を開きます。

目的別おすすめ:

| やりたいこと | 見るところ |
|---|---|
| エグゼクティブ・サマリー | この `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| モジュール完全リファレンス | [`docs/`](../../) |
| ステップバイステップの対話的チュートリアル | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| 最小限のコピペスニペット | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| 経済時系列カタログ | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## ステータス

- **バージョン:** 0.3.0 (Beta)。
- **Python:** 3.9 以上。
- **データソース:** INDEC (Censo 2022、EPH、経済時系列)、IGN (地図と Argenmap)、BCRA、datos.gob.ar (Georef)、argentinadatos.com (祝日)。
- **テスト:** 自動テスト 550 件 (2026-05-13 時点で全件パス)。
- **想定用途:** 研究、データ分析、コンサルティング、公共部門、およびアルゼンチンの行政データを扱う民間プロジェクト。

## ライセンス

MIT ── [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE) を参照。
