# argentina

用于处理阿根廷行政与地理数据的简易 Python 工具。

如果你处理阿根廷的数据库，迟早会遇到带点的 DNI、写成五种不同形式的省名、CBU、CUIT、不一致的地址或奇怪的邮政编码。本包旨在帮你解决这些问题，而不让你浪费一个上午。

## 安装

```bash
pip install argentina
```

可选 extras:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

完整列表见 [可选 extras](../../extras.md)（`maps`、`feriados`、`georef`、`elecciones` 等）。

## 推荐导入

```python
import argentina as arg
```

文档和示例都使用 `import argentina as arg`，因为这样能保持代码片段简短而一致。从项目任何地方复制片段都能直接运行。

如果只需要一个模块，也可以直接导入：

```python
from argentina import provincias
import argentina.economia as economia
```

## 快速使用

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## 轻量核心

基础包尽量保持轻量。`import argentina` 启动约 70 毫秒，并**不**会自动导入以下：

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

更重的功能通过**可选 extras** 安装，相关依赖以延迟方式导入，只有在调用相应函数时才会加载。

## 主要模块

| 模块 | 说明 |
|---|---|
| `provincias` | 省的 lookup 与元数据 |
| `departamentos` | 区的 lookup 与元数据 |
| `ciudades` | Censo 2022 的城市 |
| `personas` | DNI、CUIT/CUIL 与姓名 |
| `postal` | CP4 与 CPA 邮编 |
| `bancos` | CBU、CVU 与别名 |
| `afip` | AFIP 官方表（Monotributo、IVA、所得税） |
| `clae` | AFIP 行业代码 |
| `fechas` | 阿根廷日期解析 |
| `feriados` | 官方节假日（可选，API 调用） |
| `telefonos` | 阿根廷电话 |
| `direcciones` | 基础地址解析器 |
| `formato` | 规范化输出格式 |
| `montos` | 金额字符串解析 |
| `indices` | IPC、UVA、CER、ICL（离线） |
| `educacion` | CUE 与教育分类 |
| `salud` | 基本卫生标准化 |
| `identificar` | 通用识别器 |
| `matching` | 模糊匹配 |
| `geo` | 可选地理工具 |
| `economia` | 可选经济序列 |
| `data` | 可选公共数据集（EPH、Census） |

更多细节见 [docs/modulos/](../../modulos/)。

## 设计理念

- **轻量核心** —— `import argentina` 不会加载 pandas 或任何重型库。
- **模块化** —— 每个模块解决一个领域，可独立使用。
- **小数据内嵌，大数据按需下载** —— 省和区已内嵌；IGN shapes 与 EPH 在首次调用时下载并缓存在 `~/.cache/argentina/`。
- **对近似值保持明示** —— 模糊匹配、语法校验和部分数据都会明确说明。
- **不抓取，不收集个人数据** —— 仅使用官方公共 API（INDEC、IGN、BCRA、Georef、datos.gob.ar）。

> 目标不是重新发明 pandas 或 geopandas。目标是用简单一致的 API 解决阿根廷常见的问题。

更多细节见 [docs/filosofia.md](../../filosofia.md)。

## 文档

完整文档包括按模块的示例、逐步运行的 notebooks、限制、可选 extras 与 API 参考。

- **Web (mkdocs)：** `https://TU_USUARIO.github.io/argentina/` *(占位符 —— GitHub Pages 尚未发布)。*
- **本地：**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  打开 `http://127.0.0.1:8000`。

按需求推荐阅读：

| 如果你想…… | 前往 |
|---|---|
| 执行摘要 | 本 `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| 完整的按模块参考 | [`docs/`](../../) |
| 逐步交互式教程 | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| 最小可复制粘贴片段 | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| 经济序列目录 | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## 状态

- **版本：** 0.3.0（Beta）。
- **Python：** 3.9+。
- **数据来源：** INDEC（Censo 2022、EPH、经济序列）、IGN（制图与 Argenmap）、BCRA、datos.gob.ar（Georef）、argentinadatos.com（节假日）。
- **测试：** 550 个自动化测试（截至 2026-05-13 全部通过）。
- **适用于：** 研究、数据分析、咨询、公共部门以及处理阿根廷行政数据的私人项目。

## 许可证

MIT —— 详见 [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE)。
