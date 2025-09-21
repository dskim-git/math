# home.py
import streamlit as st
from pathlib import Path
import importlib.util
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any
import streamlit.components.v1 as components  # 임베드용

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

# ─────────────────────────────────────────────────────────────────────────────
# 전역 설정
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
    "etc": "기타",
}

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

# ─────────────────────────────────────────────────────────────────────────────
# 유틸: 동적 모듈 로딩
def load_module_from_path(py_path: Path):
    spec = importlib.util.spec_from_file_location(py_path.stem, py_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
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

# ─────────────────────────────────────────────────────────────────────────────
# 활동 자동 탐색
def discover_activities() -> Dict[str, List[Activity]]:
    registry: Dict[str, List[Activity]] = {k: [] for k in SUBJECTS.keys()}
    if not ACTIVITIES_ROOT.exists():
        return registry

    def add_from_dir(dir_path: Path, subject_key: str, slug_prefix: str = ""):
        for py_file in dir_path.glob("*.py"):
            name = py_file.name
            if name.startswith("_") or name == "__init__.py":
                continue
            module = load_module_from_path(py_file)
            if module is None:
                continue
            meta = getattr(module, "META", {})
            title = meta.get("title") or py_file.stem.replace("_", " ").title()
            description = meta.get("description") or "활동 소개가 아직 없습니다."
            render_fn = getattr(module, "render", None)
            order = int(meta.get("order", 10_000_000))
            if callable(render_fn):
                registry[subject_key].append(
                    Activity(
                        subject_key=subject_key,
                        slug=(slug_prefix + py_file.stem),  # 예: "fractal/sierpinski_chaos"
                        title=title,
                        description=description,
                        render=render_fn,
                        order=order,
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
        for subdir in subject_dir.iterdir():
            if not subdir.is_dir():
                continue
            if subdir.name in ("lessons", "__pycache__") or subdir.name.startswith("_"):
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
    # origin은 여기서 굳이 반환하지 않아도 되지만, 필요하면 꺼내 쓸 수 있음
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
def sidebar_navigation(registry: Dict[str, List[Activity]]):
    # ✅ 단원/수업 바로가기: 각 교과 expander 내에 '수업 열기' 버튼을 조건부로 추가
    st.sidebar.header("📂 교과별 페이지")
    for key, label in SUBJECTS.items():
        with st.sidebar.expander(f"{label}", expanded=False):
            # 교과 메인
            if st.button("교과 메인 열기", key=f"open_{key}_index", use_container_width=True):
                set_route("subject", subject=key)
                _do_rerun()

            # ✅ lessons 폴더가 있으면 '수업 열기' 노출
            if (ACTIVITIES_ROOT / key / "lessons" / "_units.py").exists():
                if st.button("수업 열기 (단원별 자료)", key=f"open_{key}_lessons", use_container_width=True):
                    set_route("lessons", subject=key)
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
        - **기타**: 프랙털 등 흥미 주제 모음
        """
    )
    st.subheader("교과로 이동")
    cols = st.columns(4)
    for i, (key, label) in enumerate(SUBJECTS.items()):
        with cols[i % 4]:
            if st.button(f"{label} 이동", use_container_width=True):
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

    # ▼ 활동 카드들
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

LESSON_HEADER_VISIBLE = False

def lessons_view(subject_key: str):
    """교과별 '수업(lessons)' 허브: (1) CURRICULUM 계층형 또는 (2) UNITS 평면형을 지원"""
    keep_scroll(key=f"{subject_key}/lessons", mount="sidebar")

    label = SUBJECTS.get(subject_key, subject_key)

    # 헤더는 기본 숨김(원하면 LESSON_HEADER_VISIBLE=True로)
    if LESSON_HEADER_VISIBLE:
        st.title(f"🔖 {label} 수업")
        st.caption("왼쪽 선택에서 단원을 고르면, 해당 단원의 수업 자료가 순서대로 나타납니다.")

    # ✅ 상단 네비게이션(제목 아래 고정)
    _lessons_top_nav(subject_key)

    curriculum = load_curriculum(subject_key)  # list or None
    units = load_units(subject_key)            # dict or {}

    if curriculum:
        # ── 계층형: 대단원 → 중단원 → 소단원 ─────────────────────────────
        def children(node): return node.get("children", []) if isinstance(node, dict) else []

        # URL의 unit 쿼리로 초기 선택 자동 세팅
        _, _, _, unit_qp = get_route()
        flag_key = f"_{subject_key}_lesson_idx_initialized"
        if unit_qp and st.session_state.get(flag_key) != unit_qp:
            maj_idx = mid_idx = min_idx = None
            for i, maj in enumerate(curriculum):
                if maj.get("key") == unit_qp:
                    maj_idx = i; break
                mids = children(maj)
                for j, mid in enumerate(mids):
                    if mid.get("key") == unit_qp:
                        maj_idx = i; mid_idx = j; break
                    mins = children(mid)
                    for k, mnr in enumerate(mins):
                        if mnr.get("key") == unit_qp:
                            maj_idx = i; mid_idx = j; min_idx = k; break
                    if min_idx is not None or (maj_idx is not None and mid_idx is not None):
                        break
                if maj_idx is not None and (mid_idx is None or min_idx is not None):
                    break

            if maj_idx is not None:
                st.session_state[f"_{subject_key}_major"] = maj_idx
                if mid_idx is not None:
                    st.session_state[f"_{subject_key}_mid"] = mid_idx
                else:
                    st.session_state.pop(f"_{subject_key}_mid", None)
                if min_idx is not None:
                    st.session_state[f"_{subject_key}_min"] = min_idx
                else:
                    st.session_state.pop(f"_{subject_key}_min", None)
                st.session_state[flag_key] = unit_qp

        # 사이드바 3단 선택
        with st.sidebar:
            st.subheader("📚 단원 선택")
            majors = curriculum
            maj_state_key = f"_{subject_key}_major"
            maj_idx = st.session_state.get(maj_state_key, 0)
            maj_idx = st.selectbox("대단원", range(len(majors)),
                                   format_func=lambda i: majors[i]["label"],
                                   key=maj_state_key)

            mids = children(majors[maj_idx])
            middle = None
            if mids:
                mid_state_key = f"_{subject_key}_mid"
                mid_idx = st.session_state.get(mid_state_key, 0)
                mid_idx = st.selectbox("중단원", range(len(mids)),
                                       format_func=lambda i: mids[i]["label"],
                                       key=mid_state_key)
                middle = mids[mid_idx]

            minor = None
            if middle:
                mins = children(middle)
                if mins:
                    min_state_key = f"_{subject_key}_min"
                    min_idx = st.session_state.get(min_state_key, 0)
                    min_idx = st.selectbox("소단원", range(len(mins)),
                                           format_func=lambda i: mins[i]["label"],
                                           key=min_state_key)
                    minor = mins[min_idx]

        # 렌더 노드(소 > 중 > 대)
        items_node = None
        for node in [minor, middle, majors[maj_idx]]:
            if isinstance(node, dict) and "items" in node:
                items_node = node; break

        if not items_node:
            st.info("이 단원에는 아직 자료(items)가 없습니다. `_units.py`의 해당 지점에 items를 추가해 주세요.")
            return

        st.subheader(items_node.get("label", "선택한 단원"))
        st.divider()

        # 아이템 렌더
        for i, item in enumerate(items_node.get("items", []), start=1):
            typ = item.get("type"); title = item.get("title", "")
            st.markdown(f"### {i}. {title}")

            if typ == "gslides":
                embed_iframe(item["src"], height=item.get("height", 480))
            elif typ == "gsheet":
                embed_iframe(item["src"], height=item.get("height", 700))
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
            elif typ == "activity":
                subj = item.get("subject"); slug = item.get("slug")
                if st.button(f"▶ 액티비티 열기: {title}", key=f"lesson_open_{subj}_{slug}", use_container_width=True):
                    back_key = (minor or middle or majors[maj_idx]).get("key")
                    # ✅ 원래 수업 과목(subject_key)을 origin으로 함께 전달
                    set_route("activity", subject=subj, activity=slug, unit=back_key, origin=subject_key)
                    _do_rerun()
            else:
                st.info("지원되지 않는 타입입니다. (gslides/gsheet/canva/url/activity)")

            st.divider()

        # ✅ 하단 네비 버튼은 제거됨 (상단만 사용)

    else:
        # ── 평면형 UNITS(기존 방식) ──
        if not units:
            st.info(f"`activities/{subject_key}/lessons/_units.py` 에 CURRICULUM 또는 UNITS를 정의해 주세요.")
            return

        view, subject, activity, unit_qp = get_route()
        unit_keys = list(units.keys())
        default_idx = 0 if unit_qp not in unit_keys else unit_keys.index(unit_qp)

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

        cur_key = unit_keys[default_idx]
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
            elif typ == "activity":
                subj = item.get("subject"); slug = item.get("slug")
                if st.button(f"▶ 액티비티 열기: {title}", key=f"lesson_open_{cur_key}_{slug}", use_container_width=True):
                    # ✅ UNITS 평면형에서도 origin=subject_key 전달
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
    registry = discover_activities()
    sidebar_navigation(registry)

    view, subject, activity, unit = get_route()  # unit 포함

    if view == "home":
        home_view()
    elif view == "subject" and subject in SUBJECTS:
        subject_index_view(subject, registry)
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
