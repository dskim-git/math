# auth_utils.py
"""
인증(Authentication) 유틸리티 모듈.

비밀번호 해싱  : bcrypt
사용자 DB      : Google Sheets (secrets의 users_spreadsheet_id)

워크시트 구조
  학생    : 학번, 이름, 아이디, 해시비밀번호, 학년, 승인상태, 가입일, 마지막로그인
  일반인  : 이름, 아이디, 사용목적, 해시비밀번호, 그룹, 승인상태, 가입일, 마지막로그인
  학년권한: 학년, 허용과목  (콤마로 구분된 subject key 목록)
  그룹권한: 그룹명, 허용과목
    그룹수업권한: 그룹명, 교과, 허용수업  (콤마로 구분된 unit key 목록)
"""

import re
import threading
import bcrypt
import streamlit as st
from datetime import datetime, timezone, timedelta
from typing import Optional

_KST = timezone(timedelta(hours=9))

# ── 교과 목록 (home.py의 SUBJECTS와 동기화 유지) ───────────────────────────
ALL_SUBJECTS: dict[str, str] = {
    "common":          "공통수학1",
    "common2":         "공통수학2",
    "algebra":         "대수",
    "calculus1":       "미적분1",
    "calculus2":       "미적분2",
    "probability_new": "확률과통계",
    "economics_math":  "경제수학",
    "calculus":        "미적분학(이전 교육과정)",
    "probability":     "확률과통계(이전 교육과정)",
    "geometry":        "기하학",
    "gifted":          "영재",
    "etc":             "기타",
}

# ── 상수 ─────────────────────────────────────────────────────────────────────
ADMIN_ID = "admin"

WS_STUDENTS   = "학생"
WS_GENERAL    = "일반인"
WS_GRADE_PERM = "학년권한"
WS_GROUP_PERM = "그룹권한"
WS_GROUP_LESSON_PERM = "그룹수업권한"

# ── 2026 수강생 명단 (회원가입 검증 및 학급별 현황용) ────────────────────────
WS_ROSTER = "2026수강생명단"   # 구글 시트 탭 이름

STUDENTS_HEADER   = ["학번", "이름", "아이디", "해시비밀번호", "학년",
                      "승인상태", "가입일", "마지막로그인"]
GENERAL_HEADER    = ["이름", "아이디", "사용목적", "해시비밀번호", "그룹",
                      "승인상태", "가입일", "마지막로그인"]
GRADE_PERM_HEADER = ["학년", "허용과목"]
GROUP_PERM_HEADER = ["그룹명", "허용과목"]
GROUP_LESSON_PERM_HEADER = ["그룹명", "교과", "허용수업"]

STATUS_PENDING  = "대기"
STATUS_APPROVED = "승인"
STATUS_REJECTED = "거부"

# ── 계정 잠금 ─────────────────────────────────────────────────────────────────
WS_LOCKOUT     = "계정잠금"
LOCKOUT_HEADER = ["아이디", "실패횟수", "최근실패시각", "잠금상태"]
MAX_FAIL       = 5

# ── 비밀번호 유틸 ─────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """비밀번호를 bcrypt로 해시합니다."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """비밀번호와 해시가 일치하는지 확인합니다."""
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def check_password_policy(password: str) -> list[str]:
    """비밀번호 정책 위반 항목 목록을 반환합니다. 빈 리스트 = 통과."""
    errors: list[str] = []
    if len(password) < 8:
        errors.append("비밀번호는 8자 이상이어야 합니다.")
    if not any(c.isdigit() for c in password):
        errors.append("숫자를 1개 이상 포함해야 합니다.")
    return errors


def _is_valid_user_id(uid: str) -> bool:
    """아이디 형식 검사: 영문·숫자·밑줄, 4~20자."""
    return bool(re.match(r"^[a-zA-Z0-9_]{4,20}$", uid))


# ── Google Sheets 연결 ─────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def _get_gspread_client():
    """gspread 클라이언트를 앱 수명 동안 한 번만 생성하여 재사용합니다."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return gspread.authorize(creds)
    except Exception:
        return None


def _get_users_spreadsheet_id() -> str:
    try:
        return str(st.secrets["users_spreadsheet_id"])
    except Exception:
        return ""


def _get_or_create_ws(client, sheet_id: str, ws_name: str,
                      header: list, rows: int = 1000):
    """워크시트를 가져오거나 없으면 생성하여 반환합니다."""
    try:
        sh = client.open_by_key(sheet_id)
        try:
            return sh.worksheet(ws_name)
        except Exception:
            ws = sh.add_worksheet(title=ws_name, rows=rows,
                                  cols=len(header) + 2)
            ws.append_row(header)
            return ws
    except Exception:
        return None


def _is_sheets_rate_limit_error(exc: Exception) -> bool:
    msg = str(exc)
    return "429" in msg or "Read requests per minute per user" in msg or "Quota exceeded" in msg


def _safe_get_all_records(ws) -> list[dict]:
    try:
        return ws.get_all_records(numericise_ignore=['all'])
    except Exception as e:
        if _is_sheets_rate_limit_error(e):
            print(f"[auth_utils] sheets read throttled: {e}")
            return []
        raise


def _safe_get_all_values(ws) -> list[list[str]]:
    try:
        return ws.get_all_values()
    except Exception as e:
        if _is_sheets_rate_limit_error(e):
            print(f"[auth_utils] sheets read throttled: {e}")
            return []
        raise


def _normalize_group_name(group_name: str) -> str:
    name = str(group_name or "")
    name = name.replace("\u200b", "").replace("\ufeff", "").strip()
    name = name.replace("（", "(").replace("）", ")")
    return name


def _parse_csv_tokens(raw: str) -> set[str]:
    text = str(raw or "").strip()
    if not text:
        return set()
    text = text.replace("，", ",").replace(";", ",").replace("\n", ",")
    return {token.strip() for token in text.split(",") if token.strip()}


def _clear_auth_caches(*, clear_users: bool = False,
                       clear_grade_perms: bool = False,
                       clear_group_perms: bool = False,
                       clear_group_lesson_perms: bool = False,
                       clear_lockout: bool = False,
                       clear_roster: bool = False) -> None:
    """auth_utils 내부 캐시만 선택적으로 무효화합니다."""
    try:
        if clear_users:
            _cached_students.clear()
            _cached_general.clear()
        if clear_grade_perms:
            _cached_grade_perms.clear()
        if clear_group_perms:
            _cached_group_perms.clear()
        if clear_group_lesson_perms:
            _cached_group_lesson_perms.clear()
        if clear_lockout:
            _cached_lockout.clear()
        if clear_roster:
            _cached_roster.clear()
            get_roster_debug_info.clear()
    except Exception:
        pass


# ── 캐시된 데이터 로더 ────────────────────────────────────────────────────────

@st.cache_data(ttl=60, show_spinner=False)
def _cached_students(sheet_id: str) -> list[dict]:
    client = _get_gspread_client()
    if not client or not sheet_id:
        return []
    ws = _get_or_create_ws(client, sheet_id, WS_STUDENTS, STUDENTS_HEADER)
    return _safe_get_all_records(ws) if ws else []


@st.cache_data(ttl=60, show_spinner=False)
def _cached_general(sheet_id: str) -> list[dict]:
    client = _get_gspread_client()
    if not client or not sheet_id:
        return []
    ws = _get_or_create_ws(client, sheet_id, WS_GENERAL, GENERAL_HEADER)
    return _safe_get_all_records(ws) if ws else []


@st.cache_data(ttl=60, show_spinner=False)
def _cached_grade_perms(sheet_id: str) -> dict[str, set]:
    """학년 → 허용 교과 key 집합."""
    client = _get_gspread_client()
    if not client or not sheet_id:
        return {}
    ws = _get_or_create_ws(client, sheet_id, WS_GRADE_PERM,
                           GRADE_PERM_HEADER, rows=20)
    if not ws:
        return {}
    result: dict[str, set] = {}
    for row in _safe_get_all_records(ws):
        grade = str(row.get("학년", "")).strip()
        subjects_str = str(row.get("허용과목", "")).strip()
        if grade:
            result[grade] = {s.strip() for s in subjects_str.split(",") if s.strip()}
    return result


@st.cache_data(ttl=60, show_spinner=False)
def _cached_group_perms(sheet_id: str) -> dict[str, set]:
    """그룹명 → 허용 교과 key 집합."""
    client = _get_gspread_client()
    if not client or not sheet_id:
        return {}
    ws = _get_or_create_ws(client, sheet_id, WS_GROUP_PERM,
                           GROUP_PERM_HEADER, rows=50)
    if not ws:
        return {}
    result: dict[str, set] = {}
    for row in _safe_get_all_records(ws):
        group = _normalize_group_name(row.get("그룹명", ""))
        subjects = _parse_csv_tokens(str(row.get("허용과목", "")))
        if group:
            if group not in result:
                result[group] = set()
            result[group].update(subjects)
    return result


@st.cache_data(ttl=60, show_spinner=False)
def _cached_group_lesson_perms(sheet_id: str) -> dict[str, dict[str, set[str]]]:
    """그룹명 → (교과 key → 허용 unit key 집합)."""
    client = _get_gspread_client()
    if not client or not sheet_id:
        return {}
    ws = _get_or_create_ws(client, sheet_id, WS_GROUP_LESSON_PERM,
                           GROUP_LESSON_PERM_HEADER, rows=200)
    if not ws:
        return {}
    result: dict[str, dict[str, set[str]]] = {}
    for row in _safe_get_all_records(ws):
        group = _normalize_group_name(row.get("그룹명", ""))
        subject = str(row.get("교과", "")).strip()
        unit_set = _parse_csv_tokens(str(row.get("허용수업", "")))
        if not group or not subject:
            continue
        if group not in result:
            result[group] = {}
        if subject not in result[group]:
            result[group][subject] = set()
        result[group][subject].update(unit_set)
    return result


# ── 계정 잠금 관련 함수 ──────────────────────────────────────────────────────

@st.cache_data(ttl=30, show_spinner=False)
def _cached_lockout(sheet_id: str) -> list[dict]:
    client = _get_gspread_client()
    if not client or not sheet_id:
        return []
    ws = _get_or_create_ws(client, sheet_id, WS_LOCKOUT, LOCKOUT_HEADER, rows=200)
    return _safe_get_all_records(ws) if ws else []


def _fill_merged(row: list) -> list:
    """병합 셀처럼 비어 있는 셀을 왼쪽의 마지막 값으로 채웁니다."""
    result = list(row)
    last = ""
    for i, v in enumerate(result):
        s = str(v).strip()
        if s:
            last = s
        result[i] = last
    return result


def _normalize_class_name(subject: str, cls: str) -> str:
    """
    과목명 + 반 이름 → '1학년 9반' 형식으로 정규화.
    예) subject='공통수학', cls='9반'  → '1학년 9반'
        subject='확률과 통계', cls='10반' → '2학년 10반'
    """
    subj = subject.replace(" ", "")
    if "공통수학" in subj or ("공통" in subj and "수학" in subj):
        grade = "1학년"
    elif "확률" in subj and "통계" in subj:
        grade = "2학년"
    else:
        grade = ""
    cls_num = cls.replace("반", "").strip()
    if grade and cls_num:
        return f"{grade} {cls_num}반"
    return f"{cls_num}반" if cls_num else cls


def _parse_roster_flat(all_values: list) -> list[dict]:
    """형식 A: 첫 행이 헤더인 단순 세로 목록 파싱."""
    headers_row = all_values[0]
    valid_idx = [i for i, h in enumerate(headers_row) if str(h).strip()]
    headers = [str(headers_row[i]).strip() for i in valid_idx]
    result = []
    for row in all_values[1:]:
        if not any(row):
            continue
        record = {headers[j]: (str(row[valid_idx[j]]).strip() if valid_idx[j] < len(row) else "")
                  for j in range(len(headers))}
        result.append(record)
    return result


def _parse_roster_horizontal(all_values: list) -> list[dict]:
    """
    형식 B: 가로 나열 파싱.
      행 0 : 과목명 (병합 셀 → 첫 셀에만 값)
      행 1 : 반 이름 (병합 셀 → 첫 셀에만 값)
      행 2 : '학번' / '이름' 반복 헤더
      행 3+: 데이터
    """
    # '학번'이 2회 이상 등장하는 헤더 행 탐색 (최대 5행 이내)
    header_row_idx = None
    for i, row in enumerate(all_values[:5]):
        if [str(c).strip() for c in row].count("학번") >= 2:
            header_row_idx = i
            break
    if header_row_idx is None:
        return []

    header_row = [str(c).strip() for c in all_values[header_row_idx]]
    # 병합 셀 값 채우기
    row1 = _fill_merged(all_values[0]) if header_row_idx >= 1 else []
    row2 = _fill_merged(all_values[1]) if header_row_idx >= 2 else []

    # (학번 col index, 이름 col index, 반 이름) 쌍 수집
    col_pairs = []
    for i, h in enumerate(header_row):
        if h == "학번":
            # 바로 뒤에 '이름' 컬럼 탐색
            name_col = next(
                (j for j in range(i + 1, min(i + 3, len(header_row)))
                 if header_row[j] == "이름"),
                None,
            )
            if name_col is None:
                continue
            subject = row1[i] if i < len(row1) else ""
            cls     = row2[i] if i < len(row2) else ""
            class_name = _normalize_class_name(subject, cls)
            col_pairs.append((i, name_col, class_name))

    if not col_pairs:
        return []

    result = []
    for row in all_values[header_row_idx + 1:]:
        if not any(row):
            continue
        for num_col, name_col, class_name in col_pairs:
            num  = str(row[num_col]).strip()  if num_col  < len(row) else ""
            name = str(row[name_col]).strip() if name_col < len(row) else ""
            if num and name:
                result.append({"학번": num, "이름": name, "반": class_name})
    return result


@st.cache_data(ttl=300, show_spinner=False)
def _cached_roster(sheet_id: str) -> list[dict]:
    """
    '2026수강생명단' 시트에서 전체 수강생 목록을 읽어옵니다.

    형식 A (세로 목록):  헤더행(학번|이름|반) + 데이터 행
    형식 B (가로 나열):  과목→반→학번/이름 쌍이 옆으로 나열 (현재 시트 형식)

    반환: [{"학번": "...", "이름": "...", "반": "..."}, ...]
    """
    client = _get_gspread_client()
    if not client or not sheet_id:
        return []
    try:
        sh = client.open_by_key(sheet_id)
        ws = sh.worksheet(WS_ROSTER)
        all_values = _safe_get_all_values(ws)
        if not all_values:
            return []

        first_row = [str(c).strip() for c in all_values[0]]

        # 형식 A: 첫 행에 '학번'·'이름' 포함 (단순 세로 목록)
        if "학번" in first_row and "이름" in first_row:
            return _parse_roster_flat(all_values)

        # 형식 B: 어딘가 행에 '학번'이 2번 이상 → 가로 나열
        for row in all_values[:5]:
            if [str(c).strip() for c in row].count("학번") >= 2:
                return _parse_roster_horizontal(all_values)

        return []
    except Exception:
        return []


@st.cache_data(ttl=300, show_spinner=False)
def get_roster_debug_info(sheet_id: str) -> dict:
    """
    수강생 명단 로드 상태를 점검합니다. (오류 진단용 — 캐시 없음)
    반환: {"ok": bool, "error": str, "sheet_id": str, "worksheets": list[str]}
    """
    client = _get_gspread_client()
    if not client:
        return {"ok": False, "error": "gspread 클라이언트 초기화 실패 (서비스 계정 설정을 확인하세요)", "sheet_id": sheet_id, "worksheets": []}
    if not sheet_id:
        return {"ok": False, "error": "users_spreadsheet_id secret이 설정되지 않았습니다", "sheet_id": sheet_id, "worksheets": []}
    try:
        sh = client.open_by_key(sheet_id)
        ws_list = [ws.title for ws in sh.worksheets()]
        if WS_ROSTER not in ws_list:
            return {
                "ok": False,
                "error": f"'{WS_ROSTER}' 시트가 없습니다. 현재 탭 목록: {ws_list}",
                "sheet_id": sheet_id,
                "worksheets": ws_list,
            }
        ws = sh.worksheet(WS_ROSTER)
        all_values = ws.get_all_values()
        if not all_values:
            return {"ok": False, "error": "시트가 비어 있습니다", "sheet_id": sheet_id, "worksheets": ws_list}
        first_row = [str(c).strip() for c in all_values[0]]
        fmt = "A(세로목록)" if ("학번" in first_row and "이름" in first_row) else "B(가로나열)"
        data = _cached_roster(sheet_id)
        return {"ok": True, "error": "", "sheet_id": sheet_id, "worksheets": ws_list,
                "format": fmt, "rows": len(data)}
    except Exception as e:
        return {"ok": False, "error": str(e), "sheet_id": sheet_id, "worksheets": []}


def get_roster_student_counts(sheet_id: str) -> dict[str, int]:
    """
    학급별 수강생 수를 반환합니다.
    반환: {"1학년 9반": 35, ...}  — 반 이름은 시트 '반' 또는 '학급' 컬럼 값 기준
    """
    from collections import Counter
    rows = _cached_roster(sheet_id)
    counts: Counter = Counter()
    for r in rows:
        cls = str(r.get("반", "") or r.get("학급", "")).strip()
        if cls:
            counts[cls] += 1
    return dict(counts)


def verify_roster_student(sheet_id: str, student_num: str, name: str) -> bool:
    """
    수강생 명단에 해당 학번+이름 조합이 있는지 확인합니다.
    """
    num  = student_num.strip()
    name = name.strip()
    for r in _cached_roster(sheet_id):
        if str(r.get("학번", "")).strip() == num and str(r.get("이름", "")).strip() == name:
            return True
    return False


def is_account_locked(user_id: str) -> bool:
    """계정이 잠금 상태인지 확인합니다."""
    sheet_id = _get_users_spreadsheet_id()
    for row in _cached_lockout(sheet_id):
        if str(row.get("아이디", "")).strip() == user_id:
            return str(row.get("잠금상태", "")).strip() == "잠금"
    return False


def increment_fail_count(user_id: str) -> int:
    """로그인 실패 횟수를 1 증가시킵니다. MAX_FAIL 이상이면 잠금 처리. 새 실패 횟수를 반환합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return 0
    try:
        ws = _get_or_create_ws(client, sheet_id, WS_LOCKOUT, LOCKOUT_HEADER, rows=200)
        if not ws:
            return 0
        now_str  = datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
        header   = ws.row_values(1)
        cnt_idx  = header.index("실패횟수")     + 1
        ts_idx   = header.index("최근실패시각") + 1
        lock_idx = header.index("잠금상태")     + 1
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("아이디", "")).strip() == user_id:
                new_cnt  = int(row.get("실패횟수", 0) or 0) + 1
                new_lock = "잠금" if new_cnt >= MAX_FAIL else "정상"
                ws.update_cell(i, cnt_idx,  new_cnt)
                ws.update_cell(i, ts_idx,   now_str)
                ws.update_cell(i, lock_idx, new_lock)
                _clear_auth_caches(clear_lockout=True)
                return new_cnt
        # 신규 항목 추가
        ws.append_row([user_id, 1, now_str, "정상"])
        _clear_auth_caches(clear_lockout=True)
        return 1
    except Exception:
        return 0


def reset_lockout(user_id: str) -> bool:
    """로그인 실패 횟수를 초기화하고 계정 잠금을 해제합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    try:
        ws = _get_or_create_ws(client, sheet_id, WS_LOCKOUT, LOCKOUT_HEADER, rows=200)
        if not ws:
            return False
        header   = ws.row_values(1)
        cnt_idx  = header.index("실패횟수")     + 1
        lock_idx = header.index("잠금상태")     + 1
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("아이디", "")).strip() == user_id:
                ws.update_cell(i, cnt_idx,  0)
                ws.update_cell(i, lock_idx, "정상")
                _clear_auth_caches(clear_lockout=True)
                return True
        return True  # 기록 없으면 잠금 없음 → 성공으로 처리
    except Exception:
        return False


# ── 마지막 로그인 기록 ────────────────────────────────────────────────────────

def _bump_last_login(ws_name: str, id_col: str, id_val: str) -> None:
    """마지막 로그인 일시를 Google Sheets에 기록합니다(실패 시 무시)."""
    try:
        sheet_id = _get_users_spreadsheet_id()
        client = _get_gspread_client()
        if not client or not sheet_id:
            return
        sh = client.open_by_key(sheet_id)
        ws = sh.worksheet(ws_name)
        header = ws.row_values(1)
        # 운영 중 시트 헤더가 '마지막 로그인'처럼 변경된 경우도 허용
        login_candidates = ["마지막로그인", "마지막 로그인"]
        login_col = next((c for c in login_candidates if c in header), None)
        if login_col is None:
            normalized = [h.replace(" ", "") for h in header]
            for c in login_candidates:
                c_norm = c.replace(" ", "")
                if c_norm in normalized:
                    login_col = header[normalized.index(c_norm)]
                    break
        if login_col is None:
            return
        id_idx     = header.index(id_col) + 1
        login_idx  = header.index(login_col) + 1
        now_str    = datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get(id_col, "")).strip() == id_val:
                ws.update_cell(i, login_idx, now_str)
                break
        _clear_auth_caches(clear_users=True)
    except Exception as e:
        # 로그인 성공 자체는 유지하되, 서버 로그에는 남겨 원인 추적 가능하게 함
        print(f"[auth_utils] last login update failed ({ws_name}, {id_col}={id_val}): {e}")


# ── 인증 ─────────────────────────────────────────────────────────────────────

def _get_admin_hash() -> str:
    try:
        return str(st.secrets["admin_password_hash"])
    except Exception:
        return ""


def authenticate(user_id: str, password: str) -> Optional[dict]:
    """
    아이디·비밀번호로 인증합니다.

    반환값:
      성공 → {"type": "admin"|"student"|"general", "id": str, "name": str,
                             "grade": str|None, "group": str|None,
                             "allowed_subjects": set|None,
                             "allowed_lessons": dict[str, set[str]]|None}
      미승인 → {"type": "pending", "id": str}
      잠금  → {"type": "locked",  "id": str}
      실패  → None
    """
    if not user_id or not password:
        return None

    # 관리자
    if user_id == ADMIN_ID:
        admin_hash = _get_admin_hash()
        if admin_hash and verify_password(password, admin_hash):
            return {
                "type": "admin",
                "id": ADMIN_ID,
                "name": "관리자",
                "grade": None,
                "group": None,
                "allowed_subjects": None,
                "allowed_lessons": None,
            }
        return None

    sheet_id = _get_users_spreadsheet_id()

    # 계정 잠금 확인
    if is_account_locked(user_id):
        return {"type": "locked", "id": user_id}

    # 학생
    for row in _cached_students(sheet_id):
        if str(row.get("아이디", "")).strip() != user_id:
            continue
        status = str(row.get("승인상태", "")).strip()
        if status != STATUS_APPROVED:
            return {"type": "pending", "id": user_id}
        if not verify_password(password, str(row.get("해시비밀번호", ""))):
            increment_fail_count(user_id)
            return None
        grade      = str(row.get("학년", "")).strip()
        grade_perms = _cached_grade_perms(sheet_id)
        allowed    = grade_perms.get(grade, None)
        # 마지막 로그인은 동기 기록으로 처리해 누락 가능성을 줄임
        threading.Thread(target=reset_lockout,     args=(user_id,),                          daemon=True).start()
        _bump_last_login(WS_STUDENTS, "아이디", user_id)
        return {
            "type": "student",
            "id": user_id,
            "name": str(row.get("이름", "")),
            "grade": grade,
            "group": None,
            "allowed_subjects": allowed,
            "allowed_lessons": None,
        }

    # 일반인
    for row in _cached_general(sheet_id):
        if str(row.get("아이디", "")).strip() != user_id:
            continue
        status = str(row.get("승인상태", "")).strip()
        if status != STATUS_APPROVED:
            return {"type": "pending", "id": user_id}
        if not verify_password(password, str(row.get("해시비밀번호", ""))):
            increment_fail_count(user_id)
            return None
        group       = _normalize_group_name(row.get("그룹", ""))
        group_perms = _cached_group_perms(sheet_id)
        # 일반인은 그룹/권한이 명시되기 전까지 기본 접근 없음
        allowed     = group_perms.get(group, set()) if group else set()
        lesson_perms = _cached_group_lesson_perms(sheet_id)
        allowed_lessons = lesson_perms.get(group, {}) if group else {}
        # 마지막 로그인은 동기 기록으로 처리해 누락 가능성을 줄임
        threading.Thread(target=reset_lockout,     args=(user_id,),                          daemon=True).start()
        _bump_last_login(WS_GENERAL, "아이디", user_id)
        return {
            "type": "general",
            "id": user_id,
            "name": str(row.get("이름", "")),
            "grade": None,
            "group": group,
            "allowed_subjects": allowed,
            "allowed_lessons": allowed_lessons,
        }

    return None


def get_user_permission_snapshot(user_type: str, user_id: str) -> Optional[dict]:
    """현재 시트 기준으로 사용자의 최신 권한 스냅샷을 반환합니다."""
    if not user_type or not user_id:
        return None

    if user_type == "admin":
        return {
            "type": "admin",
            "id": ADMIN_ID,
            "name": "관리자",
            "grade": None,
            "group": None,
            "allowed_subjects": None,
            "allowed_lessons": None,
        }

    sheet_id = _get_users_spreadsheet_id()

    if user_type == "student":
        for row in _cached_students(sheet_id):
            if str(row.get("아이디", "")).strip() != user_id:
                continue
            grade = str(row.get("학년", "")).strip()
            grade_perms = _cached_grade_perms(sheet_id)
            return {
                "type": "student",
                "id": user_id,
                "name": str(row.get("이름", "")),
                "grade": grade,
                "group": None,
                "allowed_subjects": grade_perms.get(grade, None),
                "allowed_lessons": None,
            }
        return None

    if user_type == "general":
        for row in _cached_general(sheet_id):
            if str(row.get("아이디", "")).strip() != user_id:
                continue
            group = _normalize_group_name(row.get("그룹", ""))
            group_perms = _cached_group_perms(sheet_id)
            lesson_perms = _cached_group_lesson_perms(sheet_id)
            return {
                "type": "general",
                "id": user_id,
                "name": str(row.get("이름", "")),
                "grade": None,
                "group": group,
                "allowed_subjects": group_perms.get(group, set()) if group else set(),
                "allowed_lessons": lesson_perms.get(group, {}) if group else {},
            }
        return None

    return None


# ── 회원가입 ──────────────────────────────────────────────────────────────────

def is_id_taken(user_id: str) -> bool:
    """아이디 중복 여부를 확인합니다."""
    if user_id == ADMIN_ID:
        return True
    sheet_id = _get_users_spreadsheet_id()
    for row in _cached_students(sheet_id):
        if str(row.get("아이디", "")).strip() == user_id:
            return True
    for row in _cached_general(sheet_id):
        if str(row.get("아이디", "")).strip() == user_id:
            return True
    return False


def is_student_num_taken(student_num: str) -> bool:
    """학번 중복 여부를 확인합니다."""
    sheet_id = _get_users_spreadsheet_id()
    for row in _cached_students(sheet_id):
        if str(row.get("학번", "")).strip() == student_num:
            return True
    return False


def register_student(student_num: str, name: str, password: str,
                     grade: str) -> tuple[bool, str]:
    """
    학생 회원가입.
    반환: (성공 여부, 생성된 아이디  |  오류 메시지)
    """
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False, "데이터베이스 연결에 실패했습니다."

    year    = datetime.now(_KST).year
    auto_id = f"{year}{student_num}"

    if is_student_num_taken(student_num):
        return False, "이미 가입된 학번입니다."
    if is_id_taken(auto_id):
        return False, f"이미 사용 중인 아이디입니다({auto_id})."

    ws = _get_or_create_ws(client, sheet_id, WS_STUDENTS, STUDENTS_HEADER)
    if ws is None:
        return False, "워크시트 연결에 실패했습니다."

    hashed  = hash_password(password)
    now_str = datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([student_num, name, auto_id, hashed,
                   grade, STATUS_PENDING, now_str, ""])
    _clear_auth_caches(clear_users=True)
    return True, auto_id


def register_general(name: str, user_id: str, password: str,
                     purpose: str) -> tuple[bool, str]:
    """
    일반인 회원가입.
    반환: (성공 여부, 오류 메시지)
    """
    if not _is_valid_user_id(user_id):
        return False, "아이디는 영문·숫자·밑줄만 사용 가능합니다 (4~20자)."
    if is_id_taken(user_id):
        return False, "이미 사용 중인 아이디입니다."

    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False, "데이터베이스 연결에 실패했습니다."

    ws = _get_or_create_ws(client, sheet_id, WS_GENERAL, GENERAL_HEADER)
    if ws is None:
        return False, "워크시트 연결에 실패했습니다."

    hashed  = hash_password(password)
    now_str = datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([name, user_id, purpose, hashed,
                   "", STATUS_PENDING, now_str, ""])
    _clear_auth_caches(clear_users=True)
    return True, ""


# ── 관리자 전용 기능 ──────────────────────────────────────────────────────────

def update_user_status(user_type: str, user_id: str, new_status: str) -> bool:
    """승인 상태를 변경합니다. user_type: 'student'|'general'"""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    ws_name = WS_STUDENTS if user_type == "student" else WS_GENERAL
    try:
        sh     = client.open_by_key(sheet_id)
        ws     = sh.worksheet(ws_name)
        header = ws.row_values(1)
        id_idx     = header.index("아이디")     + 1
        status_idx = header.index("승인상태")   + 1
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("아이디", "")).strip() == user_id:
                ws.update_cell(i, status_idx, new_status)
                _clear_auth_caches(clear_users=True)
                return True
    except Exception:
        pass
    return False


def reset_user_password(user_type: str, user_id: str,
                        new_password: str) -> bool:
    """비밀번호를 재설정합니다 (관리자 전용)."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    ws_name = WS_STUDENTS if user_type == "student" else WS_GENERAL
    try:
        sh       = client.open_by_key(sheet_id)
        ws       = sh.worksheet(ws_name)
        header   = ws.row_values(1)
        id_idx   = header.index("아이디")       + 1
        hash_idx = header.index("해시비밀번호") + 1
        new_hash = hash_password(new_password)
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("아이디", "")).strip() == user_id:
                ws.update_cell(i, hash_idx, new_hash)
                _clear_auth_caches(clear_users=True)
                return True
    except Exception:
        pass
    return False


def update_user_group(user_id: str, new_group: str) -> bool:
    """일반인 사용자의 그룹을 변경합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    try:
        sh        = client.open_by_key(sheet_id)
        ws        = sh.worksheet(WS_GENERAL)
        header    = ws.row_values(1)
        id_idx    = header.index("아이디") + 1
        group_idx = header.index("그룹")   + 1
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("아이디", "")).strip() == user_id:
                ws.update_cell(i, group_idx, _normalize_group_name(new_group))
                _clear_auth_caches(clear_users=True)
                return True
    except Exception:
        pass
    return False


def save_grade_permissions(grade: str, subjects: list[str]) -> bool:
    """학년별 허용 과목을 저장/갱신합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    try:
        ws = _get_or_create_ws(client, sheet_id, WS_GRADE_PERM,
                               GRADE_PERM_HEADER, rows=20)
        if not ws:
            return False
        header       = ws.row_values(1)
        grade_idx    = header.index("학년")   + 1
        subj_idx     = header.index("허용과목") + 1
        subjects_str = ",".join(subjects)
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("학년", "")).strip() == grade:
                ws.update_cell(i, subj_idx, subjects_str)
                _clear_auth_caches(clear_grade_perms=True)
                return True
        ws.append_row([grade, subjects_str])
        _clear_auth_caches(clear_grade_perms=True)
        return True
    except Exception:
        return False


def save_group_permissions(group_name: str, subjects: list[str]) -> bool:
    """그룹별 허용 과목을 저장/갱신합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    normalized_group = _normalize_group_name(group_name)
    try:
        ws = _get_or_create_ws(client, sheet_id, WS_GROUP_PERM,
                               GROUP_PERM_HEADER, rows=50)
        if not ws:
            return False
        header       = ws.row_values(1)
        group_idx    = header.index("그룹명")   + 1
        subj_idx     = header.index("허용과목") + 1
        subjects_str = ",".join(subjects)
        found = False
        for i, row in enumerate(ws.get_all_records(), start=2):
            if _normalize_group_name(row.get("그룹명", "")) == normalized_group:
                ws.update_cell(i, subj_idx, subjects_str)
                found = True
        if found:
            _clear_auth_caches(clear_group_perms=True)
            return True
        ws.append_row([normalized_group, subjects_str])
        _clear_auth_caches(clear_group_perms=True)
        return True
    except Exception:
        return False


def save_group_lesson_permissions(group_name: str, subject_key: str,
                                  unit_keys: list[str]) -> bool:
    """그룹별 교과 내 수업(unit) 접근 권한을 저장/갱신합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    normalized_group = _normalize_group_name(group_name)
    try:
        ws = _get_or_create_ws(client, sheet_id, WS_GROUP_LESSON_PERM,
                               GROUP_LESSON_PERM_HEADER, rows=200)
        if not ws:
            return False
        units_str = ",".join(unit_keys)
        found = False
        for i, row in enumerate(ws.get_all_records(), start=2):
            if (
                _normalize_group_name(row.get("그룹명", "")) == normalized_group
                and str(row.get("교과", "")).strip() == subject_key
            ):
                ws.update_cell(i, 3, units_str)
                found = True
        if found:
            _clear_auth_caches(clear_group_lesson_perms=True)
            return True
        ws.append_row([normalized_group, subject_key, units_str])
        _clear_auth_caches(clear_group_lesson_perms=True)
        return True
    except Exception:
        return False


def delete_group(group_name: str) -> bool:
    """그룹 행을 삭제합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    removed_any = False
    try:
        sh = client.open_by_key(sheet_id)
        ws = _get_or_create_ws(client, sheet_id, WS_GROUP_PERM,
                               GROUP_PERM_HEADER, rows=50)
        if not ws:
            return False
        for i, row in enumerate(ws.get_all_records(), start=2):
            if _normalize_group_name(row.get("그룹명", "")) == _normalize_group_name(group_name):
                ws.delete_rows(i)
                removed_any = True
                break
        ws_lesson = _get_or_create_ws(client, sheet_id, WS_GROUP_LESSON_PERM,
                                      GROUP_LESSON_PERM_HEADER, rows=200)
        if ws_lesson:
            to_delete = []
            for i, row in enumerate(ws_lesson.get_all_records(), start=2):
                if _normalize_group_name(row.get("그룹명", "")) == _normalize_group_name(group_name):
                    to_delete.append(i)
            for i in reversed(to_delete):
                ws_lesson.delete_rows(i)
            if to_delete:
                removed_any = True
        if removed_any:
            _clear_auth_caches(clear_group_perms=True, clear_group_lesson_perms=True)
            return True
    except Exception:
        pass
    return removed_any


def get_all_groups() -> list[str]:
    """등록된 그룹명 목록을 반환합니다."""
    sheet_id = _get_users_spreadsheet_id()
    perms    = _cached_group_perms(sheet_id)
    return sorted(perms.keys())


def change_own_password(user_type: str, user_id: str,
                        current_password: str, new_password: str) -> tuple[bool, str]:
    """
    본인 비밀번호 변경.
    현재 비밀번호 확인 후 새 비밀번호로 교체합니다.
    반환: (성공 여부, 오류 메시지)
    """
    # 현재 비밀번호 확인 (인증)
    result = authenticate(user_id, current_password)
    if result is None or result.get("type") in ("pending", "locked"):
        return False, "현재 비밀번호가 올바르지 않습니다."

    pw_errs = check_password_policy(new_password)
    if pw_errs:
        return False, " / ".join(pw_errs)

    ok = reset_user_password(user_type, user_id, new_password)
    if ok:
        return True, ""
    return False, "비밀번호 변경에 실패했습니다. 잠시 후 다시 시도해 주세요."


def batch_register_students(
    rows: list[dict],
) -> tuple[int, int, list[str]]:
    """
    대량 학생 등록.
    rows = [{"학번": ..., "이름": ..., "비밀번호": ..., "학년": ...}, ...]
    반환: (성공 수, 실패 수, 오류 메시지 목록)
    """
    success, fail, errors = 0, 0, []
    for r in rows:
        num   = str(r.get("학번", "")).strip()
        name  = str(r.get("이름", "")).strip()
        pw    = str(r.get("비밀번호", "")).strip()
        grade = str(r.get("학년", "")).strip()
        if not num or not name or not pw:
            fail += 1
            errors.append(f"학번 {num or '(없음)'}: 필수 항목 누락")
            continue
        pw_errs = check_password_policy(pw)
        if pw_errs:
            fail += 1
            errors.append(f"학번 {num}: {'; '.join(pw_errs)}")
            continue
        ok, msg = register_student(num, name, pw, grade)
        if ok:
            success += 1
        else:
            fail += 1
            errors.append(f"학번 {num}: {msg}")
    return success, fail, errors
