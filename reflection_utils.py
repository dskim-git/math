"""
공통 성찰 기록 폼 유틸리티.

미니 활동 파일에서 아래처럼 사용합니다::

    from reflection_utils import render_reflection_form

    _QUESTIONS = [
        {"type": "markdown", "text": "**📝 문제 2개를 만들어보세요**"},
        {"key": "문제1", "label": "문제 1", "type": "text_area", "height": 70},
        {"key": "답1",   "label": "문제 1의 정답", "type": "text_input"},
        {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
        {"key": "느낀점",        "label": "💬 느낀 점",          "type": "text_area", "height": 90},
    ]

    # render() 함수 마지막에:
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)

questions 항목 형식
--------------------
- 마크다운 구분자 : {"type": "markdown", "text": "..."}
- 단행 입력       : {"key": "...", "label": "...", "type": "text_input",
                     "placeholder": "..." (선택)}
- 다행 입력       : {"key": "...", "label": "...", "type": "text_area",
                     "height": 80 (선택), "placeholder": "..." (선택)}
"""

import datetime

import requests
import streamlit as st

# ── 성찰 로그 설정 ─────────────────────────────────────────────────────────────
_REFLECTION_LOG_SHEET  = "성찰기록"
_REFLECTION_LOG_HEADER = ["제출시각", "과목", "활동시트명", "학번", "이름"]

# secrets 키 이름으로 과목 자동 판별
_GAS_SUBJECT_MAP = {
    "gas_url_common":          "공통수학",
    "gas_url_probability_new": "확률과통계",
}

# 활동 파일에서 _QUESTIONS=[] 로 비워두면 자동으로 사용되는 과목별 기본 질문
_DEFAULT_QUESTIONS: dict = {
    "공통수학": [
        {"type": "markdown", "text": "**📝 이 활동과 관련된 수학 문제 2개를 스스로 만들고 풀어보세요**"},
        {"key": "문제1", "label": "문제 1", "type": "text_area",  "height": 70},
        {"key": "답1",   "label": "문제 1 정답", "type": "text_input"},
        {"key": "문제2", "label": "문제 2", "type": "text_area",  "height": 70},
        {"key": "답2",   "label": "문제 2 정답", "type": "text_input"},
        {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
        {"key": "느낀점",        "label": "💬 느낀 점",          "type": "text_area", "height": 90},
    ],
    "확률과통계": [
        {"type": "markdown", "text": "**📝 이 활동과 관련된 경우의 수·확률 문제 2개를 스스로 만들고 풀어보세요**"},
        {"key": "문제1", "label": "문제 1", "type": "text_area",  "height": 70},
        {"key": "답1",   "label": "문제 1 정답", "type": "text_input"},
        {"key": "문제2", "label": "문제 2", "type": "text_area",  "height": 70},
        {"key": "답2",   "label": "문제 2 정답", "type": "text_input"},
        {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
        {"key": "느낀점",        "label": "💬 느낀 점",          "type": "text_area", "height": 90},
    ],
}


def _get_or_create_reflection_log_ws():
    """성찰기록 워크시트를 가져오거나 없으면 자동 생성합니다."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds  = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        sh = client.open_by_key(st.secrets["spreadsheet_id"])
        try:
            ws = sh.worksheet(_REFLECTION_LOG_SHEET)
        except Exception:
            ws = sh.add_worksheet(title=_REFLECTION_LOG_SHEET, rows=10000, cols=5)
            ws.append_row(_REFLECTION_LOG_HEADER)
        return ws
    except Exception:
        return None


def _log_reflection_submission(
    sheet_name: str, subject: str, user_id: str, user_name: str
) -> None:
    """성찰 제출 통계를 위해 메인 스프레드시트에 최소 기록을 남깁니다."""
    try:
        ws = _get_or_create_reflection_log_ws()
        if ws is None:
            return
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now_str, subject, sheet_name, user_id, user_name])
    except Exception:
        pass  # 로그 실패가 활동 진행을 방해하지 않도록


def render_reflection_form(
    sheet_name: str,
    gas_url: str,
    questions: list,
    *,
    title: str = "✍️ 활동 후 성찰 기록",
    caption: str = "아래 질문에 답하고 **제출하기** 버튼을 눌러주세요.",
) -> None:
    """공통 성찰 기록 폼을 렌더링합니다.

    - **학생** : 로그인 정보에서 학번·이름을 자동 조회하여 폼을 표시합니다.
    - **일반인**: 성찰 기록 제출이 불필요하다는 안내 메시지만 표시합니다.
    """
    # secrets 키 이름으로 과목 자동 감지
    _subject = ""
    for _key, _subj in _GAS_SUBJECT_MAP.items():
        try:
            if st.secrets.get(_key, "") == gas_url:
                _subject = _subj
                break
        except Exception:
            pass

    # questions가 비어 있으면 과목별 기본 질문 자동 적용
    if not questions:
        questions = _DEFAULT_QUESTIONS.get(_subject, _DEFAULT_QUESTIONS.get("공통수학", []))

    st.divider()
    st.subheader(title)
    st.caption(caption)

    user_type    = st.session_state.get("_user_type", "")
    student_id   = st.session_state.get("_user_id", "")
    student_name = st.session_state.get("_user_name", "")

    # GAS·로그 전송용 학번: 앞 4자리 연도 접두어 제거 (예: "202601234" → "01234")
    _short_id = (
        student_id[4:]
        if len(student_id) >= 9 and student_id[:2] == "20"
        else student_id
    )

    # 일반인: 제출 불필요
    if user_type == "general":
        st.info("💡 일반인 사용자는 성찰 기록 제출이 필요하지 않습니다.")
        return

    # 미로그인 방어 처리 (정상 흐름에서는 발생하지 않아야 함)
    if not student_id:
        st.warning("📋 로그인 후 성찰 기록을 작성할 수 있습니다.")
        return

    # 사용자 정보 안내
    st.markdown(f"📋 **학번**: `{student_id}`　**이름**: **{student_name}**")

    with st.form(f"reflection_{sheet_name}", clear_on_submit=True):
        values: dict = {}
        for q in questions:
            qtype = q.get("type", "text_input")
            if qtype == "markdown":
                st.markdown(q["text"])
            elif qtype == "text_input":
                values[q["key"]] = st.text_input(
                    q["label"],
                    placeholder=q.get("placeholder", ""),
                )
            elif qtype == "text_area":
                values[q["key"]] = st.text_area(
                    q["label"],
                    height=q.get("height", 80),
                    placeholder=q.get("placeholder", ""),
                )

        submitted = st.form_submit_button(
            "📤 제출하기", use_container_width=True, type="primary"
        )

    if submitted:
        payload = {
            "sheet":     sheet_name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "학번":      _short_id,
            "이름":      student_name,
            **values,
        }
        try:
            resp = requests.post(gas_url, json=payload, timeout=10)
            if resp.status_code == 200:
                st.success(f"✅ {student_name}님의 기록이 제출되었습니다!")
                st.balloons()
                _log_reflection_submission(sheet_name, _subject, _short_id, student_name)
            else:
                st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
        except Exception as exc:
            st.error(f"네트워크 오류: {exc}")
