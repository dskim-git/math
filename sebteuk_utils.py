# sebteuk_utils.py
"""
세특(과목별 세부능력 및 특기사항) 자동 작성 — 데이터 계층.

성찰 기록 구글 시트(공통수학·확률과통계)에서 학생들이 제출한 답변을 읽어
학번별로 집계하고, AI 입력용 '익명 프로필 텍스트'를 만든다.

설계 메모
---------
- 데이터 소스는 두 개의 성찰 기록 스프레드시트뿐이다.
    공통수학  : st.secrets["reflection_spreadsheet_common"]
    확률과통계: st.secrets["reflection_spreadsheet_probability_new"]
  (회원 DB·진도표용 spreadsheet_id 와 절대 혼용하지 않는다.)
- 각 활동은 탭(워크시트) 하나이며, 헤더는
    [timestamp, 학번, 이름, <활동별 질문 키...>, 새롭게알게된점, 느낀점] 형태다.
- 탭을 하나씩 읽으면 Google 읽기 분당 한도(60회)를 금세 초과한다.
  → worksheets()(메타데이터 1회) + values_batch_get()(전 탭 1회)로 ~2회만 호출한다.
- 일부 탭은 이름 컬럼이 '  이름'처럼 공백이 섞여 있어 헤더는 항상 strip 후 비교한다.
- '익명화': AI로 보내는 프로필 텍스트에는 학번·이름을 절대 넣지 않는다(답변 내용만).
  학번 → 결과 매핑은 호출부가 학번 단위로 처리하므로 자동·정확하게 복원된다.
"""
from __future__ import annotations

import streamlit as st

# ── 과목 정의 (auth_utils 키와 동일) ──────────────────────────────────────────
SUBJECTS: dict[str, dict] = {
    "common": {
        "label": "공통수학",
        "secret": "reflection_spreadsheet_common",
    },
    "probability_new": {
        "label": "확률과통계",
        "secret": "reflection_spreadsheet_probability_new",
    },
}

# 완성된 세특을 저장하는 탭 이름 (각 과목 성찰 스프레드시트 안에 생성)
_RECORD_SHEET = "세특기록"
_RECORD_HEADER = ["저장시각", "학번", "이름", "세특"]

# 답변이 아닌 메타 컬럼(집계 시 제외) — strip·정규화된 이름 기준
_META_COLS = {"timestamp", "제출시각", "저장시각", "타임스탬프", "학번", "이름", "성명"}


def _norm(v) -> str:
    return str(v).strip()


def _get_sheet_id(subject_key: str) -> str:
    cfg = SUBJECTS.get(subject_key)
    if not cfg:
        return ""
    try:
        return str(st.secrets.get(cfg["secret"], "") or "")
    except Exception:
        return ""


def subject_label(subject_key: str) -> str:
    return SUBJECTS.get(subject_key, {}).get("label", subject_key)


# ── 시트 로드 + 학번별 집계 ────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def load_subject_reflections(subject_key: str, _bust: int = 0) -> dict:
    """과목 성찰 시트의 모든 활동 탭을 읽어 학번별로 집계한다.

    반환::

        {
          "ok": bool,
          "error": str,                 # ok=False 일 때 사유
          "activities": [               # 활동(탭) 요약 — 표시용
            {"title": str, "n_rows": int, "n_students": int}, ...
          ],
          "students": {
            "<학번>": {
              "이름": str,
              "submissions": [
                {"활동": str, "제출시각": str, "답변": {질문키: 답변, ...}}, ...
              ],
            }, ...
          },
        }

    @st.cache_data 로 5분 캐시한다. _bust 값을 바꾸면 강제 새로고침된다.
    """
    sheet_id = _get_sheet_id(subject_key)
    if not sheet_id:
        return {"ok": False, "error": f"`{SUBJECTS.get(subject_key, {}).get('secret', subject_key)}` secret이 비어 있습니다.",
                "activities": [], "students": {}}

    try:
        from auth_utils import _get_gspread_client
        client = _get_gspread_client()
    except Exception as e:
        return {"ok": False, "error": f"구글 클라이언트 초기화 실패: {e}", "activities": [], "students": {}}
    if client is None:
        return {"ok": False, "error": "구글 서비스 계정 연결에 실패했습니다(secrets 확인).",
                "activities": [], "students": {}}

    try:
        sh = client.open_by_key(sheet_id)
        titles = [ws.title for ws in sh.worksheets()]          # 메타데이터 1회
        if not titles:
            return {"ok": True, "error": "", "activities": [], "students": {}}
        # 시트명에 작은따옴표가 있으면 '' 로 이스케이프
        ranges = ["'" + t.replace("'", "''") + "'" for t in titles]
        batch = sh.values_batch_get(ranges)                    # 전 탭 1회
        value_ranges = batch.get("valueRanges", [])
    except Exception as e:
        msg = str(e)
        if "429" in msg or "Quota exceeded" in msg or "per minute" in msg:
            return {"ok": False, "error": "구글 시트 읽기 한도(분당)를 초과했습니다. 1분 후 다시 시도해 주세요.",
                    "activities": [], "students": {}}
        return {"ok": False, "error": f"시트 읽기 실패: {e}", "activities": [], "students": {}}

    students: dict[str, dict] = {}
    activities: list[dict] = []

    for idx, title in enumerate(titles):
        if title == _RECORD_SHEET:
            continue  # 완성 세특 저장 탭은 활동(답변)이 아니므로 집계에서 제외
        values = value_ranges[idx].get("values", []) if idx < len(value_ranges) else []
        if not values:
            activities.append({"title": title, "n_rows": 0, "n_students": 0})
            continue

        header = [_norm(h) for h in values[0]]
        rows = values[1:]

        def _find(names: set[str]) -> int:
            for i, h in enumerate(header):
                if h in names:
                    return i
            return -1

        num_i = _find({"학번"})
        name_i = _find({"이름", "성명"})
        answer_idx = [i for i, h in enumerate(header) if h and h not in _META_COLS]

        seen_nums: set[str] = set()
        for r in rows:
            num = _norm(r[num_i]) if (num_i >= 0 and num_i < len(r)) else ""
            if not num:
                continue
            name = _norm(r[name_i]) if (name_i >= 0 and name_i < len(r)) else ""
            ts_i = _find({"timestamp", "제출시각", "타임스탬프"})
            ts = _norm(r[ts_i]) if (ts_i >= 0 and ts_i < len(r)) else ""

            answers: dict[str, str] = {}
            for i in answer_idx:
                if i < len(r):
                    val = _norm(r[i])
                    if val:
                        answers[header[i]] = val
            if not answers:
                continue  # 빈 제출 스킵

            seen_nums.add(num)
            stu = students.setdefault(num, {"이름": name, "submissions": []})
            if name and not stu["이름"]:
                stu["이름"] = name
            stu["submissions"].append({"활동": title, "제출시각": ts, "답변": answers})

        activities.append({"title": title, "n_rows": len(rows), "n_students": len(seen_nums)})

    return {"ok": True, "error": "", "activities": activities, "students": students}


# ── 학생 명단 / 프로필 ─────────────────────────────────────────────────────────
def student_roster(data: dict) -> list[dict]:
    """제출 학생 목록을 학번순으로 반환한다.

    [{"학번": str, "이름": str, "활동수": int, "제출수": int}, ...]
    """
    out: list[dict] = []
    for num, info in data.get("students", {}).items():
        subs = info.get("submissions", [])
        acts = {s["활동"] for s in subs}
        out.append({
            "학번": num,
            "이름": info.get("이름", ""),
            "활동수": len(acts),
            "제출수": len(subs),
        })
    out.sort(key=lambda x: (x["학번"], x["이름"]))
    return out


def student_activities(data: dict, student_num: str) -> list[str]:
    """해당 학생이 답변한 활동명 목록(제출 순서·중복 제거)을 반환한다."""
    info = data.get("students", {}).get(student_num)
    if not info:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for s in info["submissions"]:
        act = s["활동"]
        if act not in seen:
            seen.add(act)
            out.append(act)
    return out


def build_profile_text(data: dict, student_num: str, activities=None) -> str:
    """한 학생의 답변을 활동별로 묶은 '익명' 프로필 텍스트를 만든다.

    학번·이름은 포함하지 않는다(AI 입력 익명화). 활동명 + 질문키 + 답변만.
    activities 가 주어지면 해당 활동(목록/집합)만 포함한다. None 이면 전체.
    """
    info = data.get("students", {}).get(student_num)
    if not info:
        return ""

    allowed = set(activities) if activities is not None else None
    by_act: dict[str, list[dict]] = {}
    for s in info["submissions"]:
        if allowed is not None and s["활동"] not in allowed:
            continue
        by_act.setdefault(s["활동"], []).append(s)

    lines: list[str] = []
    for act, subs in by_act.items():
        lines.append(f"### 활동: {act}")
        for s in subs:
            for key, val in s["답변"].items():
                # 한 줄로 펼쳐 토큰 절약 (개행은 공백으로)
                flat = " ".join(str(val).split())
                lines.append(f"- [{key}] {flat}")
        lines.append("")
    return "\n".join(lines).strip()


# ── NEIS byte 계산 ─────────────────────────────────────────────────────────────
def neis_bytes(text: str, kor_bytes: int = 2) -> int:
    """NEIS식 byte 수를 계산한다.

    ASCII(영문·숫자·공백·기호)는 1 byte, 그 외(한글 등)는 kor_bytes(2 또는 3)로 센다.
    NEIS 환경에 따라 한글을 2byte(EUC-KR 관행) 또는 3byte(UTF-8)로 세므로 선택 가능.
    """
    total = 0
    for ch in text:
        total += 1 if ord(ch) < 0x80 else kor_bytes
    return total


# ── 누적 사용량 로그 (로그 스프레드시트의 '세특사용량' 탭) ─────────────────────
# 잔액 조회 API가 없으므로, 생성할 때마다 토큰·예상비용을 직접 누적 기록한다.
_USAGE_SHEET = "세특사용량"
_USAGE_HEADER = ["일시", "모델", "과목", "학생수",
                 "입력토큰", "출력토큰", "캐시쓰기", "캐시읽기", "예상비용USD"]


def _get_usage_ws():
    """로그 스프레드시트(spreadsheet_id)의 '세특사용량' 워크시트를 가져오거나 생성한다."""
    try:
        from auth_utils import _get_gspread_client
        client = _get_gspread_client()
        if client is None:
            return None
        sheet_id = str(st.secrets.get("spreadsheet_id", "") or "")
        if not sheet_id:
            return None
        sh = client.open_by_key(sheet_id)
        try:
            return sh.worksheet(_USAGE_SHEET)
        except Exception:
            ws = sh.add_worksheet(title=_USAGE_SHEET, rows=5000, cols=len(_USAGE_HEADER) + 1)
            ws.append_row(_USAGE_HEADER)
            return ws
    except Exception as e:
        print(f"[sebteuk_utils] usage ws error: {e}")
        return None


def log_usage(model: str, subject_label_str: str, n_students: int,
              usage: dict, cost_usd: float) -> bool:
    """세특 생성 1건(단일=학생1명, 일괄=합산)의 토큰·예상비용을 누적 기록한다.

    실패해도 생성 흐름을 막지 않도록 best-effort 로 처리한다.
    """
    try:
        from datetime import datetime, timezone, timedelta
        ws = _get_usage_ws()
        if ws is None:
            return False
        now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([
            now, model, subject_label_str, int(n_students),
            int(usage.get("input", 0)), int(usage.get("output", 0)),
            int(usage.get("cache_write", 0)), int(usage.get("cache_read", 0)),
            round(float(cost_usd), 6),
        ])
        return True
    except Exception as e:
        print(f"[sebteuk_utils] log_usage error: {e}")
        return False


@st.cache_data(ttl=60, show_spinner=False)
def load_usage_summary(_bust: int = 0) -> dict:
    """'세특사용량' 탭을 합산한 누적 사용량 요약을 반환한다.

    {"events", "students", "input", "output", "cache_write", "cache_read",
     "tokens_total", "cost_usd"}
    """
    base = {"events": 0, "students": 0, "input": 0, "output": 0,
            "cache_write": 0, "cache_read": 0, "tokens_total": 0, "cost_usd": 0.0}
    try:
        ws = _get_usage_ws()
        if ws is None:
            return base
        records = ws.get_all_records(numericise_ignore=["all"])
    except Exception as e:
        print(f"[sebteuk_utils] load_usage_summary error: {e}")
        return base

    def _num(v) -> float:
        try:
            return float(str(v).replace(",", "").strip() or 0)
        except Exception:
            return 0.0

    for r in records:
        base["events"] += 1
        base["students"] += int(_num(r.get("학생수", 0)))
        base["input"] += int(_num(r.get("입력토큰", 0)))
        base["output"] += int(_num(r.get("출력토큰", 0)))
        base["cache_write"] += int(_num(r.get("캐시쓰기", 0)))
        base["cache_read"] += int(_num(r.get("캐시읽기", 0)))
        base["cost_usd"] += _num(r.get("예상비용USD", 0))
    base["tokens_total"] = base["input"] + base["output"] + base["cache_write"] + base["cache_read"]
    return base


# ── 완성 세특 저장 (과목별 '세특기록' 탭에 학번 기준 upsert) ───────────────────
def save_final_sebteuk(subject_key: str, student_num: str, name: str, text: str) -> tuple[bool, str]:
    """다듬은 최종 세특을 해당 과목의 성찰 스프레드시트 '세특기록' 탭에 저장한다.

    같은 학번이 이미 있으면 그 행을 갱신(덮어쓰기)하고, 없으면 새 행을 추가한다.
    반환: (성공여부, "저장" | "갱신" | 오류메시지)
    """
    text = (text or "").strip()
    if not text:
        return False, "저장할 내용이 비어 있습니다."
    sheet_id = _get_sheet_id(subject_key)
    if not sheet_id:
        return False, "성찰 스프레드시트 ID가 설정되지 않았습니다."
    try:
        from datetime import datetime, timezone, timedelta
        from auth_utils import _get_gspread_client
        client = _get_gspread_client()
        if client is None:
            return False, "구글 서비스 계정 연결에 실패했습니다."
        sh = client.open_by_key(sheet_id)
        try:
            ws = sh.worksheet(_RECORD_SHEET)
        except Exception:
            ws = sh.add_worksheet(title=_RECORD_SHEET, rows=2000, cols=len(_RECORD_HEADER) + 1)
            ws.append_row(_RECORD_HEADER)

        header = ws.row_values(1) or _RECORD_HEADER
        now = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M:%S")

        def _row_in_header_order() -> list:
            mapping = {"저장시각": now, "학번": str(student_num), "이름": str(name), "세특": text}
            return [mapping.get(col, "") for col in header]

        records = ws.get_all_records(numericise_ignore=["all"])
        for i, r in enumerate(records, start=2):  # 2행부터 데이터
            if str(r.get("학번", "")).strip() == str(student_num).strip():
                ws.update(range_name=f"A{i}", values=[_row_in_header_order()])
                return True, "갱신"
        ws.append_row(_row_in_header_order())
        return True, "저장"
    except Exception as e:
        print(f"[sebteuk_utils] save_final_sebteuk error: {e}")
        return False, str(e)
