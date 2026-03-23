# CLAUDE.md — 토정비결 프로젝트

## 프로젝트 개요

Python + FastAPI로 구현한 웹 기반 토정비결 운세 서비스.

- **언어:** Python 3
- **의존성:** `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `korean-lunar-calendar`
- **실행:** `python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`
- **접속:** `http://localhost:8000`

---

## 폴더 구조

```
tojeong/                         # 프로젝트 루트
├── main.py                      # FastAPI 앱 진입점
├── requirements.txt             # 의존성
├── CLAUDE.md                    # 프로젝트 문서
├── app/                         # 백엔드 패키지
│   ├── __init__.py
│   ├── lunar.py                 # 양력→음력 변환
│   ├── calculator.py            # 상·중·하괘 계산 엔진
│   └── data/
│       ├── generate_fortunes.py # 운세 DB 생성 스크립트
│       └── fortunes.json        # 144괘 운세 텍스트 DB
├── templates/
│   ├── index.html               # 생년월일 입력 폼
│   └── result.html              # 운세 결과 페이지
└── static/
    └── style.css                # 전통 한지 스타일 CSS
```

---

## 아키텍처

```
브라우저 (HTML Form)
    ↓ POST /result
main.py (FastAPI)
    ↓
app/calculator.py  ← app/lunar.py
    ↓
app/data/fortunes.json
    ↓
templates/result.html (Jinja2)
    ↓
브라우저 (운세 결과)
```

---

## 핵심 모듈

### `app/lunar.py`

양력 날짜를 음력으로 변환하는 모듈.

| 함수 | 역할 |
|------|------|
| `solar_to_lunar(year, month, day)` | `korean-lunar-calendar` 라이브러리로 음력 변환 |
| `get_korean_age(birth_year, target_year)` | 한국식 나이(세수) 계산: `target - birth + 1` |

### `app/calculator.py`

토정비결 괘를 계산하는 엔진.

**괘 계산 공식:**

```
상괘(1-8): (세수 + 음력 생월) % 8  — 나머지 0이면 8
중괘(1-6): 음력 생월 % 6           — 나머지 0이면 6
하괘(1-3): 음력 생일 % 3           — 나머지 0이면 3
```

**주요 함수:**

| 함수 | 역할 |
|------|------|
| `calculate_gwe(birth_solar_year, birth_solar_month, birth_solar_day, target_year)` | 양력 생년월일 + 대상 연도 → 상·중·하괘 및 괘 키 반환 |

**반환값 구조:**
```python
{
    "sang": int,       # 상괘 (1-8)
    "jung": int,       # 중괘 (1-6)
    "ha":   int,       # 하괘 (1-3)
    "key":  str,       # ex) "3-2-1"
    "lunar": dict,     # 음력 생년월일 + 윤달 여부
    "age":  int,       # 세수
    "sang_name": str,  # ex) "건(乾)"
    "jung_name": str,  # ex) "이(二)"
    "ha_name":   str,  # ex) "초(初)"
}
```

### `app/data/fortunes.json`

144가지 괘(`1-1-1` ~ `8-6-3`)에 대한 운세 텍스트 DB.

**구조:**
```json
{
  "3-2-1": {
    "key":          "3-2-1",
    "grade":        "중길(中吉)",
    "verse":        "일월광명(日月光明)",
    "year_fortune": "【중길(中吉)】 꾸준한 노력이...",
    "months": [
      {"month": "1월", "text": "..."},
      ...
    ]
  }
}
```

**등급 체계:**

| 상괘 | 등급 | 괘사 |
|------|------|------|
| 1 | 대길(大吉) | 천지개태(天地開泰) |
| 2 | 길(吉)     | 화목상생(和木相生) |
| 3 | 중길(中吉) | 일월광명(日月光明) |
| 4 | 평(平)     | 춘풍화기(春風和氣) |
| 5 | 평(平)     | 구름속달(雲中明月) |
| 6 | 중흉(中凶) | 풍전등화(風前燈火) |
| 7 | 흉(凶)     | 험산준령(險山峻嶺) |
| 8 | 대흉(大凶) | 고진감래(苦盡甘來) |

운세 DB 재생성: `python3 app/data/generate_fortunes.py`

---

## API 엔드포인트

| 메서드 | 경로 | 역할 |
|--------|------|------|
| `GET`  | `/`       | 생년월일 입력 폼 |
| `POST` | `/result` | 운세 결과 페이지 |

**POST `/result` 파라미터:**

| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `birth_year`  | int | 양력 출생 연도 |
| `birth_month` | int | 양력 출생 월 |
| `birth_day`   | int | 양력 출생 일 |
| `target_year` | int | 운세 보기 연도 |
| `gender`      | str | 성별 (남/여, 선택) |
| `name`        | str | 이름 (선택) |

---

## 렌더링 흐름

1. `index.html` — 생년월일 입력 폼 (Jinja2 템플릿)
2. `POST /result` → `calculate_gwe()` → `fortunes.json` 조회
3. `result.html` — 연간 운세 + 12개월 월별 운세 카드 표시

---

## UI 디자인

- **테마:** 전통 한지(韓紙) 스타일
- **색상 팔레트:** 금색(`#b8860b`), 한지 배경(`#fdf6e3`), 먹 글씨(`#2c1a0e`)
- **폰트:** Noto Serif KR (Google Fonts)
- **등급별 색상:** 대길(빨강) → 흉(회색) → 대흉(다크)
- **반응형:** 모바일 520px 이하 대응

---

## 개발 노트

- 테스트 파일 없음 — `curl` 또는 브라우저로 수동 검증
- 운세 DB는 `generate_fortunes.py` 스크립트로 재생성 가능
- 음력 변환 범위: `korean-lunar-calendar` 지원 범위 (1900~2050년대)
- 윤달 출생자는 평달로 처리됨
- `restart()`가 없는 stateless 구조 — 요청마다 새로 계산
