# -*- coding: utf-8 -*-
# nav_helper.py (safe version)
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
    name = re.sub(r"^\d+[_\-\s]*", "", name)      # 01_, 02- 같은 접두 제거
    name = re.sub(r"[_\s]+", "-", name.strip())   # 공백/언더스코어 -> -
    return name.lower()

def _humanize(name: str) -> str:
    name = re.sub(r"^\d+[_\-\s]*", "", name)
    return (name.replace("_", " ").replace("-", " ").strip() or "Untitled")

@lru_cache(maxsize=1)
def _discover_all_pages():
    """
    모든 과목의 메인/활동을 절대경로로 Page 객체로 만들어 캐시.
    반환형: { key: (main_page: st.Page, [activity_pages: st.Page...]) }
    """
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

        # 활동 (*.py, __init__.py 제외)
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

def category_main_page(key: str):
    return _discover_all_pages()[key][0]

def activity_pages(key: str):
    return _discover_all_pages()[key][1]

def build_navigation():
    home_fp = (BASE_DIR / "home.py").resolve()
    home = st.Page(str(home_fp), title="Home", icon="🏠", url_path="/")

    sections = {"": [home]}
    pages_map = _discover_all_pages()
    for key, label, icon in CATEGORY_INFO:
        main_page, acts = pages_map[key]
        sections[f"{icon} {label}"] = [main_page, *acts]
    return st.navigation(sections)

def inject_sidebar():
    st.sidebar.markdown("### 교과별 탐색")
    pages_map = _discover_all_pages()
    for key, label, icon in CATEGORY_INFO:
        with st.sidebar.expander(f"{icon} {label}", expanded=False):
            st.page_link(category_main_page(key), label=f"{label} 메인")
            for p in pages_map[key][1]:
                st.page_link(p, label=p.title)
