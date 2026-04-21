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
from datetime import timezone, timedelta

import requests
import streamlit as st
import streamlit.components.v1 as _components

_KST = timezone(timedelta(hours=9))

# ── 성찰 로그 설정 ─────────────────────────────────────────────────────────────
_REFLECTION_LOG_SHEET  = "성찰기록"
_REFLECTION_LOG_HEADER = ["제출시각", "과목", "활동시트명", "학번", "이름"]

# secrets 키 이름으로 과목 자동 판별 (표시용 이름)
_GAS_SUBJECT_MAP = {
    "gas_url_common":          "공통수학",
    "gas_url_probability_new": "확률과통계",
}

# secrets 키 이름 → 과목 key (auth_utils.ALL_SUBJECTS 키와 동일)
_GAS_SUBJECT_KEY_MAP = {
    "gas_url_common":          "common",
    "gas_url_probability_new": "probability_new",
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


def _get_subject_key_from_gas_url(gas_url: str) -> str:
    """GAS URL로 과목 key(auth_utils.ALL_SUBJECTS 키)를 반환합니다."""
    for secret_key, subj_key in _GAS_SUBJECT_KEY_MAP.items():
        try:
            if st.secrets.get(secret_key, "") == gas_url:
                return subj_key
        except Exception:
            pass
    return ""


def _write_reflection_to_teacher_sheet(
    teacher_sheet_id: str,
    sheet_name: str,
    payload: dict,
) -> bool:
    """교사의 구글 스프레드시트에 성찰 기록을 추가합니다.

    - 시트(탭)가 없으면 자동 생성하고 헤더를 씁니다.
    - 기존 헤더를 따르므로 열 순서가 유지됩니다.
    """
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

        sh = client.open_by_key(teacher_sheet_id)

        # 데이터 열 순서: 제출시각, 학번, 이름, 나머지 질문 key
        question_keys = [
            k for k in payload
            if k not in ("sheet", "timestamp", "학번", "이름")
        ]
        expected_header = ["제출시각", "학번", "이름"] + question_keys

        try:
            ws = sh.worksheet(sheet_name)
            existing_header = ws.row_values(1)
            if not existing_header:
                ws.append_row(expected_header)
                existing_header = expected_header
        except Exception:
            # 시트가 없으면 새로 만들고 헤더 추가
            ws = sh.add_worksheet(title=sheet_name, rows=5000,
                                  cols=len(expected_header) + 2)
            ws.append_row(expected_header)
            existing_header = expected_header

        # 헤더 순서에 맞게 행 구성
        row = []
        for col in existing_header:
            if col == "제출시각":
                row.append(payload.get("timestamp", ""))
            elif col == "학번":
                row.append(payload.get("학번", ""))
            elif col == "이름":
                row.append(payload.get("이름", ""))
            else:
                row.append(payload.get(col, ""))
        ws.append_row(row)
        return True

    except Exception as e:
        print(f"[reflection_utils] teacher sheet write error: {e}")
        return False


def _class_from_num(num: str) -> str:
    """학번 앞자리에서 학급명을 파생합니다.

    형식: 첫째 자리=학년, 둘째~셋째 자리=반 (예: '207XXXX' → '2학년 7반')
    """
    num = num.strip()
    if len(num) < 3:
        return ""
    try:
        grade = num[0]
        cls   = str(int(num[1:3]))  # 앞의 0 제거: '07' → '7'
        return f"{grade}학년 {cls}반"
    except Exception:
        return ""


def _route_reflection_to_teachers(
    sheet_name: str,
    gas_url: str,
    payload: dict,
    student_num: str,
) -> None:
    """학생의 담당 교사 시트에 성찰 기록을 라우팅합니다 (실패해도 무시).

    - student_num: 단축 학번 (연도 접두어 제거된 형태, 예: "01234")
    - gas_url: 활동의 GAS URL (과목 판별에 사용)
    """
    try:
        from auth_utils import (
            _get_users_spreadsheet_id,
            _cached_roster,
            _cached_teacher_settings,
            _cached_teacher_roster,
        )

        users_sheet_id = _get_users_spreadsheet_id()
        subject_key    = _get_subject_key_from_gas_url(gas_url)
        num            = student_num.strip()

        # ── 학생 학급 조회 (3단계 폴백) ──────────────────────────────────────
        student_class = ""

        # 1단계: 수강생명단의 반 컬럼
        for r in _cached_roster(users_sheet_id):
            if str(r.get("학번", "")).strip() == num:
                student_class = str(r.get("반", "") or r.get("학급", "")).strip()
                break

        # 2단계: 학번 형식에서 파생 (첫째자리=학년, 2~3째자리=반)
        if not student_class:
            student_class = _class_from_num(num)

        # 3단계: 각 교사의 수강생명단에서 학번 직접 검색 → 담당 학급 매칭
        # (student_class가 있어도 교사설정 순회에서 처리하므로, 없을 때만 사용)
        teacher_rows = _cached_teacher_settings(users_sheet_id)

        already_written: set[tuple] = set()

        if not student_class:
            # 학급을 끝내 알 수 없으면 교사별 명단에서 학번 직접 검색
            for row in teacher_rows:
                t_id      = str(row.get("아이디",     "")).strip()
                t_subj    = str(row.get("과목",       "")).strip()
                t_sheet   = str(row.get("성찰시트ID", "")).strip()
                roster_id = str(row.get("명단시트ID", "")).strip()

                if not t_sheet:
                    continue
                if subject_key and t_subj and subject_key != t_subj:
                    continue
                if not roster_id:
                    continue

                if t_sheet in already_written:
                    continue

                for r in _cached_teacher_roster(roster_id):
                    if str(r.get("학번", "")).strip() == num:
                        _write_reflection_to_teacher_sheet(t_sheet, sheet_name, payload)
                        already_written.add(t_sheet)
                        break
            return

        # ── 학급 기반 교사설정 매칭 ───────────────────────────────────────────
        for row in teacher_rows:
            t_id    = str(row.get("아이디",     "")).strip()
            t_subj  = str(row.get("과목",       "")).strip()
            t_sheet = str(row.get("성찰시트ID", "")).strip()

            if not t_sheet:
                continue
            if subject_key and t_subj and subject_key != t_subj:
                continue

            t_grades  = [g.strip() for g in str(row.get("학년목록", "")).split(",") if g.strip()]
            t_classes = [c.strip() for c in str(row.get("반목록",   "")).split(",") if c.strip()]

            managed = any(
                f"{g}학년 {c}반" == student_class
                for g in t_grades for c in t_classes
            )
            if not managed:
                continue

            if t_sheet in already_written:
                continue

            _write_reflection_to_teacher_sheet(t_sheet, sheet_name, payload)
            already_written.add(t_sheet)

    except Exception as e:
        print(f"[reflection_utils] teacher routing error: {e}")


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
        now_str = datetime.datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
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

    # 일반인: 제출 불필요 (단, 수학 교사는 폼 표시)
    if user_type == "general":
        _is_teacher = False
        if student_id:
            try:
                from auth_utils import is_math_teacher
                _is_teacher = is_math_teacher(student_id)
            except Exception:
                pass
        if not _is_teacher:
            st.info("💡 일반인 사용자는 성찰 기록 제출이 필요하지 않습니다.")
            return

    # 미로그인 방어 처리 (정상 흐름에서는 발생하지 않아야 함)
    if not student_id:
        st.warning("📋 로그인 후 성찰 기록을 작성할 수 있습니다.")
        return

    # 사용자 정보 안내
    st.markdown(f"📋 **학번**: `{student_id}`　**이름**: **{student_name}**")

    # ── localStorage 자동저장 스크립트 주입 ──────────────────────────────────
    # 모바일에서 백그라운드 전환으로 세션이 끊겨도 입력 내용이 보존됩니다.
    _safe_sheet = sheet_name.replace("'", "\\'").replace("`", "\\`")
    _components.html(f"""
    <script>
    (function() {{
        const KEY = 'ml_refl__{_safe_sheet}__draft';

        function setReactValue(el, value) {{
            if (!value) return;
            var proto = el.tagName === 'TEXTAREA'
                ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
            var setter = Object.getOwnPropertyDescriptor(proto, 'value');
            if (setter && setter.set) {{
                setter.set.call(el, value);
                el.dispatchEvent(new Event('input', {{bubbles: true}}));
            }}
        }}

        function getInputs() {{
            return Array.from(window.parent.document.querySelectorAll(
                '[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input[type="text"]'
            ));
        }}

        function saveAll() {{
            var inputs = getInputs();
            if (!inputs.length) return;
            var data = inputs.map(function(el) {{ return el.value; }});
            if (data.some(function(v) {{ return v && v.trim(); }})) {{
                try {{ localStorage.setItem(KEY, JSON.stringify(data)); }} catch(e) {{}}
            }}
        }}

        var restored = false;
        function tryRestore() {{
            if (restored) return;
            var saved;
            try {{ saved = localStorage.getItem(KEY); }} catch(e) {{ return; }}
            if (!saved) return;
            var data;
            try {{ data = JSON.parse(saved); }} catch(e) {{ return; }}
            var inputs = getInputs();
            if (!inputs.length) return;
            restored = true;
            inputs.forEach(function(el, i) {{
                if (data[i]) setReactValue(el, data[i]);
            }});
        }}

        // DOM 변화 감지 → 복원 시도
        var startTime = Date.now();
        var obs = new MutationObserver(function() {{
            tryRestore();
            if (restored || Date.now() - startTime > 8000) obs.disconnect();
        }});
        obs.observe(window.parent.document.body, {{childList: true, subtree: true}});

        // 입력 이벤트마다 저장
        window.parent.document.addEventListener('input', function(e) {{
            if (e.target.matches('textarea, input[type="text"]')) {{
                setTimeout(saveAll, 200);
            }}
        }}, true);

        // 30초마다 자동저장
        setInterval(saveAll, 30000);
    }})();
    </script>
    """, height=0)

    # ── 개별 위젯 (st.form 대신 session_state 키 사용) ─────────────────────
    # 이렇게 하면 같은 세션 내 rerun이 일어나도 입력 내용이 유지됩니다.
    values: dict = {}
    for q in questions:
        qtype = q.get("type", "text_input")
        _wkey = f"_refl_{sheet_name}_{q.get('key', '')}"
        if qtype == "markdown":
            st.markdown(q["text"])
        elif qtype == "text_input":
            values[q["key"]] = st.text_input(
                q["label"],
                placeholder=q.get("placeholder", ""),
                key=_wkey,
            )
        elif qtype == "text_area":
            values[q["key"]] = st.text_area(
                q["label"],
                height=q.get("height", 80),
                placeholder=q.get("placeholder", ""),
                key=_wkey,
            )

    submitted = st.button(
        "📤 제출하기", use_container_width=True, type="primary",
        key=f"_refl_submit_{sheet_name}",
    )

    if submitted:
        payload = {
            "sheet":     sheet_name,
            "timestamp": datetime.datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S"),
            "학번":      _short_id,
            "이름":      student_name,
            **values,
        }
        try:
            resp = requests.post(gas_url, json=payload, timeout=60)
            if resp.status_code == 200:
                st.success(f"✅ {student_name}님의 기록이 제출되었습니다!")
                st.balloons()
                _log_reflection_submission(sheet_name, _subject, _short_id, student_name)
                # 담당 교사의 구글 시트에도 기록 (실패해도 학생에게는 알리지 않음)
                import threading
                threading.Thread(
                    target=_route_reflection_to_teachers,
                    args=(sheet_name, gas_url, payload, _short_id),
                    daemon=True,
                ).start()
                # localStorage 초안 삭제
                _components.html(f"""
                <script>
                try {{ localStorage.removeItem('ml_refl__{_safe_sheet}__draft'); }} catch(e) {{}}
                </script>
                """, height=0)
                # 제출 후 위젯 값 초기화
                for _q in questions:
                    _k = f"_refl_{sheet_name}_{_q.get('key', '')}"
                    st.session_state.pop(_k, None)
            else:
                st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
        except Exception as exc:
            st.error(f"네트워크 오류: {exc}")
