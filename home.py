# home.py
import streamlit as st
from pathlib import Path
import importlib.util
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any
import streamlit.components.v1 as components  # 임베드용
import urllib.parse
from functools import lru_cache
import smtplib
import html as _html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta
import time
import threading

_KST = timezone(timedelta(hours=9))  # 한국 표준시 (UTC+9)

# 인증 모듈
import auth_utils as _auth_utils

from auth_utils import (
    authenticate, register_student, register_general,
    check_password_policy, is_id_taken, is_student_num_taken,
    ALL_SUBJECTS as _AUTH_SUBJECTS,
)

@lru_cache(maxsize=256)
def _load_module_cached(path_str: str, mtime: float):
    return load_module_from_path(Path(path_str))

# ─────────────────────────────────────────────────────────────────────────────
# Fallback: utils.keep_scroll이 없을 때 최소 구현
try:
    from utils import keep_scroll
except Exception:
    def keep_scroll(key: str = "default"):
        components.html(f"""
        <script>
        (function(){{
          const KEY = 'st_scroll::' + '{'{'}key{'}'}' + '::' + location.pathname + location.search;
          function restore() {{
            const y = sessionStorage.getItem(KEY);
            if (y !== null) {{
              window.scrollTo(0, parseFloat(y));
            }}
          }}
          restore(); setTimeout(restore, 50); setTimeout(restore, 250);
          let t=false;
          window.addEventListener('scroll', function(){{
            if(!t){{ requestAnimationFrame(function(){{ sessionStorage.setItem(KEY, window.scrollY); t=false; }}); t=true; }}
          }});
          setInterval(function(){{ sessionStorage.setItem(KEY, window.scrollY); }}, 500);
        }})();
        </script>
        """, height=0)

# 외부 문서 임베드 헬퍼
def embed_iframe(src: str, height: int = 600, scrolling: bool = True):
    """외부 페이지/문서를 iframe으로 임베드"""
    components.iframe(src, height=height, scrolling=scrolling)


def embed_pdf(src: str, height: int = 800):
    """
    src가 아래 중 하나면 그대로:
      - data: (base64 data URI)
      - docs.google.com/gview?embedded=true ...
      - drive.google.com/file/.../preview
    그 외 .pdf URL이면 gview로 감싸서 iframe 임베드
    """
    url = src
    s = src.lower()
    if not (s.startswith("data:") or "gview?embedded=true" in s or "drive.google.com/file" in s):
        if s.endswith(".pdf"):
            url = "https://docs.google.com/gview?embedded=true&url=" + urllib.parse.quote(src, safe="")
    components.html(
        f'<iframe src="{url}" style="width:100%; height:{height}px; border:0;" allowfullscreen></iframe>',
        height=height
    )

def to_youtube_embed(src: str) -> str:
    """YouTube watch/shorts/youtu.be/playlist 링크를 embed용으로 정규화"""
    try:
        u = urllib.parse.urlparse(src.strip())
        q = urllib.parse.parse_qs(u.query)

        # 이미 embed면 그대로
        if "/embed/" in u.path:
            return src

        # 플레이리스트
        if "list" in q and ("watch" in u.path or "playlist" in u.path):
            return f"https://www.youtube-nocookie.com/embed/videoseries?list={q['list'][0]}"

        # shorts
        if "/shorts/" in u.path:
            vid = u.path.split("/shorts/")[1].split("/")[0]
        # youtu.be 단축
        elif u.netloc.endswith("youtu.be"):
            vid = u.path.lstrip("/")
        else:
            vid = q.get("v", [""])[0]

        base = f"https://www.youtube-nocookie.com/embed/{vid}"
        # 주소에 start=초 가 있었다면 유지(선택)
        if "start" in q:
            return base + "?start=" + q["start"][0]
        return base
    except Exception:
        return src

# ─────────────────────────────────────────────────────────────────────────────
# 전역 설정
st.set_page_config(
    page_title="Mathlab",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

SHOW_MINI_IN_SIDEBAR = False

# 교과 카테고리 정의(폴더명 ↔ 표시명)
SUBJECTS = {
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

# 이전 교육과정 자료도 로그인 사용자에게 공개 (관리자 모드 전용 제한 해제)
HIDDEN_SUBJECTS: set = set()

# home.py와 같은 디렉터리 기준
ACTIVITIES_ROOT = Path(__file__).parent / "activities"

# ─────────────────────────────────────────────────────────────────────────────
# 데이터 모델
@dataclass
class Activity:
    subject_key: str
    slug: str
    title: str
    description: str
    render: Callable[[], None]
    order: int = 10_000_000  # 기본값(크게) → 지정 없으면 뒤로 밀림
    hidden: bool = False

# ─────────────────────────────────────────────────────────────────────────────
# 유틸: 동적 모듈 로딩
# --- 기존 load_module_from_path 를 아래 버전으로 교체 ---
def load_module_from_path(py_path: Path):
    spec = importlib.util.spec_from_file_location(py_path.stem, py_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"spec_from_file_location failed: {py_path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)  # type: ignore
    except SyntaxError as e:
        # 어떤 파일 몇 번째 줄에서 문법오류인지 정확히 보여줌
        raise SyntaxError(f"[{py_path}] {e.msg} (line {e.lineno}, col {e.offset})") from e
    except Exception as e:
        # 다른 예외도 파일경로를 붙여서 재전파
        raise RuntimeError(f"Error while importing {py_path}: {e}") from e
    return module


# lessons/_units.py 로더
def load_units(subject_key: str) -> Dict[str, Any]:
    """
    activities/<subject>/lessons/_units.py 안의 UNITS 사전을 로드.
    형식:
    UNITS = {
      "unit_key": {
        "label": "단원명",
        "items": [
          {"type":"gslides","title":"...","src":"임베드URL","height":480},
          {"type":"gsheet","title":"...","src":"임베드URL","height":700},
          {"type":"canva","title":"...","src":"임베드URL","height":600},
          {"type":"url","title":"...","src":"https://..."},
          {"type":"activity","title":"...","subject":"probability","slug":"binomial_simulator"},
        ],
      },
      ...
    }
    """
    units_py = ACTIVITIES_ROOT / subject_key / "lessons" / "_units.py"
    if not units_py.exists():
        return {}
    mod = load_module_from_path(units_py)
    return getattr(mod, "UNITS", {}) or {}

def load_activity_order(subject_key: str) -> List[str]:
    """activities/<subject>/_order.py 의 ORDER 리스트를 읽어옵니다."""
    p = ACTIVITIES_ROOT / subject_key / "_order.py"
    if not p.exists():
        return []
    m = load_module_from_path(p)
    return list(getattr(m, "ORDER", []) or [])

def load_curriculum(subject_key: str) -> Optional[List[Dict[str, Any]]]:
    """activities/<subject>/lessons/_units.py 의 CURRICULUM(list)을 읽습니다."""
    units_py = ACTIVITIES_ROOT / subject_key / "lessons" / "_units.py"
    if not units_py.exists():
        return None
    mod = load_module_from_path(units_py)
    cur = getattr(mod, "CURRICULUM", None)
    if isinstance(cur, list) and cur:
        return cur
    return None

def _has_lessons(subject_key: str) -> bool:
    """해당 교과에 lessons/_units.py가 있는지 확인."""
    return (ACTIVITIES_ROOT / subject_key / "lessons" / "_units.py").exists()

def _inject_subject_styles():
    """교과 메인에서 쓸 '수업 카드' 전용 스타일을 주입."""
    st.markdown(
        """
        <style>
          .lesson-card {
            background: rgba(99,102,241,0.08);
            border: 1px solid rgba(99,102,241,0.28);
            border-radius: 12px;
            padding: 14px 16px;
            margin: 0.25rem 0 1rem 0;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
          }
          .lesson-card h4 { margin: 0 0 .35rem 0; font-weight: 700; color: rgba(255,255,255,0.93); }
          .lesson-card p  { margin: .15rem 0 .5rem 0; color: rgba(255,255,255,0.52); }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _lessons_top_nav(subject_key: str):
    """수업 페이지 상단(제목 바로 아래)에 들어갈 네비게이션 버튼들."""
    cols = st.columns([1, 1], gap="small")
    with cols[0]:
        if st.button("← 교과 메인", type="secondary", use_container_width=True, key=f"lessons_top_back_{subject_key}"):
            set_route("subject", subject=subject_key); _do_rerun()
    with cols[1]:
        if st.button("🏠 홈", type="secondary", use_container_width=True, key=f"lessons_top_home_{subject_key}"):
            set_route("home"); _do_rerun()

# 🔎 커리큘럼 트리에서 key로 경로(대/중/소 인덱스)를 찾는 헬퍼
def _find_curriculum_path(curriculum: List[Dict[str, Any]], key: str) -> Optional[tuple[int, Optional[int], Optional[int]]]:
    def ch(node): return node.get("children", []) if isinstance(node, dict) else []
    for i, maj in enumerate(curriculum):
        if maj.get("key") == key:
            return (i, None, None)
        mids = ch(maj)
        for j, mid in enumerate(mids):
            if mid.get("key") == key:
                return (i, j, None)
            mins = ch(mid)
            for k, mnr in enumerate(mins):
                if mnr.get("key") == key:
                    return (i, j, k)
    return None

# ─────────────────────────────────────────────────────────────────────────────
# Streamlit 버전 호환 라우팅 유틸
def _qp_get() -> Dict[str, List[str]]:
    """
    Query params를 버전 상관없이 표준화된 dict[str, list[str]]로 반환.
    - 최신: st.query_params -> dict[str, str] 또는 dict[str, list[str]]
    - 구버전: st.experimental_get_query_params()
    """
    try:
        qp: Any = st.query_params  # 최신 API
        norm: Dict[str, List[str]] = {}
        for k, v in dict(qp).items():
            if isinstance(v, list):
                norm[k] = v
            else:
                norm[k] = [v]
        return norm
    except Exception:
        try:
            return st.experimental_get_query_params()  # type: ignore[attr-defined]
        except Exception:
            return {}

def _qp_set(params: Dict[str, Any]) -> None:
    """
    Query params 설정(버전 호환). 값은 str 또는 list[str] 허용.
    """
    normalized = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, list):
            normalized[k] = [str(x) for x in v]
        else:
            normalized[k] = str(v)

    try:
        st.query_params.clear()
        st.query_params.update(normalized)
    except Exception:
        st.experimental_set_query_params(**normalized)  # type: ignore[attr-defined]

def _do_rerun():
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()  # type: ignore[attr-defined]


# 페이드인 CSS (주요 전환 후 새 화면에 적용)
_PAGE_FADE_IN_CSS = """<style>
[data-testid="stMainBlockContainer"] {
    animation: mlPageEnter 0.22s ease-out !important;
}
@keyframes mlPageEnter {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0);   }
}
</style>"""


def _show_page_transition():
    """로그인·로그아웃 등 주요 화면 전환 시 잔상 방지.
    _do_rerun() 바로 직전에 호출합니다.
    - JS로 브라우저에 즉시 오버레이를 그려 이전 화면을 가림
    - 다음 렌더링 시 fade-in 플래그 설정
    """
    components.html(
        """
        <script>
        (function(){
            var ov = document.createElement('div');
            ov.style.cssText = 'position:fixed;inset:0;background:#0f172a;z-index:2147483647;pointer-events:none;';
            document.body.appendChild(ov);
        })();
        </script>
        """,
        height=0,
    )
    st.session_state["_page_fade_in"] = True

def _is_dev_mode() -> bool:
    """관리자 모드 여부를 세션 상태에서 읽습니다."""
    return st.session_state.get("_dev_mode", False)

# OT 자료 — 관리자 모드에서만 접근 가능
_OT_CANVA: Dict[str, str] = {
    "common":          "https://www.canva.com/design/DAHC4prloOs/iLjYVxFI-b-VKCWRB3rE9A/view?embed",
    "common2":         "https://www.canva.com/design/DAHC4prloOs/iLjYVxFI-b-VKCWRB3rE9A/view?embed",
    "algebra":         "",   # TODO: 대수 OT Canva URL
    "calculus1":       "",   # TODO: 미적분1 OT Canva URL
    "calculus2":       "",   # TODO: 미적분2 OT Canva URL
    "probability_new": "https://www.canva.com/design/DAHC5FC0x7g/wVBeRL2qrRPuWLC9BszvjQ/view?embed",
    "economics_math":  "",   # TODO: 경제수학 OT Canva URL
}

def _is_ot_mode() -> bool:
    """OT 모드: 관리자 모드일 때만 허용합니다."""
    return _is_dev_mode()


def _get_login_allowed_subjects() -> Optional[set]:
    """로그인 기반 허용 교과 집합을 반환합니다.
    None = 제한 없음(관리자 또는 미설정), set = 허용 key 목록."""
    if _is_dev_mode():
        return None
    if st.session_state.get("_user_type") == "general":
        raw = st.session_state.get("_login_allowed_subjects", set())
        if raw is None:
            return set()
        if isinstance(raw, set):
            return raw
        if isinstance(raw, (list, tuple)):
            return {str(v).strip() for v in raw if str(v).strip()}
        return set()
    return st.session_state.get("_login_allowed_subjects", None)


def _get_login_allowed_units(subject_key: str) -> Optional[set[str]]:
    """로그인 기반 수업(unit) 허용 키 집합을 반환합니다.
    None = 제한 없음, set = 허용 unit key 목록.

    현재 정책상 일반인 + 영재 교과에만 적용합니다.
    """
    if _is_dev_mode():
        return None
    if st.session_state.get("_user_type") != "general":
        return None
    if subject_key != "gifted":
        return None

    raw = st.session_state.get("_login_allowed_lessons", {})
    if not isinstance(raw, dict):
        return set()
    units = raw.get(subject_key, set())
    if isinstance(units, set):
        return units
    if isinstance(units, (list, tuple)):
        return {str(u).strip() for u in units if str(u).strip()}
    return set()


def _refresh_current_user_permissions() -> None:
    """현재 로그인 사용자의 최신 권한을 시트 기준으로 세션에 반영합니다."""
    user_type = st.session_state.get("_user_type", "")
    user_id = st.session_state.get("_user_id", "")
    if not user_type or not user_id:
        return

    get_snapshot = getattr(_auth_utils, "get_user_permission_snapshot", None)
    if not callable(get_snapshot):
        return

    snap = get_snapshot(user_type, user_id)
    if not snap:
        return

    st.session_state["_user_name"] = snap.get("name", st.session_state.get("_user_name", ""))
    st.session_state["_login_allowed_subjects"] = snap.get("allowed_subjects")
    st.session_state["_login_allowed_lessons"] = snap.get("allowed_lessons")


def _filter_curriculum_by_allowed_units(curriculum: List[Dict[str, Any]],
                                        allowed_units: set[str]) -> List[Dict[str, Any]]:
    """허용 unit key에 맞춰 CURRICULUM 트리를 필터링합니다."""
    def _walk(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for node in nodes:
            children = node.get("children", []) if isinstance(node, dict) else []
            filtered_children = _walk(children) if children else []
            key = str(node.get("key", "")).strip() if isinstance(node, dict) else ""
            include = (key in allowed_units) or bool(filtered_children)
            if include and isinstance(node, dict):
                new_node = dict(node)
                if "children" in new_node:
                    new_node["children"] = filtered_children
                out.append(new_node)
        return out

    return _walk(curriculum)


def _filter_units_by_allowed(units_dict: Dict[str, Any],
                             allowed_units: set[str]) -> Dict[str, Any]:
    """허용 unit key에 맞춰 평면형 UNITS를 필터링합니다."""
    return {k: v for k, v in units_dict.items() if k in allowed_units}


# ─────────────────────────────────────────────────────────────────────────────
# 로그인 알림 이메일
def _find_teacher_emails_for_student(student_num: str) -> list[str]:
    """학번으로 담당 교사의 이메일 목록을 반환합니다.

    1. 수강생명단에서 학번 → 반 조회
    2. 교사설정에서 해당 반을 담당하는 교사 이메일 수집
    """
    try:
        from auth_utils import (
            _get_users_spreadsheet_id,
            _cached_roster,
            _cached_teacher_settings,
            _cached_teacher_roster,
            TEACHER_ROSTER_WS,
        )
        users_sheet_id = _get_users_spreadsheet_id()
        num = student_num.strip()

        # 학번→반: 수강생명단 우선, 없으면 교사별 명단 검색
        student_class = ""
        for r in _cached_roster(users_sheet_id):
            if str(r.get("학번", "")).strip() == num:
                student_class = str(r.get("반", "") or r.get("학급", "")).strip()
                break

        teacher_rows = _cached_teacher_settings(users_sheet_id)

        # 반 정보가 없으면 교사별 수강생명단에서 직접 학번 검색
        if not student_class:
            emails: list[str] = []
            seen_emails: set[str] = set()
            for row in teacher_rows:
                roster_id = str(row.get("명단시트ID", "")).strip()
                email     = str(row.get("이메일", "")).strip()
                if not roster_id or not email or email in seen_emails:
                    continue
                for r in _cached_teacher_roster(roster_id):
                    if str(r.get("학번", "")).strip() == num:
                        emails.append(email)
                        seen_emails.add(email)
                        break
            return emails

        # 반 정보가 있으면 교사설정의 담당 학급과 비교
        emails = []
        seen_emails: set[str] = set()
        for row in teacher_rows:
            email = str(row.get("이메일", "")).strip()
            if not email or email in seen_emails:
                continue
            grades  = [g.strip() for g in str(row.get("학년목록", "")).split(",") if g.strip()]
            classes = [c.strip() for c in str(row.get("반목록",   "")).split(",") if c.strip()]
            managed = {f"{g}학년 {c}반" for g in grades for c in classes}
            if student_class in managed:
                emails.append(email)
                seen_emails.add(email)
        return emails
    except Exception:
        return []


def _send_register_notify_email(user_type: str, name: str, user_id: str,
                                extra: str = "",
                                student_num: str = "") -> None:
    """신규 가입 신청 시 관리자 및 담당 교사에게 이메일로 알립니다."""
    try:
        email_secrets = st.secrets.get("email", {})
        sender   = str(email_secrets.get("sender", ""))
        password = str(email_secrets.get("password", ""))
        if not sender or not password:
            return
        type_label = "학생" if user_type == "student" else "일반인"
        subject_line = f"[MathLab] 신규 가입 신청 – {type_label} {name}({user_id})"
        now_str  = datetime.now(_KST).strftime("%Y년 %m월 %d일 %H:%M")
        body     = (
            f"<h3>신규 가입 신청 알림</h3>"
            f"<p>유형: {type_label}<br>이름: {_html.escape(name)}<br>"
            f"아이디: {_html.escape(user_id)}<br>{_html.escape(extra)}<br>"
            f"신청 일시: {now_str}</p>"
            f"<p><a href='https://mathematicslab.streamlit.app/'>관리자 페이지</a>에서 승인하세요.</p>"
        )

        # 수신자: 관리자 + 담당 교사(학생 가입 시)
        receivers: list[str] = [_FEEDBACK_RECEIVER]
        if user_type == "student" and student_num:
            teacher_emails = _find_teacher_emails_for_student(student_num)
            for e in teacher_emails:
                if e and e not in receivers:
                    receivers.append(e)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject_line
        msg["From"]    = sender
        msg["To"]      = ", ".join(receivers)
        msg.attach(MIMEText(body, "html", "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as srv:
            srv.login(sender, password)
            srv.sendmail(sender, receivers, msg.as_string())
    except Exception:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# 로그인 / 회원가입 뷰
def _inject_login_style(hide_sidebar: bool = True):
    """MathLab 로그인 화면 전용 다크 그리드 스타일을 주입합니다."""
    sidebar_css = """
    section[data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    .stMainBlockContainer, .block-container { margin-left: auto !important; }
    """ if hide_sidebar else ""
    st.markdown("""
    <style>
    """ + sidebar_css + """
    .stApp {
        background-color: #0f172a !important;
        background-image:
            linear-gradient(rgba(99, 102, 241, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99, 102, 241, 0.08) 1px, transparent 1px) !important;
        background-size: 50px 50px !important;
    }
    .stApp > .main { background: transparent !important; }
    header[data-testid="stHeader"], .stDeployButton, footer { display: none !important; }

    /* 세로 중앙 정렬 */
    [data-testid="stMain"] {
        display: flex !important;
        align-items: center !important;
        min-height: 100vh !important;
    }
    /* Streamlit 기본 상하 패딩 축소 → 한 화면에 들어오게 */
    .block-container, [data-testid="stMainBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        width: 100% !important;
    }

    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 20px 24px 16px !important;
        box-shadow:
            0 4px 6px rgba(0, 0, 0, 0.3),
            0 20px 60px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.06),
            0 0 0 1px rgba(139, 92, 246, 0.08) !important;
    }

    .stApp p, .stApp label, .stApp span, .stApp div, .stApp li {
        color: rgba(255, 255, 255, 0.75) !important;
    }
    /* 사이드바(로컬 디버그 패널)는 라이트 테마 색상 유지 */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span:not(.st-emotion-cache-hidden),
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] caption,
    section[data-testid="stSidebar"] small {
        color: unset !important;
    }

    .stTextInput > div > div > input,
    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.85) !important;
        caret-color: #a78bfa !important;
    }
    .stTextInput > div > div > input::placeholder { color: rgba(255, 255, 255, 0.25) !important; }
    .stTextInput > div > div > input:focus {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.12) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    .stTextInput label {
        color: rgba(255, 255, 255, 0.55) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
    }

    .stFormSubmitButton > button, .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        letter-spacing: 2px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.35), 0 0 0 1px rgba(139, 92, 246, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stFormSubmitButton > button:hover, .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 28px rgba(124, 58, 237, 0.45), 0 0 0 1px rgba(139, 92, 246, 0.3) !important;
    }

    /* 입력 필드 간 세로 여백 축소 */
    .stTextInput { margin-bottom: 0 !important; }
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] { gap: 0.3rem !important; }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: rgba(255, 255, 255, 0.35) !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 8px 20px !important;
    }
    .stTabs [aria-selected="true"] {
        color: #a78bfa !important;
        border-bottom: 2px solid #a78bfa !important;
    }
    .stTabs [data-baseweb="tab-panel"] { background: transparent !important; }

    .stAlert {
        background: rgba(239, 68, 68, 0.12) !important;
        border: 1px solid rgba(239, 68, 68, 0.25) !important;
        border-radius: 10px !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.03); }
    ::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 3px; }

    /* 로컬 디버그 패널 — container 전체를 하나의 박스로 */
    [data-testid="stVerticalBlock"]:has(> div > .stMarkdown .debug-panel-header) {
        margin-top: 2.2rem;
        background: rgba(251, 191, 36, 0.07) !important;
        border: 1px solid rgba(251, 191, 36, 0.35) !important;
        border-radius: 12px !important;
        padding: 10px 14px 12px !important;
    }
    .debug-panel-header {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        color: rgba(251, 191, 36, 0.80) !important;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    </style>
    """, unsafe_allow_html=True)


def _render_login_header():
    """MathLab 로그인 화면 헤더(로고 + 배경 장식)를 렌더링합니다."""
    st.markdown("""
    <style>
    .math-bg-symbols {
        position: fixed; top: 0; left: 0;
        width: 100vw; height: 100vh;
        pointer-events: none; z-index: 0; overflow: hidden;
    }
    .math-sym {
        position: absolute;
        color: rgba(139, 92, 246, 0.12);
        font-family: 'Times New Roman', Georgia, serif;
        font-style: italic; user-select: none;
    }
    .axis-deco {
        position: fixed; bottom: 36px; left: 36px;
        opacity: 0.12; z-index: 0; pointer-events: none;
    }
    .center-glow {
        position: fixed;
        width: 700px; height: 700px;
        background: radial-gradient(circle, rgba(139,92,246,0.07) 0%, transparent 65%);
        border-radius: 50%;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        pointer-events: none; z-index: 0;
    }
    .mathlab-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }
    .mathlab-logo-svg {
        width: 81px; height: 81px; flex-shrink: 0;
        filter: drop-shadow(0 0 18px rgba(139,92,246,0.65));
    }
    .mathlab-logo-title {
        font-size: 4.2rem; font-weight: 800; letter-spacing: 8px;
        background: linear-gradient(135deg, #c4b5fd 0%, #a78bfa 40%, #818cf8 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; line-height: 1;
        margin: 0;
    }
    </style>

    <div class="center-glow"></div>

    <div class="math-bg-symbols">
        <span class="math-sym" style="top:7%;  left:5%;  font-size:2.2rem; transform:rotate(-15deg);">∑</span>
        <span class="math-sym" style="top:11%; left:18%; font-size:1rem;">f(x) = ax² + bx + c</span>
        <span class="math-sym" style="top:16%; right:7%; font-size:2.5rem; transform:rotate(10deg);">∫</span>
        <span class="math-sym" style="top:26%; right:17%; font-size:1rem;">lim<sub>x→0</sub></span>
        <span class="math-sym" style="top:4%;  right:30%; font-size:1.8rem;">π</span>
        <span class="math-sym" style="bottom:20%; left:4%;  font-size:1.4rem; transform:rotate(-5deg);">√x</span>
        <span class="math-sym" style="bottom:28%; left:16%; font-size:0.95rem;">e<sup>iπ</sup> + 1 = 0</span>
        <span class="math-sym" style="bottom:23%; right:5%; font-size:1.8rem; transform:rotate(8deg);">Δ</span>
        <span class="math-sym" style="bottom:11%; right:20%; font-size:1rem;">∞</span>
        <span class="math-sym" style="top:40%; left:3%;  font-size:2rem; transform:rotate(-8deg);">θ</span>
        <span class="math-sym" style="top:53%; right:3%; font-size:1.6rem; transform:rotate(5deg);">λ</span>
        <span class="math-sym" style="top:66%; left:9%;  font-size:0.9rem;">sin²θ + cos²θ = 1</span>
    </div>

    <div class="mathlab-header">
      <svg class="mathlab-logo-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
        <defs>
          <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#1e1b4b"/><stop offset="100%" stop-color="#0f172a"/>
          </linearGradient>
          <linearGradient id="strokeGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#c4b5fd"/><stop offset="100%" stop-color="#818cf8"/>
          </linearGradient>
          <linearGradient id="liquidGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.75"/>
            <stop offset="100%" stop-color="#4338ca" stop-opacity="0.95"/>
          </linearGradient>
          <linearGradient id="liquidShine" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#a78bfa" stop-opacity="0.4"/>
            <stop offset="50%" stop-color="#c4b5fd" stop-opacity="0.15"/>
            <stop offset="100%" stop-color="#818cf8" stop-opacity="0.3"/>
          </linearGradient>
          <radialGradient id="flaskGlow" cx="50%" cy="60%" r="50%">
            <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.2"/>
            <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
          </radialGradient>
          <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="3.5" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
          <filter id="strongGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="5" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
          <clipPath id="bgClip"><rect x="0" y="0" width="200" height="200" rx="44"/></clipPath>
          <clipPath id="flaskBodyClip">
            <path d="M 82 82 L 37 162 Q 28 190 62 190 L 138 190 Q 172 190 163 162 L 118 82 Z"/>
          </clipPath>
        </defs>
        <rect x="0" y="0" width="200" height="200" rx="44" fill="url(#bgGrad)"/>
        <g clip-path="url(#bgClip)" stroke="rgba(99,102,241,0.11)" stroke-width="0.8" fill="none">
          <line x1="50" y1="0" x2="50" y2="200"/><line x1="100" y1="0" x2="100" y2="200"/>
          <line x1="150" y1="0" x2="150" y2="200"/><line x1="0" y1="50" x2="200" y2="50"/>
          <line x1="0" y1="100" x2="200" y2="100"/><line x1="0" y1="150" x2="200" y2="150"/>
        </g>
        <ellipse cx="100" cy="145" rx="62" ry="38" fill="rgba(124,58,237,0.10)" filter="url(#strongGlow)"/>
        <text x="14" y="46" font-family="Times New Roman,serif" font-size="20" fill="#818cf8" opacity="0.30" font-style="italic">∑</text>
        <text x="158" y="45" font-family="Times New Roman,serif" font-size="20" fill="#a78bfa" opacity="0.30" font-style="italic">π</text>
        <text x="12" y="185" font-family="Times New Roman,serif" font-size="14" fill="#818cf8" opacity="0.22" font-style="italic">∞</text>
        <text x="165" y="186" font-family="Times New Roman,serif" font-size="16" fill="#a78bfa" opacity="0.22" font-style="italic">Δ</text>
        <rect x="82" y="14" width="36" height="68" rx="6" fill="rgba(139,92,246,0.07)" stroke="url(#strokeGrad)" stroke-width="2.8"/>
        <rect x="78" y="9" width="44" height="13" rx="6.5" fill="url(#strokeGrad)"/>
        <line x1="88" y1="16" x2="88" y2="80" stroke="rgba(255,255,255,0.12)" stroke-width="1.5" stroke-linecap="round"/>
        <path d="M 82 82 L 37 162 Q 28 190 62 190 L 138 190 Q 172 190 163 162 L 118 82 Z" fill="rgba(139,92,246,0.07)" stroke="url(#strokeGrad)" stroke-width="2.8" stroke-linejoin="round"/>
        <path d="M 82 82 L 37 162 Q 28 190 62 190 L 138 190 Q 172 190 163 162 L 118 82 Z" fill="url(#flaskGlow)"/>
        <rect x="0" y="142" width="200" height="55" fill="url(#liquidGrad)" clip-path="url(#flaskBodyClip)"/>
        <rect x="0" y="142" width="200" height="18" fill="url(#liquidShine)" clip-path="url(#flaskBodyClip)"/>
        <path d="M 36 142 Q 48 132 60 142 Q 72 152 84 142 Q 96 132 108 142 Q 120 152 132 142 Q 144 132 156 142 Q 161 147 164 143" fill="none" stroke="#ddd6fe" stroke-width="2.4" stroke-linecap="round" filter="url(#softGlow)" clip-path="url(#flaskBodyClip)"/>
        <circle cx="68" cy="162" r="5.5" fill="#a78bfa" opacity="0.45"/>
        <circle cx="100" cy="172" r="3.8" fill="#818cf8" opacity="0.38"/>
        <circle cx="133" cy="160" r="4.5" fill="#a78bfa" opacity="0.40"/>
        <circle cx="82" cy="178" r="2.8" fill="#c4b5fd" opacity="0.32"/>
        <circle cx="118" cy="180" r="2.2" fill="#c4b5fd" opacity="0.28"/>
        <circle cx="58" cy="135" r="2.2" fill="#c4b5fd" opacity="0.28"/>
        <circle cx="77" cy="118" r="1.6" fill="#c4b5fd" opacity="0.20"/>
        <circle cx="112" cy="122" r="1.8" fill="#c4b5fd" opacity="0.22"/>
        <circle cx="138" cy="132" r="1.4" fill="#c4b5fd" opacity="0.18"/>
        <path d="M 90 85 L 52 155" stroke="rgba(255,255,255,0.10)" stroke-width="6" stroke-linecap="round" clip-path="url(#flaskBodyClip)"/>
        <line x1="111" y1="16" x2="111" y2="78" stroke="rgba(255,255,255,0.09)" stroke-width="4" stroke-linecap="round"/>
        <g opacity="0.18" transform="translate(148,138)">
          <line x1="0" y1="34" x2="36" y2="34" stroke="#8b5cf6" stroke-width="1.2"/>
          <line x1="0" y1="0" x2="0" y2="34" stroke="#8b5cf6" stroke-width="1.2"/>
          <polyline points="3,28 10,18 17,23 24,10 33,4" stroke="#a78bfa" stroke-width="1.2" fill="none"/>
          <polygon points="36,34 32,31 32,37" fill="#8b5cf6"/>
          <polygon points="0,0 -3,6 3,6" fill="#8b5cf6"/>
        </g>
      </svg>
      <div class="mathlab-logo-title">MathLab</div>
    </div>
    """, unsafe_allow_html=True)


def login_view():
    """인증되지 않은 사용자에게 보이는 로그인 화면."""
    _inject_sidebar_nav_visibility(dev=False)
    try:
        _is_debug = bool(st.secrets.get("local_debug_mode", False))
    except Exception:
        _is_debug = False
    _inject_login_style(hide_sidebar=True)
    # 로그아웃 후 돌아올 때 부드러운 등장
    if st.session_state.pop("_page_fade_in", False):
        st.markdown(_PAGE_FADE_IN_CSS, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        _render_login_header()

        # ── 탭 선택 버튼 (session_state로 관리 → 라디오 클릭 시 탭 초기화 방지) ──
        if "_login_active_tab" not in st.session_state:
            st.session_state["_login_active_tab"] = "login"
        _tc1, _tc2 = st.columns(2)
        with _tc1:
            if st.button("🔐  로그인", use_container_width=True, key="_tab_btn_login",
                         type="primary" if st.session_state["_login_active_tab"] == "login" else "secondary"):
                st.session_state["_login_active_tab"] = "login"
        with _tc2:
            if st.button("📝  회원가입", use_container_width=True, key="_tab_btn_reg",
                         type="primary" if st.session_state["_login_active_tab"] == "register" else "secondary"):
                st.session_state["_login_active_tab"] = "register"

        st.markdown("<hr style='margin:4px 0 10px; border:none; border-top:1px solid rgba(255,255,255,0.1);'>",
                    unsafe_allow_html=True)

        # ── 로그인 탭 ──────────────────────────────────────────────────
        if st.session_state["_login_active_tab"] == "login":
            ATTEMPT_KEY = "_login_attempts"
            if st.session_state.get(ATTEMPT_KEY, 0) >= 5:
                st.error(
                    "⛔ 로그인 시도 횟수(5회)를 초과했습니다. "
                    "브라우저를 새로고침 하거나 관리자에게 문의하세요."
                )
            else:
                with st.form("login_form", clear_on_submit=False):
                    uid = st.text_input("아이디", placeholder="아이디 입력")
                    pw  = st.text_input("비밀번호", type="password",
                                        placeholder="비밀번호 입력")
                    submitted = st.form_submit_button(
                        "로그인", use_container_width=True, type="primary"
                    )

                if submitted:
                    with st.spinner("인증 중..."):
                        result = authenticate(uid.strip(), pw)

                    if result is None:
                        cnt = st.session_state.get(ATTEMPT_KEY, 0) + 1
                        st.session_state[ATTEMPT_KEY] = cnt
                        remaining = 5 - cnt
                        st.error(
                            f"❌ 아이디 또는 비밀번호가 틀렸습니다. "
                            f"(남은 시도: {remaining}회)"
                        )
                    elif result.get("type") == "locked":
                        st.error(
                            "🔒 로그인 실패가 누적되어 계정이 잠겼습니다. "
                            "담당 교사에게 잠금 해제를 요청하세요."
                        )
                    elif result.get("type") == "pending":
                        st.warning(
                            "⏳ 가입 승인 대기 중인 계정입니다. "
                            "관리자 승인 후 로그인할 수 있습니다."
                        )
                    else:
                        # 로그인 성공
                        st.session_state["_authenticated"]       = True
                        st.session_state["_user_type"]           = result["type"]
                        st.session_state["_user_id"]             = result["id"]
                        st.session_state["_user_name"]           = result["name"]
                        st.session_state["_login_allowed_subjects"] = result["allowed_subjects"]
                        st.session_state["_login_allowed_lessons"] = result.get("allowed_lessons")
                        if result["type"] == "admin":
                            st.session_state["_dev_mode"] = True
                        st.session_state.pop(ATTEMPT_KEY, None)
                        _show_page_transition()  # 잔상 방지
                        _do_rerun()

            st.markdown(
                "<div style='text-align:center; margin-top:1rem; "
                "color:var(--secondary-text-color); font-size:.85rem;'>"
                "비밀번호를 잊으셨나요? 관리자에게 문의하세요.</div>",
                unsafe_allow_html=True,
            )

        # ── 회원가입 탭 ────────────────────────────────────────────────
        else:
            reg_type = st.radio(
                "가입 유형 선택",
                ["🎓 학생", "👤 일반인"],
                horizontal=True,
                key="reg_type_radio",
            )
            st.markdown("<hr style='margin:2px 0 6px; border:none; border-top:1px solid rgba(255,255,255,0.1);'>",
                        unsafe_allow_html=True)

            if reg_type == "🎓 학생":
                st.caption("학번과 이름 입력 시 아이디 자동 생성. 예) 학번 20200 → 아이디 202620200")
                with st.form("reg_student_form", clear_on_submit=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        s_num  = st.text_input("학번 *", placeholder="예: 20200", max_chars=10)
                    with c2:
                        s_name = st.text_input("이름 *", placeholder="예: 홍길동", max_chars=20)
                    c3, c4 = st.columns(2)
                    with c3:
                        s_pw1  = st.text_input("비밀번호 *", type="password", placeholder="8자 이상, 숫자 포함")
                    with c4:
                        s_pw2  = st.text_input("비밀번호 확인 *", type="password", placeholder="비밀번호 재입력")
                    sub_s = st.form_submit_button(
                        "학생 회원가입 신청", use_container_width=True,
                        type="primary",
                    )

                if sub_s:
                    errs = []
                    if not s_num.strip().isdigit():
                        errs.append("학번은 숫자만 입력하세요.")
                    if not s_name.strip():
                        errs.append("이름을 입력하세요.")
                    if s_pw1 != s_pw2:
                        errs.append("비밀번호가 일치하지 않습니다.")
                    errs += check_password_policy(s_pw1)
                    if errs:
                        for e in errs:
                            st.error(e)
                    else:
                        # 학번 첫 자리로 학년 자동 감지
                        grade = s_num.strip()[0] if s_num.strip() else "1"
                        with st.spinner("가입 신청 중..."):
                            ok, msg = register_student(
                                s_num.strip(), s_name.strip(), s_pw1, grade
                            )
                        if ok:
                            # 관리자 + 담당 교사 알림 이메일
                            _send_register_notify_email(
                                "student", s_name.strip(),
                                msg, f"학번: {s_num.strip()}",
                                student_num=s_num.strip(),
                            )
                            st.success(
                                f"✅ 가입 신청이 완료되었습니다!\n\n"
                                f"생성된 아이디: **{msg}**\n\n"
                                "관리자 승인 후 로그인할 수 있습니다."
                            )
                        else:
                            st.error(f"❌ {msg}")

            else:
                with st.form("reg_general_form", clear_on_submit=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        g_name = st.text_input("이름 *", placeholder="예: 홍길동", max_chars=20)
                    with c2:
                        g_id   = st.text_input("아이디 *", placeholder="영문·숫자·밑줄, 4~20자", max_chars=20)
                    c3, c4 = st.columns(2)
                    with c3:
                        g_pw1  = st.text_input("비밀번호 *", type="password", placeholder="8자 이상, 숫자 포함")
                    with c4:
                        g_pw2  = st.text_input("비밀번호 확인 *", type="password", placeholder="비밀번호 재입력")
                    g_purpose = st.text_area(
                        "사용 목적 *",
                        placeholder="예: 학부모 / 타교 교사 / 수학 관련 연구 등",
                        max_chars=200,
                        height=60,
                    )
                    sub_g = st.form_submit_button(
                        "일반인 회원가입 신청", use_container_width=True,
                        type="primary",
                    )

                if sub_g:
                    errs = []
                    if not g_name.strip():
                        errs.append("이름을 입력하세요.")
                    if not g_id.strip():
                        errs.append("아이디를 입력하세요.")
                    if g_pw1 != g_pw2:
                        errs.append("비밀번호가 일치하지 않습니다.")
                    errs += check_password_policy(g_pw1)
                    if not g_purpose.strip():
                        errs.append("사용 목적을 입력하세요.")
                    if errs:
                        for e in errs:
                            st.error(e)
                    else:
                        with st.spinner("가입 신청 중..."):
                            ok, msg = register_general(
                                g_name.strip(), g_id.strip(),
                                g_pw1, g_purpose.strip(),
                            )
                        if ok:
                            _send_register_notify_email(
                                "general", g_name.strip(), g_id.strip(),
                                f"목적: {g_purpose.strip()}"
                            )
                            st.success(
                                "✅ 가입 신청이 완료되었습니다!\n\n"
                                f"아이디: **{g_id.strip()}**\n\n"
                                "관리자 승인 후 로그인할 수 있습니다."
                            )
                        else:
                            st.error(f"❌ {msg}")

        # ── 로컬 디버그 패널 (화면 내 빠른 접속) ──────────────────────
        if _is_debug:
            _DEBUG_ROLES = {
                "🔧 관리자":     {"_authenticated": True, "_user_type": "admin",
                                "_user_id": "admin", "_user_name": "관리자",
                                "_dev_mode": True, "_login_allowed_subjects": None,
                                "_login_allowed_lessons": None},
                "🎓 학생":       {"_authenticated": True, "_user_type": "student",
                                "_user_id": "202601001", "_user_name": "테스트학생",
                                "_dev_mode": False, "_login_allowed_subjects": None,
                                "_login_allowed_lessons": None},
                "👤 일반인":     {"_authenticated": True, "_user_type": "general",
                                "_user_id": "test_general", "_user_name": "테스트일반인",
                                "_dev_mode": False, "_login_allowed_subjects": set(),
                                "_login_allowed_lessons": {"gifted": set()}},
            }
            with st.container():
                st.markdown('<div class="debug-panel-header">🐛 LOCAL DEBUG — 빠른 접속</div>',
                            unsafe_allow_html=True)
                _dc = st.columns(len(_DEBUG_ROLES))
                _CLEAR = ["_authenticated", "_user_type", "_user_id", "_user_name",
                          "_dev_mode", "_login_allowed_subjects",
                          "_login_allowed_lessons", "_visit_logged"]
                for _col, (_label, _data) in zip(_dc, _DEBUG_ROLES.items()):
                    with _col:
                        if st.button(_label, use_container_width=True, key=f"_dbg_{_label}"):
                            for _k in _CLEAR:
                                st.session_state.pop(_k, None)
                            st.session_state.update(_data)
                            _do_rerun()

def _get_subject_filter() -> Optional[str]:
    """URL 우회 토큰 방식은 제거됨. 항상 None(필터 없음)을 반환합니다."""
    return None

# ─────────────────────────────────────────────────────────────────────────────
# 활동 자동 탐색
_REGISTRY_CACHE: Dict[str, Any] = {}   # {"data": registry, "ts": float}
_REGISTRY_TTL = 30                      # 캐시 유효 시간(초)

def _clear_registry_cache() -> None:
    """activity 레지스트리 캐시를 무효화합니다."""
    _REGISTRY_CACHE.clear()

def discover_activities() -> Dict[str, List[Activity]]:
    now = time.monotonic()
    if _REGISTRY_CACHE.get("data") is not None and (now - _REGISTRY_CACHE.get("ts", 0.0)) < _REGISTRY_TTL:
        return _REGISTRY_CACHE["data"]  # type: ignore[return-value]

    registry: Dict[str, List[Activity]] = {k: [] for k in SUBJECTS.keys()}
    if not ACTIVITIES_ROOT.exists():
        return registry

    def add_from_dir(dir_path: Path, subject_key: str, slug_prefix: str = ""):
        # mini 폴더 여부 판정
        is_mini = (Path(dir_path).name == "mini") or slug_prefix.startswith("mini/")

        for py_file in dir_path.glob("*.py"):
            name = py_file.name
            if name.startswith("_") or name == "__init__.py":
                continue
            try:
                module = _load_module_cached(str(py_file), py_file.stat().st_mtime)
            except Exception as e:
                # 문제 파일을 사이드바/본문에 명확히 표시하고, 나머지 파일 로딩은 계속
                st.sidebar.error(f"❌ 활동 로딩 실패: {py_file.name}\n\n{e}")
                st.error(f"활동 로딩 실패: **{py_file}**\n\n```\n{e}\n```")
                continue
            
            meta = getattr(module, "META", {})
            title = meta.get("title") or py_file.stem.replace("_", " ").title()
            description = meta.get("description") or "활동 소개가 아직 없습니다."
            render_fn = getattr(module, "render", None)
            order = int(meta.get("order", 10_000_000))
            # 파일 단위 숨김도 지원
            is_hidden_file = bool(meta.get("hidden", False))
            hidden = (is_mini and not SHOW_MINI_IN_SIDEBAR) or is_hidden_file

            if callable(render_fn):
                registry[subject_key].append(
                    Activity(
                        subject_key=subject_key,
                        slug=(slug_prefix + py_file.stem),   # 예: "mini/dice_conditional_prob"
                        title=title,
                        description=description,
                        render=render_fn,
                        order=order,
                        hidden=hidden,                       # ← 추가
                    )
                )

    for subject_dir in ACTIVITIES_ROOT.iterdir():
        if not subject_dir.is_dir():
            continue
        subject_key = subject_dir.name
        if subject_key not in SUBJECTS:
            continue

        # 1) 과목 폴더 바로 아래
        add_from_dir(subject_dir, subject_key, slug_prefix="")
        # 2) 1단계 하위 폴더(lessons, __pycache__, '_' 시작 제외)
        HIDE_DIRS = {"lessons", "__pycache__"}  # ← mini 폴더도 숨김
        for subdir in subject_dir.iterdir():
            if not subdir.is_dir():
                continue
            if subdir.name in HIDE_DIRS or subdir.name.startswith("_"):
                continue
            add_from_dir(subdir, subject_key, slug_prefix=f"{subdir.name}/")

        # ---- 정렬: _order.py > META.order > 제목 ----
        desired = load_activity_order(subject_key)  # 리스트가 비어 있으면 무시
        rank = {slug: i for i, slug in enumerate(desired)}
        registry[subject_key].sort(
            key=lambda a: (rank.get(a.slug, 10_000_000), a.order, a.title)
        )

    _REGISTRY_CACHE["data"] = registry
    _REGISTRY_CACHE["ts"]   = time.monotonic()
    return registry

# ─────────────────────────────────────────────────────────────────────────────
# 라우팅
# 구조: view=home|subject|activity|lessons & subject=probability & activity=... & unit=... & origin=...
def get_route():
    qp = _qp_get()
    def first(key: str, default: Optional[str] = None) -> Optional[str]:
        vals = qp.get(key)
        if not vals:
            return default
        return vals[0]
    view     = first("view", "home")
    subject  = first("subject", None)
    activity = first("activity", None)
    unit     = first("unit", None)     # lessons 단원 키
    # origin은 필요 시 개별 함수에서 _qp_get()으로 직접 읽음
    return view, subject, activity, unit

def set_route(view: str, subject: Optional[str] = None,
              activity: Optional[str] = None, unit: Optional[str] = None,
              origin: Optional[str] = None):  # ✅ origin 지원
    params = {"view": view}
    if subject:
        params["subject"] = subject
    if activity:
        params["activity"] = activity
    if unit:
        params["unit"] = unit
    if origin:
        params["origin"] = origin  # ✅ 원래 수업 과목을 기억
    _qp_set(params)

# ─────────────────────────────────────────────────────────────────────────────
# 공통 UI
def _inject_sidebar_nav_visibility(dev: bool):
    """Streamlit 기본 멀티페이지 내비게이션(home, Dev Tree)을 항상 숨깁니다."""
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavContainer"],
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavLink"]
    { display: none !important; visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)
    # JS MutationObserver는 브라우저 세션당 한 번만 주입하면 됨
    if "_sidebar_nav_js_injected" not in st.session_state:
        st.session_state["_sidebar_nav_js_injected"] = True
        components.html("""
    <script>
    (function hideSidebarNav() {
        const SELECTORS = [
            '[data-testid="stSidebarNav"]',
            '[data-testid="stSidebarNavContainer"]',
            '[data-testid="stSidebarNavItems"]',
            '[data-testid="stSidebarNavLink"]',
        ];
        function hide() {
            SELECTORS.forEach(function(sel) {
                var els = window.parent.document.querySelectorAll(sel);
                els.forEach(function(el) {
                    el.style.setProperty('display', 'none', 'important');
                });
            });
        }
        hide();
        var observer = new MutationObserver(hide);
        observer.observe(window.parent.document.body, { childList: true, subtree: true });
    })();
    </script>
    """, height=0)

def _inject_app_theme():
    """로그인 후 전체 앱에 다크 테마를 적용합니다."""
    from theme_utils import inject_dark_theme
    inject_dark_theme()


def sidebar_navigation(registry: Dict[str, List[Activity]]):
    dev            = _is_dev_mode()
    subject_filter = _get_subject_filter()
    login_allowed  = _get_login_allowed_subjects()
    user_type      = st.session_state.get("_user_type", "")
    user_name      = st.session_state.get("_user_name", "")
    user_id        = st.session_state.get("_user_id",   "")
    _inject_sidebar_nav_visibility(dev)

    # ── 닫기 버튼 ─────────────────────────────────────────
    if st.button("✕ 닫기", key="_close_nav_btn", use_container_width=True):
        st.session_state["_sidebar_open"] = False
        _do_rerun()

    # ── 1. 사용자 정보 / 로그아웃 ────────────────────────────
    if user_name:
        type_icon = {"admin": "🔧", "student": "🎓", "general": "👤"}.get(user_type, "👤")
        type_lbl  = {"admin": "관리자", "student": "학생", "general": "일반인"}.get(user_type, "")
        st.caption(f"{type_icon} **{user_name}** ({user_id})  |  {type_lbl}")
    if st.button("🚪 로그아웃", use_container_width=True, key="_logout_btn"):
        for k in ["_authenticated", "_user_type", "_user_id", "_user_name",
                  "_login_allowed_subjects", "_dev_mode",
                  "_login_allowed_lessons",
                  "_show_pw_input", "_pw_error", "_visit_logged",
                  "_ot_mode", "_subject_filter",
                  "_sidebar_nav_js_injected", "_main_sidebar_js_injected",
                  "_sidebar_open"]:
            st.session_state.pop(k, None)
        set_route("home")
        _show_page_transition()  # 잔상 방지
        _do_rerun()

    st.divider()

    # ── 2. 내비게이션 ─────────────────────────────────────────
    if st.button("🏠 홈으로", use_container_width=True, key="_sidebar_home_btn"):
        set_route("home")
        _do_rerun()

    # ── 2-1. 수업 화면일 때: 단원 선택 ────────────────────────
    cur_view, cur_subject, _, cur_unit = get_route()
    if cur_view == "lessons" and cur_subject:
        _cur_curriculum = load_curriculum(cur_subject)
        _cur_units      = load_units(cur_subject)
        _cur_allowed    = _get_login_allowed_units(cur_subject)
        if _cur_allowed is not None:
            if _cur_curriculum:
                _cur_curriculum = _filter_curriculum_by_allowed_units(_cur_curriculum, _cur_allowed)
            if _cur_units:
                _cur_units = _filter_units_by_allowed(_cur_units, _cur_allowed)

        if _cur_curriculum or _cur_units:
            st.divider()
            st.caption("📚 **단원 선택**")

            if _cur_curriculum:
                def _ch(node): return node.get("children", []) if isinstance(node, dict) else []
                _skip_key = f"__skip_sync_{cur_subject}"
                _maj_key  = f"_{cur_subject}_major"
                _mid_key  = f"_{cur_subject}_mid"
                _min_key  = f"_{cur_subject}_min"

                def _mark_uc(): st.session_state[_skip_key] = True
                def _on_maj():
                    st.session_state[_mid_key] = 0
                    st.session_state.pop(_min_key, None)
                    _mark_uc()
                def _on_mid():
                    st.session_state.pop(_min_key, None)
                    _mark_uc()
                def _on_min(): _mark_uc()

                _majors = _cur_curriculum
                # ── URL → 세션 동기화 (위젯 렌더 전에 처리) ──────────────────
                _skip_sync = st.session_state.pop(_skip_key, False)
                if cur_unit and not _skip_sync:
                    _url_path = _find_curriculum_path(_cur_curriculum, cur_unit)
                    if _url_path:
                        _u_maj, _u_mid, _u_min = _url_path
                        st.session_state[_maj_key] = _u_maj
                        if _u_mid is not None:
                            st.session_state[_mid_key] = _u_mid
                        else:
                            st.session_state.pop(_mid_key, None)
                        if _u_min is not None:
                            st.session_state[_min_key] = _u_min
                        else:
                            st.session_state.pop(_min_key, None)
                st.session_state.setdefault(_maj_key, 0)
                if st.session_state[_maj_key] >= len(_majors):
                    st.session_state[_maj_key] = 0

                _maj_idx = st.selectbox(
                    "대단원", options=range(len(_majors)),
                    format_func=lambda i: _majors[i]["label"],
                    key=_maj_key, on_change=_on_maj,
                    label_visibility="visible",
                )
                _mids = _ch(_majors[_maj_idx])
                _middle = None
                if _mids:
                    st.session_state.setdefault(_mid_key, 0)
                    if st.session_state[_mid_key] >= len(_mids):
                        st.session_state[_mid_key] = 0
                    _mid_idx = st.selectbox(
                        "중단원", options=range(len(_mids)),
                        format_func=lambda i: _mids[i]["label"],
                        key=_mid_key, on_change=_on_mid,
                        label_visibility="visible",
                    )
                    _middle = _mids[_mid_idx]
                else:
                    st.session_state.pop(_mid_key, None)
                    st.session_state.pop(_min_key, None)

                _minor = None
                if _middle:
                    _mins = _ch(_middle)
                    if _mins:
                        st.session_state.setdefault(_min_key, 0)
                        if st.session_state[_min_key] >= len(_mins):
                            st.session_state[_min_key] = 0
                        st.selectbox(
                            "소단원", options=range(len(_mins)),
                            format_func=lambda i: _mins[i]["label"],
                            key=_min_key, on_change=_on_min,
                            label_visibility="visible",
                        )
                        _minor = _mins[st.session_state[_min_key]]
                    else:
                        st.session_state.pop(_min_key, None)

                # 선택된 노드 → URL 동기화 (lessons_view에서 처리)

            elif _cur_units:
                _unit_keys = list(_cur_units.keys())
                _def_idx   = _unit_keys.index(cur_unit) if cur_unit in _unit_keys else 0
                st.session_state.setdefault("_lesson_sel_idx", _def_idx)

                def _on_flat_select():
                    _idx = st.session_state.get("_lesson_sel_idx", 0)
                    set_route("lessons", subject=cur_subject, unit=_unit_keys[_idx])
                    _do_rerun()

                st.selectbox(
                    "단원", options=range(len(_unit_keys)),
                    format_func=lambda i: _cur_units[_unit_keys[i]]["label"],
                    index=_def_idx, key="_lesson_sel_idx",
                    on_change=_on_flat_select,
                    label_visibility="visible",
                )

    st.markdown("**📂 교과별 활동**")
    for key, label in SUBJECTS.items():
        if key in HIDDEN_SUBJECTS and not dev:
            continue
        if subject_filter and key != subject_filter:
            continue
        if login_allowed is not None and key not in login_allowed:
            continue
        with st.expander(f"{label}", expanded=False):
            allowed_units = _get_login_allowed_units(key)
            if st.button("교과 메인 열기", key=f"open_{key}_index", use_container_width=True):
                set_route("subject", subject=key)
                _do_rerun()
            if (ACTIVITIES_ROOT / key / "lessons" / "_units.py").exists():
                if allowed_units is not None and not allowed_units:
                    st.caption("수업 권한 없음")
                else:
                    if st.button("수업 열기 (단원별 자료)", key=f"open_{key}_lessons", use_container_width=True):
                        set_route("lessons", subject=key)
                        _do_rerun()
            acts = [a for a in registry.get(key, []) if not a.hidden]
            if key == "gifted" and allowed_units is not None:
                acts = []
            if not acts:
                st.caption("아직 활동이 없습니다.")
            else:
                for act in acts:
                    if st.button(f"• {act.title}", key=f"open_{key}_{act.slug}", use_container_width=True):
                        set_route("activity", subject=key, activity=act.slug)
                        _do_rerun()

    st.divider()

    # ── 3. 개인 메뉴 ──────────────────────────────────────────
    if user_type == "student":
        if st.button("📖 내 성찰 기록", use_container_width=True, key="_my_reflection_btn"):
            set_route("my_reflection"); _do_rerun()
        # 활성화된 설문 버튼
        try:
            from survey_research_utils import get_config
            if get_config("pre_active"):
                if st.button("📋 사전 설문", use_container_width=True, key="_pre_survey_btn"):
                    set_route("activity", subject="etc", activity="survey_pre"); _do_rerun()
            if get_config("post_active"):
                if st.button("📋 사후 설문", use_container_width=True, key="_post_survey_btn"):
                    set_route("activity", subject="etc", activity="survey_post"); _do_rerun()
        except Exception:
            pass
    if st.button("💬 의견 · 오류 접수", use_container_width=True, key="_sidebar_feedback_btn"):
        set_route("feedback"); _do_rerun()
    if user_type in ("student", "general"):
        if st.button("🔑 비밀번호 변경", use_container_width=True, key="_sidebar_chpw_btn"):
            set_route("change_password"); _do_rerun()

    # ── 4. 교사 도구 (휘문고 수학과 그룹) ─────────────────────
    if user_type in ("student", "general"):
        _uid = st.session_state.get("_user_id", "")
        if _uid:
            try:
                from auth_utils import is_math_teacher
                if is_math_teacher(_uid):
                    st.divider()
                    st.caption("🏫 담당 교사 기능")
                    if st.button("👥 회원 관리", use_container_width=True,
                                 key="_teacher_member_btn"):
                        st.switch_page("pages/97_회원관리.py")
            except Exception:
                pass

    # ── 5. 관리자 도구 ────────────────────────────────────────
    if user_type == "admin":
        st.divider()
        if dev:
            st.caption("🔧 **관리자 모드** 활성화 중")
            if st.button("🔓 일반 보기 모드로 전환", use_container_width=True,
                         key="_admin_exit_btn"):
                st.session_state["_dev_mode"] = False
                _do_rerun()
            if st.button("👥 회원 관리", use_container_width=True,
                         key="_admin_member_btn"):
                st.switch_page("pages/97_회원관리.py")
            if st.button("📋 진도표 관리", use_container_width=True,
                         key="_admin_schedule_btn"):
                st.switch_page("pages/98_진도표.py")
            if st.button("📁 Dev Tree (파일 구조 보기)", use_container_width=True,
                         key="_admin_dev_tree_btn"):
                st.switch_page("pages/99_Dev_Tree.py")
            if st.button("🗂️ 설문 관리", use_container_width=True,
                         key="_admin_survey_mgr_btn"):
                set_route("activity", subject="etc", activity="survey_admin"); _do_rerun()
            if st.button("📥 피드백 게시판", use_container_width=True,
                         key="_admin_feedback_board_btn"):
                set_route("feedback_board"); _do_rerun()
            if st.button("📊 방문자 통계", use_container_width=True,
                         key="_admin_visit_stats_btn"):
                set_route("visit_stats"); _do_rerun()
            st.link_button(
                "🤖 AI 튜터와 대화하기",
                "https://copilotstudio.microsoft.com/environments/"
                "Default-62ae463a-9f12-4edf-8544-4f6ca3834524/bots/"
                "copilots_header_78f6d/webchat?__version__=2",
                use_container_width=True,
            )
        else:
            if st.button("🔧 관리자 모드로 전환", use_container_width=True,
                         key="_admin_enter_btn"):
                st.session_state["_dev_mode"] = True
                _do_rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 관리자 홈 대시보드
def _render_admin_dashboard():
    """관리자 홈 대시보드: 처리 필요 항목 요약 + 빠른 바로가기"""
    if not _is_dev_mode():
        return

    from auth_utils import (
        _cached_students, _cached_general, _cached_lockout,
        _get_users_spreadsheet_id, STATUS_PENDING,
    )

    sheet_id   = _get_users_spreadsheet_id()
    students   = _cached_students(sheet_id)
    general    = _cached_general(sheet_id)
    lockouts   = _cached_lockout(sheet_id)
    fb_rows    = _load_feedback_from_sheet()

    pending_s  = sum(1 for r in students if str(r.get("승인상태", "")).strip() == STATUS_PENDING)
    pending_g  = sum(1 for r in general  if str(r.get("승인상태", "")).strip() == STATUS_PENDING)
    total_pend = pending_s + pending_g
    locked_cnt = sum(1 for r in lockouts if str(r.get("잠금상태", "")).strip() == "잠금")

    unconfirmed = 0
    if fb_rows and len(fb_rows) > 1:
        hdr = fb_rows[0]
        try:
            ci = hdr.index("확인여부")
            unconfirmed = sum(
                1 for r in fb_rows[1:]
                if len(r) <= ci or not str(r[ci]).strip()
            )
        except ValueError:
            unconfirmed = len(fb_rows) - 1

    has_alert = total_pend > 0 or unconfirmed > 0 or locked_cnt > 0

    st.markdown("""
    <style>
    .adm-stat {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(99,102,241,0.22);
        border-radius: 10px;
        padding: 0.7rem 0.8rem;
        text-align: center;
        height: 100%;
    }
    .adm-stat-lbl  { font-size:0.78rem; color:rgba(255,255,255,0.48); margin-bottom:0.2rem; }
    .adm-stat-val  { font-size:1.9rem; font-weight:800; line-height:1.1; margin-bottom:0.15rem; color:rgba(255,255,255,0.90); }
    .adm-stat-sub  { font-size:0.72rem; color:rgba(255,255,255,0.45); }
    .adm-stat-ok   { color:#4ade80 !important; }
    .adm-stat-bad  { color:#f87171 !important; }
    .adm-shortcut-label {
        font-size:0.78rem; font-weight:600;
        color:rgba(255,255,255,0.48);
        text-align:center; margin-bottom:0.4rem;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        title_col, refresh_col = st.columns([5, 1])
        with title_col:
            alert_msg = "⚠️ 처리 필요한 항목이 있습니다" if has_alert else "✅ 현재 처리 대기 항목 없음"
            st.markdown(
                f"##### 📋 관리자 현황 &nbsp;"
                f"<span style='font-size:0.85rem;font-weight:400;"
                f"color:var(--secondary-text-color);'>{alert_msg}</span>",
                unsafe_allow_html=True,
            )
        with refresh_col:
            if st.button("🔄", key="_adm_dash_refresh", help="현황 새로고침"):
                st.cache_data.clear()
                _clear_registry_cache()
                _do_rerun()

        col_stats, col_shortcuts = st.columns([3, 1], gap="medium")

        with col_stats:
            m1, m2, m3 = st.columns(3, gap="small")
            with m1:
                vc  = "adm-stat-bad" if total_pend > 0 else "adm-stat-ok"
                sub = f"학생 {pending_s}명 · 일반인 {pending_g}명" if total_pend > 0 else "대기 없음"
                st.markdown(
                    f'<div class="adm-stat">'
                    f'<div class="adm-stat-lbl">👥 가입 승인 대기</div>'
                    f'<div class="adm-stat-val {vc}">{total_pend}</div>'
                    f'<div class="adm-stat-sub">{sub}</div></div>',
                    unsafe_allow_html=True,
                )
            with m2:
                vc  = "adm-stat-bad" if unconfirmed > 0 else "adm-stat-ok"
                sub = f"미확인 {unconfirmed}건" if unconfirmed > 0 else "모두 확인됨"
                st.markdown(
                    f'<div class="adm-stat">'
                    f'<div class="adm-stat-lbl">💬 미확인 피드백</div>'
                    f'<div class="adm-stat-val {vc}">{unconfirmed}</div>'
                    f'<div class="adm-stat-sub">{sub}</div></div>',
                    unsafe_allow_html=True,
                )
            with m3:
                vc  = "adm-stat-bad" if locked_cnt > 0 else "adm-stat-ok"
                sub = "잠금 해제 필요" if locked_cnt > 0 else "잠금 없음"
                st.markdown(
                    f'<div class="adm-stat">'
                    f'<div class="adm-stat-lbl">🔒 잠금 계정</div>'
                    f'<div class="adm-stat-val {vc}">{locked_cnt}</div>'
                    f'<div class="adm-stat-sub">{sub}</div></div>',
                    unsafe_allow_html=True,
                )

        with col_shortcuts:
            st.markdown(
                '<div class="adm-shortcut-label">⚡ 바로가기</div>',
                unsafe_allow_html=True,
            )
            if st.button("👥 회원관리", use_container_width=True, key="_adm_dash_member"):
                st.switch_page("pages/97_회원관리.py")
            if st.button("📋 진도표", use_container_width=True, key="_adm_dash_schedule"):
                st.switch_page("pages/98_진도표.py")
            if st.button("📥 피드백 게시판", use_container_width=True, key="_adm_dash_feedback"):
                set_route("feedback_board"); _do_rerun()


def _inject_home_styles():
    """홈 뷰의 CSS 스타일을 주입합니다."""
    st.markdown(
        """
        <style>
          /* 히어로 섹션 — 다크 유리 카드 */
          .hero-container {
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(99,102,241,0.25);
            border-radius: 20px;
            padding: 2.5rem 2rem;
            margin-bottom: 2.5rem;
            text-align: center;
            box-shadow: 0 8px 40px rgba(0,0,0,0.30),
                        inset 0 1px 0 rgba(255,255,255,0.06);
          }
          .hero-title {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            font-size: 3rem;
            font-weight: 800;
            margin: 0 0 0.75rem 0;
            background: linear-gradient(135deg, #c4b5fd 0%, #a78bfa 45%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }
          .hero-logo-svg {
            width: 56px; height: 56px; flex-shrink: 0;
            -webkit-text-fill-color: initial;
            filter: drop-shadow(0 0 12px rgba(139,92,246,0.65));
          }
          .hero-subtitle {
            font-size: 1.1rem;
            color: rgba(255,255,255,0.55);
            line-height: 1.7;
            margin: 0;
          }

          /* 교과 카드 */
          .subject-card { height: 100%; }
          .subject-card-icon { font-size: 2.6rem; margin-bottom: 0.6rem; }
          .subject-card-title {
            font-size: 1.25rem;
            font-weight: 700;
            margin: 0 0 0.45rem 0;
            color: rgba(255,255,255,0.93);
          }
          .subject-card-desc {
            font-size: 0.9rem;
            color: rgba(255,255,255,0.50);
            line-height: 1.55;
            margin: 0 0 1rem 0;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

def home_view():
    # CSS 스타일링 주입 (뷰가 렌더링될 때마다 적용)
    _inject_home_styles()
    
    # 히어로 섹션
    st.markdown(
        """
        <div class="hero-container">
          <div class="hero-title">
            <svg class="hero-logo-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
              <defs>
                <linearGradient id="hbgGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#1e1b4b"/><stop offset="100%" stop-color="#0f172a"/>
                </linearGradient>
                <linearGradient id="hstrokeGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#c4b5fd"/><stop offset="100%" stop-color="#818cf8"/>
                </linearGradient>
                <linearGradient id="hliquidGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.75"/>
                  <stop offset="100%" stop-color="#4338ca" stop-opacity="0.95"/>
                </linearGradient>
                <linearGradient id="hliquidShine" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stop-color="#a78bfa" stop-opacity="0.4"/>
                  <stop offset="50%" stop-color="#c4b5fd" stop-opacity="0.15"/>
                  <stop offset="100%" stop-color="#818cf8" stop-opacity="0.3"/>
                </linearGradient>
                <radialGradient id="hflaskGlow" cx="50%" cy="60%" r="50%">
                  <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.2"/>
                  <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
                </radialGradient>
                <filter id="hsoftGlow" x="-30%" y="-30%" width="160%" height="160%">
                  <feGaussianBlur stdDeviation="3.5" result="blur"/>
                  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
                <filter id="hstrongGlow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="5" result="blur"/>
                  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
                <clipPath id="hbgClip"><rect x="0" y="0" width="200" height="200" rx="44"/></clipPath>
                <clipPath id="hflaskBodyClip">
                  <path d="M 82 82 L 37 162 Q 28 190 62 190 L 138 190 Q 172 190 163 162 L 118 82 Z"/>
                </clipPath>
              </defs>
              <rect x="0" y="0" width="200" height="200" rx="44" fill="url(#hbgGrad)"/>
              <g clip-path="url(#hbgClip)" stroke="rgba(99,102,241,0.11)" stroke-width="0.8" fill="none">
                <line x1="50" y1="0" x2="50" y2="200"/><line x1="100" y1="0" x2="100" y2="200"/>
                <line x1="150" y1="0" x2="150" y2="200"/><line x1="0" y1="50" x2="200" y2="50"/>
                <line x1="0" y1="100" x2="200" y2="100"/><line x1="0" y1="150" x2="200" y2="150"/>
              </g>
              <ellipse cx="100" cy="145" rx="62" ry="38" fill="rgba(124,58,237,0.10)" filter="url(#hstrongGlow)"/>
              <text x="14" y="46" font-family="Times New Roman,serif" font-size="20" fill="#818cf8" opacity="0.30" font-style="italic">∑</text>
              <text x="158" y="45" font-family="Times New Roman,serif" font-size="20" fill="#a78bfa" opacity="0.30" font-style="italic">π</text>
              <text x="12" y="185" font-family="Times New Roman,serif" font-size="14" fill="#818cf8" opacity="0.22" font-style="italic">∞</text>
              <text x="165" y="186" font-family="Times New Roman,serif" font-size="16" fill="#a78bfa" opacity="0.22" font-style="italic">Δ</text>
              <rect x="82" y="14" width="36" height="68" rx="6" fill="rgba(139,92,246,0.07)" stroke="url(#hstrokeGrad)" stroke-width="2.8"/>
              <rect x="78" y="9" width="44" height="13" rx="6.5" fill="url(#hstrokeGrad)"/>
              <line x1="88" y1="16" x2="88" y2="80" stroke="rgba(255,255,255,0.12)" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M 82 82 L 37 162 Q 28 190 62 190 L 138 190 Q 172 190 163 162 L 118 82 Z" fill="rgba(139,92,246,0.07)" stroke="url(#hstrokeGrad)" stroke-width="2.8" stroke-linejoin="round"/>
              <path d="M 82 82 L 37 162 Q 28 190 62 190 L 138 190 Q 172 190 163 162 L 118 82 Z" fill="url(#hflaskGlow)"/>
              <rect x="0" y="142" width="200" height="55" fill="url(#hliquidGrad)" clip-path="url(#hflaskBodyClip)"/>
              <rect x="0" y="142" width="200" height="18" fill="url(#hliquidShine)" clip-path="url(#hflaskBodyClip)"/>
              <path d="M 36 142 Q 48 132 60 142 Q 72 152 84 142 Q 96 132 108 142 Q 120 152 132 142 Q 144 132 156 142 Q 161 147 164 143" fill="none" stroke="#ddd6fe" stroke-width="2.4" stroke-linecap="round" filter="url(#hsoftGlow)" clip-path="url(#hflaskBodyClip)"/>
              <circle cx="68" cy="162" r="5.5" fill="#a78bfa" opacity="0.45"/>
              <circle cx="100" cy="172" r="3.8" fill="#818cf8" opacity="0.38"/>
              <circle cx="133" cy="160" r="4.5" fill="#a78bfa" opacity="0.40"/>
              <circle cx="82" cy="178" r="2.8" fill="#c4b5fd" opacity="0.32"/>
              <circle cx="118" cy="180" r="2.2" fill="#c4b5fd" opacity="0.28"/>
              <circle cx="58" cy="135" r="2.2" fill="#c4b5fd" opacity="0.28"/>
              <circle cx="77" cy="118" r="1.6" fill="#c4b5fd" opacity="0.20"/>
              <circle cx="112" cy="122" r="1.8" fill="#c4b5fd" opacity="0.22"/>
              <circle cx="138" cy="132" r="1.4" fill="#c4b5fd" opacity="0.18"/>
              <path d="M 90 85 L 52 155" stroke="rgba(255,255,255,0.10)" stroke-width="6" stroke-linecap="round" clip-path="url(#hflaskBodyClip)"/>
              <line x1="111" y1="16" x2="111" y2="78" stroke="rgba(255,255,255,0.09)" stroke-width="4" stroke-linecap="round"/>
              <g opacity="0.18" transform="translate(148,138)">
                <line x1="0" y1="34" x2="36" y2="34" stroke="#8b5cf6" stroke-width="1.2"/>
                <line x1="0" y1="0" x2="0" y2="34" stroke="#8b5cf6" stroke-width="1.2"/>
                <polyline points="3,28 10,18 17,23 24,10 33,4" stroke="#a78bfa" stroke-width="1.2" fill="none"/>
                <polygon points="36,34 32,31 32,37" fill="#8b5cf6"/>
                <polygon points="0,0 -3,6 3,6" fill="#8b5cf6"/>
              </g>
            </svg>
            MathLab
          </div>
          <div class="hero-subtitle">
            수학 수업에서 활용할 수 있는 시뮬레이션과 활동을 한 곳에 모은 공간입니다.<br>
            원하는 교과를 선택하여 다양한 수학 활동을 체험해보세요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 관리자 모드: 현황 대시보드 표시
    _render_admin_dashboard()

    # 교과별 아이콘과 설명 데이터
    subject_data = {
        "common": {
            "icon": "🔢",
            "description": "다항식, 방·부등식, 경우의 수, 행렬 등<br>수학의 기초를 탄탄하게 다집니다."
        },
        "common2": {
            "icon": "🔣",
            "description": "도형의 방정식, 집합과 명제, 함수 등<br>함수의 기초에 대해 학습합니다."
        },
        "algebra": {
            "icon": "🔡",
            "description": "지수와 로그, 삼각함수, 수열 등<br>대수적 사고력을 키웁니다."
        },
        "calculus1": {
            "icon": "📈",
            "description": "함수의 극한과 연속, 다항함수의 미분과<br>적분을 학습합니다."
        },
        "calculus2": {
            "icon": "📊",
            "description": "수열의 극한, 지수·로그·삼각함수의 미분과<br>여러 가지 적분법을 학습합니다."
        },
        "probability_new": {
            "icon": "🎲",
            "description": "경우의 수, 확률, 통계 등<br>통계적 추론 과정을 경험합니다."
        },
        "economics_math": {
            "icon": "💹",
            "description": "수학적 개념을 경제 현상에 적용하여<br>분석하는 방법을 탐구합니다."
        },
        "calculus": {
            "icon": "📈",
            "description": "[이전 교육과정]<br>미적분학 수업 자료입니다."
        },
        "probability": {
            "icon": "🎲",
            "description": "[이전 교육과정]<br>확률과통계 수업 자료입니다."
        },
        "geometry": {
            "icon": "📐",
            "description": "평면과 공간 도형의 성질,<br>변환과 작도의 원리를 탐구합니다."
        },
        "gifted": {
            "icon": "🌟",
            "description": "영재 수업 주제별 자료를 한눈에 보고<br>각 수업 페이지로 이동합니다."
        },
        "etc": {
            "icon": "🧩",
            "description": "프랙털, 게임 이론 등<br>흥미로운 수학 주제들을 만납니다."
        }
    }
    
    # 3열 그리드 레이아웃으로 카드 배치
    dev            = _is_dev_mode()
    subject_filter = _get_subject_filter()       # URL 기반 단일 필터
    login_allowed  = _get_login_allowed_subjects() # 로그인 기반 집합 필터
    visible_subjects = [
        (k, v) for k, v in SUBJECTS.items()
        if (k not in HIDDEN_SUBJECTS or dev)
        and (not subject_filter or k == subject_filter)
        and (login_allowed is None or k in login_allowed)
    ]
    cols = st.columns(3, gap="medium")
    for i, (key, label) in enumerate(visible_subjects):
        data = subject_data.get(key, {"icon": "📚", "description": ""})
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div class="subject-card">
                      <div class="subject-card-icon">{data['icon']}</div>
                      <div class="subject-card-title">{label}</div>
                      <div class="subject-card-desc">{data['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("시작하기", key=f"home_btn_{key}", use_container_width=True, type="primary"):
                    set_route("subject", subject=key)
                    _do_rerun()

    # 의견/오류 접수 섹션은 main()에서 full-page 레벨로 렌더링 (화면 정중앙 정렬을 위해)

def subject_index_view(subject_key: str, registry: Dict[str, List[Activity]]):
    label = SUBJECTS.get(subject_key, subject_key)
    st.title(f"📘 {label} 메인")
    st.markdown("이 교과에 포함된 활동들을 한눈에 보고 바로 실행할 수 있습니다.")

    # ✅ 수업 카드 스타일
    _inject_subject_styles()

    # ✅ lessons/_units.py가 있으면 상단에 '수업' 카드 + 4단 바로가기 UI 노출
    if _has_lessons(subject_key):
        with st.container():
            st.markdown(
                f"""
                <div class="lesson-card">
                  <h4>🔖 {label} 수업 (단원별 자료 모음)</h4>
                  <p>슬라이드/시트/Canva/액티비티를 단원 순서대로 한 화면에서 볼 수 있어요.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ──────────────────────────────
            # 4단(2:2:2:1) 한 줄 구성: 대/중/소 드롭다운 + [수업 열기]
            from typing import Any
            curriculum = load_curriculum(subject_key)
            units_dict = load_units(subject_key)
            lesson_allowed = _get_login_allowed_units(subject_key)
            if lesson_allowed is not None:
                if curriculum:
                    curriculum = _filter_curriculum_by_allowed_units(curriculum, lesson_allowed)
                if units_dict:
                    units_dict = _filter_units_by_allowed(units_dict, lesson_allowed)

            if lesson_allowed is not None and not curriculum and not units_dict:
                st.info("이 그룹에는 현재 허용된 영재 수업이 없습니다. 관리자에게 수업 권한을 요청하세요.")
                return

            if curriculum:
                def ch(node: dict[str, Any]):  # 안전한 children 접근
                    return node.get("children", []) if isinstance(node, dict) else []

                maj_key = f"subj_{subject_key}_pick_major"
                mid_key = f"subj_{subject_key}_pick_mid"
                min_key = f"subj_{subject_key}_pick_min"

                cols = st.columns([2, 2, 2, 1], gap="small")

                # 대단원
                majors = curriculum
                st.session_state.setdefault(maj_key, 0)
                if st.session_state[maj_key] >= len(majors):
                    st.session_state[maj_key] = 0

                def _idx_on_major_change():
                    st.session_state[mid_key] = 0
                    st.session_state[min_key] = 0

                with cols[0]:
                    st.selectbox(
                        "대단원",
                        options=range(len(majors)),
                        format_func=lambda i: majors[i]["label"],
                        key=maj_key,
                        on_change=_idx_on_major_change,
                    )
                maj_idx = st.session_state[maj_key]
                mids = ch(majors[maj_idx])

                # 중단원
                st.session_state.setdefault(mid_key, 0)
                if mids and st.session_state[mid_key] >= len(mids):
                    st.session_state[mid_key] = 0

                def _idx_on_mid_change():
                    st.session_state[min_key] = 0

                with cols[1]:
                    if mids:
                        st.selectbox(
                            "중단원",
                            options=range(len(mids)),
                            format_func=lambda i: mids[i]["label"],
                            key=mid_key,
                            on_change=_idx_on_mid_change,
                        )
                    else:
                        st.selectbox("중단원", options=[], key=mid_key, disabled=True, placeholder="(없음)")
                mid_idx = st.session_state[mid_key]
                mins = ch(mids[mid_idx]) if mids else []

                # 소단원
                st.session_state.setdefault(min_key, 0)
                if mins and st.session_state[min_key] >= len(mins):
                    st.session_state[min_key] = 0

                with cols[2]:
                    if mins:
                        st.selectbox(
                            "소단원",
                            options=range(len(mins)),
                            format_func=lambda i: mins[i]["label"],
                            key=min_key,
                        )
                    else:
                        st.selectbox("소단원", options=[], key=min_key, disabled=True, placeholder="(없음)")

                # 선택된 노드 결정(소 > 중 > 대)
                if mins:
                    sel_node = mins[st.session_state.get(min_key, 0)]
                elif mids:
                    sel_node = mids[st.session_state.get(mid_key, 0)]
                else:
                    sel_node = majors[st.session_state.get(maj_key, 0)]

                # 수업 열기 버튼
                with cols[3]:
                    if st.button("수업 열기", key=f"open_lessons_card_direct_{subject_key}", use_container_width=True):
                        set_route("lessons", subject=subject_key, unit=sel_node.get("key"))
                        _do_rerun()

            elif units_dict:
                # 평면 UNITS인 경우: 드롭다운 + 버튼(2단)
                cols = st.columns([6, 1], gap="small")
                unit_keys = list(units_dict.keys())
                with cols[0]:
                    st.selectbox(
                        "단원",
                        options=range(len(unit_keys)),
                        format_func=lambda i: units_dict[unit_keys[i]]["label"],
                        key=f"subj_{subject_key}_units_sel",
                    )
                with cols[1]:
                    if st.button("수업 열기", key=f"open_lessons_card_units_{subject_key}", use_container_width=True):
                        idx = st.session_state.get(f"subj_{subject_key}_units_sel", 0)
                        set_route("lessons", subject=subject_key, unit=unit_keys[idx])
                        _do_rerun()
            else:
                st.caption(f"`activities/{subject_key}/lessons/_units.py`에 CURRICULUM 또는 UNITS를 정의하면 여기서 바로 이동할 수 있어요.")

    # ▼ OT 자료 진입 버튼 (비밀 토큰 URL일 때만 표시)
    if _is_ot_mode() and subject_key in _OT_CANVA:
        st.divider()
        if st.button("📋 OT 자료 보기", key=f"ot_btn_{subject_key}", type="primary"):
            set_route("ot", subject=subject_key)
            _do_rerun()

    # ▼ 활동 카드들
    acts_all = registry.get(subject_key, [])
    acts = [a for a in acts_all if not a.hidden]    # ← 추가
    if subject_key == "gifted" and _get_login_allowed_units("gifted") is not None:
        acts = []
    if not acts:
        st.info(f"아직 등록된 활동이 없습니다. `activities/{subject_key}/` 폴더에 .py 파일을 추가하세요.")
        return

    for act in acts:
        with st.container(border=True):
            st.subheader(act.title)
            st.caption(act.description)
            c1, c2 = st.columns([1, 3])
            with c1:
                if st.button("열기", key=f"open_{subject_key}_{act.slug}_in_index", use_container_width=True):
                    set_route("activity", subject=subject_key, activity=act.slug)
                    _do_rerun()
            with c2:
                st.code(f"{act.subject_key}/{act.slug}.py", language="text")

LESSON_HEADER_VISIBLE = False

LESSON_HEADER_VISIBLE = False

def gifted_subject_view():
    """영재 교과 메인 — 수업 주제 카드 목록. 클릭하면 해당 수업 lessons 페이지로 직행."""
    st.title("🌟 영재 메인")
    st.markdown("수업 주제를 선택하면 해당 수업 자료 페이지로 바로 이동합니다.")

    _inject_subject_styles()

    curriculum = load_curriculum("gifted")
    if not curriculum:
        st.info("`activities/gifted/lessons/_units.py`의 CURRICULUM에 수업 주제를 추가하세요.")
        return

    allowed_units = _get_login_allowed_units("gifted")
    if allowed_units is not None:
        curriculum = _filter_curriculum_by_allowed_units(curriculum, allowed_units)
        if not curriculum:
            st.warning("현재 계정에는 접근 가능한 영재 수업이 없습니다. 관리자에게 수업 권한을 요청하세요.")
            return

    for topic in curriculum:
        with st.container(border=True):
            st.subheader(topic.get("label", ""))
            items = topic.get("items", [])
            c1, _ = st.columns([1, 3])
            with c1:
                if st.button("열기", key=f"gifted_topic_{topic['key']}", use_container_width=True):
                    set_route("lessons", subject="gifted", unit=topic["key"])
                    _do_rerun()


def ot_view(subject_key: str):
    """OT 자료 전용 페이지."""
    label = SUBJECTS.get(subject_key, subject_key)
    st.title(f"📋 {label} OT")

    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("← 교과 메인", type="secondary", use_container_width=True):
            set_route("subject", subject=subject_key)
            _do_rerun()

    st.divider()
    components.iframe(_OT_CANVA[subject_key], height=860, scrolling=True)


def lessons_view(subject_key: str):
    keep_scroll(key=f"{subject_key}/lessons", mount="sidebar")
    label = SUBJECTS.get(subject_key, subject_key)
    if LESSON_HEADER_VISIBLE:
        st.title(f"🔖 {label} 수업")
        st.caption("왼쪽 선택에서 단원을 고르면, 해당 단원의 수업 자료가 순서대로 나타납니다.")

    _lessons_top_nav(subject_key)

    curriculum = load_curriculum(subject_key)
    units = load_units(subject_key)
    _, _, _, unit_qp = get_route()

    allowed_units = _get_login_allowed_units(subject_key)
    if allowed_units is not None:
        if curriculum:
            curriculum = _filter_curriculum_by_allowed_units(curriculum, allowed_units)
        if units:
            units = _filter_units_by_allowed(units, allowed_units)
        if not curriculum and not units:
            st.warning("현재 계정에는 접근 가능한 영재 수업이 없습니다. 관리자에게 수업 권한을 요청하세요.")
            return

    if curriculum:
        def children(node): return node.get("children", []) if isinstance(node, dict) else []

        # ── 단원 선택은 sidebar_navigation()에서 처리, URL→세션 동기화도 거기서 완료 ──
        # 세션 state에서 현재 선택값 읽기
        maj_key = f"_{subject_key}_major"
        mid_key = f"_{subject_key}_mid"
        min_key = f"_{subject_key}_min"
        skip_key = f"__skip_sync_{subject_key}"

        def ch(node): return node.get("children", []) if isinstance(node, dict) else []
        majors = curriculum

        st.session_state.setdefault(maj_key, 0)
        if st.session_state[maj_key] >= len(majors):
            st.session_state[maj_key] = 0
        maj_idx = st.session_state[maj_key]

        mids = ch(majors[maj_idx])
        middle = None
        if mids:
            st.session_state.setdefault(mid_key, 0)
            if st.session_state[mid_key] >= len(mids):
                st.session_state[mid_key] = 0
            middle = mids[st.session_state[mid_key]]
        else:
            st.session_state.pop(mid_key, None)
            st.session_state.pop(min_key, None)

        minor = None
        if middle:
            mins = ch(middle)
            if mins:
                st.session_state.setdefault(min_key, 0)
                if st.session_state[min_key] >= len(mins):
                    st.session_state[min_key] = 0
                minor = mins[st.session_state[min_key]]
            else:
                st.session_state.pop(min_key, None)

        # 현재 선택을 URL unit과 동기화 (다르면 갱신)
        sel_node = minor or middle or majors[maj_idx]
        sel_key = sel_node.get("key") if isinstance(sel_node, dict) else None
        if sel_key and sel_key != unit_qp:
            st.session_state[skip_key] = True     # ← 갱신 직전 플래그 세팅
            set_route("lessons", subject=subject_key, unit=sel_key)
            _do_rerun()
            return

        # ── 렌더 ──
        items_node = None
        for node in [minor, middle, majors[maj_idx]]:
            if isinstance(node, dict) and "items" in node:
                items_node = node; break

        if not items_node:
            st.info("이 단원에는 아직 자료(items)가 없습니다. `_units.py`의 해당 지점에 items를 추가해 주세요.")
            return

        st.subheader(items_node.get("label", "선택한 단원"))
        st.divider()

        for i, item in enumerate(items_node.get("items", []), start=1):
            typ = item.get("type"); title = item.get("title", "")
            st.markdown(f"### {i}. {title}")
            if typ == "gslides":
                embed_iframe(item["src"], height=item.get("height", 480))
            elif typ == "gsheet":
                embed_iframe(item["src"], height=item.get("height", 700))
            elif typ == "iframe":
                embed_iframe(item["src"], height=item.get("height", 800))
            elif typ == "canva":
                components.html(
                    f'''<iframe loading="lazy" style="border:0;width:100%;height:{item.get("height",600)}px;" allowfullscreen src="{item["src"]}"></iframe>''',
                    height=item.get("height", 600)
                )
            elif typ == "url":
                st.link_button("문서 열기", url=item["src"], use_container_width=True)
            elif typ == "activity":
                subj = item.get("subject"); slug = item.get("slug")
                if st.button(f"▶ 액티비티 열기: {title}", key=f"lesson_open_{subj}_{slug}", use_container_width=True):
                    back_key = (minor or middle or majors[maj_idx]).get("key")
                    set_route("activity", subject=subj, activity=slug, unit=back_key, origin=subject_key)
                    _do_rerun()
            elif typ == "pdf":
                embed_pdf(item["src"], height=item.get("height", 800))
                if item.get("download"):
                    st.link_button("PDF 다운로드", url=item["download"], use_container_width=True)
            elif typ == "youtube":
                url = to_youtube_embed(item["src"])
                embed_iframe(url, height=item.get("height", 400), scrolling=False)
            elif typ == "image":
                imgs = item.get("srcs") or item.get("src")
                caption = item.get("caption")
                width   = item.get("width")
                cols_n  = item.get("cols")
                if isinstance(imgs, list) and cols_n and cols_n > 1:
                    cols = st.columns(cols_n)
                    for j, img in enumerate(imgs):
                        with cols[j % cols_n]:
                            if width: st.image(img, width=width, caption=caption if j == 0 else None)
                            else:     st.image(img, use_container_width=True, caption=caption if j == 0 else None)
                else:
                    if width: st.image(imgs, width=width, caption=caption)
                    else:     st.image(imgs, use_container_width=True, caption=caption)
            else:
                st.info("지원되지 않는 타입입니다. (gslides/gsheet/canva/url/activity)")
            st.divider()
            
    else:
        # ── 평면형 UNITS(기존 방식) ──
        if not units:
            st.info(f"`activities/{subject_key}/lessons/_units.py` 에 CURRICULUM 또는 UNITS를 정의해 주세요.")
            return

        unit_keys = list(units.keys())
        default_idx = unit_keys.index(unit_qp) if (unit_qp in unit_keys) else 0
        # 단원 선택은 sidebar_navigation()에서 처리 — 세션 state에서 읽기
        if "_lesson_sel_idx" not in st.session_state:
            st.session_state["_lesson_sel_idx"] = default_idx

        cur_idx = st.session_state.get("_lesson_sel_idx", default_idx)
        cur_key = unit_keys[cur_idx]
        data = units[cur_key]
        st.subheader(f"단원: {data.get('label','')}")
        st.divider()

        for i, item in enumerate(data.get("items", []), start=1):
            typ = item.get("type"); title = item.get("title", "")
            st.markdown(f"### {i}. {title}")

            if typ == "gslides":
                embed_iframe(item["src"], height=item.get("height", 480))
            elif typ == "gsheet":
                embed_iframe(item["src"], height=item.get("height", 700))
            elif typ == "iframe":
                embed_iframe(item["src"], height=item.get("height", 800))
            elif typ == "canva":
                components.html(
                    f'''
                    <iframe loading="lazy" style="border:0; width:100%; height:{item.get("height",600)}px;"
                            allowfullscreen src="{item["src"]}"></iframe>
                    ''',
                    height=item.get("height", 600)
                )
            elif typ == "url":
                st.link_button("문서 열기", url=item["src"], use_container_width=True)
            elif typ == "youtube":
                url = to_youtube_embed(item["src"])
                embed_iframe(url, height=item.get("height", 400), scrolling=False)
            elif typ == "activity":
                subj = item.get("subject"); slug = item.get("slug")
                if st.button(f"▶ 액티비티 열기: {title}", key=f"lesson_open_{cur_key}_{slug}", use_container_width=True):
                    set_route("activity", subject=subj, activity=slug, unit=cur_key, origin=subject_key)
                    _do_rerun()
            else:
                st.info("지원되지 않는 타입입니다. (gslides/gsheet/canva/url/activity)")

            st.divider()



        # ✅ 하단 네비 버튼은 제거됨 (상단만 사용)


def activity_view(subject_key: str, slug: str, registry: Dict[str, List[Activity]], unit: Optional[str] = None):
    acts = registry.get(subject_key, [])
    act = next((a for a in acts if a.slug == slug), None)
    if not act:
        st.error("해당 활동을 찾을 수 없습니다. 파일명이 바뀌었는지 확인하세요.")
        return

    # ✅ 쿼리에서 origin(원래 수업 과목) 읽기
    qp = _qp_get()
    origin_subject = None
    try:
        vals = qp.get("origin")
        if vals:
            origin_subject = vals[0]
    except Exception:
        origin_subject = None

    # 영재 수업 단원 경유 액티비티는 단원 접근권한을 검사
    if unit and (subject_key == "gifted" or origin_subject == "gifted"):
        allowed_units = _get_login_allowed_units("gifted")
        if allowed_units is not None and unit not in allowed_units:
            st.error("해당 영재 수업 단원에 대한 접근 권한이 없습니다.")
            if st.button("🏠 홈으로", key="forbidden_unit_home", use_container_width=True):
                set_route("home")
                _do_rerun()
            return

    # 일반인은 영재 교과를 단원 권한 기반(lessons 경유)으로만 접근 가능
    if subject_key == "gifted" and unit is None:
        allowed_units = _get_login_allowed_units("gifted")
        if allowed_units is not None:
            st.error("영재 활동은 허용된 수업 단원을 통해서만 접근할 수 있습니다.")
            if st.button("🌟 영재 수업으로 이동", key="forbidden_gifted_go_lessons", use_container_width=True):
                set_route("lessons", subject="gifted")
                _do_rerun()
            return

    cols = st.columns([1, 1, 1])
    with cols[0]:
        if unit:
            # ✅ 수업에서 넘어온 경우: origin이 있으면 그 과목으로, 없으면 현재 과목으로 복귀
            if st.button("← 수업으로 돌아가기", type="secondary", use_container_width=True):
                target_subject = origin_subject or subject_key
                set_route("lessons", subject=target_subject, unit=unit); _do_rerun()
        else:
            if st.button("← 교과 메인", type="secondary", use_container_width=True):
                set_route("subject", subject=subject_key); _do_rerun()
    with cols[2]:
        if st.button("🏠 홈", type="secondary", use_container_width=True):
            set_route("home"); _do_rerun()

    # ✅ 스크롤 유지 스크립트를 사이드바에 주입 → 본문에 '빈 공간' 생성 안 됨
    keep_scroll(key=f"{subject_key}/{slug}", mount="sidebar")

    # ⚠️ 여기에는 divider/빈 마크다운을 넣지 마세요 (여백 원인)
    act.render()

# ─────────────────────────────────────────────────────────────────────────────
# 개인정보처리방침 팝업
@st.dialog("📜 개인정보처리방침", width="large")
def _privacy_policy_dialog():
    st.markdown("""
**MathLab** 은(는) 개인정보 보호법 제30조에 따라 정보주체의 개인정보를 보호하고 이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 하기 위하여 다음과 같이 개인정보 처리방침을 수립·공개합니다.

---

**제1조 (개인정보의 처리 목적)**

본 서비스는 다음의 목적을 위하여 개인정보를 처리합니다. 처리하고 있는 개인정보는 다음의 목적 이외의 용도로는 이용되지 않으며, 이용 목적이 변경되는 경우에는 「개인정보 보호법」 제18조에 따라 별도의 동의를 받는 등 필요한 조치를 이행할 예정입니다.

① **회원 가입 및 이용자 인증**: 학생 및 일반인 회원가입 신청 접수, 교사(관리자)의 승인 후 서비스 이용 활성화, 아이디·비밀번호를 통한 로그인 인증 및 이용자 식별
② **교과별 접근 권한 관리**: 로그인 계정의 학년 또는 그룹에 따라 허용된 교과 자료의 접근 범위 제한 및 제공
③ **수업 자료 및 학습 활동 제공**: 교과별 강의 자료(슬라이드·PDF·영상) 및 인터랙티브 시뮬레이션 활동 제공
④ **학습 활동 결과 기록 및 관리**: 학생이 활동 후 성찰 기록 제출 시 학번·이름·활동 내용을 수집하여 Google Sheets에 저장하며, 교사의 학습 확인 및 피드백 제공에 활용. 학생은 자신의 과거 성찰 제출 이력을 서비스 내에서 직접 조회할 수 있습니다.
⑤ **방문 기록 관리**: 서비스 개선을 위해 방문 시각·과목 필터·사용자 ID를 Google Sheets에 기록합니다. 해당 데이터는 관리자(교사)만 열람 가능합니다.
⑥ **교사의 진도 관리 및 상담 지원**: 날짜·반별 수업 진도 기록, Google Sheets 연동을 통한 진도 데이터 관리로 체계적인 수업 운영을 지원
⑦ **관리자(교사) 인증 및 서비스 운영**: 관리자 계정을 통한 접근 권한 확인, 회원 승인·거부·그룹 관리 등 관리자 전용 기능 제공

---

**제2조 (개인정보의 처리 및 보유기간)**

① 본 서비스는 법령에 따른 개인정보 보유·이용기간 또는 정보주체로부터 개인정보를 수집 시에 동의받은 개인정보 보유·이용기간 내에서 개인정보를 처리·보유합니다.
② 각각의 개인정보 처리 및 보유 기간은 다음과 같습니다.

- **보유 기간**: 해당 학년도 종료 시(익년 2월 말) 또는 학생의 졸업·진급 시까지
- **파기 시점**: 보유 기간 종료 후 지체 없이(5일 이내) 파기

---

**제3조 (처리하는 개인정보 항목)**

본 서비스는 학습 지원을 위해 필요한 최소한의 개인정보만을 수집합니다.

| 구분 | 수집 항목 |
|---|---|
| 학생 회원 | 학번, 이름, 아이디(연도+학번 자동생성), 비밀번호(bcrypt 암호화 저장), 학년, 가입일, 마지막 로그인 일시 |
| 일반 회원 | 이름, 아이디, 비밀번호(bcrypt 암호화 저장), 사용목적, 소속그룹, 가입일, 마지막 로그인 일시 |
| 성찰 기록 | 학번, 이름, 활동명, 제출 시각, 활동별 답변 내용 |
| 방문 기록 | 방문 시각, 과목 필터, 사용자 ID |

- **수집하지 않는 항목**: 주민등록번호, 주소, 전화번호, 이메일 등 불필요한 민감 정보

---

**제4조 (만 14세 미만 아동의 개인정보 처리에 관한 사항)**

① 본 서비스는 만 14세 미만 아동의 개인정보를 처리하기 위하여 회원가입 화면의 보호자 동의 확인란 체크 및 학기 초 학교 가정통신문(개인정보 수집·이용 동의서)을 통하여 법정대리인의 동의를 받습니다.
② 법정대리인이 동의하지 않는 경우, 해당 아동은 서비스 가입 및 이용이 제한될 수 있습니다.

---

**제5조 (개인정보의 파기 절차 및 방법)**

① 개인정보 보유기간의 경과, 처리목적 달성 등 개인정보가 불필요하게 되었을 때에는 지체 없이 해당 개인정보를 파기합니다.
② **파기 방법**: 전자적 파일 형태로 기록·저장된 개인정보는 기록을 재생할 수 없도록 영구 삭제(Google Sheets 행 삭제)하며, 별도의 종이 문서는 존재하지 않습니다.

---

**제6조 (개인정보의 안전성 확보조치)**

본 서비스는 개인정보 보호법 제29조에 따라 다음과 같이 안전성 확보에 필요한 기술적·관리적 조치를 하고 있습니다.

① **비밀번호 암호화**: 이용자의 비밀번호는 bcrypt 알고리즘을 이용한 일방향 암호화(Hash)로 저장·관리됩니다. 원문 비밀번호는 저장되지 않으며 개발자(관리자)도 확인할 수 없습니다.
② **로그인 시도 제한**: 동일 세션 내 로그인 실패가 5회 이상 발생하면 추가 시도가 차단됩니다.
③ **관리자 승인을 통한 접근 통제**: 회원가입 후 교사(관리자)의 승인을 거쳐야 서비스를 이용할 수 있으며, 학년 및 그룹 단위로 접근 가능한 교과를 제한합니다.
④ **해킹 등에 대비한 기술적 대책**: 보안 인증을 획득한 전문 클라우드 플랫폼(Google Sheets, Streamlit Cloud, GitHub)을 기반으로 운영되며, 전 구간 보안 통신(HTTPS)을 사용하여 데이터를 암호화 전송합니다.
⑤ **접근 권한 최소화**: Google 서비스 계정 키 및 비밀 설정값은 Streamlit Cloud Secrets에만 보관되며, 소스코드(GitHub)에는 일절 포함되지 않습니다.
⑥ **개인정보 취급 직원의 최소화**: 개인정보를 처리하는 담당자를 개발 교사 1인으로 지정하여 관리자 계정 접근 권한을 운영합니다.

---

**제7조 (정보주체와 법정대리인의 권리·의무 및 행사방법)**

① 정보주체(학생) 및 법정대리인은 언제든지 개인정보 열람·정정·삭제·처리정지 요구 등의 권리를 행사할 수 있습니다.
② 학생 회원은 서비스 내 **[내 성찰 기록]** 메뉴를 통해 자신의 제출 이력을 직접 열람할 수 있으며, **[비밀번호 변경]** 기능을 통해 본인 정보를 직접 수정할 수 있습니다.
③ 계정 삭제(탈퇴) 및 그 밖의 개인정보 삭제 요청은 개발 교사에게 구두나 서면으로 요청하면 지체 없이 조치하겠습니다.

---

**제8조 (개인정보 보호책임자)**

본 서비스는 개인정보 처리에 관한 업무를 총괄하여 책임지고, 개인정보 처리와 관련한 정보주체의 불만처리 및 피해구제 등을 위하여 아래와 같이 개인정보 보호책임자를 지정하고 있습니다.

- **성명**: 김대섭 (개발자)
- **소속**: 휘문고등학교
- **직위**: 교사
- **연락처**: 02-500-9513 (학교 교무실)
  ※ 개인정보 보호를 위해 교사의 개인 휴대전화 번호는 기재하지 않습니다.

---

**제9조 (개인정보 처리방침 변경)**

이 개인정보 처리방침은 **2026년 3월 10일**부터 적용됩니다.
""")

# ─────────────────────────────────────────────────────────────────────────────
# 관리자 피드백 게시판 뷰
def feedback_board_view():
    """[관리자 전용] 피드백 접수 게시판."""
    if not _is_dev_mode():
        set_route("home")
        _do_rerun()
        return

    if st.button("← 홈으로", type="secondary", key="fb_board_back_btn"):
        set_route("home")
        _do_rerun()

    st.title("📥 피드백 게시판")
    st.caption("학생들이 제출한 오류 신고 및 활동 건의 목록입니다.")
    st.divider()

    if st.button("🔄 새로고침", key="fb_board_refresh_btn"):
        st.cache_data.clear()

    with st.spinner("시트에서 불러오는 중..."):
        rows = _load_feedback_from_sheet()

    if not rows or len(rows) <= 1:
        st.info("접수된 의견이 없습니다.")
        return

    import pandas as pd
    header = rows[0]
    data   = rows[1:]
    df = pd.DataFrame(data, columns=header)

    # 필터
    col_f, col_s = st.columns([2, 3])
    with col_f:
        type_opts = ["전체"] + sorted(df["유형"].unique().tolist())
        sel_type = st.selectbox("유형 필터", type_opts, key="fb_filter_type")
    with col_s:
        search_kw = st.text_input("내용 검색", placeholder="학번/이름/내용 키워드", key="fb_search_kw")

    filtered = df.copy()
    if sel_type != "전체":
        filtered = filtered[filtered["유형"] == sel_type]
    if search_kw.strip():
        kw = search_kw.strip().lower()
        mask = (
            filtered["학번"].str.lower().str.contains(kw, na=False)
            | filtered["이름"].str.lower().str.contains(kw, na=False)
            | filtered["내용"].str.lower().str.contains(kw, na=False)
        )
        filtered = filtered[mask]

    # 최신 순으로
    filtered = filtered.iloc[::-1].reset_index(drop=True)

    has_confirm_col = "확인여부" in df.columns
    unconfirmed_total = 0
    if has_confirm_col:
        unconfirmed_total = int((df["확인여부"].fillna("").str.strip() != "확인").sum())
    else:
        unconfirmed_total = len(df)

    st.caption(
        f"전체 {len(df)}건 · 필터 결과 {len(filtered)}건"
        + (f" · 미확인 {unconfirmed_total}건" if unconfirmed_total > 0 else " · 모두 확인됨")
    )

    for _, row in filtered.iterrows():
        icon = "🛠" if "오류" in str(row.get("유형", "")) else "💡"
        is_confirmed = has_confirm_col and str(row.get("확인여부", "")).strip() == "확인"
        check_badge  = " ✅" if is_confirmed else " 🔴"
        with st.expander(
            f"{icon}{check_badge} [{row['접수시각']}]  {row['이름']}({row['학번']})  —  {row['유형']}",
            expanded=False,
        ):
            fb_ts = str(row.get("접수시각", ""))
            if is_confirmed:
                st.caption("✅ 확인 완료된 항목입니다.")
            else:
                if st.button("✅ 확인 완료로 표시", key=f"fb_chk_{fb_ts}",
                             type="primary", use_container_width=False):
                    if _mark_feedback_checked(fb_ts):
                        st.success("확인 완료로 표시했습니다.")
                        st.rerun()
                    else:
                        st.error("업데이트에 실패했습니다.")
            st.markdown(f"**답변 이메일:** {row.get('답변이메일', '') or '(미입력)'}")
            st.markdown("**내용:**")
            st.markdown(
                f"<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(99,102,241,0.22);"
                f"padding:10px;border-radius:8px;white-space:pre-wrap;line-height:1.6;"
                f"color:rgba(255,255,255,0.85);'>"
                f"{row.get('내용', '')}</div>",
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# 피드백 Google Sheets 연동
_FEEDBACK_SHEET_NAME = "피드백"
_FEEDBACK_SHEET_HEADER = ["접수시각", "유형", "학번", "이름", "답변이메일", "내용", "확인여부"]

def _get_feedback_gspread_client():
    """gspread 클라이언트를 반환. 실패 시 None."""
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

def _get_or_create_feedback_worksheet():
    """
    진도표 스프레드시트에서 '피드백' 워크시트를 가져오거나,
    없으면 자동으로 생성하고 헤더를 추가하여 반환합니다.
    """
    try:
        client = _get_feedback_gspread_client()
        if client is None:
            return None
        spreadsheet_id: str = st.secrets["spreadsheet_id"]
        sh = client.open_by_key(spreadsheet_id)
        try:
            ws = sh.worksheet(_FEEDBACK_SHEET_NAME)
        except Exception:
            ws = sh.add_worksheet(title=_FEEDBACK_SHEET_NAME, rows=1000, cols=6)
            ws.append_row(_FEEDBACK_SHEET_HEADER)
        return ws
    except Exception:
        return None

def _save_feedback_to_sheet(
    feedback_type: str,
    student_id: str,
    student_name: str,
    reply_email: str,
    content: str,
) -> bool:
    """피드백 한 행을 구글 시트에 기록합니다."""
    ws = _get_or_create_feedback_worksheet()
    if ws is None:
        return False
    try:
        now_str = datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([
            now_str,
            feedback_type,
            student_id,
            student_name,
            reply_email,
            content,
        ])
        return True
    except Exception:
        return False

def _load_feedback_from_sheet() -> "list[list]":
    """피드백 시트의 모든 행을 반환합니다(헤더 포함)."""
    ws = _get_or_create_feedback_worksheet()
    if ws is None:
        return []
    try:
        return ws.get_all_values()
    except Exception:
        return []


def _mark_feedback_checked(timestamp_str: str) -> bool:
    """피드백 행의 '확인여부'를 '확인'으로 업데이트합니다."""
    ws = _get_or_create_feedback_worksheet()
    if ws is None:
        return False
    try:
        all_vals = ws.get_all_values()
        if not all_vals:
            return False
        header = all_vals[0]
        if "확인여부" not in header:
            # 헤더에 컬럼이 없으면 시트 열 수를 먼저 늘린 뒤 추가
            col_idx = len(header) + 1
            ws.resize(rows=ws.row_count, cols=col_idx)
            ws.update_cell(1, col_idx, "확인여부")
            header = header + ["확인여부"]
        else:
            col_idx = header.index("확인여부") + 1
        ts_col = header.index("접수시각") if "접수시각" in header else 0
        for i, row in enumerate(all_vals[1:], start=2):
            if not row:
                continue
            cell_ts = row[ts_col].strip() if ts_col < len(row) else ""
            if cell_ts == timestamp_str.strip():
                ws.update_cell(i, col_idx, "확인")
                return True
        return False
    except Exception as e:
        st.error(f"[_mark_feedback_checked] {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# 방문 기록 Google Sheets 연동
_VISIT_SHEET_NAME   = "방문기록"
_VISIT_SHEET_HEADER = ["방문시각", "과목필터", "사용자ID"]

def _get_or_create_visit_worksheet():
    """
    진도표 스프레드시트에서 '방문기록' 워크시트를 가져오거나,
    없으면 자동으로 생성하고 헤더를 추가하여 반환합니다.
    """
    try:
        client = _get_feedback_gspread_client()   # 동일 서비스 계정 재사용
        if client is None:
            return None
        spreadsheet_id: str = st.secrets["spreadsheet_id"]
        sh = client.open_by_key(spreadsheet_id)
        try:
            ws = sh.worksheet(_VISIT_SHEET_NAME)
        except Exception:
            ws = sh.add_worksheet(title=_VISIT_SHEET_NAME, rows=10000, cols=3)
            ws.append_row(_VISIT_SHEET_HEADER)
        return ws
    except Exception:
        return None

def _do_log_visit_write(subject_filter: str, user_id: str) -> None:
    """방문 기록을 Google Sheets에 씁니다 (백그라운드 스레드용)."""
    try:
        ws = _get_or_create_visit_worksheet()
        if ws is None:
            return
        now_str = datetime.now(_KST).strftime("%Y-%m-%d %H:%M:%S")
        ws.append_row([now_str, subject_filter, user_id])
    except Exception:
        pass

def _log_visit() -> None:
    """
    세션당 한 번만 방문 시각과 과목 필터를 Google Sheets에 기록합니다.
    st.session_state['_visit_logged'] 플래그로 중복 기록을 방지합니다.
    Sheets 쓰기는 백그라운드 스레드에서 처리하여 첫 페이지 렌더링을 지연시키지 않습니다.
    """
    if st.session_state.get("_visit_logged"):
        return
    st.session_state["_visit_logged"] = True
    # session_state는 메인 스레드에서 미리 읽어 전달
    subject_filter = st.session_state.get("_subject_filter", "(전체)") or "(전체)"
    user_id = st.session_state.get("_user_id", "")
    threading.Thread(
        target=_do_log_visit_write,
        args=(subject_filter, user_id),
        daemon=True,
    ).start()

def _load_visit_data() -> "list[list]":
    """방문기록 시트의 모든 행(헤더 포함)을 반환합니다."""
    ws = _get_or_create_visit_worksheet()
    if ws is None:
        return []
    try:
        return ws.get_all_values()
    except Exception:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# 성찰 기록 통계 조회
_REFLECTION_LOG_SHEET_NAME = "성찰기록"

def _load_reflection_log_data() -> "list[list]":
    """성찰기록 시트의 모든 행(헤더 포함)을 반환합니다. 없으면 빈 리스트."""
    try:
        client = _get_feedback_gspread_client()
        if client is None:
            return []
        spreadsheet_id: str = st.secrets["spreadsheet_id"]
        sh = client.open_by_key(spreadsheet_id)
        try:
            ws = sh.worksheet(_REFLECTION_LOG_SHEET_NAME)
        except Exception:
            return []
        return ws.get_all_values()
    except Exception:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# 성찰 기록 통계 조회
_REFLECTION_LOG_SHEET_NAME = "성찰기록"

def _load_reflection_log_data() -> "list[list]":
    """성찰기록 시트의 모든 행(헤더 포함)을 반환합니다. 없으면 빈 리스트."""
    try:
        client = _get_feedback_gspread_client()
        if client is None:
            return []
        spreadsheet_id: str = st.secrets["spreadsheet_id"]
        sh = client.open_by_key(spreadsheet_id)
        try:
            ws = sh.worksheet(_REFLECTION_LOG_SHEET_NAME)
        except Exception:
            return []
        return ws.get_all_values()
    except Exception:
        return []


# ─────────────────────────────────────────────────────────────────────────────
# 내 성찰 기록 뷰 (학생 전용)
def my_reflection_view():
    """[학생 전용] 자신이 제출한 성찰 기록 조회."""
    import pandas as pd

    user_type = st.session_state.get("_user_type", "")
    if user_type != "student":
        set_route("home")
        _do_rerun()
        return

    if st.button("← 홈으로", type="secondary", key="myref_back_btn"):
        set_route("home")
        _do_rerun()

    user_id   = st.session_state.get("_user_id", "")
    user_name = st.session_state.get("_user_name", "")

    # 학번 앞 4자리 연도 제거 (성찰기록에 저장된 형식과 맞춤)
    short_id = (
        user_id[4:]
        if len(user_id) >= 9 and user_id[:2] == "20"
        else user_id
    )

    st.title("📖 내 성찰 기록")
    st.caption(f"**{user_name}** 님이 제출한 성찰 기록입니다.")
    st.divider()

    if st.button("🔄 새로고침", key="myref_refresh_btn"):
        st.cache_data.clear()

    with st.spinner("기록 불러오는 중..."):
        rows = _load_reflection_log_data()

    if not rows or len(rows) <= 1:
        st.info("아직 제출한 성찰 기록이 없습니다.")
        return

    raw = [r + [""] * (5 - len(r)) for r in rows[1:]]
    df = pd.DataFrame(raw, columns=["제출시각", "과목", "활동시트명", "학번", "이름"])
    df["제출시각"] = pd.to_datetime(df["제출시각"], errors="coerce")
    df = df.dropna(subset=["제출시각"])

    # 본인 기록만 필터링
    my_df = df[df["학번"] == short_id].sort_values("제출시각", ascending=False)

    if my_df.empty:
        st.info("아직 제출한 성찰 기록이 없습니다.")
        return

    # 요약
    c1, c2, c3 = st.columns(3)
    c1.metric("총 제출 횟수",  f"{len(my_df):,} 회")
    c2.metric("참여 활동 수",  f"{my_df['활동시트명'].nunique():,} 가지")
    c3.metric("최근 제출일",   my_df["제출시각"].max().strftime("%Y-%m-%d"))

    st.divider()

    # 과목 필터
    subjects = ["전체"] + sorted(my_df["과목"].dropna().unique().tolist())
    sel = st.selectbox("📚 과목 선택", subjects, key="myref_subj_filter")
    filtered = my_df if sel == "전체" else my_df[my_df["과목"] == sel]

    # 활동별 제출 횟수 요약표
    st.markdown("##### 활동별 제출 현황")
    summary = (
        filtered.groupby(["과목", "활동시트명"])
        .agg(제출횟수=("제출시각", "count"), 마지막제출=("제출시각", "max"))
        .reset_index()
        .sort_values("마지막제출", ascending=False)
    )
    summary["마지막제출"] = summary["마지막제출"].dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True,
        column_config={
            "과목":       st.column_config.TextColumn("과목"),
            "활동시트명": st.column_config.TextColumn("활동명"),
            "제출횟수":   st.column_config.NumberColumn("제출 횟수"),
            "마지막제출": st.column_config.TextColumn("마지막 제출일"),
        },
    )

    st.divider()

    # 전체 제출 이력
    st.markdown("##### 전체 제출 이력")
    show_df = filtered[["제출시각", "과목", "활동시트명"]].copy()
    show_df["제출시각"] = show_df["제출시각"].dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(show_df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# 방문 통계 뷰 (관리자 전용)
def visit_stats_view():
    """[관리자 전용] 방문자 통계 대시보드 — 중복 허용 / 중복 제거 두 모드 지원."""
    import pandas as pd
    import plotly.express as px

    def _dark_fig(fig):
        """Plotly 차트에 다크 테마를 적용합니다."""
        _gc = dict(gridcolor="rgba(99,102,241,0.15)", linecolor="rgba(99,102,241,0.25)",
                   tickfont=dict(color="rgba(255,255,255,0.60)"),
                   title_font=dict(color="rgba(255,255,255,0.70)"))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.45)",
            font=dict(color="rgba(255,255,255,0.75)", size=12),
            title_font=dict(color="rgba(255,255,255,0.90)"),
            xaxis=_gc, yaxis=_gc,
            legend=dict(bgcolor="rgba(15,23,42,0.70)",
                        bordercolor="rgba(99,102,241,0.22)",
                        font=dict(color="rgba(255,255,255,0.75)")),
        )
        return fig

    if not _is_dev_mode():
        set_route("home")
        _do_rerun()
        return

    if st.button("← 홈으로", type="secondary", key="vstats_back_btn"):
        set_route("home")
        _do_rerun()

    st.title("📊 방문자 통계")
    st.divider()

    if st.button("🔄 새로고침", key="vstats_refresh_btn"):
        st.cache_data.clear()

    with st.spinner("방문 기록 불러오는 중..."):
        rows = _load_visit_data()

    if not rows or len(rows) <= 1:
        st.info("아직 방문 기록이 없습니다.")
        return

    # 열 수가 2개(구 형식)일 수도, 3개(신 형식)일 수도 있어 유연하게 처리
    raw = [r + [""] * (3 - len(r)) for r in rows[1:]]
    df = pd.DataFrame(raw, columns=["방문시각", "과목필터", "사용자ID"])
    df["방문시각"] = pd.to_datetime(df["방문시각"], errors="coerce")
    df = df.dropna(subset=["방문시각"])
    df["날짜"] = df["방문시각"].dt.date

    today     = pd.Timestamp(datetime.now(_KST).date())
    week_ago  = today - pd.Timedelta(days=6)
    month_ago = today - pd.Timedelta(days=29)

    # ── 집계 모드 선택 ──────────────────────────────────────────────────────
    count_mode = st.radio(
        "📌 집계 방식",
        ["중복 허용 (세션 기준)", "중복 제거 (사용자 ID 기준)"],
        horizontal=True,
        key="vstats_count_mode",
    )
    is_unique = count_mode == "중복 제거 (사용자 ID 기준)"

    if is_unique:
        st.caption(
            "같은 사용자 ID로 하루에 여러 번 접속해도 하루 1회로만 집계합니다. "
            "사용자 ID가 없는 행(구 데이터 또는 비로그인)은 제외됩니다."
        )
        # 사용자 ID가 있는 행만, (날짜, 사용자ID) 기준 중복 제거
        df_u = df[df["사용자ID"] != ""].drop_duplicates(subset=["날짜", "사용자ID"])
    else:
        st.caption("세션 최초 접속 기준으로 기록된 모든 방문 데이터를 집계합니다.")
        df_u = df

    # ── 요약 수치 ───────────────────────────────────────────────────────────
    cnt_today = int((df_u["날짜"] == today.date()).sum())
    cnt_week  = int((df_u["방문시각"] >= week_ago).sum())
    cnt_month = int((df_u["방문시각"] >= month_ago).sum())
    cnt_total = len(df_u)

    if is_unique:
        # 누적 고유 사용자 수 (날짜 무관, ID 기준)
        cnt_unique_total = df[df["사용자ID"] != ""]["사용자ID"].nunique()
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("오늘",          f"{cnt_today:,} 명")
        m2.metric("최근 7일",      f"{cnt_week:,} 명")
        m3.metric("최근 30일",     f"{cnt_month:,} 명")
        m4.metric("집계 합계",     f"{cnt_total:,} 명")
        m5.metric("누적 고유 사용자", f"{cnt_unique_total:,} 명")
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("오늘",      f"{cnt_today:,} 명")
        m2.metric("최근 7일",  f"{cnt_week:,} 명")
        m3.metric("최근 30일", f"{cnt_month:,} 명")
        m4.metric("누적",      f"{cnt_total:,} 명")

    st.divider()

    # ── 차트 탭 ──────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs(["📅 최근 30일", "📅 최근 7일", "📅 과목별 분포", "📝 성찰 통계"])
    chart_color_30d = "#6366f1" if not is_unique else "#0ea5e9"
    chart_color_7d  = "#a855f7" if not is_unique else "#10b981"
    chart_label = "방문자 수" if not is_unique else "고유 사용자 수"

    with tab1:
        date_range = pd.date_range(end=today, periods=30, freq="D")
        daily = (
            df_u[df_u["방문시각"] >= month_ago]
            .groupby("날짜")
            .size()
            .reindex([d.date() for d in date_range], fill_value=0)
            .reset_index()
        )
        daily.columns = ["날짜", "방문자"]
        daily["날짜"] = pd.to_datetime(daily["날짜"])
        fig = px.bar(
            daily, x="날짜", y="방문자",
            title=f"일별 {'고유 사용자' if is_unique else '방문자'} 수 (최근 30일)",
            labels={"날짜": "날짜", "방문자": chart_label},
            color_discrete_sequence=[chart_color_30d],
        )
        fig.update_layout(hovermode="x unified")
        _dark_fig(fig)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        date_range7 = pd.date_range(end=today, periods=7, freq="D")
        daily7 = (
            df_u[df_u["방문시각"] >= week_ago]
            .groupby("날짜")
            .size()
            .reindex([d.date() for d in date_range7], fill_value=0)
            .reset_index()
        )
        daily7.columns = ["날짜", "방문자"]
        daily7["날짜"] = pd.to_datetime(daily7["날짜"])
        fig7 = px.bar(
            daily7, x="날짜", y="방문자",
            title=f"일별 {'고유 사용자' if is_unique else '방문자'} 수 (최근 7일)",
            labels={"날짜": "날짜", "방문자": chart_label},
            color_discrete_sequence=[chart_color_7d],
        )
        fig7.update_layout(hovermode="x unified")
        _dark_fig(fig7)
        st.plotly_chart(fig7, use_container_width=True)

    with tab3:
        subj_df = (
            df_u[df_u["방문시각"] >= month_ago]
            .groupby("과목필터")
            .size()
            .reset_index()
        )
        subj_df.columns = ["과목", chart_label]
        subj_df = subj_df.sort_values(chart_label, ascending=False)
        fig_s = px.pie(
            subj_df, names="과목", values=chart_label,
            title=f"과목별 비율 (최근 30일, {'고유 사용자' if is_unique else '방문자'})",
        )
        fig_s.update_traces(textposition="inside", textinfo="percent+label")
        _dark_fig(fig_s)
        st.plotly_chart(fig_s, use_container_width=True)
        st.dataframe(subj_df, use_container_width=True, hide_index=True)

    with tab4:
        with st.spinner("성찰 기록 불러오는 중..."):
            ref_rows = _load_reflection_log_data()

        if not ref_rows or len(ref_rows) <= 1:
            st.info("아직 성찰 제출 기록이 없습니다.")
        else:
            ref_raw = [r + [""] * (5 - len(r)) for r in ref_rows[1:]]
            ref_df = pd.DataFrame(
                ref_raw, columns=["제출시각", "과목", "활동시트명", "학번", "이름"]
            )
            ref_df["제출시각"] = pd.to_datetime(ref_df["제출시각"], errors="coerce")
            ref_df = ref_df.dropna(subset=["제출시각"])

            # ── 과목·활동 필터 ────────────────────────────────────────────────
            subjects = ["전체"] + sorted(ref_df["과목"].dropna().unique().tolist())
            fc1, fc2 = st.columns(2)
            sel_subject = fc1.selectbox("📚 과목 선택", subjects, key="ref_filter_subj")
            df_f = ref_df.copy()
            if sel_subject != "전체":
                df_f = df_f[df_f["과목"] == sel_subject]
            activities = ["전체"] + sorted(df_f["활동시트명"].dropna().unique().tolist())
            sel_activity = fc2.selectbox("🎯 활동 선택", activities, key="ref_filter_act")
            if sel_activity != "전체":
                df_f = df_f[df_f["활동시트명"] == sel_activity]

            # 요약 수치 (필터 적용 후)
            total_submissions = len(df_f)
            unique_students   = df_f["학번"].nunique()
            unique_activities = df_f["활동시트명"].nunique()
            rc1, rc2, rc3 = st.columns(3)
            rc1.metric("총 제출 건수",   f"{total_submissions:,} 건")
            rc2.metric("참여 학생 수",   f"{unique_students:,} 명")
            rc3.metric("활동 종류 수",   f"{unique_activities:,} 가지")

            st.divider()

            # 과목·활동별 집계 테이블
            st.markdown("##### 교과별·활동별 성찰 제출 현황")
            agg = (
                df_f
                .groupby(["과목", "활동시트명"])
                .agg(
                    제출횟수=("학번", "count"),
                    고유학생수=("학번", "nunique"),
                )
                .reset_index()
                .sort_values(["과목", "제출횟수"], ascending=[True, False])
            )
            st.dataframe(
                agg,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "과목":       st.column_config.TextColumn("과목"),
                    "활동시트명": st.column_config.TextColumn("활동명"),
                    "제출횟수":   st.column_config.NumberColumn("제출 횟수"),
                    "고유학생수": st.column_config.NumberColumn("고유 학생 수"),
                },
            )

            st.divider()

            # 과목별 막대 차트
            if not agg.empty:
                fig_ref = px.bar(
                    agg,
                    x="활동시트명", y="고유학생수", color="과목",
                    title="활동별 고유 학생 성찰 제출 수",
                    labels={"활동시트명": "활동명", "고유학생수": "고유 학생 수"},
                    barmode="group",
                )
                fig_ref.update_layout(xaxis_tickangle=-30)
                _dark_fig(fig_ref)
                st.plotly_chart(fig_ref, use_container_width=True)

            st.markdown("##### 원본 데이터 (최근 100건)")
            st.dataframe(
                df_f.sort_values("제출시각", ascending=False)
                .head(100)[["제출시각", "과목", "활동시트명", "학번", "이름"]],
                use_container_width=True,
                hide_index=True,
            )

    st.divider()
    show_cols = ["방문시각", "과목필터", "사용자ID"]
    st.markdown("##### 원본 데이터 (최근 100건)")
    st.dataframe(
        df_u.sort_values("방문시각", ascending=False).head(100)[show_cols],
        use_container_width=True,
        hide_index=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 피드백 이메일 전송
_FEEDBACK_RECEIVER = "daesobi1@gmail.com"

def _send_feedback_email(
    feedback_type: str,
    student_id: str,
    student_name: str,
    reply_email: str,
    content: str,
) -> bool:
    """
    피드백 이메일을 _FEEDBACK_RECEIVER로 Gmail SMTP를 통해 전송합니다.
    .streamlit/secrets.toml 의 [email] 섹션에 sender / password 가 필요합니다.
    """
    try:
        email_secrets = st.secrets.get("email", {})
        sender_email: str = email_secrets.get("sender", "")
        sender_password: str = email_secrets.get("password", "")
    except Exception:
        sender_email = ""
        sender_password = ""

    if not sender_email or not sender_password:
        st.warning("이메일 설정이 구성되지 않았습니다. 관리자(선생님)에게 알려주세요.", icon="⚠️")
        return False

    # 헤더 인젝션 방지: 개행 문자 제거
    def _clean(s: str) -> str:
        return s.replace("\r", "").replace("\n", " ").strip()

    s_id    = _clean(student_id)
    s_name  = _clean(student_name)
    s_reply = _clean(reply_email)
    f_type  = _clean(feedback_type)
    now_str = datetime.now(_KST).strftime("%Y년 %m월 %d일 %H:%M")

    subject_line = f"[MathLab 피드백] {f_type} – {s_name}({s_id})"

    # HTML 이메일 본문 (내용은 XSS 방지를 위해 html.escape 처리)
    html_body = f"""
<html>
<body style="font-family:Arial,sans-serif; color:#333;">
  <h2 style="color:#6366f1;">📬 MathLab 학생 피드백</h2>
  <table border="1" cellpadding="8" cellspacing="0"
         style="border-collapse:collapse; min-width:400px;">
    <tr><th style="background:#f0f4ff; text-align:left; width:120px;">유형</th>
        <td>{_html.escape(f_type)}</td></tr>
    <tr><th style="background:#f0f4ff; text-align:left;">학번</th>
        <td>{_html.escape(s_id)}</td></tr>
    <tr><th style="background:#f0f4ff; text-align:left;">이름</th>
        <td>{_html.escape(s_name)}</td></tr>
    <tr><th style="background:#f0f4ff; text-align:left;">답변 이메일</th>
        <td>{_html.escape(s_reply) if s_reply else "(미입력)"}</td></tr>
    <tr><th style="background:#f0f4ff; text-align:left;">접수 시각</th>
        <td>{now_str}</td></tr>
  </table>
  <h3>내용</h3>
  <div style="background:#f9f9f9; border:1px solid #ddd; padding:12px; border-radius:6px;
              white-space:pre-wrap; line-height:1.6;">
{_html.escape(content)}
  </div>
  <p style="color:#888; font-size:0.85rem;">– MathLab 자동 발송 메일 –</p>
</body>
</html>
"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject_line
        msg["From"]    = sender_email
        msg["To"]      = _FEEDBACK_RECEIVER
        if s_reply:
            msg["Reply-To"] = s_reply
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, _FEEDBACK_RECEIVER, msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        st.error("이메일 인증에 실패했습니다. 관리자에게 알려주세요. (SMTP 앱 비밀번호 확인 필요)")
        return False
    except Exception as exc:
        st.error(f"이메일 전송 중 오류가 발생했습니다: {exc}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# 비밀번호 변경 뷰 (로그인한 일반 사용자)
def change_password_view():
    """로그인한 학생·일반인이 본인 비밀번호를 변경하는 페이지."""
    from auth_utils import change_own_password

    if st.button("← 홈으로", type="secondary", key="chpw_back_btn"):
        set_route("home"); _do_rerun()

    st.title("🔑 비밀번호 변경")
    st.caption("현재 비밀번호를 확인한 뒤 새 비밀번호로 변경합니다.")
    st.divider()

    user_id   = st.session_state.get("_user_id", "")
    user_type = st.session_state.get("_user_type", "")

    with st.form("change_pw_form", clear_on_submit=True):
        cur_pw  = st.text_input("현재 비밀번호 *", type="password")
        new_pw1 = st.text_input("새 비밀번호 *", type="password",
                                help="8자 이상, 숫자 1개 이상 포함")
        new_pw2 = st.text_input("새 비밀번호 확인 *", type="password")
        submitted = st.form_submit_button("변경하기", use_container_width=True,
                                          type="primary")

    if submitted:
        errs = []
        if not cur_pw:
            errs.append("현재 비밀번호를 입력하세요.")
        if new_pw1 != new_pw2:
            errs.append("새 비밀번호가 일치하지 않습니다.")
        from auth_utils import check_password_policy
        errs += check_password_policy(new_pw1)

        if errs:
            for e in errs:
                st.error(e)
        else:
            ok, msg = change_own_password(user_type, user_id, cur_pw, new_pw1)
            if ok:
                st.success("✅ 비밀번호가 변경되었습니다.")
            else:
                st.error(f"❌ {msg}")


# ─────────────────────────────────────────────────────────────────────────────
# 피드백/의견 접수 뷰
def feedback_view():
    """학생 의견 접수 페이지 (오류 신고 / 활동 건의)."""
    if st.button("← 홈으로", type="secondary", key="feedback_back_btn"):
        set_route("home"); _do_rerun()

    st.title("💬 의견 보내기")
    st.caption(
        "활동을 이용하다가 불편한 점이 있으시거나, 새로운 활동을 원하신다면 아래에 작성해 주세요. "
        "선생님께서 확인 후 답변드립니다."
    )
    st.divider()

    # 로그인 사용자 정보 자동 사용
    auto_id   = st.session_state.get("_user_id",   "")
    auto_name = st.session_state.get("_user_name", "")

    st.info(f"**{auto_name}** ({auto_id}) 님의 계정으로 접수됩니다.")

    # 피드백 유형 선택
    feedback_type = st.radio(
        "어떤 내용을 보내시겠어요?",
        ["🛠 활동 오류를 접수합니다", "💡 이런 활동도 만들어주세요"],
        horizontal=True,
        key="feedback_type_radio",
    )

    st.markdown("")  # 여백

    with st.form("feedback_form", clear_on_submit=True):
        reply_email = st.text_input(
            "답변받을 이메일 (선택)",
            placeholder="예: student@example.com",
            max_chars=100,
        )

        content = st.text_area(
            "내용 *",
            placeholder=(
                "오류 신고 예시: '확률과통계 > 이항분포 시뮬레이터에서 n=100 설정 시 화면이 멈춥니다.'\n"
                "활동 건의 예시: '정규분포 표준화 과정을 시각적으로 보여주는 활동이 있으면 좋겠습니다.'"
            ),
            height=220,
        )

        submitted = st.form_submit_button(
            "✉️ 보내기",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        errors: list[str] = []
        if reply_email.strip() and "@" not in reply_email:
            errors.append("이메일 주소 형식을 확인해 주세요.")
        if not content.strip():
            errors.append("내용을 입력해 주세요.")

        if errors:
            for err in errors:
                st.error(err, icon="❌")
        else:
            with st.spinner("전송 중입니다..."):
                email_ok = _send_feedback_email(
                    feedback_type=feedback_type,
                    student_id=auto_id,
                    student_name=auto_name,
                    reply_email=reply_email.strip(),
                    content=content.strip(),
                )
                sheet_ok = _save_feedback_to_sheet(
                    feedback_type=feedback_type,
                    student_id=auto_id,
                    student_name=auto_name,
                    reply_email=reply_email.strip(),
                    content=content.strip(),
                )
            if email_ok or sheet_ok:
                st.success(
                    "✅ 의견이 선생님께 전달되었습니다! 소중한 의견 감사합니다.",
                    icon="🎉",
                )


# ─────────────────────────────────────────────────────────────────────────────
# Footer
def _render_footer():
    st.markdown(
        """
        <style>
          .site-footer {
            margin-top: 1.5rem;
            padding: 0.75rem 1rem;
            border-top: 1px solid rgba(99,102,241,0.18);
            font-size: 0.82rem;
            color: rgba(255,255,255,0.35);
            text-align: center;
            line-height: 1.8;
          }
        </style>
        <div class="site-footer">
          © 2026 MathLab. All rights reserved. &nbsp;|&nbsp;
          개인정보책임자: 김대섭 교사 (휘문고등학교) &nbsp;|&nbsp; 문의: 02-500-9513
        </div>
        """,
        unsafe_allow_html=True,
    )
    _, _fc2, _ = st.columns([3, 2, 3])
    with _fc2:
        if st.button("📋 개인정보처리방침", key="_footer_privacy_btn", use_container_width=True):
            _privacy_policy_dialog()

# ─────────────────────────────────────────────────────────────────────────────
# 로컬 디버깅 패널
def _render_debug_sidebar():
    """로컬 개발 환경 전용 빠른 로그인 패널.
    .streamlit/secrets.toml 에  local_debug_mode = true  를 추가하면 활성화됩니다.
    """
    try:
        is_debug = bool(st.secrets.get("local_debug_mode", False))
    except Exception:
        is_debug = False
    if not is_debug:
        return

    _role_map = {
        "👤 (로그인 안함)": None,
        "🔧 관리자": {
            "_authenticated": True, "_user_type": "admin",
            "_user_id": "admin",    "_user_name": "관리자",
            "_dev_mode": True,       "_login_allowed_subjects": None,
            "_login_allowed_lessons": None,
        },
        "🎓 학생 (테스트)": {
            "_authenticated": True, "_user_type": "student",
            "_user_id": "202601001", "_user_name": "테스트학생",
            "_dev_mode": False,      "_login_allowed_subjects": None,
            "_login_allowed_lessons": None,
        },
        "👤 일반인 (테스트)": {
            "_authenticated": True, "_user_type": "general",
            "_user_id": "test_general", "_user_name": "테스트일반인",
            "_dev_mode": False,          "_login_allowed_subjects": set(),
            "_login_allowed_lessons": {"gifted": set()},
        },
    }

    with st.sidebar:
        st.markdown(
            "<div style='background:rgba(255,165,0,0.15);border:1px solid "
            "rgba(255,165,0,0.5);border-radius:8px;padding:0.4rem 0.7rem;"
            "margin:0.5rem 0 0.3rem;font-size:0.82rem;font-weight:700;'>🐛 LOCAL DEBUG</div>",
            unsafe_allow_html=True,
        )
        # 현재 로그인 상태 표시
        cur_type = st.session_state.get("_user_type", "")
        cur_name = st.session_state.get("_user_name", "")
        if st.session_state.get("_authenticated"):
            type_icon = {"admin": "🔧", "student": "🎓", "general": "👤"}.get(cur_type, "👤")
            st.caption(f"현재: {type_icon} {cur_name}")
        else:
            st.caption("현재: 비로그인")

        c1, c2 = st.columns([3, 1])
        with c1:
            sel = st.selectbox(
                "역할", list(_role_map.keys()),
                key="_dbg_role_sel", label_visibility="collapsed",
            )
        with c2:
            if st.button("적용", key="_dbg_apply", use_container_width=True):
                _clear_keys = [
                    "_authenticated", "_user_type", "_user_id", "_user_name",
                    "_dev_mode", "_login_allowed_subjects",
                    "_login_allowed_lessons", "_visit_logged",
                    "_sidebar_open",
                ]
                for k in _clear_keys:
                    st.session_state.pop(k, None)
                data = _role_map.get(sel)
                if data:
                    st.session_state.update(data)
                _do_rerun()
        st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# 메인
def main():
    # 로컬 디버깅 패널 (local_debug_mode = true 시 활성화)
    _render_debug_sidebar()

    # 주요 전환 후 페이드인
    if st.session_state.pop("_page_fade_in", False):
        st.markdown(_PAGE_FADE_IN_CSS, unsafe_allow_html=True)

    # sub-page에서의 라우트 이동 요청 처리
    if "_nav_to" in st.session_state:
        target = st.session_state.pop("_nav_to")
        set_route(target)
        _do_rerun()

    # ── 로그인 게이트 ──────────────────────────────────────────────────────────
    if not st.session_state.get("_authenticated", False):
        login_view()
        _render_footer()
        st.stop()
    # ──────────────────────────────────────────────────────────────────────────

    _refresh_current_user_permissions()
    _log_visit()   # 세션 최초 1회 방문 기록
    _inject_app_theme()  # 전체 앱 다크 테마 적용
    registry = discover_activities()
    view, subject, activity, unit = get_route()  # unit 포함

    # ── 커스텀 사이드바 레이아웃 ──────────────────────────────────────────────
    # 기본 Streamlit 사이드바 숨기기 (디버그 모드 제외)
    try:
        _is_local_debug = bool(st.secrets.get("local_debug_mode", False))
    except Exception:
        _is_local_debug = False
    if not _is_local_debug:
        st.markdown("""
        <style>
        section[data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"] { display: none !important; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    /* 페이지 전체 여백 */
    [data-testid="stMainBlockContainer"],
    [data-testid="stMainBlockContainer"] > .block-container,
    [data-testid="stMainBlockContainer"] > div {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 0.75rem !important;
        max-width: 100% !important;
    }
    /* nav/main 레이아웃: #__ml_nav__ 마커를 포함한 컬럼과 그 형제만 대상으로 지정 */
    /* 바깥 HorizontalBlock — nav 마커를 포함할 때만 gap 적용 */
    [data-testid="stHorizontalBlock"]:has(#__ml_nav__) {
        gap: 2rem !important;
        padding: 0 !important;
    }
    /* 커스텀 nav 열 */
    [data-testid="column"]:has(#__ml_nav__) {
        background: transparent !important;
        padding: 1rem 0.8rem 2rem 0.8rem !important;
        min-height: calc(100vh - 1.5rem) !important;
    }
    /* nav 열 내 버튼 — 폰트 압축 */
    [data-testid="column"]:has(#__ml_nav__) button {
        font-size: 0.79rem !important;
    }
    /* nav 열 내 expander 헤더 — 한 줄 말줄임표 */
    [data-testid="column"]:has(#__ml_nav__) [data-testid="stExpander"] summary p,
    [data-testid="column"]:has(#__ml_nav__) [data-testid="stExpander"] summary span {
        font-size: 0.79rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    /* 메인 콘텐츠 열 (nav 열의 인접 형제) */
    [data-testid="column"]:has(#__ml_nav__) + [data-testid="column"] {
        padding-left: 1.5rem !important;
        padding-right: 1rem !important;
    }
    /* 메인 열 내부 중첩 컬럼 리셋 — 외부 CSS 부작용 방지 */
    [data-testid="column"]:has(#__ml_nav__) + [data-testid="column"] [data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
    }
    [data-testid="column"]:has(#__ml_nav__) + [data-testid="column"] [data-testid="column"] {
        padding: 0 !important;
        min-height: 0 !important;
    }
    /* 햄버거 버튼 스타일 (사이드바 닫힘 시) */
    [data-testid="stMainBlockContainer"] > div > div > div:first-child button[kind="secondary"]:first-of-type {
        background: rgba(99,102,241,0.15) !important;
        border: 1px solid rgba(99,102,241,0.35) !important;
        color: rgba(255,255,255,0.85) !important;
        font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _sidebar_open = st.session_state.get("_sidebar_open", True)

    if _sidebar_open:
        # stApp 배경 자체를 2색으로 분할: 왼쪽(사이드바)=짙은 보라, 오른쪽(메인)=기본 navy
        # columns([1,5]) + padding 0.75rem×2 + gap 2rem → 분기점 = (100% - 3.5rem)/6 + 1.75rem
        st.markdown("""
        <style>
        .stApp {
            background-image:
                linear-gradient(to right,
                    #0d0626 calc((100% - 3.5rem) / 6 + 1.75rem),
                    #0f172a calc((100% - 3.5rem) / 6 + 1.75rem)
                ),
                linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
                linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px) !important;
            background-size: 100% 100%, 50px 50px, 50px 50px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        nav_col, main_col = st.columns([1, 5])
        with nav_col:
            st.markdown('<div id="__ml_nav__"></div>', unsafe_allow_html=True)
            sidebar_navigation(registry)
    else:
        if st.button("☰  메뉴", key="_hamburger_open_btn", help="메뉴 열기"):
            st.session_state["_sidebar_open"] = True
            _do_rerun()
        main_col = st.container()

    with main_col:
        if view == "home":
            home_view()
        elif view == "change_password":
            change_password_view()
        elif view == "feedback":
            feedback_view()
        elif view == "feedback_board":
            feedback_board_view()
        elif view == "visit_stats":
            visit_stats_view()
        elif view == "my_reflection":
            my_reflection_view()
        elif view == "subject" and subject == "gifted":
            gifted_subject_view()
        elif view == "subject" and subject in SUBJECTS:
            subject_index_view(subject, registry)
        elif view == "ot" and subject in SUBJECTS and _is_ot_mode() and subject in _OT_CANVA:
            ot_view(subject)
        elif view == "lessons" and subject in SUBJECTS:
            lessons_view(subject)
        elif view == "activity" and subject in SUBJECTS and activity:
            activity_view(subject, activity, registry, unit=unit)
        else:
            # 예외 시 홈으로
            set_route("home")
            _do_rerun()

        if view == "home":
            st.divider()
            st.markdown(
                """
                <div style="text-align:center; padding: 0.5rem 0 1rem;">
                  <div style="font-size:1.8rem;">💬</div>
                  <div style="font-size:1.1rem; font-weight:700; margin-bottom:0.3rem;">의견 · 오류 접수</div>
                  <div style="font-size:0.92rem; color:rgba(255,255,255,0.55); line-height:1.6;">
                    활동 중 오류를 발견하셨나요? 새로운 활동을 건의하고 싶으신가요?<br>
                    아래 버튼을 눌러 선생님께 직접 말씀해 주세요.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            _, _fb_col, _ = st.columns([3, 2, 3])
            with _fb_col:
                if st.button("✉️ 의견 · 오류 접수하기", key="home_feedback_btn",
                             use_container_width=True, type="secondary"):
                    set_route("feedback"); _do_rerun()

        _render_footer()

if __name__ == "__main__":
    main()
