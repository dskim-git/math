# MathLab 프로젝트 Copilot 규칙

## 프로젝트 개요

- **앱**: Streamlit 기반 수학 학습 앱 (배포: https://mathematicslab.streamlit.app/)
- **언어**: Python, 일부 HTML/JS (Streamlit components)
- **인증**: 로그인 시스템 (`auth_utils.py`), 세션 상태 키 `_user_type` / `_user_id` / `_user_name`

---

## 미니활동 파일 규칙 (가장 중요)

### 위치
- 공통수학 활동: `activities/common/mini/` 폴더
- 확률과통계 활동: `activities/probability_new/mini/` 폴더

### 필수 패턴 (반드시 모든 활동 파일에 포함)

```python
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]   # 공통수학
# 확률과통계라면:
# _GAS_URL = st.secrets["gas_url_probability_new"]

_SHEET_NAME = "시트명(활동이름_영문또는한글)"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 이 활동과 관련된 ...**"},
    {"key": "문제1",      "label": "문제 1",    "type": "text_area",  "height": 70},
    {"key": "답1",        "label": "정답 1",    "type": "text_input"},
    # ... 활동 특성에 맞는 추가 질문 ...
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]
```

### render() 함수 끝에 반드시 포함

```python
def render():
    # ... 활동 본문 ...

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
```

### META 딕셔너리 (units 등록용)

```python
META = {
    "title":       "활동 제목",
    "description": "활동 한 줄 설명",
    "order":       99,   # _units.py 에서의 순서
}
```

### _questions 작성 가이드
- 마지막 두 질문은 항상 `새롭게알게된점` / `느낀점`으로 고정
- 그 앞에 활동 고유 질문 추가 (문제만들기, 비교분석, 적용사례 등)
- `type`은 `"text_input"` (단답형) 또는 `"text_area"` (서술형) 또는 `"markdown"` (안내문구)

---

## 기존 파일 참고 (패턴 확인용)

- `activities/common/mini/poly_add_sub_game.py` — 기본 게임형 활동
- `activities/common/mini/gelosia_mul.py` — 시각적 알고리즘형 활동
- `activities/probability_new/mini/rep_perm_dice.py` — 확통 활동

---

## 시각 처리 규칙 (매우 중요)

- **모든 시각은 한국 시간(KST, UTC+9) 기준**으로 기록한다.
- `datetime.now()` 대신 반드시 `datetime.now(_KST)` 또는 `datetime.now(KST)`를 사용한다.
- 파일 내 KST 정의가 없으면 다음을 추가한다:
  ```python
  from datetime import timezone, timedelta
  _KST = timezone(timedelta(hours=9))
  ```
- `reflection_utils.py`의 `_KST`가 글로벌 선언되어 있으므로, 미니 활동 파일에서는 별도 선언 불필요.

---

## Google Sheets 연동

> **⚠️ 스프레드시트 구분 (매우 중요)**
> - `st.secrets["spreadsheet_id"]` → **수업 진도표·방문기록·성찰 요약 로그** 전용 (`13dDQ4...`). 서비스 계정 접근 가능.
> - `st.secrets["reflection_spreadsheet_common"]` → **공통수학 성찰 실제 데이터** 전용 (`1HESVcl...`). GAS(`gas_url_common`)가 여기에 쓴다. 스크립트로 헤더/시트를 만들 때도 이 ID를 사용할 것.
> - `st.secrets["reflection_spreadsheet_probability_new"]` → **확률과통계 성찰 실제 데이터** 전용 (`1GXT4sYZ...`). GAS(`gas_url_probability_new`)가 여기에 쓴다. 스크립트로 헤더/시트를 만들 때도 이 ID를 사용할 것.
> - 세 스프레드시트를 절대 혼용하지 말 것. 특히 성찰 활동 관련 스크립트에서 `spreadsheet_id`를 쓰면 **잘못된 시트**에 데이터가 들어간다.

- **GAS URL (공통수학)**: `activities/common/mini/` 내 기존 파일의 `_GAS_URL` 참고
- **GAS URL (확률과통계)**: `activities/probability_new/mini/` 내 기존 파일의 `_GAS_URL` 참고
- `render_reflection_form` 호출 시 제출 성공하면 자동으로 `spreadsheet_id` 시트의 "성찰기록" 탭에도 요약 로그가 남음

### 새 활동 만들 때 헤더 설정 (스크립트 실행 방법)
- **공통수학**: `secrets["reflection_spreadsheet_common"]` → `1HESVclXf1iBlKLHLYgj00eQkLfmOTb9tw763NEkjOgA`
- **확률과통계**: `secrets["reflection_spreadsheet_probability_new"]` → `1GXT4sYZfsrJZUadiCYQ8l2Yfl265G0P8bkVM6vc60PA`
- 헤더 형식: `['timestamp', '학번', '이름', <활동 고유 질문 키...>, '새롭게알게된점', '느낀점']`
  - 답란이 있는 경우: `['timestamp', '학번', '이름', '문제1', '답1', '문제2', '답2', '새롭게알게된점', '느낀점']`
  - 서술형만인 경우: `['timestamp', '학번', '이름', '문제1', '문제2', '새롭게알게된점', '느낀점']`

---

## 사용자 권한

- `_user_type`: `"admin"` / `"student"` / `"general"`
- 성찰 폼은 `render_reflection_form`이 자동으로 권한 분기 처리 (일반인 제외, 미로그인 경고)
- 별도 권한 체크 코드 불필요
