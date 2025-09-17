# nav_helper.py
from __future__ import annotations
from pathlib import Path
import re
import streamlit as st

# 과목 정의: (폴더키, 레이블, 아이콘)
CATEGORY_INFO = [
    ("common", "공통수학", "📚"),
    ("calculus", "미적분학", "∫"),
    ("stats", "확률과통계", "🎲"),
    ("geometry", "기하학", "📐"),
]

BASE_DIR = Path(__file__).parent
SECTIONS_DIR = BASE_DIR / "sections"

def _slugify(name: str) -> str:
    name = re.sub(r"^\d+[_\-\s]*", "", name)  # 숫자 접두어 제거
    name = re.sub(r"[_\s]+", "-", name.strip())
    return name.lower()

def _humanize(name: str) -> str:
    name = re.sub(r"^\d+[_\-\s]*", "", name)
    name = name.replace("_", " ").replace("-", " ").strip()
    return name if name else "Untitled"

# ---- URL 경로(라우트) 헬퍼 ----
def category_route(category_key: str) -> str:
    return f"/{category_key}"

def activity_route(category_key: str, filename_stem: str) -> str:
    return f"/{category_key}/{_slugify(filename_stem)}"

# 활동 자동 탐색(라우트 포함)
def _discover_activities(category_key: str):
    folder = SECTIONS_DIR / category_key
    pages = []
    for fp in sorted(folder.glob("*.py")):
        if fp.name == "__init__.py":
            continue
        title = _humanize(fp.stem)
        url = activity_route(category_key, fp.stem)
        pages.append(st.Page(str(fp), title=title, icon="🔹", url_path=url))
    # 카테고리 메인
    main_path = folder / "__init__.py"
    label = next(lbl for k, lbl, _ in CATEGORY_INFO if k == category_key)
    main_page = st.Page(str(main_path), title=f"{label} 메인", icon="🗂️", url_path=category_route(category_key))
    return main_page, pages

def build_navigation():
    home = st.Page("home.py", title="Home", icon="🏠", url_path="/")
    sections = {"": [home]}
    for key, label, icon in CATEGORY_INFO:
        main_page, acts = _discover_activities(key)
        sections[f"{icon} {label}"] = [main_page, *acts]
    return st.navigation(sections)

def inject_sidebar():
    st.sidebar.markdown("### 교과별 탐색")
    for key, label, icon in CATEGORY_INFO:
        with st.sidebar.expander(f"{icon} {label}", expanded=False):
            # 메인으로
            st.page_link(category_route(key), label=f"{label} 메인")
            # 활동들
            folder = SECTIONS_DIR / key
            for fp in sorted(folder.glob("*.py")):
                if fp.name == "__init__.py":
                    continue
                st.page_link(
                    activity_route(key, fp.stem),
                    label=_humanize(fp.stem)
                )
