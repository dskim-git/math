"""
연구대회 설문 공유 유틸리티
Google Sheets 탭: pre_survey / post_survey / survey_config
"""
from __future__ import annotations
import streamlit as st
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

SHEET_PRE    = "pre_survey"
SHEET_POST   = "post_survey"
SHEET_CONFIG = "survey_config"

PRE_HEADER = [
    "제출시각", "학번", "학년", "학급",
    "[A]흥미1", "[A]흥미2", "[A]흥미3", "[A]흥미4",
    "[B]효능1", "[B]효능2", "[B]효능3", "[B]효능4",
    "[C]불안1", "[C]불안2", "[C]불안3",
    "[D]ICT1",  "[D]ICT2",  "[D]ICT3",
    "[E]시각1", "[E]시각2", "[E]시각3",
    "[F]학습1", "[F]학습2", "[F]학습3",
]

POST_HEADER = [
    "제출시각", "학번", "학년", "학급",
    "[A]흥미1", "[A]흥미2",
    "[B]효능1", "[B]효능2",
    "[C]불안1", "[C]불안2",
    "[D]ICT1",  "[D]ICT2",
    "[E]시각1", "[E]시각2",
    "[F]학습1", "[F]학습2",
    "[G]앱1",   "[G]앱2",   "[G]앱3",
    "[H]개념1", "[H]개념2", "[H]개념3",
    "[I]수업1", "[I]수업2",
    "[J]서술1", "[J]서술2",
]

CONFIG_HEADER = ["key", "value"]

# ── 내부 헬퍼 ─────────────────────────────────────────────────────────────────

def _get_client():
    try:
        import auth_utils
        return auth_utils._get_gspread_client()
    except Exception:
        return None


def _get_spreadsheet():
    client = _get_client()
    if client is None:
        return None
    try:
        sid = str(st.secrets["survey_spreadsheet_id"])
        return client.open_by_key(sid)
    except Exception:
        return None


def _get_or_create_ws(sh, name: str, header: list):
    try:
        return sh.worksheet(name)
    except Exception:
        ws = sh.add_worksheet(title=name, rows=2000, cols=len(header) + 2)
        ws.append_row(header)
        return ws

# ── 설정 (활성화 토글) ────────────────────────────────────────────────────────

# API 실패 시 마지막 성공 값을 유지하는 fallback 저장소
_config_fallback: dict[str, bool] = {}


@st.cache_data(ttl=300, show_spinner=False)
def get_config(key: str) -> bool:
    """survey_config 탭에서 key 값을 읽어 True/False 반환. 5분 캐시."""
    try:
        sh = _get_spreadsheet()
        if sh is None:
            return _config_fallback.get(key, False)
        ws = _get_or_create_ws(sh, SHEET_CONFIG, CONFIG_HEADER)
        for row in ws.get_all_records(numericise_ignore=["all"]):
            if str(row.get("key", "")).strip() == key:
                result = str(row.get("value", "FALSE")).strip().upper() == "TRUE"
                _config_fallback[key] = result   # 성공 시 fallback 갱신
                return result
        _config_fallback.setdefault(key, False)
        return _config_fallback[key]
    except Exception:
        # API 실패 시 마지막 성공 값 반환 (버튼이 사라지는 현상 방지)
        return _config_fallback.get(key, False)


def set_config(key: str, value: bool) -> bool:
    """survey_config 탭에 key=value 저장. 성공 True."""
    try:
        sh = _get_spreadsheet()
        if sh is None:
            return False
        ws = _get_or_create_ws(sh, SHEET_CONFIG, CONFIG_HEADER)
        val_str = "TRUE" if value else "FALSE"
        all_vals = ws.get_all_values()
        for i, row in enumerate(all_vals):
            if row and str(row[0]).strip() == key:
                ws.update_cell(i + 1, 2, val_str)
                get_config.clear()  # 캐시 무효화
                return True
        ws.append_row([key, val_str])
        get_config.clear()  # 캐시 무효화
        return True
    except Exception as e:
        st.error(f"설정 저장 실패: {e}")
        return False

# ── 제출 확인 / 저장 ──────────────────────────────────────────────────────────

def has_submitted(sheet_name: str, user_id: str) -> bool:
    """해당 학번이 이미 제출했는지 확인."""
    try:
        sh = _get_spreadsheet()
        if sh is None:
            return False
        header = PRE_HEADER if sheet_name == SHEET_PRE else POST_HEADER
        ws = _get_or_create_ws(sh, sheet_name, header)
        for row in ws.get_all_records(numericise_ignore=["all"]):
            if str(row.get("학번", "")).strip() == str(user_id).strip():
                return True
        return False
    except Exception:
        return False


def submit_survey(sheet_name: str, user_id: str, answers: dict) -> bool:
    """설문 응답 1행 추가. 성공 True."""
    try:
        sh = _get_spreadsheet()
        if sh is None:
            return False
        header = PRE_HEADER if sheet_name == SHEET_PRE else POST_HEADER
        ws = _get_or_create_ws(sh, sheet_name, header)

        uid = str(user_id).strip()
        grade    = uid[4]     if len(uid) >= 5 else "?"
        class_no = uid[5:7]   if len(uid) >= 7 else "?"
        now_str  = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")

        row = [now_str, uid, grade, class_no]
        for col in header[4:]:
            row.append(answers.get(col, ""))

        ws.append_row(row)
        return True
    except Exception as e:
        st.error(f"제출 실패: {e}")
        return False

# ── 세션 헬퍼 ─────────────────────────────────────────────────────────────────

def current_user() -> dict:
    return {
        "authenticated": st.session_state.get("_authenticated", False),
        "type":          st.session_state.get("_user_type", ""),
        "id":            st.session_state.get("_user_id",   ""),
        "name":          st.session_state.get("_user_name", ""),
    }

def is_admin()   -> bool:
    u = current_user()
    return u["authenticated"] and u["type"] == "admin"

def is_student() -> bool:
    u = current_user()
    return u["authenticated"] and u["type"] == "student"
