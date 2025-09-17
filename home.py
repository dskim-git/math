import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Callable, List, Tuple

import streamlit as st
from utils import set_base_page, page_header, goto, get_route

# ------------ 기본 세팅 ------------
set_base_page(page_title="수학 시뮬레이션 허브", page_icon="🧮")

# 표시용 그룹 정렬 우선순위 (없는 그룹은 뒤로)
PREFERRED_GROUP_ORDER = ["공통수학", "미적분", "확률과통계", "기하학"]

# 디렉터리명 → 라우트 그룹 키 (URL용 슬러그)
GROUP_KEY_MAP = {
    "common_math": "common",
    "calculus": "calc",
    "prob_stats": "prob",
    "geometry": "geom",
}

# ------------ 동적 페이지 탐색 ------------
@st.cache_resource(show_spinner=False)
def discover_pages() -> Dict[str, Dict]:
    """
    sections/ 아래 모든 모듈 중 PAGE_META & render() 가 있는 파일을 자동 등록.
    route 키: '<group_key>/<file_stem>'
    반환값: {route: {'title','group','group_key','icon','fn'}}
    """
    pages: Dict[str, Dict] = {}
    base_pkg = "sections"

    # sections 패키지 import (없으면 에러)
    importlib.import_module(base_pkg)
    import sections  # type: ignore

    for mod in pkgutil.walk_packages(sections.__path__, sections.__name__ + "."):
        mod_name = mod.name
        # __init__ 제외 & 패키지 자체 제외
        if mod_name.endswith(".__init__") or mod.ispkg:
            continue
        try:
            m = importlib.import_module(mod_name)
        except Exception:
            # 문제가 있는 모듈은 건너뜀
            continue

        meta = getattr(m, "PAGE_META", None)
        fn: Callable = getattr(m, "render", None)
        if not (meta and callable(fn)):
            continue

        # 모듈 경로에서 그룹 키/파일 스템 추출 (sections.<dir>.<file>)
        parts = mod_name.split(".")
        if len(parts) < 3:
            continue
        dir_name = parts[1] if parts[0] == "sections" else parts[-2]
        file_stem = parts[-1]

        group_key = GROUP_KEY_MAP.get(dir_name, dir_name)
        route = meta.get("route", f"{group_key}/{file_stem}")

        pages[route] = {
            "title": meta.get("title", file_stem),
            "group": meta.get("group", "기타"),
            "group_key": group_key,
            "icon": meta.get("icon", "📄"),
            "fn": fn,
        }
    return pages

PAGES = discover_pages()

def _sorted_groups() -> List[str]:
    # 사용 중인 그룹 표시명 수집
    used = sorted({v["group"] for v in PAGES.values()})
    # 선호 순서대로 배치, 나머지는 알파벳순으로 뒤에
    ordered = [g for g in PREFERRED_GROUP_ORDER if g in used]
    tail = [g for g in used if g not in PREFERRED_GROUP_ORDER]
    return ordered + sorted(tail)

def sidebar_nav():
    st.sidebar.title("📚 카테고리")
    current = get_route(default="home")

    # Home 버튼
    if st.sidebar.button("🏠 Home으로", use_container_width=True):
        goto("home")

    # 그룹별 항목 수집
    groups: Dict[str, List[Tuple[str, str]]] = {}
    for route, meta in PAGES.items():
        groups.setdefault(meta["group"], []).append(
            (route, f'{meta["icon"]} {meta["title"]}')
        )

    # 그룹별 사이드바 (접힘/펼침)
    for g in _sorted_groups():
        items = groups.get(g, [])
        if not items:
            with st.sidebar.expander(f"📁 {g}", expanded=False):
                st.caption("아직 준비 중이에요.")
            continue

        expanded = any(current == r for r, _ in items)
        with st.sidebar.expander(f"📁 {g}", expanded=expanded):
            for route, label in items:
                if st.button(label, key=f"nav-{route}", use_container_width=True):
                    goto(route)

def render_home():
    page_header("수학 시뮬레이션 허브", "수업에 바로 쓰는 인터랙티브 실험실")

    st.markdown("""
    왼쪽 **카테고리**에서 폴더를 펼치면 하위 페이지가 보여요.  
    아래 **바로가기**는 최근 추가/자주 쓰는 항목 일부를 자동으로 노출합니다. 😄
    """)

    # 바로가기: 확률과통계 중 상위 6개 (있으면)
    target_group = "확률과통계"
    shortcuts = [(r, m) for r, m in PAGES.items() if m["group"] == target_group][:6]

    if shortcuts:
        st.subheader(f"🔖 {target_group} 바로가기")
        cols = st.columns(3)
        for i, (route, meta) in enumerate(shortcuts):
            label = f'{meta["icon"]} {meta["title"]}'
            if cols[i % 3].button(label, use_container_width=True, key=f"home-shortcut-{route}"):
                goto(route)

    with st.expander("📂 내 자료(CSV) 빠르게 불러오기/미리보기"):
        up = st.file_uploader("CSV 업로드", type=["csv"])
        if up is not None:
            import pandas as pd
            df = pd.read_csv(up)
            st.dataframe(df.head(50))
            st.session_state["__LAST_UPLOADED_DF__"] = df
            st.success("세션에 저장했어요. 다른 페이지에서도 사용 가능!")

# ---- 실행 흐름 ----
sidebar_nav()
route = get_route(default="home")

if route == "home":
    render_home()
elif route in PAGES:
    meta = PAGES[route]
    page_header(f'{meta["icon"]} {meta["title"]}', f'{meta["group"]} / {meta["title"]}')
    PAGES[route]["fn"]()
else:
    st.error("존재하지 않는 페이지 경로입니다. Home으로 이동합니다.")
    goto("home")
