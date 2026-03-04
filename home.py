# home.py
import streamlit as st
from pathlib import Path
import importlib.util
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any
import streamlit.components.v1 as components  # 임베드용
import urllib.parse
from functools import lru_cache

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
    layout="wide"
)

SHOW_MINI_IN_SIDEBAR = False

# 교과 카테고리 정의(폴더명 ↔ 표시명)
SUBJECTS = {
    "common": "공통수학",
    "calculus": "미적분학",
    "probability_new": "확률과통계",
    "probability": "확률과통계(이전 교육과정)",
    "geometry": "기하학",
    "etc": "기타",
}

# 일반 사용자에게 숨길 교과 키 (개발자 모드에서만 노출)
# URL에 ?dev=1 을 붙이면 개발자 모드가 활성화됩니다.
HIDDEN_SUBJECTS: set = {"probability"}

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
    """교과 메인에서 쓸 '수업 카드' 전용 스타일을 한 번만 주입."""
    if "_subject_styles" in st.session_state:
        return
    st.session_state["_subject_styles"] = True
    st.markdown(
        """
        <style>
          .lesson-card{
            background: linear-gradient(180deg, rgba(240,244,255,.9), rgba(235,248,255,.9));
            border: 1px solid rgba(0,90,200,.22);
            border-radius: 12px;
            padding: 14px 16px;
            margin: 0.25rem 0 1rem 0;
          }
          .lesson-card h4{ margin: 0 0 .35rem 0; font-weight: 700; }
          .lesson-card p{ margin: .15rem 0 .5rem 0; color: var(--secondary-text-color); }
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

def _is_dev_mode() -> bool:
    """관리자 모드 여부를 세션 상태에서 읽습니다."""
    return st.session_state.get("_dev_mode", False)

_ADMIN_PASSWORD = "1906"

# OT 자료 비밀 토큰 — URL에 ?ot=<이 값> 을 붙이면 해당 과목 OT 자료가 표시됩니다.
_OT_TOKEN = "mathot2026"
_OT_CANVA: Dict[str, str] = {
    "common":          "https://www.canva.com/design/DAHC4prloOs/iLjYVxFI-b-VKCWRB3rE9A/view?embed",
    "probability_new": "https://www.canva.com/design/DAHC5FC0x7g/wVBeRL2qrRPuWLC9BszvjQ/view?embed",
}

def _is_ot_mode() -> bool:
    """URL ?ot=토큰 이 있으면 세션에 기억하고 OT 모드를 유지합니다."""
    qp = _qp_get()
    if qp.get("ot", [""])[0] == _OT_TOKEN:
        st.session_state["_ot_mode"] = True
    return st.session_state.get("_ot_mode", False)

# 과목 필터 토큰 — URL에 ?class=<이 값> 을 붙이면 해당 과목만 표시됩니다.
_SUBJECT_TOKENS: Dict[str, str] = {
    "common1":   "common",           # 1학년 공통수학 전용
    "prob2":     "probability_new",  # 2학년 확률과통계 전용
}

def _get_subject_filter() -> Optional[str]:
    """URL ?class=토큰 이 있으면 세션에 기억하고 필터 과목 키를 반환합니다.
    관리자 모드에서는 항상 None(필터 없음)을 반환합니다."""
    if _is_dev_mode():
        return None
    qp = _qp_get()
    token = qp.get("class", [""])[0]
    if token in _SUBJECT_TOKENS:
        st.session_state["_subject_filter"] = _SUBJECT_TOKENS[token]
    return st.session_state.get("_subject_filter", None)

def _admin_mode_ui():
    """사이드바 하단에 관리자 모드 토글 UI를 렌더링합니다."""
    dev = _is_dev_mode()
    st.sidebar.divider()

    if dev:
        st.sidebar.caption("🔧 관리자 모드 활성화 중")
        if st.sidebar.button("🔓 일반 모드로 돌아가기", use_container_width=True, key="_admin_exit_btn"):
            st.session_state["_dev_mode"] = False
            st.session_state.pop("_show_pw_input", None)
            st.session_state.pop("_pw_error", None)
            _do_rerun()
        st.sidebar.page_link("pages/99_Dev_Tree.py", label="📁 Dev Tree (파일 구조 보기)", use_container_width=True)
    else:
        if st.session_state.get("_show_pw_input", False):
            pw = st.sidebar.text_input(
                "관리자 비밀번호", type="password", key="_admin_pw_input",
                placeholder="비밀번호 입력 후 Enter"
            )
            c1, c2 = st.sidebar.columns(2)
            with c1:
                if st.button("확인", key="_admin_pw_confirm", use_container_width=True):
                    if pw == _ADMIN_PASSWORD:
                        st.session_state["_dev_mode"] = True
                        st.session_state["_show_pw_input"] = False
                        st.session_state.pop("_pw_error", None)
                        _do_rerun()
                    else:
                        st.session_state["_pw_error"] = True
            with c2:
                if st.button("취소", key="_admin_pw_cancel", use_container_width=True):
                    st.session_state["_show_pw_input"] = False
                    st.session_state.pop("_pw_error", None)
                    _do_rerun()
            if st.session_state.get("_pw_error"):
                st.sidebar.error("비밀번호가 틀렸습니다.")
        else:
            if st.sidebar.button("🔐 관리자 모드", use_container_width=True, key="_admin_enter_btn"):
                st.session_state["_show_pw_input"] = True
                st.session_state.pop("_pw_error", None)
                _do_rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 활동 자동 탐색
def discover_activities() -> Dict[str, List[Activity]]:
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
    [data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"] nav
    { display: none !important; visibility: hidden !important; }
    </style>
    """, unsafe_allow_html=True)
    components.html("""
    <script>
    (function hideSidebarNav() {
        const SELECTORS = [
            '[data-testid="stSidebarNav"]',
            '[data-testid="stSidebarNavContainer"]',
            '[data-testid="stSidebarNavItems"]',
            '[data-testid="stSidebarNavLink"]',
            'section[data-testid="stSidebar"] nav',
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

def sidebar_navigation(registry: Dict[str, List[Activity]]):
    dev = _is_dev_mode()
    subject_filter = _get_subject_filter()  # None → 필터 없음
    _inject_sidebar_nav_visibility(dev)
    st.sidebar.header("📂 교과별 페이지")
    for key, label in SUBJECTS.items():
        if key in HIDDEN_SUBJECTS and not dev:
            continue
        if subject_filter and key != subject_filter:
            continue
        with st.sidebar.expander(f"{label}", expanded=False):
            # 교과 메인
            if st.button("교과 메인 열기", key=f"open_{key}_index", use_container_width=True):
                set_route("subject", subject=key)
                _do_rerun()

            # lessons 진입
            if (ACTIVITIES_ROOT / key / "lessons" / "_units.py").exists():
                if st.button("수업 열기 (단원별 자료)", key=f"open_{key}_lessons", use_container_width=True):
                    set_route("lessons", subject=key)
                    _do_rerun()

            # 활동 목록 (숨김 제외)
            acts_all = registry.get(key, [])
            acts = [a for a in acts_all if not a.hidden]
            if not acts:
                st.caption("아직 활동이 없습니다. 파일을 추가하면 자동 등록됩니다.")
            else:
                for act in acts:
                    if st.button(f"• {act.title}", key=f"open_{key}_{act.slug}", use_container_width=True):
                        set_route("activity", subject=key, activity=act.slug)
                        _do_rerun()

    st.sidebar.divider()
    if st.button("🏠 홈으로", type="secondary", use_container_width=True):
        set_route("home")
        _do_rerun()
    st.sidebar.link_button(
        "🤖 AI 튜터와 대화하기", 
        "https://copilotstudio.microsoft.com/environments/Default-62ae463a-9f12-4edf-8544-4f6ca3834524/bots/copilots_header_78f6d/webchat?__version__=2",
        use_container_width=True
    )
    _admin_mode_ui()

def _inject_home_styles():
    """홈 뷰의 CSS 스타일을 주입합니다."""
    st.markdown(
        """
        <style>
          /* 히어로 섹션 스타일 */
          .hero-container {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
            border-radius: 16px;
            padding: 2.5rem 2rem;
            margin-bottom: 2.5rem;
            text-align: center;
            border: 1px solid rgba(99, 102, 241, 0.2);
          }
          .hero-title {
            font-size: 3rem;
            font-weight: 800;
            margin: 0 0 0.75rem 0;
            background: linear-gradient(135deg, #6366f1, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }
          .hero-subtitle {
            font-size: 1.15rem;
            color: var(--secondary-text-color);
            line-height: 1.6;
            margin: 0;
          }
          
          /* 카드 스타일 */
          .subject-card {
            height: 100%;
          }
          .subject-card-icon {
            font-size: 3rem;
            margin-bottom: 0.75rem;
          }
          .subject-card-title {
            font-size: 1.35rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            color: var(--text-color);
          }
          .subject-card-desc {
            font-size: 0.95rem;
            color: var(--secondary-text-color);
            line-height: 1.5;
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
          <div class="hero-title">MathLab</div>
          <div class="hero-subtitle">
            수학 수업에서 활용할 수 있는 시뮬레이션과 활동을 한 곳에 모은 공간입니다.<br>
            원하는 교과를 선택하여 다양한 수학 활동을 체험해보세요.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 교과별 아이콘과 설명 데이터
    subject_data = {
        "common": {
            "icon": "🔢",
            "description": "수와 연산, 함수, 수열 등<br>수학의 기초를 탄탄하게 다집니다."
        },
        "calculus": {
            "icon": "📈",
            "description": "극한, 미분, 적분의 변화를<br>시각적으로 확인하고 이해합니다."
        },
        "probability_new": {
            "icon": "🎲",
            "description": "데이터 분포와 확률 시뮬레이션으로<br>통계적 추론 과정을 경험합니다."
        },
        "probability": {
            "icon": "🎲",
            "description": "[이전 교육과정] 확률과통계 수업 자료입니다.<br>개발자 모드에서만 표시됩니다."
        },
        "geometry": {
            "icon": "📐",
            "description": "평면과 공간 도형의 성질,<br>변환과 작도의 원리를 탐구합니다."
        },
        "etc": {
            "icon": "🧩",
            "description": "프랙털, 게임 이론 등<br>흥미로운 수학 주제들을 만납니다."
        }
    }
    
    # 3열 그리드 레이아웃으로 카드 배치
    dev = _is_dev_mode()
    subject_filter = _get_subject_filter()  # None → 필터 없음
    visible_subjects = [
        (k, v) for k, v in SUBJECTS.items()
        if (k not in HIDDEN_SUBJECTS or dev)
        and (not subject_filter or k == subject_filter)
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

            if curriculum:
                def ch(node: dict[str, Any]):  # 안전한 children 접근
                    return node.get("children", []) if isinstance(node, dict) else []

                maj_key = f"subj_{subject_key}_pick_major"
                mid_key = f"subj_{subject_key}_pick_mid"
                min_key = f"subj_{subject_key}_pick_min"

                cols = st.columns([2, 2, 2, 1], gap="small")

                # 대단원
                majors = curriculum
                with cols[0]:
                    st.selectbox(
                        "대단원",
                        options=range(len(majors)),
                        format_func=lambda i: majors[i]["label"],
                        key=maj_key,
                    )
                maj_idx = st.session_state.get(maj_key, 0)
                prev_maj = st.session_state.get(maj_key + "__prev")
                if prev_maj is None or prev_maj != maj_idx:
                    st.session_state[maj_key + "__prev"] = maj_idx
                    st.session_state[mid_key] = 0
                    st.session_state.pop(min_key, None)
                mids = ch(majors[maj_idx])

                # 중단원
                with cols[1]:
                    if mids:
                        st.selectbox(
                            "중단원",
                            options=range(len(mids)),
                            format_func=lambda i: mids[i]["label"],
                            key=mid_key,
                        )
                    else:
                        st.selectbox("중단원", options=[], key=mid_key, disabled=True, placeholder="(없음)")
                if mids:
                    mid_idx = st.session_state.get(mid_key, 0)
                    prev_mid = st.session_state.get(mid_key + "__prev")
                    if prev_mid is None or prev_mid != mid_idx:
                        st.session_state[mid_key + "__prev"] = mid_idx
                        st.session_state.pop(min_key, None)
                    mins = ch(mids[mid_idx])
                else:
                    mins = []

                # 소단원
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

    if curriculum:
        def children(node): return node.get("children", []) if isinstance(node, dict) else []

        # 사용자 변경 시 동기화 건너뛰기용 플래그
        skip_key = f"__skip_sync_{subject_key}"
        skip_sync = st.session_state.pop(skip_key, False)

        # URL → 세션 동기화 (사용자 변경이 아닌 경우에만)
        if unit_qp and not skip_sync:
            path = _find_curriculum_path(curriculum, unit_qp)
            maj_state_key = f"_{subject_key}_major"
            mid_state_key = f"_{subject_key}_mid"
            min_state_key = f"_{subject_key}_min"
            if path:
                maj_i, mid_i, min_i = path
                st.session_state[maj_state_key] = maj_i
                if mid_i is not None: st.session_state[mid_state_key] = mid_i
                else: st.session_state.pop(mid_state_key, None)
                if min_i is not None: st.session_state[min_state_key] = min_i
                else: st.session_state.pop(min_state_key, None)

        # ── 사이드바 선택 ──
        with st.sidebar:
            st.subheader("📚 단원 선택")

            def ch(node): return node.get("children", []) if isinstance(node, dict) else []

            majors = curriculum
            maj_key = f"_{subject_key}_major"
            mid_key = f"_{subject_key}_mid"
            min_key = f"_{subject_key}_min"

            # 사용자 변경 마크
            def _mark_user_change():
                st.session_state[skip_key] = True

            # 대단원
            st.session_state.setdefault(maj_key, 0)
            if st.session_state[maj_key] >= len(majors):
                st.session_state[maj_key] = 0

            def _on_major_change():
                st.session_state[mid_key] = 0
                st.session_state.pop(min_key, None)
                _mark_user_change()

            maj_idx = st.selectbox(
                "대단원",
                options=range(len(majors)),
                format_func=lambda i: majors[i]["label"],
                key=maj_key,
                on_change=_on_major_change,
            )

            # 중단원
            mids = ch(majors[maj_idx])
            middle = None
            if mids:
                st.session_state.setdefault(mid_key, 0)
                if st.session_state[mid_key] >= len(mids):
                    st.session_state[mid_key] = 0

                def _on_mid_change():
                    st.session_state.pop(min_key, None)
                    _mark_user_change()

                mid_idx = st.selectbox(
                    "중단원",
                    options=range(len(mids)),
                    format_func=lambda i: mids[i]["label"],
                    key=mid_key,
                    on_change=_on_mid_change,
                )
                middle = mids[mid_idx]
            else:
                st.session_state.pop(mid_key, None)
                st.session_state.pop(min_key, None)

            # 소단원
            minor = None
            if middle:
                mins = ch(middle)
                if mins:
                    st.session_state.setdefault(min_key, 0)
                    if st.session_state[min_key] >= len(mins):
                        st.session_state[min_key] = 0

                    def _on_min_change():
                        _mark_user_change()

                    min_idx = st.selectbox(
                        "소단원",
                        options=range(len(mins)),
                        format_func=lambda i: mins[i]["label"],
                        key=min_key,
                        on_change=_on_min_change,   # ← 추가
                    )
                    minor = mins[min_idx]
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
        st.session_state["_lesson_sel_idx"] = default_idx

        def _on_select():
            idx = st.session_state.get("_lesson_sel_idx", 0)
            set_route("lessons", subject=subject_key, unit=unit_keys[idx])
            _do_rerun()

        with st.sidebar:
            st.subheader("📚 단원 선택")
            st.selectbox("단원", options=range(len(unit_keys)),
                         format_func=lambda i: units[unit_keys[i]]["label"],
                         index=default_idx, key="_lesson_sel_idx",
                         on_change=_on_select)

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
# 메인
def main():
    # URL 파라미터를 가장 먼저 읽어 세션에 기록 (이후 set_route로 파라미터가 지워지기 전에)
    _is_ot_mode()
    _get_subject_filter()
    registry = discover_activities()
    sidebar_navigation(registry)

    view, subject, activity, unit = get_route()  # unit 포함

    if view == "home":
        home_view()
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

if __name__ == "__main__":
    main()
