# argentina

아르헨티나의 행정·지리 데이터를 다루기 위한 간단한 Python 유틸리티 모음.

아르헨티나 데이터베이스를 다루다 보면 결국 점이 있는 DNI, 다섯 가지로 적힌 주 이름, CBU, CUIT, 들쭉날쭉한 주소, 이상한 우편번호와 마주치게 됩니다. 이 패키지는 그런 반복 작업으로 오전을 통째로 날리지 않게 해 주는 것을 목표로 합니다.

## 설치

```bash
pip install argentina
```

선택적 extras:

```bash
pip install "argentina[geo]"
pip install "argentina[economia]"
pip install "argentina[data]"
```

전체 목록은 [선택적 extras](../../extras.md)를 참고하세요 (`maps`, `feriados`, `georef`, `elecciones` 등).

## 권장 임포트

```python
import argentina as arg
```

문서와 예제는 `import argentina as arg`을 사용합니다. 스니펫을 짧고 일관되게 유지하기 때문입니다. 프로젝트 어디서든 스니펫을 복사하면 그대로 동작합니다.

특정 모듈 하나만 필요하면 개별 임포트도 유효합니다:

```python
from argentina import provincias
import argentina.economia as economia
```

## 빠른 사용

```python
import argentina as arg

arg.provincias.lookup("PBA")
arg.personas.limpiar_dni("12.345.678")
arg.postal.validar_cpa("C1425ABC")
arg.bancos.validar_cbu(
    "2850590940090418135201"
)
```

## 가벼운 코어

기본 패키지는 가볍게 유지하려고 합니다. `import argentina`은 약 70 ms에 시작되며, 다음을 **자동으로 임포트하지 않습니다**:

- `pandas`
- `geopandas`
- `requests`
- `duckdb`
- `pyarrow`
- `folium`

더 무거운 기능은 **선택적 extras**로 설치되며, 의존성은 해당 함수를 호출할 때에만 지연 임포트됩니다.

## 주요 모듈

| 모듈 | 설명 |
|---|---|
| `provincias` | 주의 lookup과 메타데이터 |
| `departamentos` | 군의 lookup과 메타데이터 |
| `ciudades` | 2022년 인구조사 기준 도시 |
| `personas` | DNI, CUIT/CUIL, 이름 |
| `postal` | CP4와 CPA 우편번호 |
| `bancos` | CBU, CVU, 별칭 |
| `afip` | AFIP 공식 표 (Monotributo, IVA, 소득세) |
| `clae` | AFIP 업종 코드 |
| `fechas` | 아르헨티나 날짜 파싱 |
| `feriados` | 공식 공휴일 (선택, API 호출) |
| `telefonos` | 아르헨티나 전화번호 |
| `direcciones` | 기본 주소 파서 |
| `formato` | 표준 출력 형식화 |
| `montos` | 금액 문자열 파싱 |
| `indices` | IPC, UVA, CER, ICL (오프라인) |
| `educacion` | CUE와 교육 카테고리 |
| `salud` | 기본 보건 표준화 |
| `identificar` | 범용 인스펙터 |
| `matching` | 퍼지 매칭 |
| `geo` | 선택적 지리 도구 |
| `economia` | 선택적 경제 시계열 |
| `data` | 선택적 공공 데이터셋 (EPH, 인구조사) |

자세한 내용은 [docs/modulos/](../../modulos/) 참조.

## 철학

- **가벼운 코어** — `import argentina`은 pandas나 무거운 것을 로드하지 않습니다.
- **모듈식** — 모듈마다 한 영역을 해결하며 독립적으로 사용 가능합니다.
- **작은 데이터는 내장, 큰 데이터는 온디맨드 다운로드** — 주와 군은 내장. IGN shapes와 EPH는 최초 호출 시 다운로드되어 `~/.cache/argentina/`에 캐시됩니다.
- **근사값은 명시** — 퍼지 매칭, 구문 검증, 부분 데이터는 그렇다는 사실을 명시합니다.
- **스크래핑 없음, 개인정보 없음** — 공식 공개 API만 사용 (INDEC, IGN, BCRA, Georef, datos.gob.ar).

> 목표는 pandas나 geopandas를 다시 만드는 것이 아닙니다. 아르헨티나에서 흔히 마주치는 문제를 단순하고 일관된 API로 해결하는 것이 목표입니다.

자세한 내용은 [docs/filosofia.md](../../filosofia.md) 참조.

## 문서

전체 문서에는 모듈별 예제, 단계별 노트북, 한계, 선택적 extras, API 레퍼런스가 포함됩니다.

- **웹 (mkdocs):** `https://TU_USUARIO.github.io/argentina/` *(자리표시자 — GitHub Pages 아직 미공개)*.
- **로컬:**

  ```bash
  pip install -e ".[dev]"
  mkdocs serve
  ```

  `http://127.0.0.1:8000`을 엽니다.

용도별 추천:

| 원하는 것 | 이동 위치 |
|---|---|
| 요약 | 이 `README.md` / [PyPI](https://pypi.org/project/argentina/) |
| 모듈별 전체 레퍼런스 | [`docs/`](../../) |
| 단계별 인터랙티브 튜토리얼 | [`notebooks/`](https://github.com/tobiasyatche/argentina/tree/main/notebooks) |
| 최소 복사-붙여넣기 스니펫 | [`examples/`](https://github.com/tobiasyatche/argentina/tree/main/examples) |
| 경제 시계열 카탈로그 | [`SERIES_DISPONIBLES.md`](https://github.com/tobiasyatche/argentina/blob/main/SERIES_DISPONIBLES.md) |

## 상태

- **버전:** 0.3.0 (Beta).
- **Python:** 3.9 이상.
- **출처:** INDEC (Censo 2022, EPH, 경제 시계열), IGN (지도와 Argenmap), BCRA, datos.gob.ar (Georef), argentinadatos.com (공휴일).
- **테스트:** 550개 자동화 테스트 (2026-05-13 기준 전부 통과).
- **대상:** 연구, 데이터 분석, 컨설팅, 공공 부문 및 아르헨티나의 행정 데이터를 다루는 민간 프로젝트.

## 라이선스

MIT — [LICENSE](https://github.com/tobiasyatche/argentina/blob/main/LICENSE) 참조.
