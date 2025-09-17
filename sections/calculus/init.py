# sections/calculus/__init__.py
import streamlit as st
from pathlib import Path

st.title("∫ 미적분학 메인")
st.write("미적분 시뮬레이션 모음입니다. 아래에서 활동을 선택하세요.")

folder = Path(__file__).parent
for p in sorted(x for x in folder.glob("*.py") if x.name != "__init__.py"):
    name = p.stem
    name = name[name.find("_")+1:] if "_" in name else name
    st.page_link(str(p), label=f"🔹 {name.replace('_',' ').title()}", use_container_width=True)
