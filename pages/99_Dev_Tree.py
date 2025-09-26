# pages/99_Dev_Tree.py
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Project Tree", layout="centered")
st.title("📁 Project Tree (copy & share)")

# pages/ 아래에 이 파일이 있으니, 프로젝트 루트는 parents[1]
ROOT = Path(__file__).resolve().parents[1]

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
dirs = sum(1 for p in ROOT.rglob("*") if p.is_dir() and allowed(p))
st.caption(f"요약: 폴더 {dirs}개, 파일 {files}개 (깊이 {depth})")
st.caption("Tip: 이 텍스트를 여기 채팅에 붙여주시면, 계층형 네비(상위 클릭 → 하위 펼침) 구조를 바로 짜 드릴게요.")
