# nav_helper.py
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
import re
import streamlit as st

# 과목: (키, 라벨, 아이콘)
CATEGORY_INFO = [
    ("common",   "공통수학",   "📚"),
    ("calculus", "미적분학",   "∫"),
    ("stats",    "확률과통계", "🎲"),
    ("geometry", "기하학",     "📐"),
]

BASE_DIR = Path(__file__).parent.resolve()
SECTIONS_DIR = (BASE_DIR / "sections").resolve()

def _slugify(name: str) -> str:
    name = re.sub(r"^\d+[_\-\s]*", "", name)
    name = re.sub(r"[_\s]+", "-", name.strip())
    return name.lower()

def _humanize(name: str) -> str:
    name = re.sub(r"^\d+[_\-\s]*", "", name)
    return name.replace("_", " ").replace("-", " ").strip() or "Untitled"

@lru_cache(maxsize=1)
def _discover_all():
    """모든 과목의 메인/활동 Page 객체를 절대경로로 생성해 캐시."""
    data = {}
    for key, label, icon in CATEGORY_INFO:
        folder = (SECTIONS_DIR / key).resolve()
        folder.mkdir(parents=True, exist_ok=True)

        # 과목 메인 (__init__.py)
        main_fp = (folder / "__init__.py").resolve()
        main_page = st.Page(
            str(main_fp),
            title=f"{label} 메인",
            icon="🗂️",
            url_path=f"/{key}",
        )

        # 활동들 (*.py, __init__.py 제외)
        acts = []
        for fp in sorted(folder.glob("*.py")):
            if fp.name == "__init__.py":
                continue
            fp = fp.resolve()
            acts.append(
                st.Page(
                    str(fp),
                    title=_humanize(fp.stem),
                    icon="🔹",
                    url_path=f"/{key}/{_slugify(fp.stem)}",
                )
            )

        data[key] = (main_page, acts)
    return data

def category_main_page(key: str) -> st.Page:
    return _discover_all()[key][0]

def activity_pages(key: str):
    return _discover_all()[key][1]

def build_navigation():
    home_fp = (BASE_DIR / "home.py").resolve()
    home = st.Page(str(home_fp), title="Home", icon="🏠", url_path="/")

    sections = {"": [home]}
    for key, label, icon in CATEGORY_INFO:
        main_page, acts = _discover_all()[key]
        sections[f"{icon} {label}"] = [main_page, *acts]
    return st.navigation(sections)

def inject_sidebar():
    st.sidebar.markdown("### 교과별 탐색")
    for key, label, icon in CATEGORY_INFO:
        with st.sidebar.expander(f"{icon} {label}", expanded=False):
            st.page_link(category_main_page(key), label=f"{label} 메인")
            for p in activity_pages(key_
