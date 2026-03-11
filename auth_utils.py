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
"""

import re
import bcrypt
import streamlit as st
from datetime import datetime
from typing import Optional

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
    "etc":             "기타",
}

# ── 상수 ─────────────────────────────────────────────────────────────────────
ADMIN_ID = "admin"

WS_STUDENTS   = "학생"
WS_GENERAL    = "일반인"
WS_GRADE_PERM = "학년권한"
WS_GROUP_PERM = "그룹권한"

STUDENTS_HEADER   = ["학번", "이름", "아이디", "해시비밀번호", "학년",
                      "승인상태", "가입일", "마지막로그인"]
GENERAL_HEADER    = ["이름", "아이디", "사용목적", "해시비밀번호", "그룹",
                      "승인상태", "가입일", "마지막로그인"]
GRADE_PERM_HEADER = ["학년", "허용과목"]
GROUP_PERM_HEADER = ["그룹명", "허용과목"]

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

def _get_gspread_client():
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


# ── 캐시된 데이터 로더 ────────────────────────────────────────────────────────

@st.cache_data(ttl=60, show_spinner=False)
def _cached_students(sheet_id: str) -> list[dict]:
    client = _get_gspread_client()
    if not client or not sheet_id:
        return []
    ws = _get_or_create_ws(client, sheet_id, WS_STUDENTS, STUDENTS_HEADER)
    return ws.get_all_records() if ws else []


@st.cache_data(ttl=60, show_spinner=False)
def _cached_general(sheet_id: str) -> list[dict]:
    client = _get_gspread_client()
    if not client or not sheet_id:
        return []
    ws = _get_or_create_ws(client, sheet_id, WS_GENERAL, GENERAL_HEADER)
    return ws.get_all_records() if ws else []


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
    for row in ws.get_all_records():
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
    for row in ws.get_all_records():
        group = str(row.get("그룹명", "")).strip()
        subjects_str = str(row.get("허용과목", "")).strip()
        if group:
            result[group] = {s.strip() for s in subjects_str.split(",") if s.strip()}
    return result


# ── 계정 잠금 관련 함수 ──────────────────────────────────────────────────────

@st.cache_data(ttl=30, show_spinner=False)
def _cached_lockout(sheet_id: str) -> list[dict]:
    client = _get_gspread_client()
    if not client or not sheet_id:
        return []
    ws = _get_or_create_ws(client, sheet_id, WS_LOCKOUT, LOCKOUT_HEADER, rows=200)
    return ws.get_all_records() if ws else []


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
        now_str  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                st.cache_data.clear()
                return new_cnt
        # 신규 항목 추가
        ws.append_row([user_id, 1, now_str, "정상"])
        st.cache_data.clear()
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
                st.cache_data.clear()
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
        if "마지막로그인" not in header:
            return
        id_idx     = header.index(id_col) + 1
        login_idx  = header.index("마지막로그인") + 1
        now_str    = datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get(id_col, "")).strip() == id_val:
                ws.update_cell(i, login_idx, now_str)
                break
        st.cache_data.clear()
    except Exception:
        pass


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
               "grade": str|None, "group": str|None, "allowed_subjects": set|None}
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
        reset_lockout(user_id)
        _bump_last_login(WS_STUDENTS, "아이디", user_id)
        return {
            "type": "student",
            "id": user_id,
            "name": str(row.get("이름", "")),
            "grade": grade,
            "group": None,
            "allowed_subjects": allowed,
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
        group       = str(row.get("그룹", "")).strip()
        group_perms = _cached_group_perms(sheet_id)
        allowed     = group_perms.get(group, None) if group else None
        reset_lockout(user_id)
        _bump_last_login(WS_GENERAL, "아이디", user_id)
        return {
            "type": "general",
            "id": user_id,
            "name": str(row.get("이름", "")),
            "grade": None,
            "group": group,
            "allowed_subjects": allowed,
        }

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

    year    = datetime.now().year
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
    st.cache_data.clear()
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
    st.cache_data.clear()
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
                st.cache_data.clear()
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
                st.cache_data.clear()
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
                ws.update_cell(i, group_idx, new_group)
                st.cache_data.clear()
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
                st.cache_data.clear()
                return True
        ws.append_row([grade, subjects_str])
        st.cache_data.clear()
        return True
    except Exception:
        return False


def save_group_permissions(group_name: str, subjects: list[str]) -> bool:
    """그룹별 허용 과목을 저장/갱신합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    try:
        ws = _get_or_create_ws(client, sheet_id, WS_GROUP_PERM,
                               GROUP_PERM_HEADER, rows=50)
        if not ws:
            return False
        header       = ws.row_values(1)
        group_idx    = header.index("그룹명")   + 1
        subj_idx     = header.index("허용과목") + 1
        subjects_str = ",".join(subjects)
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("그룹명", "")).strip() == group_name:
                ws.update_cell(i, subj_idx, subjects_str)
                st.cache_data.clear()
                return True
        ws.append_row([group_name, subjects_str])
        st.cache_data.clear()
        return True
    except Exception:
        return False


def delete_group(group_name: str) -> bool:
    """그룹 행을 삭제합니다."""
    sheet_id = _get_users_spreadsheet_id()
    client   = _get_gspread_client()
    if not client or not sheet_id:
        return False
    try:
        sh = client.open_by_key(sheet_id)
        ws = sh.worksheet(WS_GROUP_PERM)
        for i, row in enumerate(ws.get_all_records(), start=2):
            if str(row.get("그룹명", "")).strip() == group_name:
                ws.delete_rows(i)
                st.cache_data.clear()
                return True
    except Exception:
        pass
    return False


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
