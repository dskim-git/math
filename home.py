import streamlit as st
from pathlib import Path
import importlib.util
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

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

ACTIVITIES_ROOT = Path(__file__).parent / "activities"

# ---------- 데이터 모델 ----------
@dataclass
class Activity:
    subject_key: str           # 예: "probability"
    slug: str                  # 파일명 기준 slug (확장자 제외)
    title: str                 # UI에 표시할 제목
    description: str           # 간단 설명
    render: Callable[[], None] # Streamlit 렌더 함수

# ---------- 유틸: 동적 모듈 로딩 ----------
def load_module_from_path(py_path: Path):
    spec = importlib.util.spec_from_file_location(py_path.stem, py_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module

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
            # 미정의 폴더는 스킵(원하면 SUBJECTS에 추가)
            continue

        for py_file in subject_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue

            module = load_module_from_path(py_file)
            if module is None:
                continue

            # 활동 메타 정보: 각 파일에 META/ render 함수가 있으면 사용
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
            # render가 없으면 자동 등록하지 않음(안전장치)

        # 제목 가나다 순 정렬
        registry[subject_key].sort(key=lambda a: a.title)

    return registry

# ---------- 라우팅: query_params 사용 ----------
# 구조: ?view=home | subject | activity  & subject=probability & activity=random_walk_demo
def get_route():
    qp = st.query_params
    view = qp.get("view", ["home"])[0]
    subject = qp.get("subject", [None])[0]
    activity = qp.get("activity", [None])[0]
    return view, subject, activity

def set_route(view: str, subject: Optional[str] = None, activity: Optional[str] = None):
    params = {"view": view}
    if subject:
        params["subject"] = subject
    if activity:
        params["activity"] = activity
    st.query_params.clear()
    st.query_params.update(params)

# ---------- 공통 UI 컴포넌트 ----------
def sidebar_navigation(registry: Dict[str, List[Activity]]):
    st.sidebar.header("📂 교과별 페이지")
    # 상위(교과) 토글 → 하위(활동) 목록
    for key, label in SUBJECTS.items():
        with st.sidebar.expander(f"{label}", expanded=False):
            # 교과 메인 바로가기
            if st.button("교과 메인 열기", key=f"open_{key}_index"):
                set_route("subject", subject=key)
                st.rerun()

            # 하위 활동 버튼 리스트
            acts = registry.get(key, [])
            if not acts:
                st.caption("아직 활동이 없습니다. 파일을 추가하면 자동 등록됩니다.")
            else:
                for act in acts:
                    if st.button(f"• {act.title}", key=f"open_{key}_{act.slug}"):
                        set_route("activity", subject=key, activity=act.slug)
                        st.rerun()

    st.sidebar.divider()
    if st.button("🏠 홈으로", type="secondary"):
        set_route("home")
        st.rerun()

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
                st.rerun()

def subject_index_view(subject_key: str, registry: Dict[str, List[Activity]]):
    label = SUBJECTS.get(subject_key, subject_key)
    st.title(f"📘 {label} 메인")
    st.markdown("이 교과에 포함된 활동들을 한눈에 보고 바로 실행할 수 있습니다.")

    acts = registry.get(subject_key, [])
    if not acts:
        st.info("아직 등록된 활동이 없습니다. `activities/{}/` 폴더에 .py 파일을 추가하세요.".format(subject_key))
        return

    for act in acts:
        with st.container(border=True):
            st.subheader(act.title)
            st.caption(act.description)
            c1, c2 = st.columns([1, 3])
            with c1:
                if st.button("열기", key=f"open_{subject_key}_{act.slug}_in_index"):
                    set_route("activity", subject=subject_key, activity=act.slug)
                    st.rerun()
            with c2:
                st.code(f"{act.subject_key}/{act.slug}.py", language="text")

def activity_view(subject_key: str, slug: str, registry: Dict[str, List[Activity]]):
    acts = registry.get(subject_key, [])
    act = next((a for a in acts if a.slug == slug), None)
    if not act:
        st.error("해당 활동을 찾을 수 없습니다. 파일명이 바뀌었는지 확인하세요.")
        return

    # 상단 네비
    cols = st.columns([1, 2, 1])
    with cols[0]:
        if st.button("← 교과 메인", type="secondary"):
            set_route("subject", subject=subject_key)
            st.rerun()
    with cols[2]:
        if st.button("🏠 홈", type="secondary"):
            set_route("home")
            st.rerun()

    st.title(f"🔬 {SUBJECTS.get(subject_key, subject_key)} · {act.title}")
    st.caption(act.description)
    st.divider()

    # 실제 렌더
    act.render()

# ---------- 메인 실행 ----------
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
        st.rerun()

if __name__ == "__main__":
    main()
