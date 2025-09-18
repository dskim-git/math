# home.py — 기존 구조 유지 + 'etc → topic → activity' 계층 지원
import streamlit as st
from pathlib import Path
import importlib.util
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any, Tuple

try:
    from utils import keep_scroll
except Exception:
    import streamlit.components.v1 as components
    def keep_scroll(key: str = "default", mount: str = "sidebar"):
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
st.set_page_config(page_title="수학 수업 시뮬레이션 허브", page_icon="🧮", layout="wide")

# 교과 카테고리 정의(폴더명 ↔ 표시명)
SUBJECTS = {
    "common": "공통수학",
    "calculus": "미적분학",
    "probability": "확률과통계",
    "geometry": "기하학",
    "etc": "기타",   # ✅ 'etc'는 토픽 단계가 1칸 더 있음
}

# (선택) 홈 카드 표시 순서
SUBJECT_ORDER = ["common", "calculus", "probability", "geometry", "etc"]

# 'etc' 토픽 라벨/아이콘 (원하면 여기만 수정)
ETC_TOPIC_LABELS: Dict[str, str] = {
    "fractal": "프랙털",
}
ETC_TOPIC_ICONS: Dict[str, str] = {
    "fractal": "🌀",
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
    # ✅ etc 토픽용 (일반 교과는 None)
    topic: Optional[str] = None

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
    try:
        qp: Any = st.query_params  # 최신 API
        norm: Dict[str, List[str]] = {}
        for k, v in dict(qp).items():
            norm[k] = v if isinstance(v, list) else [v]
        return norm
    except Exception:
        try:
            return st.experimental_get_query_params()  # type: ignore[attr-defined]
        except Exception:
            return {}

def _qp_set(params: Dict[str, Any]) -> None:
    normalized = {}
    for k, v in params.items():
        if v is None: continue
        normalized[k] = [str(x) for x in v] if isinstance(v, list) else str(v)
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

# ---------- 활동 자동 탐색 ----------
# 반환: (일반 교과 레지스트리, etc 토픽 레지스트리)
# - 일반 교과: Dict[subject_key, List[Activity]]
# - etc 토픽: Dict[topic_slug, List[Activity]]
def discover_activities() -> Tuple[Dict[str, List[Activity]], Dict[str, List[Activity]]]:
    normal_registry: Dict[str, List[Activity]] = {k: [] for k in SUBJECTS.keys()}
    etc_topics: Dict[str, List[Activity]] = {}
    if not ACTIVITIES_ROOT.exists():
        return normal_registry, etc_topics

    for subject_dir in ACTIVITIES_ROOT.iterdir():
        if not subject_dir.is_dir():
            continue
        subject_key = subject_dir.name
        if subject_key not in SUBJECTS:
            continue

        # ✅ 일반 교과: 바로 .py 스캔
        if subject_key != "etc":
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
                    normal_registry[subject_key].append(
                        Activity(subject_key=subject_key, slug=py_file.stem,
                                 title=title, description=description, render=render_fn)
                    )
            normal_registry[subject_key].sort(key=lambda a: a.title)
            continue

        # ✅ etc: 1단계 더 들어가 토픽(하위 폴더) 스캔
        for topic_dir in subject_dir.iterdir():
            if not topic_dir.is_dir():
                continue
            topic_slug = topic_dir.name
            etc_topics.setdefault(topic_slug, [])
            for py_file in topic_dir.glob("*.py"):
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
                    etc_topics[topic_slug].append(
                        Activity(subject_key="etc", slug=py_file.stem, title=title,
                                 description=description, render=render_fn, topic=topic_slug)
                    )
            etc_topics[topic_slug].sort(key=lambda a: a.title)

    # etc는 일반 레지스트리엔 비워둠(토픽 화면에서 보여줌)
    normal_registry["etc"] = []
    return normal_registry, etc_topics

# ---------- 라우팅 ----------
# 구조:
#   view = home | subject | topic | activity
#   subject = e.g. 'probability' or 'etc'
#   topic = (etc 전용) e.g. 'fractal'
#   activity = 파일 슬러그
def get_route():
    qp = _qp_get()
    def first(key: str, default: Optional[str] = None) -> Optional[str]:
        vals = qp.get(key)
        return default if not vals else vals[0]
    view = first("view", "home")
    subject = first("subject", None)
    topic = first("topic", None)
    activity = first("activity", None)
    return view, subject, topic, activity

def set_route(view: str, subject: Optional[str] = None,
              activity: Optional[str] = None, topic: Optional[str] = None):
    params = {"view": view}
    if subject: params["subject"] = subject
    if topic:   params["topic"] = topic
    if activity: params["activity"] = activity
    _qp_set(params)

# ---------- 공통 UI ----------
def sidebar_navigation(registry: Dict[str, List[Activity]], etc_topics: Dict[str, List[Activity]]):
    st.sidebar.header("📂 교과별 페이지")
    for key, label in SUBJECTS.items():
        with st.sidebar.expander(f"{label}", expanded=False):
            # 교과 메인
            if st.button("교과 메인 열기", key=f"open_{key}_index", use_container_width=True):
                set_route("subject", subject=key); _do_rerun()

            # 하위 목록
            if key != "etc":
                acts = registry.get(key, [])
                if not acts:
                    st.caption("아직 활동이 없습니다. 파일을 추가하면 자동 등록됩니다.")
                else:
                    for act in acts:
                        if st.button(f"• {act.title}", key=f"open_{key}_{act.slug}", use_container_width=True):
                            set_route("activity", subject=key, activity=act.slug); _do_rerun()
            else:
                # ✅ etc: 토픽 → 액티비티
                if not etc_topics:
                    st.caption("아직 등록된 토픽이 없습니다. activities/etc/<topic>/ 파일을 추가하세요.")
                else:
                    for topic_slug in sorted(etc_topics.keys()):
                        topic_label = ETC_TOPIC_LABELS.get(topic_slug, topic_slug)
                        icon = ETC_TOPIC_ICONS.get(topic_slug, "🧩")
                        with st.expander(f"{icon} {topic_label}", expanded=False):
                            if st.button("토픽 메인 열기", key=f"open_topic_{topic_slug}", use_container_width=True):
                                set_route("topic", subject="etc", topic=topic_slug); _do_rerun()
                            acts = etc_topics.get(topic_slug, [])
                            for act in acts:
                                if st.button(f"• {act.title}", key=f"open_etc_{topic_slug}_{act.slug}", use_container_width=True):
                                    set_route("activity", subject="etc", topic=topic_slug, activity=act.slug); _do_rerun()

    st.sidebar.divider()
    if st.button("🏠 홈으로", type="secondary", use_container_width=True):
        set_route("home"); _do_rerun()

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
    n_cols = min(4, max(1, len(SUBJECTS)))
    cols = st.columns(n_cols)
    for i, key in enumerate(SUBJECT_ORDER if SUBJECT_ORDER else list(SUBJECTS.keys())):
        label = SUBJECTS[key]
        with cols[i % n_cols]:
            if st.button(f"{label} 이동", use_container_width=True):
                set_route("subject", subject=key); _do_rerun()

def subject_index_view(subject_key: str, registry: Dict[str, List[Activity]],
                       etc_topics: Dict[str, List[Activity]]):
    label = SUBJECTS.get(subject_key, subject_key)
    if subject_key == "etc":
        # ✅ 기타는 '토픽 리스트'를 보여줌
        st.title(f"📘 {label} 메인")
        st.markdown("주제(토픽)를 먼저 선택하세요.")
        if not etc_topics:
            st.info("아직 등록된 토픽이 없습니다. `activities/etc/<topic>/` 폴더를 만들고 .py를 추가하세요.")
            return
        n_cols = 3
        cols = st.columns(n_cols)
        for i, topic_slug in enumerate(sorted(etc_topics.keys())):
            topic_label = ETC_TOPIC_LABELS.get(topic_slug, topic_slug)
            icon = ETC_TOPIC_ICONS.get(topic_slug, "🧩")
            with cols[i % n_cols]:
                st.markdown(f"### {icon} {topic_label}")
                if st.button("열기", key=f"open_topic_card_{topic_slug}", use_container_width=True):
                    set_route("topic", subject="etc", topic=topic_slug); _do_rerun()
        return

    # ✅ 일반 교과: 활동 리스트
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
                    set_route("activity", subject=subject_key, activity=act.slug); _do_rerun()
            with c2:
                st.code(f"{act.subject_key}/{act.slug}.py", language="text")

def topic_index_view(topic_slug: str, etc_topics: Dict[str, List[Activity]]):
    topic_label = ETC_TOPIC_LABELS.get(topic_slug, topic_slug)
    icon = ETC_TOPIC_ICONS.get(topic_slug, "🧩")

    cols = st.columns([1, 1])
    with cols[0]:
        if st.button("← 기타 메인", type="secondary", use_container_width=True):
            set_route("subject", subject="etc"); _do_rerun()
    with cols[1]:
        if st.button("🏠 홈", type="secondary", use_container_width=True):
            set_route("home"); _do_rerun()

    st.title(f"{icon} {topic_label}")
    acts = etc_topics.get(topic_slug, [])
    if not acts:
        st.info("이 토픽에는 아직 등록된 액티비티가 없습니다.")
        return
    for act in acts:
        with st.container(border=True):
            st.subheader(act.title)
            st.caption(act.description)
            c1, c2 = st.columns([1, 3])
            with c1:
                if st.button("열기", key=f"open_topic_{topic_slug}_{act.slug}_in_index", use_container_width=True):
                    set_route("activity", subject="etc", topic=topic_slug, activity=act.slug); _do_rerun()
            with c2:
                st.code(f"etc/{topic_slug}/{act.slug}.py", language="text")

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
    keep_scroll(key=f"{subject_key}/{slug}", mount="sidebar")
    act.render()

def activity_view_etc(topic_slug: str, slug: str, etc_topics: Dict[str, List[Activity]]):
    acts = etc_topics.get(topic_slug, [])
    act = next((a for a in acts if a.slug == slug), None)
    if not act:
        st.error("해당 활동을 찾을 수 없습니다. 파일명이 바뀌었는지 확인하세요.")
        return
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("← 토픽 메인", type="secondary", use_container_width=True):
            set_route("topic", subject="etc", topic=topic_slug); _do_rerun()
    with cols[1]:
        if st.button("← 기타 메인", type="secondary", use_container_width=True):
            set_route("subject", subject="etc"); _do_rerun()
    with cols[2]:
        if st.button("🏠 홈", type="secondary", use_container_width=True):
            set_route("home"); _do_rerun()
    keep_scroll(key=f"etc/{topic_slug}/{slug}", mount="sidebar")
    act.render()

# ---------- 메인 ----------
def main():
    registry, etc_topics = discover_activities()
    sidebar_navigation(registry, etc_topics)

    view, subject, topic, activity = get_route()
    if view == "home":
        home_view()
    elif view == "subject" and subject in SUBJECTS:
        subject_index_view(subject, registry, etc_topics)
    elif view == "topic" and subject == "etc" and topic:
        topic_index_view(topic, etc_topics)
    elif view == "activity" and subject in SUBJECTS and activity:
        if subject == "etc" and topic:
            activity_view_etc(topic, activity, etc_topics)
        else:
            activity_view(subject, activity, registry)
    else:
        set_route("home"); _do_rerun()

if __name__ == "__main__":
    main()
