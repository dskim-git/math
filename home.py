import streamlit as st
from pathlib import Path
import importlib.util
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any

try:
    from utils import keep_scroll
except Exception:
    import streamlit.components.v1 as components
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

# ---------- 전역 설정 ----------
st.set_page_config(
    page_title="수학 수업 시뮬레이션 허브",
    page_icon="🧮",
    layout="wide"
)

# 교과 카테고리 정의(폴더명 ↔ 표시명)
SUBJECTS = {
    "common": "공통수학",
    "calculus": "미적분학",
    "probability": "확률과통계",
    "geometry": "기하학",
}

# home.py와 같은 디렉터리 기준
ACTIVITIES_ROOT = Path(__file__).parent / "activities"

# ---------- 데이터 모델 ----------
@dataclass
class Activity:
    subject_key: str
    slug: str
    title: str
    description: str
    render: Callable[[], None]

# ---------- 유틸: 동적 모듈 로딩 ----------
def load_module_from_path(py_path: Path):
    spec = importlib.util.spec_from_file_location(py_path.stem, py_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module

# ---------- Streamlit 버전 호환 라우팅 유틸 ----------
def _qp_get() -> Dict[str, List[str]]:
    """
    Query params를 버전 상관없이 표준화된 dict[str, list[str]]로 반환.
    - 최신: st.query_params -> dict[str, str] 또는 dict[str, list[str]]
    - 구버전: st.experimental_get_query_params()
    """
    try:
        qp: Any = st.query_params  # 최신 API
        # st.query_params가 dict-like
        norm: Dict[str, List[str]] = {}
        for k, v in dict(qp).items():
            if isinstance(v, list):
                norm[k] = v
            else:
                norm[k] = [v]
        return norm
    except Exception:
        # 구버전 experimental API
        try:
            return st.experimental_get_query_params()  # type: ignore[attr-defined]
        except Exception:
            return {}

def _qp_set(params: Dict[str, Any]) -> None:
    """
    Query params 설정(버전 호환). 값은 str 또는 list[str] 허용.
    """
    # 모두 문자열/리스트 문자열로 normalize
    normalized = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, list):
            normalized[k] = [str(x) for x in v]
        else:
            normalized[k] = str(v)

    try:
        # 최신 API: 직접 할당/업데이트
        st.query_params.clear()
        st.query_params.update(normalized)
    except Exception:
        # 구버전 experimental API
        st.experimental_set_query_params(**normalized)  # type: ignore[attr-defined]

def _do_rerun():
    # 버전에 맞춰 rerun 호출
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()  # type: ignore[attr-defined]

# ---------- 활동 자동 탐색 ----------
def discover_activities() -> Dict[str, List[Activity]]:
    registry: Dict[str, List[Activity]] = {k: [] for k in SUBJECTS.keys()}
    if not ACTIVITIES_ROOT.exists():
        return registry

    for subject_dir in ACTIVITIES_ROOT.iterdir():
        if not subject_dir.is_dir():
            continue
        subject_key = subject_dir.name
        if subject_key not in SUBJECTS:
            continue

        for py_file in subject_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            module = load_module_from_path(py_file)
            if module is None:
                continue

            meta = getattr(module, "META", {})
            title = meta.get("title") or py_file.stem.replace("_", " ").title()
            description = meta.get("description") or "활동 소개가 아직 없습니다."
            render_fn = getattr(module, "render", None)

            if callable(render_fn):
                registry[subject_key].append(
                    Activity(
                        subject_key=subject_key,
                        slug=py_file.stem,
                        title=title,
                        description=description,
                        render=render_fn,
                    )
                )

        registry[subject_key].sort(key=lambda a: a.title)

    return registry

# ---------- 라우팅 ----------
# 구조: view=home|subject|activity  & subject=probability & activity=random_walk_demo
def get_route():
    qp = _qp_get()
    def first(key: str, default: Optional[str]=None) -> Optional[str]:
        vals = qp.get(key)
        if not vals:
            return default
        return vals[0]
    view = first("view", "home")
    subject = first("subject", None)
    activity = first("activity", None)
    return view, subject, activity

def set_route(view: str, subject: Optional[str] = None, activity: Optional[str] = None):
    params = {"view": view}
    if subject:
        params["subject"] = subject
    if activity:
        params["activity"] = activity
    _qp_set(params)

# ---------- 공통 UI ----------
def sidebar_navigation(registry: Dict[str, List[Activity]]):
    st.sidebar.header("📂 교과별 페이지")
    for key, label in SUBJECTS.items():
        with st.sidebar.expander(f"{label}", expanded=False):
            # 교과 메인
            if st.button("교과 메인 열기", key=f"open_{key}_index", use_container_width=True):
                set_route("subject", subject=key)
                _do_rerun()

            # 하위 활동
            acts = registry.get(key, [])
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

def home_view():
    st.title("🧮 수학 수업 시뮬레이션 허브")
    st.markdown(
        """
        이 웹앱은 **수학 수업에서 바로 활용**할 수 있는 시뮬레이션과 활동을 한 곳에 모은 허브입니다.  
        아래에서 교과를 고르고, 교과별 메인 페이지에서 구체 활동으로 들어가세요.

        - **공통수학**: 수와 연산, 함수 기초, 수열 등
        - **미적분학**: 극한/연속, 미분/적분의 핵심 개념 시각화
        - **확률과통계**: 난수, 분포, 추정·검정 체험형 시뮬
        - **기하학**: 도형 성질, 변환, 작도 아이디어
        """
    )
    st.subheader("교과로 이동")
    cols = st.columns(4)
    for i, (key, label) in enumerate(SUBJECTS.items()):
        with cols[i]:
            if st.button(f"{label} 이동", use_container_width=True):
                set_route("subject", subject=key)
                _do_rerun()

def subject_index_view(subject_key: str, registry: Dict[str, List[Activity]]):
    label = SUBJECTS.get(subject_key, subject_key)
    st.title(f"📘 {label} 메인")
    st.markdown("이 교과에 포함된 활동들을 한눈에 보고 바로 실행할 수 있습니다.")

    acts = registry.get(subject_key, [])
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

def activity_view(subject_key: str, slug: str, registry: Dict[str, List[Activity]]):
    acts = registry.get(subject_key, [])
    act = next((a for a in acts if a.slug == slug), None)
    if not act:
        st.error("해당 활동을 찾을 수 없습니다. 파일명이 바뀌었는지 확인하세요.")
        return

    cols = st.columns([1, 2, 1])
    with cols[0]:
        if st.button("← 교과 메인", type="secondary", use_container_width=True):
            set_route("subject", subject=subject_key); _do_rerun()
    with cols[2]:
        if st.button("🏠 홈", type="secondary", use_container_width=True):
            set_route("home"); _do_rerun()

    # ✅ 스크롤 유지 스크립트를 사이드바에 주입 → 본문에 '빈 공간' 생성 안 됨
    keep_scroll(key=f"{subject_key}/{slug}", mount="sidebar")

    # ⚠️ 여기에는 어떤 divider/빈 마크다운도 넣지 마세요 (여백 원인)
    act.render()



# ---------- 메인 ----------
def main():
    registry = discover_activities()
    sidebar_navigation(registry)

    view, subject, activity = get_route()
    if view == "home":
        home_view()
    elif view == "subject" and subject in SUBJECTS:
        subject_index_view(subject, registry)
    elif view == "activity" and subject in SUBJECTS and activity:
        activity_view(subject, activity, registry)
    else:
        # 예외 시 홈으로
        set_route("home")
        _do_rerun()

if __name__ == "__main__":
    main()
