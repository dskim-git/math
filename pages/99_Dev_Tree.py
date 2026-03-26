# pages/99_Dev_Tree.py
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Project Tree", layout="centered")

from theme_utils import inject_dark_theme, inject_hide_nav
inject_dark_theme()
inject_hide_nav()

# ── 커스텀 사이드바 ──────────────────────────────────────────────────────────
_nav_col, _main_col = st.columns([1, 5], gap="small")
with _nav_col:
    st.markdown('''<style>
    [data-testid="stMainBlockContainer"] {
        padding-left: 0 !important;
        padding-right: 0.5rem !important;
    }
    [data-testid="column"]:first-child {
        background: linear-gradient(180deg,rgba(6,8,22,0.99) 0%,rgba(4,8,20,0.99) 100%) !important;
        border-right: 2px solid rgba(99,102,241,0.35) !important;
        border-radius: 0 !important;
        min-height: 100vh !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.55) !important;
        padding: 1rem 0.6rem 2rem 0.8rem !important;
    }
    [data-testid="column"]:nth-child(2) {
        padding-left: 1rem !important;
    }
    [data-testid="column"]:first-child button {
        font-size: 0.79rem !important;
    }
    </style>''', unsafe_allow_html=True)
    if st.button("🏠 홈으로", key="_99_nav_home", use_container_width=True):
        st.switch_page("home.py")
    if st.session_state.get("_dev_mode", False):
        st.divider()
        st.caption("🔧 관리자 기능")
        if st.button("👥 회원관리", use_container_width=True, key="_99_nav_member"):
            st.switch_page("pages/97_회원관리.py")
        if st.button("📋 진도표 관리", use_container_width=True, key="_99_nav_schedule"):
            st.switch_page("pages/98_진도표.py")

with _main_col:
    # pages/ 아래에 이 파일이 있으니, 프로젝트 루트는 parents[1]
    ROOT = Path(__file__).resolve().parents[1]

    st.title("📁 Project Tree (copy & share)")

    depth = st.slider("표시할 깊이", min_value=1, max_value=6, value=3)
    skip_default = ".git,__pycache__,.mypy_cache,.pytest_cache,.streamlit/cache,venv,.venv,.ipynb_checkpoints"
    skip = st.text_input("제외할 폴더(콤마로 구분)", skip_default)
    skip_parts = {s.strip() for s in skip.split(",") if s.strip()}

    def allowed(p: Path) -> bool:
        return not any(part in skip_parts for part in p.parts)

    def build_tree(root: Path, max_depth: int) -> str:
        lines = []
        for p in sorted(root.rglob("*")):
            if not allowed(p):
                continue
            rel = p.relative_to(root)
            if len(rel.parts) > max_depth:
                continue
            indent = "    " * (len(rel.parts) - 1)
            name = rel.name + ("/" if p.is_dir() else "")
            lines.append(f"{indent}{name}")
        return "\n".join(lines)

    tree_text = build_tree(ROOT, depth)
    st.code(tree_text or "(비어 있음)", language="text")

    st.download_button("⬇️ tree.txt로 저장", data=tree_text, file_name="tree.txt")

    files = sum(1 for p in ROOT.rglob("*") if p.is_file() and allowed(p))
    dirs  = sum(1 for p in ROOT.rglob("*") if p.is_dir() and allowed(p))
    st.caption(f"요약: 폴더 {dirs}개, 파일 {files}개 (깊이 {depth})")
    st.caption("Tip: 이 텍스트를 여기 채팅에 붙여주시면, 계층형 네비 구조를 바로 짜 드릴게요.")
