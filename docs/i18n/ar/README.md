# argentina

<div dir="rtl">

أدوات بايثون بسيطة للتعامل مع البيانات الإدارية والجغرافية للأرجنتين.

إن كنت تعمل على قواعد بيانات أرجنتينية، فعاجلاً أم آجلاً ستظهر أرقام DNI مع نقاط، وأسماء مقاطعات مكتوبة بخمس طرق مختلفة، وأرقام CBU و CUIT، وعناوين غير متناسقة، ورموز بريدية غريبة. تهدف هذه الحزمة إلى حل ذلك دون أن تضيع عليك ساعات الصباح.

## التثبيت

```bash
pip install argentina
```

Extras اختيارية:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

انظر [Extras اختيارية](../../extras.md) للجدول الكامل (`maps`، `feriados`، `georef`، `elecciones`، إلخ).

## الاستيراد الموصى به

```python
import argentina as arg
```

التوثيق والأمثلة تستخدم `import argentina as arg` لأن ذلك يحافظ على المقاطع البرمجية قصيرة ومتسقة. إذا نسخت مقطعاً من أي مكان في المشروع، فإنه يعمل كما هو.

كما يمكن استيراد وحدات بعينها عندما تحتاج واحدة فقط:

```python
from argentina import provincias
import argentina.economia as economia
```

## استخدام سريع

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## نواة خفيفة

تحاول الحزمة الأساسية البقاء خفيفة. الأمر `import argentina` ينطلق في حوالي 70 مللي ثانية، و**لا** يستورد تلقائياً:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

تُثبَّت الميزات الأثقل عبر **extras اختيارية**، وتُستورد اعتمادياتها بشكل مؤجل، فقط حين تستدعي الدالة التي تحتاجها.

## الوحدات الرئيسية

| الوحدة | الوصف |
|---|---|
| `provincias` | بحث وبيانات وصفية للمقاطعات |
| `departamentos` | بحث وبيانات وصفية للأقسام |
| `ciudades` | مدن إحصاء 2022 |
| `personas` | DNI و CUIT/CUIL والأسماء |
| `postal` | الرموز البريدية CP4 و CPA |
| `bancos` | CBU و CVU والأسماء المستعارة |
| `afip` | جداول AFIP الرسمية (Monotributo، ضريبة، أرباح) |
| `clae` | أنشطة AFIP الاقتصادية |
| `fechas` | تحليل التواريخ الأرجنتينية |
| `feriados` | العطلات الرسمية (اختياري، عبر API) |
| `telefonos` | الهواتف الأرجنتينية |
| `direcciones` | محلل عناوين أساسي |
| `formato` | تنسيق المخرجات القياسي |
| `montos` | تحليل نصوص المبالغ |
| `indices` | IPC و UVA و CER و ICL (دون اتصال) |
| `educacion` | CUE وفئات التعليم |
| `salud` | تطبيع صحي أساسي |
| `identificar` | مفتش شامل |
| `matching` | مطابقة ضبابية |
| `geo` | أدوات جغرافية اختيارية |
| `economia` | سلاسل اقتصادية اختيارية |
| `data` | مجموعات بيانات عامة اختيارية (EPH، الإحصاء) |

تفاصيل أكثر في [docs/modulos/](../../modulos/).

## الفلسفة

- **نواة خفيفة** — `import argentina` لا يحمّل pandas ولا أي شيء ثقيل.
- **مُجزَّأة** — كل وحدة تحل مجالاً واحداً ويمكن استخدامها منفصلة.
- **بيانات مدمجة للصغير، تنزيل عند الطلب للكبير** — المقاطعات والأقسام مدمجة؛ أشكال IGN و EPH تُنزَّل وتُخزَّن في `~/.cache/argentina/` في الاستدعاء الأول.
- **صريح بشأن ما هو تقريبي** — المطابقات الضبابية، التحقق الإملائي، والبيانات الجزئية مُوثَّقة كذلك.
- **بدون scraping ولا بيانات شخصية** — فقط واجهات برمجية عامة رسمية (INDEC، IGN، BCRA، Georef، datos.gob.ar).

> الهدف ليس إعادة اختراع pandas أو geopandas. الهدف هو حل المشكلات الأرجنتينية الشائعة عبر واجهة برمجة بسيطة ومتسقة.

تفاصيل أكثر في [docs/filosofia.md](../../filosofia.md).

## التوثيق

يشمل التوثيق الكامل أمثلة لكل وحدة، ودفاتر Jupyter خطوة بخطوة، والقيود، و extras الاختيارية، ومرجع API.

- **ويب (mkdocs):** `https://TU_USUARIO.github.io/argentina/` *(عنصر نائب — GitHub Pages لم يُنشَر بعد).*
- **محلياً:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  افتح `http://127.0.0.1:8000`.

قراءات مقترحة حسب الحاجة:

| إذا كنت تريد… | اذهب إلى |
|---|---|
| ملخص تنفيذي | هذا `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| مرجع كامل لكل وحدة | [`docs/`](../../) |
| شروحات تفاعلية خطوة بخطوة | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| مقتطفات نسخ-لصق دنيا | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| فهرس السلاسل الاقتصادية | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## الحالة

- **الإصدار:** 0.3.0 (Beta).
- **Python:** 3.9 فأعلى.
- **المصادر:** INDEC (Censo 2022، EPH، السلاسل الاقتصادية)، IGN (الخرائط و Argenmap)، BCRA، datos.gob.ar (Georef)، argentinadatos.com (العطلات).
- **الاختبارات:** 550 اختباراً آلياً (جميعها تجتاز بتاريخ 2026-05-13).
- **الجمهور المستهدف:** البحث، تحليل البيانات، الاستشارات، القطاع العام، والمشاريع الخاصة التي تتعامل مع بيانات إدارية أرجنتينية.

## الترخيص

MIT — انظر [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE).

</div>
